# SkillForge Hierarchy

Reference for the SkillForge organization structure, skill metadata, and onboarding steps.

## Organizational Hierarchy

```
Upland (Organization)
└── Panviva (Product Group)
    └── Modernisation (Project)
        └── Members (Individual developers)
```

Each level controls:
- **Upland** — platform-level skills, cross-organization standards
- **Panviva** — team-shared skills for the Panviva product group
- **Modernisation** — project-specific skills for the modernisation workstream
- **Members** — personal skills, visible only to the individual

Skills flow downward (Upland skills visible to all below) but not upward (Member skills not visible to team).

## SkillForge URLs

```
SKILLFORGE_URL = https://skillforge-struong-app.victoriouspebble-7d643944.eastus.azurecontainerapps.io
SKILLFORGE_REPO = git+https://github.com/panviva/pv-ai-skillforge.git
```

## Skill Metadata Schema

Each skill in SkillForge has:

```json
{
  "id": "uuid",
  "name": "skill-name-kebab-case",
  "display_name": "Human Readable Name",
  "description": "What this skill does and when to use it",
  "version": "1.0.0",
  "owner": {
    "level": "upland | team | project | member",
    "id": "org/team/project/user id"
  },
  "visibility": "public | private",
  "tags": ["tag1", "tag2"],
  "created_by": "user@example.com",
  "created_at": "2026-01-01T00:00:00Z",
  "updated_at": "2026-01-01T00:00:00Z",
  "skill_path": "path/to/SKILL.md in registry",
  "origin": "imported | evolved | created",
  "parent_skill_ids": [],
  "compatibility": ["claude-code", "cursor"]
}
```

## SKILL.md Format (SkillForge-compatible)

```markdown
---
name: skill-name
description: "Concise description with trigger phrases"
recommended_model: claude-sonnet-4-6 | claude-haiku-4-5
compatibility: [claude-code]
version: 1.0.0
---

# Skill Name

[Body: workflow, steps, rules]
```

## 7-Step Onboarding Flow

1. **Okta group** — admin adds user to Okta group for their product (not self-serve)
2. **SSO sign-in** — open `SKILLFORGE_URL`, sign in via Okta SSO
3. **API key** — Settings → API Keys → Generate → copy immediately (shown once)
4. **Install CLI** — `pip install git+https://github.com/panviva/pv-ai-skillforge.git`
5. **Set server URL** — `skillforge config set server_url <SKILLFORGE_URL>`
6. **Set API key** — `skillforge config set api_key <key-from-step-3>`
7. **Init project** — `skillforge init <project-name>`

Steps must be done in order — steps 5-7 fail if steps 3-4 were skipped.

## CLI Commands

```bash
# Config
skillforge config set server_url <url>
skillforge config set api_key <key>
skillforge config get server_url
skillforge config get api_key      # masked output

# Skills
skillforge list                    # list all accessible skills
skillforge init <project>          # pull project's skills locally
skillforge search "query"          # search skill library
skillforge install <skill-name>    # install a specific skill
skillforge push <skill-dir>        # upload a skill to SkillForge

# Version
skillforge --version
```

## Registry Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /api/skills` | List skills (filtered by access level) |
| `GET /api/skills/<id>` | Get skill metadata |
| `POST /api/skills` | Upload new skill |
| `PATCH /api/skills/<id>` | Update skill |
| `GET /api/projects/<name>/skills` | List project skills (used by `init`) |

Auth: Bearer token (`api_key` from config).

## Common Onboarding Errors

| Error | Cause | Fix |
|---|---|---|
| Okta "access denied" | Step 1 not done | Ping admin for Okta group |
| `skillforge: command not found` | pip entry point not on PATH | `py -m skillforge` on Windows |
| `ModuleNotFoundError: No module named 'src'` | Repo packaging bug | File upstream issue |
| `init` returns 401 | api_key not set or wrong | `skillforge config get api_key` + reset |
| `init` returns 404 on project | Wrong project slug or wrong Okta group | Verify slug, check Okta |
