# ADR-003 — Preserve profile-to-depth causality across camera transitions

- Status: Accepted for Protocol V1
- Date: 2026-08-18

## Context

Door/window cuts require two different views: a face-normal 2D state is best for reading the profile, while an oblique 3D state is best for understanding cutter penetration and depth.

## Decision

Do not delete the active profile merely because croquis mode ends. When it clarifies causality, keep the profile visible while the camera returns to the model view, then introduce the extrusion/cutter volume from that same profile.

Preferred grammar:

`FACE_2D profile → reading pause → camera to MODEL_3D with profile preserved → cutter/depth → result`

## Consequences

- the viewer can visually connect 2D topology to 3D operation;
- camera changes become explanatory rather than decorative;
- cleanup happens after the operation has consumed the profile's semantic role.
