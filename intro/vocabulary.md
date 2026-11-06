# GenAI Vocabulary

**Author:** Yerkegul Assaiyn
**Course:** EPAM — Generative AI for Software Development (Introduction module)

Terms selected from my research report ([research.md](research.md)) and explained in my own words.

---

## Core concepts

**LLM (Large Language Model)** — a model trained on huge amounts of text that generates text by predicting the next token, using the context of the conversation. Chat platforms like ChatGPT or Claude are built on top of LLMs.
*Example from my report:* banking app assistants (case 1) and AI tutors (case 4) are built on LLMs.

**Token** — a small piece of text (a word or part of a word) that the model reads and generates. AI usage is usually paid per token.
*Example from my report:* every conversation with a banking assistant has a token cost.

**Tokenomics** — the economics of token usage: tracking how many tokens AI consumes and balancing cost against quality, for example by using shorter prompts or smaller models for simple tasks.
*Example from my report:* at millions of bank customers or students, token costs become a real business constraint.

**Prompt** — the input text or instructions given to an AI model. Writing prompts well is called *prompt engineering*.
*Example from my report:* system prompts tell an AI tutor not to give ready answers.

**Hallucination** — when AI confidently "makes things up": the answer sounds plausible but is false, because the model generates the most probable text, not checked facts.
*Example from my report:* an assistant may invent bank fees, or an agent may create a Jira requirement that nobody said in the meeting.

## Working with data

**RAG (Retrieval-Augmented Generation)** — the system first searches the knowledge base for relevant information and then answers based on it. This reduces (but does not fully prevent) hallucinations.
*Example from my report:* contact-center agent assist searches bank policies before suggesting an answer (case 2).

**Low-resource language** — a language with little text available on the open internet, so AI models work worse with it. Example: Kazakh.
*Example from my report:* in my experience, Kazakh calls first had to be processed manually because models handled Kazakh poorly (case 2).

**Speech-to-text** — converting spoken voice into written text. In contact centers it is the first step before AI can analyze a call; it works worse for Kazakh.
*Example from my report:* the first block of the contact-center pipeline and the base for meeting transcripts (cases 2 and 3).

## Agents and safety

**AI agent** — an AI system that not only answers but acts: it plans steps by itself and calls the tools it needs (APIs, Jira, payments) to reach a goal.
*Example from my report:* Freedom AI Assistant performs banking operations; Atlassian Rovo creates Jira issues from a meeting transcript.

**Human-in-the-loop** — a person watches the AI's work and approves or rejects its results ("OK / not OK") before they take effect.
*Example from my report:* Rovo creates tickets only after user confirmation; the operator decides whether to use the AI suggestion.

**Guardrails** — rules and filters that keep AI within allowed limits, like barriers on a bridge. They are set through the system prompt and extra checks on input and output.
*Example from my report:* an AI tutor is not allowed to give ready solutions; a banking assistant must not discuss other people's accounts.

**Prompt injection** — an attack through text: hidden instructions try to make the AI break its rules. It is especially dangerous for agents that can act. Guardrails help protect against it.
*Example from my report:* an agent that executes transactions can be targeted by injected instructions (case 1).

## Types of AI tools

**Copilot** — AI added to an existing program as a helper, like a co-pilot next to the pilot. Example: GitHub Copilot inside an IDE.
*Example from my report:* contact-center agent assist "augments" the operator instead of replacing them (case 2).

**AI-native** — a product or company built around AI from the start, not with AI added later. Example: Cursor IDE, or a bank that redesigns its processes around AI.
*Example from my report:* ForteBank positions itself as an AI-native organization (case 1).

## Process and education

**Acceptance criteria** — the conditions a task must meet to be accepted as "done". Example: in Jira, a ticket can be closed only if all its acceptance criteria are satisfied.
*Example from my report:* Rovo drafts acceptance criteria for Jira issues from a meeting transcript (case 3).

**Socratic approach** — a teaching method where the teacher does not give the answer but asks guiding questions so the student finds it alone. The goal is learning, not copying.
*Example from my report:* Khanmigo and CS50 Duck guide students with questions instead of giving solutions (cases 4 and 5).
