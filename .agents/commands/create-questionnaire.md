---
name: create-questionnaire
description: Create a v1 questionnaire from questions or input document following schema. Use when user asks to create a questionnaire.
---

Create a v1 questionnaire using the v1 schema:
- Schema: data/questions/v1/schema-questionnaire-v1.json
- README: data/questions/v1/README.md

## Input Options

You can create a questionnaire from:
1. **User-provided list of questions** - User will provide questions directly
2. **Input document** - Convert an existing document into questionnaire format

## Instructions

- Create the questionnaire in the relevant folder for the customer
- Propose `assert_fuzzy` or `assert_any` where plausible
- Do NOT add risk scoring to any questions
- Use `|` after `hidden_instructions:` to allow multi-line hidden instructions while preserving `\n` characters
- Keep contents visible in the prompt rather than moving them into hidden_instructions
- Only add hidden_instructions if there are points of confusion
- Reference other questionnaires in data/questions/v1 for examples

## Metadata Format

Ensure you use the right versioning information and customer name:

```yaml
metadata:
  title: Technical Privacy Review (Lumin Digital, v1.0)
  description: A basic privacy technical review used for Lumin Digital - v1.0.0
``` 