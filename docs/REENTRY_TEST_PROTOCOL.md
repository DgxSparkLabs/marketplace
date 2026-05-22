# Re-Entry Test Protocol

How we verify that our orientation artifacts (`docs/RESUME_HERE.md` + `HANDOFF.md` + the planning dossier) are good enough that a cold agent can pick up the project without misalignment.

This is a reusable test. Run it any time after substantial doc changes, after a long break, or before handing off to a new contributor. The protocol is designed so a fresh sub-agent can score itself against criteria we've documented here — without needing us to babysit the test.

---

## Why We Test the Orientation Kit

The orientation kit is only as good as how well a cold agent can use it. A nice-looking `RESUME_HERE.md` that fails to convey the WHY behind decisions will produce well-meaning agents who re-litigate settled questions. A glossary missing key terms produces agents who ask clarifying questions about facts that are documented but not findable. A dead-ends list buried at the bottom of a doc produces agents who repeat them.

Stress-testing the kit with a cold sub-agent gives us:

- **Concrete failure modes** — "the agent thought X meant Y" → we know exactly what to clarify
- **Validation that the artifacts carry the load** — if a cold agent re-orients in 90 seconds, the kit works
- **Improvement suggestions from a fresh perspective** — the cold agent sees things we've internalized and stopped noticing

The cost is low (~one sub-agent run) and the value compounds: each test makes the kit a little more durable.

---

## Five Alignment Criteria Families

A returning agent (cold sub-agent OR our future self) must demonstrate understanding of:

### 1. State Awareness
Where the project is right now.

- Active branch and last commit
- Open PR and its status
- Two completed work phases and one pending phase
- Next concrete action (in priority order)

**Failure mode to catch:** Agent doesn't know where to look; reads the wrong file first; can't articulate where they are.

### 2. Decision Discipline
The 20 locked decisions are load-bearing, not open questions.

- When asked "should we do X instead?", reach for the decisions table
- When asked "why was Y chosen?", cite the rationale from RESUME_HERE.md or PLAN doc
- Do not propose to re-litigate locked decisions
- Recognize that the locked-decision rationale was deliberately captured in `RESUME_HERE.md` "Top Decisions with Rationale" section

**Failure mode to catch:** Agent proposes alternatives to settled questions, treats Section 4 of the validation plan as a draft list rather than locked commitments.

### 3. Dead-End Avoidance
The "Dead Ends" section in RESUME_HERE.md exists so failed approaches don't get re-tried.

- Recognize the 10 documented dead ends and the one-sentence reasoning for each
- Don't suggest UserPromptSubmit hooks for rules (clunky, rejected)
- Don't suggest `vars.X_WHITELIST_GRANTED` gating (unnecessary; `continue-on-error` handles it)
- Don't suggest web research for current CLI surfaces (stale; use empirical CI + local instead)
- Don't suggest a council of 6 specialist agents for design review (theatrical)

**Failure mode to catch:** Agent proposes a pattern we already tried and rejected. Indicates the dead-ends section wasn't loud enough, or the agent skipped it.

### 4. Method Adherence
Use the same patterns we discovered work.

