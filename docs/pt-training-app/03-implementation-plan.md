# Phased Implementation Plan — PT Training App

Version 0.1. Phases are gated: each ends with a go/no-go checkpoint whose exit
criteria are listed. FR/NFR/CR references → `01-product-requirements.md`;
architecture references → `02-architecture.md`.

Assumption: a small team (1–2 engineers, 1 content producer, contracted PT and
legal reviewer). Durations are calendar estimates at that staffing; adjust
proportionally.

---

## Phase 0 — De-risk (2–3 weeks) — *nothing else starts until this passes*

The two existential risks are (1) Google Flow's ability to produce
PT-approvable demonstration video under the layout contract, and (2) pose
tracking quality in real living rooms. Phase 0 attacks only those.

**Workstream A — Content pilot**
1. Define avatar persona + voice; build the shared **character reference set**
   (avatar + demonstrator) used by all image/video generation.
2. Stand up the **storyboard/keyframe A/B workflow** (grill Q3.4): per
   exercise, generate start/end pose keyframes with both Nano Banana Pro and
   OpenAI's image model from the same prompt; PT picks winners; log each A/B
   round (prompt, provider, winner, notes) in the content repo.
3. Produce **3 pilot exercises** end-to-end (script → storyboard/keyframe A/B
   → Flow frames-to-video → assembly → QC → R2 + YouTube unlisted): one
   rep-based (squat variant), one time-based (wall sit), one
   `pose_tracking: off` (floor stretch).
4. PT reviews the *generated motion* (keyframes are pre-approved by
   construction — the open question is Flow's in-between interpolation);
   verify Flow, Nano Banana Pro, and OpenAI image output licenses permit
   commercial use (grill Q8.3).

**Workstream B — Tech spike (throwaway code allowed)**
1. Flutter spike: camera → MediaPipe Pose Landmarker at ≥ 20 fps on Pixel 6a
   + iPhone SE 3; measure thermals over 20 min (NFR-1, NFR-6).
2. Rep counter prototype for the squat pilot: hysteresis state machine on
   knee-flexion angle; validate against human count on 10 recorded takes
   (target ≥ 90%).
3. Video spike: local MP4, `playSegment(intro_end_ms …)` seek < 300 ms,
   seamless loop check.
4. Confirm Flutter vs React Native decision (grill Q6.1) based on spike pain.

**Exit criteria (go/no-go):**
- PT signs off pilot videos **or** fallback (filmed demo + Flow avatar intro)
  is adopted and one fallback pilot passes review.
- ≥ 20 fps sustained pose tracking on both reference devices; ≥ 90% rep
  accuracy on the pilot exercise.
- Framework decision recorded as ADR.
- Product owner has confirmed/overridden the ASSUMED items in
  `00-grill-session.md` §10.

## Phase 1 — Foundations (4–5 weeks, parallel tracks)

**Track: App skeleton**
- Project scaffolding, CI (build, test, lint), device farm smoke tests.
- Local store (drift schemas §4.5), profiles (FR-201…204), onboarding +
  red-flag screening (FR-101…104) with placeholder copy for legal review.
- Manifest client + schema validation + atomic swap (FR-701); video cache
  with checksums, LRU, prefetch (FR-702…705); "manage downloads" screen.

**Track: Cloudflare backend**
- R2 buckets, Worker (`/manifest` with ETag, `/telemetry`), D1 schema, Pages
  site with privacy policy draft; wrangler CI deploy (§3).
- Content publish pipeline: manifest schema validator + R2 uploader in CI.

**Track: Content production ramp**
- Production template + automated QC script (architecture §5 step 4) hardened
  from pilots; keyframe A/B log tooling promoted from pilot scripts.
- Produce first pain group's exercises (knee: 10 exercises + 3 routines +
  starter program), including pose-rule configs and cue scripts with PT.
- Record cue audio library (FR-601) with the avatar voice.

**Exit criteria:** app installs, creates profiles, syncs manifest, downloads
and lists knee content offline; backend deployed on free tier; 10 knee
exercises published to R2 (YouTube uploads can lag).

