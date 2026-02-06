# Comparison Report: Our Idea vs. Literature (Punnoose & Deepa Papers)

This report compares the project idea (from *LiteratureReviewHelper.ipynb*, PROJECT_CONTEXT) with the ideas implemented in the papers contained in `punnoose_papers.txt` and `deepa_papers.txt`. Each factual claim is cited to a specific paper with the relevant sentence.

---

## 1. Our Idea

Our proposed system is a **stakeholder-facing chatbot** that answers user queries by combining:

- **LLM-based intent understanding** — An Intent Identifier (e.g., Gemini, GPT, Claude) classifies the user’s intent, assigns confidence, and groups intents; it is used only for semantic understanding, not for execution.
- **Deterministic function selection** — A non-LLM, rule-based Function Selector maps intents to predefined backend functions, validates inputs and preconditions, and decides whether to execute or request clarification.
- **Structured data retrieval and execution** — A Code Executor runs the selected function, fetches data from structured sources (databases, predefined datasets), applies business logic, and produces raw structured data with no natural language generation at this stage.
- **LLM-based result interpretation** — A Data Interpreter (LLM) turns raw execution results into human-readable explanations, summaries, and contextual insights; it has no access to execution logic and operates only on raw data, the original query, and optional metadata.

**Core design principle:** Separate reasoning from execution to ensure **predictability**, **controllability**, **reduced hallucination risk**, and **easier comparison** with task-oriented dialogue systems, slot-filling approaches, and agent-based LLM workflows. Critical decisions (which function to run, what to execute) are **rule-based and auditable**; LLMs are used only where probabilistic reasoning is beneficial (understanding and explaining).

**Positioning:** The system is comparable to task-oriented dialogue systems (TOD), LLM agent frameworks (ReAct, Toolformer, AutoGPT), hybrid neuro-symbolic architectures, and enterprise conversational AI platforms. Key differentiators: **dual-LLM design** (intent + interpretation), **deterministic execution core**, and **explicit input and function schemas**.

---

## 2. Our Research Questions

Derived from the project context and positioning:

1. **Separation of concerns:** Can separating *understanding* (LLM intent), *decision* (rule-based function selection), *execution* (code executor), and *explanation* (LLM interpreter) reduce hallucination and improve interpretability compared to end-to-end RAG or agentic LLM systems?
2. **Intent vs. execution:** Does using the LLM only for intent classification (and interpretation), with deterministic function selection and execution, yield more predictable and auditable behaviour than systems where the LLM chooses and invokes tools/functions?
3. **Stakeholder-facing QA:** How does this hybrid architecture perform for stakeholder-facing question answering over structured data (e.g., domain datasets, databases) compared to pure RAG chatbots or multi-agent LLM systems in similar domains (e.g., automotive, compliance)?
4. **Comparability:** How does the design compare with slot-filling, semantic frame parsing, and ontology-driven dialogue systems in terms of ambiguity handling, confidence-aware behaviour, and explainability?

---

## 3. Research Gaps Common to All Papers in These Text Files

Across **punnoose_papers.txt** (14 papers) and **deepa_papers.txt** (23 papers), the following gaps recur:

