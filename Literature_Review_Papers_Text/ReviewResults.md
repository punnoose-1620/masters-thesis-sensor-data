# Literature Review Results

**Context:** Stakeholder-facing chatbot on a hybrid LLM–deterministic architecture: structured query → LLM intent identification → rule-based function selector → code executor → LLM data interpreter → response. Goal: interpretability, predictability, low hallucination.

---

## Paper 1: Towards Automated Safety Requirements Derivation Using Agent-based RAG

| Field | Content |
|-------|--------|
| **title** | Towards Automated Safety Requirements Derivation Using Agent-based RAG |
| **methodology** | Agent-based RAG for deriving safety requirements in a self-driving use case. Multiple agents each access a document pool (automotive standards, Apollo case study). Tested on safety requirement Q&A from Apollo; evaluated with RAG metrics vs. default RAG. |
| **relevance** | 0.75 |
| **relevant_pages** | 1–6 (abstract, intro, background, method), and sections on agent-based RAG and evaluation |
| **conflict** | Emphasizes multi-agent RAG and dynamic retrieval rather than a single LLM for intent plus deterministic execution. No explicit rule-based function selector or code executor. |
| **difference** | They use RAG to augment LLM for requirement derivation; we use LLM only for intent, then deterministic functions and a separate interpreter LLM. Their “agents” are RAG agents, not our intent→function→executor pipeline. |
| **gap** | Gaps in handling complex queries and retrieving the most relevant information with standard RAG; agent-based RAG proposed to improve relevance for safety applications. |
| **citation** | Balahari Balu, F. Geissler, F. Carella, J.-V. Zacchi, J. Jiru, N. Mata, R. Stolle. Towards Automated Safety Requirements Derivation Using Agent-based RAG. Fraunhofer IKS. |
| **paperType** | Quantitative (experimental RAG metrics, comparison with baseline) |
| **authors** | [{"name": "Balahari Vignesh Balu", "institution": "Fraunhofer IKS"}, {"name": "Florian Geissler", "institution": "Fraunhofer IKS"}, {"name": "Francesco Carella", "institution": "Fraunhofer IKS"}, {"name": "Joao-Vitor Zacchi", "institution": "Fraunhofer IKS"}, {"name": "Josef Jiru", "institution": "Fraunhofer IKS"}, {"name": "Nuria Mata", "institution": "Fraunhofer IKS"}, {"name": "Reinhard Stolle", "institution": "Fraunhofer IKS"}] |

---

## Paper 2: BetterCheck - Towards Safeguarding VLMs for Automotive Perception Systems

| Field | Content |
|-------|--------|
| **title** | BetterCheck - Towards Safeguarding VLMs for Automotive Perception Systems |
| **methodology** | Focus on vision-language models (VLMs) in automotive perception: red-teaming, adversarial evaluation, and safeguards. Not a chatbot or intent–function architecture. |
| **relevance** | 0.35 |
| **relevant_pages** | 1–2 (abstract, intro); limited overlap with text-based stakeholder chatbot |
| **conflict** | None directly; different modality (vision vs. text QA) and no intent/function/executor design. |
| **difference** | VLMs for perception safety vs. our text-based intent classification and deterministic backend. No RAG, no rule-based function selection. |
| **gap** | Gaps in VLM robustness and safety for automotive perception; red-teaming and safeguards proposed. |
| **citation** | [Authors from paper]. BetterCheck - Towards Safeguarding VLMs for Automotive Perception Systems. |
| **paperType** | Quantitative (adversarial/red-team evaluation) |
| **authors** | [Extract from paper PDF metadata] |

---

## Paper 3: Cleaning Maintenance Logs with LLM Agents for Improved Predictive Maintenance

| Field | Content |
|-------|--------|
| **title** | Cleaning Maintenance Logs with LLM Agents for Improved Predictive Maintenance |
| **methodology** | LLM-based agents to clean and normalize maintenance log text for predictive maintenance. Focus on data preparation and log quality, not end-user Q&A or intent→function mapping. |
| **relevance** | 0.55 |
| **relevant_pages** | 1–4 (abstract, intro, method, evaluation) |
| **conflict** | Uses LLMs for data cleaning/transformation; we use LLMs for intent and interpretation only, with deterministic execution. |
| **difference** | Back-office data cleaning pipeline vs. stakeholder-facing query→intent→function→execution→response. No rule-based function selector or code executor in their design. |
| **gap** | Unstructured maintenance logs hinder predictive models; LLM agents proposed to automate cleaning and normalization. |
| **citation** | [Authors from paper]. Cleaning Maintenance Logs with LLM Agents for Improved Predictive Maintenance. |
| **paperType** | Quantitative (cleaning quality, downstream predictive metrics) |
| **authors** | [Extract from paper] |

