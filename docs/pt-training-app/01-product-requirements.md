# Product Requirements Document — PT Training App ("the App") + YouTube Channel

Version 0.1 — derived from `00-grill-session.md`. Requirement IDs are stable;
cite them in issues/PRs. Decisions marked ASSUMED in the grill session are
treated as accepted here until overridden.

---

## 1. Vision

A mobile app that gives people with common musculoskeletal pain (knees, hips,
lower back, shoulders) safe, evidence-based exercise routines they can follow at
home — with a virtual trainer avatar teaching each movement, and the phone's
front camera acting as a form coach: counting reps, running timers, and giving
spoken form corrections in real time. A companion YouTube Shorts channel
publishes every exercise video for discovery and credibility.

**Positioning (binding):** general wellness product. The App never diagnoses,
treats, or claims to cure any condition. See PRD §9.

## 2. Personas

- **P1 "Maya", 52** — recurring lower-back and hip stiffness, desk job, owns a
  phone, wants guided 15-minute daily routines and reassurance her form is OK.
- **P2 "Sam", 34** — runner with knee pain flare-ups, wants targeted routines
  and to skip instructions he's already heard.
- **P3 "The Rivera family"** — shared kitchen tablet; three adults with
  different pain areas; each needs their own profile, plan, and history.

## 3. Functional Requirements

### 3.1 Onboarding & Problem Selection

- **FR-101** First launch shows a medical disclaimer + red-flag screening
  (numbness/tingling, recent trauma/surgery, chest pain, unexplained weight
  loss). Any red flag → hard stop screen advising professional care; the app
  does not proceed to routine creation for that profile until re-screened.
- **FR-102** User selects one or more **pain groups**: knee, hip, lower back,
  shoulder (v1 set; extensible via manifest).
- **FR-103** User selects pain severity (0–10), fitness level
  (beginner/intermediate/active), and available equipment (none / band /
  light dumbbells).
- **FR-104** No free-text symptom input anywhere in v1.

### 3.2 Profiles (shared-device support)

- **FR-201** Up to 8 device-local profiles: display name, avatar color, age
  gate ("I am 13 or older"), pain-group selections, plan, history, settings.
  No passwords, no cloud account in v1.
- **FR-202** Profile picker on cold launch; one-tap profile switcher on home.
- **FR-203** Deleting a profile erases all its data on device (with confirm).
- **FR-204** All session state (intro-played flags, in-progress workout) is
  profile-scoped.

### 3.3 Routines & Plans

- **FR-301** From the selected pain group(s), the app lists **evidence-based
  routines** (from the content manifest, composed of KB-traceable exercises
  per CR-5) matching fitness level and equipment.
- **FR-302** User assembles a **weekly plan**: assign a routine (or rest) to
  each weekday. A starter plan is pre-filled from the manifest's recommended
  program for the pain group.
- **FR-303** Routine editing: reorder exercise blocks; swap an exercise with
  another from the same pain group's approved list; edit sets, target
  reps/duration, rest length; remove/add blocks. Edits are per-profile copies;
  library routines stay pristine.
- **FR-304** Plans and routines are editable at any time; changes take effect
  next session.

### 3.4 Workout Session

- **FR-401** A session runs a routine as a sequence: per block →
  [intro video (conditional, FR-407)] → sets of exercise with video loop →
  rest countdown → next block. Progress bar shows position in routine.
- **FR-402** **Rep mode:** the app counts reps via pose detection (FR-501)
  toward the block's target, announcing each rep aloud. Manual "+1" tap
  fallback is always visible for when tracking is off/unreliable.
- **FR-403** **Time mode:** countdown timer with spoken milestones (start,
  halfway, 5-4-3-2-1) for stretches/holds.
- **FR-404** Rest periods: countdown with spoken 5-second warning; skippable.
- **FR-405** Pause/resume/abandon at any time; abandoning saves partial
  history.
