# coordinator_agent.py
from crewai import Agent, Task, Crew, Process, LLM
from sales_agent import sales_agent
from customer_agent import customer_agent

# Use Ollama (free, local)
llm = LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11434"
)

GENIE_INSTRUCTION = """
IMPORTANT: When you use **Query Sales Genie** or **Query Customer Genie**, 
pass the question **as a plain string** inside JSON **exactly** like this:

```json
{"question": "What were Q3 sales by customer segment?"}
Never include description, type, or any other fields.
"""

# Schema columns
SALES_COLUMNS = {"date", "product", "category", "revenue", "region"}
CUSTOMER_COLUMNS = {"customer_id", "segment", "lifetime_value", "churn_risk", "region"}

def process_query(query: str) -> str:
    """Process a query using the multi-agent system with schema-based selection"""

    query_lower = query.lower()
    tasks = []
    agents_to_use = set()

    # Check schema-based relevance
    involves_sales = any(col in query_lower for col in SALES_COLUMNS)
    involves_customer = any(col in query_lower for col in CUSTOMER_COLUMNS)

    # If query mentions "sales", "revenue", "product", etc. → Sales agent
    if involves_sales:
        sales_task = Task(
            description=f"Answer this sales-related question: {query}\n"
                        f"{GENIE_INSTRUCTION}",
            agent=sales_agent,
            expected_output="Detailed sales insights based on the query"
        )
        tasks.append(sales_task)
        agents_to_use.add(sales_agent)

    # If query mentions "customer", "segment", "churn", etc. → Customer agent
    if involves_customer:
        customer_task = Task(
            description=f"Answer this customer-related question: {query}\n"
                        f"{GENIE_INSTRUCTION}",
            agent=customer_agent,
            expected_output="Detailed customer insights based on the query"
        )
        tasks.append(customer_task)
        agents_to_use.add(customer_agent)

    # If the query doesn’t match either schema clearly, use both agents
    if not tasks:
        sales_task = Task(
            description=f"Analyze this query from a sales perspective: {query}\n"
                        f"{GENIE_INSTRUCTION}",
            agent=sales_agent,
            expected_output="Sales-related insights if applicable"
        )
        customer_task = Task(
            description=f"Analyze this query from a customer perspective: {query}\n"
                        f"{GENIE_INSTRUCTION}",
            agent=customer_agent,
            expected_output="Customer-related insights if applicable"
        )
        tasks = [sales_task, customer_task]
        agents_to_use = {sales_agent, customer_agent}

    # Create crew with sequential execution
    crew = Crew(
        agents=list(agents_to_use),
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )

    # Execute and return combined result
    result = crew.kickoff()
    return result
