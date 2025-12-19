# Problem Statement

Over the years, we have observed a recurring challenge:

Although vehicles generate millions of data points, internal teams repeatedly ask the same fundamental questions:

- **What data are we collecting?**
- **Which signal indicates a specific vehicle state (on/off, level, status)?**
- **Do we collect data for a specific component or feature?**

To answer these questions, we often need to:

- Identify the correct domain expert
- Translate user questions into specific signal names
- Respond to repeated requests across teams

This process is time-consuming, inefficient, and does not scale, especially since we are not experts in every domain area.

# Proposed Idea

One idea we discussed is to build an internal chatbot connected to structured metadata and documentation about vehicle data. The chatbot should be able to answer questions such as:
- Are we collecting this data?
- Which signals are available for a given component?
- What does this signal represent?
- What is the data source, frequency, and quality?

Additionally, the chatbot must be able to :
- Provide context-aware answers without requiring users to contact multiple people
- Be generic, not tied to one specific data domain, and reusable across different datasets

# Constraints and Challenges

Several constraints must be considered:
- Enterprise tool approval process for GenAI solutions
- Data access and privacy restrictions
- Readiness of data for AI (metadata quality, documentation, access control)
- Maintenance and lifecycle management if deployed in production
- Scalability across teams and departments
- Potential need for different agents for different use cases

Additionally, onboarding and experimentation currently require significant self-learning, trial-and-error, and varying levels of expertise across team members.

# Technology Context

Potential platforms and tools include:
- Azure
- Databricks
- Approved GenAI tools within the company ecosystem

The solution does not necessarily need real-time processing, but it should handle routinely updated datasets and scale with growing data volumes.

# Objective

The objective is to move beyond a one-off prototype and instead create a holistic, scalable solution that:
- Reduces repetitive questions
- Improves data discoverability
- Spreads knowledge across the organization
- Delivers long-term value while complying with governance and privacy requirements