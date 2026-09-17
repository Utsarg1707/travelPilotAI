"""Evaluation Runner CLI Script."""

import os
import sys

# Ensure backend package is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from evaluation.evaluators.agent_evaluator import AgentEvaluator


def main():
    dataset_path = os.path.join(os.path.dirname(__file__), "datasets", "benchmark_dataset.json")
    print("=" * 60)
    print("      TRAVELPILOT AI — AGENT EVALUATION BENCHMARK SUITE")
    print("=" * 60)
    print(f"Loading evaluation dataset: {dataset_path}...\n")

    summary = AgentEvaluator.run_suite(dataset_path)

    print(f"Total Scenarios Tested : {summary['total_scenarios']}")
    print(f"Passed Scenarios       : {summary['passed_scenarios']}")
    print(f"Failed Scenarios       : {summary['failed_scenarios']}")
    print(f"Accuracy Score         : {summary['accuracy_percentage']}%\n")

    print("Detailed Scenario Results:")
    print("-" * 60)
    for r in summary["results"]:
        status = "PASSED" if r["passed"] else "FAILED"
        symbol = "PASS" if r["passed"] else "FAIL"
        print(f"[{symbol}] #{r['id']} {r['scenario']}")

        if not r["passed"]:
            print(f"    Notes: {', '.join(r['notes'])}")
    print("=" * 60)


if __name__ == "__main__":
    main()
