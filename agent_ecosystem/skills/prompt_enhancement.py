from pydantic import BaseModel, Field
from agent_ecosystem.skills.base import create_skill


class PromptEnhancementArgs(BaseModel):
    prompt: str = Field(..., description="The original prompt to be enhanced")
    context: str = Field(
        "", description="Optional context to include in the enhancement"
    )
    tone: str = Field("professional", description="The desired tone of the prompt")


def enhance_prompt(prompt: str, context: str = "", tone: str = "professional") -> str:
    """
    Enhances a prompt to be more clear, detailed, and actionable for an AI agent.
    """
    enhancement = (
        f"Act as a prompt engineer. Enhance the following prompt with a {tone} tone"
    )
    if context:
        enhancement += f" using this context: {context}"
    enhancement += f".\n\nOriginal prompt: {prompt}"

    return enhancement


prompt_enhancement_skill = create_skill(enhance_prompt, PromptEnhancementArgs)
