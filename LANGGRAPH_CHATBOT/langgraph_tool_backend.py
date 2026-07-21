# backend.py
from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage,HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode,tools_condition
from langchain_community.tools import DuckDuckGoSearchRun,ArxivQueryRun,StackExchangeTool
from langchain_core.tools import tool
from dotenv import load_dotenv
import sqlite3
import os
import requests

load_dotenv()

# ========================= 1.LLM ===============
llm=ChatOpenAI(
    model="openai/gpt-oss-20b",   # Must support structured outputs
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

# ======================== 2.TOOLS ===================
# tools
search_tool=DuckDuckGoSearchRun(region="us-en")
research_tool=ArxivQueryRun()
stack_tool=StackExchangeTool()

@tool
def calculator(first_num:float,second_num:float,operation:str)->dict:
    """
    Perform a basic arithmetic operation on two numbers.
    Supported operations:add,sub,mul,div
    """

    try:
        if operation=='add':
            return first_num+second_num
        elif operation=='sub':
            return first_num-second_num
        elif operation=='mul':
            return first_num*second_num
        elif operation=='div':
            if second_num==0:
                return{'error':'Division by zero is not allowed'}
            result=first_num/second_num
        else:
            return{'error':f"Unsupported operation '{operation}'"}
        
        return {'first_num':first_num,'second_num':second_num,'operation':operation,'result':result}
    
    except Exception as e:
        return{'error':str(e)}
    
@tool 
def get_stock_price(symbol:str)->dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL','TSLA')
    using Alpha Ventage with API key in the URL.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=C9PE94QUEW9VWGFM"
    r=requests.get(url)
    return r.json()

tools=[search_tool,research_tool,stack_tool,calculator,get_stock_price]
llm_with_tools=llm.bind_tools(tools)


# STATE
class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

# Nodes

def chat_node(state:ChatState):
    """LLM node that may answer or request a tool call."""

    messages=state['messages']
    response=llm_with_tools.invoke(messages)
    return {"messages":[response]}

tool_node=ToolNode(tools)

# 5.Checkpointer
conn=sqlite3.connect(database='chatbot.db',check_same_thread=False)
checkpointer=SqlieSaver(conn=conn)

# 6.Graph
graph=StateGraph(ChatState)

graph.add_node('chat_node',chat_node)
graph.add_node('tools',tool_node)

graph.add_edge(START,'chat_node')
graph.add_conditional_edges('chat_node',tools_condition)
graph.add_edge('tools','chat_node')

chatbot=graph.compile(checkpointer=checkpointer)

# 7. Helper
def retrieve_all_threads():
    all_threads=set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpointer.config['configurable']['thread_id'])

    return list(all_threads)