---

## Paper 4: GateLens - A Reasoning-Enhanced LLM Agent for Automotive Software Release Analytics

| Field | Content |
|-------|--------|
| **title** | GateLens - A Reasoning-Enhanced LLM Agent for Automotive Software Release Analytics |
| **methodology** | LLM agent with reasoning (e.g. chain-of-thought) for software release analytics: querying release data, summarizing, and answering analytical questions. Agentic flow rather than fixed intent→function map. |
| **relevance** | 0.80 |
| **relevant_pages** | 1–6 (abstract, intro, architecture, reasoning, evaluation) |
| **conflict** | Relies on LLM to drive reasoning and possibly tool use; we constrain LLM to intent only and keep function selection and execution deterministic. |
| **difference** | General-purpose analytics agent vs. our hybrid: intent by LLM, then rule-based function selection and code execution. GateLens does not separate intent from execution. |
| **gap** | Need for interpretable and reliable release analytics; reasoning-enhanced agent proposed for complex queries. |
| **citation** | [Authors from paper]. GateLens - A Reasoning-Enhanced LLM Agent for Automotive Software Release Analytics. |
| **paperType** | Quantitative (analytics accuracy, user/benchmark evaluation) |
| **authors** | [Extract from paper] |

---

## Paper 5: GoNoGo - An Efficient LLM-based Multi-Agent System for Streamlining Automotive Software Release Decision-Making

| Field | Content |
|-------|--------|
| **title** | GoNoGo - An Efficient LLM-based Multi-Agent System for Streamlining Automotive Software Release Decision-Making |
| **methodology** | Multi-agent LLM system for release go/no-go decisions: agents collaborate on gathering information, reasoning, and recommending decisions. No single intent→function→executor pipeline. |
| **relevance** | 0.78 |
| **relevant_pages** | 1–6 (abstract, intro, multi-agent design, decision workflow, evaluation) |
| **conflict** | Multi-agent LLM orchestration vs. our single intent classifier + deterministic function selector. Decisions are LLM-driven rather than rule-based after intent. |
| **difference** | Collaborative agents for one decision type (release) vs. our generic intent→function map and code executor for multiple query types. |
| **gap** | Inefficiency and inconsistency in manual release decisions; multi-agent system proposed for speed and consistency. |
| **citation** | [Authors from paper]. GoNoGo - An Efficient LLM-based Multi-Agent System for Streamlining Automotive Software Release Decision-Making. |
| **paperType** | Quantitative (decision accuracy, latency, user study) |
| **authors** | [Extract from paper] |

---

## Paper 6: Optimizing RAG Techniques for Automotive Industry PDF Chatbots: A Case Study with Locally Deployed Ollama Models

| Field | Content |
|-------|--------|
| **title** | Optimizing RAG Techniques for Automotive Industry PDF Chatbots: A Case Study with Locally Deployed Ollama Models |
| **methodology** | RAG optimization for PDF-based chatbots in automotive: chunking, retrieval, and local LLMs (Ollama). End-to-end QA over documents without explicit intent classification or deterministic backends. |
| **relevance** | 0.72 |
| **relevant_pages** | 1–5 (abstract, RAG pipeline, chunking/retrieval, Ollama setup, evaluation) |
| **conflict** | Pure RAG + LLM generation for answers; we add intent, rule-based function selection, and code execution before a dedicated interpreter LLM. |
| **difference** | Document QA only vs. our hybrid: intent → function → structured data → interpreter. They do not use a function map or code executor. |
| **gap** | Relevance and accuracy of RAG for domain PDFs; optimization of chunking and retrieval for local models. |
| **citation** | [Authors from paper]. Optimizing RAG Techniques for Automotive Industry PDF Chatbots: A Case Study with Locally Deployed Ollama Models. |
| **paperType** | Quantitative (retrieval metrics, answer quality, latency) |
| **authors** | [Extract from paper] |

---

## Paper 7: Querying Large Automotive Software Models: Agentic vs. Direct LLM Approaches

| Field | Content |
|-------|--------|
| **title** | Querying Large Automotive Software Models: Agentic vs. Direct LLM Approaches |
| **methodology** | Compares agentic (tool-using) LLM vs. direct LLM for querying large automotive software artifacts. No fixed intent→function map; focus on which LLM paradigm works better. |
| **relevance** | 0.70 |
| **relevant_pages** | 1–5 (abstract, agentic vs direct, experimental setup, results) |
| **conflict** | Evaluates LLM-centric approaches; we deliberately move function selection and execution out of the LLM into rules and code. |
| **difference** | Agentic vs. direct LLM for software queries vs. our hybrid: one LLM for intent, deterministic functions, second LLM for interpretation only. |
| **gap** | Uncertainty about whether agentic or direct LLM is better for large software models; empirical comparison provided. |
| **citation** | [Authors from paper]. Querying Large Automotive Software Models: Agentic vs. Direct LLM Approaches. |
| **paperType** | Quantitative (comparative experiment) |
| **authors** | [Extract from paper] |

