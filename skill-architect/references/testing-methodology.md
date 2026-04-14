# Testing and Iteration Methodology

Complete framework for testing, description optimization, iteration, and final delivery. Read at Phase 7.

---

## 1. Three-Layer Evaluation Structure

| Layer | What | When | How |
|-------|------|------|-----|
| **Layer 1: Static review** | Structure, spec compliance, instruction quality | Phase 4 + 6 | scripts/ + manual checklist |
| **Layer 2: Dynamic testing** | Triggering accuracy, functional correctness, performance | Phase 7 | Test execution + measurement |
| **Layer 3: Human review** | Subjective quality, usability, "feel" | Phase 7 | User inspection of outputs |

Phase 7 focuses on Layers 2 and 3. Layer 1 was completed in earlier phases.

---

## 2. Test Case Design

### Three components per test case

```json
{
  "id": 1,
  "prompt": "realistic user message with context",
  "expected_output": "human-readable success description",
  "files": ["optional/input/files.csv"]
}
```

### Design principles

- **Start small**: 2-3 test cases first. Expand after seeing results.
- **Vary prompts**: mix formal/casual, terse/detailed, explicit/implicit.
- **Include edge cases**: at least one boundary condition, unusual input, or ambiguous request.
- **Use realistic context**: file paths, column names, personal backstory — real users include these.

### When to add assertions

Do NOT write assertions before the first test run. You don't know what "good" looks like until you see the output. After the first run, write assertions based on what you observe.

---

## 3. Assertion Design

### Priority hierarchy

1. **Programmatically verifiable**: "output file is valid JSON", "line count ≤ 500" → write a script
2. **LLM-judgeable**: "the report includes at least 3 recommendations" → LLM grading
3. **Human-reviewable**: "the output feels professional" → human review, not an assertion

### Assertion format

```json
{
  "text": "The output includes a valid SKILL.md with frontmatter",
  "passed": true,
  "evidence": "Found SKILL.md (45 lines) with valid name and description fields"
}
```

### Assertion hygiene

- **Always-pass assertions**: remove them. They don't measure skill value.
- **Always-fail assertions**: fix the assertion, not just the skill. The assertion may be unrealistic.
- **Flaky assertions** (pass sometimes, fail sometimes): the skill's instructions may be ambiguous. Tighten the relevant instruction.

---

## 4. Description Optimization

The most systematic method for ensuring the target skill triggers reliably.

### Step 1: Write 20 eval queries

8-10 should-trigger + 8-10 should-not-trigger.

**Should-trigger variety axes**:
- Phrasing: formal ("Please create a...") vs casual ("hey can you make a...")
- Explicitness: names the domain ("build a CSV analyzer") vs describes the need ("my boss wants charts from this data")
- Detail: terse ("analyze my sales data") vs context-heavy (file paths, column names, backstory)
- Complexity: single-step vs multi-step workflows

**Should-not-trigger — prioritize near-misses**:
Near-misses share keywords but need a different skill. These are the hardest and most valuable negative tests.

Weak negatives (too easy, test nothing):
- "Write a fibonacci function" — no keyword overlap
- "What's the weather?" — obviously irrelevant

Strong negatives (near-misses):
- "Install this skill to my Claude Code" — shares "skill" keyword but is installation, not creation
- "Help me write a good SKILL.md description" — shares terminology but is a knowledge question, not a build task

**Realistic context**: include file paths (`~/Downloads/report.xlsx`), personal context ("my manager asked"), specific details.

### Step 2: Train/validation split

Split 60% train / 40% validation. Maintain the should-trigger/should-not-trigger ratio in both sets. Keep the split fixed across all iterations.

### Step 3: Measure trigger rates

Run each query 3+ times (model behavior is nondeterministic).

```
trigger_rate = times_skill_triggered / total_runs
```

Pass criteria:
- should-trigger: rate > 0.5
- should-not-trigger: rate < 0.5

### Step 4: Optimization loop (max 5 iterations)

