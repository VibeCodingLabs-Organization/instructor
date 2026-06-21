import inspect
from pydantic import BaseModel
from typing import Any, Callable


class Skill(BaseModel):
    name: str
    description: str
    parameters: type[BaseModel]

    def execute(self, **kwargs: Any) -> Any:
        raise NotImplementedError("Skill must implement execute method")


def create_skill(func: Callable[..., Any], model: type[BaseModel]) -> Skill:
    """
    Creates a Skill from a Python function and a Pydantic model representing its arguments.
    """
    docstring = inspect.getdoc(func) or "No description provided."
    name = func.__name__

    class CustomSkill(Skill):
        def execute(self, **kwargs: Any) -> Any:
            return func(**kwargs)

    return CustomSkill(name=name, description=docstring, parameters=model)
