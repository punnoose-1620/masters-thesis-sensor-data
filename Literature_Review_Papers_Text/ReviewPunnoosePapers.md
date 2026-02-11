# Literature Review Results – Punnoose Papers

**Context:** Stakeholder-facing chatbot on a hybrid LLM–deterministic architecture: structured query → LLM intent identification only → rule-based function selector → code executor → LLM data interpreter → response. Goal: interpretability, predictability, low hallucination.

**Thresholding:** Papers are given relevance scores based on how connected they are to our approach. Papers below 0.70 relevance rating are excempted/avoided from further analysis. The below list is arranged on the basis of relevance ratings. 

**Next Step:** Qualitative Analysis for paper's reliability is yet to be done. This will be our next step.

---

## Paper 1: GateLens - A Reasoning-Enhanced LLM Agent for Automotive Software Release Analytics

| Field | Content |
|-------|--------|
| **title** | GateLens: A Reasoning-Enhanced LLM Agent for Automotive Software Release Analytics |
| **methodology** | LLM agent with reasoning (e.g. chain-of-thought) for software release analytics: querying release data, summarizing, answering analytical questions. Agentic flow; tool use / reasoning over release artifacts. No fixed intent→function map. |
| **relevance** | 0.80 |
| **relevant_pages** | 1–6 (abstract, intro, architecture, reasoning, evaluation) |
| **conflict** | Relies on LLM to drive reasoning and possibly tool use; we constrain LLM to intent only and keep function selection and execution deterministic. |
| **difference** | General-purpose analytics agent vs. our hybrid: intent by LLM, then rule-based function selection and code execution. GateLens does not separate intent from execution. |
| **gap** | Need for interpretable and reliable release analytics; reasoning-enhanced agent proposed for complex queries. |
| **citation** | [Authors], "GateLens: A Reasoning-Enhanced LLM Agent for Automotive Software Release Analytics," submitted for publication. |
| **paperType** | Quantitative |
| **authors** | [Extract from paper] |

---

## Paper 2: GoNoGo - An Efficient LLM-based Multi-Agent System for Streamlining Automotive Software Release Decision-Making

| Field | Content |
|-------|--------|
| **title** | GoNoGo: An Efficient LLM-based Multi-Agent System for Streamlining Automotive Software Release Decision-Making |
| **methodology** | Multi-agent LLM system for release go/no-go decisions: agents collaborate on gathering information, reasoning, and recommending decisions. No single intent→function→executor pipeline; LLM-driven orchestration. |
| **relevance** | 0.78 |
| **relevant_pages** | 1–6 (abstract, intro, multi-agent design, decision workflow, evaluation) |
| **conflict** | Multi-agent LLM orchestration vs. our single intent classifier + deterministic function selector. Decisions are LLM-driven rather than rule-based after intent. |
| **difference** | Collaborative agents for one decision type (release) vs. our generic intent→function map and code executor for multiple query types. |
| **gap** | Inefficiency and inconsistency in manual release decisions; multi-agent system proposed for speed and consistency. |
| **citation** | [Authors], "GoNoGo: An Efficient LLM-based Multi-Agent System for Streamlining Automotive Software Release Decision-Making," submitted for publication. |
| **paperType** | Quantitative |
| **authors** | [Extract from paper] |

---

## Paper 3: Adopting RAG for LLM-Aided Future Vehicle Design

| Field | Content |
|-------|--------|
| **title** | Adopting RAG for LLM-Aided Future Vehicle Design |
| **methodology** | Integration of LLMs with RAG for automotive design and software development. Two case studies: standardization compliance chatbot and design copilot; RAG indexing (load, split, store) and retrieval+generation. LangChain/LCEL; evaluation of GPT-4o, LLAMA3, Mistral, Mixtral for accuracy and execution time. Local deployment to address data privacy. |
| **relevance** | 0.76 |
| **relevant_pages** | 1–6 (abstract, intro, RAG background, LangChain, case studies, evaluation) |
| **conflict** | RAG + LLM for end-to-end answers; we use intent classification and deterministic execution before a dedicated interpreter LLM. |
| **difference** | Compliance chatbot and design copilot with RAG vs. our intent→function map and code executor. They do not separate intent from retrieval/generation. |
| **gap** | Sensitive automotive data and cloud LLMs; RAG with local LLMs proposed for design workflows and compliance. |
| **citation** | V. Zolfaghari, N. Petrovic, F. Pan, K. Lebioda, A. Knoll, "Adopting RAG for LLM-Aided Future Vehicle Design," in Proc. IEEE Conf. (Automotive/Software), 2024. |
| **paperType** | Quantitative |
| **authors** | [{"name": "Vahid Zolfaghari", "institution": "Technical University of Munich"}, {"name": "Nenad Petrovic", "institution": "Technical University of Munich"}, {"name": "Fengjun Pan", "institution": "Technical University of Munich"}, {"name": "Krzysztof Lebioda", "institution": "Technical University of Munich"}, {"name": "Alois Knoll", "institution": "Technical University of Munich"}] |