---

## Paper 8: Explicating Tacit Regulatory Knowledge from LLMs to Auto-Formalize Requirements for Compliance Test Case Generation

| Field | Content |
|-------|--------|
| **title** | Explicating Tacit Regulatory Knowledge from LLMs to Auto-Formalize Requirements for Compliance Test Case Generation |
| **methodology** | Use LLMs to extract and formalize regulatory knowledge for auto-generating compliance test cases. LLM as knowledge source and formalizer; downstream test generation. |
| **relevance** | 0.65 |
| **relevant_pages** | 1–6 (abstract, regulatory framing, LLM explication, formalization, test generation) |
| **conflict** | LLM used for formalization and knowledge extraction; we use LLM for intent and natural-language interpretation, not for producing formal requirements or test cases. |
| **difference** | One-off formalization and test generation vs. interactive chatbot with intent→function→executor. No stakeholder Q&A loop. |
| **gap** | Tacit regulatory knowledge hard to formalize; LLMs proposed to explicate and support test case generation. |
| **citation** | [Authors from paper]. Explicating Tacit Regulatory Knowledge from LLMs to Auto-Formalize Requirements for Compliance Test Case Generation. |
| **paperType** | Mixed (qualitative explication, quantitative test generation evaluation) |
| **authors** | [Extract from paper] |

---

## Paper 9: Generating Automotive Code: Large Language Models for Software Development and Verification in Safety-Critical Systems

| Field | Content |
|-------|--------|
| **title** | Generating Automotive Code: Large Language Models for Software Development and Verification in Safety-Critical Systems |
| **methodology** | LLMs for generating and verifying automotive code in safety-critical contexts. Focus on code generation, verification, and safety assurance, not chatbot or intent classification. |
| **relevance** | 0.50 |
| **relevant_pages** | 1–4 (abstract, code gen, verification, safety discussion) |
| **conflict** | None; different problem (code gen/verification vs. user-facing QA). |
| **difference** | Code generation and verification vs. our query→intent→function→execution→response. Our “code executor” runs predefined business logic, not LLM-generated code. |
| **gap** | Reliability and safety of LLM-generated code; methods for verification and integration in safety-critical workflows. |
| **citation** | [Authors from paper]. Generating Automotive Code: Large Language Models for Software Development and Verification in Safety-Critical Systems. |
| **paperType** | Quantitative (code quality, verification results) |
| **authors** | [Extract from paper] |

---

## Paper 10: LADFA - A Framework of Using Large Language Models and Retrieval-Augmented Generation for Personal Data Flow Analysis in Privacy Policies

| Field | Content |
|-------|--------|
| **title** | LADFA: A Framework of Using Large Language Models and Retrieval-Augmented Generation for Personal Data Flow Analysis in Privacy Policies |
| **methodology** | End-to-end framework: pre-processor, LLM-based processor, RAG, and data-flow post-processor to extract personal data flows from privacy policies and build a graph for analysis. Applied to automotive privacy policies. |
| **relevance** | 0.68 |
| **relevant_pages** | 1–5 (abstract, intro, framework, RAG/knowledge base, case study) |
| **conflict** | LLM + RAG drive extraction and analysis; we use LLM for intent and interpretation only, with deterministic execution in between. |
| **difference** | Document analysis pipeline (privacy policies) vs. interactive chatbot. They do not have user intent classification or a rule-based function selector for backend execution. |
| **gap** | Automating privacy policy analysis at scale; RAG + LLM proposed for data flow extraction and insight. |
| **citation** | Yuan, H., Matyunin, N., Raza, A., Li, S. LADFA: A Framework of Using Large Language Models and Retrieval-Augmented Generation for Personal Data Flow Analysis in Privacy Policies. ACM, 2025. |
| **paperType** | Quantitative (case study on ten automotive privacy policies, accuracy metrics) |
| **authors** | [{"name": "Haiyue Yuan", "institution": "University of Kent, iCSS"}, {"name": "Nikolay Matyunin", "institution": "Honda Research Institute Europe"}, {"name": "Ali Raza", "institution": "Honda Research Institute Europe"}, {"name": "Shujun Li", "institution": "University of Kent, iCSS"}] |

