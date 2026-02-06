# Literature Review Results – Deepa Papers

**Context:** Stakeholder-facing chatbot on a hybrid LLM–deterministic architecture: structured query → LLM intent identification only → rule-based function selector → code executor → LLM data interpreter → response. Goal: interpretability, predictability, low hallucination.

---

## Paper 1: Enhancing Large Model Document Question Answering through Retrieval Augmentation

| Field | Content |
|-------|--------|
| **title** | Enhancing Large Model Document Question Answering through Retrieval Augmentation |
| **methodology** | DocQA with dual-path retrieval (M3E vector retrieval + BM25 lexical matching) for coarse ranking, then matching-model re-ranking for precision ranking. Knowledge base creation: loading, sentence-based segmentation (≤512 words), vectorization (M3E), FAISS. Manually annotated test set for validation. |
| **relevance** | 0.72 |
| **relevant_pages** | 1–5 (abstract, intro, method, dual-path retrieval, LLM generation, experiment) |
| **conflict** | Pure RAG + LLM generation for answers; no intent classification or rule-based function selector. |
| **difference** | Document QA over retrieved passages vs. our intent→function→executor→interpreter pipeline. They do not separate intent from retrieval or use a static function map. |
| **gap** | Vector-only retrieval limits DocQA; dual-path retrieval and re-ranking proposed to improve relevance and reduce hallucinations. |
| **citation** | J. Zeng, R. Zheng, C. Wang, W. Xue, X. Yu, T. Zhang, "Enhancing Large Model Document Question Answering through Retrieval Augmentation," in Proc. Int. Conf. Artificial Intelligence and Power Systems (AIPS), 2024, pp. 57–62. |
| **paperType** | Quantitative |
| **authors** | [{"name": "Jingwen Zeng", "institution": "State Grid Information & Telecom"}, {"name": "Rongrong Zheng", "institution": "State Grid Information & Telecom"}, {"name": "Chenhui Wang", "institution": "State Grid Information & Telecom"}, {"name": "Wenting Xue", "institution": "State Grid Information & Telecom"}, {"name": "Xiaoyang Yu", "institution": "State Grid Information & Telecom"}, {"name": "Tao Zhang", "institution": "State Grid Sgitg Digital Technology"}] |

---

## Paper 2: A Distributed Search Engine Based on a Re-ranking Algorithm Model

| Field | Content |
|-------|--------|
| **title** | A Distributed Search Engine Based on a Re-ranking Algorithm Model |
| **methodology** | Distributed search engine: Apache Nutch (crawling), Hadoop/HDFS (storage), Solr (Lucene indexing), ZooKeeper (coordination). Re-ranking algorithm using user click logs: P(click\|q,url), P(click\|pos); combines ClickScore and LuceneScore (TF-IDF). Statistical probability, threshold on query frequency. |
| **relevance** | 0.45 |
| **relevant_pages** | 1–5 |
| **conflict** | None; focus is web search and click-based re-ranking, not chatbot or intent. |
| **difference** | General-purpose distributed IR and click-based re-ranking vs. our stakeholder chatbot with intent classification and deterministic execution. |
| **gap** | Lucene scoring ignores user behavior; re-ranking from click logs proposed to better match user intent. |
| **citation** | J. Wan, B. Wang, W. Guo, K. Chen, J. Wang, "A Distributed Search Engine Based on a Re-ranking Algorithm Model," in Proc. 10th Int. Conf. Computer Science and Education (ICCSE), Cambridge, UK, 2015, pp. 64–68. |
| **paperType** | Quantitative |
| **authors** | [{"name": "Jingyong Wan", "institution": "Xiamen University"}, {"name": "Beizhan Wang", "institution": "Xiamen University"}, {"name": "Wei Guo", "institution": "Xiamen University"}, {"name": "Kang Chen", "institution": "Xiamen University"}, {"name": "Jiajun Wang", "institution": "Xiamen University"}] |

---

## Paper 3: A Re-ranking Method Based on Cloud Model

| Field | Content |
|-------|--------|
| **title** | A Re-ranking Method Based on Cloud Model |
| **methodology** | IR re-ranking using cloud model (Expectation Ex, Entropy En, Super-entropy He) to model uncertainty between query and document. Backward cloud generator; relevance as uncertainty degree of document representing query. Evaluated on NTCIR-5 SLIR (Chinese). |
| **relevance** | 0.48 |
| **relevant_pages** | 1–5 |
| **conflict** | None; classical IR re-ranking, no LLM or intent. |
| **difference** | Uncertainty-theoretic re-ranking for IR vs. our hybrid LLM intent + deterministic function selection and execution. |
| **gap** | Traditional Chinese IR rarely models uncertainty; cloud model proposed for re-ranking while preserving recall. |
| **citation** | M. Zhang, Z. Lou, J. Chen, "A Re-ranking Method Based on Cloud Model," in Proc. Int. Conf. Computer Science and Network Technology (ICCSNT), Harbin, China, 2011, pp. 142–146. |
| **paperType** | Quantitative |
| **authors** | [{"name": "Maoyuan Zhang", "institution": "Central China Normal University"}, {"name": "Zhenxia Lou", "institution": "Central China Normal University"}, {"name": "Jinguang Chen", "institution": "Central China Normal University"}] |