- Surface decisions via `AskUserQuestion` with 3 explicit options + a Recommended marker
- Use empirical exploration (CI or local) instead of web research for current-state CLI questions
- Treat catalog rows as the executable spec for CI assertions
- Spawn reviewer agents after locking decisions (not before — that's the work, not its review)
- Per-construct workflow organization (not per-platform)

**Failure mode to catch:** Agent reaches for inferior methods (open-ended yes/no questions instead of structured options, doc research instead of empirical exploration, per-platform workflow layout, etc.).

### 5. Scope Awareness
What's NOT in scope.

- The migration architecture is locked (PR #1) — don't propose changes
- Adding new construct types beyond the 10 Claude Code supports — not our scope
- Adding new platforms beyond the 6 we mirror — not our scope
- Building `compat-rule.yml` — explicitly rejected per decision #11
- Caching strategies are deferred to implementation-time empirical resolution — not pre-committed

**Failure mode to catch:** Agent proposes scope expansion. Indicates the "what's NOT in scope" boundary wasn't communicated.

---

## Three Test Rounds

### Round 1 — Cold Orientation
Drop the agent into the repo with minimal context. Goal: do they find `RESUME_HERE.md` quickly and read it fully?

**Measured:**
- Did they find the orientation entry point?
- Did they read it before doing anything else?
- Can they summarize the project state in 3 sentences?

**Failure mode:** They read random files first, ignore RESUME_HERE.md, or read it partially.

### Round 2 — Targeted Alignment Probes
Specific questions across the five criteria families. Each has a "right answer" that's documented somewhere in the kit.

8 questions, one per criterion (with two for the "decisions" family because it's the biggest surface area).

**Measured:**
- Per-question pass/fail
- Per-question: did they cite specific files/sections as evidence?

**Failure mode:** Vague answers that paraphrase without citing; wrong answers despite the info being available; "I don't know" answers despite the info being available.

### Round 3 — Hypothetical Drift Scenarios
Concrete scenarios designed to surface dead-end repetition or method drift.

4 scenarios, each engineered to be a tempting trap if the agent isn't well-oriented.

**Measured:**
- Does the response match what we'd actually do?
- Does the response avoid the documented dead ends?
- Does the response use the documented methods?

**Failure mode:** They take the bait — propose `compat-rule.yml`, suggest web research, etc.

---

## The Prompt Template

This is the canonical rookie-friendly framing. Copy-paste into a sub-agent invocation (general-purpose, claude with sonnet model recommended).

```
Welcome to DgxSparkLabs/marketplace.

You're joining a project mid-flight. The previous contributors finished
a long working session on 2026-05-22 and went on break. They left
orientation artifacts on disk specifically so a fresh contributor like
you (or their future selves) can pick up without losing context.

We're glad you're here. This isn't a hostile interview — your goal is
to get oriented, not to perform. The friendlier this exchange goes, the
better our orientation artifacts probably are.

We do want to verify the orientation kit works. So after you orient
yourself, please complete three short test rounds. The test results
help us improve the artifacts; failures aren't graded against you
personally — they're diagnostic data about our docs.

## Your starting point

- Working directory: C:\Users\devic\source\marketplace
- The repo has many files. The orientation artifacts were designed to
  be findable; you'll know them when you see them.
- You should NOT need to read source code (skills/, rules/, scripts/,
  tests/) to complete this exercise. Documentation and config files
  only.

## Round 1 — Cold orientation (10 minutes)

Without any further hint from us:

1. Find and read the file the previous contributors intended you to
   read first. (Hint: it's named in a way that suggests "start here.")
2. Read other files in the order it recommends.
3. In 3–5 sentences, summarize: what is this project, where is it
   right now, what's the next concrete action?

## Round 2 — Targeted alignment probes (15 minutes)

Answer each question concisely. Cite the specific file and section
where you found the answer. "I don't know" or "the docs don't say" is
a valid answer if the info genuinely isn't there — and is useful
diagnostic data.

1. (State) What branch should you be on, and what's the last commit?
   What's the next concrete action?

2. (Phases) What two major work phases have been completed, and what
   phase is pending? When was the last work session?

3. (Decisions — #1) Why does this project use job-level
   `continue-on-error: true` for Codex/Gemini matrix entries instead
   of a `vars.X_WHITELIST_GRANTED` toggle? Cite the decision.

4. (Decisions — #2) Why does `compat-rule.yml` NOT exist as a planned
   workflow? Cite the reason.

5. (Decisions — #3) Why is the workflow organization per-construct
   rather than per-platform? Cite the rationale.

6. (Methods) How would you verify whether `gemini skills list`
   requires auth in May 2026? What's the documented method here?

7. (Methods) When you encounter a design ambiguity that needs a
   decision, what's the documented pattern for resolving it?

8. (Scope) What's explicitly NOT in scope for the multi-platform
   validation work? Name 3 things.

## Round 3 — Hypothetical drift scenarios (10 minutes)

For each scenario, describe what you would do. Brief responses — 2–4
sentences each.

1. A new contributor opens a PR adding `.github/workflows/compat-rule.yml`
   with assertions like `claude plugin install rule-blast-radius@... &&
   bash ~/.claude/plugins/cache/.../activate.sh`. What's your response?

2. You need to verify what subcommands `codex` exposes in May 2026.
   The package version may have changed since the catalog was written.
   What's your approach?

3. Two design docs in this repo describe how rules are installed
   differently. One says "rules ship as plugins with activate.sh";
   another says "rules aren't installable via plugins." What's the
   resolution?

4. You're about to write the first compat workflow file. Walk through
   your first 5 steps, in order.

## Round 4 — Orientation kit feedback

Now that you've completed Rounds 1–3, please report:

1. **What was clear** — what in the orientation artifacts worked well?
2. **What was unclear** — what made you have to dig, guess, or ask?
3. **Proposed edits to RESUME_HERE.md or HANDOFF.md** — what specific
   sections or sentences would you add/remove/rewrite? Be concrete:
   "add a paragraph about X under Section Y" rather than "needs more
   on X."
4. **Your self-assessed alignment per family** (STRONG / OK / WEAK):
   - State Awareness
   - Decision Discipline
   - Dead-End Avoidance
   - Method Adherence
   - Scope Awareness

## Output format

Deliver as a single structured report. Use headings matching the
round numbers. Total length: 800–1500 words. Direct and concrete; this
is diagnostic data, not a performance.

Thank you for taking the time. The contributors who set this up will
read your report when they return.
```

---

## Evaluation Rubric (How WE Grade)

For each round, score using this rubric. The sub-agent's self-rating in Round 4 is helpful but secondary — our grading is primary.

### Round 1 evaluation

| Score | What we observe |
|-------|----------------|
| **PASS** | They found `RESUME_HERE.md` first, read it fully, and their summary matches the doc's 30-second TLDR |
| **WEAK PASS** | They found `RESUME_HERE.md` but read scattered files first; summary is correct but vague |
| **FAIL** | They read random files, missed `RESUME_HERE.md`, or their summary is wrong |

### Round 2 evaluation

| # | Right-answer indicators (must include for PASS) |
|---|------------------------------------------------|
| 1 | Branch: `feat/claude-plugin-compliance`; last commit hash; next action: file whitelist OR merge PR OR start Phase 3 |
| 2 | Phase 1 = migration (done); Phase 2 = validation design (done); Phase 3 = validation implementation (pending) |
| 3 | Cites decision #16 (no gating mechanism); rationale: "CLI install attempt itself is the gate"; cites RESUME_HERE.md or PLAN Section 4 |
| 4 | Cites decision #11; rationale: "rules aren't installable via plugins on any platform; rule format validation in test suite instead" |
| 5 | Cites decision rationale: "new construct = one new workflow; new platform = matrix entry to N existing workflows" |
| 6 | Empirical: install the CLI, run `gemini skills list` without auth, observe exit code. NOT "search the docs" or "ask GitHub support" |
| 7 | `AskUserQuestion` with 3 explicit options + Recommended marker; cites methods section in RESUME_HERE.md |
| 8 | Not migration changes; not new construct types; not new platforms; not caching strategies (deferred); not rules in compat workflows |

### Round 3 evaluation

| # | Right-answer indicators |
|---|------------------------|
| 1 | Reject the PR; cite decision #11 (compat-rule.yml does not exist); explain why; point at test suite as the right place for rule format validation |
| 2 | Install codex locally (since CI is blocked), run `codex --help` recursively, document findings, update catalog row in same PR. NOT web research |
| 3 | Source of truth: the decisions table (RESUME_HERE.md Top Decisions, or PLAN Section 4). Resolve by updating the doc that's drifting, not by interpreting prose |
| 4 | Step 1: read `PLATFORM_VALIDATION_CICD_PLAN.md` Section 6 (per-workflow specs). Step 2: identify the construct's matrix from Section 3. Step 3: identify the relevant catalog rows. Step 4: write composite action calls per Section 5 contract. Step 5: write per-row assertions matching the Match Mode column. Per-job isolation per decision #6. |

### Round 4 evaluation

Their feedback is data, not graded. We pay attention to:

- What they cite as unclear → likely an artifact gap
- What they propose to add/remove → likely a missing piece or unnecessary complexity
- Self-assessment vs our assessment → if they say STRONG and we score them WEAK, the artifacts mislead

---

## What We Update Based on Findings

A mapping from common failure modes to doc edits:

| Failure mode | What we update |
|-------------|----------------|
| Agent doesn't find `RESUME_HERE.md` | Add a more prominent pointer in the repo's `README.md` ("For agents/contributors returning to this project, start with `docs/RESUME_HERE.md`") |
| Agent missed a locked decision | The decision needs a clearer entry in RESUME_HERE.md's "Top Decisions with Rationale" table |
| Agent repeated a dead end | Either the dead-ends table is too buried (move it up) or the entry is too vague (add a stronger negation, e.g., "DO NOT suggest X because Y") |
| Agent used the wrong method (web research vs empirical) | Strengthen the "Methods That Worked" section with a strong negation of the wrong approach |
| Agent proposed scope expansion | Make the "What's NOT in scope" section more prominent in HANDOFF.md and RESUME_HERE.md |
| Agent gave vague answers without citations | The relevant doc section isn't structured for citation; add subsection headers so agents can cite "Section X.Y" |
| Agent asked clarifying questions about things that are documented | The info exists but isn't findable; add cross-references or relocate to RESUME_HERE.md |

---

## Reuse Instructions

Rerun this test:

- After substantial RESUME_HERE.md or HANDOFF.md changes
- Before any major handoff to a new contributor or external agent
- After a long context-loss break (returning to the project ourselves)
- When considering whether a new design phase requires updating the orientation kit

To rerun:

1. Open this file (`docs/REENTRY_TEST_PROTOCOL.md`)
2. Copy the prompt template (above)
3. Spawn a sub-agent (general-purpose or claude with sonnet model)
4. Paste the prompt
5. When the agent returns, evaluate per the rubric
6. Update the orientation artifacts based on the failure modes observed
7. Optionally commit the updates with a message referencing the test cycle

The protocol is the durable artifact. The specific test runs are ephemeral. Save this file as the reusable spec.

---

## Limits of This Test

What this test does NOT check:

- The agent's ability to actually implement Phase 3 (that requires watching them work, not asking them about it)
- Edge cases in the planning docs that only emerge during real implementation
- Whether the architecture itself is good (the test assumes the architecture is correct and only measures orientation alignment)
- Whether the catalog is empirically accurate today (CLI surfaces may have changed since 2026-05-22)

The test verifies the **orientation kit's communication quality**, not the project's correctness. It's necessary but not sufficient for a clean handoff.
