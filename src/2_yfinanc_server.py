# Import all required libraries
from python_a2a.mcp import FastMCP, text_response
import threading
import requests
import re
import yfinance as yf
import socket
import time
import signal
import sys

# Global flag for graceful shutdown
running = True

# YFinance MCP Server for stock price data
yfinance_mcp = FastMCP(
    name="YFinance MCP",
    version="1.0.0",
    description="Stock market data tools"
)

@yfinance_mcp.tool()
def get_stock_price(ticker: str) -> dict:
    """Get current stock price for a given ticker symbol."""
    try:
        # Get stock data
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        
        if data.empty:
            return {"error": f"No data found for ticker {ticker}"}
        
        # Extract the price
        price = data['Close'].iloc[-1]
        
        return {
            "ticker": ticker,
            "price": price,
            "currency": "USD",
            "timestamp": data.index[-1].strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        return {"error": f"Error fetching stock data: {str(e)}"}

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

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    global running
    print("\nShutting down YFinance server...")
    running = False
    sys.exit(0)

def run_yfinance_server():
    """Run the YFinance server with error handling"""
    try:
        if is_port_in_use(5002):
            print("Warning: Port 5002 is already in use!")
            return
        print("Starting YFinance MCP server on http://0.0.0.0:5002")
        yfinance_mcp.run(host="0.0.0.0", port=5002)
    except Exception as e:
        print(f"Error starting YFinance server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start server in background thread
    yfinance_thread = threading.Thread(target=run_yfinance_server, daemon=True)
    yfinance_thread.start()

    # Wait for server to start
    if wait_for_server(5002):
        print("YFinance MCP server is running on http://0.0.0.0:5002")
    else:
        print("Failed to start server within timeout period")
        sys.exit(1)

    # Keep the main thread alive
    try:
        while running:
            if not yfinance_thread.is_alive():
                print("Server thread has stopped unexpectedly")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nReceived keyboard interrupt")
        running = False
    finally:
        print("Server shutdown complete")