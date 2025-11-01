# sales_agent.py
from crewai import Agent, LLM
from genie_tools import query_sales_genie

# Use Ollama (free, local)
llm = LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11434"
)

sales_agent = Agent(
    role='Sales Analytics Expert',
    goal='Provide accurate sales and revenue insights using available data tools',
    backstory="""You are an experienced sales analyst with deep expertise in 
    analyzing sales data, revenue trends, and business performance metrics. 
    You excel at querying data systems and presenting insights clearly.""",
    verbose=True,
    allow_delegation=False,
    tools=[query_sales_genie],
    llm=llm
)