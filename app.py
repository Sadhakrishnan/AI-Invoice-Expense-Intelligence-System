import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Invoice Intelligence Dashboard", layout="wide")

API_URL = "http://localhost:8000"

st.title("🧾 AI Invoice & Expense Intelligence")

tabs = st.tabs(["Upload Invoice", "Dashboard", "Invoices", "Anomalies"])

with tabs[0]:
    st.header("Upload New Invoice")
    uploaded_file = st.file_uploader("Choose a PDF or Image", type=["pdf", "png", "jpg", "jpeg"])
    if st.button("Process Invoice"):
        if uploaded_file is not None:
            with st.spinner("Processing..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                response = requests.post(f"{API_URL}/upload_invoice", files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("Invoice processed successfully!")
                    st.json(data)
                    if data.get("anomaly"):
                        st.error(f"🚨 Anomaly Detected: {data.get('anomaly_reason')}")
                else:
                    st.error(f"Error: {response.text}")
        else:
            st.warning("Please upload a file.")

with tabs[1]:
    st.header("Analytics Dashboard")
    try:
        response = requests.get(f"{API_URL}/analytics")
        if response.status_code == 200:
            analytics = response.json()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Monthly Spending")
                monthly = pd.DataFrame(analytics["monthly_spending"])
                if not monthly.empty:
                    fig = px.line(monthly, x="month", y="total", markers=True)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data yet.")
                    
            with col2:
                st.subheader("Category Distribution")
                category = pd.DataFrame(analytics["category_distribution"])
                if not category.empty:
                    fig = px.pie(category, names="category", values="total")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data yet.")
                    
            st.subheader("Top Vendors")
            vendors = pd.DataFrame(analytics["top_vendors"])
            if not vendors.empty:
                fig = px.bar(vendors, x="vendor", y="total")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data yet.")
    except:
        st.error("Could not connect to API. Is it running?")

with tabs[2]:
    st.header("All Invoices")
    try:
        response = requests.get(f"{API_URL}/invoices")
        if response.status_code == 200:
            invoices = pd.DataFrame(response.json())
            if not invoices.empty:
                st.dataframe(invoices, use_container_width=True)
            else:
                st.info("No invoices found.")
    except:
        st.error("Could not connect to API.")

with tabs[3]:
    st.header("Detected Anomalies 🚨")
    try:
        response = requests.get(f"{API_URL}/anomalies")
        if response.status_code == 200:
            anomalies = pd.DataFrame(response.json())
            if not anomalies.empty:
                st.dataframe(anomalies, use_container_width=True)
            else:
                st.success("No anomalies detected!")
    except:
        st.error("Could not connect to API.")
