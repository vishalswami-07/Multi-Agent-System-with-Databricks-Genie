# main.py
from coordinator_agent import process_query

def main():
    print("Multi-Agent System with CrewAI and Databricks Genie")
    print("=" * 60)
    print("Ask questions about sales or customers. Type 'exit' to quit.\n")
    
    while True:
        user_query = input("You: ").strip()
        
        if user_query.lower() in ['exit', 'quit', 'q']:
            print("Goodbye!")
            break
            
        if not user_query:
            continue
        
        print("\n" + "=" * 60)
        print("Processing your query...\n")
        
        try:
            result = process_query(user_query)
            print("\n" + "=" * 60)
            print(f"Answer: {result}")
            print("=" * 60 + "\n")
        except Exception as e:
            print(f"\nError: {str(e)}\n")

if __name__ == "__main__":
    main()