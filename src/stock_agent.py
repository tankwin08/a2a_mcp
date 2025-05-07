from python_a2a import A2AServer, Message, TextContent, MessageRole, run_server
from python_a2a.mcp import FastMCPAgent

class StockAgent(A2AServer, FastMCPAgent):
    """Agent that handles both ticker lookup and price information."""
    
    def __init__(self, mcp_endpoint="http://localhost:5001"):
        A2AServer.__init__(self)
        FastMCPAgent.__init__(
            self,
            mcp_servers={"stock": mcp_endpoint}
        )
    
    async def handle_message_async(self, message):
        if message.content.type == "text":
            # Extract company name or ticker from message
            text = message.content.text.lower()
            
            if "ticker" in text:
                # Handle ticker lookup
                company_name = self._extract_company_name(text)
                ticker = await self.call_mcp_tool("stock", "search_ticker", company_name=company_name)
                return self._create_response(f"The ticker symbol for {company_name} is {ticker}.", message)
            else:
                # Handle price lookup
                ticker = self._extract_ticker(text)
                price_info = await self.call_mcp_tool("stock", "get_stock_price", ticker=ticker)
                return self._create_response(f"{ticker} is currently trading at {price_info['price']:.2f} {price_info['currency']}.", message)

if __name__ == "__main__":
    agent = StockAgent()
    run_server(agent, port=5002)