---

## Paper 4: Towards Automated Safety Requirements Derivation Using Agent-based RAG

| Field | Content |
|-------|--------|
| **title** | Towards Automated Safety Requirements Derivation Using Agent-based RAG |
| **methodology** | Agent-based RAG for deriving safety requirements in a self-driving use case. Multiple agents each access a document pool (automotive standards, Apollo case study). Customized retrieval mechanism; RAG pipeline with domain knowledge pre-processing, vector store, refined context retrieval. Tested on safety requirement Q&A from Apollo; evaluated with RAG metrics vs. default RAG. Background: ISO 26262, ISO 21448 (SOTIF), HARA, safety lifecycle. |
| **relevance** | 0.75 |
| **relevant_pages** | 1–6 (abstract, intro, background, method, agent-based RAG, evaluation) |
| **conflict** | Emphasizes multi-agent RAG and dynamic retrieval rather than a single LLM for intent plus deterministic execution. No explicit rule-based function selector or code executor. |
| **difference** | They use RAG to augment LLM for requirement derivation; we use LLM only for intent, then deterministic functions and a separate interpreter LLM. Their “agents” are RAG agents, not our intent→function→executor pipeline. |
| **gap** | Gaps in handling complex queries and retrieving the most relevant information with standard RAG; agent-based RAG proposed to improve relevance for safety applications. |
| **citation** | B. V. Balu, F. Geissler, F. Carella, J.-V. Zacchi, J. Jiru, N. Mata, R. Stolle, "Towards Automated Safety Requirements Derivation Using Agent-based RAG," submitted for publication. |
| **paperType** | Quantitative |
| **authors** | [{"name": "Balahari Vignesh Balu", "institution": "Fraunhofer IKS"}, {"name": "Florian Geissler", "institution": "Fraunhofer IKS"}, {"name": "Francesco Carella", "institution": "Fraunhofer IKS"}, {"name": "Joao-Vitor Zacchi", "institution": "Fraunhofer IKS"}, {"name": "Josef Jiru", "institution": "Fraunhofer IKS"}, {"name": "Nuria Mata", "institution": "Fraunhofer IKS"}, {"name": "Reinhard Stolle", "institution": "Fraunhofer IKS"}] |

---

## Paper 5: Optimizing RAG Techniques for Automotive Industry PDF Chatbots: A Case Study with Locally Deployed Ollama Models

| Field | Content |
|-------|--------|
| **title** | Optimizing RAG Techniques for Automotive Industry PDF Chatbots: A Case Study with Locally Deployed Ollama Models |
| **methodology** | RAG optimization for PDF-based chatbots in automotive: chunking, retrieval, and local LLMs (Ollama). End-to-end QA over documents; indexing (load, split, store), retrieval and generation. No explicit intent classification or deterministic backends. |
| **relevance** | 0.72 |
| **relevant_pages** | 1–5 (abstract, RAG pipeline, chunking/retrieval, Ollama setup, evaluation) |
| **conflict** | Pure RAG + LLM generation for answers; we add intent, rule-based function selection, and code execution before a dedicated interpreter LLM. |
| **difference** | Document QA only vs. our hybrid: intent → function → structured data → interpreter. They do not use a function map or code executor. |
| **gap** | Relevance and accuracy of RAG for domain PDFs; optimization of chunking and retrieval for local models. |
| **citation** | [Authors], "Optimizing RAG Techniques for Automotive Industry PDF Chatbots: A Case Study with Locally Deployed Ollama Models," submitted for publication. |
| **paperType** | Quantitative |
| **authors** | [Extract from paper] |

---

## Paper 6: Querying Large Automotive Software Models: Agentic vs. Direct LLM Approaches