- **FR-406** Video playback: the exercise-loop segment loops seamlessly for
  the duration of the set. The avatar (burned into the video, circular frame
  top-left) remains visible; app overlays (timer, rep count, form cues) render
  only in the bottom 20% band reserved by the video layout contract.
- **FR-407 Intro-skip logic:** play the intro segment (video start →
  `intro_end_ms`) only on the profile's first encounter of that exercise in
  the current session, or if the profile hasn't performed it in ≥ N days
  (manifest default 14). Otherwise start playback at `intro_end_ms`.
  Per-profile "always skip intros" setting; "replay instructions" button in
  session UI.
- **FR-408** Session summary screen: exercises completed, reps/durations,
  form-cue counts; stored in profile history. History view shows per-week
  adherence.

### 3.5 Pose Evaluation (machine vision)

- **FR-501** On-device pose estimation from the front camera; **no camera
  frame or landmark data is ever stored or transmitted** (binding privacy
  commitment).
- **FR-502** Framing assistant before tracked exercises: live skeleton
  preview, target silhouette, green in-frame confirmation; per-exercise
  required-visibility set from manifest.
- **FR-503** Rep counting via per-exercise state machine (angle signal,
  up/down thresholds, hysteresis, min rep duration) defined in the manifest's
  pose-rule config — no exercise-specific logic hardcoded in the app.
- **FR-504** Form rules: up to 4 predicates per exercise (joint-angle /
  alignment with tolerances). Violations trigger spoken coaching cues,
  throttled to ≤ 1 cue per 6 s, positive phrasing, safety cues prioritized.
- **FR-505** Confidence gating: when landmark visibility drops, counting
  pauses and the app says "step back into frame"; it never guesses reps.
- **FR-506** Exercises flagged `pose_tracking: "off"` in the manifest run in
  timer/manual mode with no camera. Camera permission denial degrades the
  whole app to this mode — everything still works.

### 3.6 Audio

- **FR-601** Pre-recorded voice cue library (bundled): numbers, countdowns,
  standard coaching phrases; voice matched to the avatar's voice.
- **FR-602** Cue priority: safety/form > rep count > timer. Never queue more
  than one pending cue; drop stale ones.
- **FR-603** Respects device silent switch/volume; ducks (not stops) the
  user's background music; all cues have on-screen text equivalents
  (accessibility).

### 3.7 Content Delivery & Caching

- **FR-701** App fetches the versioned content manifest from the Cloudflare
  Worker on launch when online; applies updates atomically (a routine never
  references a missing exercise).
- **FR-702** Videos download from Cloudflare R2 (never from YouTube), verified
  by checksum from the manifest.
- **FR-703** Prefetch: after a plan is created/edited, videos for its routines
  download in the background (Wi-Fi by default; cellular opt-in).
- **FR-704** Cached videos are **permanent — no time-based expiration**. A
  video is re-downloaded only when change detection (FR-706) shows it changed.
  Videos referenced by the profile's current plans are pinned; only videos
  from removed routines are eligible for LRU eviction under the disk-space cap
  (default 1 GB, user-adjustable; "manage downloads" screen). A fully cached
  routine is fully usable offline.
- **FR-705** If a needed video is not cached at session start, show a blocking
  "preparing your workout" download step — sessions never stream.
- **FR-706 Change detection:** performed via the manifest only — one
  conditional `GET /manifest` (`If-None-Match`) per launch when online; `304`
  means no further requests. When the manifest changes, videos whose hash
  differs from the cached copy are re-downloaded in the background and stale
  files deleted. The app never polls individual video URLs for freshness.

### 3.8 YouTube Channel (companion, not a runtime dependency)

- **FR-801** Every exercise master video is published as a portrait YouTube
  Short (intro + loop, full narration) with SEO title/description linking to
  the app.
