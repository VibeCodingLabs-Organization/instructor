def render_agent_prompt(role: str, objective: str, constraints: list[str]) -> str:
    prompt = f"You are a {role}. Your objective is: {objective}.\n\nConstraints:\n"
    for constraint in constraints:
        prompt += f"- {constraint}\n"
    return prompt
