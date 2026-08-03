# Grill Session — PT Training App + YouTube Channel

This document is the output of a requirements "grilling": every hard question a
demanding product / engineering / legal reviewer would ask before this project
is funded, together with a **recommended answer**. Where the answer was not
given by the product owner, it is marked **ASSUMED** — these are the decisions
you should confirm or override. Everything downstream
(`01-product-requirements.md`, `02-architecture.md`, `03-implementation-plan.md`)
is built on the answers below.

Legend:
- ✅ **GIVEN** — stated by the product owner in the original brief.
- 🔶 **ASSUMED** — recommended decision; confirm or override.
- 🔴 **RISK** — a decision that carries real product/legal/technical risk even
  after being answered.

---

## 1. Product & Users

### Q1.1 Who exactly is the user? A post-surgery rehab patient, a chronic-pain sufferer, or a healthy person doing "prehab"?
🔶 **ASSUMED:** Primary persona is a *self-directed adult with chronic
musculoskeletal pain* (knee, hip, lower back, shoulder, neck) who is not
currently under active clinical supervision. Secondary persona is a healthy
adult doing preventive mobility work. **Explicitly out of scope for v1:**
post-operative rehab protocols and anyone under active PT prescription —
because that moves the app toward a regulated medical device (see Q8.1).

### Q1.2 Is this a medical device?
🔴 **ASSUMED:** No — and the product must be written so it stays a *general
wellness* product under the FDA General Wellness guidance: it promotes
fitness/mobility and never claims to *diagnose, treat, or cure* a condition.
Concretely: UI copy says "discomfort area", not "diagnosis"; onboarding shows a
medical disclaimer and red-flag screening ("see a doctor if…"); marketing never
promises pain cure. One claim like "cures sciatica" on the YouTube channel can
reclassify the whole product. This constraint binds copywriting on both the app
and the channel.

### Q1.3 What does "problem description selection" actually collect?
✅ **GIVEN:** Body-region pain groups (knees, hips, lower back, shoulders, …).
🔶 **ASSUMED:** v1 collects: body region(s), pain severity (0–10 self-report),
red-flag screening questions (numbness, recent trauma, chest pain → hard stop
with "consult a professional" message), fitness level, and available equipment
(none / resistance band / light dumbbells). No free-text symptom entry in v1 —
free text invites diagnostic expectations we must not meet.

### Q1.4 Who builds the exercise programs — an algorithm or a human?
🔴 **ASSUMED:** A licensed physical therapist (or equivalent credentialed
professional) authors a static **program library**: for each pain group ×
fitness level there is a curated set of routines. The app *selects and
sequences* from this library; it does not generate novel exercise prescriptions
algorithmically in v1. This is both a safety decision and a scope decision.
**Open item: who is the credentialed content author?** This is the single
biggest non-engineering dependency in the project.

### Q1.5 How many exercises at launch?
🔶 **ASSUMED:** v1 launch target: **40 exercises** covering 4 pain groups
(knee, hip, lower back, shoulder) × ~10 exercises each, composed into ~12
routines. Each exercise = one 15–30 s video segment. This bounds the Google
Flow video-production effort (~40 videos + retakes) and the pose-rule authoring
effort (40 rule configs).

### Q1.6 What platforms?
🔶 **ASSUMED:** iOS + Android phones and tablets from a single Flutter
codebase (see Q6.1). Tablet layout matters because the brief explicitly calls
out shared-tablet family use. No web app in v1 (camera + on-device ML on mobile
web is materially worse). Portrait-primary UI.

### Q1.7 Monetization?
🔶 **ASSUMED:** Free at launch (consistent with "Cloudflare free hosting").
Architecture must not *preclude* later subscriptions, but no payment, no
entitlement system, no ads in v1. YouTube channel monetization (AdSense) is
independent and allowed.

---

## 2. Profiles & Accounts

### Q2.1 Are profiles local or cloud accounts?
✅ **GIVEN:** Multiple profiles on a shared device (family tablet).
🔶 **ASSUMED:** v1 profiles are **device-local, no sign-in, no password** —
like Netflix profiles on one device. A profile = name + avatar color + pain
groups + routines + history. Cloud sync/backup is Phase 4 (see roadmap),
because the moment health-adjacent data leaves the device you take on privacy
obligations (Q8.2) that v1 doesn't need.

### Q2.2 Children?
🔴 **ASSUMED:** The app is 13+ (COPPA line) and marketing targets adults.
Profile creation asks for an age gate ("13 or older") but stores no birthdate.
No child-directed content on the YouTube channel (affects YouTube's
made-for-kids flags).

### Q2.3 What happens when two profiles use the app back-to-back on one tablet?
🔶 **ASSUMED:** Profile picker on every cold launch; a persistent
profile-switch button on the home screen; per-profile "played intro already"
state is scoped to a *session*, so each family member hears the exercise
introduction the first time in *their* session (see Q5.4).

