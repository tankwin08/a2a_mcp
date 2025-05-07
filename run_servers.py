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
        # Start Stock MCP (combined DuckDuckGo and YFinance)
        mcp_proc = subprocess.Popen(['python', 'src/stock_mcp.py'])
        processes.append(('Stock MCP', mcp_proc))
        time.sleep(2)

        # Start Stock Agent (combined DuckDuckGo and YFinance agents)
        agent_proc = subprocess.Popen([
            'python', 'src/stock_agent.py',
            '--mcp-endpoint', f'http://localhost:{ports["mcp"]}',
            '--port', str(ports['agent'])
        ])
        processes.append(('Stock Agent', agent_proc))
        time.sleep(2)

        # Start Stock Assistant
        assistant_proc = subprocess.Popen([
            'python', 'src/5_stock_assistant.py'
        ])
        processes.append(('Stock Assistant', assistant_proc))

        print("All servers started successfully!")
        print("\nPress Ctrl+C to stop all servers")
        
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
    parser = argparse.ArgumentParser(description="Run stock servers")
    parser.add_argument("--mcp-port", type=int, default=5001)
    parser.add_argument("--agent-port", type=int, default=5002)
    
    args = parser.parse_args()
    
    ports = {
        "mcp": args.mcp_port,
        "agent": args.agent_port
    }
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    run_servers(ports)