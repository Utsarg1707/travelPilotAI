"""Input and Output Guardrail Schemas."""


from pydantic import BaseModel, Field


class InputGuardrailResult(BaseModel):
    """Evaluation result from Input Guardrail Node."""

    allowed: bool = Field(..., description="Whether user request is allowed to proceed")
    risk_level: str = Field("low", description="Risk assessment: 'low', 'medium', 'high'")
    reason: str = Field("", description="Reason for block or approval note")
    sanitized_query: str = Field(..., description="Cleaned, sanitized user prompt")
    detected_injection: bool = Field(False, description="Flag indicating prompt injection attempt")
    requires_clarification: bool = Field(False, description="Flag indicating underspecified intent")


class OutputGuardrailResult(BaseModel):
    """Evaluation result from Output Guardrail Node."""

    allowed: bool = Field(..., description="Whether final synthesized response passes safety & consistency checks")
    risk_level: str = Field("low", description="Risk assessment: 'low', 'medium', 'high'")
    reason: str = Field("", description="Reason for validation state")
    sanitized_response: str = Field(..., description="Cleaned output response text")
    checked_items: list[str] = Field(default_factory=list, description="Validated items (budget, schema, safety)")


class GuardrailResults(BaseModel):
    """Combined Guardrail status container."""

    input: InputGuardrailResult | None = Field(None, description="Input guardrail result")
    output: OutputGuardrailResult | None = Field(None, description="Output guardrail result")
