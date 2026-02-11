# Comparison Report: Our Idea vs. Literature (Punnoose & Deepa Papers)

This report compares the project idea (from *LiteratureReviewHelper.ipynb*, PROJECT_CONTEXT) with the ideas implemented in the papers contained in `punnoose_papers.txt` and `deepa_papers.txt`. Each factual claim is cited to a specific paper with the relevant sentence.

**Section:** Cross-cutting comparison of our agentic chatbot approach with the most relevant literature across both Deepa and Punnoose paper sets.

**Thresholding:** Only papers with relevance **≥ 0.70** in `ReviewDeepaPapers.md` and `ReviewPunnoosePapers.md` are used as direct evidence in this report; lower-scoring papers are excluded from further analysis here.

**Next Step:** Perform qualitative reliability assessment of these high-relevance papers and refine our research questions and evaluation design based on their strengths and weaknesses.

**Pivot (current project direction):** The project has moved on from the original design (intent-only LLM + rule-based function selector + code executor). We now adopt an **agentic approach**: the LLM chooses which tools/functions to call and orchestrates execution. Intent classification remains relevant as related work and a possible baseline; it is not the primary design.

---

## 1. Our Idea

Our proposed system is a **stakeholder-facing chatbot** using an **agentic** design:

- **LLM with tool use** — The LLM receives the user query and a set of available tools/functions (e.g. via schemas). It decides which tool(s) to call and with what arguments, and may chain multiple calls.
- **Tool execution** — A separate executor runs the selected function(s), fetches data from structured sources, and returns results to the LLM.
- **Response generation** — The LLM turns execution results (and optional context) into a natural-language response for the user.

**Core design principle:** Use the LLM for both *understanding* and *tool choice* to gain **flexibility** and easier extension (new tools without rewriting a rule map). We still aim for **reliability** and **interpretability** via a fixed tool set, structured outputs where possible, and local or trusted deployment. The system is comparable to agentic LLM frameworks (ReAct, Toolformer, OpenAI function calling) and multi-agent orchestration (e.g. GateLens, GoNoGo).

---

## 2. Our Research Questions

Derived from the project context and positioning:

1. **Agentic vs. direct:** When does an agentic (tool-using) LLM outperform a direct LLM (no tools) for stakeholder-facing QA over structured data in domains such as automotive or compliance?
2. **Reliability and interpretability:** How can we improve reliability, interpretability, and auditability of agentic systems (e.g. structured tool outputs, logging, guardrails) while keeping flexibility?
3. **Stakeholder-facing QA:** How does our agentic architecture perform for stakeholder-facing question answering compared to pure RAG chatbots or intent-based + deterministic execution designs in similar domains?
4. **Safety and adoption:** How do we address hallucination, tool misuse, and data exposure (e.g. local deployment, tool allowlists) so the system is acceptable in sensitive or regulated settings?

---

## 2a. Review Synthesis

The high-relevance papers (≥ 0.70) cluster into a few themes that set the context for our agentic project:

- **Agentic and LLM-driven systems** — GateLens, GoNoGo, Simple Action Model, and “Querying Large Automotive Software Models: Agentic vs. Direct” use the LLM to choose tools or orchestrate steps. They show that agentic designs are viable for automotive and release workflows but raise questions about consistency, reliability, and when agentic beats direct LLM use.
- **RAG and document QA** — Tax Law RAG, Safety Requirements RAG, Adopting RAG for vehicle design, and Optimizing RAG for automotive PDFs focus on retrieval, re-ranking, and generation. They stress hallucination risk when retrieval is poor and the need for reliable, explainable outputs in safety or compliance.
- **Intent classification (related work)** — BERT/RoBERTa intent, French recruitment chatbot, NNSI, MAML+embeddings, and LLM function calling with structured outputs treat intent or tool-call format as central. They offer baselines or techniques we can compare against or reuse (e.g. structured outputs for tool calls).
- **Domain and security** — Several papers (e.g. Adopting RAG, Safety Requirements RAG) emphasise domain-specific knowledge, local deployment, and avoiding exposure of sensitive data to external APIs.

