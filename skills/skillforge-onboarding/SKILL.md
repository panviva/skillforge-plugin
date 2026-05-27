---
name: skillforge-onboarding
description: Walks a new Panviva team member through SkillForge onboarding - Okta group, SSO sign-in, API key generation, plugin install, and skillforge init. Use whenever the user mentions onboarding to skillforge, installing the skillforge plugin, the SkillForge Azure URL, API keys in SkillForge, or hits errors in skillforge init. Pushy - if any SkillForge setup step is mentioned, run this skill instead of answering ad-hoc.
recommended_model: haiku
compatibility: Requires Python 3.9+, pip, git, and browser access for Okta SSO.
---

# SkillForge Onboarding

This skill walks a new user through getting SkillForge working from zero. Fixed 5-step sequence — confirm each step before moving on.

## Constants

```
SKILLFORGE_URL = https://skillforge-struong-app.victoriouspebble-7d643944.eastus.azurecontainerapps.io
```

## Step 1 — Okta group membership (admin action)

The user cannot do this themselves.

> Ping your admin and ask them to add you to the Okta group for your product (e.g. `skillforge-panviva`). Without this, Step 2 will fail with "access denied". Let me know once confirmed.

**Wait for confirmation before proceeding.**

## Step 2 — Sign in via Okta SSO

> Open `{SKILLFORGE_URL}` in your browser and sign in with your Upland SSO. You should land on the SkillForge dashboard. If Okta says "access denied", Step 1 hasn't landed yet — check with your admin.

## Step 3 — Generate an API key

> In the SkillForge UI go to **Settings → API Keys**, click **Generate**, and copy the key immediately — it won't be shown again. Save it to a password manager or scratchpad.

Ask the user to confirm they've saved it before moving on.

## Step 4 — Install the SkillForge plugin

This installs the `/skillforge` skill into Claude Code — no cloning required.

```
/plugin marketplace add panviva/upland-marketplace
/plugin install skillforge --scope user
```

**Verify:** type `/skillforge` — it should appear in the `/` menu.

Then authenticate the CLI (installed automatically by the plugin):

```bash
skillforge auth login --server {SKILLFORGE_URL} --email <your-email> --password <api-key-from-step-3>
```

**Verify:**
```bash
skillforge status
```

If `skillforge: command not found` after plugin install — the CLI wasn't bootstrapped yet. Run:
```bash
pip install git+https://github.com/upld-internal/skillforge.git
```

## Step 5 — Initialize your project

```bash
skillforge init <project-name>
```

Ask the user which project they're onboarding into — don't guess. Use the exact project name from the SkillForge dashboard.

**Verify:**
```bash
skillforge list
```

Skills marked `[x]` are installed and ready. Restart Claude Code to load them.

## Updating Later

| What to update | Command |
|---|---|
| Project skills to latest versions | `skillforge update` |
| The SkillForge CLI | `pip install --upgrade git+https://github.com/upld-internal/skillforge.git` |
| The Claude Code plugin itself | `/plugin update skillforge` |

## Error Reference

| Symptom | Likely cause | Fix |
|---|---|---|
| Okta "access denied" | Step 1 not done | Ping admin |
| API key dialog closed before copy | Clicked away | Generate new key, delete unused |
| `skillforge: command not found` | CLI not bootstrapped | `pip install git+https://github.com/upld-internal/skillforge.git` |
| `init` returns 401 | Wrong api_key | Re-run `skillforge auth login` |
| `init` returns 404 on project | Wrong project name or wrong Okta group | Check name in dashboard |
