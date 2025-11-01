# customer_agent.py
from crewai import Agent, LLM
from genie_tools import query_customer_genie

# Use Ollama (free, local)
llm = LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11434"
)

customer_agent = Agent(
    role='Customer Insights Expert',
    goal='Provide accurate customer behavior and churn insights using available data tools',
    backstory="""You are a customer analytics specialist with extensive experience 
    in understanding customer behavior, demographics, and retention patterns. 
    You are skilled at extracting meaningful insights from customer data.""",
    verbose=True,
    allow_delegation=False,
    tools=[query_customer_genie],
    llm=llm
)