"""Supervisor Agent for Intent Extraction and Specialist Routing."""

import re

from langchain_core.prompts import ChatPromptTemplate

from backend.app.config.llm_factory import LLMFactory
from backend.app.schemas.supervisor import SupervisorDecision
from backend.app.schemas.travel_state import TravelState

SUPERVISOR_SYSTEM_PROMPT = """You are the Lead Supervisor Agent for TravelPilot AI.
Your sole job is to analyze user travel requests, extract key parameters, and select which specialist agents must run.

Available Specialist Agents:
- "flight": Search and compare flight options between origin and destination.
- "hotel": Search accommodation options in destination.
- "weather": Fetch destination weather forecast and travel recommendations.
- "budget": Compute deterministic cost breakdown and budget feasibility.
- "itinerary": Generate day-by-day travel activities schedule.

Routing Rules:
1. If the user asks ONLY about weather (e.g., "What is the weather in Dubai?"), select ONLY ["weather"].
2. If the user asks ONLY about flights (e.g., "Find flights from Bangalore to Dubai"), select ONLY ["flight"].
3. If the user asks ONLY about hotels, select ONLY ["hotel"].
4. If the user asks for a complete trip plan or itinerary, select ALL relevant agents: ["flight", "hotel", "weather", "budget", "itinerary"].

Return structured output matching SupervisorDecision schema. DO NOT output chain-of-thought or raw reasoning text."""


class SupervisorAgent:
    """Supervisor Agent coordinating workflow execution and dynamic routing."""

    @classmethod
    def run(cls, state: TravelState) -> SupervisorDecision:
        """Execute Supervisor decision logic."""
        user_query = state.get("user_query", "")

        # Try LLM-based structured extraction if Groq key is configured
        if LLMFactory.is_groq_available():
            try:
                llm = LLMFactory.get_chat_model(temperature=0.1)
                structured_llm = llm.with_structured_output(SupervisorDecision)
                prompt = ChatPromptTemplate.from_messages(
                    [
                        ("system", SUPERVISOR_SYSTEM_PROMPT),
                        ("human", "{user_query}"),
                    ]
                )
                chain = prompt | structured_llm
                decision: SupervisorDecision = chain.invoke({"user_query": user_query})
                return decision
            except Exception:
                # Log error and fallback gracefully to deterministic router
                pass

        # Deterministic Fallback Router for Demo / Offline Mode
        return cls._fallback_deterministic_router(user_query)

    @classmethod
    def _fallback_deterministic_router(cls, query: str) -> SupervisorDecision:
        """Deterministic rule-based router for demo mode without LLM calls."""
        query_lower = query.lower()

        # Destination extraction heuristic
        destination = "Dubai"
        for city in ["dubai", "paris", "tokyo", "singapore", "goa", "london", "rome", "bali", "bangalore"]:
            if city in query_lower:
                destination = city.capitalize()
                break

        # Origin extraction heuristic
        origin = "Bangalore"
        origin_match = re.search(r"from\s+([a-zA-Z]+)", query_lower)
        if origin_match and origin_match.group(1).lower() != destination.lower():
            origin = origin_match.group(1).capitalize()

        # Duration extraction heuristic
        duration = 5
        duration_match = re.search(r"(\d+)\s*[-_\s]*days?", query_lower)
        if duration_match:
            duration = int(duration_match.group(1))

        # Travelers extraction heuristic
        travelers = 2
        people_match = re.search(r"(\d+)\s*(people|person|travelers?|pax)", query_lower)
        if people_match:
            travelers = int(people_match.group(1))

        # Budget extraction heuristic (INR)
        budget = 150000.0
        budget_match = re.search(r"(?:budget|under|below|of)?\s*₹?\s*([\d,]+)", query_lower)
        if budget_match:
            try:
                raw_num = budget_match.group(1).replace(",", "")
                if len(raw_num) >= 4:  # Reasonable budget figure
                    budget = float(raw_num)
            except ValueError:
                pass

        # Agent selection heuristic
        required_agents: list[str] = []
        is_weather_only = "weather" in query_lower and not any(k in query_lower for k in ["plan", "trip", "flight", "hotel", "itinerary"])
        is_flight_only = "flight" in query_lower and not any(k in query_lower for k in ["plan", "trip", "hotel", "itinerary", "weather"])
        is_hotel_only = "hotel" in query_lower and not any(k in query_lower for k in ["plan", "trip", "flight", "itinerary", "weather"])

        if is_weather_only:
            required_agents = ["weather"]
            reason = "Weather query detected: Routing exclusively to Weather Agent."
        elif is_flight_only:
            required_agents = ["flight"]
            reason = "Flight query detected: Routing exclusively to Flight Agent."
        elif is_hotel_only:
            required_agents = ["hotel"]
            reason = "Hotel query detected: Routing exclusively to Hotel Agent."
        else:
            required_agents = ["flight", "hotel", "weather", "budget", "itinerary"]
            reason = f"Full travel plan requested for {destination}. Routing to specialist agents."

        return SupervisorDecision(
            destination=destination,
            origin=origin,
            travelers=travelers,
            duration_days=duration,
            required_agents=required_agents,
            routing_reason=reason,
            constraints={"budget": budget},
        )
