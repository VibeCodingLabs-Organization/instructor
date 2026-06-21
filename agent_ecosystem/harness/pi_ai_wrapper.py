from pydantic import BaseModel, Field
from typing import Any
import instructor


class PiAIConfig(BaseModel):
    api_key: str = Field(..., description="API key for Pi-AI / Inflection")
    model: str = Field("pi-base-v1", description="Model to use")
    temperature: float = Field(0.7, description="Sampling temperature")


class PiAIWrapper:
    """
    A wrapper class to interface with Pi-AI (Inflection AI) or a compatible API.
    Provides structured outputs utilizing instructor.
    """

    def __init__(self, config: PiAIConfig, client: Any = None):
        self.config = config
        self.client = client  # E.g., instructor.from_openai(openai.OpenAI(base_url="...", api_key="..."))

        # If no client is provided, we assume the user will pass a patched instructor client
        if self.client is None:
            # Fallback or stub logic
            import openai

            # Example using a custom base URL if Pi-AI had an OpenAI-compatible endpoint
            self.client = instructor.from_openai(
                openai.OpenAI(api_key=self.config.api_key)
            )

    def chat_completion(
        self, messages: list[dict[str, str]], response_model: type[BaseModel], **kwargs
    ) -> Any:
        """
        Sends a chat completion request using the wrapper's client and configuration.
        """
        # Merge configuration defaults with provided kwargs
        request_kwargs = {
            "model": self.config.model,
            "temperature": self.config.temperature,
        }
        request_kwargs.update(kwargs)

        response = self.client.chat.completions.create(
            messages=messages, response_model=response_model, **request_kwargs
        )
        return response