| Gap | Papers (representative) |
|-----|-------------------------|
| **Hallucination and reliability** | LLMs must produce “highly reliable and explainable results” (Safety Requirements RAG); “LLMs and VLMs are prone to hallucination” (BetterCheck); RAG can “reduce hallucinations and improve factual accuracy” when retrieval is good, but “if irrelevant or even incorrect context is retrieved, the probability of hallucinations is exacerbated” (Tax Law RAG; Safety Requirements RAG). |
| **Retrieval relevance** | “Existing RAG approaches … their performance deteriorates when handling complex queries and it becomes increasingly harder to retrieve the most relevant information” (Safety Requirements RAG); “Traditional RAG systems rely heavily on internal document retrieval, which can lead to incomplete or inaccurate responses when relevant information is missing” (Secure Multifaceted-RAG). |
| **Domain-specific knowledge** | “Conventional approaches that utilise pre-trained LLMs to assist in safety analyses typically lack domain-specific knowledge” (Safety Requirements RAG); “The limitation of a lack of domain-specific knowledge in understanding technical terms and processes within automotive and safety domains is acknowledged” (Explicating Tacit Regulatory Knowledge). |
| **Intent classification with limited data** | “The dependency on large annotated datasets remains a critical bottleneck”; “the need for models to understand and classify intents with minimal training data” (MAML + embeddings for few-shot intent); “Intent classifiers are generally lacking in real-world training data” (NNSI for intent classification). |
| **Rule-based vs. flexible understanding** | “Rule-based systems are inflexible, involve high development and maintenance costs due to the need for manual updates, and are less robust to variations in user input, often failing to recognize intent in cases of misspellings, slang, or acronyms” (Comparative Analysis BERT and RoBERTa for Indonesian Chatbots). |
| **Security and data exposure** | “Providing documents and other specification-related information in automotive was considered quite problematic — as it involved practically sending the secret information to online services and other parties involved” (Adopting RAG for LLM-Aided Future Vehicle Design); “leveraging external Large Language Models … introduces security risks and high operational costs” (Secure Multifaceted-RAG). |
| **Controlled use of LLMs** | Many papers use LLMs for end-to-end generation, tool choice, or multi-agent orchestration without a deterministic “execution core”; few explicitly separate *intent only* (LLM) from *function selection and execution* (rules/code). |

---

## 4. How Our Project Can Address This Research Gap

- **Hallucination and reliability:** We restrict the LLM to *intent* and *interpretation* and keep *which function runs* and *what code executes* deterministic. So retrieval errors or model drift affect only understanding and wording, not which backend runs or what data is fetched — reducing the risk that “irrelevant or even incorrect context” leads to wrong actions. *Cite: “The risk of hallucinations is related to the information accessible to the LLM, and its suitability to solve the task at hand” (Towards Automated Safety Requirements Derivation Using Agent-based RAG).* By giving the interpreter only *retrieved execution results* (and optional metadata), we align with the need for “highly reliable and explainable results” in safety-sensitive settings.

- **Retrieval relevance:** Where we add RAG (e.g. for the interpreter or for intent disambiguation), we can adopt the same directions as the literature: hybrid retrieval, re-ranking, and chunking strategies (e.g. Enhancing Retrieval and Re-ranking in RAG, Chunking Techniques, Optimizing RAG for Automotive PDF Chatbots). Our architecture still bounds the impact of bad retrieval: bad retrieval cannot directly change *which* function is selected, because that is rule-based from the intent label.

- **Domain-specific knowledge:** We do not rely on the LLM to “know” the domain; we inject domain through the **function map**, **preconditions**, and **structured data sources**. So we address “lack of domain-specific knowledge” by encoding domain in the deterministic layer (functions, schemas, data) rather than in the model’s parameters. *Cite: “To integrate additional domain-specific information, techniques such as fine-tuning or retrieval-augmented generation (RAG) are commonly used” (Safety Requirements RAG).* We combine that with a fixed intent→function mapping so domain behaviour is auditable.

- **Intent with limited data:** Our intent layer can use the same techniques as the reviewed papers: few-shot or zero-shot LLM intent detection, MAML + embeddings for few-shot intent, NNSI-style data augmentation, or traditional classifiers (BERT/RoBERTa, Naive Bayes, Logistic Regression) when labels exist. So we address “lack of real-world training data” and “minimal training data” by allowing pluggable intent models and, where needed, small labelled sets or augmentation.

- **Rule-based inflexibility:** We keep rules only for *function selection* (intent → function), not for *understanding* the user. Understanding is done by the LLM, which handles paraphrasing, misspellings, and variation; the rule layer then maps the *interpreted intent* to a function. So we mitigate “rule-based systems are inflexible … less robust to variations in user input” by using the LLM for robustness and rules for controllability. *Cite: Comparative Analysis of Intent Classification in Indonesian Chatbots (BERT and RoBERTa).*

