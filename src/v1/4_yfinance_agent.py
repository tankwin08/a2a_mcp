# YFinance Agent for stock prices
from python_a2a import A2AServer, Message, TextContent, MessageRole, run_server 
from python_a2a.mcp import FastMCPAgent
import signal
import sys
import threading
import time
import socket
# Global flag for graceful shutdown
running = True

class YFinanceAgent(A2AServer, FastMCPAgent):
    def __init__(self, mcp_endpoint="http://localhost:5002"):
        A2AServer.__init__(self)
        FastMCPAgent.__init__(
            self,
            mcp_servers={"finance": mcp_endpoint}
        )
    
    async def handle_message_async(self, message):
        if message.content.type == "text":
            # Extract ticker from message
            import re
            ticker_match = re.search(r"\b([A-Z]{1,5})\b", message.content.text)
            if ticker_match:
                ticker = ticker_match.group(1)
                
                # Call MCP tool to get price
                price_info = await self.call_mcp_tool("finance", "get_stock_price", ticker=ticker)
                
                if "error" in price_info:
                    return Message(
                        content=TextContent(text=f"Error getting price for {ticker}: {price_info['error']}"),
                        role=MessageRole.AGENT,
                        parent_message_id=message.message_id,
                        conversation_id=message.conversation_id
                    )
                
                return Message(
                    content=TextContent(
                        text=f"{ticker} is currently trading at {price_info['price']:.2f} {price_info['currency']}."
                    ),
                    role=MessageRole.AGENT,
                    parent_message_id=message.message_id,
                    conversation_id=message.conversation_id
                )
        
        # Handle other message types or errors
        return Message(
            content=TextContent(text="I can provide stock price information for ticker symbols."),
            role=MessageRole.AGENT,
            parent_message_id=message.message_id,
            conversation_id=message.conversation_id
        )

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
    print("\nShutting down YFinance agent...")
    running = False
    sys.exit(0)

def run_agent(mcp_endpoint="http://localhost:5002", agent_port=5004):
    """Run the YFinance agent with configurable endpoints"""
    try:
        agent = YFinanceAgent(mcp_endpoint)
        if is_port_in_use(agent_port):
            print(f"Warning: Port {agent_port} is already in use!")
            return
        print(f"Starting YFinance agent on port {agent_port}")
        run_server(agent, port=agent_port)
    except Exception as e:
        print(f"Error starting agent: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start agent in background thread
    import argparse
    parser = argparse.ArgumentParser(description="YFinance Stock Agent")
    parser.add_argument("--mcp-endpoint", default="http://localhost:5002",
                      help="MCP server endpoint")
    parser.add_argument("--port", type=int, default=5004,
                      help="Agent port number")
    args = parser.parse_args()
    
    agent_thread = threading.Thread(target=run_agent, 
                                  args=(args.mcp_endpoint, args.port),
                                  daemon=True)
    agent_thread.start()

    # Wait for agent to start
    agent_port = 5004
    if wait_for_server(agent_port):
        print(f"YFinance agent is running on port {agent_port}")
    else:
        print("Failed to start agent within timeout period")
        sys.exit(1)

    # Keep the main thread alive
    try:
        while running:
            if not agent_thread.is_alive():
                print("Agent thread has stopped unexpectedly")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nReceived keyboard interrupt")
        running = False
    finally:
        print("Agent shutdown complete")