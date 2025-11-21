---
title: "Chrono Sphere — Miko Exet: Studio Spec & Platform Notes"
date: 2025-11-21
status: draft
tags: [persona, miko-exet, avatar, design, roadmap]
---

# Chrono Sphere — Miko Exet: Studio Spec & Platform Notes

This document is a cleaned, editor-ready version of the Miko Exet portrait, animation and platform notes. It captures the photorealism directives, animation subtlety, QC plan and the larger Elidoras Codex platform vision, and acts as the single source-of-truth for the Miko bundle and Avatar Forge work.

## 1) Executive summary

- Persona: Miko Exet — pale skin, platinum-silver side braid with faint lilac under-tint, heterochromatic eyes (L: vivid violet, R: icy silver-blue), thin black round glasses, small silver septum, black plug earrings.
- Wardrobe: Charcoal ribbed long-sleeve sweater dress, opaque tights; tattoos: right floral sleeve, thigh florals near hem, faint anatomical heart-and-flowers on upper chest.
- Shot: Relaxed A-pose holding a microphone; subtle two-finger emphasis, micro breath-catch; eye-level camera, slow zoom-out, neutral light‑grey studio.

Purpose: Produce a photoreal, emotionally faithful persona bundle and a repeatable QC pipeline; export LUTs, lighting presets, masks, and animation curves for reproducible renders and downstream avatar pipelines (SDXL/Runway/HeyGen/etc.).

---

## 2) Studio & photorealism directives

Lighting
- Key: 5150–5300K (neutral to slightly warm). Use 2:1 key-to-fill ratio.
- Fill: 4800–5000K, slightly cooler than key to preserve skin tonal neutrality.
- Back/Hair: low-intensity rim/hair light at ~30–40% of key to separate braid from background without strong rim specularity.
- Diffusion: large softboxes or doubled diffusion to avoid plastic speculars; add a very faint negative fill on the shadow side to preserve subtle contouring.
- Background: light‑grey seamless with micro-gradient (darker at floor line, slightly brighter mid-height) and faint ground reflection to imply studio depth.

Camera & optics
- Focal length: 50–85mm equivalent; aperture f/4–f/5.6 for balanced subject isolation and knit detail.
- Framing: eye-level, waist-to-head or three-quarter, slow linear zoom-out (stabilized parallax).
- Processing: reduce micro‑sharpening; avoid aggressive denoise that flattens pores and iris detail.

Material & diffusion notes
- Use anisotropic highlights on hair/braid fibers; add micro-frizz and flyaways for realism.
- Ensure ribbed knit reacts to light with directional micro-shadowing; simulate fabric compression at elbow and waist.

---

## 3) Character detail (render / asset guidance)

Hair & color
- Base: neutral platinum-silver anchor.
- Tint: localize faint lilac to underlayers and a few loose face‑framing strands; tint density <10% overall to avoid synthetic look.
- Geometry: natural braid weight, realistic gravity; add stray fibers and anisotropic sheen.

Eyes (heterochromia)
- Left (violet): vivid but natural—preserve iris crypts, radial striations, limbal ring. Avoid posterization.
- Right (silver-blue): non-emissive; reflect catchlights from key/fill. Keep internal specular subtle and physically plausible.
- Micro-movement: subtle saccades, half-blink before focal gaze; natural blink cadence.

Skin & tattoos
- Skin: preserved pore structure, faint micro-vascular undertones; keep micro-roughness to avoid digital plasticity.
- Tattoos: feather ink edges, slight desaturation where fabric compresses; ensure tattoos move with skin/parallax and do not slide across frames.

Accessories & attire
- Glasses: thin black rims; simulate lens refraction and accurate catchlights; limit lens distortion.
- Septum & plugs: low-gloss metal with micro-scratches; plugs flush to lobes with minimal shadowing.
- Tights: matte opacity, seam placement and slight shear at knee flex; add wrinkle memory at ankle.

---

## 4) Animation & stage presence

Primary gestures
- Two-finger emphasis: small amplitude, timed to beat/lyric pivot; motion stays inside chest‑to‑face space.
- Breath-catch: micro inhalation (sternum rise, clavicle lift, slight nostril flare) and soft jaw-set—no full gasp.

