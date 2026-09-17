# Agent Design Specification & Supervisor Routing

## Supervisor Routing Diagram

```mermaid
graph TD
    UserQuery[User Input Query] --> Supervisor[Supervisor Agent]
    
    Supervisor -->|Weather Query Only| WeatherOnly[Weather Agent -> Output Guardrail]
    Supervisor -->|Flight Query Only| FlightOnly[Flight Agent -> Output Guardrail]
    Supervisor -->|Hotel Query Only| HotelOnly[Hotel Agent -> Output Guardrail]
    Supervisor -->|Full Trip Request| FullPipeline[Flight -> Hotel -> Weather -> Budget -> Itinerary]
```

## Agent Specification Table

| Agent | Responsibility | Primary Tool / Provider | Output Schema |
| :--- | :--- | :--- | :--- |
| **Supervisor** | Intent extraction & dynamic agent selection | Groq LLM / Rule-based | `SupervisorDecision` |
| **Flight Agent** | Flight option search & comparison | MCP `search_flights` | `FlightSearchResult` |
| **Hotel Agent** | Accommodation option search & rating check | MCP `search_hotels` | `HotelSearchResult` |
| **Weather Agent** | Destination weather forecast | Free Open-Meteo REST API | `WeatherResult` |
| **Budget Agent** | Deterministic cost calculation & balance | Python Math Engine | `BudgetAnalysis` |
| **Itinerary Agent** | Day-by-day activity synthesis & scheduling | Structured Reasoning | `Itinerary` |
