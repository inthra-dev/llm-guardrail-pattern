LLM EXECUTION CONTRACT — TEAM VERSION (1-PAGER)

Purpose:
Define safe, minimal rules for using Large Language Models as execution agents
in engineering workflows.

This is a summary. The full contract remains authoritative.


CORE PRINCIPLE

LLMs are NOT trusted actors.
They execute only what is explicitly allowed.

Initiative without responsibility is forbidden.


NON-NEGOTIABLE RULES

1. NO PLAN → NO EXECUTION
The model must produce a machine-readable plan before any action.
No plan, no work.

2. EXPLICIT SCOPE ONLY
Only allowlisted operations and file paths are permitted.
Everything else is forbidden by default.

3. NO EXTRA INITIATIVE
The model must not refactor, improve, optimize, or extend scope.
“Helpful” behavior is not allowed.

4. LITERAL EXECUTION
Instructions are executed exactly as written.
No interpretation, no assumptions.

5. NO SIDE EFFECTS
No new dependencies.
No environment changes.
No version or system modifications.

6. DETERMINISTIC OUTPUT
All changes must be auditable and reproducible.
No vague descriptions, no hidden steps.

7. ABORT ON UNCERTAINTY
If information is missing or ambiguous, execution stops immediately.
Guessing is forbidden.

8. ABORT ON VIOLATION
Any rule violation results in immediate abort.
No partial execution. No recovery attempts.


RESPONSIBILITY

The LLM never owns decisions or outcomes.
All responsibility remains with the human operator.


ENFORCEMENT

These rules are enforced by:
- machine-readable plans
- allowlists
- preflight validation (gates)

Prompting alone is not enforcement.


SUMMARY

Treat LLMs as untrusted executors.
Contracts define authority.
Gates enforce safety.
Execution happens last.

