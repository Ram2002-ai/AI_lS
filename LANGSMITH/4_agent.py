from dotenv import load_dotenv
import os
import requests

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_agent

load_dotenv()

search_tool = DuckDuckGoSearchRun()


@tool
def get_weather_data(city: str) -> str:
    """Get current weather for a city."""

    url = f"https://api.weatherstack.com/current?access_key=f07d9636974c4120025fadf60678771b&query={city}"

    response = requests.get(url)

    return str(response.json())


llm = ChatOpenAI(
    model="openai/gpt-oss-20b",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
)

agent = create_agent(
    model=llm,
    tools=[search_tool, get_weather_data],
)

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is the release date of Dhadak 2?"
            }
        ]
    }
)

print(response)

# print(response['output'])