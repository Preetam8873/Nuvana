import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import random
from utils.db import load_user_data

def show_dashboard(user_data):
    st.title("Dashboard")
    
    # Get primary account
    primary_account = user_data["accounts"][0]
    
    # Display account summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<h3>Account Balance</h3>", unsafe_allow_html=True)
        st.markdown(f"<p class='balance-large'>₹{primary_account['balance']:,.2f}</p>", unsafe_allow_html=True)
        st.markdown("<p>Available Balance</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<h3>Account Details</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Account Number:</strong> {primary_account['account_number']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Account Type:</strong> {primary_account['account_type']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Status:</strong> {primary_account['status']}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.markdown("<h3>Quick Actions</h3>", unsafe_allow_html=True)
        if st.button("Transfer Money"):
            st.session_state.current_page = "transactions"
            st.rerun()
        if st.button("Apply for Loan"):
            st.session_state.current_page = "loans"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Get transactions
    transactions = primary_account.get("transactions", [])
    
    # Recent transactions
    st.markdown("<h3>Recent Transactions</h3>", unsafe_allow_html=True)
    
    if not transactions:
        st.info("No transactions found")
    else:
        # Sort transactions by timestamp (newest first)
        sorted_transactions = sorted(transactions, key=lambda x: x.get("timestamp", ""), reverse=True)
        
        # Display only the 5 most recent transactions
        recent_transactions = sorted_transactions[:5]
        
        # Create a DataFrame for display
        df = pd.DataFrame(recent_transactions)
        
        # Format the DataFrame
        if not df.empty:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df["date"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M")
            df["amount_formatted"] = df.apply(
                lambda row: f"+₹{row['amount']:,.2f}" if row["type"] == "credit" else f"-₹{row['amount']:,.2f}",
                axis=1
            )
            
            # Display transactions in a table
            st.markdown("<div class='transaction-table'>", unsafe_allow_html=True)
            
            for _, row in df.iterrows():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"<div class='transaction-item'>", unsafe_allow_html=True)
                    st.markdown(f"<p class='transaction-desc'>{row['description']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='transaction-date'>{row['date']}</p>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"<div class='transaction-item'>", unsafe_allow_html=True)
                    if row["type"] == "credit":
                        st.markdown(f"<p class='transaction-amount credit'>+₹{row['amount']:,.2f}</p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p class='transaction-amount debit'>-₹{row['amount']:,.2f}</p>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"<div class='transaction-item'>", unsafe_allow_html=True)
                    st.markdown(f"<p class='transaction-type'>{row['type'].capitalize()}</p>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # View all transactions button
            if st.button("View All Transactions"):
                st.session_state.current_page = "transactions"
                st.rerun()
    
    # Spending Analytics
    st.markdown("<h3>Spending Analytics</h3>", unsafe_allow_html=True)
    
    # Filter transactions for the last 30 days
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_transactions = [
        t for t in transactions 
        if t.get("type") == "debit" and 
        datetime.fromisoformat(t.get("timestamp", datetime.now().isoformat())) > thirty_days_ago
    ]
    
    if not recent_transactions:
        st.info("No spending data available for the last 30 days")
    else:
        # Create spending categories (in a real app, transactions would have categories)
        # For demo, we'll assign random categories
        categories = ["Shopping", "Food", "Transportation", "Entertainment", "Utilities", "Others"]
        
        # Assign categories to transactions
        for t in recent_transactions:
            if "category" not in t:
                # In a real app, you would use a categorization algorithm
                # For demo, we'll assign random categories
                t["category"] = random.choice(categories)
        
        # Group by category
        category_spending = {}
        for t in recent_transactions:
            category = t.get("category", "Others")
            if category not in category_spending:
                category_spending[category] = 0
            category_spending[category] += t.get("amount", 0)
        
        # Create DataFrame for plotting
        df_spending = pd.DataFrame({
            "Category": list(category_spending.keys()),
            "Amount": list(category_spending.values())
        })
        
        # Create two columns for charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Create pie chart
            fig = px.pie(
                df_spending, 
                values="Amount", 
                names="Category",
                title="Spending by Category",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Create bar chart
            fig = px.bar(
                df_spending, 
                x="Category", 
                y="Amount",
                title="Spending by Category",
                color="Category",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_layout(xaxis_title="Category", yaxis_title="Amount (₹)")
            st.plotly_chart(fig, use_container_width=True)
    
    # Loan Summary (if any)
    if user_data.get("loans"):
        st.markdown("<h3>Loan Summary</h3>", unsafe_allow_html=True)
        
        # Create DataFrame for loans
        df_loans = pd.DataFrame(user_data["loans"])
        
        # Display loans in a table
        st.markdown("<div class='loan-table'>", unsafe_allow_html=True)
        
        for _, row in df_loans.iterrows():
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.markdown(f"<div class='loan-item'>", unsafe_allow_html=True)
                st.markdown(f"<p class='loan-type'>{row.get('type', 'Loan')}</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='loan-id'>Loan ID: {row.get('loan_id', '')}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"<div class='loan-item'>", unsafe_allow_html=True)
                st.markdown(f"<p class='loan-amount'>₹{row.get('amount', 0):,.2f}</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='loan-tenure'>Tenure: {row.get('tenure', '0')} months</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"<div class='loan-item'>", unsafe_allow_html=True)
                status = row.get('status', 'pending')
                status_class = "status-approved" if status == "approved" else "status-pending" if status == "pending" else "status-rejected"
                st.markdown(f"<p class='loan-status {status_class}'>{status.capitalize()}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # View all loans button
        if st.button("View All Loans"):
            st.session_state.current_page = "loans"
            st.rerun()
