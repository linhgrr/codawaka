from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from . import prompt

class SummaryAgent:
    def __init__(self, model: str):
        self.agent = Agent(
            model=LiteLlm(model=model), 
            name="summary_agent",
            description="An agent capable of summarizing coding problems.",
            instruction=prompt.SUMMARY_AGENT_PROMPT,
        )