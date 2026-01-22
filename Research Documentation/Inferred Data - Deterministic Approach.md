# Deterministic AI System – Data Documentation

This document describes the **data requirements** for building a deterministic (non-LLM) AI-based natural language system to support access to vehicle sensor data. It also documents **what additional information can be inferred** from existing sensor data using classical data analysis and machine learning techniques.

## Part B – Information That Can Be Extracted or Inferred from Vehicle Sensor Data

This section documents **derived data and insights** that can be obtained from raw vehicle sensor data using classical data analysis and ML techniques.

---

### 1. Data Availability Metrics

| Inferred Information | Description                    | Example                     |
| -------------------- | ------------------------------ | --------------------------- |
| Data coverage        | Percentage of time data exists | 92% coverage last week      |
| Missing intervals    | Gaps in data streams           | No data between 02:00–03:00 |

---

### 2. Statistical Summaries

| Inferred Information | Description         | Example                                 |
| -------------------- | ------------------- | --------------------------------------- |
| Mean / median        | Central tendency    | Avg speed = 54 km/h                     |
| Min / max            | Range of values     | Max temp = 78°C                         |
| Variance             | Stability of signal | Low variance indicates steady operation |

---

### 3. Trend Analysis

| Inferred Information | Description        | Example                      |
| -------------------- | ------------------ | ---------------------------- |
| Long-term trend      | Directional change | Gradual battery degradation  |
| Seasonal patterns    | Repeating behavior | Higher consumption in winter |

---

### 4. Anomaly Detection

| Inferred Information | Description            | Example                    |
| -------------------- | ---------------------- | -------------------------- |
| Point anomalies      | Sudden abnormal values | Temperature spike at 14:32 |
| Contextual anomalies | Abnormal in context    | High speed while parked    |

---

### 5. Event Detection

| Inferred Information | Description                | Example                       |
| -------------------- | -------------------------- | ----------------------------- |
| Threshold events     | Values crossing limits     | Brake temp > safety limit     |
| Change points        | Sudden distribution shifts | Sensor recalibration detected |

---

### 6. Sensor Health Indicators

| Inferred Information | Description            | Example                |
| -------------------- | ---------------------- | ---------------------- |
| Drift                | Gradual bias over time | Pressure sensor offset |
| Noise increase       | Signal degradation     | Sensor aging           |

---

### 7. Cross-Sensor Correlations

| Inferred Information | Description       | Example                          |
| -------------------- | ----------------- | -------------------------------- |
| Correlated behavior  | Linked signals    | Speed vs energy consumption      |
| Redundancy detection | Duplicate signals | Two sensors reporting same trend |

---

### 8. Usage & Operational Patterns

| Inferred Information | Description         | Example                    |
| -------------------- | ------------------- | -------------------------- |
| Driving patterns     | Behavioral insights | Frequent short trips       |
| Vehicle utilization  | Active vs idle time | 70% parked during weekdays |

---

## Notes

* All inferred information relies on **existing sensor data only**
* No additional data collection is required
* These insights can be generated using deterministic algorithms and classical ML models

---

*This document supports system design, data governance discussions, and implementation planning for deterministic AI systems in an automotive context.*