- **FR-802** The app may deep-link to the channel (e.g. "watch more on
  YouTube") but never embeds or streams YouTube content inside the workout
  flow.

## 4. Content Requirements (production side)

- **CR-1** Video master: 1080×1920 @30 fps, H.264/AAC, MP4.
- **CR-2** Layout contract: avatar in circular frame, center (18% W, 12% H),
  diameter 28% W, reserved region; bottom 20% band free of burned-in text.
- **CR-3** Intro segment exactly 10.0 s (convention) **and** accurate
  `intro_end_ms` recorded in the manifest (authoritative). Exercise segment
  15–30 s, clean loop (matching first/last pose).
- **CR-4** Exercise-loop segment carries no narration audio.
- **CR-5** Every exercise ships with: video, pose-rule config, cue script,
  metadata (name, pain groups, equipment, level, default sets/reps/tempo) —
  and must trace to a production-eligible entry in the exercise knowledge
  base (`knowledge-base/`): corroborated by ≥ 2 independent authoritative
  sources (≥ 1 clinical/professional tier), with video script, form cues,
  pose rules, and dosage derived from that entry's fields. No exercise ships
  without a KB entry; when sources disagree, the more conservative clinical
  guidance wins.
- **CR-6** v1 library: 40 exercises, 12 routines, 4 pain-group starter
  programs.

## 5. Non-Functional Requirements

- **NFR-1 Performance:** pose pipeline sustains ≥ 20 fps on a 2021 mid-range
  device (e.g. Pixel 6a / iPhone SE 3); rep announcement latency ≤ 500 ms
  after rep completion; video seek-to-`intro_end_ms` starts within 300 ms.
- **NFR-2 Offline:** all core flows (profiles, plans, cached workouts,
  history) work with zero connectivity.
- **NFR-3 Privacy:** no camera/pose data stored or transmitted; v1 transmits
  nothing but anonymous crash + minimal usage telemetry (opt-out shown at
  onboarding); store privacy labels match reality.
- **NFR-4 Cost:** steady-state infrastructure runs on Cloudflare free tier
  (Workers 100k req/day, R2 10 GB / zero egress) up to ~10k active devices;
  design must not require paid tier before that scale.
- **NFR-5 Accessibility:** all audio cues mirrored as text; dynamic type
  support; color-contrast AA; workout usable without camera (FR-506).
- **NFR-6 Battery/thermal:** a 20-minute tracked session must not thermally
  throttle a mid-range device into < 15 fps pose tracking; camera pipeline
  released immediately for untracked exercises.
- **NFR-7 App size:** initial install ≤ 150 MB (videos are downloads, not
  bundle assets; cue library bundled).

## 6. Success Metrics (v1)

- Activation: ≥ 60% of installs complete onboarding and create a plan.
- Engagement: median ≥ 2 sessions/week per active profile in week 4.
- Session completion rate ≥ 75%.
- Rep-count accuracy ≥ 90% vs. human count on the 40-exercise validation set
  (measured in Phase 2 testing, not from user data).
- Crash-free sessions ≥ 99.5%.
- Channel: ≥ 40 Shorts published at launch; CTR from channel to store links
  tracked via UTM.

## 7. Release Criteria (v1 ship gate)

1. All 40 exercises KB-traceable per CR-5 and passing rep-accuracy validation.
2. FR-101 screening + disclaimers legally reviewed.
3. Offline session on airplane mode passes full regression.
4. Free-tier load test: manifest + cold-download path at 1k simulated devices.
5. Store privacy labels audited against actual network traffic (must show no
   health data collection).

## 8. Out of Scope (v1)

As enumerated in grill session §9: no clinical/post-op protocols, no
algorithmic prescription, no cloud accounts/sync, no wearables/health-platform
export, no payments, no web app, no non-English localization, no in-app
YouTube playback.

## 9. Disclaimers & Positioning (binding copy constraints)

- Onboarding, store listings, and the YouTube channel "About" carry: "This app
  provides general wellness and fitness content and is not medical advice,
  diagnosis, or treatment. Consult a healthcare professional before starting
  any exercise program, and stop if you feel pain."
- Prohibited vocabulary in all surfaces: diagnose, treat, cure, therapy for
  [condition], patient. Permitted: discomfort, mobility, strength, wellness.
- Red-flag screening (FR-101) is not skippable by design.
