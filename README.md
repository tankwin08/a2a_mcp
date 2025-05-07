
# A2A-MCP Stock Assistant

A distributed AI system that combines Model Context Protocol (MCP) with Agent-to-Agent (A2A) communication to provide real-time stock information and analysis.

## Overview

This project demonstrates the power of combining A2A (Agent-to-Agent) and MCP (Model Context Protocol) architectures to create a practical AI system for stock market information. It features:

- Real-time stock price lookups
- Company ticker symbol searches
- Natural language interaction
- Distributed microservice architecture

## System Architecture

The system consists of three main components:

1. **MCP Servers**
   - Stock MCP: Combined service for stock data and search functionality
   - Handles ticker symbol lookups and real-time price fetching

2. **Stock Agent**
   - Intermediary service that communicates with MCP servers
   - Processes user queries and formats responses

3. **Stock Assistant**
   - Main user interface
   - Powered by OpenAI's GPT models
   - Natural language processing for user queries

## Requirements

- Python 3.10 or higher
- Dependencies listed in pyproject.toml:
  - python-a2a[all] >= 0.5.4
  - python-dotenv >= 1.1.0
  - requests >= 2.32.3
  - yfinance >= 0.2.58

## Installation

1. Clone the repository
2. Create a virtual environment using uv:
```bash
uv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
uv install 

uv add package-name
```

## Configuration

1. Create a `.env` file in the project root
2. Add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Start the servers:
```bash
python run_servers.py
```

2. In a separate terminal, run the interactive client:
```bash
python interact_client.py
```

3. Example queries in your terminal:
   - Apple
   - Apple Inc
   - amd

## Architecture Details

### MCP Servers
- Provides standardized interfaces for stock data
- Implements DuckDuckGo search for ticker lookup
- Uses YFinance for real-time stock data

### Stock Agent
- Handles communication between components
- Processes and routes queries
- Formats responses for consistency

### Stock Assistant
- Natural language processing
- Query understanding and decomposition
- Response generation and formatting

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Acknowledgments

This project is inspired by the article ["The Power Duo: How A2A & MCP Let You Build Practical AI Systems Today"](https://medium.com/@the_manoj_desai/the-power-duo-how-a2a-mcp-let-you-build-practical-ai-systems-today-9c19064b027b).


        