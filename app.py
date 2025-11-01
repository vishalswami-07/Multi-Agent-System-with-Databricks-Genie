import streamlit as st
from coordinator_agent import process_query

# =============================================
# Page Config & CSS
# =============================================
st.set_page_config(page_title="Multi-Agent Analytics System", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    .main { padding: 2rem; }
    .chat-message {
        padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem;
        display: flex; flex-direction: column; color: black;
    }
    .user-message { background-color: #e3f2fd; border-left: 4px solid #2196f3; }
    .assistant-message { background-color: #f5f5f5; border-left: 4px solid #4caf50; }
    </style>
""", unsafe_allow_html=True)

# =============================================
# Session State
# =============================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processing" not in st.session_state:
    st.session_state.processing = False

# =============================================
# Header & Sidebar
# =============================================
st.title("Multi-Agent Analytics System")
st.markdown("*Powered by CrewAI, Databricks Genie, and Ollama*")

with st.sidebar:
    st.header("System Information")
    st.info("""
    **Available Agents:**
    - Coordinator: Routes queries
    - Sales Agent: Revenue insights
    - Customer Agent: Churn & LTV
    """)
    st.divider()
    st.header("Settings")
    st.selectbox("Select LLM", ["Ollama (llama3.2)", "Ollama (mistral)", "Ollama (qwen2.5)"])
    st.slider("Temperature", 0.0, 1.0, 0.0, 0.1)

    st.divider()
    st.header("Example Queries")
    examples = {
        "Sales": "What were Q3 sales by region?",
        "Customer": "Which segment has highest churn?",
        "Both": "Show sales and retention trends"
    }
    for label, q in examples.items():
        if st.button(label, key=f"ex_{label}"):
            st.session_state.pending_input = q

    st.divider()
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# =============================================
# MAIN CHAT UI (ONE PLACE ONLY)
# =============================================
st.header("Chat Interface")

# --- Display Messages ---
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You:</strong><br>{msg["content"]}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>Assistant:</strong><br>{msg["content"]}
                </div>
            """, unsafe_allow_html=True)

# --- Input Box (ONLY when not processing) ---
if not st.session_state.processing:
    col1, col2 = st.columns([6, 1])
    with col1:
        default = st.session_state.get("pending_input", "")
        if "pending_input" in st.session_state:
            del st.session_state.pending_input
        user_input = st.text_input(
            "Ask a question:",
            value=default,
            placeholder="e.g., What is revenue by product?",
            key="user_input",
            label_visibility="collapsed"
        )
    with col2:
        send = st.button("Send", type="primary", use_container_width=True)
else:
    st.info("Processing your request... Please wait.")
    send = False
    user_input = ""

# =============================================
# PROCESS INPUT (ONLY ONCE)
# =============================================
if send and user_input and not st.session_state.processing:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.processing = True

    # Run query with spinner
    with st.spinner("Thinking..."):
        try:
            result = process_query(user_input)
            response = str(result)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.success("Done!")
        except Exception as e:
            error = f"Error: {e}"
            st.session_state.messages.append({"role": "assistant", "content": error})
            st.error(error)
        finally:
            st.session_state.processing = False

    # Auto-rerun to refresh UI
    st.rerun()

# =============================================
# Footer
# =============================================
st.divider()
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Built with Streamlit • CrewAI • Databricks Genie</p>
    </div>
""", unsafe_allow_html=True)