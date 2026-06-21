# Agent Ecosystem

A robust, Pydantic-driven framework for building, testing, and running AI agents and skills. This ecosystem is built as an extension on top of the [Instructor](https://python.useinstructor.com) library, leveraging structured outputs to ensure reliability and type safety in agent interactions.

---

## 🏗 Architecture

The `agent_ecosystem` is designed with modularity, extensibility, and safety in mind. It separates concerns into distinct components:

### Core Components

*   **🤖 Agents (`/agents`)**: Stateful entities that hold a system prompt, context, and a set of capabilities. They execute tasks using provided language models.
*   **🛠️ Skills (`/skills`)**: Reusable, isolated functions adhering to the `agentskills.io` design pattern. Skills map Python functions to Pydantic models for strict argument validation.
    *   *Example*: `jina-ai` RAG pipeline integration.
*   **⚡ Actions (`/actions`)**: Standardized payloads representing discrete steps an agent wants to take.
*   **🏃‍♂️ Runners (`/runners`)**: Execution engines (like `LocalRunner`) that take an action and route it to the appropriate skill or API.
*   **⚙️ Workers (`/workers`)**: Background processes that poll for tasks, utilizing runners to execute them asynchronously.
*   **🛡️ Harness (`/harness`)**: A secure execution boundary (`AgentHarness`) that wraps agent runs. It records execution history, tracks metrics, and injects API wrappers.
*   **🔌 Wrappers (`/harness/pi_ai_wrapper.py`)**: Provider-specific adapters (e.g., `PiAIWrapper` for Inflection's Pi-AI) that interface with `Instructor` to guarantee structured responses.

### Scaffolding & Support

*   **`cobras/`**: Contains boilerplate for Go-based CLI tools (e.g., `jina-cli`) used by the agent ecosystem.
*   **`prompts/` & `templates/`**: Centralized libraries for managing system instructions and rendering prompts dynamically.
*   **`examples/`**: Reference implementations demonstrating how to wire components together.
*   **`assets/` & `references/`**: Static files, schemas, Open API specs, and documentation.
*   **`tests/`**: Comprehensive `pytest` suite ensuring the reliability of the ecosystem.

---

## 🚀 Quick Start

### Prerequisites

Ensure you have the required dependencies installed (this ecosystem inherits from `Instructor`'s development environment):

```bash
# If using uv
uv pip install -e ".[dev]"
```

### Running an Agent via the Harness

The safest way to run an agent is through the `AgentHarness`. This example demonstrates how to set up the Pi-AI wrapper and execute a basic extraction agent.

```python
import instructor
import openai
from pydantic import BaseModel
from agent_ecosystem.agents.base import Agent
from agent_ecosystem.harness.pi_ai_wrapper import PiAIConfig, PiAIWrapper
from agent_ecosystem.harness.agent_harness import AgentHarness

# 1. Define the desired structured output
class UserInfo(BaseModel):
    name: str
    age: int

# 2. Configure the API Wrapper (using OpenAI as a mock backend for Pi-AI in this example)
config = PiAIConfig(api_key="your-api-key", model="gpt-4o-mini")
client = instructor.from_openai(openai.OpenAI(api_key=config.api_key))
wrapper = PiAIWrapper(config=config, client=client)

# 3. Initialize the Harness and Agent
harness = AgentHarness(wrapper=wrapper)
agent = Agent(
    name="DataExtractor",
    system_prompt="Extract user information accurately."
)

# 4. Execute
result = harness.run_agent(
    agent=agent,
    user_message="Jason is 25 years old.",
    response_model=UserInfo
)

print(f"Agent: {result.agent_name}")
print(f"Output: {result.output_data.model_dump()}")
# Output: {'name': 'Jason', 'age': 25}
```

---

## 🧪 Testing and Quality Assurance

We use `pytest` for testing and `ruff` for linting/formatting. Dedicated scripts are provided to streamline development.

Run the test suite:
```bash
./scripts/test_agent_ecosystem.sh
```

Run the linter and formatter:
```bash
./scripts/lint_agent_ecosystem.sh
```

---

## 📚 Best Practices & Industry Standards

When contributing to or utilizing the `agent_ecosystem`, please adhere to the following standards:

1.  **Pydantic First**: Every input, output, configuration, and state object must be defined as a Pydantic `BaseModel`. This provides free validation, serialization, and schema generation.
2.  **Stateless Skills**: Skills should ideally be stateless, pure functions. Side effects (like writing to a database or hitting an external API) should be managed explicitly by the Runner or an injected dependency.
3.  **Use the Harness**: Do not invoke an `Agent` directly in production. Always wrap execution in the `AgentHarness` to ensure observability, metrics tracking, and error boundaries.
4.  **Strict Typing**: Leverage Python's `typing` module extensively. Code without type hints will fail the Ruff linter.
5.  **Fail Fast**: Utilize Pydantic validators (`@field_validator`) to catch bad data *before* it reaches the LLM, saving tokens and latency.
6.  **Provider Agnosticism**: When adding new models, use the Wrapper pattern (like `PiAIWrapper`) to abstract away the specific SDK, relying on `Instructor`'s unified `from_provider` factory where possible.

---

## 📁 Jina AI RAG Pipeline Integration

This ecosystem includes scaffolding for advanced RAG (Retrieval-Augmented Generation) pipelines, specifically tailored for [Jina AI](https://jina.ai/).

Check out `agent_ecosystem/skills/rag-pipeline/jina-ai/` for:
*   OpenAPI schemas and Zod/Pydantic models.
*   Evaluation YAMLs (Positive and Negative test cases).
*   CLI wrappers written in Go (`cobras/jina-cli/`).
*   Scripts for initialization and API key validation.