- **Security and data exposure:** We can run the intent LLM and the interpreter LLM locally or in a trusted environment; the only component that must access structured data is the Code Executor, which does not send raw user text or proprietary docs to external APIs. So we align with the concern that “sending the secret information to online services” is problematic (Adopting RAG for LLM-Aided Future Vehicle Design) and with the need for “confidentiality-preserving filter” and “proprietary corporate data is not sent to external models” (Secure Multifaceted-RAG).

- **Controlled use of LLMs:** We explicitly separate “understanding ≠ decision ≠ execution ≠ explanation.” No reviewed paper in these sets proposes exactly this split: many use RAG + one LLM for full answers, or multi-agent LLM orchestration, or LLM-driven function/tool choice. Our project fills the gap of a **hybrid architecture with a deterministic execution core** and dual-LLM (intent + interpreter) design.

---

## 5. What Further Research Might Be Needed

- **Empirical comparison:** Compare our hybrid pipeline (intent → deterministic function → executor → interpreter) against pure RAG chatbots and agentic LLM systems on the same stakeholder QA tasks (e.g. automotive, compliance) for accuracy, hallucination rate, latency, and interpretability.
- **Intent model choice:** Systematically compare LLM-based intent vs. BERT/RoBERTa vs. few-shot (MAML + embeddings) vs. classical ML (e.g. Naive Bayes, Logistic Regression) for intent accuracy, robustness to paraphrasing, and required training data — and their interaction with the deterministic function selector.
- **RAG in our pipeline:** If RAG is added (e.g. for the interpreter or for disambiguation), study which retrieval/re-ranking/chunking strategies (as in Tax Law RAG, Chunking Techniques, Optimizing RAG for Automotive PDF Chatbots) work best and how they interact with our separation of intent, execution, and interpretation.
- **Formalisation and safety:** Investigate how to export or formalise our “function map” and preconditions so they can be checked against regulatory or safety requirements (linking to themes in Explicating Tacit Regulatory Knowledge and Generating Automotive Code).
- **Scaling and maintenance:** Study the cost of maintaining the intent→function map and preconditions as the domain grows (new intents, new functions, new data sources) and how to semi-automate or recommend updates from usage logs or feedback.
- **Multimodal and enterprise:** If extending to enterprise or multimodal settings, combine our architecture with security filtering and multi-source retrieval (as in Secure Multifaceted-RAG) and, if relevant, with hallucination detection (as in BetterCheck) for any generative part.

---

## 6. According to These Papers, What Might Be the Downsides / Limitations of Our Approach

- **Rule-based inflexibility and maintenance:**  
  **Paper:** Comparative Analysis of Intent Classification in Indonesian Chatbots Using BERT and RoBERTa Models (*deepa_papers.txt*).  
  **Quote:** “Rule-based systems are inflexible [3], involve high development and maintenance costs due to the need for manual updates [4], and are less robust to variations in user input, often failing to recognize intent in cases of misspellings, slang, or acronyms [5].”  
  **Implication for us:** Our *function selector* is rule-based (intent → function). If the intent set or function map is large, manual updates and preconditions could become costly. We mitigate by using an LLM for *understanding* (so robustness to variation is in the intent layer), but the rule layer itself remains rigid and must be kept in sync with the domain.

- **LLM format compliance when used for intent:**  
  **Paper:** Enhancing LLM Function Calling with Structured Outputs (*deepa_papers.txt*).  
  **Quote:** “The prevalent approach relies on instructing the LLM via system prompts to produce outputs adhering to a specified schema. While often effective, this method can suffer from inconsistencies, where the LLM fails to strictly follow the requested format, leading to parsing errors and unreliable behavior in downstream applications.”  
  **Implication for us:** Our intent layer expects the LLM to output a *structured intent label*. If the model does not adhere to the schema, parsing can fail and the deterministic selector may get wrong or empty input, leading to fallback or errors. We may need constrained decoding or structured-output methods (as in that paper) for the intent LLM.

