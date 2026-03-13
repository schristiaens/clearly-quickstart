# Clearly AI Questionnaires

This directory contains questionnaires used by Clearly AI to generate structured reports. Each questionnaire focuses on a specific topic like security threat modeling or privacy assessments, breaking down complex analysis into modular questions.

## How Questionnaires Work

Under the hood the review pipeline executes an agentic loop for every question.

1. Initial context gathering  
   - A search is run against (a) the project's code/documents and (b) the shared knowledge-base using the question text.  
   - The top results are passed to the LLM together with the question, its `hidden_instructions`, and the conversation history.

2. Iterative research (max three rounds)  
   - After reviewing the initial results, the agent decides whether to perform another project or knowledge-base search or whether it already has enough information to answer.  
   - Newly retrieved documents are added to its working context before it thinks again.

3. Answer synthesis  
   - Once enough information has been gathered the agent writes its answer.  
     * Free-form questions receive a prose answer.  
     * Single- and multi-select questions receive the option(s) selected by the agent. The options you define in the block become the available choices.  
   - Every answer also includes supporting citations, the agent's confidence level, and a brief explanation of its reasoning.

4. Optional compliance check  
   - When a block includes an `assert_fuzzy`, `assert_any`, or `assert_all` field (see "Compliance Assertions" below) the system automatically evaluates whether the answer meets the specified requirements.  
   - The resulting `COMPLIANT` / `NON_COMPLIANT` status and a short explanation are stored alongside the answer.

After every block has an answer the worker assembles them into the final review.

## Questionnaire Structure

Questionnaires are defined in YAML format with the following components:

### Top-level Metadata

```yaml
metadata:
  title: "Questionnaire Title"
  description: "Brief description of what this questionnaire analyzes"
  general_instructions: "Overall instructions for the entire questionnaire"
```

### Blocks

The main content is organized into blocks, which can be one of several types:

1. **Text blocks** - Static text to appear in the report:
```yaml
- text: "## Section Heading"
```

2. **Free-form text questions** - Questions expecting a prose response:
```yaml
- prompt: "Describe the security posture of the application."
  hidden_instructions: "Search for security-related code, authentication mechanisms, encryption usage, etc."
```

3. **Multiple-choice questions** - Questions with predefined options where multiple can be selected:
```yaml
- prompt: "What types of sensitive data does the application handle?"
  multi_options:
  - option: "Personal Identifiable Information (PII)"
    risk: 80
  - option: "Financial Data"
    risk: 70
  - option: "Health Information"
    risk: 90
```

4. **Single-choice questions** - Questions where only one option can be selected:
```yaml
- prompt: "What is the primary authentication method?"
  single_options:
  - option: "OAuth 2.0"
    risk: 20
  - option: "Session-based authentication"
    risk: 30
  - option: "Basic authentication"
    risk: 70
  max_risk: 100  # Optional, enables deterministic risk aggregation downstream
```

5. **Table generation blocks** - Ask the AI to synthesize a structured table from project documents:
```yaml
- type: "table_generation"
  id: "controls_inventory"
  text: "Generate a table of detected security controls from project documentation."
  hidden_instructions: >-
    Extract concrete, verifiable facts from authoritative documents. Prefer explicit lists
    and configuration files. Avoid speculation.
  table_config:
    title: "Security Controls Inventory"
    columns:
      - name: "Control"
        type: "string"
        description: "Control name"
      - name: "Category"
        type: "enum"
        values: ["Identity", "Access", "Network", "Data", "Monitoring", "Other"]
      - name: "Implemented"
        type: "boolean"
        description: "True if the control is implemented"
      - name: "Source"
        type: "string"
        description: "File or doc where evidence appears"
      - name: "Last Updated"
        type: "date"
    baml_instructions: >-
      Use conservative extraction. Include only items with explicit evidence in the provided documents.
    followup_questionnaire_id: "control_details_v1"  # optional, allows you to use the generated table contents as inputs into a new questionnaire
```


1. **Summarize blocks** - Create a review summary after all questions are answered:
```yaml
- block_type: "summarize"
  id: "exec_summary"
  text: >-
    Provide an executive summary of key findings, major risks, and recommended next steps.
  hidden_instructions: >-
    Synthesize across all prior answers and generated tables. Be concise and action-oriented. 
    Don't output the answer in JSON. 
  tools: ["search_knowledge_base"]  # optional
```

Note: This block is processed after all other blocks complete. The system aggregates Q&A pairs and uses them to create the final summary stored on this block.

### Risk Aggregation Blocks

Use an `aggregate_risks` block to deterministically roll up option-level risks into a single score that later blocks (typically `summarize`) can reference.

```yaml
- block_type: aggregate_risks
  text: "Overall SaaS risk summary"
  strategy: sum_as_percentage
```

Guidelines:

* Only single- or multi-select blocks may opt into aggregation by setting `max_risk` (per question) and `risk` (per option). Questions without `max_risk` are ignored by the aggregator.
* `max_risk` is optional and can be tuned per block; unanswered questions still count toward the max denominator so reviewers can see coverage gaps.
* The aggregate block's `text` is required (an empty string is allowed) so editors can control how the frontend explains the output.
* `strategy: sum_as_percentage` adds up selected option risks as the numerator, sums all contributing `max_risk` values as the denominator, and displays the total points plus percentage.

### Hidden Instructions

The `hidden_instructions` field provides guidance on how the agent should use the tools available to it and how to answer the question.

### Compliance Assertions

Add one of the following optional fields directly inside a question block to let Clearly AI automatically grade the answer:

* `assert_fuzzy` – a single string requirement for free-form questions.
* `assert_any` – a list of options; at least one must be selected to pass.
* `assert_all` – a list of options; **every** item must be selected to pass.

Examples:

```yaml
# Free-form question with a fuzzy assertion
- prompt: "How is data encrypted in transit?"
  hidden_instructions: "Look for TLS / HTTPS usage."
  assert_fuzzy: "The answer must state that data is encrypted using TLS or HTTPS."

# Single-select question requiring a specific answer
- prompt: "Is MFA enabled for all admin accounts?"
  options:
  - option: "Yes"
  - option: "No"
  assert_any:
    - "Yes"

# Multi-select question that needs ALL listed controls
- prompt: "Select the methods your product uses for authenticating a person's access to the service"
  multi_options:
  - option: "SAML / OIDC SSO"
  - option: "Password + source IP validation"
  - option: "Password + source IP validation with API"
  assert_all:
    - "SAML / OIDC SSO"
    - "Password + source IP validation"
    - "Password + source IP validation with API"
```

## Block Reference

See [`questionnaire-blocks-reference.yaml`](questionnaire-blocks-reference.yaml) for a complete, commented example of every block type and field. Use it as a starting point or copy-paste source when authoring new questionnaires.

## Creating New Questionnaires

To create a new questionnaire:

1. Start from the [block reference](questionnaire-blocks-reference.yaml) or an existing questionnaire
2. Define the metadata section
3. Create blocks that walk through a logical assessment process
4. For each question, carefully craft the `hidden_instructions` to optimise search results and answer quality
5. When you need Clearly AI to grade the answer, add an `assert_fuzzy`, `assert_any`, or `assert_all` field as described above
6. Run `uv run pytest` to validate parsing before committing

## Warnings

- AVOID the Norway problem! This is where YAML interprets `NO` as `false` instead of the string `"NO"`. So use the string `"NO"` instead!
- For multi-line strings, just use the `>-` symbol to start a new block and avoid complexity with YAML parsing.
