# skillforge-onboarding

## Overview

Walks a new Panviva team member through the full SkillForge CLI onboarding flow — from Okta group access through `skillforge init <project-name>`. Deterministic 7-step sequence: the user doesn't need to know the URLs, commands, or order — the skill delivers them and verifies each step before moving on.

## When to Use

Invoke when the user:
- Is new to SkillForge and needs the install flow
- Asks "how do I install skillforge" / "set up the skillforge CLI"
- Hits an error at `skillforge init` (walk them back through)
- Mentions the SkillForge Azure URL, `pv-ai-skillforge`, or API keys in SkillForge

## Workflow

1. **Okta group** — admin adds user to product's Okta group (blocks step 2)
2. **SSO sign-in** — user signs into SkillForge at the Azure Container Apps URL
3. **API key** — generate under Settings → API Keys (copy immediately)
4. **Install CLI** — `pip install git+https://github.com/panviva/pv-ai-skillforge.git`
5. **Set server_url** — `skillforge config set server_url <URL>`
6. **Set api_key** — `skillforge config set api_key <key>`
7. **Init project** — `skillforge init <project-name>` pulls the project's skills

Each step verifies before proceeding. If `init` fails, the skill knows how to walk the user back.

## Prerequisites

- Python 3.9+ with `pip` on PATH
- `git` installed (needed for `pip install git+...`)
- Browser access for Okta SSO
- An admin who can add you to the right Okta group in your product

## Examples

**Example 1 — fresh onboard:**
> User: "I just joined the team, how do I install skillforge so I can get my project's skills?"
> → Skill runs the full 7-step flow, pausing for Okta admin action and API key copy.

**Example 2 — stuck mid-flow:**
> User: "skillforge init is giving me 401"
> → Skill jumps to the error table, diagnoses auth issue, re-runs steps 5 & 6 to verify config.

**Example 3 — install fails:**
> User: "pip install for skillforge worked but `skillforge` command isn't found"
> → Skill checks PATH/Python mismatch; falls back to `py -m skillforge` on Windows; catches the known `pyproject.toml` missing-packages bug if present.

## Model

Recommended: **Haiku**. Fixed sequence, fixed commands, no synthesis needed.
