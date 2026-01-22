# Deterministic AI System – Data Documentation

This document describes the **data requirements** for building a deterministic (non-LLM) AI-based natural language system to support access to vehicle sensor data. It also documents **what additional information can be inferred** from existing sensor data using classical data analysis and machine learning techniques.

---

## Part A – Data Required to Build the Deterministic System

This section focuses on **non-sensor data** required to make the system functional, predictable, and explainable.

### 1. User Query Dataset (Natural Language Queries)

**Purpose**: Train and/or validate intent classification and slot extraction modules.

| Attribute       | Description                                                           |
| --------------- | --------------------------------------------------------------------- |
| Data type       | Text (natural language)                                               |
| Example value   | "Show available temperature data for vehicle V123 last week"          |
| Minimum entries | 200–300 queries                                                       |
| Notes           | Can be synthetically generated and later refined with real user input |

---

### 2. Intent Labels

**Purpose**: Define what type of action the system should perform.

| Attribute          | Description                                                       |
| ------------------ | ----------------------------------------------------------------- |
| Data type          | Categorical label                                                 |
| Example value      | `check_data_availability`                                         |
| Minimum entries    | Same as number of queries (1 label per query)                     |
| Example intent set | data_availability, summary_request, anomaly_detection, comparison |

---

### 3. Slot / Entity Annotations

**Purpose**: Extract structured parameters from user queries.

| Slot Type   | Example Value | Minimum Required |
| ----------- | ------------- | ---------------- |
| vehicle_id  | `V123`        | 200–300          |
| sensor_type | `temperature` | 200–300          |
| time_range  | `last_week`   | 200–300          |
| aggregation | `average`     | 100–150          |

**Notes**:

* Can be rule-based or ML-based
* Not all slots are required for all intents

---

### 4. Sensor Metadata Registry

**Purpose**: Enable validation and mapping of user requests to real data.

| Attribute       | Description                                                     |
| --------------- | --------------------------------------------------------------- |
| Data type       | Structured metadata (JSON / table)                              |
| Example value   | `{ "sensor": "temperature", "unit": "°C", "frequency": "1Hz" }` |
| Minimum entries | One per sensor type                                             |

---

### 5. Function Capability Registry

**Purpose**: Deterministic planning and function selection.

| Attribute       | Description                            |
| --------------- | -------------------------------------- |
| Data type       | Configuration / rules                  |
| Example value   | `detect_anomalies(sensor, time_range)` |
| Minimum entries | One per supported operation            |

---

### 6. Visualization Mapping Rules

**Purpose**: Decide which visualization to use for which data type.

| Attribute       | Description                                      |
| --------------- | ------------------------------------------------ |
| Data type       | Rules or lookup table                            |
| Example value   | `time_series + anomaly → line_plot_with_markers` |
| Minimum entries | 10–20 rules                                      |

---

### 7. Explanation Templates

**Purpose**: Generate human-readable explanations without generative models.

| Attribute       | Description                                                           |
| --------------- | --------------------------------------------------------------------- |
| Data type       | Text templates                                                        |
| Example value   | "The data shows a temperature increase of {value}°C during {period}." |
| Minimum entries | 15–30 templates                                                       |

---


