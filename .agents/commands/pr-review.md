---
name: pr-review
description: Automated PR review for questionnaire quality, YAML correctness, and documentation. Used by GitHub Actions and locally.
---

Review this pull request thoroughly, but report concisely.

Read `questions/v1/questionnaire-blocks-reference.yaml` first. It is the canonical reference for every block type and field. Use it to validate that PRs follow correct patterns.

Then analyze these categories in depth:
1. Questionnaire quality: clear and unambiguous prompts, well-crafted hidden_instructions that guide effective search and answer synthesis, appropriate use of block types (freeform vs single-select vs multi-select), logical flow between questions, risk scores that make sense relative to each other
2. YAML correctness: valid YAML syntax, proper quoting (watch for the Norway problem where YES/NO/true/false are parsed as booleans), correct use of schema fields (metadata, blocks, options, assertions), multi-line strings using `>-`
3. Compliance assertions: assert_fuzzy/assert_any/assert_all used correctly, assertion values match available options for select questions, fuzzy assertions are specific enough to be meaningful
4. Documentation accuracy: README.md, AGENTS.md, inline comments

Then, report ONLY the following:

**PR Summary:** (1-2 sentences max)

**Issues Found:**
For each issue found in your analysis, add a section with this format:

[SEVERITY] Brief issue title
File: path/to/file:line
Issue: One line explanation
Fix: One line solution
(If MUST FIX) Cursor prompt: Complete prompt with instructions and context on how to fix the issue

Rules:

- Severity levels:
    - MUST FIX - blocks merge, will break parsing or produce incorrect review results
    - SHOULD FIX - recommended fix before merge
    - NOTED - everything else (follow-up tickets, nitpicks, FYIs, etc)
    - PREEXISTING - issues you spot in the changed files but are not part of the PR's diff
- If no issues found, write: ✓ All checks passed (after the Issues Found heading)
- Skip positive feedback, explanations of your process, or why things are good
- Be terse and concise. Developers understand context.
- One section per distinct issue
- Run `uv run pytest` to validate all questionnaires parse correctly. If any test fails, report it as MUST FIX.
- Unquoted YAML values that could trigger the Norway problem (YES, NO, true, false, null, NA, numeric ranges like 1-100) are always MUST FIX.
- Option values in assert_any/assert_all must exactly match an option string defined in the same block. Mismatches are MUST FIX.