| Field | Content |
|-------|--------|
| **title** | Querying Large Automotive Software Models: Agentic vs. Direct LLM Approaches |
| **methodology** | Compares agentic (tool-using) LLM vs. direct LLM for querying large automotive software artifacts. No fixed intent→function map; focus on which LLM paradigm works better. |
| **relevance** | 0.70 |
| **relevant_pages** | 1–5 (abstract, agentic vs direct, experimental setup, results) |
| **conflict** | Evaluates LLM-centric approaches; we deliberately move function selection and execution out of the LLM into rules and code. |
| **difference** | Agentic vs. direct LLM for software queries vs. our hybrid: one LLM for intent, deterministic functions, second LLM for interpretation only. |
| **gap** | Uncertainty about whether agentic or direct LLM is better for large software models; empirical comparison provided. |
| **citation** | [Authors], "Querying Large Automotive Software Models: Agentic vs. Direct LLM Approaches," submitted for publication. |
| **paperType** | Quantitative |
| **authors** | [Extract from paper] |

---

**CUT-OFF**
---

## Paper 7: LADFA - A Framework of Using Large Language Models and Retrieval-Augmented Generation for Personal Data Flow Analysis in Privacy Policies

| Field | Content |
|-------|--------|
| **title** | LADFA: A Framework of Using Large Language Models and Retrieval-Augmented Generation for Personal Data Flow Analysis in Privacy Policies |
| **methodology** | End-to-end framework: pre-processor, LLM-based processor, RAG, and data-flow post-processor to extract personal data flows from privacy policies and build a graph for analysis. Applied to automotive privacy policies; case study on ten policies. |
| **relevance** | 0.68 |
| **relevant_pages** | 1–5 (abstract, intro, framework, RAG/knowledge base, case study) |
| **conflict** | LLM + RAG drive extraction and analysis; we use LLM for intent and interpretation only, with deterministic execution in between. |
| **difference** | Document analysis pipeline (privacy policies) vs. interactive chatbot. They do not have user intent classification or a rule-based function selector for backend execution. |
| **gap** | Automating privacy policy analysis at scale; RAG + LLM proposed for data flow extraction and insight. |
| **citation** | H. Yuan, N. Matyunin, A. Raza, S. Li, "LADFA: A Framework of Using Large Language Models and Retrieval-Augmented Generation for Personal Data Flow Analysis in Privacy Policies," ACM Trans., vol. 1, no. 1, Jan. 2025, to be published. |
| **paperType** | Quantitative |
| **authors** | [{"name": "Haiyue Yuan", "institution": "University of Kent, iCSS"}, {"name": "Nikolay Matyunin", "institution": "Honda Research Institute Europe"}, {"name": "Ali Raza", "institution": "Honda Research Institute Europe"}, {"name": "Shujun Li", "institution": "University of Kent, iCSS"}] |

---

## Paper 8: Explicating Tacit Regulatory Knowledge from LLMs to Auto-Formalize Requirements for Compliance Test Case Generation

| Field | Content |
|-------|--------|
| **title** | Explicating Tacit Regulatory Knowledge from LLMs to Auto-Formalize Requirements for Compliance Test Case Generation |
| **methodology** | Use LLMs to extract and formalize regulatory knowledge for auto-generating compliance test cases. LLM as knowledge source and formalizer; downstream test generation. Not interactive chatbot. |
| **relevance** | 0.65 |
| **relevant_pages** | 1–6 (abstract, regulatory framing, LLM explication, formalization, test generation) |
| **conflict** | LLM used for formalization and knowledge extraction; we use LLM for intent and natural-language interpretation, not for producing formal requirements or test cases. |
| **difference** | One-off formalization and test generation vs. interactive chatbot with intent→function→executor. No stakeholder Q&A loop. |
| **gap** | Tacit regulatory knowledge hard to formalize; LLMs proposed to explicate and support test case generation. |
| **citation** | [Authors], "Explicating Tacit Regulatory Knowledge from LLMs to Auto-Formalize Requirements for Compliance Test Case Generation," submitted for publication. |
| **paperType** | Mixed |
| **authors** | [Extract from paper] |

---

## Paper 9: Knowledge Management for Automobile Failure Analysis Using Graph RAG

