import openai
import instructor
from pydantic import BaseModel
from agent_ecosystem.agents.base import Agent
from agent_ecosystem.prompts.library import PROMPT_LIBRARY


class UserInfo(BaseModel):
    name: str
    age: int


def run_example():
    client = instructor.from_openai(openai.OpenAI())

    extractor = Agent(
        name="Data Extractor", system_prompt=PROMPT_LIBRARY["data_extractor"]
    )

    result = extractor.run(
        client=client,
        user_message="Jason is 25 years old.",
        response_model=UserInfo,
        model="gpt-3.5-turbo",
    )

    print(result)


if __name__ == "__main__":
    # run_example()
    pass
