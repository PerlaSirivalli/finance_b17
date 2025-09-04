import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# =====================
# Backend API URL
# =====================
API_URL = "http://127.0.0.1:8000"

# =====================
# Custom CSS
# =====================
st.markdown("""
    <style>
        /* App background */
        .stApp {
            background: linear-gradient(135deg, #e0c3fc, #8ec5fc);
            font-family: 'Segoe UI', sans-serif;
        }

        /* Main title */
        .main-header {
            font-size: 55px;
            font-weight: bold;
            text-align: center;
            background: -webkit-linear-gradient(45deg, #6a11cb, #2575fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 30px;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.2);
        }

        /* Section headers */
        .section-header {
            font-size: 32px;
            font-weight: 800;
            text-align: center;
            background: -webkit-linear-gradient(45deg,#ff6ec4,#7873f5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-top: 30px;
            margin-bottom: 20px;
        }

        /* Text & number input fields */
        .stTextInput>div>div>input,
        .stNumberInput>div>div>input {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 2px solid #6a11cb !important;
            border-radius: 10px !important;
            padding: 10px !important;
            font-size: 16px !important;
        }

        /* Fix Streamlit number input (entire container) */
        [data-baseweb="input"] {
            background-color: #ffffff !important;
            color: #000000 !important;
            border-radius: 10px !important;
            font-size: 16px !important;
        }

        /* Table styling */
        .dataframe {
            border-radius: 12px;
            border: 2px solid #6a11cb;
            overflow: hidden;
            box-shadow: 0px 5px 15px rgba(0,0,0,0.1);
        }
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th {
            background: linear-gradient(45deg, #6a11cb, #2575fc);
            color: white;
            padding: 12px;
            font-size: 17px;
        }
        td {
            padding: 10px;
            text-align: center;
            font-size: 15px;
        }
        tr:nth-child(even) {background-color: #f3e5f5;}
        tr:nth-child(odd) {background-color: #ede7f6;}

        /* Buttons */
        .stButton>button {
            background: linear-gradient(45deg, #6a11cb, #2575fc);
            color: white;
            border-radius: 12px;
            padding: 12px 28px;
            font-size: 18px;
            font-weight: 600;
            border: none;
            transition: 0.3s;
        }
        .stButton>button:hover {
            transform: scale(1.05);
            background: linear-gradient(45deg, #2575fc, #6a11cb);
        }

        /* Tabs customization */
        .stTabs [role="tablist"] {
            gap: 15px;
            justify-content: center;
        }

        .stTabs [role="tab"] {
            background: #ffffff !important;
            color: #000000 !important;
            padding: 12px 25px !important;
            border-radius: 12px 12px 0 0 !important;
            font-size: 18px !important;
            font-weight: 600 !important;
            border: 2px solid #6a11cb !important;
            transition: 0.3s;
        }

        .stTabs [role="tab"][aria-selected="true"] {
            background: linear-gradient(45deg, #6a11cb, #2575fc) !important;
            color: #ffffff !important;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
        }
    </style>
""", unsafe_allow_html=True)

# =====================
# Plotly theme
# =====================
px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = px.colors.sequential.Purples + px.colors.sequential.Blues

# =====================
# Session state
# =====================
if "token" not in st.session_state:
    st.session_state.token = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# =====================
# Login Page
# =====================
def login_page():
    st.markdown("<h1 class='main-header'>💰 Finance Chatbot</h1>", unsafe_allow_html=True)
    with st.container():
        st.subheader("🔑 Login to Continue")
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")

        if st.button("Login"):
            res = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
            if res.status_code == 200:
                data = res.json()
                st.session_state.token = data["access_token"]
                st.session_state.user_id = data["user_id"]
                st.session_state.username = data["username"]
                st.success(f"✅ Welcome {data['username']}!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")


# =====================
# Dashboard Page
# =====================
def dashboard_page():
    st.sidebar.title(f"👋 Hello, {st.session_state.username}")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.token = None
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.chat_history = []
        st.rerun()

    st.markdown(f"<h1 class='main-header'>📊 Dashboard</h1>", unsafe_allow_html=True)

    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    tab1, tab2, tab3 = st.tabs(["➕ Add Expense", "📜 Expense History", "🤖 Chat Assistant"])

    # ---- Add Expense ----
    with tab1:
        st.markdown("<div class='section-header'>Add New Expense</div>", unsafe_allow_html=True)
        description = st.text_input("Description")
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        if st.button("Add Expense"):
            if description and amount > 0:
                res = requests.post(
                    f"{API_URL}/expenses/",
                    json={"description": description, "amount": amount, "user_id": st.session_state.user_id},
                    headers=headers,
                )
                if res.status_code == 200:
                    st.success("✅ Expense added!")
                    st.rerun()
                else:
                    st.error("❌ Failed to add expense")
            else:
                st.warning("⚠ Please enter a valid description and amount")

    # ---- Expense History ----
    with tab2:
        st.markdown("<div class='section-header'>Your Expenses</div>", unsafe_allow_html=True)
        res = requests.get(f"{API_URL}/expenses/{st.session_state.user_id}", headers=headers)
        if res.status_code == 200:
            expenses = res.json()
            if expenses:
                df = pd.DataFrame(expenses)
                st.dataframe(df[["description", "amount"]], use_container_width=True)

                total_expenses = df["amount"].sum()
                st.metric("💵 Total Expenses", f"${total_expenses:.2f}")

                col1, col2 = st.columns(2)
                with col1:
                    fig = px.pie(df, names="description", values="amount", title="💡 Expense Breakdown")
                    st.plotly_chart(fig, use_container_width=True)
                with col2:
                    fig2 = px.bar(df, x="description", y="amount", text="amount", title="📊 Expense by Category")
                    st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No expenses yet.")
        else:
            st.error("Could not fetch expenses")

    # ---- Chat Assistant ----
    with tab3:
        st.markdown("<div class='section-header'>Ask the AI Assistant</div>", unsafe_allow_html=True)
        query = st.text_input("💬 Ask something about your finances...")
        if st.button("Ask"):
            if query:
                res = requests.post(f"{API_URL}/chat", json={"query": query}, headers=headers)
                if res.status_code == 200:
                    answer = res.json().get("answer", "No response")
                    st.session_state.chat_history.append(("You", query))
                    st.session_state.chat_history.append(("AI", answer))
                else:
                    st.error("❌ Failed to get response from AI assistant")
            else:
                st.warning("⚠ Please enter a question")

        # Display chat history
        for role, text in st.session_state.chat_history:
            if role == "You":
                st.markdown(f"🧑 *{role}:* {text}")
            else:
                st.markdown(f"🤖 *{role}:* {text}")


# =====================
# Main app
# =====================
if st.session_state.token:
    dashboard_page()
else:
    login_page()