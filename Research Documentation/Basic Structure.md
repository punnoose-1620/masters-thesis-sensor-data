# Core Idea

**Design and evaluate an adaptive agent that decides what vehicle data to fetch, how to fetch it and how to interpret it, using metadata aware reasoning over evolving time-series storage**

### Key Emphasis:
- The agent does not stream live data
- Data changes over time (new files, new signals, new aggregations)
- Minimal code changes -> Adaptibility based on Metadata
- Focus on decision making, not just querying

# Ideal High Level Architecture

Use Reasoning + Acting style Agent [ReAct Style](https://arxiv.org/pdf/2210.03629). 
Add constraints to manage safety for data privacy and storage security. ReAct structure by itself is too chaotic to be used directly.

```java
User Question
   ↓
Query Interpreter (LLM)
   ↓
Reasoning Step (What do I need?)
   ↓
Metadata & Governance Agent  ←── MOST IMPORTANT
   ↓
Data Retrieval Agent (tools)
   ↓
Interpretation Agent
   ↓
Answer + Explanation
```
Instead of using a single agent, convert it into an agent loop with clear sections marking which is responsible for each. This would allow easier diagnosis and clearer explainability since Automotive Data interpretation needs to be concise.

# Agent Roles

## 1. Query Interpretation Agent (LLM)

Since Volvo has ties with copilot, Copilot would be the preferred candidate here. This can be replaced easily with other agents as and when company requires since this is not a **pre-trained** module.

*Note: This agent does not involve in fetching data. It only interprets human idea into machine understandable idea. This can be replaced with locally run models if required without affecting performance.*

**Input**

*“Was the vehicle braking unusually hard during the last test run?”*

**Output (Expected Structure)**

```json
{
  "task": "analyze",
  "concepts": ["braking", "hard braking"],
  "time_scope": "last test run",
  "confidence_required": "medium"
}
```

## 2. Metadata and Catalog Agent (Key Novelty of this project)

This agent is meant to answer the following doubts every time : 
- What signals exist?
- What are they called?
- Units of measurement and sampling rate clarifications
- Clarify Raw vs Derived responses/interpretations
- Who owns the data that has been fetched
- Who has access to this data

**Example output**
```json
[
  {
    "signal": "brake_pressure",
    "unit": "bar",
    "sampling_rate": "100Hz",
    "derived_versions": ["brake_pressure_avg_1s"],
    "access": "allowed"
  }
]
```
This part enables adaptability. This allows for new kinds of data to be added to the source without having to alter the code or the algorithm to adapt to that kind of data. This would allow this algorithm to be used on a larger scale for longer terms with minimal changes.

## 3. Governance and Access Agent

This agent blocks illegal access and forces an aggregation-first access order. The idea here is that before data is fetched, the following questions are answered : 
- Is this user allowed to access the requested data?
- Is the data sensitive?
- Is aggregation from different sources/functions required for this data?

**Example Output**
```json
{
  "allowed": true,
  "restriction": "use aggregated data only"
}
```

## 4. Data Retrieval Agent

This agent is supposed to only call functions. The SQL queries implemented by these functions are supposed to be pre-written and the agent will have no say in what is being queried or the structure of the query. The sources will be selected based on metadata instead of going through each source every time.
This agent is responsible for making the following decisions : 
- Aggregated vs Raw - which to use
- Which functions to run to fetch the right data
- Test Metadata to see which files/sources to invoke

**Example calls from Agent**

```python
get_aggregated_signal(signal_name, start_time, end_time)
get_raw_signal(signal_name, run_id)
get_dtc_codes(run_id)
get_test_metadata(run_id)
```

## 5. Interpretation and Analysis Agent

This agent will be responsible for the following tasks : 
- Interpret the numeric data values fetched
- Detect anomalies in the fetched data values
- Compare fetched data to baseline values which may be generic or pre-determined by the company. Predetermined baseline values will need additional functions to be implemented in this flow since they will also be stored rather than implied.
- Summarize patterns in the fetched data

This agent is where the domain-based reasoning happens. We can use either a raw LLM or rule-base + LLM based on the details of the data being handled and the expected applications.

**Example Json Result**
```json
{
  "finding": "Hard braking detected",
  "evidence": "Peak brake pressure exceeded 95th percentile",
  "confidence": "high"
}
```

## 6. Mapping Datatypes to Agent's Decisions

This is where we make sure the data we fetched from the source fits the response from the agent naturally and without conflict.
We could add more rules based off of our interactions with data owners and domain experts but basically, we should follow the following rules for each type of data, assuming these are all the required rules :
- **Raw Time Series Data**
   - Only use aggregation if data from single source is insufficient
   - High cost should trigger a justification from agent for the reasons regarding high cost
   - Basic logic implemented by this agent *“Is there a derived feature that answers this faster?”*
- **Derived vs Aggregated Data**
   - First choice for all features is aggregated data. 
   - Makes the outputs efficient, scalable and more importantly, explainable since we know which data came from where without digging too deep
   - Basically gives this agent a bias that implies *Always try aggregate data first*
- **Meta-data and Data Catalog**
   - This part acts as the brain of the system, controlling sources and keeping track of where each file lies. 
   - This part describes 
      - **the nature of signals**
      - **the meaning of a given signal** and 
      - **the sources of a signal**. 
   - This is a part of our project that makes it unique above similar projects.
- **Diagnostic Troubleshooting Codes**
   - This is planned to be handled through Ontology lookup and semantic mapping. 
   - Further details on implementation has to be based on how error codes are stored/mapped in company database and how they can be accessed.
- **Event/State signals**
   - This part would be ideal for rule-based checks and fast responses.
   - This would also reduce the resources consumed

# Proposed Evaluation Metrics
- Tool Selection Ratio (Number of times of aggregated tools selected vs raw tools selected per N selections)
- Correct Signal Identification
- Governance Violations (should be 0 ideally)
- Answer Correctness (verified by domain experts)

