---
name: skill-architect
description: >
  Design and build high-quality custom skills from requirements to tested,
  packaged output. Use when the user wants to create a new skill, build a
  custom skill for a specific workflow, automate a recurring process as a
  reusable skill, turn existing knowledge into a skill, or improve an
  existing skill's quality. Systematically researches existing skills,
  extracts best practices, designs with quality standards, implements with
  QA gates, and optimizes descriptions for reliable triggering. Produces
  SKILL.md + references/ + scripts/ conforming to the Agent Skills open
  standard. Do NOT use for running existing skills, managing installations,
  or MCP server setup.
---

# Skill Architect

Design and build high-quality custom skills through a systematic 8-phase pipeline. This skill orchestrates the full lifecycle — from requirements through market research, design, QA, implementation, testing, and packaged delivery — with five user checkpoints to ensure alignment.

**Terminology**: Throughout this skill, "target skill" refers to the skill being designed and built. Do not confuse the target skill's files with skill-architect's own files.

## Prerequisites

```bash
pip install pyyaml --break-system-packages
```

Web search capability is required for Phase 1 (market survey). File system access is required for all phases.

## Use Cases

**UC1 — Build a new skill from scratch**: User describes a workflow or domain. Skill-architect researches existing solutions, designs the skill structure, builds it, and delivers a tested package.

**UC2 — Turn an existing process into a skill**: User has a working process (documented or undocumented). Skill-architect formalizes it into a reusable skill with proper structure, quality standards, and testing.

**UC3 — Improve an existing skill's quality**: User has a skill that works but isn't well-structured or triggers unreliably. Skill-architect applies QA standards and description optimization.

## Workflow Overview

```
Phase 0: Requirements ──────────────── >>> USER APPROVAL 1 <<<
Phase 1: Market Survey ─────────────── >>> USER APPROVAL 2 <<<
Phase 2: Knowledge Extraction ──────── >>> USER APPROVAL 3 <<<
Phase 3: Design ────────────────────── >>> USER APPROVAL 4 <<<
Phase 4: Design QA ─────────────────── (auto)
Phase 5: Implementation ────────────── (auto)
Phase 6: Implementation QA ─────────── >>> USER APPROVAL 5 <<<
Phase 7: Testing & Final Output ────── (complete)
```

Five interaction points. Everything else is autonomous.

## Quality Declaration Protocol

Execute this protocol at the start of **every Phase without exception**, including Phase 0 and Phase 6:

```
1. DECLARE: "Quality criteria for this Phase: [state 1-3 specific, verifiable criteria]"
2. EXECUTE: Perform the Phase's work
3. VERIFY: "Self-check against declared criteria: [PASS/FAIL for each criterion]"
4. RESOLVE: If any FAIL, fix before proceeding to next Phase
```

Phase-specific criteria guidelines:

| Phase | Declare what |
|-------|-------------|
| 0 | Completeness of requirements (all 6 questions answered, use cases defined) |
| 1 | Survey coverage (5 axes, ★★★ depth, difference analysis, freshness) |
| 2 | Extraction completeness (5 categories, mapping precision, difference clarity) |
| 3 | Spec compliance (agentskills.io), Tessle Discovery 12/12 for description |
| 4 | QA rigor (number of checks run, deficiencies found) |
| 5 | Zero syntax errors, 100% reference integrity, zero design deviations |
| 6 | Different verification types than Phase 4 (content accuracy, not structural) |
| 7 | Test coverage (trigger rate, functional test pass rate) |

---

## Phase 0: Requirements Definition

### Step 1 — Skill-or-not filter

Before anything else, determine if a Skill is the right format:

| User's need | Best format | Why |
|-------------|-------------|-----|
| Always-on coding standards | Rules (.mdc / .instructions.md) | Needs constant context, no dynamic loading |
| Explicit user-triggered action | Commands / Prompts | User-invoked, not model-invoked |
| Context-dependent knowledge + procedures | **Skill** | Progressive disclosure adds value |
| Live external data access | MCP | Tool connection, not knowledge package |
| Autonomous goal pursuit with tool constraints | Agent | Persona + permission boundaries |

