import yfinance as yf
from ddgs import DDGS

def get_stock_data(ticker: str) -> str:
    """
    Fetches fundamental financial data for a company given its Yahoo Finance ticker.
    Returns a summary containing the sector, current price, margins, P/E ratio, and debt.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Extracting only what matters to avoid blowing up the LLM context window unnecessarily
        summary = (
            f"Company: {info.get('shortName', 'N/A')}\n"
            f"Sector: {info.get('sector', 'N/A')}\n"
            f"Current Price: {info.get('currentPrice', 'N/A')} {info.get('currency', 'N/A')}\n"
            f"P/E Ratio (Trailing PE): {info.get('trailingPE', 'N/A')}\n"
            f"Profit Margin: {info.get('profitMargins', 'N/A')}\n"
            f"Debt to Equity Ratio: {info.get('debtToEquity', 'N/A')}\n"
            f"Business Summary: {str(info.get('longBusinessSummary', 'N/A'))[:500]}..."
        )
        return summary
    except Exception as e:
        return f"Error fetching data for ticker {ticker}: {str(e)}"


def get_recent_news(query: str, max_results: int = 5) -> str:
    """
    Fetches the most recent news about a company or topic using DuckDuckGo.
    Useful for understanding the current macroeconomic context of the asset.
    """
    try:
        results = DDGS().text(f"{query} finance news", max_results=max_results)
        news_summary = ""
        for i, res in enumerate(results):
            news_summary += f"{i+1}. Title: {res.get('title')}\nSummary: {res.get('body')}\n\n"
        return news_summary if news_summary else "No relevant news found."
    except Exception as e:
        return f"Error fetching news: {str(e)}"


# Block to quickly test if the code works before moving to the Agent
if __name__ == "__main__":
    print("--- Testing Financial Data (NVDA) ---")
    print(get_stock_data("NVDA"))
    print("\n--- Testing News (Nvidia) ---")
    print(get_recent_news("Nvidia"))