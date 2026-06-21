from pydantic import BaseModel, Field
from typing import Any
from agent_ecosystem.skills.base import Skill


class AgentContext(BaseModel):
    history: list[dict[str, str]] = Field(default_factory=list)
    variables: dict[str, Any] = Field(default_factory=dict)


class Agent(BaseModel):
    name: str
    system_prompt: str
    skills: list[Skill] = Field(default_factory=list)

    def run(self, client, user_message: str, response_model: type[BaseModel], **kwargs):
        """
        Runs the agent with the given client and user message, extracting the desired response model.
        """
        messages = [{"role": "system", "content": self.system_prompt}]

        # In a more advanced implementation, skills would be mapped to tools here.
        # This is a simplified version using Instructor for structured output.

        messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            messages=messages, response_model=response_model, **kwargs
        )

        return response
