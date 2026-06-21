from agent_ecosystem.runners.local_runner import LocalRunner
from agent_ecosystem.actions.base import Action


class DummyAction(Action):
    name: str = "dummy"
    description: str = "Dummy action"

    def execute(self, payload):
        return payload.get("value", 0) + 1


def test_local_runner():
    runner = LocalRunner()
    action = DummyAction()
    runner.register_action(action)

    result = runner.run("dummy", {"value": 5})
    assert result == 6
