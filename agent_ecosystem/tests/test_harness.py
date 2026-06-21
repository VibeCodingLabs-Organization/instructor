from pydantic import BaseModel
from agent_ecosystem.harness.pi_ai_wrapper import PiAIConfig, PiAIWrapper
from agent_ecosystem.harness.agent_harness import AgentHarness
from agent_ecosystem.agents.base import Agent


class DummyResponseModel(BaseModel):
    result: str


class FakeClient:
    class Chat:
        class Completions:
            def create(self, **kwargs):
                return kwargs.get("response_model")(result="Success")

        completions = Completions()

    chat = Chat()


def test_pi_ai_wrapper():
    config = PiAIConfig(api_key="test-key")
    wrapper = PiAIWrapper(config=config, client=FakeClient())

    response = wrapper.chat_completion(
        messages=[{"role": "user", "content": "hello"}],
        response_model=DummyResponseModel,
    )

    assert response.result == "Success"


def test_agent_harness():
    config = PiAIConfig(api_key="test-key")
    wrapper = PiAIWrapper(config=config, client=FakeClient())
    harness = AgentHarness(wrapper=wrapper)

    agent = Agent(name="TestAgent", system_prompt="You are a test agent.")

    execution_result = harness.run_agent(
        agent=agent, user_message="Do something", response_model=DummyResponseModel
    )

    assert execution_result.agent_name == "TestAgent"
    assert execution_result.output_data.result == "Success"
    assert len(harness.history) == 1
