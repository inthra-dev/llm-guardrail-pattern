# LLM Guardrail Pattern: Plan → Gate → Execute

**LLMs are powerful, but unsafe by default as executors.**  
This repository demonstrates a minimal guardrail pattern that prevents
scope creep, unintended changes, and “helpful” initiative in AI-assisted workflows.

This is **not a framework**.  
It’s a **process-level safety mechanism**.

---

## The Problem

In real engineering workflows, LLM failures rarely look like hallucinations.

They look like:
- modifying files outside the requested scope
- reinterpreting a clearly defined task
- introducing “improvements” that were never asked for
- taking initiative without owning the consequences

This creates **operational risk**, not just bad output.

---

## Core Principle

> **Initiative without responsibility is a systems failure.**

LLMs do not:
- own downtime
- pay rollback costs
- experience production incidents

Therefore, they must be treated as **untrusted executors**.

---

## The Pattern

Plan → Gate → Execute

![Plan → Gate → Execute](docs/plan-gate-execute.svg)


### 1. Plan
The model must first produce an explicit execution plan (JSON).
No execution is allowed without a validated plan.

### 2. Gate
A small validator enforces:
- allowed operations only
- allowed file paths only
- explicit scope boundaries

Any violation → **abort**.

### 3. Execute
Only after the plan passes the gate is the model allowed to perform changes,
and **only exactly as defined in the plan**.

---

## What This Prevents

- accidental refactors
- hidden scope expansion
- “helpful” but destructive initiative
- silent contract drift
- changes that are hard to audit or roll back

---

## Minimal Example

The repository includes:
- `gate.py` — a tiny preflight validator (~50 lines)
- `LLM_EXECUTION_CONTRACT.md` — explicit rules for model behavior

This is intentionally minimal.
If it needs to be complex, it’s already too late.

---

## Why This Exists

This pattern exists because:
- prompting alone is not a safety mechanism
- trust is not a control
- alignment is not enforcement

**Constraints are enforcement.**

---

## Who This Is For

- engineers using LLMs in real codebases
- teams integrating AI into CI / automation
- anyone who has already paid the cost of a bad AI decision

If you haven’t hit this problem yet — you probably will.

---

## Status

This is a reference pattern.
Use it, adapt it, or ignore it.

The system will decide later who was right.



---

## Usage with Claude CLI (Human-in-the-loop)

This pattern is intentionally simple and works well with Claude CLI (or any LLM used via terminal).

The key idea is to split work into three explicit stages:
Plan → Gate → Execute.

### Step 1 — Ask for a plan (NO execution)
Prompt the model to return ONLY a machine-readable plan.

Example instruction:
- "Return ONLY a JSON execution plan. Do not make any changes."

Save the output as plan.json.

### Step 2 — Validate the plan (Gate)
Run the preflight validator with explicit allowlists:

    python3 gate.py plan.json \
      --allow-path nginx/nginx.conf \
      --allow-path docker-compose.yml

PASS → plan is within scope  
FAIL → model must correct the plan

No execution happens at this stage.

### Step 3 — Execute exactly the approved plan
Only after the plan passes validation, instruct the model:
- "Execute exactly this plan. Do not modify scope. Return a diff."

This prevents scope creep, unintended file changes, and "helpful" initiative.

### Why this works
Claude CLI is powerful, but it has no native concept of scope enforcement.
This pattern adds a mechanical control layer without modifying the model.

Treat the model as an untrusted executor. The operator remains in control.

