"""Explicit, separated statuses (never one overall boolean).

Verification statuses follow the project contract:
  verified            every problem passed the engine's validator (quotes located on the page,
                      answers recomputed with exact arithmetic, checks and independent verification hold)
  partially_verified  some, not all, problems passed; nothing is rendered or delivered
  requires_review     the validator rejected the spec, or the model declared the document does not fit
  unsupported         no problem could be detected / the document type is outside the engine
"""
from __future__ import annotations

from enum import Enum


class Verification(str, Enum):
    VERIFIED = "verified"
    PARTIALLY_VERIFIED = "partially_verified"
    REQUIRES_REVIEW = "requires_review"
    UNSUPPORTED = "unsupported"


class StageStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    SKIPPED = "SKIPPED"
    NOT_RUN = "NOT_RUN"
