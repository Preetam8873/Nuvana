import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime, timedelta
import json
from utils.db import load_user_data, add_transaction, transfer_funds

def show_transactions(user_data):
    st.title("Transactions")
    
    # Create tabs for different transaction functions
    tab1, tab2, tab3 = st.tabs(["Transaction History", "Transfer Money", "Mini Statement"])
    
    with tab1:
        show_transaction_history(user_data)
    
    with tab2:
        show_transfer_money(user_data)
    
    with tab3:
        show_mini_statement(user_data)

def show_transaction_history(user_data):
    st.subheader("Transaction History")
    
    # Get primary account
    primary_account = user_data["accounts"][0]
    
    # Get transactions
    transactions = primary_account.get("transactions", [])
    
    if not transactions:
        st.info("No transactions found")
        return
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Date range filter
        date_range = st.selectbox(
            "Date Range",
            ["All Time", "Last 7 Days", "Last 30 Days", "Last 90 Days", "Custom"]
        )
        
        if date_range == "Custom":
            start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
            end_date = st.date_input("End Date", datetime.now())
        else:
            # Set date range based on selection
            end_date = datetime.now()
            if date_range == "Last 7 Days":
                start_date = end_date - timedelta(days=7)
            elif date_range == "Last 30 Days":
                start_date = end_date - timedelta(days=30)
            elif date_range == "Last 90 Days":
                start_date = end_date - timedelta(days=90)
            else:  # All Time
                start_date = datetime.min
    
    with col2:
        # Transaction type filter
        transaction_type = st.selectbox(
            "Transaction Type",
            ["All", "Credit", "Debit"]
        )
    
    with col3:
        # Sort options
        sort_by = st.selectbox(
            "Sort By",
            ["Newest First", "Oldest First", "Amount (High to Low)", "Amount (Low to High)"]
        )
    
    # Create DataFrame for transactions
    df = pd.DataFrame(transactions)
    
    # Apply filters
    if not df.empty:
        # Convert timestamp to datetime
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        
        # Apply date filter
        if date_range != "All Time":
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.max.time())
            df = df[(df["timestamp"] >= start_datetime) & (df["timestamp"] <= end_datetime)]
        
        # Apply transaction type filter
        if transaction_type != "All":
            df = df[df["type"].str.lower() == transaction_type.lower()]
        
        # Apply sorting
        if sort_by == "Newest First":
            df = df.sort_values("timestamp", ascending=False)
        elif sort_by == "Oldest First":
            df = df.sort_values("timestamp", ascending=True)
        elif sort_by == "Amount (High to Low)":
            df = df.sort_values("amount", ascending=False)
        elif sort_by == "Amount (Low to High)":
            df = df.sort_values("amount", ascending=True)
        
        # Format the DataFrame for display
        df["date"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M")
        df["amount_formatted"] = df.apply(
            lambda row: f"+₹{row['amount']:,.2f}" if row["type"] == "credit" else f"-₹{row['amount']:,.2f}",
            axis=1
        )
        
        # Display transactions
        if df.empty:
            st.info("No transactions found matching the filters")
        else:
            # Display transaction count
            st.markdown(f"<p>Showing {len(df)} transactions</p>", unsafe_allow_html=True)
            
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
            
            # Download options
            st.subheader("Download Statement")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Download as PDF"):
                    st.info("Generating PDF statement... (This is a demo feature)")
            
            with col2:
                if st.button("Download as CSV"):
                    st.info("Generating CSV statement... (This is a demo feature)")
            
            # Transaction Analytics
            st.subheader("Transaction Analytics")
            
            # Create charts for transaction analysis
            if not df.empty:
                # Group by date and type
                df["date_only"] = df["timestamp"].dt.date
                
                # Create summary by type
                type_summary = df.groupby("type")["amount"].sum().reset_index()
                
                # Create summary by date
                date_summary = df.groupby(["date_only", "type"])["amount"].sum().reset_index()
                
                # Create two columns for charts
                col1, col2 = st.columns(2)
                
                with col1:
                    # Pie chart for credit vs debit
                    fig = px.pie(
                        type_summary, 
                        values="amount", 
                        names="type",
                        title="Credit vs Debit",
                        color="type",
                        color_discrete_map={"credit": "#4CAF50", "debit": "#F44336"}
                    )
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Line chart for transaction history
                    fig = px.line(
                        date_summary,
                        x="date_only",
                        y="amount",
                        color="type",
                        title="Transaction History",
                        color_discrete_map={"credit": "#4CAF50", "debit": "#F44336"}
                    )
                    fig.update_layout(xaxis_title="Date", yaxis_title="Amount (₹)")
                    st.plotly_chart(fig, use_container_width=True)

def show_transfer_money(user_data):
    st.subheader("Transfer Money")
    
    # Get primary account
    primary_account = user_data["accounts"][0]
    
    # Display current balance
    st.markdown(f"<p>Current Balance: <span class='balance-large'>₹{primary_account['balance']:,.2f}</span></p>", unsafe_allow_html=True)
    
    # Transfer form
    with st.form("transfer_form"):
        st.markdown("<h3>Transfer Details</h3>", unsafe_allow_html=True)
        
        # Beneficiary details
        beneficiary_account = st.text_input("Beneficiary Account Number")
        beneficiary_name = st.text_input("Beneficiary Name")
        
        # Transfer details
        amount = st.number_input("Amount (₹)", min_value=1.0, step=100.0)
        description = st.text_input("Description/Remarks")
        
        # Submit button
        submit_button = st.form_submit_button("Transfer")
        
        if submit_button:
            # Validate inputs
            if not beneficiary_account or not beneficiary_name or amount <= 0:
                st.error("Please fill in all required fields with valid values")
            elif amount > primary_account["balance"]:
                st.error("Insufficient balance")
            else:
                # Perform transfer
                success, message = transfer_funds(
                    user_data["user_id"],
                    0,  # Primary account index
                    beneficiary_account,
                    amount,
                    description
                )
                
                if success:
                    st.success(f"Successfully transferred ₹{amount:,.2f} to {beneficiary_name}")
                    
                    # Refresh user data
                    st.session_state.user_data = load_user_data(user_data["user_id"])
                    
                    # Show receipt
                    st.markdown("<h3>Transaction Receipt</h3>", unsafe_allow_html=True)
                    st.markdown("<div class='receipt'>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Transaction ID:</strong> {user_data['accounts'][0]['transactions'][-1]['transaction_id']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>From:</strong> {primary_account['account_number']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>To:</strong> {beneficiary_account}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Amount:</strong> ₹{amount:,.2f}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Description:</strong> {description}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Status:</strong> <span class='status-approved'>Success</span></p>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error(message)
    
    # Quick transfer options (for demo)
    st.markdown("<h3>Quick Add Money (Demo)</h3>", unsafe_allow_html=True)
    st.markdown("<p>For demonstration purposes only</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Add ₹1,000"):
            success, message = add_transaction(
                user_data["user_id"],
                0,  # Primary account index
                "credit",
                1000,
                "Demo credit"
            )
            
            if success:
                st.success("Added ₹1,000 to your account")
                # Refresh user data
                st.session_state.user_data = load_user_data(user_data["user_id"])
                st.rerun()
            else:
                st.error(message)
    
    with col2:
        if st.button("Add ₹5,000"):
            success, message = add_transaction(
                user_data["user_id"],
                0,  # Primary account index
                "credit",
                5000,
                "Demo credit"
            )
            
            if success:
                st.success("Added ₹5,000 to your account")
                # Refresh user data
                st.session_state.user_data = load_user_data(user_data["user_id"])
                st.rerun()
            else:
                st.error(message)
    
    with col3:
        if st.button("Add ₹10,000"):
            success, message = add_transaction(
                user_data["user_id"],
                0,  # Primary account index
                "credit",
                10000,
                "Demo credit"
            )
            
            if success:
                st.success("Added ₹10,000 to your account")
                # Refresh user data
                st.session_state.user_data = load_user_data(user_data["user_id"])
                st.rerun()
            else:
                st.error(message)

def show_mini_statement(user_data):
    st.subheader("Mini Statement")
    
    # Get primary account
    primary_account = user_data["accounts"][0]
    
    # Get transactions
    transactions = primary_account.get("transactions", [])
    
    if not transactions:
        st.info("No transactions found")
        return
    
    # Sort transactions by timestamp (newest first)
    sorted_transactions = sorted(transactions, key=lambda x: x.get("timestamp", ""), reverse=True)
    
    # Display only the 5 most recent transactions
    mini_statement = sorted_transactions[:5]
    
    # Create DataFrame for display
    df = pd.DataFrame(mini_statement)
    
    # Format the DataFrame
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["date"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M")
        df["amount_formatted"] = df.apply(
            lambda row: f"+₹{row['amount']:,.2f}" if row["type"] == "credit" else f"-₹{row['amount']:,.2f}",
            axis=1
        )
        
        # Display account details
        st.markdown("<div class='mini-statement'>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Account Number:</strong> {primary_account['account_number']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Account Type:</strong> {primary_account['account_type']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Current Balance:</strong> ₹{primary_account['balance']:,.2f}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Display transactions
        st.markdown("<h4>Last 5 Transactions</h4>", unsafe_allow_html=True)
        st.markdown("<div class='transaction-table mini'>", unsafe_allow_html=True)
        
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
        
        # Download mini statement
        if st.button("Download Mini Statement"):
            st.info("Generating mini statement... (This is a demo feature)")

def perform_transfer(user_data, to_account, amount, description):
    """
    Perform a transfer from the user's primary account to another account
    """
    return transfer_funds(
        user_data["user_id"],
        0,  # Primary account index
        to_account,
        amount,
        description
    )
