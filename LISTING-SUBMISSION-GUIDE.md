# ESP32-AI-Agent-Skill — Plugin Listing Submission Guide

> Ready-to-run commands and PR content for submitting to every major Claude plugin/skill listing on GitHub, plus the official Anthropic registry.

---

## Quick Reference — Target Repositories

| # | Repository | Stars | Format | Category Fit |
|---|-----------|-------|--------|-------------|
| 1 | [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit) | 4k+ | Table in README + plugin folder | Plugins |
| 2 | [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | 2k+ | Bulleted list `[Name](url) by Author - desc` | Skills / Plugins |
| 3 | [ComposioHQ/awesome-claude-plugins](https://github.com/ComposioHQ/awesome-claude-plugins) | 1k+ | Bulleted list `[name](url) - desc` by category | Plugins |
| 4 | [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) | 1k+ | Table + bulleted collections | Individual Skills |
| 5 | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | 500+ | Bulleted list `[Name](url) - desc` | Skills |
| 6 | [jqueryscript/awesome-claude-code](https://github.com/jqueryscript/awesome-claude-code) | 1k+ | Badge + link + star count | Plugins |
| 7 | [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | 500+ | Domain table | Engineering skills |
| 8 | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | Official | Form submission | Official registry |

---

## 0. Official Anthropic Plugin Registry

**Submission URL:** https://clau.de/plugin-directory-submission

This is the official Anthropic-managed directory. Submit via the form (not a PR). Key info to provide:

- **Plugin Name:** ESP32
- **GitHub URL:** https://github.com/ezrover/ESP32-AI-Agent-Skill
- **Description:** Expert ESP32 embedded systems guidance — chip selection across 9 variants, GPIO validation with anti-bricking safety checks, code generation for Arduino and ESP-IDF, LVGL UI references (v8.2–v9.5), and 60+ Waveshare board pinouts.
- **Author:** ezrover
- **License:** MIT
- **Install command:** `claude /install-plugin https://github.com/ezrover/ESP32-AI-Agent-Skill`

---

## 1. rohitg00/awesome-claude-code-toolkit

**Format:** Markdown table row in README + optional plugin folder submission.
**CONTRIBUTING.md:** Yes — fork → branch → add → PR. Commit format: `"Add new-skill: description"`.

### README table entry (add under the Plugins table)

```markdown
| [ESP32-AI-Agent-Skill](https://github.com/ezrover/ESP32-AI-Agent-Skill) | | Expert ESP32 embedded systems plugin — chip selection across 9 variants, GPIO validation with anti-bricking safety, Arduino/ESP-IDF code gen, LVGL v8–v9.5 refs, 60+ Waveshare board pinouts. Install: `claude /install-plugin https://github.com/ezrover/ESP32-AI-Agent-Skill` |
```

### Commands

```bash
# Fork and clone
gh repo fork rohitg00/awesome-claude-code-toolkit --clone
cd awesome-claude-code-toolkit

# Create branch
git checkout -b add-esp32-ai-agent-skill

# Edit README.md — add the table row above in the Plugins section
# (manually or with sed)

# Commit and push
git add README.md
git commit -m "Add ESP32-AI-Agent-Skill: embedded systems plugin with GPIO validation and code gen"
git push origin add-esp32-ai-agent-skill

# Open PR
gh pr create \
  --title "Add ESP32-AI-Agent-Skill plugin" \
  --body "$(cat <<'EOF'
## What

Adds [ESP32-AI-Agent-Skill](https://github.com/ezrover/ESP32-AI-Agent-Skill) to the plugins table.

## Description

A Claude Code plugin for ESP32 embedded systems development:
- Chip selection guidance across 9 ESP32 variants (ESP32, S2, S3, C3, C6, C2, C5, H2, P4)
- GPIO pin validation with anti-bricking safety checks (strapping pins, flash pins, ADC2/WiFi conflicts)
- Code generation for Arduino and ESP-IDF frameworks
- LVGL reference docs (v8.2–v9.5) with migration guides
- 60+ Waveshare board pinout tables
- 50 automated tests, MIT licensed

Install: `claude /install-plugin https://github.com/ezrover/ESP32-AI-Agent-Skill`
EOF
)"
```

---

## 2. hesreallyhim/awesome-claude-code

**Format:** Bulleted list — `[Name](url) by [Author](author-url) - Description`.
**Best section:** 🧠 Agent Skills → or 🔌 Claude Plugins

### Entry to add

```markdown
- [ESP32-AI-Agent-Skill](https://github.com/ezrover/ESP32-AI-Agent-Skill) by [ezrover](https://github.com/ezrover) - Expert ESP32 embedded systems plugin with chip selection across 9 variants, GPIO pin validation (anti-bricking safety checks for strapping pins, flash pins, ADC2/WiFi conflicts), Arduino and ESP-IDF code generation, LVGL v8.2–v9.5 reference docs, and 60+ Waveshare board pinouts.
```

### Commands

```bash
gh repo fork hesreallyhim/awesome-claude-code --clone
cd awesome-claude-code
git checkout -b add-esp32-ai-agent-skill

# Edit README.md — add entry in the Plugins section

git add README.md
git commit -m "Add ESP32-AI-Agent-Skill: embedded systems plugin"
git push origin add-esp32-ai-agent-skill

gh pr create \
  --title "Add ESP32-AI-Agent-Skill" \
  --body "$(cat <<'EOF'
Adds ESP32-AI-Agent-Skill — a Claude Code plugin for ESP32 embedded systems development with GPIO validation, code generation, and hardware reference docs.

**Repo:** https://github.com/ezrover/ESP32-AI-Agent-Skill
**License:** MIT | **Tests:** 50 automated tests
EOF
)"
```

---

## 3. ComposioHQ/awesome-claude-plugins

**Format:** Bulleted list under category headers — `[name](url) - Description`.
**Best section:** Backend & Architecture, or a new "Hardware & Embedded" section.
**CONTRIBUTING:** Fork → add plugin folder + README entry → PR. Must address genuine use case, not duplicate existing.

### Entry to add

```markdown
- [ESP32-AI-Agent-Skill](https://github.com/ezrover/ESP32-AI-Agent-Skill) - ESP32 embedded systems expert with chip selection across 9 variants, GPIO validation with anti-bricking safety checks, Arduino/ESP-IDF code generation, LVGL v8–v9.5 references, and 60+ Waveshare board pinouts.
```

### Commands

```bash
gh repo fork ComposioHQ/awesome-claude-plugins --clone
cd awesome-claude-plugins
git checkout -b add-esp32-plugin

# Edit README.md — add entry under appropriate section

git add README.md
git commit -m "Add ESP32-AI-Agent-Skill plugin for embedded systems"
git push origin add-esp32-plugin

gh pr create \
  --title "Add ESP32-AI-Agent-Skill plugin" \
  --body "$(cat <<'EOF'
## Summary

Adds ESP32-AI-Agent-Skill — the first hardware/embedded systems plugin in this collection.

- GPIO pin validation with safety checks preventing hardware damage
- Code generation for Arduino and ESP-IDF
- 9 ESP32 variants, LVGL UI, 60+ Waveshare boards
- MIT licensed, 50 automated tests

**Repo:** https://github.com/ezrover/ESP32-AI-Agent-Skill
EOF
)"
```

---

## 4. travisvn/awesome-claude-skills

**Format:** Table for individual skills, bulleted list for collections.
**Best section:** Individual Skills table (Hardware/IoT category) or Tools section.

### Table entry

```markdown
| [ESP32-AI-Agent-Skill](https://github.com/ezrover/ESP32-AI-Agent-Skill) | ESP32 embedded systems — chip selection, GPIO validation with anti-bricking safety, Arduino/ESP-IDF code gen, LVGL v8–v9.5 refs, 60+ Waveshare pinouts |
```

### Commands

```bash
gh repo fork travisvn/awesome-claude-skills --clone
cd awesome-claude-skills
git checkout -b add-esp32-skill

# Edit README.md — add table row in Individual Skills section

git add README.md
git commit -m "Add ESP32-AI-Agent-Skill for embedded systems development"
git push origin add-esp32-skill

gh pr create \
  --title "Add ESP32-AI-Agent-Skill" \
  --body "$(cat <<'EOF'
Adds ESP32-AI-Agent-Skill — embedded systems skill with GPIO validation, code generation, and hardware reference documentation for 9 ESP32 variants.

https://github.com/ezrover/ESP32-AI-Agent-Skill
EOF
)"
```

---

## 5. ComposioHQ/awesome-claude-skills

**Format:** Bulleted list — `[Name](url) - Description`.
**Best section:** Development & Code Tools, or a new Hardware/IoT section.

### Entry

```markdown
- [ESP32-AI-Agent-Skill](https://github.com/ezrover/ESP32-AI-Agent-Skill) - ESP32 embedded systems with chip selection, GPIO pin validation, Arduino/ESP-IDF code generation, LVGL UI references, and Waveshare board pinouts. *By @ezrover*
```

### Commands

```bash
gh repo fork ComposioHQ/awesome-claude-skills --clone
cd awesome-claude-skills
git checkout -b add-esp32-skill

# Edit README.md

git add README.md
git commit -m "Add ESP32-AI-Agent-Skill"
git push origin add-esp32-skill

gh pr create \
  --title "Add ESP32-AI-Agent-Skill" \
  --body "Adds ESP32-AI-Agent-Skill for embedded systems development. https://github.com/ezrover/ESP32-AI-Agent-Skill"
```

---

## 6. jqueryscript/awesome-claude-code

**Format:** Badge + `**name** (⭐ count) - Description`. Badge: ✨ for <100 stars.
**Best section:** 🔌 Claude Plugins or 🧠 Agent Skills

### Entry

```markdown
- ✨ **[ESP32-AI-Agent-Skill](https://github.com/ezrover/ESP32-AI-Agent-Skill)** - ESP32 embedded systems plugin with chip selection across 9 variants, GPIO validation with anti-bricking safety, Arduino/ESP-IDF code gen, LVGL v8–v9.5 refs, and 60+ Waveshare board pinouts.
```

### Commands

```bash
gh repo fork jqueryscript/awesome-claude-code --clone
cd awesome-claude-code
git checkout -b add-esp32-plugin

# Edit README.md

git add README.md
git commit -m "Add ESP32-AI-Agent-Skill plugin"
git push origin add-esp32-plugin

gh pr create \
  --title "Add ESP32-AI-Agent-Skill" \
  --body "Adds ESP32-AI-Agent-Skill — first embedded/hardware plugin. GPIO validation, code gen, 9 ESP32 variants. https://github.com/ezrover/ESP32-AI-Agent-Skill"
```

---

## 7. alirezarezvani/claude-skills

**Format:** Domain table with columns: Domain | Count | Highlights | Details folder path.
**Note:** This repo bundles skills directly. Best approach is to open an issue suggesting inclusion rather than a PR, since they'd need to integrate your skill into their folder structure.

### Issue title

```
Feature request: Add ESP32 embedded systems skill
```

### Issue body

```markdown
## Suggestion

Add an ESP32 embedded systems skill covering:
- Chip selection across 9 ESP32 variants
- GPIO pin validation with anti-bricking safety checks
- Arduino and ESP-IDF code generation
- LVGL v8.2–v9.5 reference documentation
- 60+ Waveshare board pinout tables

The skill is open source (MIT) and available as a Claude Code plugin:
https://github.com/ezrover/ESP32-AI-Agent-Skill

This would be the first hardware/embedded engineering domain in the collection.
```

---

## Batch Script — Submit All PRs

Save this as `submit-all-listings.sh` and run after installing `gh`:

```bash
#!/bin/bash
set -e

REPO_URL="https://github.com/ezrover/ESP32-AI-Agent-Skill"
PLUGIN_DESC="ESP32 embedded systems plugin — chip selection across 9 variants, GPIO validation with anti-bricking safety, Arduino/ESP-IDF code gen, LVGL v8–v9.5 refs, 60+ Waveshare board pinouts"

# List of repos to fork and PR
declare -A REPOS
REPOS[rohitg00/awesome-claude-code-toolkit]="add-esp32-ai-agent-skill"
REPOS[hesreallyhim/awesome-claude-code]="add-esp32-ai-agent-skill"
REPOS[ComposioHQ/awesome-claude-plugins]="add-esp32-plugin"
REPOS[travisvn/awesome-claude-skills]="add-esp32-skill"
REPOS[ComposioHQ/awesome-claude-skills]="add-esp32-skill"
REPOS[jqueryscript/awesome-claude-code]="add-esp32-plugin"

for repo in "${!REPOS[@]}"; do
  branch="${REPOS[$repo]}"
  dirname=$(echo "$repo" | cut -d'/' -f2)
  
  echo "=== Processing $repo ==="
  gh repo fork "$repo" --clone --default-branch-only
  cd "$dirname"
  git checkout -b "$branch"
  
  echo ""
  echo ">>> Now manually edit README.md in $(pwd) <<<"
  echo ">>> Add the ESP32-AI-Agent-Skill entry in the correct format <<<"
  echo ">>> Then run: git add README.md && git commit -m 'Add ESP32-AI-Agent-Skill' && git push origin $branch <<<"
  echo ""
  
  cd ..
done

echo ""
echo "=== Don't forget: ==="
echo "1. Submit to official Anthropic registry: https://clau.de/plugin-directory-submission"
echo "2. Open issue on alirezarezvani/claude-skills for inclusion"
```

---

## PR Best Practices (Observed from Successful Submissions)

1. **Keep it minimal** — one entry, one file changed (README.md)
2. **Match the existing format exactly** — don't add extra columns, badges, or formatting
3. **Place in the right category** — if no hardware/embedded section exists, add near "Backend" or "Developer Productivity"
4. **PR title format:** `Add [PluginName]` or `Add [PluginName]: short description`
5. **PR body:** 3-5 bullet points about what makes it unique
6. **Unique angle:** Emphasize this is the **first hardware/embedded systems plugin** — most listings are 100% software-focused
7. **Include install command** where the format allows it
