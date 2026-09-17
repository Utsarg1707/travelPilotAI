"""Input Guardrail Node and Prompt Injection Protection."""

import re

from backend.app.schemas.guardrails import InputGuardrailResult

# Known prompt injection & jailbreak patterns
PROMPT_INJECTION_PATTERNS: list[re.Pattern] = [
    re.compile(r"ignore\s+(all\s+)?(previous|above|prior)\s+instructions?", re.IGNORECASE),
    re.compile(r"forget\s+(all\s+)?(your\s+)?(system\s+)?rules?", re.IGNORECASE),
    re.compile(r"you\s+are\s+now\s+a\s+", re.IGNORECASE),
    re.compile(r"system\s*:\s*", re.IGNORECASE),
    re.compile(r"<\s*system\s*>", re.IGNORECASE),
    re.compile(r"\[\s*system\s*\]", re.IGNORECASE),
    re.compile(r"override\s+safety\s+filter", re.IGNORECASE),
    re.compile(r"developer\s+mode\s+enabled", re.IGNORECASE),
    re.compile(r"jailbreak", re.IGNORECASE),
    re.compile(r"DAN\s+mode", re.IGNORECASE),
    re.compile(r"execute\s+code", re.IGNORECASE),
    re.compile(r"eval\s*\(", re.IGNORECASE),
    re.compile(r"exec\s*\(", re.IGNORECASE),
    re.compile(r"DROP\s+TABLE", re.IGNORECASE),
]

# Keywords indicating travel relevance
TRAVEL_KEYWORDS: list[str] = [
    "trip", "travel", "flight", "hotel", "visit", "vacation", "holiday",
    "itinerary", "stay", "resort", "fly", "weather", "budget", "tour",
    "destination", "attraction", "beach", "city", "explore", "booking",
    "places", "days", "lake", "mountain", "dubai", "bangalore", "paris",
    "tokyo", "singapore", "goa", "london", "rome", "bali", "thailand",
]


class InputGuardrail:
    """Input Guardrail evaluator for safety, scope, and prompt injection defense."""

    @classmethod
    def evaluate(cls, user_query: str) -> InputGuardrailResult:
        """Evaluate raw user input query against deterministic guardrail rules."""
        if not user_query or not user_query.strip():
            return InputGuardrailResult(
                allowed=False,
                risk_level="high",
                reason="User query is empty or whitespace only.",
                sanitized_query="",
                detected_injection=False,
                requires_clarification=True,
            )

        sanitized_query = cls._sanitize(user_query)

        # 1. Check for prompt injection
        has_injection, injection_pattern = cls._detect_prompt_injection(sanitized_query)
        if has_injection:
            return InputGuardrailResult(
                allowed=False,
                risk_level="critical",
                reason=f"Prompt injection attempt detected matching pattern: {injection_pattern}",
                sanitized_query=sanitized_query,
                detected_injection=True,
                requires_clarification=False,
            )

        # 2. Check travel scope relevance
        is_travel, relevance_reason = cls._check_travel_relevance(sanitized_query)
        if not is_travel:
            return InputGuardrailResult(
                allowed=False,
                risk_level="medium",
                reason=relevance_reason,
                sanitized_query=sanitized_query,
                detected_injection=False,
                requires_clarification=False,
            )

        # 3. Check query length and clarity
        if len(sanitized_query) < 4:
            return InputGuardrailResult(
                allowed=False,
                risk_level="low",
                reason="Query is too short to extract travel requirements.",
                sanitized_query=sanitized_query,
                detected_injection=False,
                requires_clarification=True,
            )

        return InputGuardrailResult(
            allowed=True,
            risk_level="low",
            reason="Query validated successfully. Safe travel request.",
            sanitized_query=sanitized_query,
            detected_injection=False,
            requires_clarification=False,
        )

    @staticmethod
    def _sanitize(query: str) -> str:
        """Sanitize control characters and excess spaces."""
        # Strip zero-width / non-printable characters except standard whitespace
        cleaned = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]", "", query)
        # Normalize whitespace
        return " ".join(cleaned.split()).strip()

    @classmethod
    def _detect_prompt_injection(cls, query: str) -> tuple[bool, str]:
        """Detect prompt manipulation or system override syntax."""
        for pattern in PROMPT_INJECTION_PATTERNS:
            if pattern.search(query):
                return True, pattern.pattern
        return False, ""

    @classmethod
    def _check_travel_relevance(cls, query: str) -> tuple[bool, str]:
        """Verify if request is within travel planning domain."""
        query_lower = query.lower()
        # Direct keyword match or generic travel query structure
        if any(keyword in query_lower for keyword in TRAVEL_KEYWORDS):
            return True, "Travel keyword matched"

        # Heuristic check for city-to-city or days pattern (e.g., "5 days in Rome", "from A to B")
        if re.search(r"\b\d+\s*days?\b", query_lower) or re.search(r"\bfrom\s+\w+\s+to\s+\w+\b", query_lower):
            return True, "Travel pattern matched"

        return False, "Request does not appear to be travel-related. Please ask a travel or trip-planning question."
