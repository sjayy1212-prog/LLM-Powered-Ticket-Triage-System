import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="Ticket Triage AI", layout="wide")
st.title("Ticket Triage AI Dashboard")

st.sidebar.header("Submit New Ticket")
subject = st.sidebar.text_input("Subject (optional)")
body = st.sidebar.text_area("Ticket body", height=150)
email = st.sidebar.text_input("Customer email (optional)")

if st.sidebar.button("Submit and Triage"):
    if not body.strip():
        st.sidebar.error("Ticket body is required.")
    else:
        with st.spinner("Running AI triage..."):
            resp = requests.post(f"{API_BASE}/tickets/", json={
                "subject": subject or None,
                "body": body,
                "customer_email": email or None,
            })
        if resp.ok:
            t = resp.json()
            st.sidebar.success(f"Ticket created: {t['id'][:8]}...")
            st.sidebar.json({
                "category": t["category"],
                "urgency": t["urgency"],
                "team": t["assigned_team"],
                "confidence": t["confidence"],
            })
        else:
            st.sidebar.error(f"Error: {resp.text}")

st.header("Analytics Overview")

try:
    analytics = requests.get(f"{API_BASE}/analytics/summary").json()
except Exception:
    st.error("Could not connect to API. Is the server running?")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Tickets", analytics["total_tickets"])
c2.metric("Avg Confidence", f"{analytics['avg_confidence']:.1%}")
c3.metric("Avg Latency", f"{analytics['avg_latency_ms']:.0f} ms")
c4.metric("Override Rate", f"{analytics['override_rate']:.1%}")

col1, col2 = st.columns(2)

with col1:
    if analytics["by_category"]:
        df_cat = pd.DataFrame(
            list(analytics["by_category"].items()),
            columns=["Category", "Count"]
        )
        fig = px.pie(df_cat, names="Category", values="Count", title="Tickets by Category")
        st.plotly_chart(fig, use_container_width=True)

with col2:
    if analytics["by_urgency"]:
        df_urg = pd.DataFrame(
            list(analytics["by_urgency"].items()),
            columns=["Urgency", "Count"]
        )
        color_map = {"low": "#2ecc71", "normal": "#3498db", "high": "#f39c12", "critical": "#e74c3c"}
        fig = px.bar(df_urg, x="Urgency", y="Count", title="Urgency Distribution",
                     color="Urgency", color_discrete_map=color_map)
        st.plotly_chart(fig, use_container_width=True)

st.header("Recent Tickets")
try:
    tickets = requests.get(f"{API_BASE}/tickets/?limit=20").json()
    if tickets:
        df = pd.DataFrame(tickets)
        display_cols = ["id", "category", "urgency", "assigned_team", "confidence", "status", "created_at"]
        existing = [c for c in display_cols if c in df.columns]
        st.dataframe(df[existing], use_container_width=True)
    else:
        st.info("No tickets yet. Submit one from the sidebar!")
except Exception as e:
    st.error(f"Failed to load tickets: {e}")