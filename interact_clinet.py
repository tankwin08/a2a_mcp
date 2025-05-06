from python_a2a import A2AClient, Message, TextContent, MessageRole
import argparse

def interactive_session(client):
    """Interactive session with the stock assistant."""
    print("\n===== Stock Price Assistant =====")
    print("Type 'exit' or 'quit' to end the session.")
    print("Example queries:")
    print("  - What's the stock price of Apple?")
    print("  - How much is Microsoft trading for?")
    print("  - Get the current price of Tesla stock")
    print("=" * 50)
    
    while True:
        try:
            user_input = input("\n> ")
            
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            
            # Send as a text message
            message = Message(
                content=TextContent(text=user_input),
                role=MessageRole.USER
            )
            
            print("Sending to assistant...")
            response = client.send_message(message)
            
            # Display the response
            print(f"\nAssistant: {response.content.text}")
            
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again or type 'exit' to quit.")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stock Assistant Client")
    parser.add_argument("--endpoint", default="http://localhost:5005/a2a", 
                        help="Stock assistant endpoint URL")
    
    args = parser.parse_args()
    
    # Create a client
    client = A2AClient(args.endpoint)
    
    # Start interactive session
    interactive_session(client)