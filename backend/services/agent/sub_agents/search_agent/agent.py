from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from . import prompt
from ...tools.search_db import SearchDBTool
from ...tools.search_web import SearchWebTool

class SearchAgent:
    def __init__(self, model: str):
        # Create instances of the search tools
        self.db_tool = SearchDBTool()
        self.web_tool = SearchWebTool()
        
        self.agent = Agent(
            model=LiteLlm(model=model), 
            name="search_code_agent",
            description="A search agent that can search the web and databases for coding solution.",
            instruction=prompt.SEARCH_AGENT_PROMPT,
            tools=[self.db_tool.search, self.web_tool.search],
        )