---

## 3. Content Pipeline (Google Flow, avatar, video format)

### Q3.1 What exactly does Google Flow produce, and what is the layout contract?
✅ **GIVEN:** Each exercise video is produced with Google Flow (Veo) as a
15–30 s portrait segment; a PT **avatar in a circular frame, top-left**
narrates; videos are uploaded as YouTube Shorts in portrait.
🔶 **ASSUMED — layout contract (binding on production):**
- Frame: 1080×1920 (9:16), 30 fps, H.264 + AAC.
- Avatar circle: centered at (x = 18% W, y = 12% H), diameter = 28% W. This
  region is **reserved**: the demonstrating figure and any on-screen text must
  never enter it.
- The bottom 20% of frame is reserved for the app to overlay its own timer /
  rep counter without covering the demonstration. No burned-in text in that
  band.
- The avatar is composited **into the video at production time** (burned in),
  not overlaid live by the app. The app never composites video.

### Q3.2 What is the video's internal structure?
✅ **GIVEN:** Each video = *intro segment* (avatar explains the exercise and
its benefits) + *exercise loop segment* (the movement itself). The intro must
be skippable after first play, so it must be a **fixed, known duration**.
🔶 **ASSUMED — segment contract:**
- Intro segment: **exactly 10.0 s** in every video (production pads/trims to
  this). Exercise segment: 15–30 s, and it must **loop cleanly** (first and
  last frames match pose) because the app replays it for every rep/set.
- *In addition to* the fixed 10 s convention, every video carries an
  `intro_end_ms` field in the content manifest (Q4.2). The app trusts the
  manifest, not the convention. Rationale: one mis-edited video with a 12 s
  intro would otherwise cause a mid-sentence skip forever. The convention makes
  production predictable; the manifest makes playback correct.

### Q3.3 Who narrates the reps/timer — the video or the app?
✅ **GIVEN:** Separation of concerns: the **video/avatar** teaches the
exercise and its benefits (intro) and demonstrates form; the **app** speaks
timer, rep counts, and pose corrections.
🔶 **ASSUMED:** The exercise-loop segment of the video therefore has **no
narration audio** (background-free or light ambient only), so app audio cues
never fight the video audio. The app ducks/plays its cues over the muted or
quiet loop.

### Q3.4 Can Google Flow actually deliver a *consistent* avatar and *anatomically correct* movement demonstrations?
🔴 **RISK — must be validated in Phase 0.** Generative video (Veo/Flow) is
known to struggle with (a) character consistency across dozens of clips and
(b) precise joint mechanics — exactly what a form-teaching video needs.
Mitigation plan: Phase 0 produces 3 pilot exercises end-to-end; a credentialed
PT reviews them for anatomical correctness; if Flow's demonstration quality
fails review, fallback is **filmed human demonstrations** with a Flow-generated
avatar only in the intro circle. The architecture is agnostic to this — only
the production pipeline changes.

### Q3.5 What are YouTube Shorts' constraints?
Shorts must be ≤ 3 min (fine), portrait (fine). But Shorts **cannot be
monetized per-video the usual way, cannot have end screens, and the Shorts
player UI (like/comment overlays) covers parts of the frame**. Also, the
YouTube channel is a *distribution/marketing* surface — the app does not play
from YouTube (see Q4.1). 🔶 **ASSUMED:** Channel uses Shorts for discovery;
the same master files are the app's source of truth via R2.

---

## 4. Video Delivery & Caching (the YouTube ToS problem)

### Q4.1 The brief says "cache the video locally so it's not re-downloaded from YouTube." Is that allowed?
🔴 **NO — and this changes the architecture.** YouTube's ToS and API policies
prohibit downloading/caching video content outside YouTube's own players, and
prohibit playback UIs that hide/modify the player. An app that streams from
YouTube cannot legally cache, cannot skip-seek reliably without the IFrame
player chrome, and risks channel termination.
✅ **RESOLUTION (adopted):** **Dual-hosting.**
- **YouTube** hosts the public channel (marketing, SEO, community). The app
  may deep-link out to the channel but never embeds it in the workout flow.
