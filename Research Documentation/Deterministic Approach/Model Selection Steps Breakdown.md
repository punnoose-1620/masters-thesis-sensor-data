# Deterministic AI Approach – Model Breakdown (Deep Dive)

This document provides a **deeper, practical breakdown** of each model or logical component in the deterministic AI approach for supporting natural language access to vehicle data. The focus is on **engineering considerations**, **time estimates**, and **practical constraints**, rather than algorithms or implementation details.

All steps assume required datasets are already available in a local `datasets/` directory.

---

## Step 1: User Intent Classification Model

* **What to consider when choosing the right model**
  Number of supported intents, variability of user language, need for explainability, and tolerance for misclassification.

* **Expected time to completion**
  1–2 weeks (including dataset preparation and validation).

* **Tips to speed up the process**
  Start with a small, well-defined intent set and expand incrementally; reuse existing task-oriented dialogue datasets for structure.

* **Expected processing power required**
  Low to moderate; CPU-based training is sufficient for classical models, lightweight GPU optional for transformer-based classifiers.

* **Models historically proven in automotive domain**
  Support Vector Machines (SVM), Logistic Regression, fine-tuned DistilBERT for in-vehicle assistants.

---

## Step 2: Slot / Entity Extraction Model

* **What to consider when choosing the right model**
  Entity consistency, domain-specific terminology, explainability, and ease of rule augmentation.

* **Expected time to completion**
  1–2 weeks.

* **Tips to speed up the process**
  Combine rule-based extraction for stable entities with ML-based NER for flexible language patterns.

* **Expected processing power required**
  Low; CPU-only environments are sufficient for CRF or rule-based systems.

* **Models historically proven in automotive domain**
  Conditional Random Fields (CRF), spaCy NER pipelines, rule-based entity extractors.

---

## Step 3: Query Validation & Normalization Engine

* **What to consider when choosing the right model**
  Alignment with data governance rules, sensor catalog completeness, and need for deterministic behavior.

* **Expected time to completion**
  1 week.

* **Tips to speed up the process**
  Use predefined metadata schemas and lookup tables rather than learned models.

* **Expected processing power required**
  Minimal; simple rule evaluation on CPU.

* **Models historically proven in automotive domain**
  Rule-based validation engines, decision-tree–based validators.

---

## Step 4: Data Availability Inference Model

* **What to consider when choosing the right model**
  Metadata quality, timestamp accuracy, and latency of data ingestion pipelines.

* **Expected time to completion**
  1–2 weeks.

* **Tips to speed up the process**
  Focus on metadata-driven availability checks before analyzing raw signal data.

* **Expected processing power required**
  Low; primarily metadata queries on CPU.

* **Models historically proven in automotive domain**
  Statistical coverage analysis, rule-based availability detection.

---

## Step 5: Analytical Insight Model (Trend / Anomaly Detection)

* **What to consider when choosing the right model**
  Signal frequency, seasonality, noise levels, and availability of labeled events.

* **Expected time to completion**
  2–3 weeks.

* **Tips to speed up the process**
  Start with simple statistical methods before introducing ML-based anomaly detectors.

* **Expected processing power required**
  Moderate; CPU sufficient for most models, GPU optional for deep time-series models.

* **Models historically proven in automotive domain**
  Isolation Forest, Seasonal-Trend Decomposition (STL), change point detection methods.

---

## Step 6: Visualization Recommendation Model

* **What to consider when choosing the right model**
  User expectations, data dimensionality, and consistency with internal visualization standards.

* **Expected time to completion**
  1 week.

* **Tips to speed up the process**
  Predefine visualization mappings based on data type and task.

* **Expected processing power required**
  Minimal; rule evaluation only.

* **Models historically proven in automotive domain**
  Rule-based visualization mapping systems, decision trees.

---

## Step 7: Explanation & Reporting Model

* **What to consider when choosing the right model**
  Clarity, auditability, and suitability for non-technical users.

* **Expected time to completion**
  1–2 weeks.

* **Tips to speed up the process**
  Reuse standardized explanation templates and focus on key metrics only.

* **Expected processing power required**
  Minimal; text rendering only.

* **Models historically proven in automotive domain**
  Template-based natural language generation systems.

---

## Overall Time & Resource Summary

* **Total estimated development time**: 8–12 weeks
* **Primary hardware requirement**: Standard workstation (CPU-focused)
* **GPU dependency**: Optional, not required for deterministic approach

---