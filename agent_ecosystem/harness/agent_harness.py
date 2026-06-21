from pydantic import BaseModel, Field
from typing import Any
from agent_ecosystem.agents.base import Agent
from agent_ecosystem.harness.pi_ai_wrapper import PiAIWrapper


class HarnessExecutionResult(BaseModel):
    agent_name: str
    input_message: str
    output_data: Any
    metrics: dict[str, Any] = Field(default_factory=dict)


class AgentHarness:
    """
    A harness for managing and executing agents safely with a specific AI wrapper.
    It intercepts execution to inject tools, monitor history, and record metrics.
    """

    def __init__(self, wrapper: PiAIWrapper):
        self.wrapper = wrapper
        self.history: list[HarnessExecutionResult] = []

    def run_agent(
        self, agent: Agent, user_message: str, response_model: type[BaseModel], **kwargs
    ) -> HarnessExecutionResult:
        """
        Runs the specified agent inside the harness.
        """
        # Pre-execution hooks (e.g., logging, metric start)
        print(f"[Harness] Starting execution for agent: {agent.name}")

        messages = [{"role": "system", "content": agent.system_prompt}]
        messages.append({"role": "user", "content": user_message})

        # Execute using the injected wrapper
        output = self.wrapper.chat_completion(
            messages=messages, response_model=response_model, **kwargs
        )

        # Post-execution hooks (e.g., store result, calculate metrics)
        result = HarnessExecutionResult(
            agent_name=agent.name,
            input_message=user_message,
            output_data=output,
            metrics={"status": "success"},  # Placeholder for real metrics
        )

        self.history.append(result)
        print(f"[Harness] Finished execution for agent: {agent.name}")

        return result
