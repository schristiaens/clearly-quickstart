# Clearly AI <> NebFog 2026

## Greetings!

Hi Everyone we're Clearly AI \- we automate security assessments like threat modeling for security engineers at large enterprises. But what we're really building is an AI tool that can evaluate any source information to accomplish any security assessment task.

## Challenge

Our challenge today is to use Clearly AI to accomplish a new and creative goal, like creating the best AGENTS.md file for secure vibe coding, or a threat-driven pen testing plan you can feed straight into an AI pen test tool, or an AI secrets scanner.

We're a great side quest while your agents are running \- it should take only 15-20 minutes to build out a workflow end to end. And we're giving away 6 months free Claude Code Max to the winner\! Come find us for access to the quickstart repo and platform to get started.

Create a Clearly AI questionnaire to accomplish a creative mission\! 

Example ideas:

1. Use Clearly AI to generate a threat model / pen testing plan that an agent can follow  
2. Use Clearly AI to create an AGENTS.md for secure vibe coding and auto published on my GH repo  
3. Use Clearly AI to generate a secrets hunting agent using Clearly AI's secret scanner

Evaluation criteria:

* ambitiousness of mission
* ability to accomplish mission  
* quality of questionnaire design  
* utilization of Clearly AI system capabilities  
* Extra points for using workflows, Clearly API, etc.

## Onboarding
1. Sign up here: https://nebfog.clearly-app.com/
2. Create a questionnaire using this repo and upload in Settings
3. Add any integrations & set up any workflows (hidden URL: https://nebfog.clearly-app.com/workflows)

## Important Notes
Because we are an enterprise product, you are all in the same enterprise org:
1. You will be able to see each other's questionnaires. Please operate on the honor system and don't look at other people's work!!
2. If you add integrations via Personal Access Token or Org-wide OAuth you WILL expose your data to everyone else on the platform
3. Other people can see the source docs you upload to evaluate your questionnaire - don't throw anything sensitive in!


# What is Clearly AI?

Clearly AI is a SaaS for **security teams** who need to complete security (and related) reviews faster.

**The problem:** Security teams at enterprises spend significant time gathering scattered information—design docs, code, tickets, wikis—and performing repetitive baseline security reviews across many systems.

**The solution:** Clearly AI helps by gathering that information faster (via Integrations and uploads) and generating **structured assessments** with AI. You bring the context (Projects, Knowledge Base, Integrations); Clearly AI runs Questionnaires against that context and produces answers with citations and, where applicable, compliance status.

**Intended audience:** Security engineers, compliance analysts, and risk owners at mid-size to large organizations who run threat models, control assessments, privacy impact assessments, or similar reviews. Clearly AI acts as a force multiplier: it handles triage and data gathering so experts can focus on judgment and high-risk items.

**What Clearly AI is built for:**

1. **Triage** – Check many systems for baseline controls, flag what needs human attention, and approve low-risk systems quickly.
2. **Deep analysis** – For complex systems, synthesize context and produce thorough security analysis that would take hours to gather manually.

The sections below describe the main components you use to do this: Projects, Reviews, Questionnaires, Knowledge Base, Chat, Integrations, and Workflows.

---

## Projects

**Projects** are context containers for a system or application you want to review. Each Project groups:

- **Design and reference documents** (uploaded files or linked integrations)
- **Source code** (via connected repos such as GitHub or Azure DevOps)
- **Integrations** (issue trackers, document sources, etc.)

A Project has a name, description, owner, and a **review stage** (e.g., Draft, In Review, Approved, Needs Revision). Projects are versioned: when you change files, integrations, or metadata, a new Project version is created. Reviews always run against a specific Project version so results stay consistent and auditable.

---

## Reviews

**Reviews** are point-in-time security (or compliance) assessments. You create a Review by:

1. Choosing a **Questionnaire** (the Review template)
2. Running it against a **Project** (and thus a specific Project version)

Clearly AI uses your project’s documents, code, and integrations as context and generates structured answers—often with citations and compliance status. You can edit answers, add feedback, and regenerate individual answers. Reviews help with both **triage** (baseline checks across many systems) and **deep analysis** (thorough assessment of complex systems).

---

## Questionnaires

**Questionnaires** are customizable Review templates. They define the questions and structure of a Review (e.g., STRIDE, OWASP, privacy impact, or custom frameworks). Each Questionnaire has one or more **blocks** (e.g., freeform, single/multi-select, table generation). Questionnaires can be org-specific and versioned so you can track which template was used for each Review.

---

## Knowledge Base

The **Knowledge Base** is your organization’s shared context that informs all analysis—Reviews and Chat. It typically includes:

- **Files** – Policies, standards, runbooks, and other reference documents (with optional categories and trust levels)
- **Snippets** – Short reusable text (e.g., standard statements, boilerplate)
- **FAQs** – Question-and-answer pairs that the system can use when answering Review or Chat questions

Content in the Knowledge Base is searchable and is used to ground LLM answers so they align with your policies and past decisions.

---

## Chat

**Chat** is an ad-hoc Q&A interface. You can ask security or compliance questions and get answers that use:

- Your **Knowledge Base**
- One or more **Projects** (and their documents and Reviews)
- Optional **focus** on a specific Project, Review, or even a single Review block

Chat is available in the web app and (where configured) in Slack. It is meant for quick questions without creating a full Review.

---

## Integrations

**Integrations** connect Clearly AI to external systems so Project context and automation can use live data. Types include:

- **Source code** – e.g., GitHub, Azure DevOps, Bitbucket
- **Issue trackers** – e.g., Jira, Linear
- **Documents / knowledge** – e.g., Google Drive, SharePoint, Confluence
- **Messaging** – e.g., Slack, Microsoft Teams
- **Other** – e.g., ServiceNow (tickets and knowledge)

Integrations can be attached to Projects (as **integration sources**) to pull in repos, tickets, or documents. They can also power Workflows (e.g., opening tickets, posting to Slack).

---

## Workflows

**Workflows** are automated processes that perform multi-step actions, such as:

- Refreshing or syncing data (e.g., re-pulling from integrations)
- Creating or updating tickets in issue trackers
- Notifying channels or users
- Triggering follow-up steps based on Review or findings

Workflows are configured per Organization and can be triggered by events or schedules.

---

## Organization and Access

Data in Clearly AI is scoped by **Organization** (tenant). Users belong to one or more Organizations. Projects, Reviews, Questionnaires, Knowledge Base content, and Integrations are all org-scoped. Access control and permissions (e.g., who can create Projects, run Reviews, or change settings) are currently enforced at the Organization level.

---

## Summary

| Component       | Purpose |
|----------------|---------|
| **Projects**   | Group documents, code, and Integrations for a system you want to review |
| **Reviews**    | Point-in-time assessments created by running a Questionnaire against a Project |
| **Questionnaires** | Reusable Review templates (questions and structure) |
| **Knowledge Base**  | Org-wide policies, snippets, and FAQs used to inform Reviews and Chat |
| **Chat**       | Ad-hoc Q&A with optional Project/Review focus |
| **Integrations**   | Connections to repos, issue trackers, docs, and messaging |
| **Workflows**  | Automated multi-step processes (refresh, tickets, notifications) |
| **Organization**   | Tenant boundary for data and access control |
