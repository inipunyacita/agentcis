import os
from openai import OpenAI
from phi.agent import Agent
from phi.model.xai import xAI
from phi.tools.googlesearch import GoogleSearch
from phi.tools.yfinance import YFinanceTools

# API keys (replace with your actual keys if different)
os.environ['OPENAI_API_KEY']='xai-YJsj80sT17xQSiWnfQnvQCNfDVF47BdPqUjS37f9dxEyPsspMHvhfsRcmkZY9s2l0Q19FxPBGqqS4a7T'
# TELEGRAM_TOKEN = '7350103114:AAE16Xns7k9UDSQTeWbr0QrgsI0857hyxu8'

# AI Agent setup (optional, can be integrated into the bot later if desired)
sentiment_agent = Agent(
    name="Sentiment Agent",
    role="Search and interpret news articles",
    model=xAI(id="grok-beta"),
    tools=[GoogleSearch()],
    instructions=[
        "Find relevant news about macro economy that related with cryptocurrency and affected to cryptocurrency",
        "Find relevant news about Bitcoin",
        "Find relevant news about high-risk assets recently",
    ],
    markdown=True,
    show_tool_calls=True,
)

coin_search_agent = Agent(
    name="Project Research Agent",
    role="Project Info",
    model=xAI(id="grok-beta"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=False, company_news=True)]
)

agent_team = Agent(
    model=xAI(id="grok-beta"),
    team=[sentiment_agent, coin_search_agent],
    instructions=[
        "Combine the expertise from all agents to provide a cohesive, well-supported, and critical response"
    ],
    show_tool_calls=True,
    markdown=True,
)

agent_team.print_response(
    "Analyze the current (up to date) sentiment & news of market based on current data that Sentiment Agent & Project Research Agent already research related to Bitcoin. \n \n"
    "1. **Give the comprehensive analysis with price prediction and any upcoming events relate to the bitcoin"
    "Ensure your response is accurate, comprehensive, and comes with financial data",
    stream=True
)