| Field | Content |
|-------|--------|
| **title** | Knowledge Management for Automobile Failure Analysis Using Graph RAG |
| **methodology** | Graph RAG: knowledge graph + retrieval over graph for automobile failure analysis. Query over structured failure knowledge; may use LLM for answering. Not an intent→function→executor chatbot. |
| **relevance** | 0.62 |
| **relevant_pages** | 1–4 (abstract, graph construction, RAG over graph, failure analysis use case) |
| **conflict** | Graph-centric retrieval and possibly open-ended LLM answers; we use flat intent→function map and code executor before interpretation. |
| **difference** | Failure-analysis knowledge management vs. general stakeholder Q&A. No explicit rule-based function selector; graph RAG serves as retrieval backend. |
| **gap** | Managing and querying failure knowledge at scale; graph RAG proposed to improve retrieval and reasoning over failures. |
| **citation** | [Authors], "Knowledge Management for Automobile Failure Analysis Using Graph RAG," submitted for publication. |
| **paperType** | Quantitative |
| **authors** | [Extract from paper] |

---

## Paper 10: Secure Multifaceted-RAG for Enterprise: Hybrid Knowledge Retrieval with Security Filtering

| Field | Content |
|-------|--------|
| **title** | Secure Multifaceted-RAG for Enterprise: Hybrid Knowledge Retrieval with Security Filtering |
| **methodology** | SecMulti-RAG: three sources—internal documents, pre-generated expert knowledge for anticipated queries, on-demand external LLM-generated knowledge. Confidentiality-preserving filter so proprietary data is not sent to external LLMs; local open-source generator, selective use of external LLMs when prompts are safe. Evaluated on report generation in automotive; correctness, richness, helpfulness. |
| **relevance** | 0.60 |
| **relevant_pages** | 1–4 (abstract, intro, multi-source retrieval, filtering, evaluation) |
| **conflict** | None; complementary focus on security and retrieval. We could adopt similar filtering in a RAG component if we add one. |
| **difference** | Enterprise RAG security and hybrid retrieval vs. our hybrid architecture (intent + deterministic functions + interpreter). They do not define intent→function→executor. |
| **gap** | Limited retrieval scope and data security risks in enterprise RAG; SecMulti-RAG and filtering proposed for completeness and confidentiality. |
| **citation** | G. Byun, S. Lee, N. Choi, J. D. Choi, "Secure Multifaceted-RAG for Enterprise: Hybrid Knowledge Retrieval with Security Filtering," in Proc. Annu. Meeting Assoc. Comput. Linguist. (ACL), 2024. |
| **paperType** | Quantitative |
| **authors** | [{"name": "Grace Byun", "institution": "Emory University"}, {"name": "Shinsun Lee", "institution": "Emory University / Hyundai Motor Company"}, {"name": "Nayoung Choi", "institution": "Emory University"}, {"name": "Jinho D. Choi", "institution": "Emory University"}] |

---

## Paper 11: Measuring design compliance using neural language models – an automotive case study

| Field | Content |
|-------|--------|
| **title** | Measuring design compliance using neural language models – an automotive case study |
| **methodology** | Neural language models to measure design compliance (e.g. requirements vs. design docs) in automotive. Classification/similarity for compliance checking; not interactive Q&A. |
| **relevance** | 0.58 |
| **relevant_pages** | 1–4 (abstract, compliance task, model setup, case study results) |
| **conflict** | None; compliance checking is a different task from stakeholder chatbot. |
| **difference** | Batch or single-shot compliance assessment vs. our real-time intent→function→execution→response. No user intent or function map. |
| **gap** | Manual compliance checking is costly; NLMs proposed for automated compliance measurement. |
| **citation** | [Authors], "Measuring design compliance using neural language models – an automotive case study," submitted for publication. |
| **paperType** | Quantitative |
| **authors** | [Extract from paper] |

---

## Paper 12: Cleaning Maintenance Logs with LLM Agents for Improved Predictive Maintenance

| Field | Content |
|-------|--------|
| **title** | Cleaning Maintenance Logs with LLM Agents for Improved Predictive Maintenance |
| **methodology** | LLM-based agents to clean and normalize maintenance log text for predictive maintenance. Data preparation, log quality, normalization; focus on unstructured log → structured/clean data for downstream models. Not end-user Q&A or intent→function mapping. |
| **relevance** | 0.55 |
| **relevant_pages** | 1–4 (abstract, intro, method, evaluation) |
| **conflict** | Uses LLMs for data cleaning/transformation; we use LLMs for intent and interpretation only, with deterministic execution. |
| **difference** | Back-office data cleaning pipeline vs. stakeholder-facing query→intent→function→execution→response. No rule-based function selector or code executor in their design. |
| **gap** | Unstructured maintenance logs hinder predictive models; LLM agents proposed to automate cleaning and normalization. |
| **citation** | [Authors], "Cleaning Maintenance Logs with LLM Agents for Improved Predictive Maintenance," submitted for publication. |
| **paperType** | Quantitative |
| **authors** | [Extract from paper] |

