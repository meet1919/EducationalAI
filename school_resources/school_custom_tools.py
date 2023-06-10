from langchain.callbacks.manager import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun
from langchain.utilities import SerpAPIWrapper
from school_staff.tutor import ScienceTutor, CommerceTutor
from langchain.chat_models import ChatOpenAI
from langchain.utilities import PythonREPL
from langchain.tools import BaseTool
from langchain.agents import Tool
from school_staff.python_programmer import PythonProgrammer
from typing import Optional

class ScienceProfessorRouterTool(BaseTool):
    name = 'science professor router'
    description = 'useful when you need to answer academics question related to science stream.'
    # return_direct = True
    llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.9)

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """ Choose which professor to call to answer the user query with router chains """
        science_tutor = ScienceTutor()
        answer = science_tutor.assist_with(query)
        return answer
        
    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
    
class CommerceProfessorRouterTool(BaseTool):
    name = 'commerce professor router'
    description = 'useful when you need to answer academics question related to commerce stream.'
    # return_direct = True
    llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.9)

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """ Choose which professor to call to answer the user query with router chains """
        commerce_tutor = CommerceTutor()
        answer = commerce_tutor.assist_with(query)
        return answer
        
    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
    
class PythonExecutorTool(BaseTool):
    name = 'python_exec'
    description = 'useful when you need to answer academics question related to commerce stream.'
    return_direct = True
    llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.9)
    
    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """ Choose which professor to call to answer the user query with router chains """
        python_executor = PythonProgrammer()
        answer = python_executor.solve(query)
        return answer
        
    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
    
def define_tools():
    python_repl = PythonREPL()
    internet_search = SerpAPIWrapper()
    tools = [
        ScienceProfessorRouterTool(),
        CommerceProfessorRouterTool(),
        PythonExecutorTool(),
        Tool(
            name="internet_search",
            description='Useful when you need current/latest data on the internet',
            func=internet_search.run
        )

    ]

    return tools