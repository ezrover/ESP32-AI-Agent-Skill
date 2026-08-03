# Architecture Specification — PT Training App

Version 0.1. Companion to `01-product-requirements.md`; FR/NFR/CR references
point there.

---

## 1. System Overview

```mermaid
flowchart LR
    subgraph Production["Content Production (offline pipeline)"]
        FLOW[Google Flow / Veo\nvideo generation] --> EDIT[Edit & QC\nintro=10s, clean loop,\nlayout contract]
        EDIT --> MASTER[(Master MP4s)]
        PT[Credentialed PT\nreview & sign-off] --> EDIT
        PT --> RULES[Pose-rule configs\n+ cue scripts]
    end

    MASTER --> YT[YouTube Shorts channel\n(marketing only)]
    MASTER --> R2[(Cloudflare R2\nvideos + manifest)]
    RULES --> MANIFEST[Content manifest JSON]
    MANIFEST --> R2

    subgraph CF["Cloudflare (free tier)"]
        R2
        WORKER[Worker:\nmanifest endpoint,\ntelemetry ingest]
        D1[(D1: telemetry)]
        PAGES[Pages: site,\nprivacy policy]
        WORKER --> R2
        WORKER --> D1
    end

    subgraph App["Flutter App (iOS/Android)"]
        SYNC[Manifest sync +\nvideo cache (LRU)]
        SESSION[Session engine]
        PLAYER[Video player\n(segment/loop control)]
        POSE[Pose pipeline\nMediaPipe on-device]
        AUDIO[Audio cue engine]
        STORE[(Local store: profiles,\nplans, history — SQLite)]
        SYNC --> SESSION
        SESSION --> PLAYER
        SESSION --> POSE
        SESSION --> AUDIO
        SESSION --> STORE
    end

    WORKER -- manifest --> SYNC
    R2 -- video files --> SYNC
```

Design stance: **client-heavy, local-first, static backend.** The server side
is a content CDN plus a version endpoint; all product logic lives in the app.
This is what makes the Cloudflare free tier sufficient (NFR-4) and the privacy
story airtight (NFR-3).

## 2. Content Manifest (the central contract)

Single versioned JSON document, produced by the content pipeline, served via
Worker (`GET /manifest` with `ETag`; app sends `If-None-Match`). Everything the
app knows about content comes from here — no app release needed for new
exercises/routines.

```jsonc
{
  "schema_version": 1,
  "content_version": "2026.08.1",
  "intro_replay_days": 14,                  // FR-407 N
  "exercises": [{
    "id": "knee_wall_sit_v1",
    "name": "Wall Sit",
    "pain_groups": ["knee"],
    "level": "beginner",
    "equipment": "none",
    "mode": "time",                          // "reps" | "time"
    "video": {
      "url": "https://cdn.example.com/v/knee_wall_sit_v1.mp4",
      "sha256": "…",
      "bytes": 8123456,
      "intro_end_ms": 10000,                 // authoritative (CR-3)
      "loop_start_ms": 10000,
      "loop_end_ms": 32000
    },
    "defaults": { "sets": 3, "target_seconds": 30, "rest_seconds": 45 },
    "pose": {
      "tracking": "on",                      // "on" | "off" (FR-506)
      "required_visibility": ["hips", "knees", "ankles"],
      "rep_counter": null,                   // null for time mode
      "form_rules": [{
        "id": "back_against_wall",
        "signal": "trunk_vertical_angle",
        "op": "lte", "value": 15, "tolerance": 5,
        "severity": "coach",                 // "coach" | "safety"
        "cue": "cue_back_flat"
      }]
    },
    "cues": { "intro_skippable": true }
  }],
  "routines": [{
    "id": "knee_starter_a",
    "name": "Knee Relief — Starter A",
    "pain_group": "knee",
    "level": "beginner",
    "blocks": [{ "exercise_id": "knee_wall_sit_v1", "sets": 3,
                 "target_seconds": 30, "rest_seconds": 45 }]
  }],
  "programs": [{
    "pain_group": "knee", "level": "beginner",
    "weekly_default": { "mon": "knee_starter_a", "wed": "knee_starter_b",
                        "fri": "knee_starter_a" }
  }]
}
```

Rep-mode exercises define `rep_counter`:

```jsonc
"rep_counter": {
  "signal": "knee_flexion_angle",     // named signal from the signal library
  "down_below": 100, "up_above": 160, // degrees, with hysteresis built in
  "min_rep_ms": 1200, "max_rep_ms": 8000
}
```