- **Cloudflare R2** hosts the exact same master MP4 files as the app's video
  origin. R2's free tier: 10 GB storage, **zero egress fees**, generous free
  request quota. 40 videos × ~8 MB ≈ 0.3 GB — two orders of magnitude of
  headroom. The app downloads from R2 once, caches on device (fully legal —
  it's our content), and plays locally thereafter. This *better* satisfies the
  original goal (no constant re-downloading) than YouTube ever could.

### Q4.2 How does the app know what content exists?
🔶 **ASSUMED:** A versioned **content manifest** (JSON) served by a Cloudflare
Worker (or as a static R2 object behind the Worker): exercise metadata, R2
video URL, `intro_end_ms`, `loop_start_ms`/`loop_end_ms`, rep tempo, pose-rule
config, audio-cue script, program/routine definitions. The app checks the
manifest version on launch (when online) and lazily downloads new/changed
videos. The manifest is the single integration contract between the content
pipeline and the app.

### Q4.3 Cache policy on device?
🔶 **ASSUMED:** LRU cache, default cap 1 GB (user-adjustable), videos for the
user's *active routines* are prefetched on Wi-Fi after routine creation; a
session never streams — if a video isn't cached yet, the session screen shows
a short "preparing your workout" download step. Offline: fully cached routines
work with no connectivity (aligns with local profiles, Q2.1).

### Q4.4 What does Cloudflare's free tier actually cover, and where are the cliffs?
🔶 Validated against free-tier limits (as of early 2026 — re-verify at build
time): Workers free plan **100k requests/day**; R2 free **10 GB-month storage,
1M Class A + 10M Class B ops/month, zero egress**; Pages free (unlimited static
requests); D1 free **5 GB storage, 5M rows read/day**; KV free 100k reads/day.
The v1 design (static manifest + R2 video, client-heavy, local-first) keeps all
server traffic at "manifest check + video download once per device", so the
free tier survives to roughly **tens of thousands of active devices**. The
first paid cliff is Workers requests if we later add sync (Phase 4) — at $5/mo
paid tier, acceptable. 🔴 **RISK accepted:** free tier has no SLA.

---

## 5. Workout Session Mechanics

### Q5.1 What is a "routine" precisely?
🔶 **ASSUMED:** Routine = ordered list of exercise blocks; block =
{exercise, mode, target, sets, rest_seconds}. `mode` ∈ **rep-based** (target
reps, rep counted by pose) or **time-based** (target seconds, e.g. planks,
stretches). Routines are assigned to weekdays (the "create a routine for each
day" requirement) forming a weekly **plan**. Users can edit blocks, reorder,
swap exercises (from the same pain-group's approved list), change
sets/reps/rest, and toggle days.

### Q5.2 How are reps counted?
🔶 **ASSUMED:** On-device pose estimation (MediaPipe Pose Landmarker, 33
landmarks) feeds a per-exercise **rep state machine**: each exercise's config
defines a primary joint-angle signal, an "up" threshold, a "down" threshold,
hysteresis, and min-rep-duration. Crossing down→up→down = 1 rep. Rep count is
spoken and displayed. Confidence gating: if landmark visibility drops below
threshold, the app pauses counting and says "step back into frame" rather than
miscounting.

### Q5.3 What does the pose evaluator actually evaluate — and what does it *say*?
🔴 **ASSUMED (safety-sensitive):** Per-exercise **form rules** (2–4 per
exercise), each a joint-angle/alignment predicate with tolerance, authored
alongside the PT (e.g. squat: "knees don't collapse inward" = knee x-distance
≥ ankle x-distance × 0.9; "back stays neutral" = shoulder-hip-knee angle
within range). Feedback is **coaching language, throttled** (max one cue per
6 s, positive-first: "try keeping your knees over your toes"), never clinical
or alarming. The evaluator can *pause* an exercise on repeated severe
violations, showing "let's review the form video". It must never claim to
guarantee safe form — disclaimer covers that pose estimation is approximate.

### Q5.4 The intro-skip logic — first play per what, exactly?
✅ **GIVEN:** Intro (benefits/how-to) plays once, subsequent sets/reps skip
straight to the exercise segment.
🔶 **ASSUMED — precise rule:** Intro plays on the **first encounter of that
exercise in the current session** for the current profile. Later sets in the
same session, and looped replays within a set, start at `intro_end_ms`. A
per-profile setting "always skip intros" (for experienced users) and a "replay
instructions" button during any exercise. Across sessions, default is to play
the intro again only if the profile hasn't done that exercise in ≥ 14 days
(refresh memory), otherwise skip — this is a tunable manifest value.

### Q5.5 Audio: what talks, when, and does it fight the video?
✅ **GIVEN:** App speaks timer, reps, pose corrections.
🔶 **ASSUMED:** Pre-recorded cue library (not on-device TTS) for numbers
1–50, countdowns, and the ~30 standard coaching phrases, generated once with a
TTS voice matched to the avatar's voice; shipped in the app bundle. Rationale:
zero-latency, consistent voice, works offline. Cue priority: safety cue >
rep count > timer. Respect system volume/mute; audio session ducks any
background music the user is playing.

### Q5.6 Camera placement UX?
🔶 **ASSUMED:** Before the first exercise needing pose tracking, a framing
step: silhouette outline + "place your phone so your whole body is visible"
with a live skeleton preview and a green "you're in frame" state. Per-exercise
manifest flag for which body parts must be visible (squat needs full body;
neck stretch needs upper body). Exercises where tracking is impractical
(floor-lying, side-on) can set `pose_tracking: "off"` and fall back to
timer-only — **do not force machine vision where it can't work.**

---

## 6. Technology Choices

### Q6.1 Mobile framework?
🔶 **ASSUMED: Flutter.** One codebase for iOS/Android/tablets; first-class
camera + MediaPipe Tasks support; strong video player (`media_kit`/
`video_player`) with precise seeking; ships its own renderer so the
circular-avatar-and-overlay UI is identical on both platforms. React Native is
viable; native ×2 is not justified at this team size. If the team has deep
existing React expertise, RN is the acceptable swap — decide once, in Phase 0.

### Q6.2 Pose estimation engine?
🔶 **ASSUMED: MediaPipe Pose Landmarker (full model), on-device, CPU/GPU
delegate.** ~30 fps on mid-range phones at the "lite" model if needed; 33
landmarks with visibility scores; free, no per-call cost, no cloud latency, no
video ever leaves the device (privacy story writes itself). Alternative
(MoveNet Thunder via TFLite) is the fallback if Flutter-MediaPipe integration
disappoints on iOS.

### Q6.3 Backend?
🔶 **ASSUMED:** Cloudflare **Pages** (marketing site + privacy policy),
**R2** (video + manifest storage), one **Worker** (manifest endpoint with
version header, signed-URL issuing if we later gate content, anonymous
telemetry ingest), **D1** (telemetry + future accounts). No servers, no
containers. v1 has **no user-data backend at all** — profiles/history are
on-device (Q2.1), which is the cheapest and most private design that satisfies
the brief.

### Q6.4 Analytics/telemetry?
🔶 **ASSUMED:** Anonymous, opt-in-by-default-OFF for anything health-adjacent.
v1 collects only: app opens, session completed (exercise IDs, durations —
no pose data, no camera data, ever), crash reports (Sentry free tier or
Crashlytics). Pose/camera frames are processed in memory and never stored or
transmitted — this is a hard product commitment stated in the privacy policy.

---

## 7. YouTube Channel Strategy

### Q7.1 What is the channel *for*, if the app doesn't stream from it?
🔶 **ASSUMED:** (1) Discovery/acquisition — Shorts are the top-of-funnel ad
for the app; (2) credibility — a public library people can browse; (3)
optional revenue later. Channel description and each Short's description link
to the app stores. Upload cadence: batch-publish per pain group as app content
ships. Titles follow "Exercise name — pain group relief" SEO pattern.

### Q7.2 Same file on YouTube and R2?
🔶 **ASSUMED:** Yes — one master per exercise, rendered once, uploaded to
both. YouTube gets the full version (intro + loop); the app plays segments of
the identical file via manifest timestamps. No separate edits to maintain.

---

## 8. Legal / Compliance

### Q8.1 Regulatory posture
🔴 See Q1.2 — general wellness positioning, red-flag screening, disclaimers at
onboarding and in every store listing. An attorney should review the final
copy. Budget for it.

### Q8.2 Privacy
🔶 **ASSUMED:** v1 stores everything locally → privacy policy is short and
strong: "no account, no health data leaves your device, camera frames are
processed on-device and never recorded". App-store privacy labels must match.
The moment Phase 4 sync ships, this must be revisited (HIPAA does **not**
apply — we're not a covered entity — but state privacy laws like CPRA and
"consumer health data" laws like Washington's My Health My Data likely do).

### Q8.3 Music/voice rights
🔶 **ASSUMED:** No commercial music in videos (silence/ambient). The TTS/
avatar voice license must permit commercial distribution in both the videos
and the app's cue library — verify Google Flow's output license terms for
commercial use in Phase 0.

---

## 9. Explicitly Out of Scope (v1)

- Post-operative or clinician-prescribed rehab protocols
- Algorithmic/AI-generated exercise prescription
- Cloud accounts, cross-device sync, social features, leaderboards
- Wearable integration, Apple Health / Google Fit export
- Payments/subscriptions; ads in app
- Web app; smart-TV casting
- Languages other than English
- Live streaming from YouTube inside the workout flow (prohibited by ToS)

---

## 10. Open Items Requiring the Product Owner (blocking noted)

| # | Item | Blocks |
|---|------|--------|
| 1 | Confirm the ASSUMED decisions above, especially Q1.4 (who is the credentialed PT content author?) | Phase 1 content |
| 2 | Flutter vs React Native — confirm team skill fit (Q6.1) | Phase 1 build |
| 3 | Phase 0 pilot verdict: is Google Flow demonstration quality PT-approvable? (Q3.4) | Phase 1 content |
| 4 | App name, branding, and the avatar's persona/voice | Store listing, video production |
| 5 | Legal review budget for wellness positioning + privacy policy (Q8.1) | Launch |