Across these themes, a recurring limitation is that agentic and RAG systems still need better reliability, interpretability, and control (e.g. when the LLM chooses the wrong tool or hallucinates). The gaps below summarise where our agentic project can contribute.

---

## 3. Research Gaps Common to the High-Relevance Papers

Across the **high-relevance papers** (relevance ≥ 0.70) in **punnoose_papers.txt** and **deepa_papers.txt**, the following gaps recur:

| Gap | Papers (representative) |
|-----|-------------------------|
| **Hallucination and reliability** | LLMs must produce “highly reliable and explainable results” (Safety Requirements RAG); RAG can “reduce hallucinations and improve factual accuracy” when retrieval is good, but “if irrelevant or even incorrect context is retrieved, the probability of hallucinations is exacerbated” (Tax Law RAG; Safety Requirements RAG). |
| **Retrieval relevance** | “Existing RAG approaches … their performance deteriorates when handling complex queries and it becomes increasingly harder to retrieve the most relevant information” (Safety Requirements RAG). |
| **Domain-specific knowledge** | “Conventional approaches that utilise pre-trained LLMs to assist in safety analyses typically lack domain-specific knowledge” (Safety Requirements RAG). |
| **Intent classification with limited data** | “The dependency on large annotated datasets remains a critical bottleneck”; “the need for models to understand and classify intents with minimal training data” (MAML + embeddings for few-shot intent); “Intent classifiers are generally lacking in real-world training data” (NNSI for intent classification). |
| **Rule-based vs. flexible understanding** | “Rule-based systems are inflexible, involve high development and maintenance costs due to the need for manual updates, and are less robust to variations in user input, often failing to recognize intent in cases of misspellings, slang, or acronyms” (Comparative Analysis BERT and RoBERTa for Indonesian Chatbots). |
| **Security and data exposure** | “Providing documents and other specification-related information in automotive was considered quite problematic — as it involved practically sending the secret information to online services and other parties involved” (Adopting RAG for LLM-Aided Future Vehicle Design). |
| **Controlled use of LLMs** | Many papers use LLMs for end-to-end generation, tool choice, or multi-agent orchestration without a deterministic “execution core”; few explicitly separate *intent only* (LLM) from *function selection and execution* (rules/code). |

---

## 4. How Our Project Can Address This Research Gap

- **Hallucination and reliability:** We use an agentic LLM but constrain the **tool set** and ground responses in **execution results**. We can evaluate and mitigate wrong tool choice or hallucinated calls (e.g. logging, guardrails). *Cite: “The risk of hallucinations is related to the information accessible to the LLM, and its suitability to solve the task at hand” (Towards Automated Safety Requirements Derivation Using Agent-based RAG).* Aligning with “highly reliable and explainable results” in safety-sensitive settings remains a goal via structured outputs and evaluation.

- **Retrieval relevance:** If we add RAG as a tool or context source, we adopt the same directions as the literature (hybrid retrieval, re-ranking). We can study how retrieval quality affects agentic behaviour and bound impact via tool design (e.g. which tools are allowed).

- **Domain-specific knowledge:** We inject domain through **tool schemas**, **allowed functions**, and **structured data** the tools can access. So we address “lack of domain-specific knowledge” by encoding domain in the tool layer rather than relying only on the model’s parameters. *Cite: Safety Requirements RAG on integrating domain-specific information.*

- **Intent with limited data:** Agentic LLMs can work with minimal labelled data (few-shot, zero-shot tool use). We can compare or combine with intent-classification techniques (MAML+embeddings, NNSI-style augmentation) as baselines or for specific sub-tasks.

- **Rule-based vs. flexible understanding:** We use the LLM for both understanding and tool choice, so we avoid the “rule-based inflexibility” the literature cites (e.g. Comparative Analysis BERT and RoBERTa). We trade some predictability for flexibility.

- **Security and data exposure:** We can run the agentic LLM locally or in a trusted environment and restrict which tools (and thus which data) are exposed. So we align with the concern that “sending the secret information to online services” is problematic (Adopting RAG for LLM-Aided Future Vehicle Design).

