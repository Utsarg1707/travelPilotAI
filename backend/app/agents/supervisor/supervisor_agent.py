"""Supervisor Agent for Intent Extraction and Specialist Routing."""

import re

from langchain_core.prompts import ChatPromptTemplate

from backend.app.config.llm_factory import LLMFactory
from backend.app.schemas.supervisor import SupervisorDecision
from backend.app.schemas.travel_state import TravelState

SUPERVISOR_SYSTEM_PROMPT = """You are the Lead Supervisor Agent for TravelPilot AI.
Your sole job is to analyze user travel requests, extract key parameters, and select which specialist agents must run.

Multi-Destination Extraction:
- Extract all target destination cities requested by the user into the 'destinations' list (e.g., ["Dubai", "Abu Dhabi"], or ["Paris", "Rome"]).
- If only one city is requested, 'destinations' should contain that single city (e.g., ["Dubai"]).
- Set 'destination' to a formatted string combining all target cities (e.g., "Dubai & Abu Dhabi" or "Paris & Rome").

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
                if decision:
                    if not decision.destinations and decision.destination:
                        decision.destinations = [decision.destination]
                    elif len(decision.destinations) > 1 and " & " not in decision.destination:
                        decision.destination = " & ".join(decision.destinations)
                    return decision
            except Exception:
                # Log error and fallback gracefully to deterministic router
                pass

        # Deterministic Fallback Router for Demo / Offline Mode
        return cls._fallback_deterministic_router(user_query)

    @classmethod
    def _extract_destinations_from_query(cls, query: str, origin: str) -> list[str]:
        """Dynamically parse destination cities/regions from user natural language query."""
        query_lower = query.lower()

        # 1. Regex pattern for "to <destinations> from", "to <destinations> for", "trip to <destinations>"
        pattern = r"(?:to|visit|in|explore)\s+([a-zA-Z\s,-]+?)(?:\s+from|\s+for|\s+with|\s+under|\s+below|\s+of|\s+\d|\s*[\.!?]|$)"
        match = re.search(pattern, query, re.IGNORECASE)

        raw_dest_str = ""
        if match:
            raw_dest_str = match.group(1).strip()
            if " from " in raw_dest_str.lower():
                raw_dest_str = raw_dest_str.lower().split(" from ")[0].strip()

        if raw_dest_str:
            parts = re.split(r",|\s+and\s+|\s*&\s*", raw_dest_str, flags=re.IGNORECASE)
            stop_words = {
                "a",
                "an",
                "the",
                "trip",
                "days",
                "day",
                "people",
                "person",
                "budget",
                "pax",
                "travelers",
                "traveler",
                "snow",
                "with",
                "for",
                "from",
                "today",
                "tomorrow",
                "tonight",
                "week",
                "next",
                "month",
                "year",
                "weather",
                "flights",
                "flight",
                "hotels",
                "hotel",
                "itinerary",
                "plan",
                origin.lower(),
            }
            dests: list[str] = []
            for p in parts:
                cleaned = p.strip()
                words = [w for w in cleaned.split() if w.lower() not in stop_words]
                if words:
                    city_name = " ".join(w.capitalize() for w in words)
                    if city_name and city_name.lower() != origin.lower() and city_name not in dests:
                        dests.append(city_name)
            if dests:
                return dests

        # 2. Known places list (expanded)
        known_cities = [
            "shimla",
            "kashmir",
            "manali",
            "ladakh",
            "goa",
            "kerala",
            "jaipur",
            "udaipur",
            "mumbai",
            "delhi",
            "bangalore",
            "dubai",
            "abu dhabi",
            "paris",
            "rome",
            "venice",
            "tokyo",
            "singapore",
            "london",
            "bali",
            "switzerland",
            "new york",
            "barcelona",
        ]
        found_destinations: list[str] = []
        for city in known_cities:
            if city in query_lower and city != origin.lower():
                formatted_city = " ".join(w.capitalize() for w in city.split())
                if formatted_city not in found_destinations:
                    found_destinations.append(formatted_city)

        if found_destinations:
            return found_destinations

        return ["Dubai"]

    @classmethod
    def _fallback_deterministic_router(cls, query: str) -> SupervisorDecision:
        """Deterministic rule-based router for demo mode without LLM calls."""
        query_lower = query.lower()

        # Origin extraction heuristic
        origin = "Bangalore"
        origin_match = re.search(r"from\s+([a-zA-Z]+)", query_lower)
        if origin_match:
            origin = origin_match.group(1).capitalize()

        # Multi-destination dynamic extraction heuristic
        destinations = cls._extract_destinations_from_query(query, origin)
        destination = " & ".join(destinations) if len(destinations) > 1 else destinations[0]

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
        is_weather_only = "weather" in query_lower and not any(
            k in query_lower for k in ["plan", "trip", "flight", "hotel", "itinerary"]
        )
        is_flight_only = "flight" in query_lower and not any(
            k in query_lower for k in ["plan", "trip", "hotel", "itinerary", "weather"]
        )
        is_hotel_only = "hotel" in query_lower and not any(
            k in query_lower for k in ["plan", "trip", "flight", "itinerary", "weather"]
        )

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
            reason = f"Full multi-destination travel plan requested for {destination}. Routing to specialist agents."

        return SupervisorDecision(
            destination=destination,
            destinations=destinations,
            origin=origin,
            travelers=travelers,
            duration_days=duration,
            required_agents=required_agents,
            routing_reason=reason,
            constraints={"budget": budget},
        )
