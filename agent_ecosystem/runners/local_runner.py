from typing import Any
from agent_ecosystem.actions.base import Action


class LocalRunner:
    def __init__(self):
        self.actions: dict[str, Action] = {}

    def register_action(self, action: Action):
        self.actions[action.name] = action

    def run(self, action_name: str, payload: dict[str, Any]) -> Any:
        if action_name not in self.actions:
            raise ValueError(f"Action {action_name} not found")
        return self.actions[action_name].execute(payload)