- **Controlled use of LLMs:** We use an **agentic** design (LLM chooses tools) but still aim for control via a **fixed tool set**, **structured outputs** where possible, and **evaluation** of reliability and tool misuse. Our project contributes an agentic system designed and evaluated for stakeholder-facing QA in domains where the literature calls for reliability and interpretability.

---

## 5. What Further Research Might Be Needed

- **Empirical comparison:** Compare our hybrid pipeline (intent → deterministic function → executor → interpreter) against pure RAG chatbots and agentic LLM systems on the same stakeholder QA tasks (e.g. automotive, compliance) for accuracy, hallucination rate, latency, and interpretability.
- **Intent model choice:** Systematically compare LLM-based intent vs. BERT/RoBERTa vs. few-shot (MAML + embeddings) vs. classical ML (e.g. Naive Bayes, Logistic Regression) for intent accuracy, robustness to paraphrasing, and required training data — and their interaction with the deterministic function selector.
- **RAG in our pipeline:** If RAG is added (e.g. for the interpreter or for disambiguation), study which retrieval/re-ranking strategies (as in Tax Law RAG, Optimizing RAG for Automotive PDF Chatbots) work best and how they interact with our separation of intent, execution, and interpretation.
- **Formalisation and safety:** Investigate how to export or formalise our “function map” and preconditions so they can be checked against regulatory or safety requirements.
- **Scaling and maintenance:** Study the cost of maintaining the intent→function map and preconditions as the domain grows (new intents, new functions, new data sources) and how to semi-automate or recommend updates from usage logs or feedback.
- **Multimodal and enterprise:** If extending to enterprise or multimodal settings, combine our architecture with security filtering and multi-source retrieval, and, if relevant, with hallucination detection for any generative part.

---

## 6. According to These Papers, What Might Be the Downsides / Limitations of Our Approach

- **LLM tool choice and format compliance:**  
  **Paper:** Enhancing LLM Function Calling with Structured Outputs (*deepa_papers.txt*).  
  **Quote:** “The prevalent approach relies on instructing the LLM via system prompts to produce outputs adhering to a specified schema. While often effective, this method can suffer from inconsistencies, where the LLM fails to strictly follow the requested format, leading to parsing errors and unreliable behavior in downstream applications.”  
  **Implication for us:** Our agentic LLM must output valid tool calls. If the model does not adhere to the schema, parsing can fail or the wrong tool may be invoked. We may need constrained decoding or structured-output methods (as in that paper).

- **Less predictability than deterministic execution:**  
  With agentic design, the LLM chooses which tools to call. Wrong or unnecessary tool choices are possible; behaviour is harder to audit than a rule-based intent→function map. We trade predictability for flexibility.

- **Incomplete responses or missing tools:**  
  If the tool set or data sources do not cover a user need, the system can only refuse or give a partial answer. “Missing relevant information” appears as missing tools or data, not only retrieval.

- **Hallucination and context quality:**  
  **Paper:** Towards Automated Safety Requirements Derivation Using Agent-based RAG (*punnoose_papers.txt*).  
  **Quote:** “If irrelevant or even incorrect context is retrieved, the probability of hallucinations is exacerbated.”  
  **Implication for us:** If we add RAG or extra context for the agent, bad context can worsen hallucinations or tool choice. We should design and evaluate any such addition carefully.

- **Adoption barriers for sensitive data:**  
  **Paper:** Adopting RAG for LLM-Aided Future Vehicle Design (*punnoose_papers.txt*).  
  **Quote:** “Providing documents and other specification-related information in automotive was considered quite problematic — as it involved practically sending the secret information to online services and other parties involved.”  
  **Implication for us:** If the agentic LLM is cloud-based, user queries or tool inputs might be sent externally. We need local or trusted deployment, or strict filtering, so that no sensitive payloads leave the organisation.

---

## 7. According to These Papers, What Might Be the Strengths of Our Approach