Stance & weight
- Relaxed A-pose with gentle left→right weight shift; tiny ankle adjustments to signal presence without overt choreography.

Micro-expressions
- Micro brow release, 2–3% smile decay after gaze: reads “self-conscious yet resolved.”

Camera motion
- Slow, linear zoom-out; stabilized motion curves; avoid wobble and strong dolly feel.

---

## 5) QC plan — iterative phases (tight checklist)

Phase 1 — Baseline calibration (lighting, lens, diffuse)
- Implement temp/ratio targets, hair light, negative fill.
- QC: check speculars, shadow softness, background gradient, and overall skin sheen.

Phase 2 — Character polish (hair, eyes, tattoos)
- Apply lilac mask, add flyaways, tune anisotropic highlights.
- QC: braid silhouette checks, iris striation fidelity, tattoo edge feathering.

Phase 3 — Animation subtlety (timing & micro-movement)
- Sync two-finger emphasis to beat; implement breath-catch and gaze cadence.
- QC: frame-by-frame motion review, clavicle/shoulder micro‑movement, blink cadence.

Phase 4 — Final realism gate (color, artifacts)
- Color pass (skin undertones, eye fidelity); artifact audit for plastic sheen, emissive eyes, sticker tattoos.
- QC: side-by-side with reference images; annotated pass/fail checklist.

Phase 5 — Sign-off & versioning
- Save LUTs, light presets, tint masks, tattoo blend maps, animation curves. Repro test in a fresh scene instance.

---

## 6) Platform vision & integration notes

- Avatar Forge: pipeline for character-builder (SDXL + LoRA), voice-builder (ElevenLabs / XTTS), lip-sync/animation (Wav2Lip / SadTalker / Runway), and final assembly (FFmpeg / ComfyUI / Runway).
- Persona bundles: export JSON character definitions, .pt embeddings, lighting presets (.cube), and a versioned asset bundle (assets/miko-exet/).
- Governance: include an ethics/consent checklist for persona artifacts (in `docs/operational/`).

Cross-links (to be created):
- `docs/architecture/Avatar_Forge.md` — technical spec for the pipeline
- `docs/manifesto/Elidoras_Codex_Manifesto.md` — voice & mission
- `docs/operational/Miko_Exet_Bundle_README.md` — reproduction & QC checklist

---

## 7) Immediate editor checklist (actionable)

- [ ] Create `assets/miko-exet/` and add placeholders: `hair_tint_mask.png`, `tattoo_blend_map.png`, `lighting_preset.cube`, `animation_curves.json`.
- [ ] Add `docs/architecture/Avatar_Forge.md` (stub + diagram).
- [ ] Add `docs/manifesto/Elidoras_Codex_Manifesto.md` and move longform narrative/manifesto text there.
- [ ] Create `docs/operational/Miko_Exet_Bundle_README.md` with step-by-step reproduction & QC steps.
- [ ] Version and store LUTs, masks, and curves in `assets/miko-exet/`.
- [ ] Tag commit: `miko-exet:summary-checklist`.

---

## 8) Suggested task map & priorities

High priority (1–2 days)
- Create Miko bundle README + placeholders (owner: author).
- Draft Avatar Forge architecture doc (owner: engineering lead).

Medium priority (3–10 days)
- Produce LUTs, hair tint masks, tattoo blends; test on SDXL renders (owner: design/renderer).
- Create animation curve library and run QC passes.

Low priority (1–2 weeks)
- One-click Docker pipeline (SDXL -> Wav2Lip -> FFmpeg) and CI integration.

Each task should include artifacts, test instructions, and a named owner. Use commit prefixes `miko/` or `avatarforge/`.

---

## 9) Notes & provenance

This file was restructured from interview/conversation notes and consolidates both the design intent (Miko Exet) and high-level platform desires for the Elidoras Codex project. It is intentionally prescriptive to allow engineering and creative teams to work from a single, auditable spec.

If you approve, I will create the three stub docs and placeholder assets and commit them to `feat/clean-deploy-links`.