- **Incomplete responses when retrieval/data is missing:**  
  **Paper:** Secure Multifaceted-RAG for Enterprise: Hybrid Knowledge Retrieval with Security Filtering (*punnoose_papers.txt*).  
  **Quote:** “Traditional RAG systems rely heavily on internal document retrieval, which can lead to incomplete or inaccurate responses when relevant information is missing.”  
  **Implication for us:** We are not RAG-only; we have a Code Executor over structured data. If the function map or data sources do not cover a user need, our system can only clarify or refuse — we might produce “incomplete” answers in the sense of not covering unmodelled intents or missing data. So the limitation of “missing relevant information” appears as *missing functions or data* in our design, not only missing retrieval.

- **Hallucination in the interpreter:**  
  **Paper:** Towards Automated Safety Requirements Derivation Using Agent-based RAG (*punnoose_papers.txt*).  
  **Quote:** “If irrelevant or even incorrect context is retrieved, the probability of hallucinations is exacerbated.”  
  **Implication for us:** Our Data Interpreter receives *execution results* (and optional context). If we later add RAG for the interpreter, the same risk applies: bad or irrelevant context could lead the interpreter to “hallucinate” around the answer. So any RAG used in the interpretation stage should be designed and evaluated to avoid exacerbating hallucinations.

- **Adoption barriers for sensitive data:**  
  **Paper:** Adopting RAG for LLM-Aided Future Vehicle Design (*punnoose_papers.txt*).  
  **Quote:** “Providing documents and other specification-related information in automotive was considered quite problematic — as it involved practically sending the secret information to online services and other parties involved. For that reason, the adoption of LLM-aided tools in automotive was considered quite problematic.”  
  **Implication for us:** If the *intent* or *interpreter* LLM is cloud-based, user queries or internal context might be sent to external services. To avoid the same adoption barrier, we need local or trusted deployment for both LLMs, or strict filtering so that no sensitive payloads leave the organisation (as in Secure Multifaceted-RAG).

- **Less flexibility than full agentic LLM:**  
  Papers such as GateLens, GoNoGo, Simple Action Model, and Querying Large Automotive Software Models (agentic vs. direct) use the LLM to *choose* tools or *orchestrate* steps. Our approach fixes the set of functions and the mapping from intent to function. So we trade flexibility (e.g. arbitrary tool chains, new tools at runtime) for predictability and auditability — which can be a limitation in highly dynamic or exploratory use cases.

---

## 7. According to These Papers, What Might Be the Strengths of Our Approach

- **Explicit need for reliable and explainable LLM outputs:**  
  **Paper:** Towards Automated Safety Requirements Derivation Using Agent-based RAG (*punnoose_papers.txt*).  
  **Quote:** “However, to efficiently support safety engineers in these tasks, LLMs must generate highly reliable and explainable results.”  
  **Strength:** Our design separates *generation of the final answer* (Data Interpreter) from *decision and execution*. The interpreter only explains *given* data; it does not decide which function runs or what data is fetched. That makes it easier to constrain and explain outputs and aligns with the need for “highly reliable and explainable results” in safety or compliance contexts.

- **Grounding and hallucination reduction via retrieval/context:**  
  **Paper:** Enhancing Retrieval and Re-ranking in RAG: A Case Study on Tax Law (*deepa_papers.txt*).  
  **Quote:** “By incorporating retrieved evidence, RAG models significantly reduce hallucinations and improve factual accuracy [4, 5].”  
  **Strength:** We ground the *interpreter* in **execution results** (and optionally in retrieved context). So we do not ask the LLM to “invent” which backend to call or what data exists — we give it the actual output of the Code Executor. That is a form of strong grounding that can “reduce hallucinations and improve factual accuracy” for the answer text, as long as the interpreter is constrained to the provided data.

- **Deterministic tools for solving the task:**  
  **Paper:** Towards Automated Safety Requirements Derivation Using Agent-based RAG (*punnoose_papers.txt*).  
  **Quote:** “Subsequently, deterministic tools are leveraged to actually solve the task.”  
  **Strength:** The reviewed paper itself uses “deterministic tools” after retrieval/LLM steps. Our architecture makes this explicit: the **Function Selector** and **Code Executor** are deterministic. So “deterministic tools are leveraged to actually solve the task” is a direct strength of our approach — we centralise the solving step in a deterministic core rather than in the LLM.