- **Explicit need for reliable and explainable LLM outputs:**  
  **Paper:** Towards Automated Safety Requirements Derivation Using Agent-based RAG (*punnoose_papers.txt*).  
  **Quote:** “However, to efficiently support safety engineers in these tasks, LLMs must generate highly reliable and explainable results.”  
  **Strength:** We still aim for reliable and explainable outputs. We can ground the agent in **tool execution results** and use a **fixed tool set** so that answers are tied to actual data; we can evaluate and improve tool-choice reliability.

- **Grounding in execution results:**  
  **Paper:** Enhancing Retrieval and Re-ranking in RAG: A Case Study on Tax Law (*deepa_papers.txt*).  
  **Quote:** “By incorporating retrieved evidence, RAG models significantly reduce hallucinations and improve factual accuracy [4, 5].”  
  **Strength:** We ground the agent in **execution results** from tools (and optionally retrieved context). The LLM does not “invent” data — it reasons over actual tool outputs, which can “reduce hallucinations and improve factual accuracy” when we constrain the agent to use tool results.

- **Deterministic tool execution:**  
  **Paper:** Towards Automated Safety Requirements Derivation Using Agent-based RAG (*punnoose_papers.txt*).  
  **Quote:** “Subsequently, deterministic tools are leveraged to actually solve the task.”  
  **Strength:** Tool *execution* is still deterministic (the executor runs the chosen function and returns data). So “deterministic tools are leveraged to actually solve the task” applies: the LLM chooses *which* tool; the execution step itself is deterministic.

- **Interpretable and layered design:**  
  **Paper:** Enhancing Retrieval and Re-ranking in RAG: A Case Study on Tax Law (*deepa_papers.txt*).  
  **Quote:** “Our findings offer practical insights into building robust and **interpretable RAG systems** for legal and structured text retrieval.”  
  **Strength:** We can keep interpretability by making tool calls, tool results, and final answers inspectable (logged, traceable). If we add RAG as a tool, we can adopt layered retrieval/re-ranking as in the literature.

- **Flexibility and single-model design:**  
  **Papers:** GateLens, GoNoGo, Simple Action Model, Agentic vs. Direct LLM (*punnoose_papers.txt*).  
  **Strength:** Agentic design gives **flexibility**: new tools can be added without maintaining a rule map; the LLM handles paraphrasing and variation. We align with the literature that uses LLMs to choose and orchestrate tools for complex tasks.

- **Security and local deployment:**  
  **Paper:** Adopting RAG for LLM-Aided Future Vehicle Design (*punnoose_papers.txt*).  
  **Quote:** “LLAMA3 and Mistral also show promising capabilities for **local deployment**, **addressing data privacy concerns** in automotive applications.”  
  **Strength:** We can run the agentic LLM locally or in a trusted environment and restrict which tools (and thus which data) are available. So we can “address data privacy concerns” and avoid sending sensitive payloads to external APIs.

---

## Summary Table: Papers Referenced

| Source file | Paper (short) | Section(s) cited |
|-------------|----------------|------------------|
| punnoose_papers.txt | Towards Automated Safety Requirements Derivation Using Agent-based RAG | 3, 4, 6, 7 |
| punnoose_papers.txt | Adopting RAG for LLM-Aided Future Vehicle Design | 3, 4, 6, 7 |
| deepa_papers.txt | Enhancing Retrieval and Re-ranking in RAG: A Case Study on Tax Law | 3, 4, 7 |
| deepa_papers.txt | Comparative Analysis of Intent Classification in Indonesian Chatbots (BERT and RoBERTa) | 3, 4, 6, 7 |
| deepa_papers.txt | Enhancing LLM Function Calling with Structured Outputs | 6 |
| deepa_papers.txt | NNSI for Intent Classification; MAML + embeddings for few-shot intent | 3, 4, 7 |
| deepa_papers.txt | Intent Classification French Recruitment Chatbot (CamemBERT) | 7 |

All cited sentences are quoted from the paper texts in `punnoose_papers.txt` or `deepa_papers.txt` as indicated.
