import os
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
import psycopg2
from langchain.tools.retriever import create_retriever_tool
from langchain_community.utilities import SerpAPIWrapper
from langchain.agents import load_tools
from langchain.tools import StructuredTool, tool
from LLM.store import vectorstore
from LLM.llm import GROQ_LLM


os.environ['SERPAPI_API_KEY'] = 'your key'


tools=[]
serpapi = SerpAPIWrapper()

@tool
def search(query:str):
    """Use when you dont know about something or want to search about current events"""
    return serpapi.run(query)


db = SQLDatabase.from_uri("postgresql://postgres:postgres@localhost:5432/fastapidb")
toolkit = SQLDatabaseToolkit(db=db, llm=GROQ_LLM)
sql = create_sql_agent(llm=GROQ_LLM, toolkit=toolkit, verbose=True)

def sql_method(query):
    response = sql.invoke(query)
    return response

sql_tool = StructuredTool.from_function(
    func=sql_method,
    name="sql_tool",
    description="Database retriever tool, helps you to answer questions regarding lego, such as lego parts, lego themes, lego colors, lego inventory , etc",
)

retriever = vectorstore.as_retriever()
retrieverTool = create_retriever_tool(
    retriever,
    "DocumentsKnowledge",
    "Search for information about topic cricket",
)

@tool
def llm_tool(query:str):
    """Use only if you are already familiar with topic, answer general questions which can be answered by llm, or use this to add additional information"""
    return GROQ_LLM.invoke(query)

tools.append(llm_tool)
tools.append(retrieverTool)
tools.append(search)
tools.append(sql_tool)