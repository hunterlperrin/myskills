# Quality Standards Reference

Complete quality evaluation framework for skill-architect. Read this at Phase 4 (Design QA) and Phase 6 (Implementation QA).

---

## 1. Tessle 3-Axis Quality Model

### 1a. Discovery (Activation Quality) — 12 points total

How reliably the agent finds and selects the skill.

| Dimension | 1 point | 2 points | 3 points |
|-----------|---------|----------|----------|
| **Specificity** | Vague ("helps with tasks") | Some actions listed | Multiple concrete actions with clear scope |
| **Completeness** | Only WHAT or only WHEN | Both present but one is thin | WHAT + WHEN both detailed |
| **Trigger Term Quality** | Generic terms only | Mix of technical and natural language | Comprehensive user-phrase coverage including casual variants |
| **Distinctiveness** | No scope boundaries | Some boundaries implied | Explicit negative conditions, no overlap with adjacent skills |

Target: 12/12 for every skill produced by skill-architect.

### 1b. Implementation (Instruction Quality) — 12 points total

How well the instructions guide the agent.

| Dimension | 1 point | 2 points | 3 points |
|-----------|---------|----------|----------|
| **Conciseness** | Bloated SKILL.md with inline details | Mostly lean but some sections too long | Lean SKILL.md, all details in references/ |
| **Actionability** | Abstract guidance ("handle errors properly") | Some concrete steps, some vague | Every instruction has concrete steps, commands, or templates |
| **Workflow Clarity** | Steps listed but no validation points | Steps with some checkpoints | Clear steps + verification points + iteration guidance |
| **Progressive Disclosure** | Everything in one file | Split exists but loading signals unclear | Clean 3-layer split with explicit "read when" signals |

Target: 11/12 minimum. 12/12 preferred.

### 1c. Validation (Structural Compliance) — Pass/Fail

Every item must PASS:

```
[ ] SKILL.md exists (exact case)
[ ] YAML frontmatter present with --- delimiters
[ ] name: 1-64 chars, lowercase + hyphens, no leading/trailing/consecutive hyphens
[ ] name matches parent directory name
[ ] description: 1-1024 chars, non-empty
[ ] description contains trigger hint ("Use when..." or similar imperative)
[ ] description in third person or imperative voice (not first person)
[ ] No XML angle brackets (< >) in frontmatter
[ ] SKILL.md body present (not empty after frontmatter)
[ ] SKILL.md ≤ 500 lines
[ ] Examples or code fences present in body
[ ] Output format specified somewhere in body
[ ] No README.md in skill directory
[ ] Folder name is kebab-case
```

---

## 2. Anthropic Official Checklist (Applicable Subset)

### Before you start (4 items)

```
[ ] 2-3 specific use cases identified and documented
[ ] Required tools identified (built-in commands, MCP servers, scripts)
[ ] Official guides and example skills reviewed for the target domain
[ ] Folder structure planned before writing
```

### During development (10 key items)

```
[ ] Folder named in kebab-case matching frontmatter name
[ ] SKILL.md has valid YAML frontmatter
[ ] Description explains WHAT the skill does
[ ] Description explains WHEN to use it
[ ] No XML tags in frontmatter
[ ] Instructions are actionable (numbered steps, concrete commands)
[ ] Error handling / troubleshooting section present
[ ] Examples provided (input/output or walkthrough)
[ ] References clearly linked with "read when" guidance
[ ] Skill tested with paraphrased trigger queries
```

### Before upload (5 key items)

```
[ ] 5+ should-trigger queries tested (varied phrasing)
[ ] 5+ should-NOT-trigger queries tested (near-misses)
[ ] Skill produces expected output for each use case
[ ] Line count verified ≤ 500
[ ] All referenced files exist and are reachable
```

---

## 3. agentskills.io Specification Constraints

### Frontmatter fields

| Field | Required | Constraint |
|-------|----------|------------|
| name | Yes | 1-64 chars, lowercase alphanumeric + hyphens, no leading/trailing/consecutive hyphens, must match directory name |
| description | Yes | 1-1024 chars, non-empty, should include trigger hints |
| license | No | Short license name or reference to LICENSE file |
| compatibility | No | ≤ 500 chars, environment requirements |
| metadata | No | Arbitrary key-value pairs (author, version, etc.) |
| allowed-tools | No | Space-delimited tool list (experimental) |

### Size budgets

| Component | Budget |
|-----------|--------|
| Discovery (name + description) | ~100 tokens |
| SKILL.md body | < 5000 tokens recommended |
| SKILL.md total | ≤ 500 lines |
| Reference files | Focused, one level deep |

### Permitted directories

`scripts/`, `references/`, `assets/` are the standard three. Additional directories are allowed but not recommended without good reason.

---

## 4. Phase-Specific QA Application Guide

### Phase 4 (Design QA) — Check the design document

The target skill's files do not exist yet. Verify the design against standards.

Detection targets: structural gaps, spec violations, filter omissions, missing use cases.

Actions:
1. Score the planned description against Discovery 4 dimensions
2. Score the planned SKILL.md structure against Implementation 4 dimensions
3. Run the Validation checklist against planned frontmatter values
4. Walk through the Anthropic "Before you start" items
5. Check all agentskills.io constraints against planned values
6. Verify domain-specific quality criteria from Phase 0 requirements

### Phase 6 (Implementation QA) — Check the actual files

The target skill's files now exist. Inspect actual content.

Detection targets: content inaccuracies, ambiguous language, API errors, duplication, security.

Actions:
1. Run `scripts/validate_skill.py` on the target skill folder
2. Run `scripts/qa_checklist.py` on the target skill folder
3. Review auto-detected ambiguous expressions in context
4. Web search to verify API names, library names, command names
5. Check for knowledge duplication across references/ files
6. Security scan: no hardcoded credentials, no dangerous commands, no data exfiltration

---

## 5. Quality Declaration Verification Template

```
## Phase [N] Quality Verification

Declared criteria:
1. [criterion 1]
2. [criterion 2]

Verification:
1. [criterion 1]: PASS / FAIL — [evidence]
2. [criterion 2]: PASS / FAIL — [evidence]

Deficiencies found: [N]
Resolution: [action for each FAIL]
```