If the answer is not Skill, tell the user and suggest the appropriate format. If it is Skill, proceed.

### Step 2 — Collect requirements

Ask these 6 questions (adapt phrasing to the conversation):

```
1. What should this skill enable Claude to do? (purpose and goal)
2. When should this skill trigger? (activation conditions, user phrases)
3. What's the expected output format? (file types, structure)
4. Should we set up test cases? (is output objectively verifiable?)
5. What are the quality criteria? (domain-specific definition of "good")
6. What tools or APIs are needed? (dependencies, external services)
```

### Step 3 — Define use cases

For each use case:
```
Use Case: [name]
Trigger: [what the user says or does]
Steps: [what the skill does]
Result: [what the user receives]
```

Define 2-3 use cases. Save as `requirements.md`.

### >>> INTERACTION POINT 1 <<<

Present `requirements.md` to the user. Ask: "Are these requirements complete? Anything to add or change?"

**Wait for user response.** Do not proceed until explicitly approved.

---

## Phase 1: Market Survey

Before starting, read `references/survey-methodology.md` for the complete survey framework.

**Quality declaration**: Coverage across 5 axes, ★★★ skills read in full, difference analysis for all discoveries, information freshness verified.

### Steps

1. Fetch `https://agentskills.io/specification` to confirm latest spec requirements.
2. Search the 5 axes defined in `references/survey-methodology.md`:
   - Direct competitors (skills solving the same problem)
   - Quality evaluation tools (how to measure skill quality)
   - Official specifications and guides
   - Ecosystem and distribution platforms
   - Adjacent domain approaches (Rules, Commands, MCP alternatives)
3. For each discovery, assign importance: ★★★ (full read) / ★★☆ (key points) / ★☆☆ (overview).
4. Build a mapping table: target skill Phase × discovered skill × relevance × importance.
5. Write difference analysis: what each discovery adds, what's better than our approach, what's worse.
6. If web search is unavailable:
   - Ask the user for known skill repository URLs
   - Directly fetch anthropics/skills, agentskills/agentskills repos
   - Ask user to provide reference skill files
7. Self-verify against declared quality criteria.

Save as `survey.md`.

### >>> INTERACTION POINT 2 <<<

Present `survey.md`. Ask: "Is the survey scope sufficient? Anything else to investigate?"

**Wait for user response.**

---

## Phase 2: Knowledge Extraction

Continue using `references/survey-methodology.md` (extraction sections).

**Quality declaration**: All 5 categories covered, every element mapped to a target skill Phase, "as-is" vs "adapted" clearly distinguished.

### Steps

1. Read ★★★ skills in full. Read ★★☆ key sections. Skim ★☆☆.
2. Extract into 5 categories:
   - Structure patterns (file organization, progressive disclosure)
   - Code fragments (scripts, CLI patterns)
   - Concepts and principles (design philosophy, quality rules)
   - Templates (formats, checklists)
   - Quality criteria (evaluation standards, benchmarks)
3. For each element: mark "use as-is" or "adapt" (with specific adaptation noted).
4. Create an integration table mapping each element to the target skill's Phase.
5. Self-verify against declared quality criteria.

Save as `extraction.md`.

### >>> INTERACTION POINT 3 <<<

Present `extraction.md`. Ask: "Are the extractions accurate? Anything missing?"

**Wait for user response.**

---

## Phase 3: Design

Before starting, read `references/design-principles.md` for design judgment criteria.

**Quality declaration**: agentskills.io spec compliance, Tessle Discovery 12/12 for description, all design decisions justified.

Execute these sub-steps in order:

### Sub-step 1 — File structure

Decide what files the target skill needs. Apply the 4 design tests from `references/design-principles.md`:
- Same every time? → script
- Only needed in specific phase? → separate reference file
- Default behavior unsatisfactory? → write negation rules
- What must NOT happen? → define prohibitions

Result: directory tree with purpose and line budget for each file.

### Sub-step 2 — Workflow design

Define the target skill's phases: inputs, processing steps, outputs, transitions (auto or user checkpoint).

### Sub-step 3 — Detection (description design)

