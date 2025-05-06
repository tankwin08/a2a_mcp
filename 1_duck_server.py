# Import all required libraries
from python_a2a.mcp import FastMCP, text_response
import threading
import requests
import re
import yfinance as yf
import socket
import time

# DuckDuckGo MCP Server for ticker lookup
duckduckgo_mcp = FastMCP(
    name="DuckDuckGo MCP",
    version="1.0.0",
    description="Search capabilities for finding stock information"
)

@duckduckgo_mcp.tool()
def search_ticker(company_name: str) -> str:
    """Find stock ticker symbol for a company using DuckDuckGo search."""
    # Implementation details (simplified)
    query = f"{company_name} stock ticker symbol"
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    response = requests.get(url)
    data = response.json()
    
    # Extract ticker from results
    # Look for patterns like "NYSE: AAPL" or "NASDAQ: MSFT"
    text = data.get("Abstract", "")
    ticker_match = re.search(r'(?:NYSE|NASDAQ):\s*([A-Z]+)', text)
    if ticker_match:
        return ticker_match.group(1)
    
    # Fall back to common tickers for demo purposes
    if company_name.lower() == "apple":
        return "AAPL"
    elif company_name.lower() == "microsoft":
        return "MSFT"
    elif company_name.lower() == "google" or company_name.lower() == "alphabet":
        return "GOOGL"
    elif company_name.lower() == "amazon":
        return "AMZN"
    elif company_name.lower() == "tesla":
        return "TSLA"
    
    return f"Could not find ticker for {company_name}"

# # YFinance MCP Server for stock price data
# yfinance_mcp = FastMCP(
#     name="YFinance MCP",
#     version="1.0.0",
#     description="Stock market data tools"
# )

# @yfinance_mcp.tool()
# def get_stock_price(ticker: str) -> dict:
#     """Get current stock price for a given ticker symbol."""
#     try:
#         # Get stock data
#         stock = yf.Ticker(ticker)
#         data = stock.history(period="1d")
        
#         if data.empty:
#             return {"error": f"No data found for ticker {ticker}"}
        
#         # Extract the price
#         price = data['Close'].iloc[-1]
        
#         return {
#             "ticker": ticker,
#             "price": price,
#             "currency": "USD",
#             "timestamp": data.index[-1].strftime('%Y-%m-%d %H:%M:%S')
#         }
#     except Exception as e:
#         return {"error": f"Error fetching stock data: {str(e)}"}

# # For Jupyter Notebook, use threads to run both servers non-blocking
def is_port_in_use(port: int) -> bool:
    """Check if a port is in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def wait_for_server(port: int, timeout: int = 5) -> bool:
    """Wait for server to start up."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_port_in_use(port):
            return True
        time.sleep(0.1)
    return False

def run_duckduckgo_server():
    """Run the DuckDuckGo server with status check."""
    try:
        if is_port_in_use(5001):
            print("Warning: Port 5001 is already in use!")
            return
        duckduckgo_mcp.run(host="0.0.0.0", port=5001)
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    # Start server in background thread
    duckduckgo_thread = threading.Thread(target=run_duckduckgo_server, daemon=True)
    duckduckgo_thread.start()

    # Wait for server to start
    if wait_for_server(5001):
        print("DuckDuckGo MCP server is running on http://0.0.0.0:5001")
    else:
        print("Failed to start server within timeout period")

    # Keep main thread alive
    try:
        while True:
            if not duckduckgo_thread.is_alive():
                print("Server thread has stopped unexpectedly")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down server...")


# def run_yfinance_server():
#     yfinance_mcp.run(host="0.0.0.0", port=5002)

# # Start both servers in background threads
duckduckgo_thread = threading.Thread(target=run_duckduckgo_server, daemon=True)
# yfinance_thread = threading.Thread(target=run_yfinance_server, daemon=True)

duckduckgo_thread.start()
# yfinance_thread.start()

print("DuckDuckGo MCP server is running on http://0.0.0.0:5001")
# print("YFinance MCP server is running on http://0.0.0.0:5002")

# # Example usage - you can run these in a separate cell to test
# # Test the DuckDuckGo ticker search
# print("\nTesting ticker search:")
# companies = ["Apple", "Microsoft", "Amazon"]
# for company in companies:
#     ticker = search_ticker(company)
#     print(f"{company} ticker: {ticker}")

# # Test the YFinance stock price lookup
# print("\nTesting stock price lookup:")
# tickers = ["AAPL", "MSFT", "AMZN"]
# for ticker in tickers:
#     price_data = get_stock_price(ticker)
#     print(f"{ticker} price data: {price_data}")