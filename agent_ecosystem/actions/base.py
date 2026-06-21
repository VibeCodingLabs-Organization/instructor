from pydantic import BaseModel
from typing import Any


class Action(BaseModel):
    name: str
    description: str

    def execute(self, payload: dict[str, Any]) -> Any:
        raise NotImplementedError
