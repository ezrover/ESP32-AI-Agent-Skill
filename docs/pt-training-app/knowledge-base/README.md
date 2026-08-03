# Exercise Knowledge Base

The project's content authority. Every exercise that ships in the app or on
the YouTube channel must originate from this knowledge base, which is built by
deep research of complete, authoritative public sources — not by an in-house
clinical reviewer (product-owner decision, 2026-08-03; see grill session
Q1.4).

## Files

One file per pain group: `knee.md`, `hip.md`, `lower-back.md`, `shoulder.md`.
Extraction date and counts are stamped at the top of each file.

## Sourcing rules (binding)

1. **Source tiers.**
   - **T1 — clinical:** NHS/NHS Inform, AAOS OrthoInfo, Mayo Clinic,
     Cleveland Clinic, Harvard Health, NIAMS, Versus Arthritis, Arthritis
     Foundation, published rehab protocols (GLA:D, McGill, McKenzie as
     described in reputable clinical summaries).
   - **T2 — professional organizations:** APTA/ChoosePT, ACSM, NASM,
     Physiopedia.
   - **T3 — credentialed professionals' channels/sites:** licensed physical
     therapists and certified trainers on YouTube and the web (e.g. Bob &
     Brad, AskDoctorJo). Used for corroboration and practical form cues,
     never as an exercise's only source.
2. **Corroboration rule:** an exercise is production-eligible only if it
   appears in ≥ 2 independent sources, at least one of them T1 or T2.
   Single-source finds live in each file's "Candidates" appendix and are not
   production-eligible until corroborated.
3. **Own words:** all descriptions are rewritten; no verbatim copying from
   sources. Source URLs are recorded per exercise.
4. **Every exercise records:** aliases, position, equipment, target
   structures, purpose, steps, form cues, common mistakes, typical dosage,
   progression/regression, cautions, camera trackability (with proposed
   pose-signal), and sources with tiers.

## How the KB drives production

- **Video scripts** (intro narration, choreography) are written from the KB's
  purpose/steps/form-cue fields.
- **Storyboard keyframes:** the A/B winner between image providers is selected
  against the KB's form cues and common mistakes (the objective checklist that
  replaces subjective review).
- **Pose rules** (`rep_counter`, `form_rules` in the content manifest) are
  derived from the KB's camera-trackability assessment and form cues.
- **Dosage defaults** (sets/reps/hold/rest in the manifest) come from the KB's
  typical-dosage field.
- **Cautions** feed each exercise's in-app "take it easy" copy and the
  pain-group onboarding screens.

## Maintenance

Re-verify sources and re-run extraction per pain group before each major
content release; bump the extraction date. New pain groups (neck, ankle, …)
enter as new files under the same rules.

## Honest limitation (recorded once, binding on copy)

This KB aggregates published guidance from authoritative sources; it is not a
substitute for individualized professional judgment, and no clinician reviews
our specific renditions. Consequences: (a) the app's wellness positioning and
disclaimers (PRD §9) carry more weight and must never be diluted; (b) the
corroboration rule above is strict — when sources disagree, we follow the
more conservative T1 guidance or drop the exercise; (c) exercises whose safe
execution depends on individualized assessment (per source cautions) are
excluded from starter routines.