- **Interpretable RAG / knowledge-aware systems:**  
  **Paper:** Enhancing Retrieval and Re-ranking in RAG: A Case Study on Tax Law (*deepa_papers.txt*).  
  **Quote:** “These results highlight the importance of layered architecture that integrates both hybrid retrieval and re-ranking to enhance relevance, especially in regulation-heavy domains. Our findings offer practical insights into building robust and **interpretable RAG systems** for legal and structured text retrieval.”  
  **Strength:** We prioritise interpretability by making each layer inspectable: intent (LLM), function choice (rules), execution (code), explanation (LLM on fixed data). So we align with the goal of “interpretable” systems; if we add RAG, we can adopt similar layered retrieval/re-ranking for the parts that need it.

- **Intent classification as a core, well-studied component:**  
  **Papers:** e.g. Comparative Analysis of Intent Classification in Indonesian Chatbots (BERT and RoBERTa), Intent Classification French Recruitment Chatbot (CamemBERT), NNSI for Intent Classification, MAML + embeddings for few-shot intent (*deepa_papers.txt*).  
  **Strength:** The literature treats intent classification as central to chatbots and dialogue systems. Our design puts **intent** at the centre and then connects it to a **deterministic** backend. So we build on a well-understood, comparable component (intent classification) while differentiating in the execution layer (rule-based function selection + code executor).

- **Security and local deployment:**  
  **Paper:** Adopting RAG for LLM-Aided Future Vehicle Design (*punnoose_papers.txt*).  
  **Quote:** “Our results demonstrate that while GPT-4 offers superior performance, LLAMA3 and Mistral also show promising capabilities for **local deployment**, **addressing data privacy concerns** in automotive applications.”  
  **Strength:** Our pipeline can run with local or trusted LLMs for intent and interpreter; only the Code Executor needs to touch internal data. So we can “address data privacy concerns” by avoiding sending sensitive documents or user inputs to external APIs, consistent with the emphasis on local deployment and privacy in the literature.

- **Separation of parametric knowledge and execution:**  
  **Paper:** RAGRouter and related RAG/LLM papers (*punnoose* / *deepa*) discuss “parametric knowledge” vs. “retrieval-induced” behaviour.  
  **Strength:** We clearly separate **what the model knows** (intent semantics, how to explain) from **what the system does** (which function runs, what data is read). That makes it easier to reason about correctness (execution is deterministic) and to update behaviour (change function map or data) without retraining the LLM.

---

## Summary Table: Papers Referenced

| Source file | Paper (short) | Section(s) cited |
|-------------|----------------|------------------|
| punnoose_papers.txt | Towards Automated Safety Requirements Derivation Using Agent-based RAG | 3, 4, 6, 7 |
| punnoose_papers.txt | BetterCheck: Towards Safeguarding VLMs for Automotive Perception Systems | 3, 6 |
| punnoose_papers.txt | Adopting RAG for LLM-Aided Future Vehicle Design | 3, 4, 6, 7 |
| punnoose_papers.txt | Secure Multifaceted-RAG for Enterprise | 3, 4, 6, 7 |
| punnoose_papers.txt | Explicating Tacit Regulatory Knowledge from LLMs | 3 |
| deepa_papers.txt | Enhancing Retrieval and Re-ranking in RAG: A Case Study on Tax Law | 3, 7 |
| deepa_papers.txt | Comparative Analysis of Intent Classification in Indonesian Chatbots (BERT and RoBERTa) | 3, 4, 6, 7 |
| deepa_papers.txt | Enhancing LLM Function Calling with Structured Outputs | 6 |
| deepa_papers.txt | NNSI for Intent Classification; MAML + embeddings for few-shot intent | 3, 4, 7 |
| deepa_papers.txt | Intent Classification French Recruitment Chatbot (CamemBERT) | 7 |

All cited sentences are quoted from the paper texts in `punnoose_papers.txt` or `deepa_papers.txt` as indicated.
