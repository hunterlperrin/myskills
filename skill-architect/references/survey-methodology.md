# Survey and Extraction Methodology

How to research existing skills and extract reusable knowledge. Read at Phase 1 (Market Survey) and Phase 2 (Knowledge Extraction).

---

## 1. Five Survey Axes

Every market survey must explore all five:

| Axis | What to find | Why it matters |
|------|-------------|---------------|
| **1. Direct competitors** | Skills solving the same problem | Avoid reinventing; learn from their structure |
| **2. Quality evaluation** | Tools and standards for measuring skill quality | Establishes the bar for the target skill |
| **3. Official specs & guides** | Platform documentation, best practice guides | Authoritative constraints and patterns |
| **4. Ecosystem & distribution** | Marketplaces, registries, CLI tools | Context on how skills are shared and discovered |
| **5. Adjacent domains** | Rules, Commands, MCP approaches to similar problems | Ensures "Skill" is the right format; borrows cross-domain patterns |

If an axis yields nothing after reasonable search effort, note it explicitly rather than silently skipping.

---

## 2. Search Destinations (8 Starting Points)

Search these in order. Add domain-specific sources as needed.

| # | Destination | What to search | URL pattern |
|---|------------|----------------|-------------|
| 1 | anthropics/skills | Official Anthropic skills repo | github.com/anthropics/skills |
| 2 | GitHub general | Community skills for the target domain | github.com search: "[domain] SKILL.md" |
| 3 | LobeHub | Skills marketplace | lobehub.com/skills |
| 4 | Playbooks | Skill registry | playbooks.com/skills |
| 5 | Smithery | Skill and MCP registry | smithery.ai/skills |
| 6 | SkillsMP | Large skill marketplace | skillsmp.com |
| 7 | agentskills.io | Official spec + guides | agentskills.io |
| 8 | Domain-specific | Academic papers, industry tools, existing automation | Web search with domain keywords |

### First action in every Phase 1

Fetch `https://agentskills.io/specification` to confirm the latest spec. Requirements may have changed since skill-architect was last updated.

---

## 3. Search Execution

### Query patterns

Use short, specific queries (1-6 words):
- `"[domain] SKILL.md"` — finds skill repos
- `"[domain] agent skill"` — broader
- `"[domain] automation workflow"` — adjacent approaches
- `"[domain] .cursorrules"` or `"[domain] .mdc"` — Rules-based alternatives

### Recording discoveries

For each discovery, capture:
```
Name: [skill/tool name]
Source: [URL]
Type: [skill | tool | platform | spec | guide]
Importance: ★★★ / ★★☆ / ★☆☆
One-line summary: [what it does]
```

---

## 4. Importance Rating Criteria

| Rating | Definition | Action required |
|--------|-----------|----------------|
| ★★★ | Directly solves the same problem OR defines quality standards we must meet | Read SKILL.md in full. Obtain complete file structure. |
| ★★☆ | Solves a related problem OR contains reusable patterns | Read key sections. Understand structure and approach. |
| ★☆☆ | Tangentially relevant OR confirms our approach | Skim overview. Note existence. |

---

## 5. Mapping Table Format

Create a table mapping discoveries to the target skill's phases:

```markdown
| Discovery | Target Phase | Relevance | Importance | Key takeaway |
|-----------|-------------|-----------|------------|-------------|
| [name]    | Phase [N]   | [why]     | ★★★       | [what to use] |
```

---

## 6. Difference Analysis

For each discovery, explicitly answer:
- What does this do better than our planned approach?
- What does our approach do better?
- What should we adopt?
- What should we intentionally not adopt? (with reason)

Structure as a comparison matrix for ★★★ discoveries:

```markdown
| Feature | Our approach | [Competitor] | Adopt? |
|---------|-------------|-------------|--------|
| [feature] | [our way] | [their way] | Yes/No — [reason] |
```

---

## 7. Survey Quality Criteria

Declare these at the start of Phase 1 and verify at the end:

- **Coverage**: all 5 axes explored, minimum 3 discoveries per axis (or explicit "nothing found")
- **Depth**: every ★★★ item has full SKILL.md text obtained
- **Difference analysis**: systematic comparison for every ★★★ and ★★☆ item
- **Freshness**: all sources from within the past 12 months preferred; note any older sources

---

## 8. Knowledge Extraction (Phase 2)

### Five extraction categories

For each ★★★ and ★★☆ discovery, extract into these categories:

| Category | What to extract | Example |
|----------|----------------|---------|
| **Structure patterns** | File organization, progressive disclosure, directory layout | "References split by phase, not by topic" |
| **Code fragments** | Reusable scripts, CLI patterns, automation snippets | "validate.py checks frontmatter with pyyaml" |
| **Concepts & principles** | Design philosophy, quality rules, anti-patterns | "Description carries entire burden of triggering" |
| **Templates** | Formats, checklists, document structures | "Grading format: {text, passed, evidence}" |
| **Quality criteria** | Evaluation standards, benchmarks, pass/fail definitions | "Tessle Implementation 11/12 minimum" |

### Integration table format

Map each extracted element to the target skill:

```markdown
| Element | Source | Target Phase | Use method |
|---------|--------|-------------|------------|
| [what]  | [from] | Phase [N]   | As-is / Adapt: [how] |
```

"As-is" = use without modification. "Adapt" = must specify what changes and why.

### Extraction quality criteria

Declare at start of Phase 2:

- **Completeness**: all 5 categories covered for every ★★★ item
- **Mapping precision**: every element mapped to a specific target Phase (no "generally useful")
- **Difference clarity**: "as-is" vs "adapt" clearly distinguished, adaptations specified