Write the target skill's frontmatter description. Verify against Tessle Discovery:
- Specificity: multiple concrete actions listed (3/3)
- Completeness: WHAT + WHEN both present (3/3)
- Trigger Term Quality: natural user phrases included (3/3)
- Distinctiveness: negative conditions, no scope overlap (3/3)

Draft 5 should-trigger and 5 should-not-trigger queries as early validation.

### Sub-step 4 — Interaction point design

Define where the target skill pauses for user input and what it presents at each point.

Save as `design.md`.

### >>> INTERACTION POINT 4 <<<

Present `design.md`. Ask: "Does this design look right? Any changes to the structure or approach?"

**Wait for user response.**

---

## Phase 4: Design QA

Read `references/quality-standards.md` for the complete quality framework.

This is **design-level QA**: the target skill's files do not exist yet. Check the design document against standards. Detection target: structural gaps, spec violations, filter omissions, missing use cases.

### Steps

1. Run `references/quality-standards.md` checklist against `design.md`:
   - Tessle Discovery (4 dimensions × description)
   - Tessle Implementation (4 dimensions × planned SKILL.md structure)
   - Tessle Validation (all pass/fail items against planned frontmatter)
   - Anthropic 30-item checklist (Before you start + During development items)
   - agentskills.io spec constraints (name, description, line count, directory rules)
   - Domain-specific quality criteria (from Phase 0 requirements)
2. List every deficiency found.
3. Define a fix for each deficiency.
4. Apply all fixes to `design.md`.

Output: `design_qa_report.md` + updated `design.md`.

**Proceed automatically to Phase 5.**

---

## Phase 5: Implementation

**Quality declaration**: Zero syntax errors, 100% reference integrity, zero deviations from QA'd design.

### Steps

1. Create the target skill's directory structure per `design.md`.
2. Write SKILL.md following the design exactly.
3. Write each references/ file following the design's section outlines.
4. Write each scripts/ file following the design's interface specifications.
5. For Python scripts: run syntax check (`python3 -c "import py_compile; py_compile.compile('path')"`)
6. For shell scripts: run `bash -n path`
7. Verify reference integrity:
   - Every file referenced in SKILL.md exists
   - No orphan files in references/ or scripts/
8. Count SKILL.md lines — must be ≤ 500.

Output: complete target skill folder.

**Proceed automatically to Phase 6.**

---

## Phase 6: Implementation QA

Read `references/quality-standards.md` again.

This is **implementation-level QA**: the target skill's files now exist. Inspect actual content. Detection target: content inaccuracies, ambiguous language, API name errors, knowledge duplication, security issues.

This phase checks **different things** than Phase 4: Phase 4 verified the design's logic. Phase 6 verifies the implementation's content.

### Steps

