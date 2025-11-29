# Agent Architecture

This system uses a sequential hierarchical flow where the Planner dictates the steps, and context is passed forward to ensure agents are "aware" of previous findings.

```mermaid
graph TD
    User[User Query] --> Planner[Planner Agent]
    Planner -->|Generates Steps| Orchestrator[run.py Loop]
    
    Orchestrator -->|Step 1: Get Metrics| Data[Data Agent]
    Data -->|Pandas Calculation| DB[(CSV Data)]
    DB -->|Raw Numbers| Data
    Data -->|Data Context| Orchestrator
    
    Orchestrator -->|Step 2: Find Patterns| Insight[Insight Agent]
    Insight -->|Hypothesis| Orchestrator
    
    Orchestrator -->|Step 3: Fix Ads| Creative[Creative Agent]
    Creative -->|New Ad Copy| Orchestrator
    
    Orchestrator -->|Compiles| Report[Final Report.md]