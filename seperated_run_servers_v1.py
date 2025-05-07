import subprocess
import argparse
import time
import signal
import sys

def signal_handler(signum, frame):
    print("\nShutting down all servers...")
    sys.exit(0)

def run_servers(ports):
    processes = []
    try:
        # Start DuckDuckGo MCP
        duck_proc = subprocess.Popen(['python', 'src/1_duck_server.py'])
        processes.append(('DuckDuckGo MCP', duck_proc))
        time.sleep(2)  # Wait for server to start

        # Start YFinance MCP
        yf_proc = subprocess.Popen(['python', 'src/2_yfinanc_server.py'])
        processes.append(('YFinance MCP', yf_proc))
        time.sleep(2)

        # Start DuckDuckGo Agent
        duck_agent_proc = subprocess.Popen([
            'python', 'src/3_duckduckgo_agent.py',
            '--mcp-endpoint', f'http://localhost:{ports["duck_mcp"]}',
            '--port', str(ports['duck_agent'])
        ])
        processes.append(('DuckDuckGo Agent', duck_agent_proc))
        time.sleep(2)

        # Start YFinance Agent
        yf_agent_proc = subprocess.Popen([
            'python', 'src/4_yfinance_agent.py',
            '--mcp-endpoint', f'http://localhost:{ports["yf_mcp"]}',
            '--port', str(ports['yf_agent'])
        ])
        processes.append(('YFinance Agent', yf_agent_proc))
        time.sleep(2)

        # Start Stock Assistant
        stock_assistant_proc = subprocess.Popen([
            'python', 'src/5_stock_assistant.py'
        ])
        processes.append(('Stock Assistant', stock_assistant_proc))

        print("All servers started successfully!")
        print("\nPress Ctrl+C to stop all servers")
        
        # Keep the script running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nShutting down servers...")
    finally:
        for name, proc in processes:
            print(f"Stopping {name}...")
            proc.terminate()
            proc.wait()
        print("All servers stopped")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run all stock servers")
    parser.add_argument("--duck-mcp-port", type=int, default=5001)
    parser.add_argument("--yf-mcp-port", type=int, default=5002)
    parser.add_argument("--duck-agent-port", type=int, default=5003)
    parser.add_argument("--yf-agent-port", type=int, default=5004)
    
    args = parser.parse_args()
    
    ports = {
        "duck_mcp": args.duck_mcp_port,
        "yf_mcp": args.yf_mcp_port,
        "duck_agent": args.duck_agent_port,
        "yf_agent": args.yf_agent_port
    }
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    run_servers(ports)