from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from . import prompt

class AlgorithmSelectorAgent:
    def __init__(self, model: str):
        self.agent = Agent(
            model=LiteLlm(model=model), 
            name="algorithm_selector_agent",
            description="A agent that can select most suitable algorithm for provided problemproblem.",
            instruction=prompt.ALGORITHM_SELECTOR_PROMPT,
        )