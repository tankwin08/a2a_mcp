from python_a2a.mcp import FastMCP, text_response
import requests
import re
import yfinance as yf

# Combined Stock MCP Server
stock_mcp = FastMCP(
    name="Stock MCP",
    version="1.0.0",
    description="Stock market data and search tools"
)

@stock_mcp.tool()
def search_ticker(company_name: str) -> str:
    """Find stock ticker symbol for a company using DuckDuckGo search."""
    # ... existing DuckDuckGo search implementation ...

@stock_mcp.tool()
def get_stock_price(ticker: str) -> dict:
    """Get current stock price for a given ticker symbol."""
    # ... existing YFinance implementation ...

if __name__ == "__main__":
    stock_mcp.run(host="0.0.0.0", port=5001)