---

## Paper 4: Enhancing Retrieval and Re-ranking in RAG: A Case Study on Tax Law

| Field | Content |
|-------|--------|
| **title** | Enhancing Retrieval and Re-ranking in RAG: A Case Study on Tax Law |
| **methodology** | RAG for Azerbaijani Tax Code: sparse retrievers (BM25, SPLADE), dense embeddings (BGE-m3, text-embedding-3-large, all-MiniLM-L6-v2), hybrid retrieval (BM25 + BGE-m3), cross-encoder re-ranking (bge-reranker-base). Metrics: recall@100, NDCG. |
| **relevance** | 0.78 |
| **relevant_pages** | 1–7 |
| **conflict** | RAG drives retrieval and generation; we use LLM only for intent and interpretation, with deterministic execution in between. |
| **difference** | Layered hybrid retrieval + re-ranking for legal QA vs. our intent→function map and code executor. No explicit intent classification or function selector. |
| **gap** | Single retriever recall limits RAG; hybrid retrieval and re-ranking proposed for regulation-heavy domains. |
| **citation** | Z. Rustamov, M. Gasimzade, S. Rustamov, "Enhancing Retrieval and Re-ranking in RAG: A Case Study on Tax Law," in Proc. IEEE Int. Conf. Communications and Information Technologies Applications, 2022. |
| **paperType** | Quantitative |
| **authors** | [{"name": "Zaid Rustamov", "institution": "MegaSec LLC"}, {"name": "Mehdi Gasimzade", "institution": "MegaSec LLC"}, {"name": "Samir Rustamov", "institution": "ADA University"}] |

---

## Paper 5: The Research on Re-ranking Algorithm for FAQ-based Systems in the Petroleum Domain

| Field | Content |
|-------|--------|
| **title** | The Research on Re-ranking Algorithm for FAQ-based Systems in the Petroleum Domain |
| **methodology** | Dense retrieval (DPR, BAAI/bge-m3, XLM-RoBERTa) for initial recall; re-ranking with BAAI/bge-reranker. Contrastive learning, LoRA fine-tuning with domain petroleum data. Multi-stage retrieval, semantic matching. |
| **relevance** | 0.70 |
| **relevant_pages** | 1–6 |
| **conflict** | FAQ retrieval + re-ranking for QA; we add intent classification and rule-based function selection before execution. |
| **difference** | Vertical-domain FAQ QA with DPR + reranker vs. our generic intent→function→executor→interpreter pipeline. |
| **gap** | Professional terminology and semantic matching in oil-industry FAQ; re-ranking and domain fine-tuning proposed. |
| **citation** | J. Zhang, J. Han, "The Research on Re-ranking Algorithm for FAQ-based Systems in the Petroleum Domain," in Proc. 10th Int. Conf. Intelligent Computing and Signal Processing (ICSP), 2025, pp. 108–113. |
| **paperType** | Quantitative |
| **authors** | [{"name": "Jiaxiang Zhang", "institution": "Xi'an Shiyou University"}, {"name": "Jiaxin Han", "institution": "Xi'an Shiyou University"}] |

---

## Paper 6: A Sentence-Level Semantic Annotated Corpus Based on HNC Theory

