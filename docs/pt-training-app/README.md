# PT Training App — Product & Engineering Specs

A physical-therapy-inspired wellness training app (iOS/Android) with a
companion YouTube Shorts channel. Users pick discomfort areas (knee, hip,
lower back, shoulder), get PT-authored routines with avatar-narrated exercise
videos, and the phone's front camera counts reps and coaches form on-device.
Infrastructure runs on Cloudflare's free tier; videos are produced with
Google Flow and dual-hosted on YouTube (marketing) and Cloudflare R2 (app
delivery + legal local caching).

## Documents

| Doc | Purpose |
|---|---|
| [00-grill-session.md](00-grill-session.md) | Requirements grilling: every hard question with a recommended answer; ASSUMED decisions flagged for product-owner confirmation; open items list |
| [01-product-requirements.md](01-product-requirements.md) | PRD: personas, functional requirements (FR-xxx), content requirements (CR-x), NFRs, success metrics, release criteria, legal positioning |
| [02-architecture.md](02-architecture.md) | Architecture: system diagram, content-manifest contract, Cloudflare deployment, Flutter app design (session engine, pose pipeline, playback, audio), production pipeline, ADRs |
| [03-implementation-plan.md](03-implementation-plan.md) | Phased plan: Phase 0 de-risk gate → foundations → session engine → launch; risk register; external dependencies |

## Read this first

Two decisions in these docs deliberately diverge from the original brief:

1. **The app does not stream or cache from YouTube.** YouTube's ToS prohibits
   it. Videos are dual-hosted: the identical master files go to YouTube (as
   the public channel) and to Cloudflare R2 (zero-egress free tier), which the
   app downloads from once and caches locally — achieving the original
   "don't re-download constantly" goal legally and more reliably.
2. **The fixed-duration intro is a production convention, not a playback
   mechanism.** Intros are produced at exactly 10 s, but the app skips intros
   using a per-video `intro_end_ms` field in the content manifest, so one
   mis-edited video can never break intro-skipping.

All other ASSUMED decisions are listed in
[00-grill-session.md §10](00-grill-session.md) awaiting confirmation.
