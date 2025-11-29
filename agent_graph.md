# Agent Architecture

This system uses a sequential hierarchical flow where the Planner dictates the steps, and context is passed forward to ensure agents are "aware" of previous findings.

```mermaid
graph LR
    User[User Query] --> Planner[Planner Agent]
    Planner -->|Generates<br/>Steps| Orch[Orchestrator<br/>(run.py)]
    
    Orch -->|Step 1:<br/>Get Metrics| Data[Data Agent]
    Data -->|Pandas<br/>Calc| DB[(CSV Data)]
    DB -->|Returns<br/>Data| Data
    Data -.->|Data<br/>Context| Orch
    
    Orch -->|Step 2:<br/>Find Patterns| Insight[Insight Agent]
    Insight -.->|Hypothesis| Orch
    
    Orch -->|Step 3:<br/>Fix Ads| Creative[Creative Agent]
    Creative -.->|New<br/>Ad Copy| Orch
    
    Orch ==>|Compiles| Report[Final Report.md]
    
    %% Style the nodes for better visibility
    style Orch fill:#f9f,stroke:#333,stroke-width:2px
    style DB fill:#ff9,stroke:#333,stroke-width:2px
    style Report fill:#9f9,stroke:#333,stroke-width:2px