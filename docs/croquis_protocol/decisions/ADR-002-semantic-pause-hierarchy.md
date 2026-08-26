# ADR-002 — Use semantic pause categories

- Status: Accepted for Protocol V1
- Date: 2026-08-18

## Context

V3 contains many numerically reasonable waits, but their purpose is encoded only by location. That makes pacing difficult to review or reuse and allows important construction layers to run back-to-back without viewer processing time.

## Decision

Stable croquis scenes should prefer named pause categories:

- camera settling;
- micro separation;
- construction separation;
- reading;
- explanation;
- final observation.

The values are tunable defaults, not universal constants. The category is the protocol; the exact duration remains scene-sensitive.

## Consequences

- code review can ask whether a pause is semantically justified;
- pacing can be tuned globally without erasing intent;
- future QA can compare expected pause category against rendered timing;
- the scene becomes slightly longer, but only where viewer cognition requires it.
