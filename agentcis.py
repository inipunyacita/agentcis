import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from phi.agent import Agent
from openai import OpenAI
from phi.agent import Agent
from phi.model.xai import xAI
from phi.tools.googlesearch import GoogleSearch
from phi.tools.yfinance import YFinanceTools
from fetch_latest_news import get_latest_news

news_data = get_latest_news()

# Set environment variables
TELEGRAM_BOT_TOKEN = "7350103114:AAE16Xns7k9UDSQTeWbr0QrgsI0857hyxu8"

# API keys (replace with your actual keys if different)
os.environ['OPENAI_API_KEY']='xai-f30jxq5aSEHJIUaB0o3Lrj7iYlBhg3sUaHJ6dxVr1aaCrxN2YbVZGhOWVz0iZXLzOZwYXxRlxmrNeCB7'
# TELEGRAM_TOKEN = '7350103114:AAE16Xns7k9UDSQTeWbr0QrgsI0857hyxu8'

# Format for the agent
formatted_news = "\n\n".join([
    f"- {item['data_time']} | {item['title']} | Actual: {item['actual']}, Forecast: {item['forecast']}, Previous: {item['previous']}"
    for item in news_data
])

# AI Agent setup (optional, can be integrated into the bot later if desired)
# sentiment_agent = Agent(
#     name="Sentiment Agent",
#     role="Search and interpret news articles",
#     model=xAI(id="grok-3-fast"),
#     tools=[GoogleSearch()],
#     instructions=[
#         "Find relevant news about macro economy that related with cryptocurrency and affected to cryptocurrency or risk on assets",
#         "Find relevant news about geopolitical tension",
#         "Find relevant news about high-risk assets recently",
#     ],
#     markdown=True,
#     show_tool_calls=True,
# )

# Format instructions cleanly
instructions_text = f"""
You are provided with the latest macroeconomic news scraped from FinancialJuice.
Use the data to analyze sentiment, predict short-term and long-term impacts on Bitcoin, crypto markets, and risk-on assets.
Consider the differences between actual and forecast values to identify surprising shifts.
Base your outlook strictly on the data provided below.

### NEWS DATA ###
{formatted_news}

Now summarize the macroeconomic outlook, risks, and price impact.
"""

# Pass this as a single string in the instructions list
sentiment_by_financialjuices_agent = Agent(
    name="Financial Juice Agent",
    role="Analyze FinancialJuice macroeconomic news and predict crypto impact",
    model=xAI(id="grok-3-fast"),
    instructions=[instructions_text],
    markdown=True,
    show_tool_calls=True,
)



# coin_search_agent = Agent(
#     name="Project Research Agent",
#     role="Project Info",
#     model=xAI(id="grok-3-fast"),
#     tools=[YFinanceTools(stock_price=True, analyst_recommendations=False, company_news=True)],
#     instructions=[
#         "Find bitcoin fundamental, underlying, prospect, and current sentiment",
#         "Find relevant news about Bitcoin",
#         "Find relevant news about high-risk assets recently",
#     ],
# )

agent_team = Agent(
    model=xAI(id="grok-3-fast"),
    team=[
        sentiment_by_financialjuices_agent,
    ],
    instructions=[
        "Given a cryptocurrency ticker (e.g., BTC, ETH, SOL), analyze its recent performance and give an outlook.",
        "use all data in sentiment_by_financialjuices_agent to analyze current macro economy situation", 
        "based on sentiment_by_financialjuices_agent data, combine and find all corelated data and do analyze ",
        
    ],
    markdown=True,
    # show_tool_calls=True,
)


# agent_team.print_response(
#     "Analyze the current (up to date) sentiment & news of market based on current data that sentiment_agent & sentiment_by_financialjuices_agent give that can affected to Bitcoin Price. \n \n"
#     "Ensure your response is accurate, comprehensive, and comes with financial data",
#     stream=True
# )

# Telegram bot command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send me a crypto ticker (like BTC or ETH), and I'll analyze it.")

# Handle text messages (ticker inputs)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ticker = update.message.text.strip().upper()
    message = f"Analyze the recent performance and macro+micro outlook for {ticker}. Include any macroeconomic context and sentiment from the latest FinancialJuice data."

    # Use your AI agent to analyze the ticker
    try:
        response = agent_team.run(message, stream= False)
        reply = str(response)
        MAX_LENGTH = 4000

        reply = getattr(response, "content", str(response))  # fallback if content missing
        await update.message.reply_text(reply[:MAX_LENGTH])
    except Exception as e:
        await update.message.reply_text(f"Error analyzing ticker: {e}")

# Main entry point
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()