**Signals are a fixed library in the app** (joint angles, alignment ratios,
distances computed from MediaPipe's 33 landmarks). The manifest composes them;
it cannot inject code. Adding a genuinely new signal type requires an app
release — accepted trade-off for safety and app-store compliance.

Manifest updates are atomic on-device: download full manifest → validate schema
+ referential integrity (every routine's exercise exists) → swap.

### 2.1 Change detection & permanent caching (FR-704/FR-706)

Videos are **content-addressed**: the R2 object key embeds the file's SHA-256
(e.g. `v/knee_wall_sit_v1-3fa9c2….mp4`), so any URL is immutable and served
with `Cache-Control: immutable, max-age=31536000`. Consequences:

- **On-device cache is permanent** — a cached file can never silently go
  stale, because a changed video is a *different URL*. No TTLs, no expiry
  timers, no per-video revalidation requests.
- **All change detection collapses into one request:** conditional
  `GET /manifest` with `If-None-Match` on launch. `304` → the entire content
  set is unchanged, zero further traffic. Manifest changed → diff cached
  hashes vs. manifest hashes; re-download only changed/new videos in the
  background; delete superseded files. This is the minimum possible
  request count on the Workers free tier (1 request/device/day of use).
- Pinning: videos referenced by any profile's current plan are exempt from
  eviction; the LRU cap only reclaims space from videos no longer referenced.

## 3. Cloudflare Deployment

| Service | Use | Free-tier relevance |
|---|---|---|
| R2 | Master MP4s + manifest object | 10 GB storage, zero egress — 40 videos ≈ 0.3 GB |
| Worker | `GET /manifest` (ETag/304), `POST /telemetry` (fire-and-forget), future signed URLs | 100k req/day → manifest checks for ~tens of k devices/day |
| D1 | Telemetry events (append-only) | 5 GB, 100k writes/day cap respected by client-side sampling |
| Pages | Marketing site, privacy policy, support page | unlimited static |

Custom domain on Cloudflare; R2 served through the Worker route (or R2 custom
domain) so cache headers (`immutable`, 1-year) apply. No authentication in v1;
if content gating is ever needed, the Worker mints time-limited signed URLs —
the app already fetches URLs from the manifest, so this is a drop-in change.

Deployment is `wrangler` via GitHub Actions: content repo push → validate
manifest schema → upload changed videos to R2 → publish manifest with new
`content_version`.

## 4. Mobile App Architecture (Flutter)

Layered, with the session engine as the heart:

```
lib/
  data/        # SQLite (drift) repos: profiles, plans, history, cache index
  content/     # manifest client, schema validation, video cache (LRU, checksums)
  session/     # SessionEngine state machine (the core)
  pose/        # camera + MediaPipe isolate, signal library, RepCounter, FormEvaluator
  playback/    # video controller wrapper: segment seek, seamless loop
  audio/       # cue engine: priority queue, throttling, bundled assets
  ui/          # screens: onboarding, profiles, plan editor, session, history
```

### 4.1 SessionEngine (state machine)

States: `idle → framing → intro_playing → exercising(set n) → resting →
… → summary`. Events come from three async sources — pose pipeline (rep
detected, form violation, visibility lost), playback (intro finished, loop
tick), and clock (timers). The engine is a pure reducer over these events
(easily unit-tested with scripted event streams, which is how rep-count logic
is validated in CI without a camera).

Key behaviors bound to requirements:
- On entering a block: consult profile's `exercise_last_seen` + session's
  `intros_played` → start playback at 0 or `intro_end_ms` (FR-407).
- `exercising`: playback loops `[loop_start_ms, loop_end_ms]`; RepCounter or
  timer drives progress; FormEvaluator posts throttled cues (FR-504).
- Visibility loss → `tracking_paused` sub-state: counting freezes, cue
  "step back into frame", manual +1 stays live (FR-505, FR-402).
- Camera permission denied or `pose.tracking == "off"` → engine runs the same
  states minus the pose source (FR-506).

### 4.2 Pose pipeline

- Camera frames → MediaPipe Pose Landmarker (Tasks API) on a dedicated
  isolate/platform thread; UI receives only derived events, never frames.
- Target ≥ 20 fps sustained (NFR-1); auto-degrade: full → lite model on
  thermal pressure; drop to every-other-frame before dropping the session.
- Signal library: pure functions `landmarks → scalar` (e.g.
  `knee_flexion_angle = angle(hip, knee, ankle)`), smoothed with a One Euro
  filter before thresholding to kill jitter-driven false reps.
- RepCounter: hysteresis state machine per §2 config. FormEvaluator: evaluates
  predicates once per N frames, debounces violations (must persist ≥ 1 s),
  emits cue events with severity.
- Hard rule: nothing derived from the camera is ever written to disk or
  network (NFR-3). Code-review enforced; no serialization code in `pose/`.

### 4.3 Playback

- `media_kit` (or `video_player` if sufficient) wrapper providing:
  `playSegment(from, to, {loop})` with pre-seek before play to hit the 300 ms
  seek budget (NFR-1); videos are always local files (FR-705), which makes
  precise seeking and looping reliable — another reason sessions never stream.
- Loop seam: seek-to-`loop_start_ms` on `loop_end_ms` tick; masters are
  authored to loop cleanly (CR-3) so a straight cut is acceptable.

### 4.4 Audio cue engine

- Bundled OGG/AAC assets, id-addressed (`cue_rep_12`, `cue_halfway`,
  `cue_back_flat`…), voice-matched to the avatar.
- Single-slot priority queue: safety > rep > timer; a lower-priority cue
  arriving while busy is dropped, not queued (FR-602). Every cue also emits a
  UI caption event (NFR-5).
- Audio session config: ducking, respects silent switch on iOS
  (`ambient`-style category with explicit user override), Android audio focus
  `AUDIOFOCUS_GAIN_TRANSIENT_MAY_DUCK`.

### 4.5 Local storage

SQLite via drift. Tables: `profiles`, `plans` (weekday → routine ref),
`routine_overrides` (per-profile edited copies, FR-303), `session_history`,
`exercise_last_seen`, `cache_index` (file, hash, bytes, last-used for LRU),
`settings`. All rows carry `profile_id` except cache (shared). Profile delete
= cascading delete (FR-203).

## 5. Content Production Pipeline

1. **Script** per exercise: intro narration (benefits + how-to, written to fit
   10 s), loop choreography, cue script, pose rules — drafted with, and
   signed off by, the credentialed PT (CR-5).
2. **Generate** with Google Flow: avatar clip (circular-frame region) +
   demonstration clip per the layout contract (CR-2). *Phase 0 validates Flow
   can do this; fallback is filmed human demo + Flow avatar for the intro
   circle only.*
3. **Assemble** (template project or ffmpeg script): enforce 1080×1920@30,
   intro exactly 10.0 s, loop trimmed to clean seam, loudness-normalized
   intro narration, silent loop segment (CR-4). Automated QC script checks
   duration, resolution, audio presence per segment, and that the avatar
   region + bottom band are respected (frame-difference heuristics).
4. **Publish:** upload master to R2 (content-addressed name), add manifest
   entry with measured `intro_end_ms`/loop bounds + rule config; CI validates
   schema and referential integrity; bump `content_version`. Upload same
   master to YouTube as a Short with templated title/description/UTM link.

## 6. Cross-Cutting Concerns

- **Privacy:** enumerated egress: manifest GET, R2 video GET, telemetry POST
  (anonymous install-id UUID, event name, timestamp), crash reports. Nothing
  else. Store privacy labels derived from this list (release criterion 5).
- **Failure modes:** manifest fetch fails → use cached manifest; video
  download fails mid-session-prep → retry with backoff, offer "skip this
  exercise"; corrupted cache file (hash mismatch) → evict + redownload; clock
  skew irrelevant (no server time dependence).
- **Observability:** client-side sampled telemetry (≤ 1 event batch/session)
  to stay inside D1/Worker free limits; Sentry (free tier) for crashes with
  PII scrubbing on.
- **Testing strategy:** session engine = pure reducer tests; pose signal
  library = golden-file tests (recorded landmark sequences → expected
  reps/violations) so rep accuracy (metric §6 in PRD) is regression-tested in
  CI without cameras; integration tests with prerecorded landmark streams;
  manual device matrix for thermal/fps (NFR-1, NFR-6).

## 7. Key Decisions & Alternatives (ADR summary)

| # | Decision | Alternative rejected | Why |
|---|---|---|---|
| A1 | Dual-host video: YouTube (marketing) + R2 (app origin) | Stream/cache from YouTube | YouTube ToS prohibits caching & player modification; R2 egress is free |
| A2 | Manifest `intro_end_ms` authoritative; 10 s as production convention | Hard-coded fixed intro length only | One mis-edited video would break skip forever; manifest is self-healing |
| A3 | On-device MediaPipe pose | Cloud vision API | Latency, privacy, free-tier cost; camera data must never leave device |
| A4 | Flutter single codebase | Native ×2 / React Native | Team size; camera+ML plugin maturity; identical overlay UI. RN acceptable if team is React-deep — decide in Phase 0 |
| A5 | Local-first, no accounts in v1 | Cloud profiles | Shared-tablet need is local; privacy posture; free tier headroom; sync deferred to Phase 4 |
| A6 | Declarative pose rules in manifest, fixed signal library in app | Downloadable code/models per exercise | Store compliance, safety review-ability, testability |
| A7 | Bundled recorded cue audio | On-device TTS | Zero latency, consistent avatar voice, offline |
| A8 | Sessions never stream; download-then-play | Progressive streaming | Reliable seek/loop, offline guarantee, simpler player |
