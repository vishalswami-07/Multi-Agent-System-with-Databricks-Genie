
````markdown
# 🧠 Multi-Agent System with Databricks Genie (CrewAI + Ollama)

This project implements a **multi-agent AI coordination system** designed to intelligently route analytical queries related to **Sales** and **Customers**.  
It uses **CrewAI** for agent orchestration and **Ollama (Llama 3.2)** as the local language model backend.

---

## 🚀 Project Overview

The system consists of:
- A **Coordinator Agent** that decides which specialized agent(s) should handle a user query.
- Two specialized agents:
  - **Sales Agent** — handles all queries related to sales, products, and revenue.
  - **Customer Agent** — handles all queries related to customer segments, churn, and lifetime value.
- A **Config File** to store model and environment settings.
- A **Genie Tools Module (`genie_tools.py`)** that connects each agent to its respective data source (e.g., Databricks Genie or APIs).

---

## 🧩 Architecture

```plaintext
User Query
   │
   ▼
Coordinator Agent
   │
   ├──> Sales Agent (if query mentions sales schema columns)
   │        └── Uses Sales Genie tools → Sales Table (date, product, category, revenue, region)
   │
   ├──> Customer Agent (if query mentions customer schema columns)
   │        └── Uses Customer Genie tools → Customer Table (customer_id, segment, lifetime_value, churn_risk, region)
   │
   ▼
Aggregated Response Returned to User
````

---

## ⚙️ Components

### 1. `coordinator_agent.py`

* Acts as the **central decision-maker**.
* Parses user queries.
* Determines which agent(s) should respond based on **schema-based field detection**.
* If a query involves both sales and customer fields, both agents are invoked sequentially.
* Uses `Crew` with `Process.sequential` for deterministic, reliable execution.

**Schema-based decision logic:**

```python
SALES_COLUMNS = {"date", "product", "category", "revenue", "region"}
CUSTOMER_COLUMNS = {"customer_id", "segment", "lifetime_value", "churn_risk", "region"}
```

Example routing:

| Query                                      | Routed To      |
| ------------------------------------------ | -------------- |
| “Show revenue by category”                 | Sales Agent    |
| “Customer churn risk by region”            | Customer Agent |
| “Compare revenue and churn risk by region” | Both Agents    |

---

### 2. `sales_agent.py`

* Specializes in **sales insights** such as revenue trends, product performance, or regional breakdowns.
* Integrates with `genie_tools.QuerySalesGenie()` for querying data.

---

### 3. `customer_agent.py`

* Handles **customer behavior analysis**, such as churn prediction, segmentation, and LTV analysis.
* Integrates with `genie_tools.QueryCustomerGenie()`.

---

### 4. `config.py`

* Stores model configurations and environment variables.
* Example:

```python
OLLAMA_BASE_URL = "http://localhost:11434"
MODEL_NAME = "ollama/llama3.2"
```

---

### 5. `genie_tools.py`

* Contains helper classes and functions to interface with Databricks Genie or similar APIs.
* Example stubs:

```python
class QuerySalesGenie:
    def query(self, question: str):
        # Query the Sales dataset or API
        pass

class QueryCustomerGenie:
    def query(self, question: str):
        # Query the Customer dataset or API
        pass
```

---

## 🧠 LLM Configuration

The system uses **Ollama** (local model runner) for privacy and zero API costs.

```python
from crewai import LLM

llm = LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11434"
)
```

To run Ollama locally:

```bash
ollama pull llama3.2
ollama serve
```

Then the agents will automatically connect via `http://localhost:11434`.

---

## 🧰 Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/<your-username>/multi-agent-genie.git
   cd multi-agent-genie
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Start Ollama (if not running)**

   ```bash
   ollama serve
   ```

---

## ▶️ Running the System

Run the main script to test the query orchestration:

```bash
python main.py
```

Example interaction:

```python
from coordinator_agent import process_query

query = "Compare revenue and churn risk by region"
result = process_query(query)
print(result)
```

Expected behavior:

* Coordinator detects both “revenue” (Sales) and “churn risk” (Customer).
* Runs both agents sequentially.
* Returns a merged, context-aware summary.

---

## 🧪 Example Outputs

**Input:**

```
What was the revenue trend by category in Q3?
```

**Output:**

```
The Electronics category led Q3 with a 12% increase in revenue, while Furniture dropped by 5%.
```

**Input:**

```
Which customer segments have the highest churn risk in the West region?
```

**Output:**

```
High-value enterprise customers show the highest churn risk in the West, mainly due to delayed renewals.
```

---

## 🧭 Future Enhancements

* 🤖 Add **semantic query detection** using embeddings (e.g., “income” → “revenue”).
* 🔗 Integrate Databricks SQL or Snowflake for live data retrieval.
* 🪄 Use hierarchical process flow (Coordinator → Sub-Agents → Aggregator Agent).
* 📊 Add visualization support for results (matplotlib, Plotly).

---

## 📄 License

Feel free to use and modify it for research, demos, or production systems.

---

**Author:** Vishal Swami
**Role:** AI Engineer
**Focus:** Multi-Agent Systems | LLM Integration | Generative AI Solutions


