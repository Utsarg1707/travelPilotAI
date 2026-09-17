"""Agent Benchmark Evaluator."""

import json
from typing import Any, Dict, List
from backend.app.graph import create_travel_graph
from backend.app.schemas.travel_state import TravelState


class AgentEvaluator:
    """Evaluates agent performance across benchmark test scenarios."""

    @classmethod
    def evaluate_scenario(cls, item: Dict[str, Any]) -> Dict[str, Any]:
        """Run single evaluation scenario through LangGraph state machine."""
        query = item["query"]
        graph = create_travel_graph(with_checkpointer=False)
        initial_state: TravelState = {"user_query": query}

        res = graph.invoke(initial_state)

        input_guard = res.get("input_guardrail")
        is_allowed = input_guard.allowed if input_guard else False
        decision = res.get("supervisor_decision")
        selected_agents = decision.required_agents if decision else []

        passed = True
        notes: List[str] = []

        # 1. Guardrail evaluation
        if "expected_allowed" in item:
            if is_allowed != item["expected_allowed"]:
                passed = False
                notes.append(f"Guardrail allowed mismatch: expected {item['expected_allowed']}, got {is_allowed}")

        if item.get("expected_injection"):
            if not input_guard or not input_guard.detected_injection:
                passed = False
                notes.append("Expected prompt injection detection failed")

        # 2. Routing evaluation
        if is_allowed and "expected_agents" in item:
            if set(selected_agents) != set(item["expected_agents"]):
                passed = False
                notes.append(f"Routing mismatch: expected {item['expected_agents']}, got {selected_agents}")

        return {
            "id": item["id"],
            "scenario": item["scenario"],
            "passed": passed,
            "notes": notes or ["Passed all metrics"],
            "selected_agents": selected_agents,
            "allowed": is_allowed,
        }

    @classmethod
    def run_suite(cls, dataset_path: str) -> Dict[str, Any]:
        """Run full evaluation suite from JSON dataset."""
        with open(dataset_path, "r", encoding="utf-8") as f:
            dataset = json.load(f)

        results = [cls.evaluate_scenario(item) for item in dataset]
        total = len(results)
        passed = sum(1 for r in results if r["passed"])
        accuracy = (passed / total) * 100.0 if total > 0 else 0.0

        return {
            "total_scenarios": total,
            "passed_scenarios": passed,
            "failed_scenarios": total - passed,
            "accuracy_percentage": round(accuracy, 2),
            "results": results,
        }