1. Run `scripts/validate_skill.py` against the **target skill folder** (not skill-architect's own folder):
   ```bash
   python scripts/validate_skill.py /path/to/target-skill/
   ```
2. Run `scripts/qa_checklist.py` against the target skill folder:
   ```bash
   python scripts/qa_checklist.py /path/to/target-skill/
   ```
3. Manual content checks:
   - Ambiguous expressions: review auto-detected instances in context
   - API names, library names, command names: web search to verify current accuracy
   - Knowledge duplication: keyword frequency across references/ files
   - Security: no hardcoded keys, no dangerous commands, no data exfiltration
4. Fix every issue found. Re-run validation.

Output: `qa_report.md` + fixed target skill folder.

### >>> INTERACTION POINT 5 <<<

Present the target skill folder and `qa_report.md`. Ask: "Here's the built skill with QA results. Ready to proceed to testing, or any changes needed?"

**Wait for user response.**

---

## Phase 7: Testing, Iteration & Final Output

Before starting, read `references/testing-methodology.md` for the complete testing framework.

### Testing

1. Design 2-3 test cases (Prompt + Expected Output + optional Input Files).
2. Run the target skill on each test case.
3. After seeing results, write assertions (programmatically verifiable preferred).
4. Grade results: {text, passed, evidence} for each assertion.

### Description optimization (if Claude Code CLI available)

Follow the full methodology in `references/testing-methodology.md`:
1. Write 20 eval queries (8-10 should-trigger + 8-10 should-not-trigger with near-misses).
2. Split 60/40 train/validation.
3. Measure trigger rates (3+ runs per query).
4. Optimize loop (max 5 iterations) — train set guides changes, validation set selects winner.

### Iteration

If test results reveal issues:
1. Identify the root cause (ambiguous instruction? missing step? wrong approach?).
2. Read execution transcripts when available.
3. Make targeted fixes — generalize from specific failures, don't overfit.
4. Re-run tests. Repeat until satisfied or diminishing returns.
5. If stuck after 5 iterations, try a structurally different approach to the problematic section.

### Final output

1. Suggest freshness metadata for the target skill:
   ```yaml
   metadata:
     last-reviewed: "YYYY-MM-DD"
     review-interval: "90d"
   ```
2. Package as ZIP (target skill folder as root, no README.md inside).
3. Generate initial prompt template for using the target skill.

Output: `[target-skill-name].zip` + `prompt.md`

---

## Quick Example

A condensed walkthrough: "Create a skill for generating client reports."

```
Phase 0 → Filter: Skill (not Rules — reports are complex, context-dependent workflows).
          Requirements: purpose = consistent client reports, output = DOCX,
          quality = follows company template, no API needed.

Phase 1 → Surveys: finds docx skill (Anthropic official), report-generator community skills,
          Tessl quality standards. Maps each to target phases.

Phase 2 → Extracts: docx skill's python-docx patterns, report-generator's template structure,
          Tessl's validation checklist. 12 elements across 5 categories.

Phase 3 → Designs: SKILL.md (report workflow) + a template-guide reference +
          a generate_report script. Description: "Generate client reports from project
          data. Use when user asks to create a report, write a client deliverable..."

Phase 4 → QA: Finds 3 issues — missing error handling, description too narrow,
          no example section. Fixes all three.

Phase 5 → Builds all files. validate_skill.py: PASS. Line count: 280.

Phase 6 → QA: Finds 1 issue — python-docx API method name outdated.
          Web searches, confirms correct method, fixes.

Phase 7 → Tests with sample project data. Report generates as expected.
          Description triggers on 8/8 should-trigger queries.
          Packages ZIP + prompt template.
```

## Troubleshooting

### Web search unavailable in Phase 1
Use fallback: ask user for repository URLs, directly fetch known repos (anthropics/skills, agentskills/agentskills), or have user provide reference skill files.

### validate_skill.py errors
- `pyyaml not found`: `pip install pyyaml --break-system-packages`
- `SKILL.md not found`: verify the path points to the target skill's root directory

### Description trigger rate won't improve
- Check if should-not-trigger queries are true near-misses (keyword overlap but different task)
- Try a structurally different description rather than incremental tweaks
- Verify the skill's scope isn't too broad — narrower skills trigger more reliably

### Target skill exceeds 500 lines
- Apply the "only needed now?" test: move details to references/
- Check for content Claude already knows (basic concept explanations are unnecessary)
- Split large sections into focused reference files linked with "Read when..." guidance

## Design Decisions

**skill-creator test infrastructure**: Testing methodology is included as knowledge in `references/testing-methodology.md`, not as bundled scripts. Reason: test cases, assertions, and grading criteria are entirely domain-specific to the target skill. Claude Code writes target-specific tests inline, guided by the methodology, rather than using generic test scripts.

## References

Read these at the indicated phase — not before:

- **`references/quality-standards.md`** — Read at Phase 4 and Phase 6. Tessle 3-axis criteria, Anthropic 30-item checklist, agentskills.io spec constraints, Phase-specific QA guidelines.

- **`references/design-principles.md`** — Read at Phase 3. Four design judgment tests, Progressive Disclosure principles, Detection methodology, pattern selection, security principles, skill-or-not filter details.

- **`references/survey-methodology.md`** — Read at Phase 1 and Phase 2. Five survey axes, 8 search destinations, importance ratings, mapping table format, 5 extraction categories, difference analysis method.

- **`references/testing-methodology.md`** — Read at Phase 7. Three-layer evaluation structure, description optimization (20 queries, train/validation split), with/without comparison, assertion design, 7 iteration principles, blind comparison, packaging.