## Phase 2 — Session Engine & Pose (5–6 weeks) — the core

- SessionEngine reducer + full state machine (§4.1) with scripted-event unit
  tests; plan/routine editor UI (FR-301…304).
- Playback wrapper: segment seek, loop, intro-skip logic (FR-406, FR-407).
- Pose pipeline productionization: isolate, signal library + One Euro
  filtering, RepCounter, FormEvaluator with throttling/debounce
  (FR-501…505); framing assistant (FR-502); degraded modes (FR-506).
- Audio cue engine with priority/ducking/captions (FR-601…603).
- Session summary + history (FR-408).
- **Validation harness:** record landmark streams for every shipped exercise
  (3 testers × 3 takes); golden-file regression tests; measure rep accuracy
  per exercise — any exercise < 90% gets its thresholds retuned or is demoted
  to `pose_tracking: off` before ship.

**Exit criteria:** complete knee routine end-to-end on both reference devices,
offline, with rep counting, form cues, intro-skip verified; accuracy ≥ 90% on
all tracked knee exercises; 20-min thermal soak passes.

## Phase 3 — Content Scale-out & Launch Hardening (4–6 weeks)

- Produce remaining pain groups (hip, lower back, shoulder): 30 exercises,
  9 routines, starter programs; PT sign-off each (CR-5, CR-6).
- Publish all 40 Shorts to the channel with SEO templates + UTM links
  (FR-801); channel art, about page with disclaimer copy.
- Legal review: disclaimers, red-flag copy, privacy policy, store listings
  (PRD §9); implement final copy.
- Accessibility pass (NFR-5); localization scaffolding only (strings
  externalized, English-only).
- Load test manifest + cold-download at 1k simulated devices (release
  criterion 4); free-tier quota alarming (Cloudflare notifications).
- Beta: TestFlight / Play internal → closed beta with 20–50 real users incl.
  ≥ 3 shared-tablet families; fix top issues; store submissions.

**Exit criteria = v1 release criteria (PRD §7).** Ship.

## Phase 4 — Post-launch (backlog, priority order)

1. Cloud backup/sync of profiles (revisits privacy posture — grill Q8.2;
   Workers paid tier likely).
2. More pain groups (neck, ankle/foot, wrist/elbow) — pure content-pipeline
   work, no app release needed (§2).
3. Adaptive progression (PT-authored progression ladders, still no
   algorithmic prescription).
4. Apple Health / Google Fit session export (opt-in).
5. Localization; tablet-optimized side-by-side session layout.
6. Monetization exploration (subscription for premium programs) — requires
   entitlements + likely paid Cloudflare tier.

## Risk Register (top 5, live)

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Flow's in-between motion interpolates joints badly despite approved keyframes | Med | High | Storyboard/keyframe A/B workflow controls poses pre-render; Phase 0 gate validates motion; filmed-demo fallback keeps everything else intact |
| No credentialed PT secured | Med | High (blocks all content) | Contract before Phase 1; content budget line item |
| Rep accuracy < 90% on some exercises in real homes (lighting, clothing, camera angle) | Med | Med | Framing assistant, confidence gating, manual +1 fallback, demote to timer mode per exercise |
| iOS MediaPipe/Flutter integration friction | Med | Med | Phase 0 spike; MoveNet/TFLite fallback (A3 alt) |
| Free-tier cliffs at unexpected growth | Low | Low-Med | Quota alarms; $5 Workers paid tier is the pressure valve; architecture already minimizes requests |

## Dependency Summary (external)

- Credentialed PT (content author/reviewer) — needed from Phase 0.
- Google Flow + Nano Banana Pro + OpenAI image model access, with
  commercial-use license confirmation for all three — Phase 0.
- Apple/Google developer accounts — Phase 1.
- Legal reviewer (wellness positioning + privacy) — Phase 3, engaged earlier
  for copy guidelines.
- Cloudflare account with R2 enabled (payment card on file even for free
  tier) — Phase 1.
