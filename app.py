import requests
import streamlit as st

st.title("Personal Finance Chatbot")

# --- Login section ---
st.subheader("Login")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
if st.button("Login"):
    # Placeholder login (later connect to backend auth)
    st.success(f"Logged in as {username}")

# --- Chat section ---
st.subheader("Chat with your Finance Assistant")
user_question = st.text_area("Ask your finance question:")

if st.button("Ask"):
    try:
        response = requests.post(
            "http://127.0.0.1:8000/chat",   # backend URL
            json={"message": user_question}
        )
        if response.status_code == 200:
            reply = response.json().get("reply", "No reply from backend")
            st.write("💬 Bot:", reply)
        else:
            st.error(f"Backend error: {response.status_code}")
    except Exception as e:
        st.error(f"Request failed: {e}")

# --- Add Expense section ---
st.subheader("Add Expense")
expense_amount = st.number_input("Amount", min_value=0.0, step=0.01)
expense_category = st.text_input("Category")
expense_desc = st.text_input("Description")

if st.button("Add Expense"):
    # Placeholder for adding expense
    st.success(f"Expense added: ₹{expense_amount} for {expense_category}")