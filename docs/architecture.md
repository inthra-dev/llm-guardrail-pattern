Architecture: Plan → Gate → Execute

This repository implements a minimal control architecture for using LLMs
as execution agents in engineering workflows.

The goal is not collaboration, but containment.


FLOW

1. PLAN
The LLM produces a machine-readable execution plan.
No execution is allowed at this stage.

2. GATE
The plan is validated against strict allowlists:
- permitted operations
- permitted file paths
- mandatory reasons

Any violation results in immediate abort.

3. EXECUTE
Only after the plan passes validation is execution allowed.
Execution must follow the plan exactly.


WHY THIS WORKS

- Planning separates intent from action.
- Gating enforces scope mechanically.
- Execution happens only after control is established.

This removes initiative from the model and restores it to the operator.


DESIGN GOAL

Make unsafe behavior impossible,
not merely discouraged.