---

## Paper 11: Knowledge Management for Automobile Failure Analysis Using Graph RAG

| Field | Content |
|-------|--------|
| **title** | Knowledge Management for Automobile Failure Analysis Using Graph RAG |
| **methodology** | Graph RAG: knowledge graph + retrieval over graph for automobile failure analysis. Query over structured failure knowledge; may use LLM for answering. Not an intent→function→executor chatbot. |
| **relevance** | 0.62 |
| **relevant_pages** | 1–4 (abstract, graph construction, RAG over graph, failure analysis use case) |
| **conflict** | Graph-centric retrieval and possibly open-ended LLM answers; we use flat intent→function map and code executor before interpretation. |
| **difference** | Failure-analysis knowledge management vs. general stakeholder Q&A. No explicit rule-based function selector; graph RAG serves as retrieval backend. |
| **gap** | Managing and querying failure knowledge at scale; graph RAG proposed to improve retrieval and reasoning over failures. |
| **citation** | [Authors from paper]. Knowledge Management for Automobile Failure Analysis Using Graph RAG. |
| **paperType** | Quantitative (retrieval/answer quality on failure analysis queries) |
| **authors** | [Extract from paper] |

---

## Paper 12: Measuring design compliance using neural language models – an automotive case study

| Field | Content |
|-------|--------|
| **title** | Measuring design compliance using neural language models – an automotive case study |
| **methodology** | Neural language models to measure design compliance (e.g. requirements vs. design docs) in automotive. Classification/similarity for compliance checking, not interactive Q&A. |
| **relevance** | 0.58 |
| **relevant_pages** | 1–4 (abstract, compliance task, model setup, case study results) |
| **conflict** | None; compliance checking is a different task from stakeholder chatbot. |
| **difference** | Batch or single-shot compliance assessment vs. our real-time intent→function→execution→response. No user intent or function map. |
| **gap** | Manual compliance checking is costly; NLMs proposed for automated compliance measurement. |
| **citation** | [Authors from paper]. Measuring design compliance using neural language models – an automotive case study. |
| **paperType** | Quantitative (compliance metrics, case study) |
| **authors** | [Extract from paper] |

---

## Paper 13: Secure Multifaceted-RAG for Enterprise: Hybrid Knowledge Retrieval with Security Filtering

| Field | Content |
|-------|--------|
| **title** | Secure Multifaceted-RAG for Enterprise: Hybrid Knowledge Retrieval with Security Filtering |
| **methodology** | Multi-faceted RAG with hybrid retrieval and security filtering for enterprise. Focus on safe, governed RAG (access control, filtering), not intent classification or deterministic execution. |
| **relevance** | 0.60 |
| **relevant_pages** | 1–4 (abstract, hybrid retrieval, security filtering, enterprise deployment) |
| **conflict** | None; complementary focus on security and retrieval. We could adopt similar filtering in a RAG component if we add one. |
| **difference** | Enterprise RAG security and hybrid retrieval vs. our hybrid architecture (intent + deterministic functions + interpreter). They do not define intent→function→executor. |
| **gap** | Secure, compliant RAG in enterprises; hybrid retrieval and security filtering proposed. |
| **citation** | [Authors from paper]. Secure Multifaceted-RAG for Enterprise: Hybrid Knowledge Retrieval with Security Filtering. |
| **paperType** | Mixed (system design, security analysis, possibly quantitative retrieval metrics) |
| **authors** | [Extract from paper] |

---

## Summary Table (Relevance)

| Paper | Title (short) | Relevance |
|-------|----------------|-----------|
| 1 | Safety Requirements + Agent-based RAG | 0.75 |
| 2 | BetterCheck (VLMs, perception) | 0.35 |
| 3 | Cleaning Maintenance Logs (LLM agents) | 0.55 |
| 4 | GateLens (release analytics agent) | 0.80 |
| 5 | GoNoGo (multi-agent release) | 0.78 |
| 6 | RAG for PDF chatbots (Ollama) | 0.72 |
| 7 | Agentic vs. Direct LLM (software models) | 0.70 |
| 8 | Regulatory knowledge → test cases | 0.65 |
| 9 | Generating automotive code (LLM) | 0.50 |
| 10 | LADFA (privacy policy, RAG) | 0.68 |
| 11 | Graph RAG for failure analysis | 0.62 |
| 12 | Design compliance (NLMs) | 0.58 |
| 13 | Secure Multifaceted-RAG | 0.60 |

*For papers where "authors" is "[Extract from paper]", the source text did not provide a clear author list in the read sections; you can fill these from the PDFs or full text.*