For each iteration:
1. Evaluate on both train and validation sets
2. Analyze **train set** failures only to guide changes:
   - Should-trigger failures → description is too narrow → broaden scope
   - Should-not-trigger failures → description is too broad → sharpen boundaries
3. **Do NOT add specific keywords from failed queries** — that's overfitting. Find the general category.
4. If stuck after 3 incremental tweaks, try a **structurally different** description (different framing, different sentence structure, different emphasis).
5. Check that description stays ≤ 1024 characters.

### Step 5: Select best version

Use **validation set pass rate** to pick the winner. The last iteration is NOT always the best — earlier versions may generalize better.

---

## 5. With/Without Comparison

Compare the target skill's output against a no-skill baseline.

### Workspace structure

```
target-skill-workspace/
└── iteration-N/
    ├── eval-[test-name]/
    │   ├── with_skill/
    │   │   ├── outputs/
    │   │   ├── timing.json
    │   │   └── grading.json
    │   └── without_skill/
    │       ├── outputs/
    │       ├── timing.json
    │       └── grading.json
    └── benchmark.json
```

### timing.json format

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332
}
```

### benchmark.json format

```json
{
  "run_summary": {
    "with_skill": {
      "pass_rate": { "mean": 0.83, "stddev": 0.06 },
      "time_seconds": { "mean": 45.0, "stddev": 12.0 },
      "tokens": { "mean": 3800, "stddev": 400 }
    },
    "without_skill": {
      "pass_rate": { "mean": 0.33, "stddev": 0.10 },
      "time_seconds": { "mean": 32.0, "stddev": 8.0 },
      "tokens": { "mean": 2100, "stddev": 300 }
    },
    "delta": { "pass_rate": 0.50, "time_seconds": 13.0, "tokens": 1700 }
  }
}
```

The delta tells you the cost (time, tokens) and benefit (pass rate improvement) of the skill.

---

## 6. Seven Iteration Principles

1. **Generalize from specific failures**: fix the underlying pattern, not the specific test case
2. **Keep the skill lean**: fewer, better instructions outperform exhaustive rules
3. **Explain why**: reasoning-based instructions ("Do X because Y") > rigid directives ("ALWAYS X")
4. **Bundle repeated work**: if every test run writes a similar helper script, bundle it in scripts/
5. **Read execution transcripts**: identify whether failures come from ambiguous instructions or unnecessary work
6. **Try structural alternatives**: after 5 incremental tweaks, change the framing entirely
7. **Stop when returns diminish**: empty feedback from human review = done

---

## 7. Blind Comparison (Optional)

For comparing two versions of a skill:

1. Run both versions on the same test cases
2. Present outputs to an LLM judge anonymously (don't reveal which is which)
3. Judge scores on: organization, formatting, usability, correctness, polish
4. Analyze why the winner won — this reveals what the skill's instructions are actually contributing

Use this when assertion pass rates are similar but you suspect one version is qualitatively better.

---

## 8. Packaging and Final Delivery

### ZIP packaging

1. Verify folder name matches frontmatter `name` field
2. Run `scripts/validate_skill.py` one final time
3. Create ZIP with the skill folder as root:
   ```bash
   cd /path/to/parent && zip -r target-skill-name.zip target-skill-name/
   ```
4. Do NOT include README.md inside the skill folder

### Freshness metadata

Suggest adding to the target skill's frontmatter:
```yaml
metadata:
  last-reviewed: "YYYY-MM-DD"
  review-interval: "90d"
```

Explain to the user: this helps track when the skill should be re-evaluated for outdated API names, changed specs, or evolved best practices.

### Initial prompt template

Generate a prompt the user can give to Claude Code to use the new skill:

```
[One paragraph explaining what the skill does and when to use it]

To get started: [specific first instruction based on UC1]

For more details, the skill includes:
- references/[file1].md — [what it covers]
- references/[file2].md — [what it covers]
- scripts/[script].py — [what it does]
```

Keep it actionable. The user should be able to copy-paste and go.
