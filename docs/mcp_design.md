# Model Context Protocol (MCP) Design

## MCP Communication Diagram

```mermaid
sequenceDiagram
    autonumber
    participant Agent as Specialist Agent
    participant Client as MCP Client
    participant Registry as Tool Allowlist
    participant Server as MCP Server
    participant Provider as Provider Adapter

    Agent->>Client: call_tool(name, args)
    Client->>Registry: is_tool_allowed(name)
    alt Allowed Tool
        Registry-->>Client: True
        Client->>Server: invoke_tool(args)
        Server->>Provider: execute(args)
        Provider-->>Server: Return Data
        Server-->>Client: Result Dict
        Client-->>Agent: (Success, Result, ToolCallInfo)
    else Unallowlisted Tool
        Registry-->>Client: False
        Client-->>Agent: (Failure, Error, ToolCallInfo)
    end
```

## MCP Tools Catalog
1. `search_flights(origin, destination, travelers)`
2. `get_flight_details(flight_number)`
3. `search_hotels(destination, nights, travelers)`
4. `get_hotel_details(hotel_name)`
5. `get_weather_forecast(destination, days)`
6. `search_attractions(destination)`
7. `get_destination_info(destination)`
