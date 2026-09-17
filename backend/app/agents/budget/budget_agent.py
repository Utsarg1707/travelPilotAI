"""Budget Specialist Agent using Deterministic Python Arithmetic."""


from backend.app.schemas.budget import BudgetAnalysis, CostBreakdown
from backend.app.schemas.flights import FlightSearchResult
from backend.app.schemas.hotels import HotelSearchResult
from backend.app.schemas.travel_state import TravelState


class BudgetAgent:
    """Specialist Agent responsible for deterministic financial analysis."""

    @classmethod
    def calculate(
        cls,
        budget_limit: float = 150000.0,
        duration_days: int = 5,
        travelers: int = 2,
        flight_results: FlightSearchResult | None = None,
        hotel_results: HotelSearchResult | None = None,
    ) -> BudgetAnalysis:
        """Perform exact deterministic arithmetic calculations for trip expenses."""
        # 1. Flight Expense
        flight_cost = 0.0
        if flight_results and flight_results.cheapest_option:
            flight_cost = flight_results.cheapest_option.total_price_inr
        else:
            # Baseline estimation if flight agent was skipped
            flight_cost = 14200.0 * travelers

        # 2. Hotel Expense
        hotel_cost = 0.0
        if hotel_results and hotel_results.options:
            hotel_cost = hotel_results.options[0].total_price_inr
        else:
            # Baseline estimation if hotel agent was skipped
            hotel_cost = 6200.0 * max(1, duration_days - 1)

        # 3. Deterministic Daily Expense Estimates (INR per traveler/day)
        food_cost = 1500.0 * duration_days * travelers
        transport_cost = 1000.0 * duration_days * travelers
        activities_cost = 1500.0 * duration_days * travelers
        misc_cost = 1000.0 * duration_days

        total_estimated = flight_cost + hotel_cost + food_cost + transport_cost + activities_cost + misc_cost
        remaining = budget_limit - total_estimated
        within_budget = total_estimated <= budget_limit

        breakdown = CostBreakdown(
            flights=round(flight_cost, 2),
            accommodation=round(hotel_cost, 2),
            food=round(food_cost, 2),
            transport=round(transport_cost, 2),
            activities=round(activities_cost, 2),
            miscellaneous=round(misc_cost, 2),
        )

        recommendations: list[str] = []
        if within_budget:
            status_label = "Within Budget"
            recommendations.append(f"Excellent! Your plan is ₹{abs(remaining):,.2f} under budget.")
            recommendations.append("Consider allocating excess budget for fine dining or desert safari upgrades.")
        else:
            status_label = "Over Budget"
            recommendations.append(f"Warning: Estimated expenses exceed budget limit by ₹{abs(remaining):,.2f}.")
            recommendations.append("Consider opting for budget airlines or choosing 3-star downtown accommodations.")

        return BudgetAnalysis(
            estimated_total=round(total_estimated, 2),
            budget_limit=round(budget_limit, 2),
            remaining_budget=round(remaining, 2),
            within_budget=within_budget,
            cost_breakdown=breakdown,
            recommendations=recommendations,
            status_label=status_label,
        )

    @classmethod
    def run_node(cls, state: TravelState) -> TravelState:
        """Execute Budget Agent as a LangGraph node handler."""
        budget_limit = state.get("budget") or 150000.0
        decision = state.get("supervisor_decision")
        duration = decision.duration_days if decision else 5
        travelers = decision.travelers if decision else 2

        analysis = cls.calculate(
            budget_limit=budget_limit,
            duration_days=duration,
            travelers=travelers,
            flight_results=state.get("flight_results"),
            hotel_results=state.get("hotel_results"),
        )
        return {"budget_analysis": analysis}