---

## Paper 13: Generating Automotive Code: Large Language Models for Software Development and Verification in Safety-Critical Systems

| Field | Content |
|-------|--------|
| **title** | Generating Automotive Code: Large Language Models for Software Development and Verification in Safety-Critical Systems |
| **methodology** | LLMs for generating and verifying automotive code in safety-critical contexts. Code generation, verification, safety assurance; not chatbot or intent classification. |
| **relevance** | 0.50 |
| **relevant_pages** | 1–4 (abstract, code gen, verification, safety discussion) |
| **conflict** | None; different problem (code gen/verification vs. user-facing QA). |
| **difference** | Code generation and verification vs. our query→intent→function→execution→response. Our “code executor” runs predefined business logic, not LLM-generated code. |
| **gap** | Reliability and safety of LLM-generated code; methods for verification and integration in safety-critical workflows. |
| **citation** | [Authors], "Generating Automotive Code: Large Language Models for Software Development and Verification in Safety-Critical Systems," submitted for publication. |
| **paperType** | Quantitative |
| **authors** | [Extract from paper] |

---

## Paper 14: BetterCheck - Towards Safeguarding VLMs for Automotive Perception Systems

| Field | Content |
|-------|--------|
| **title** | BetterCheck: Towards Safeguarding VLMs for Automotive Perception Systems |
| **methodology** | Systematic assessment of 3 state-of-the-art VLMs on traffic situations from Waymo Open Dataset. Adapted SelfCheckGPT for multimodal (image/video) hallucination detection; captioning + self-check to discard captions that overlook traffic agents or hallucinate. Safety guardrails for VLM-supported perception; red-teaming / hallucination detection strategies. |
| **relevance** | 0.35 |
| **relevant_pages** | 1–2 (abstract, intro, RQs); limited overlap with text-based stakeholder chatbot |
| **conflict** | None directly; different modality (vision vs. text QA) and no intent/function/executor design. |
| **difference** | VLMs for perception safety vs. our text-based intent classification and deterministic backend. No RAG for Q&A, no rule-based function selection. |
| **gap** | VLMs prone to hallucination (missing or inventing traffic agents); BetterCheck and hallucination detection strategies proposed for automotive perception. |
| **citation** | M. A. M. Dona, B. Cabrero-Daniel, Y. Yu, C. Berger, "BetterCheck: Towards Safeguarding VLMs for Automotive Perception Systems," in Proc. IEEE Int. Conf. Software Verification and Validation, 2024. |
| **paperType** | Quantitative |
| **authors** | [{"name": "Malsha Ashani Mahawatta Dona", "institution": "University of Gothenburg"}, {"name": "Beatriz Cabrero-Daniel", "institution": "Chalmers University of Technology"}, {"name": "Yinan Yu", "institution": "Chalmers University of Technology"}, {"name": "Christian Berger", "institution": "University of Gothenburg"}] |

---

## Summary Table (Relevance)

| Paper | Title (short) | Relevance |
|-------|----------------|-----------|
| 1 | GateLens (release analytics agent) | 0.80 |
| 2 | GoNoGo (multi-agent release) | 0.78 |
| 3 | Adopting RAG for LLM-Aided Vehicle Design | 0.76 |
| 4 | Safety Requirements + Agent-based RAG | 0.75 |
| 5 | RAG for PDF chatbots (Ollama) | 0.72 |
| 6 | Agentic vs. Direct LLM (software models) | 0.70 |
|------|-------------------Cut-Off----------------------|-----------|
| 7 | LADFA (privacy policy, RAG) | 0.68 |
| 8 | Regulatory knowledge → test cases | 0.65 |
| 9 | Graph RAG for failure analysis | 0.62 |
| 10 | Secure Multifaceted-RAG | 0.60 |
| 11 | Design compliance (NLMs) | 0.58 |
| 12 | Cleaning Maintenance Logs (LLM agents) | 0.55 |
| 13 | Generating automotive code (LLM) | 0.50 |
| 14 | BetterCheck (VLMs, perception) | 0.35 |


*Citations follow: Pre-Print/arXiv; In-Press (to be published); Submitted; Journal; Conference as per project conventions. Where venue was not stated in the excerpt, "submitted for publication" or a generic conference form is used; replace with actual venue when known.*
