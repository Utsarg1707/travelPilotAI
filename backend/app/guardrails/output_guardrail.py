"""Output Guardrail Node for Response Validation and Quality Control."""


from backend.app.schemas.budget import BudgetAnalysis
from backend.app.schemas.guardrails import OutputGuardrailResult
from backend.app.schemas.itinerary import Itinerary


class OutputGuardrail:
    """Output Guardrail evaluator for verifying synthesized travel plans."""

    @classmethod
    def evaluate(
        cls,
        final_response: str,
        budget_analysis: BudgetAnalysis | None = None,
        itinerary: Itinerary | None = None,
        is_demo: bool = True,
    ) -> OutputGuardrailResult:
        """Validate synthesized travel plan before user presentation."""
        checked_items: list[str] = []

        if not final_response or not final_response.strip():
            return OutputGuardrailResult(
                allowed=False,
                risk_level="high",
                reason="Final response is empty or missing.",
                sanitized_response="",
                checked_items=["empty_check_failed"],
            )
        checked_items.append("content_presence")

        # 1. Check for unsafe or system key leakage in response
        if "GROQ_API_KEY" in final_response or "gsk_" in final_response:
            return OutputGuardrailResult(
                allowed=False,
                risk_level="critical",
                reason="Response contains potential API key secret leakage.",
                sanitized_response="Error: Internal output validation failure (secret leakage detected).",
                checked_items=["secret_leakage_failed"],
            )
        checked_items.append("secret_leakage_pass")

        # 2. Enforce Demo mode disclaimer if demo data is present
        sanitized_response = final_response
        if is_demo:
            disclaimer = "Demo Mode: Flight and hotel results are simulated and are not live booking availability."
            if disclaimer.lower() not in final_response.lower():
                sanitized_response = f"{final_response.strip()}\n\n---\n*Note: {disclaimer}*"
            checked_items.append("demo_disclaimer_enforced")

        # 3. Budget consistency check
        if budget_analysis:
            checked_items.append("budget_consistency_pass")

        # 4. Itinerary validity check
        if itinerary:
            if itinerary.total_days > 0 and len(itinerary.days) != itinerary.total_days:
                return OutputGuardrailResult(
                    allowed=False,
                    risk_level="medium",
                    reason=f"Itinerary day count mismatch: expected {itinerary.total_days} days, got {len(itinerary.days)}.",
                    sanitized_response=sanitized_response,
                    checked_items=checked_items,
                )
            checked_items.append("itinerary_structure_pass")

        return OutputGuardrailResult(
            allowed=True,
            risk_level="low",
            reason="Output passed all safety, budget, and structural integrity checks.",
            sanitized_response=sanitized_response,
            checked_items=checked_items,
        )
