# Design Principles Reference

Judgment criteria for designing skills. Read this at Phase 3 (Design).

---

## 1. The Essence of a Skill

A skill is the **externalization of judgment criteria** — not just procedures, but the decisions that produce consistent quality. Two things must be fixed simultaneously:

- **Process reproducibility**: the same steps every time (workflow)
- **Judgment reproducibility**: the same quality decisions every time (standards embedded in instructions)

If a skill only fixes the process, different runs produce different quality. If it only fixes the judgment, the process varies wildly. Both must be locked down.

---

## 2. Four Design Judgment Tests

Apply these to every piece of content when deciding where it belongs:

### Test 1: "Same every time?"

If yes, make it a script. Scripts are deterministic; language instructions are not.

Examples: frontmatter validation, line counting, reference integrity checks.

### Test 2: "Only needed in a specific phase?"

If yes, put it in a separate reference file loaded only at that phase.

Examples: survey methodology (Phase 1-2), testing methodology (Phase 7).

### Test 3: "Is the default output unsatisfactory?"

Only write instructions when you need to shift Claude's default convergence point. Write negation rules to push away from failure modes rather than exhaustively describing ideal behavior.

### Test 4: "What must NOT happen?"

Often more important than what should happen. Define prohibitions explicitly.

Examples: "Do NOT include README.md", "Do NOT hardcode API keys".

---

## 3. Progressive Disclosure Design

| Layer | Content | Budget | Loaded when |
|-------|---------|--------|-------------|
| 1. Metadata | name + description | ~100 tokens | Always (all skills) |
| 2. Instructions | SKILL.md body | < 5000 tokens | When skill activates |
| 3. Resources | references/, scripts/, assets/ | As needed | When specific phase requires |

Rules:
- SKILL.md = workflow skeleton only
- Domain knowledge → references/
- Deterministic operations → scripts/
- Each reference file has a "read when" signal in SKILL.md
- File references one level deep only — no chains

---

## 4. Detection (Description Design)

The description determines whether the skill activates at all. Treat it as a first-class design activity.

### Writing principles

- **Imperative phrasing**: "Use this skill when..." not "This skill does..."
- **User intent focus**: what the user wants to achieve, not internal mechanics
- **Be pushy**: include contexts where the skill applies even without explicit domain mention
- **Negative conditions**: state what the skill is NOT for

### Quality checklist

```
[ ] WHAT the skill does (first sentence)
[ ] WHEN to use it ("Use when..." with specific user phrases)
[ ] HOW it helps (capabilities or differentiators)
[ ] WHAT it produces (output format)
[ ] What it does NOT do (negative conditions)
[ ] ≤ 1024 characters
[ ] Natural user language included
```

### Early validation

Draft 5 should-trigger and 5 should-not-trigger queries at design time. If the description doesn't clearly match/exclude them, revise before proceeding.

---

## 5. Design Pattern Selection

| Pattern | When to use | Example |
|---------|-------------|---------|
| **Sequential** | Ordered multi-step process | Report: gather → analyze → format → output |
| **Iterative Refinement** | Quality improves through cycles | Image: generate → evaluate → regenerate |
| **Context-aware Selection** | Different tools based on input | API: OpenAI vs Gemini by availability |
| **Domain Intelligence** | Deep specialized knowledge | Legal: regulatory requirements embedded |
| **Multi-MCP** | Multiple external services | Dashboard: database + charts + notifications |

Most skills use 2-3 patterns. Name the combination explicitly in the design document.

---

## 6. Security Principles

Every target skill must be checked for:

- **No hardcoded credentials**: API keys, passwords, tokens from env vars or runtime input only
- **No dangerous commands**: `rm -rf` without path safeguards, `curl | bash`, `eval` on user input
- **No data exfiltration**: no sending user data externally without consent
- **No XML injection**: no `<` or `>` in frontmatter

---

## 7. Skill-or-Not Filter (Detailed)

| Need pattern | Best format | Recognition signal |
|-------------|-------------|-------------------|
| "Always follow these rules for all code" | Rules (.mdc) | Universal, no context loading |
| "When I type /deploy, run this" | Commands | Explicit user trigger |
| "When the task involves X, follow this process" | **Skill** | Context-dependent, progressive disclosure |
| "Connect to our database and pull metrics" | MCP | Live external data |
| "Act as a security reviewer with read-only" | Agent | Persona + tool constraints |

Gray areas: suggest starting as a Skill, extract always-on components to Rules later.

---

## 8. SKILL.md Recommended Structure

```markdown
---
name: target-skill-name
description: >
  [WHAT]. Use when [WHEN with trigger phrases].
  [Capabilities]. [Output format].
  Do NOT use for [negative conditions].
---

# Target Skill Name

[1-2 sentence overview]

## Prerequisites
## Use Cases
## Workflow Overview
## [Phase sections with input → steps → output → transition]
## Quick Example
## Troubleshooting
## References
```

---

## 9. Instruction Writing Principles

- **Imperative voice**: "Run X", "Verify Y" — not "You might want to..."
- **Explain why**: reasoning outperforms ALWAYS/NEVER directives
- **Skip what Claude knows**: basic concepts waste tokens and lower Tessle scores
- **Concrete over abstract**: "line count ≤ 500" beats "appropriate length"
- **Important instructions first**: critical rules before detailed procedures
