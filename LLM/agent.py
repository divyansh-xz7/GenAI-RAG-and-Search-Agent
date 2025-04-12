from langchain.agents import AgentExecutor, create_tool_calling_agent, create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from LLM.tools import tools
from LLM.llm import GROQ_LLM
from langchain import hub

prompt = hub.pull("hwchase17/react-chat")

agent = create_react_agent(GROQ_LLM, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True, max_iterations=3,)