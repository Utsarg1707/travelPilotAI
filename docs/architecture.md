# TravelPilot AI — Architecture & System Design

## 1. High-Level Architecture

```mermaid
flowchart TD
    User([User Prompt]) --> InputGuardrail[Input Guardrail Node]
    InputGuardrail -->|Pass| Supervisor[Supervisor Agent]
    InputGuardrail -->|Block| BlockedResponse[Return Guardrail Error]
    
    Supervisor -->|Dynamic Routing| SpecialistAgents{Required Specialist Agents}
    
    SpecialistAgents --> Flight[Flight Agent]
    SpecialistAgents --> Hotel[Hotel Agent]
    SpecialistAgents --> Weather[Weather Agent]
    
    Flight --> MCP_Flight[MCP Flight Server]
    Hotel --> MCP_Hotel[MCP Hotel Server]
    Weather --> OpenMeteo[Open-Meteo Free API]
    
    Flight & Hotel & Weather --> Budget[Budget Agent - Deterministic]
    Budget --> Itinerary[Itinerary Agent]
    Itinerary --> OutputGuardrail[Output Guardrail Node]
    
    OutputGuardrail --> HITL[Human Review Node - Interrupt]
    
    HITL -->|Approve| Complete[Final Response]
    HITL -->|Edit| Reevaluate[Update Feedback & Revise]
    HITL -->|Reject| EndState[End Session]
```

## 2. LangGraph Stateful Workflow

```mermaid
stateDiagram-v2
    [*] --> InputGuardrail
    InputGuardrail --> Supervisor: Validated & Safe
    InputGuardrail --> [*]: Unsafe / Out of Scope
    
    Supervisor --> FlightAgent: 'flight' requested
    Supervisor --> HotelAgent: 'hotel' requested
    Supervisor --> WeatherAgent: 'weather' requested
    Supervisor --> OutputGuardrail: Synthesize Response
    
    FlightAgent --> HotelAgent
    HotelAgent --> WeatherAgent
    WeatherAgent --> BudgetAgent
    BudgetAgent --> ItineraryAgent
    ItineraryAgent --> OutputGuardrail
    
    OutputGuardrail --> HumanReview
    HumanReview --> [*]: Approved / Rejected
    HumanReview --> OutputGuardrail: Edited
```

## 3. Why Multi-Agent & Why LangGraph?
* **Decoupled Responsibilities**: Small, focused specialist agents (Flight, Hotel, Weather, Budget, Itinerary) prevent giant prompt pollution and improve reasoning precision.
* **Deterministic Financial Control**: Arithmetic calculations (flight + hotel + daily expenses) are computed in pure Python within the `BudgetAgent`, eliminating LLM calculation hallucinations.
* **Stateful Interrupts**: LangGraph provides native checkpointer thread state (`MemorySaver` / SQLite) allowing the workflow to interrupt execution for human review and resume seamlessly when approved, edited, or rejected.
