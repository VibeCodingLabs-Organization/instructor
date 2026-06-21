from pydantic import BaseModel
from agent_ecosystem.agents.base import Agent


class FakeClient:
    class Chat:
        class Completions:
            def create(self, **kwargs):
                return kwargs.get("response_model")(name="Test", age=30)

        completions = Completions()

    chat = Chat()


class User(BaseModel):
    name: str
    age: int


def test_agent_run():
    agent = Agent(name="TestAgent", system_prompt="You are a test agent.")
    client = FakeClient()
    result = agent.run(client, "test message", response_model=User)
    assert result.name == "Test"
    assert result.age == 30
