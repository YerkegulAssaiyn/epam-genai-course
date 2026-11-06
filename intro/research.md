# Research on Generative AI Applications

**Author:** Yerkegul Assaiyn
**Course:** EPAM — Generative AI for Software Development (Introduction module)
**Focus:** 3 FinTech use cases + 2 EdTech use cases

---

## Contents

1. [FinTech: AI assistants in mobile banking apps](#1-fintech-ai-assistants-in-mobile-banking-apps)
2. [FinTech: AI assistants for contact-center agents](#2-fintech-ai-assistants-for-contact-center-agents)
3. [FinTech: From meeting transcript to requirements and Jira tickets](#3-fintech-from-meeting-transcript-to-requirements-and-jira-tickets)
4. [EdTech: Personal AI tutors](#4-edtech-personal-ai-tutors)
5. [EdTech: AI assistants for programming education](#5-edtech-ai-assistants-for-programming-education)
6. [Cross-cutting observations](#6-cross-cutting-observations)

The three FinTech cases follow one path inside a bank: GenAI for **customers** (case 1), for **employees** who serve customers (case 2), and for the **delivery teams** who build the bank's products (case 3).

---

## 1. FinTech: AI assistants in mobile banking apps

Banks are moving from scripted chatbots to LLM-based virtual assistants inside their mobile apps. These assistants understand free-form questions, explain spending, and increasingly **perform operations** on the customer's behalf (payments, transfers, tax payments). The **business value** is 24/7 self-service at scale, lower call-center load, and personalized financial guidance that used to require a human advisor. The scale is already significant: first-generation assistants built on classic NLP have handled billions of interactions, and banks such as Lloyds expect generative AI to add more than £100m of value in 2026 alone.

**Technical challenges:** the assistant must be grounded in live account data and current product terms (typically via RAG and tool/function calling), support local languages, and keep personal financial data inside the bank's security perimeter. When the assistant moves from answering to *acting*, it becomes an agentic system that needs strict permissions, confirmations, and audit logs. **Weak points:** hallucinated answers about fees, rates, or regulations create legal and reputational risk; prompt injection and social engineering can target an agent that executes transactions; and customers may not trust or adopt a new assistant if it is not clearly better than the old one. Every conversation also has a token cost, so tokenomics matter at millions of users.

**Maturity levels.** Not every "AI assistant" in a banking app is generative AI. Assistants in the market sit on different levels:

| Level | What it can do | Example |
|---|---|---|
| Rule-based bot | Buttons and fixed scripts, FAQ answers | Classic banking chatbots |
| NLP assistant | Understands free-form questions, routes to answers | Bank of America Erica (launched 2018 on classic NLP/ML) |
| GenAI assistant | Free dialogue, explanations, personalized guidance | Starling Bank assistant built on Google Gemini |
| Agentic assistant | Performs banking operations on the user's behalf | Freedom AI Assistant (dozens of operations by voice) |

Even the most famous banking assistant, Erica, was built on classic natural-language processing rather than generative AI ([source](https://www.emarketer.com/content/genai-moves-banks-customer-facing-apps-lloyds)). Banks are now moving up this ladder, and each level adds value but also risk: an assistant that only answers can mislead, while an agent that acts can move money.

**Architecture trade-off: cloud LLM vs self-hosted.** A bank can call a powerful external model (faster start, better quality, lower initial cost) or host the model inside its own data centers (full control over customer data, easier compliance, but higher infrastructure cost and usually a smaller model). Freedom Bank chose to run its assistant inside its own secure data centers, which shows how strongly security drives architecture decisions in finance.

**Existing implementations:**
- **Bank of America Erica** — https://promotions.bankofamerica.com/digitalbanking/mobilebanking/erica — the reference virtual assistant in retail banking, launched in 2018 and used for billions of customer interactions.
- **Freedom AI Assistant (Kazakhstan)** — https://astanatimes.com/?p=108743 — a voice assistant in Freedom Bank's business app that executes dozens of banking operations in Kazakh and Russian and runs in the bank's own data centers.
- **ForteBank AI-Nur (Kazakhstan)** — https://digitalbusiness.kz/2026-07-02/ainezamenyaet-lyudey-nomenyaet-protsessi-kak-forte-stroit-bank-novogo-tipa/ — a customer-service assistant in a bank that positions itself as an AI-native organization.

### From my experience

As a customer, I have seen AI assistants in the apps of several banks, including Bank of America, Freedom, ForteBank, Otbasy Bank, and Halyk Bank. A recent non-banking case showed me the main risk of the "replace" strategy. When I tried to transfer my WhatsApp history from Android to iPhone, I got errors many times, but both in-app and email support appeared to be fully automated, and I could not reach a human. For a bank, where the problem may be a blocked card or a lost payment, the lack of a clear escalation path to a person would be much more serious.

---

## 2. FinTech: AI assistants for contact-center agents

Not every banking AI talks to customers directly. **Agent assist** tools support the human operator during a call or chat: they listen to the conversation in real time, detect the customer's intent, search internal policies and procedures, suggest an answer or a step-by-step guide, and write the call summary afterwards. The **business value** is shorter handling time, faster onboarding of new operators (they do not need to memorize every product rule), more consistent answers, and full analytics of conversations that were previously checked only by small manual samples.

**Technical challenges:** the system needs reliable real-time speech-to-text (including mixed Kazakh–Russian speech in local banks), low latency so suggestions arrive while the customer is still talking, and a RAG pipeline over a large, constantly changing knowledge base of tariffs, rules, and scripts. It must also integrate with the existing contact-center platform and CRM. **Weak points:** if the knowledge base is outdated or contradictory, the assistant confidently suggests wrong answers, and a tired operator may repeat them to the customer; call recordings contain sensitive personal and financial data; and operators can over-rely on suggestions and stop building their own expertise. The human remains responsible for what is said to the customer.

**How the pipeline works:**

```mermaid
flowchart LR
    A[Customer call or chat] --> B[Speech-to-text]
    B --> C[Intent detection]
    C --> D[RAG search in knowledge base]
    D --> E[Suggested answer and steps for operator]
    E --> F[Operator decides and answers]
    F --> G[Auto-generated call summary]
    G --> H[Analytics of all conversations]
```

**Measuring impact.** Contact centers measure this use case with clear business metrics: **AHT** (average handling time), **FCR** (first contact resolution), and **CSAT** (customer satisfaction). Early results at Discover showed that call handling time and policy search time dropped by as much as 70% ([source](https://www.acainternational.org/?p=123254)).

**Replace vs augment.** Case 1 and case 2 show two different strategies. In case 1 the AI **replaces** the human for simple requests and talks to the customer itself. In case 2 the AI **augments** the human: it only suggests, and the operator makes the final decision. This is the same difference as between a Copilot (an AI helper added to an existing workflow) and an AI-native tool (the workflow is rebuilt around AI). For regulated, high-risk conversations, the augment strategy is often the safer first step.

**Existing implementations:**
- **Discover Financial Services + Google Cloud Vertex AI** — https://americanbanker.com/news/discover-deploys-generative-ai-in-its-contact-center — a US bank uses generative AI to summarize policies and procedures for nearly 10,000 contact-center agents, reporting large reductions in call handling and policy search time.
- **Google Cloud Agent Assist** — https://cloud.google.com/agent-assist — recommends responses, step-by-step guidance, and coaching to agents from the company knowledge base.
- **Amazon Q in Connect** — https://docs.aws.amazon.com/connect/latest/adminguide/amazon-q-connect.html — a generative AI assistant in the Amazon Connect agent workspace that gives real-time recommendations during calls and chats.
- **ForteBank speech analytics (Kazakhstan)** — https://digitalbusiness.kz/2026-07-02/ainezamenyaet-lyudey-nomenyaet-protsessi-kak-forte-stroit-bank-novogo-tipa/ — an in-house generative AI platform that analyzes almost all customer communications instead of about 1% reviewed manually before.

### From my experience

I saw this use case from the inside in banking. At first, a lot of the work was manual: we listened to customer calls, filled in the data, and corrected it ourselves, because many requests were in Kazakh and the available NLP and LLM models did not handle Kazakh well. In parallel, the AI solution was improved step by step, and now it works well enough to noticeably reduce the manual workload of the contact center. For me this is a clear example of the course idea that GenAI quality depends mostly on data: low-resource languages like Kazakh need extra human effort before AI becomes reliable.

---

## 3. FinTech: From meeting transcript to requirements and Jira tickets

In banks, a large part of delivery time is spent turning business discussions into formal artifacts: requirements documents, user stories, acceptance criteria, and tickets in Jira. GenAI can take a **meeting transcript**, extract decisions, requirements, and action items, draft a structured specification, and create Jira work items with descriptions and assignees after a human reviews them. The **business value** is faster time from idea to backlog, fewer requirements lost between business and IT, standardized ticket quality, and analysts freed from routine documentation to focus on clarifying real business needs.

**Technical challenges:** transcription quality decides everything (speaker identification, accents, code-switching between Kazakh, Russian, and English, banking terminology); the model must map vague phrases like "we should check this with risk" to concrete owners and deadlines; and the integration with Jira and Confluence requires correct permissions and fields. This is an agentic workflow: read the transcript → extract items → draft the specification → create tickets after confirmation. **Weak points:** the model may invent requirements that nobody said (hallucination) or miss implicit context that participants share but never say aloud; meeting content in a bank is confidential, so sending it to an external LLM may be forbidden; and if teams stop reviewing the generated tickets, errors go straight into development. A human "approve before create" step is essential.

**Existing implementations:**
- **Atlassian Rovo — meeting transcripts to Jira issues** — https://www.atlassian.com/software/rovo/use-cases/agent-meeting-transcripts-to-jira-issues — an agent that parses a pasted transcript, proposes Jira issues with descriptions and acceptance criteria, creates them after user confirmation, and can draft Confluence requirements.
- **Deloitte Ascend AI Assist — Product Owner Agent** — https://aws.amazon.com/marketplace/pp/prodview-4vsvppi4se3v4 — an assistant that captures meeting notes, refines epic descriptions, and generates user stories for agile teams.
- **AI @ Morgan Stanley Debrief** — https://www.morganstanley.com/press-releases/ai-at-morgan-stanley-debrief-launch — a finance example of meeting intelligence: with client consent, it generates meeting notes, surfaces action items, and drafts follow-up emails for financial advisors.

---

## 4. EdTech: Personal AI tutors

AI tutors try to give every learner something close to a personal teacher: they explain concepts, adapt to the learner's level, and practice with them at any time. The best-known products deliberately use a **Socratic approach**, asking guiding questions instead of giving the final answer, and add teacher-facing tools such as lesson planning and progress reports. The **business value** is personalized learning at a very low cost per student, which matters most where human tutors are expensive or unavailable, for example in rural areas.

**Technical challenges:** the model must be constrained by system prompts and guardrails so it does not simply solve homework; it must be safe and age-appropriate for children; and it needs to stay aligned with the curriculum (often via RAG over course content). Voice and conversation features add multimodal components (speech-to-text, text-to-speech). **Weak points:** tutors can still make factual or grammatical mistakes; engagement is a real problem, since Khan Academy reported that only about 15% of students with access to Khanmigo use it regularly; and quality drops sharply for low-resource languages such as Kazakh because there is much less high-quality training data.

**Existing implementations:**
- **Khanmigo (Khan Academy)** — https://www.khanmigo.ai — a GPT-4-based tutor and teaching assistant that guides students with questions instead of giving direct answers.
- **Duolingo Max** — https://blog.duolingo.com/duolingo-max — a premium tier with Video Call, Roleplay, and Explain My Answer features powered by generative AI for language practice.
- **Khanmigo engagement redesign (case note)** — https://www.edtechinnovationhub.com/news/only-15-percent-of-students-with-access-to-khanmigo-actually-use-it-khan-academy-admits — Khan Academy's public admission of low usage, which led to a 2026 product redesign.

---

## 5. EdTech: AI assistants for programming education

Programming courses use AI assistants to help students understand error messages, debug code, and get hints on assignments without receiving ready-made solutions. These assistants are usually grounded in the specific course materials and documentation, so answers match what students are actually learning. The **business value** is scaling individual support to thousands of online students, reducing teaching-assistant workload, and improving course completion rates.

**Technical challenges:** balancing helpfulness with academic integrity (the assistant must guide, not write the solution), grounding answers in course content through RAG, integrating directly into the coding environment (IDE plugins, "explain highlighted code"), and controlling token costs when every student asks many questions. **Weak points:** students can become dependent on the assistant and skip the struggle that builds real skill; the assistant may still hallucinate APIs or give subtly wrong explanations; and determined students can switch to general-purpose chatbots that do give full answers.

**Existing implementations:**
- **CS50.ai / CS50 Duck (Harvard)** — https://cs50.readthedocs.io/cs50.ai/ — a "rubber duck debugger" tutor for Harvard's CS50 that leads students toward answers instead of revealing them.
- **Codio Coach** — https://www.codio.com/features/coach-ai-learning-assistant — an AI learning assistant that explains programming errors and summarizes assignments while protecting academic integrity.
- **Codecademy AI Learning Assistant** — https://www.codecademy.com/resources/videos/official-codecademy-events/transform-your-learning-experience-with-codecademy-s-ai-assistant — an assistant inside Codecademy courses that gives instant guidance, debugging help, and explanations.

---

## 6. Cross-cutting observations

- **Data quality decides the result.** In every case quality depends mostly on the data the model uses: current product terms for app assistants, the knowledge base for agent assist, transcript quality for requirements, course materials for tutors. This is why low-resource languages such as Kazakh are among the hardest cases.
- **Grounding over memory.** Because an LLM stores knowledge as lossy statistical patterns, production systems ground it in real data with RAG, tool calling, and human review instead of trusting its "memory".
- **From chat to agents.** Assistants that execute payments and agents that create Jira tickets show the 2026 shift from PoC chatbots to agentic AI adoption.
- **Security and tokenomics.** Financial data, call recordings, internal meetings, and student data require strict privacy controls (sometimes self-hosted models), and per-token costs become a real business constraint at scale.
- **Human in the loop.** Customer answers, ticket creation, and learning outcomes still need human oversight; AI accelerates the work but does not remove responsibility.
