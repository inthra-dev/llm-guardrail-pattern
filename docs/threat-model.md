Threat Model: LLM as Execution Agent

This document lists common failure modes observed when using LLMs
as executors in real engineering environments.


THREAT 1 — Initiative Creep

Description:
The model introduces actions beyond the explicitly requested scope.

Impact:
Unintended changes, silent regressions, hard-to-audit diffs.

Mitigation:
- Explicit machine-readable plans
- Strict allowlists
- Abort on extra operations


THREAT 2 — Contract Drift

Description:
The model reinterprets instructions over time or across steps.

Impact:
Behavior diverges from the original request.

Mitigation:
- Literal execution rules
- Deterministic outputs
- Abort on ambiguity


THREAT 3 — Hidden Side Effects

Description:
The model introduces dependencies, environment changes, or system-level actions.

Impact:
Security issues, production instability.

Mitigation:
- No implicit dependencies rule
- Scope-limited execution
- Preflight validation


THREAT 4 — Over-Agreeableness

Description:
The model agrees instead of correcting or stopping on uncertainty.

Impact:
Errors propagate silently.

Mitigation:
- Abort on uncertainty
- Explicit requirement to stop when information is missing


SUMMARY

LLMs fail like optimistic junior operators,
but without accountability.

Controls must assume failure and enforce safety mechanically.
