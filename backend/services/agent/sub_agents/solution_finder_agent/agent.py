from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from . import prompt

class SolutionFinderAgent:
    def __init__(self, model: str):
        self.agent = Agent(
            model=LiteLlm(model=model), 
            name="solution_finder_agent",
            description="An agent that can find solutions to coding problems.",
            instruction=prompt.SOLUTION_FINDER_PROMPT,
        )