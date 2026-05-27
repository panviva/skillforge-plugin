---
name: skillforge
description: Manage SkillForge AI agent skills -- install, upload, search, list, and check status of skills in your project.
recommended_model: claude-haiku-4-5-20251001
allowed-tools: Bash(python:*) Bash(skillforge:*) Bash(pip:*)
compatibility: |
  - Requires: Python 3.11+ with skillforge CLI installed (`pip install -e .` from repo root)
  - Requires: Authenticated session (`skillforge auth login`)
  - Requires: Project initialized (`skillforge init <project>`) — positional form preferred; `--project <name>` flag works as hidden alias
---

# SkillForge CLI Skill

Manage your team's AI agent skills directly from Claude Code. Install, upload, search, and monitor skills without leaving your session.

## First-Time Setup

If `skillforge` isn't on your PATH yet, install the CLI:

```bash
pip install git+https://github.com/panviva/pv-ai-skillforge.git
```

Then authenticate and initialize:

```bash
skillforge auth login --server https://skillforge-struong-app.victoriouspebble-7d643944.eastus.azurecontainerapps.io --email <your-email> --password <your-api-key>
skillforge init <project-name>
```

## Updating SkillForge

To update the CLI to the latest version:

```bash
pip install --upgrade git+https://github.com/panviva/pv-ai-skillforge.git
```

To update the Claude Code skill itself:

```bash
/plugin update skillforge
```

To update your installed project skills to the latest versions:

```bash
skillforge update
```

## Quick Start

```bash
# Check your project status
skillforge status

# See all skills in your project
skillforge list

# Install a skill
skillforge install epic-validator

# Upload a skill by name (from your skills directory)
skillforge upload adr-walkthrough

# Search for skills
skillforge search "code review"

# Update all installed skills
skillforge update
```

## Visibility Management (v7.0)

Admins can change a skill's visibility scope (project | org | admin-restricted) via CLI:

```bash
# Promote a project-scoped skill to org-wide visibility
skillforge visibility set my-skill org

# Check current visibility
skillforge visibility get my-skill
```

Every visibility change emits a row in `skill_events` (audit log). Non-admins get 403. Pre-v7 skills default to `project` visibility tied to their origin — see [MIGRATING-v6-to-v7.md](../../docs/MIGRATING-v6-to-v7.md).

## Commands

### skillforge status
Show current project, installed skills count, and available updates.
```bash
skillforge status
```

### skillforge list
List all skills in the current project with install status.
```bash
skillforge list
```

### skillforge install <name>
Download and install a skill. Auto-scopes to current project.
```bash
skillforge install epic-validator
skillforge install code-reviewer --project-id <uuid>  # explicit project
```

### skillforge upload <name-or-path>
Upload a skill to the registry. Resolves skill names from your skills directory.
```bash
skillforge upload adr-walkthrough                    # by name
skillforge upload ./path/to/skill/                   # by path
skillforge upload adr-walkthrough --project-id <uuid> # explicit project
```

### skillforge search <query>
Search the skill registry with hybrid keyword + semantic search.
```bash
skillforge search "validator"
skillforge search "code review" --limit 5
```

### skillforge update [name]
Update one or all installed skills to latest version.
```bash
skillforge update                    # update all
skillforge update epic-validator     # update specific
```

### skillforge init --project <name>
Initialize project context. Downloads required skills.
```bash
skillforge init --project Modernisation
```

### skillforge config <set|get|list>
Manage CLI configuration.
```bash
skillforge config list
skillforge config set skills_dir ~/.claude/skills
skillforge config get server_url
```

## Workflow

1. **Check state**: `skillforge status` -- see what's installed and what needs updating
2. **Browse skills**: `skillforge list` -- see all project skills with install markers
3. **Act**: `skillforge install <name>` or `skillforge upload <name>` as needed
4. **Verify**: `skillforge status` -- confirm changes

## Error Handling

| Error | Fix |
|-------|-----|
| "Not authenticated" | `skillforge auth login --server <url> --email <email> --password <pass>` |
| "No project configured" | `skillforge init --project <name>` |
| "Skill not found" | `skillforge search <query>` to find the correct name |
| "No --project-id specified" | `skillforge init --project <name>` to set default project |

## Gate Contract (v7.0)

Before `skillforge upload` accepts a skill, it must pass 3 gates:

1. **README content** — present, ≥200 characters, not whitespace-only
2. **evals.json** — valid JSON array with ≥1 eval case, AND at least one SkillEval row (A9 hybrid)
3. **SKILL.md description** — frontmatter `description` field set and non-empty

Full contract + failure modes + how-to-pass: see [docs/GATES.md](../../docs/GATES.md).

Upload failures return HTTP 422 with a `rule_slug` field (e.g., `readme-min-length`, `evals-min-one-case`, `description-set`) that deep-links to the matching anchor in GATES.md.
