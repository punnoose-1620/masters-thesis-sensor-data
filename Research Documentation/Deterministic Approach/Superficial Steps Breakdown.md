# Deterministic AI Approach – Model Breakdown (High-Level)

This document provides a **step-by-step, model-level breakdown** of the deterministic AI system for supporting natural language access to vehicle data. The descriptions are **intentionally superficial and model-agnostic at implementation level**, focusing on *what* is built and *why*, not *how*.

The document assumes all required datasets are available in a local `datasets/` directory.

---

## Step 1: User Intent Classification Model

* **What ML/AI model would be best for this**
  Multinomial Logistic Regression, Support Vector Machine (SVM), or DistilBERT (fine-tuned classifier)

* **Brief reason for selecting this model**
  These models are well-established for intent classification tasks, offer predictable behavior, and can be tuned for high precision in constrained domains.

* **What this model does**
  Classifies a user’s natural language query into a predefined intent such as data availability, summary request, anomaly check, or comparison.

* **Input data format**
  Plain text query string

* **Output data format**
  Single categorical label representing the detected intent

* **Starting hyperparameter for this model**
  Regularization strength (e.g., C = 1.0)

* **Evaluation metrics for this step**
  Accuracy, Precision, Recall, F1-score

* **Why these evaluation metrics were selected**
  Intent misclassification directly impacts system correctness; precision and recall are critical to avoid incorrect function execution.

* **Target performance values for these metrics**
  F1-score ≥ 0.85

* **Limitations for reaching this performance**
  Ambiguous queries, overlapping intents, and limited labeled training data

---

## Step 2: Slot / Entity Extraction Model

* **What ML/AI model would be best for this**
  Conditional Random Fields (CRF), spaCy NER pipeline, or rule-based entity extraction

* **Brief reason for selecting this model**
  CRF and NER-based models are effective for structured entity extraction, while rules provide full transparency for domain-specific entities.

* **What this model does**
  Extracts structured parameters such as vehicle ID, sensor name, time range, and aggregation type from user queries.

* **Input data format**
  Tokenized text with optional linguistic features

* **Output data format**
  Key–value pairs representing extracted slots

* **Starting hyperparameter for this model**
  L2 regularization coefficient

* **Evaluation metrics for this step**
  Entity-level Precision, Recall, F1-score

* **Why these evaluation metrics were selected**
  Partial extraction errors can lead to invalid queries or misleading results.

* **Target performance values for these metrics**
  Entity F1-score ≥ 0.80

* **Limitations for reaching this performance**
  Inconsistent naming conventions and complex time expressions

---

## Step 3: Query Validation & Normalization Model

* **What ML/AI model would be best for this**
  Rule-based validation engine or decision tree classifier

* **Brief reason for selecting this model**
  Validation logic must be deterministic, explainable, and aligned with data governance rules.

* **What this model does**
  Validates extracted slots against known sensor metadata and normalizes values to canonical forms.

* **Input data format**
  Structured intent and slot dictionary

* **Output data format**
  Validated and normalized query object

* **Starting hyperparameter for this model**
  Decision confidence threshold (if ML-based)

* **Evaluation metrics for this step**
  Validation success rate, false rejection rate

* **Why these evaluation metrics were selected**
  Ensures correct rejection of invalid queries while minimizing unnecessary failures.

* **Target performance values for these metrics**
  Validation success rate ≥ 95%

* **Limitations for reaching this performance**
  Incomplete metadata catalogs and evolving sensor definitions

---

## Step 4: Data Availability Inference Model

* **What ML/AI model would be best for this**
  Statistical analysis engine or rule-based availability checker

* **Brief reason for selecting this model**
  Data availability is best derived from metadata and timestamps rather than learned models.

* **What this model does**
  Determines whether requested vehicle data exists for a given time period and sensor.

* **Input data format**
  Time-indexed metadata tables

* **Output data format**
  Availability summary with coverage metrics

* **Starting hyperparameter for this model**
  Minimum coverage threshold (e.g., 80%)

* **Evaluation metrics for this step**
  Availability detection accuracy

* **Why these evaluation metrics were selected**
  Incorrect availability reporting directly impacts user trust.

* **Target performance values for these metrics**
  Accuracy ≥ 98%

* **Limitations for reaching this performance**
  Missing metadata, delayed ingestion pipelines

---

## Step 5: Analytical Insight Model (Optional)

* **What ML/AI model would be best for this**
  Isolation Forest, Seasonal Decomposition, or Change Point Detection models

* **Brief reason for selecting this model**
  These models are proven for time-series anomaly and trend detection in industrial data.

* **What this model does**
  Extracts trends, anomalies, or summary statistics from sensor data.

* **Input data format**
  Time-series numerical arrays

* **Output data format**
  Statistical summaries or flagged events

* **Starting hyperparameter for this model**
  Contamination rate (e.g., 0.05)

* **Evaluation metrics for this step**
  Precision, Recall for detected events

* **Why these evaluation metrics were selected**
  False positives and false negatives have different operational impacts.

* **Target performance values for these metrics**
  Precision ≥ 0.80, Recall ≥ 0.70

* **Limitations for reaching this performance**
  Lack of labeled anomalies and sensor noise

---

## Step 6: Visualization Recommendation Model

* **What ML/AI model would be best for this**
  Rule-based mapping or decision tree

* **Brief reason for selecting this model**
  Visualization logic must be deterministic and easy to justify.

* **What this model does**
  Selects an appropriate visualization type based on data and task.

* **Input data format**
  Data type and analysis result metadata

* **Output data format**
  Visualization specification

* **Starting hyperparameter for this model**
  Rule priority order

* **Evaluation metrics for this step**
  User satisfaction score, correctness rate

* **Why these evaluation metrics were selected**
  Visualization effectiveness is best measured via user feedback.

* **Target performance values for these metrics**
  User satisfaction ≥ 4/5

* **Limitations for reaching this performance**
  Subjective user preferences and diverse use cases

---

## Step 7: Explanation & Reporting Model

* **What ML/AI model would be best for this**
  Template-based natural language generation system

* **Brief reason for selecting this model**
  Ensures predictable, auditable explanations without generative uncertainty.

* **What this model does**
  Converts analytical results into human-readable explanations.

* **Input data format**
  Structured analysis results

* **Output data format**
  Natural language explanation text

* **Starting hyperparameter for this model**
  Template selection priority

* **Evaluation metrics for this step**
  Clarity score, user comprehension rate

* **Why these evaluation metrics were selected**
  Explanations must be understandable and actionable.

* **Target performance values for these metrics**
  Comprehension rate ≥ 85%

* **Limitations for reaching this performance**
  Overly rigid templates and varying user expertise

---