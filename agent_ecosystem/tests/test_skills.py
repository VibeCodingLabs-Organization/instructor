from agent_ecosystem.skills.prompt_enhancement import (
    enhance_prompt,
    prompt_enhancement_skill,
)


def test_enhance_prompt():
    original = "write code"
    enhanced = enhance_prompt(original, tone="friendly")
    assert "write code" in enhanced
    assert "friendly" in enhanced


def test_skill_execution():
    result = prompt_enhancement_skill.execute(prompt="hello", tone="professional")
    assert "professional" in result
    assert "hello" in result
