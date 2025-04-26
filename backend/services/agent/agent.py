import asyncio
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types  # For creating response content

from .sub_agents.summary_agent.agent import SummaryAgent
from .sub_agents.search_agent.agent import SearchAgent
from .sub_agents.algorithm_selector_agent.agent import AlgorithmSelectorAgent
from .sub_agents.solution_finder_agent.agent import SolutionFinderAgent

load_dotenv()

class CodeAgent:
    """
    Main agent orchestrator that coordinates sub-agents to solve coding problems.
    This agent utilizes Google's Agent Development Kit (ADK) to manage and delegate tasks
    between specialized sub-agents.
    """

    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.model = model

        # Initialize sub-agents
        self.summary_agent = SummaryAgent(model=self.model)
        self.search_agent = SearchAgent(model=self.model)
        self.algorithm_selector_agent = AlgorithmSelectorAgent(model=self.model)
        self.solution_finder_agent = SolutionFinderAgent(model=self.model)

        # Initialize main orchestrator agent
        self.orchestrator = self._create_orchestrator()

    def _create_orchestrator(self):
        """Creates the main agent orchestrator with access to all sub-agents."""
        main_agent = Agent(
            model=LiteLlm(model=self.model),
            name="code_agent_orchestrator",
            description="Orchestrates specialized sub-agents to solve coding problems",
            instruction=""" 
            You are a code generation assistant that helps users solve coding problems.
            
            Follow this EXACT workflow for handling user requests:
            
            1. **SEARCH STEP**: 
                When a user submits a coding problem, use the `search_code_agent` to search for an exact match in the database or web.
                If an exact match is found, return that solution immediately. 
                Ensure you remove all comments from the code before returning it.
            
            2. **PROBLEM UNDERSTANDING**: 
                If no exact solution was found in the search step, use the `summary_agent` to analyze and summarize the problem statement.
            
            3. **ALGORITHM SELECTION**: 
                After the problem has been summarized, use the `algorithm_selector_agent` to determine the most appropriate algorithm for the problem.
            
            4. **SOLUTION GENERATION**: 
                After selecting the algorithm, use the `solution_finder_agent` to generate the final code solution.
                Ensure the solution is based on both the problem summary and the selected algorithm. 
                The generated code must NOT contain any comments.
            
            **CODE STYLE REQUIREMENTS**:
            - Generated code must be clean and efficient without comments.
            - Use descriptive variable and function names to avoid needing comments.
            
            **LANGUAGE PREFERENCE**:
            - Default to C++ if the user does not specify a programming language.
            - All sub-agents are instructed to use C++ unless otherwise specified by the user.
            
            **SEARCH STRATEGY**:
            - Formulate precise queries that capture the exact problem when performing a search.
            """,
            sub_agents=[
                self.search_agent.agent, 
                self.summary_agent.agent, 
                self.algorithm_selector_agent.agent, 
                self.solution_finder_agent.agent
            ],
        )
    
        return main_agent

    async def solve_problem(self, problem_statement: str, context: dict = None) -> str:
        """
        Solve a coding problem and return the solution code as a string.
        """
        if context is None:
            context = {}
        if "language" not in context:
            context["language"] = "C++"
        context["code_style"] = {
            "include_comments": False,
            "descriptive_names": True
        }

        session_service = InMemorySessionService()

        # Create session
        session = session_service.create_session(
            app_name="code_agent_app",
            user_id="user_1",
            session_id="session_001"
        )
        
        # Create runner
        runner = Runner(agent=self.orchestrator, 
                        session_service=session_service,
                        app_name="code_agent_app",
                        )

        # Send and await response, only take final event
        final_response = "No response from agent."

        content = types.Content(role='user', parts=[types.Part(text=problem_statement)])

        async for event in runner.run_async(
            user_id="user_1",
            session_id="session_001",
            new_message=content,
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response = event.content.parts[0].text
                break

        return final_response
