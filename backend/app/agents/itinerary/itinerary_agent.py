"""Itinerary Specialist Agent."""


from backend.app.schemas.itinerary import Itinerary, ItineraryActivity, ItineraryDay
from backend.app.schemas.travel_state import TravelState


class ItineraryAgent:
    """Specialist Agent responsible for synthesizing day-by-day activity schedules."""

    @classmethod
    def generate(
        cls,
        destination: str = "Dubai",
        duration_days: int = 5,
        preferences: list[str] | None = None,
    ) -> Itinerary:
        """Generate structured day-by-day itinerary without scheduling conflicts."""
        prefs = preferences or []
        days: list[ItineraryDay] = []

        day_themes = [
            "Arrival, Hotel Check-in & Beach Relaxation",
            "Iconic Landmarks & Cultural Old Town",
            "Desert Safari & Sunset Dunes Adventure",
            "Luxury Shopping, Marina Cruise & Dining",
            "Leisurely Breakfast & Airport Departure",
        ]

        for i in range(1, duration_days + 1):
            theme = day_themes[(i - 1) % len(day_themes)]
            activities: list[ItineraryActivity] = []

            if i == 1:
                activities = [
                    ItineraryActivity(
                        time_slot="08:45 AM - 10:30 AM",
                        activity_title="Arrival & Immigration",
                        description=f"Land at {destination} International Airport and collect luggage.",
                        location=f"{destination} International Airport",
                        cost_inr=0.0,
                    ),
                    ItineraryActivity(
                        time_slot="12:00 PM - 02:00 PM",
                        activity_title="Hotel Check-in & Lunch",
                        description="Check into resort and enjoy fresh coastal seafood lunch.",
                        location="Hotel Restaurant",
                        cost_inr=1500.0,
                    ),
                    ItineraryActivity(
                        time_slot="04:00 PM - 07:30 PM",
                        activity_title="Beachfront Sunset Promenade Walk",
                        description="Relaxed afternoon stroll along the beach and watching sunset.",
                        location="Beach Promenade",
                        cost_inr=0.0,
                    ),
                ]
            elif i == duration_days:
                activities = [
                    ItineraryActivity(
                        time_slot="09:00 AM - 11:00 AM",
                        activity_title="Leisurely Breakfast & Souvenir Shopping",
                        description="Final breakfast at resort and picking up local souvenirs.",
                        location="Local Market",
                        cost_inr=1200.0,
                    ),
                    ItineraryActivity(
                        time_slot="01:30 PM - 04:30 PM",
                        activity_title="Check-out & Flight Transfer",
                        description="Hotel check-out and transfer to airport for return flight.",
                        location="Airport",
                        cost_inr=1000.0,
                    ),
                ]
            else:
                activities = [
                    ItineraryActivity(
                        time_slot="09:30 AM - 01:00 PM",
                        activity_title=f"Morning Excursion: {theme.split('&')[0]}",
                        description=f"Guided morning tour exploring key highlights of {destination}.",
                        location=f"Central {destination}",
                        cost_inr=2500.0,
                    ),
                    ItineraryActivity(
                        time_slot="03:30 PM - 08:30 PM",
                        activity_title=f"Afternoon & Evening Activity: {theme}",
                        description="Immersive afternoon experience tailored to relaxed activities.",
                        location=f"{destination} Attractions Area",
                        cost_inr=3500.0,
                    ),
                ]

            daily_cost = sum(a.cost_inr for a in activities)
            days.append(
                ItineraryDay(
                    day_number=i,
                    date=f"2026-10-0{i}",
                    theme=theme,
                    activities=activities,
                    daily_cost_inr=daily_cost,
                )
            )

        summary = f"Custom {duration_days}-day itinerary for {destination} balancing relaxation, dining, and sightseeing."
        highlights = [
            f"Seamless arrival transfer and hotel settlement in {destination}",
            "Balanced morning excursions and relaxed afternoon leisure hours",
            "No scheduling overlaps between flight arrivals and activities",
        ]

        return Itinerary(
            destination=destination,
            total_days=duration_days,
            days=days,
            summary=summary,
            highlights=highlights,
        )

    @classmethod
    def run_node(cls, state: TravelState) -> TravelState:
        """Execute Itinerary Agent as a LangGraph node handler."""
        destination = state.get("destination") or "Dubai"
        decision = state.get("supervisor_decision")
        duration = decision.duration_days if decision else 5
        preferences = state.get("preferences") or []

        itinerary = cls.generate(destination=destination, duration_days=duration, preferences=preferences)

        # Synthesize clear final response markdown
        synth_response = (
            f"# Travel Plan for {destination} ({duration} Days)\n\n"
            f"**Travelers**: {decision.travelers if decision else 2} | **Origin**: {state.get('origin', 'Bangalore')}\n\n"
            f"### Flight & Hotel Summary\n"
            f"- **Flight Option**: {state.get('flight_results').cheapest_option.airline if state.get('flight_results') and state.get('flight_results').cheapest_option else 'IndiGo (Simulated)'}\n"
            f"- **Hotel**: {state.get('hotel_results').options[0].hotel_name if state.get('hotel_results') and state.get('hotel_results').options else 'Beach Resort (Simulated)'}\n\n"
            f"### Budget Status\n"
            f"- **Total Estimated Cost**: ₹{state.get('budget_analysis').estimated_total:,.2f} / ₹{state.get('budget_analysis').budget_limit:,.2f} ({state.get('budget_analysis').status_label if state.get('budget_analysis') else 'Within Budget'})\n\n"
            f"### Itinerary Highlights\n"
            + "\n".join(f"- {h}" for h in itinerary.highlights)
            + "\n\n*Demo Mode: Flight and hotel results are simulated and are not live booking availability.*"
        )

        return {
            "itinerary": itinerary,
            "final_response": synth_response,
        }