| Field | Content |
|-------|--------|
| **title** | A Sentence-Level Semantic Annotated Corpus Based on HNC Theory |
| **methodology** | HNC (Hierarchical Network of Concepts) semantic annotation: sentence category, semantic chunks, sub-sentence. XML markup; 57 basic sentence categories; corpus of 395 articles, ~1M characters (People's Daily). Top-down annotation (discourse → sentences → chunks → words). |
| **relevance** | 0.42 |
| **relevant_pages** | 1–4 |
| **conflict** | None; resource-building for Chinese semantics, not dialogue or intent. |
| **difference** | Semantic corpus and chunk structure for NLP vs. our dialogue architecture (intent, function map, executor, interpreter). |
| **gap** | Lack of sentence-level semantic resources for Chinese; HNC-based corpus proposed for language study and IR. |
| **citation** | Z. Liu, Y. Jin, C. Miao, "A Sentence-Level Semantic Annotated Corpus Based on HNC Theory," in Proc. Int. Conf. Asian Language Processing (IALP), 2011, pp. 5–8. |
| **paperType** | Qualitative / resource |
| **authors** | [{"name": "Zhiying Liu", "institution": "Beijing Normal University"}, {"name": "Yaohong Jin", "institution": "Beijing Normal University"}, {"name": "Chuanjiang Miao", "institution": "Hong Kong Polytechnic University"}] |

---

## Paper 7: Comparison of Chunking Techniques Across Diverse Document Types in NLP Retrieval Tasks

| Field | Content |
|-------|--------|
| **title** | Comparison of Chunking Techniques Across Diverse Document Types in NLP Retrieval Tasks |
| **methodology** | Comparison of fixed-size (with overlap), sentence-based, recursive, and semantic-similarity chunking for retrieval. Metrics: Precision, Recall, MRR, NDCG, ss2fd, SRGT, retrieval token cost, QCS, chunking time. Sentence-BERT embeddings, Faiss; PDF + QA pairs. |
| **relevance** | 0.68 |
| **relevant_pages** | 1–6 |
| **conflict** | None; preprocessing for retrieval, complementary to our pipeline. |
| **difference** | Chunking for RAG/retrieval vs. our intent classification and function execution. Chunking could support a RAG component if we add one. |
| **gap** | Limited empirical comparison of chunking strategies for retrieval; study provides task-specific guidelines. |
| **citation** | S. Jaiswal, P. Bisht, K. Kansara, M. S. Shankar Datta, "Comparison of Chunking Techniques Across Diverse Document Types in NLP Retrieval Tasks," in Proc. IEEE Int. Conf. Explainable AI and Generative AI, 2024. |
| **paperType** | Quantitative |
| **authors** | [{"name": "Shruti Jaiswal", "institution": "Bosch Global Software Technologies"}, {"name": "Priyank Bisht", "institution": "Bosch Global Software Technologies"}, {"name": "Krity Kansara", "institution": "Bosch Global Software Technologies"}, {"name": "Shankar Datta", "institution": "Bosch Global Software Technologies"}] |

---

## Paper 8: Enhancing LLM Function Calling with Structured Outputs

| Field | Content |
|-------|--------|
| **title** | Enhancing LLM Function Calling with Structured Outputs |
| **methodology** | Constrained Generation (CG): grammar-based decoding (xgrammar) to enforce JSON/function-call format during generation; JSON schema → generative automaton, vocabulary masking. Compared to Post-Parsing (PP) on Hermes-Function-Calling-v1; Llama-3.3-70B, Qwen3-30B. |
| **relevance** | 0.82 |
| **relevant_pages** | 1–5 |
| **conflict** | LLM both chooses and formats function calls; we use LLM only for intent and a rule-based function selector. |
| **difference** | Reliable LLM-generated function calls (format compliance) vs. our deterministic intent→function map and code executor. Their approach keeps “which function” in the LLM. |
| **gap** | Prompt-based function calling leads to parsing errors; structured outputs (e.g. xgrammar) proposed for compliance. |
| **citation** | K. Sejourné, A. Lata, "Enhancing LLM Function Calling with Structured Outputs," in Proc. 2nd Int. Generative AI and Computational Language Modelling Conf. (GenAI/CLM), 2025, pp. 171–176. |
| **paperType** | Quantitative |
| **authors** | [{"name": "Kevin Sejourné", "institution": "Cloud Temple"}, {"name": "Alexandru Lata", "institution": "Cloud Temple"}] |

---

## Paper 9: Simple Action Model: Enabling LLM to Sequential Function Calling Tool Chain

| Field | Content |
|-------|--------|
| **title** | Simple Action Model: Enabling LLM to Sequential Function Calling Tool Chain |
| **methodology** | OpenAPI schema → type definitions (OpenAPI-TS, OpenAPI-Zod); LLM receives user prompt + schema, outputs JSON; custom JSON parser + OpenAPI-Fetch; Action Engine executes and chains functions. Single LLM call for “what to do”; no fine-tuning required, in-context learning. |
| **relevance** | 0.80 |
| **relevant_pages** | 1–6 |
| **conflict** | LLM decides which functions to call and in what order; we use a static intent→function map and deterministic execution. |
| **difference** | LLM-driven tool chain (one request → multiple sequential calls) vs. our intent classifier + rule-based selector + code executor. |
| **gap** | Complex function calling and chaining; simple action model with OpenAPI and single LLM call proposed. |
| **citation** | R. S. Sen, A. K. Prithviraj, S. P. Jose, N. Joseph, R. Thomas, "Simple Action Model: Enabling LLM to Sequential Function Calling Tool Chain," in Proc. Int. Conf. Advancement in Renewable Energy and Intelligent Systems (AREIS), 2024. |
| **paperType** | Quantitative |
| **authors** | [{"name": "Rajat Sandeep Sen", "institution": "SJCET Palai"}, {"name": "Amalkrishna M", "institution": "SJCET Palai"}, {"name": "Sharon Prashant Jose", "institution": "SJCET Palai"}, {"name": "Neena Joseph", "institution": "SJCET Palai"}, {"name": "Renjith Thomas", "institution": "SJCET Palai"}] |

---

## Paper 10: The Splitting and Matching Algorithm of Dynamic Path Oriented the Function Calling Relationship

| Field | Content |
|-------|--------|
| **title** | The Splitting and Matching Algorithm of Dynamic Path Oriented the Function Calling Relationship |
| **methodology** | White-box testing: path coverage by function-call relationship. Instrumentation for entry/exit/branch pile points; dynamic path from execution; splitting algorithm to decompose into static-path subsets; matching against global static path set; coverage rate. Not NLP or LLM. |
| **relevance** | 0.25 |
| **relevant_pages** | 1–4 |
| **conflict** | None; software testing, unrelated to chatbot or intent. |
| **difference** | Function-call paths for test coverage vs. our “function” as backend API/routine selected by intent. Different meaning of “function.” |
| **gap** | Full path coverage infeasible; function-call-level path coverage proposed for adequacy. |
| **citation** | Y. Mu, H. Li, B. Jiang, X. Liu, M. Wu, "The Splitting and Matching Algorithm of Dynamic Path Oriented the Function Calling Relationship," in Proc. 5th Int. Conf. Intelligent Human-Machine Systems and Cybernetics, 2013, pp. 34–38. |
| **paperType** | Quantitative |
| **authors** | [{"name": "Yongmin Mu", "institution": "Beijing Information Science & Technology University"}, {"name": "Huili Li", "institution": "Beijing Information Science & Technology University"}, {"name": "Bing Jiang", "institution": "Beijing Information Science & Technology University"}, {"name": "Xuefei Liu", "institution": "Beijing Information Science & Technology University"}, {"name": "Miao Wu", "institution": "Beijing Information Science & Technology University"}] |

---

## Paper 11: A New Data Augmentation Method for Intent Classification Enhancement and its Application on Spoken Conversation Datasets

| Field | Content |
|-------|--------|
| **title** | A New Data Augmentation Method for Intent Classification Enhancement and its Application on Spoken Conversation Datasets |
| **methodology** | NNSI (Nearest Neighbors Scores Improvement): ambiguity measure Δ = s_(M) − s_(M−1); high-ambiguity samples labeled by averaging classifier scores over k nearest neighbors (labeled + unlabeled); add to training set. Weakly supervised; applied to two voice conversation systems; up to ~10% error reduction. |
| **relevance** | 0.85 |
| **relevant_pages** | 1–4 |
| **conflict** | None; improves intent classifier training, aligns with using intent classification. |
| **difference** | Data augmentation and labeling for intent classifiers vs. our architecture design. Complementary: we could use NNSI to improve our intent classifier data. |
| **gap** | Lack of real-world training data for intent classifiers; NNSI for automatic selection and labeling of ambiguous samples proposed. |
| **citation** | Z. Kons, A. Satt, H.-K. Kuo, S. Thomas, B. Carmeli, R. Ho, B. Kingsbury, "A New Data Augmentation Method for Intent Classification Enhancement and its Application on Spoken Conversation Datasets," in Proc. IEEE Int. Conf. Acoustics, Speech and Signal Processing (ICASSP), 2022, pp. 763–767. |
| **paperType** | Quantitative |
| **authors** | [{"name": "Zvi Kons", "institution": "IBM Research"}, {"name": "Aharon Satt", "institution": "IBM Research"}, {"name": "Hong-Kwang Kuo", "institution": "IBM Research"}, {"name": "Samuel Thomas", "institution": "IBM Research"}, {"name": "Boaz Carmeli", "institution": "IBM Research"}, {"name": "Ron Ho", "institution": "IBM Research"}, {"name": "Brian Kingsbury", "institution": "IBM Research"}] |

---

## Paper 12: Comparative Analysis of Intent Classification in Indonesian Chatbots Using BERT and RoBERTa Models

| Field | Content |
|-------|--------|
| **title** | Comparative Analysis of Intent Classification in Indonesian Chatbots Using BERT and RoBERTa Models |
| **methodology** | Intent classification for chatbot: BERT vs. RoBERTa on University Chatbot Dataset (38 intents, 405 patterns); translated to Bahasa Indonesia (DeepL). Accuracy, F1, precision, recall. BERT 0.89, RoBERTa 0.84. |
| **relevance** | 0.88 |
| **relevant_pages** | 1–6 |
| **conflict** | None; directly addresses intent classification for chatbots. |
| **difference** | Model choice (BERT vs. RoBERTa) for intent only vs. our full pipeline (intent → function selector → executor → interpreter). Same intent step, different downstream. |
| **gap** | Need for effective intent classification in non-English chatbots; transformer comparison for Indonesian. |
| **citation** | A. Abdiansah, M. Fachrurrozi, A. Dwiyono, "Comparative Analysis of Intent Classification in Indonesian Chatbots Using BERT and RoBERTa Models," in Proc. Int. Conf. Computing and Information (CICI), 2022. |
| **paperType** | Quantitative |
| **authors** | [{"name": "Abdiansah Abdiansah", "institution": "Sriwijaya University"}, {"name": "Muhammad Fachrurrozi", "institution": "Sriwijaya University"}, {"name": "Aswin Dwiyono", "institution": "Sriwijaya University"}] |

---

## Paper 13: Comparison Of Multinomial Naive Bayes Algorithm And Logistic Regression For Intent Classification In Chatbot

| Field | Content |
|-------|--------|
| **title** | Comparison Of Multinomial Naive Bayes Algorithm And Logistic Regression For Intent Classification In Chatbot |
| **methodology** | Intent classification for community-reporting chatbot: Multinomial Naive Bayes vs. Logistic Regression; TF-IDF features; classes: greet, report, info, point, trade-point, thanks. Evaluation: accuracy, precision, recall (confusion matrix). Logistic Regression outperformed Naive Bayes. |
| **relevance** | 0.82 |
| **relevant_pages** | 1–5 |
| **conflict** | None; classical ML for intent, compatible with our intent step. |
| **difference** | Traditional ML (NB, LR) for intent vs. our LLM-based intent; we could use similar evaluation or fallback. |
| **gap** | Need for practical intent classification in domain chatbots; comparison of NB vs. LR for small labeled sets. |
| **citation** | M. Y. Helmi Setyawan, R. Maula, A. Awangga, S. R. Efendi, "Comparison Of Multinomial Naive Bayes Algorithm And Logistic Regression For Intent Classification In Chatbot," in Proc. IEEE Conf., 2018. |
| **paperType** | Quantitative |
| **authors** | [{"name": "Muhammad Yusril Helmi Setyawan", "institution": "Politeknik Pos Indonesia"}, {"name": "Rolly Maulana", "institution": "Politeknik Pos Indonesia"}, {"name": "Awangga Safif", "institution": "Politeknik Pos Indonesia"}, {"name": "Rafi Efendi", "institution": "Politeknik Pos Indonesia"}] |

---

## Paper 14: Integrating Model-Agnostic Meta-Learning with Advanced Language Embeddings for Few-Shot Intent Classification

| Field | Content |
|-------|--------|
| **title** | Integrating Model-Agnostic Meta-Learning with Advanced Language Embeddings for Few-Shot Intent Classification |
| **methodology** | MAML + embeddings (BERT, LaBSE, text-embedding-ada-002) for few-shot intent classification. CLINC150; N-way K-shot; MLP on top of embeddings. text-embedding-ada-002 best (e.g. 97.07% 5-way 1-shot, 99.1% 5-way 5-shot). Outer/inner loop optimization. |
| **relevance** | 0.85 |
| **relevant_pages** | 1–5 |
| **conflict** | None; improves intent classification with few examples. |
| **difference** | Few-shot intent learning (MAML + embeddings) vs. our pipeline design. Complementary for low-data intent setup. |
| **gap** | Dependency on large labeled data for intent; MAML + modern embeddings proposed for few-shot intent. |
| **citation** | A. Rahimi, H. Veisi, "Integrating Model-Agnostic Meta-Learning with Advanced Language Embeddings for Few-Shot Intent Classification," in Proc. 32nd Int. Conf. Electrical Engineering (ICEE), 2024. |
| **paperType** | Quantitative |
| **authors** | [{"name": "Ali Rahimi", "institution": "University of Tehran"}, {"name": "Hadi Veisi", "institution": "University of Tehran"}] |

---

## Paper 15: Intent Classification: French Recruitment Chatbot Use Case

| Field | Content |
|-------|--------|
| **title** | Intent Classification: French Recruitment Chatbot Use Case |
| **methodology** | Comparison of DIETClassifier (Rasa), Wit.ai, and CamemBERT for intent classification on French recruitment chatbot. Custom dataset: 22 intents, 2,547 examples. CamemBERT best (93%), then Wit.ai (88%), DIET (86%). Accuracy, precision, recall, F1, confusion matrix. |
| **relevance** | 0.88 |
| **relevant_pages** | 1–5 |
| **conflict** | None; intent classification for task-oriented chatbot. |
| **difference** | Framework/model comparison for intent in one language vs. our full hybrid architecture. Same intent goal, we add deterministic function selection and execution. |
| **gap** | Lack of comparison of intent classifiers for French recruitment chatbots; CamemBERT recommended. |
| **citation** | N. Boudjani, V. Colas, A. Fotouhi, "Intent Classification: French Recruitment Chatbot Use Case," in Proc. Int. Conf. Computational Science and Computational Intelligence (CSCI), 2023, pp. 68–73. |
| **paperType** | Quantitative |
| **authors** | [{"name": "Nadira Boudjani", "institution": "SogetiLabs"}, {"name": "Vivian Colas", "institution": "SogetiLabs"}, {"name": "Azade Fotouhi", "institution": "SogetiLabs"}] |

---

## Paper 16: Fine-tuned BERT with Bi-GRU-CapsNet for Intent Prediction (intent_prediction.pdf)

| Field | Content |
|-------|--------|
| **title** | Fine-tuned BERT with Bi-GRU-CapsNet for Intent Prediction |
| **methodology** | Intent prediction using BERT encoder + Bi-GRU + CapsNet. BERT for contextual representations, Bi-GRU for sequence modeling, CapsNet for classification. Fine-tuning on intent datasets. |
| **relevance** | 0.80 |
| **relevant_pages** | 1–6 |
| **conflict** | None; intent prediction model design. |
| **difference** | BERT+Bi-GRU+CapsNet for intent vs. our use of an LLM for intent and separate function selector; complementary model option. |
| **gap** | Improving intent prediction accuracy; hybrid BERT–Bi-GRU–CapsNet proposed. |
| **citation** | N. Shafi et al., "Fine-tuned BERT with Bi-GRU-CapsNet for Intent Prediction," in Proc. Int. Conf. Advancement in Computing Technologies and Applications, 2023. |
| **paperType** | Quantitative |
| **authors** | [{"name": "Nahida Shafi", "institution": "Department of Computer Science"}] |

---

## Paper 17: Leveraging BERT for Next-Generation Spoken Language Understanding with Joint Intent Classification and Slot Filling

| Field | Content |
|-------|--------|
| **title** | Leveraging BERT for Next-Generation Spoken Language Understanding with Joint Intent Classification and Slot Filling |
| **methodology** | Joint intent classification and slot filling: BERT encoder, intent2slot (intent probability broadcast to sequence for slot labels), slot2intent (slot distributions for intent). Bi-directional NLU; joint loss. Evaluated on ATIS, SNIPS. |
| **relevance** | 0.90 |
| **relevant_pages** | 1–5 |
| **conflict** | Slot filling and intent jointly in one model; we only use intent and then deterministic function/inputs. |
| **difference** | SLU with intent + slots (task-oriented dialogue) vs. our intent only then rule-based function selector. We could use similar joint model and then map intent+slots to functions. |
| **gap** | Error propagation in separate intent/slot models; joint BERT-based intent and slot filling proposed. |
| **citation** | S. Gore, D. Jadhav, M. E. Ingale, S. Gore, U. Nanavare, "Leveraging BERT for Next-Generation Spoken Language Understanding with Joint Intent Classification and Slot Filling," in Proc. Int. Conf. Advanced Computing Technologies and Applications (ICACTA), 2023. |
| **paperType** | Quantitative |
| **authors** | [{"name": "Santosh Gore", "institution": "Sai Info Solution"}, {"name": "Devani Jadhav", "institution": "Sanjivani College of Engineering"}, {"name": "Mayur Eknath Ingale", "institution": "Sandip Institute of Technology"}, {"name": "Sujata Gore", "institution": "Sai Info Solution"}, {"name": "Umesh Nanavare", "institution": "MIT ADT University"}] |

---

## Paper 18: Logistic Regression-Based Example Selection for Enhanced Few-Shot Learning in Intent Classification

| Field | Content |
|-------|--------|
| **title** | Logistic Regression-Based Example Selection for Enhanced Few-Shot Learning in Intent Classification |
| **methodology** | Few-shot intent classification with LLM: initial k examples by retriever (all-mpnet-base-v2), embed; train logistic regression on (X, y); transform embedding space by W; recompute similarity in transformed space; top-20 examples for prompt. Llama 2 7B; BANKING77, CLINC150, HWU64; 5-shot, 10-shot. |
| **relevance** | 0.82 |
| **relevant_pages** | 1–4 |
| **conflict** | None; improves example selection for intent classification with LLMs. |
| **difference** | Example selection for in-context intent classification vs. our architecture; we could use this for our intent LLM. |
| **gap** | Simple similarity retrieval fails for semantically similar intents; logistic regression-based embedding transformation proposed. |
| **citation** | G. Park, H. Lee, "Logistic Regression-Based Example Selection for Enhanced Few-Shot Learning in Intent Classification," in Proc. IEEE Int. Conf. Consumer Electronics (ICCE), 2025. |
| **paperType** | Quantitative |
| **authors** | [{"name": "Gyutae Park", "institution": "Chung-Ang University"}, {"name": "Hwanhee Lee", "institution": "Chung-Ang University"}] |

---

## Paper 19: Enhancing Public Access to Legal Knowledge in India: A Legal Chatbot Using Legal BERT, GPT-2, and Retrieval-Augmented Generation (RAG)

| Field | Content |
|-------|--------|
| **title** | Enhancing Public Access to Legal Knowledge in India: A Legal Chatbot Using Legal BERT, GPT-2, and Retrieval-Augmented Generation (RAG) |
| **methodology** | Legal chatbot: Legal BERT (query understanding, fine-tuned on Indian legal corpus), RAG (retrieve statutes/case law), GPT-2 (generate response). Pipeline: query → Legal BERT → RAG retrieval → GPT-2 generation. 94.6% accuracy reported; real-time deployment. |
| **relevance** | 0.75 |
| **relevant_pages** | 1–6 |
| **conflict** | RAG + generator LLM for end-to-end answers; we use intent → deterministic execution → interpreter LLM. |
| **difference** | Domain QA (legal) with BERT + RAG + GPT-2 vs. our intent→function→executor→interpreter. No intent classification or function map. |
| **gap** | Access to and comprehension of Indian legal information; Legal BERT + RAG + GPT-2 proposed. |
| **citation** | A. Garlapati, H. Koutharapu, N. Doddi, "Enhancing Public Access to Legal Knowledge in India: A Legal Chatbot Using Legal BERT, GPT-2, and Retrieval-Augmented Generation (RAG)," in Proc. IEEE Int. Conf. Engineering and Technology, 2022. |
| **paperType** | Quantitative |
| **authors** | [{"name": "Abhinav Garlapati", "institution": "Velagapudi Ramakrishna Siddhartha Engineering College"}, {"name": "Hemanth Koutharapu", "institution": "Velagapudi Ramakrishna Siddhartha Engineering College"}, {"name": "Neha Doddi", "institution": "Velagapudi Ramakrishna Siddhartha Engineering College"}] |

---

## Paper 20: Integrating Retrieval-Augmented Generation and Large Language Models for Financial Question Answering

| Field | Content |
|-------|--------|
| **title** | Integrating Retrieval-Augmented Generation and Large Language Models for Financial Question Answering |
| **methodology** | RAG for financial QA: BM25, embedding (multilingual-e5-large), reranker (bge-reranker-v2-m3); hybrid BM25 + reranker; Recursive Token Chunker. Llama3-TAIDE for generation. AI CUP 2024 dataset (FAQ, Financial Statements, Insurance). Best: BM25 + Reranker + chunker, accuracy 0.92. |
| **relevance** | 0.75 |
| **relevant_pages** | 1–3 |
| **conflict** | RAG + LLM generation for answers; we separate intent, execution, and interpretation. |
| **difference** | Financial QA with RAG + LLM vs. our intent→function→executor→interpreter. No intent classification or code executor. |
| **gap** | Rule-based chatbots and LLM hallucination in financial QA; RAG + chunking + reranker proposed. |
| **citation** | Y.-J. Chen, Y.-C. Chu, W.-C. Wang, P.-H. Chen, C.-M. Yang, T.-C. Tung, Y.-C. Chou, S.-W. Du, C.-S. Fuh, "Integrating Retrieval-Augmented Generation and Large Language Models for Financial Question Answering," in Proc. Int. Conf. Intelligent Informatics and Biomedical Sciences (ICIIBMS), Okinawa, Japan, 2025, pp. 9–11. |
| **paperType** | Quantitative |
| **authors** | [{"name": "Yu-Jen Chen", "institution": "National Taiwan University"}, {"name": "Yu-Chin Chu", "institution": "National Taiwan University"}, {"name": "Wei-Chien Wang", "institution": "National Taiwan University"}, {"name": "Ping-Han Chen", "institution": "Chunghwa Telecom / National Cheng Kung University"}, {"name": "Chung-Ming Yang", "institution": "Chunghwa Telecom"}, {"name": "Tzu-Chia Tung", "institution": "National Changhua University of Education"}, {"name": "Yung-Chien Chou", "institution": "National Changhua University of Education"}, {"name": "Sian-Wun Du", "institution": "National Taiwan University"}, {"name": "Chiou-Shann Fuh", "institution": "National Taiwan University"}] |

---

## Paper 21: RAGRouter: Learning to Route Queries to Multiple Retrieval-Augmented Language Models

| Field | Content |
|-------|--------|
| **title** | RAGRouter: Learning to Route Queries to Multiple Retrieval-Augmented Language Models |
| **methodology** | Query routing to one of multiple RAG-augmented LLMs. Document encoder + RAG-capability embedding per LLM; contrastive learning (answerable vs. unanswerable with/without RAG). Models knowledge shift when documents are injected. Preprint; open and closed-source LLMs, local and online retrieval. |
| **relevance** | 0.72 |
| **relevant_pages** | 1–22 |
| **conflict** | Routing chooses which LLM answers; we route intent to deterministic functions, not between LLMs. |
| **difference** | Multi-model RAG routing vs. our single intent LLM + rule-based function selection. Different notion of “routing.” |
| **gap** | Static parametric knowledge ignores RAG-induced capability shift; RAGRouter models document–query–model interaction for routing. |
| **citation** | J. Zhang, X. Liu, Y. Hu, C. Niu, F. Wu, G. Chen, "RAGRouter: Learning to Route Queries to Multiple Retrieval-Augmented Language Models," arXiv, vol. abs/2503.02502, 2025. |
| **paperType** | Quantitative |
| **authors** | [{"name": "Jiarui Zhang", "institution": "Shanghai Jiao Tong University"}, {"name": "Xiangyu Liu", "institution": "Shanghai Jiao Tong University"}, {"name": "Yong Hu", "institution": "Shanghai Jiao Tong University"}, {"name": "Chaoyue Niu", "institution": "Shanghai Jiao Tong University"}, {"name": "Fan Wu", "institution": "Shanghai Jiao Tong University"}, {"name": "Guihai Chen", "institution": "Shanghai Jiao Tong University"}] |

---

## Paper 22: Retrieval-Augmented Generation (RAG) and LLM Integration

| Field | Content |
|-------|--------|
| **title** | Retrieval-Augmented Generation (RAG) and LLM Integration |
| **methodology** | Survey/overview: RAG integrates IR with LLMs for dynamic knowledge; retrieval → augmentation → generation. Discussion of static vs. dynamic data, IR (TF-IDF, VSM, dense retrieval), RAG for QA and chatbots. References Lewis et al. 2020, FiD, RePAQ, Sentence-BERT, ColBERT. |
| **relevance** | 0.70 |
| **relevant_pages** | 1–5 |
| **conflict** | None; RAG overview, we can use RAG as a component. |
| **difference** | General RAG + LLM integration vs. our hybrid with intent and deterministic execution; RAG could support retrieval before or after intent. |
| **gap** | LLMs’ static knowledge and outdated data; RAG proposed for real-time external information. |
| **citation** | B. Tural, Z. Örpek, Z. Destan, "Retrieval-Augmented Generation (RAG) and LLM Integration," in Proc. IEEE Int. Conf. Systems and Applications, 2024. |
| **paperType** | Qualitative / survey |
| **authors** | [{"name": "Büşra Tural", "institution": "Vakıf Research & Development Center"}, {"name": "Zeynep Örpek", "institution": "Vakıf Research & Development Center"}, {"name": "Zeynep Destan", "institution": "Vakıf Research & Development Center"}] |

---

## Paper 24: Retrieval Augmented Generation (RAG) using LLMs

| Field | Content |
|-------|--------|
| **title** | Retrieval Augmented Generation (RAG) using LLMs |
| **methodology** | RAG pipeline: retrieval (external sources) → augmentation (merge with prompt) → generation (LLM). Comparison of Llama, Mistral, Falcon, T5 with and without RAG. Metrics: accuracy, contextual understanding, domain relevance. Addresses hallucination and outdated knowledge. |
| **relevance** | 0.72 |
| **relevant_pages** | 1–5 |
| **conflict** | None; RAG as enhancement to LLMs. |
| **difference** | Generic RAG + multi-LLM comparison vs. our intent→function→executor→interpreter; RAG could feed our interpreter or a retrieval step. |
| **gap** | Hallucinations and outdated knowledge in LLMs; RAG proposed to improve reliability of generated content. |
| **citation** | M. Vahaj, S. M. Raza, V. Nehra, "Retrieval Augmented Generation (RAG) using LLMs," in Proc. Annual Int. Conf. Data Science, Machine Learning and Blockchain Technology (AICDMB), 2025. |
| **paperType** | Quantitative |
| **authors** | [{"name": "Madiha Vahaj", "institution": "Amity School of Engineering and Technology"}, {"name": "Syed Mehran Raza", "institution": "Amity School of Engineering and Technology"}, {"name": "Vibha Nehra", "institution": "Amity School of Engineering and Technology"}] |

---

## Summary Table (Relevance)

| # | Title (short) | Relevance |
|---|----------------|-----------|
| 1 | DocQA through Retrieval Augmentation (dual-path, re-ranking) | 0.72 |
| 2 | Distributed Search Engine, Re-ranking (click logs) | 0.45 |
| 3 | Re-ranking Based on Cloud Model | 0.48 |
| 4 | RAG Retrieval and Re-ranking (Tax Law) | 0.78 |
| 5 | Re-ranking for FAQ (Petroleum) | 0.70 |
| 6 | HNC Sentence-Level Semantic Corpus | 0.42 |
| 7 | Chunking Techniques for NLP Retrieval | 0.68 |
| 8 | LLM Function Calling with Structured Outputs | 0.82 |
| 9 | Simple Action Model, Sequential Function Calling | 0.80 |
| 10 | Splitting/Matching Algorithm, Function Calling (testing) | 0.25 |
| 11 | NNSI for Intent Classification (spoken) | 0.85 |
| 12 | BERT vs. RoBERTa Intent (Indonesian Chatbot) | 0.88 |
| 13 | Naive Bayes vs. Logistic Regression Intent | 0.82 |
| 14 | MAML + Embeddings Few-Shot Intent | 0.85 |
| 15 | Intent Classification French Recruitment Chatbot | 0.88 |
| 16 | BERT Bi-GRU-CapsNet Intent Prediction | 0.80 |
| 17 | BERT Joint Intent and Slot Filling (SLU) | 0.90 |
| 18 | Logistic Regression Example Selection Few-Shot Intent | 0.82 |
| 19 | Legal BERT, GPT-2, RAG Legal Chatbot India | 0.75 |
| 20 | Integrating RAG and LLM Financial QA | 0.75 |
| 21 | RAGRouter: Route to Multiple RAG-LLMs | 0.72 |
| 22 | RAG and LLM Integration (overview) | 0.70 |
| 23 | RAG using LLMs (Llama, Mistral, Falcon, T5) | 0.72 |
