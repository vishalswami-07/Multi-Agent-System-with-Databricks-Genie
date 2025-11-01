# genie_tools.py
from crewai.tools import tool
from config import w, SALES_SPACE_ID, CUSTOMER_SPACE_ID

@tool("Query Sales Genie")
def query_sales_genie(question: str) -> str:
    """Ask the Sales Analytics Genie space a question about sales, revenue, products, regions."""
    assert isinstance(question, str), "Question must be a string"
    message = w.genie.start_conversation_and_wait(
        space_id=SALES_SPACE_ID,
        content=question
    )
    return _extract_genie_text(message)

@tool("Query Customer Genie")
def query_customer_genie(question: str) -> str:
    """Ask the Customer Insights Genie space a question about customers, segments, churn, LTV, regions."""
    assert isinstance(question, str), "Input must be string"
    message = w.genie.start_conversation_and_wait(
        space_id=CUSTOMER_SPACE_ID,
        content=question
    )
    return _extract_genie_text(message)

def _extract_genie_text(message):
    """Extract natural language insights from Genie message."""
    text = ""
    if hasattr(message, 'content') and message.content:
        text += message.content + "\n"
    if hasattr(message, 'attachments'):
        for att in message.attachments or []:
            if hasattr(att, 'type') and att.type == "text" and hasattr(att, 'text'):
                text += att.text + "\n"
    return text.strip() or "No response extracted. Check space setup."