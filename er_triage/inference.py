# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
Inference script for the ER Triage Environment.

This script demonstrates how a Large Language Model (LLM) agent can play
the ER Triage game. It defines a simple rule-based agent that mimics
the decision-making process of an LLM.

To run this script:
1. Make sure the ER Triage server is running:
   python -m er_triage.server.app
2. Run this script in a separate terminal:
   python -m er_triage.inference
"""

import argparse
import random

# Use a try-except block for robust imports
try:
    from .client import ERTriageEnv
    from .models import ERTriageAction, ERTriageObservation
except ImportError:
    # This path is for direct execution
    from client import ERTriageEnv
    from models import ERTriageAction, ERTriageObservation


class SimpleRuleBasedAgent:
    """
    A simple, rule-based agent that simulates an LLM's decision-making.

    A real implementation would replace the `decide_action` method with calls
    to an actual LLM, providing the observation as context and parsing the
    LLM's output to construct an ERTriageAction.
    """

    def decide_action(self, obs: ERTriageObservation) -> ERTriageAction:
        """
        Decides the next action based on a simple set of rules.

        Args:
            obs: The current observation from the environment.

        Returns:
            The action to take.
        """
        reasoning = "The agent is making a decision based on the available information."

        # Rule 1: If vitals are available, assess them.
        if obs.vitals:
            # Simple heuristic: if heart rate is high or SpO2 is low, it's critical.
            if obs.vitals.get("hr", 0) > 100 or obs.vitals.get("spo2", 100) < 94:
                reasoning = "Vitals are abnormal (high HR or low SpO2), assigning critical priority."
                return ERTriageAction(action_type="assign_priority", priority="critical", reasoning=reasoning)
            else:
                reasoning = "Vitals seem stable, assigning non-urgent priority."
                return ERTriageAction(action_type="assign_priority", priority="non-urgent", reasoning=reasoning)

        # Rule 2: If no vitals, request them.
        if "request_vitals" in obs.available_actions:
            reasoning = "Vitals are not available, requesting them for a better assessment."
            return ERTriageAction(action_type="request_vitals", reasoning=reasoning)

        # Rule 3: Fallback - if vitals can't be requested, make a guess.
        reasoning = "Cannot get more information, making a guess based on chief complaint."
        priority = random.choice(["critical", "urgent", "non-urgent"])
        return ERTriageAction(action_type="assign_priority", priority=priority, reasoning=reasoning)


def main(base_url: str):
    """
    Runs a full episode of the ER Triage environment with the agent.

    Args:
        base_url: The URL of the running environment server.
    """
    agent = SimpleRuleBasedAgent()
    print(f"Connecting to environment at {base_url}...")

    try:
        # Use client.sync() for synchronous code
        with ERTriageEnv(base_url=base_url).sync() as client:
            print("Connection successful. Starting new episode...")
            result = client.reset()
            obs = result.observation
            done = result.done
            total_reward = 0

            print(f"\n--- Patient 1 ---")
            print(f"Chief Complaint: {obs.chief_complaint}")

            while not done:
                # 1. Agent decides on an action
                action = agent.decide_action(obs)
                print(f"\nAgent Action: {action.action_type}")
                if action.action_type == "assign_priority":
                    print(f"  -> Priority: {action.priority}")
                print(f"Agent Reasoning: {action.reasoning}")

                # 2. Environment executes the action
                result = client.step(action)
                obs = result.observation
                done = result.done
                total_reward += result.reward

                # 3. Print the outcome
                print(f"\nEnvironment Observation:")
                if obs.vitals:
                    print(f"  -> Vitals: {obs.vitals}")
                if obs.question_answer:
                    print(f"  -> Answer: {obs.question_answer}")
                print(f"Reward for this step: {result.reward}")
                print(f"Is episode finished? {done}")

            print("\n--- Episode Finished ---")
            print(f"Total Reward: {total_reward}")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please ensure the ER Triage server is running.")
        print("You can start it with: uvicorn er_triage.server.app:app --reload")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run inference on the ER Triage environment.")
    parser.add_argument(
        "--base-url",
        type=str,
        default="http://localhost:8000",
        help="URL of the environment server.",
    )
    args = parser.parse_args()
    main(base_url=args.base_url)