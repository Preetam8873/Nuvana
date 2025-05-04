import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import uuid
from utils.db import load_user_data, add_loan

def show_loans(user_data):
    st.title("Loan Management")
    
    # Create tabs for different loan functions
    tab1, tab2 = st.tabs(["My Loans", "Apply for Loan"])
    
    with tab1:
        show_my_loans(user_data)
    
    with tab2:
        show_loan_application(user_data)

def show_my_loans(user_data):
    st.subheader("My Loans")
    
    # Get loans
    loans = user_data.get("loans", [])
    
    if not loans:
        st.info("You don't have any loans")
        return
    
    # Create DataFrame for loans
    df = pd.DataFrame(loans)
    
    # Format the DataFrame
    if not df.empty:
        # Convert timestamp to datetime if present
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df["application_date"] = df["timestamp"].dt.strftime("%Y-%m-%d")
        
        # Display loans
        for _, row in df.iterrows():
            with st.expander(f"{row.get('type', 'Loan')} - ₹{row.get('amount', 0):,.2f}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("<div class='loan-details'>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Loan ID:</strong> {row.get('loan_id', '')}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Loan Type:</strong> {row.get('type', 'Loan')}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Amount:</strong> ₹{row.get('amount', 0):,.2f}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Interest Rate:</strong> {row.get('interest_rate', 0)}%</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Tenure:</strong> {row.get('tenure', 0)} months</p>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown("<div class='loan-details'>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Application Date:</strong> {row.get('application_date', '')}</p>", unsafe_allow_html=True)
                    
                    status = row.get('status', 'pending')
                    status_class = "status-approved" if status == "approved" else "status-pending" if status == "pending" else "status-rejected"
                    st.markdown(f"<p><strong>Status:</strong> <span class='{status_class}'>{status.capitalize()}</span></p>", unsafe_allow_html=True)
                    
                    if status == "approved":
                        st.markdown(f"<p><strong>EMI:</strong> ₹{row.get('emi', 0):,.2f}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p><strong>Disbursement Date:</strong> {row.get('disbursement_date', '')}</p>", unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Show EMI details if loan is approved
                if row.get('status') == "approved":
                    st.subheader("EMI Schedule")
                    
                    # Calculate EMI schedule
                    principal = row.get('amount', 0)
                    rate = row.get('interest_rate', 0) / (12 * 100)  # Monthly interest rate
                    tenure = row.get('tenure', 0)
                    emi = row.get('emi', 0)
                    
                    # Create EMI schedule
                    schedule = []
                    balance = principal
                    
                    for month in range(1, tenure + 1):
                        interest = balance * rate
                        principal_component = emi - interest
                        balance -= principal_component
                        
                        schedule.append({
                            "Month": month,
                            "EMI": emi,
                            "Principal": principal_component,
                            "Interest": interest,
                            "Balance": max(0, balance)
                        })
                    
                    # Create DataFrame for EMI schedule
                    df_schedule = pd.DataFrame(schedule)
                    
                    # Display EMI schedule
                    st.dataframe(df_schedule.style.format({
                        "EMI": "₹{:.2f}",
                        "Principal": "₹{:.2f}",
                        "Interest": "₹{:.2f}",
                        "Balance": "₹{:.2f}"
                    }))
                    
                    # Create charts for EMI breakdown
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Pie chart for principal vs interest
                        total_interest = df_schedule["Interest"].sum()
                        total_principal = principal
                        
                        fig = px.pie(
                            values=[total_principal, total_interest],
                            names=["Principal", "Interest"],
                            title="Loan Breakdown",
                            color_discrete_sequence=["#4CAF50", "#F44336"]
                        )
                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # Line chart for balance reduction
                        fig = px.line(
                            df_schedule,
                            x="Month",
                            y="Balance",
                            title="Balance Reduction Over Time",
                            markers=True
                        )
                        fig.update_layout(xaxis_title="Month", yaxis_title="Balance (₹)")
                        st.plotly_chart(fig, use_container_width=True)

def show_loan_application(user_data):
    st.subheader("Apply for Loan")
    
    # Loan application form
    with st.form("loan_application_form"):
        st.markdown("<h3>Loan Details</h3>", unsafe_allow_html=True)
        
        # Loan type
        loan_type = st.selectbox(
            "Loan Type",
            ["Personal Loan", "Home Loan", "Car Loan", "Education Loan", "Business Loan"]
        )
        
        # Loan amount
        amount = st.number_input("Loan Amount (₹)", min_value=10000.0, max_value=10000000.0, step=10000.0)
        
        # Loan tenure
        tenure = st.slider("Loan Tenure (months)", min_value=6, max_value=240, step=6, value=36)
        
        # Interest rate (would be calculated based on loan type and credit score in a real app)
        interest_rate = 0.0
        if loan_type == "Personal Loan":
            interest_rate = 12.0
        elif loan_type == "Home Loan":
            interest_rate = 8.5
        elif loan_type == "Car Loan":
            interest_rate = 9.5
        elif loan_type == "Education Loan":
            interest_rate = 7.5
        elif loan_type == "Business Loan":
            interest_rate = 14.0
        
        st.markdown(f"<p><strong>Interest Rate:</strong> {interest_rate}% per annum</p>", unsafe_allow_html=True)
        
        # Calculate EMI
        monthly_rate = interest_rate / (12 * 100)
        emi = (amount * monthly_rate * (1 + monthly_rate) ** tenure) / ((1 + monthly_rate) ** tenure - 1)
        
        st.markdown(f"<p><strong>Monthly EMI:</strong> ₹{emi:,.2f}</p>", unsafe_allow_html=True)
        
        # Purpose of loan
        purpose = st.text_area("Purpose of Loan")
        
        # Terms and conditions
        terms = st.checkbox("I agree to the terms and conditions")
        
        # Submit button
        submit_button = st.form_submit_button("Apply for Loan")
        
        if submit_button:
            if not purpose:
                st.error("Please specify the purpose of the loan")
            elif not terms:
                st.error("Please agree to the terms and conditions")
            else:
                # Create loan data
                loan_data = {
                    "loan_id": str(uuid.uuid4()),
                    "type": loan_type,
                    "amount": amount,
                    "interest_rate": interest_rate,
                    "tenure": tenure,
                    "emi": emi,
                    "purpose": purpose,
                    "status": "pending",
                    "timestamp": datetime.now().isoformat()
                }
                
                # Add loan to user data
                success, message = add_loan(user_data["user_id"], loan_data)
                
                if success:
                    st.success("Loan application submitted successfully")
                    
                    # Refresh user data
                    st.session_state.user_data = load_user_data(user_data["user_id"])
                    
                    # Show application receipt
                    st.markdown("<h3>Application Receipt</h3>", unsafe_allow_html=True)
                    st.markdown("<div class='receipt'>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Application ID:</strong> {loan_data['loan_id']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Loan Type:</strong> {loan_type}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Amount:</strong> ₹{amount:,.2f}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Tenure:</strong> {tenure} months</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Interest Rate:</strong> {interest_rate}% per annum</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Monthly EMI:</strong> ₹{emi:,.2f}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Status:</strong> <span class='status-pending'>Pending</span></p>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error(message)

def show_emi_calculator():
    st.title("EMI Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='calculator-card'>", unsafe_allow_html=True)
        st.markdown("<h3>Loan Details</h3>", unsafe_allow_html=True)
        
        # Loan amount
        amount = st.slider("Loan Amount (₹)", min_value=10000, max_value=10000000, step=10000, value=1000000)
        
        # Interest rate
        interest_rate = st.slider("Interest Rate (% per annum)", min_value=1.0, max_value=20.0, step=0.1, value=8.5)
        
        # Loan tenure
        tenure = st.slider("Loan Tenure (months)", min_value=6, max_value=360, step=6, value=60)
        
        # Calculate EMI
        monthly_rate = interest_rate / (12 * 100)
        emi = (amount * monthly_rate * (1 + monthly_rate) ** tenure) / ((1 + monthly_rate) ** tenure - 1)
        
        # Calculate total payment and interest
        total_payment = emi * tenure
        total_interest = total_payment - amount
        
        st.markdown("<h3>EMI Details</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Monthly EMI:</strong> <span class='emi-amount'>₹{emi:,.2f}</span></p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Total Interest:</strong> ₹{total_interest:,.2f}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Total Payment:</strong> ₹{total_payment:,.2f}</p>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # Create EMI schedule
        schedule = []
        balance = amount
        
        for month in range(1, tenure + 1):
            interest = balance * monthly_rate
            principal = emi - interest
            balance -= principal
            
            schedule.append({
                "Month": month,
                "EMI": emi,
                "Principal": principal,
                "Interest": interest,
                "Balance": max(0, balance)
            })
        
        # Create DataFrame for EMI schedule
        df_schedule = pd.DataFrame(schedule)
        
        # Create charts for EMI breakdown
        st.markdown("<h3>Loan Breakdown</h3>", unsafe_allow_html=True)
        
        # Pie chart for principal vs interest
        fig = px.pie(
            values=[amount, total_interest],
            names=["Principal", "Interest"],
            title="Principal vs Interest",
            color_discrete_sequence=["#4CAF50", "#F44336"]
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        
        # Line chart for balance reduction
        fig = px.line(
            df_schedule,
            x="Month",
            y="Balance",
            title="Balance Reduction Over Time",
            markers=True
        )
        fig.update_layout(xaxis_title="Month", yaxis_title="Balance (₹)")
        st.plotly_chart(fig, use_container_width=True)
        
        # Bar chart for EMI breakdown
        fig = px.bar(
            df_schedule.iloc[::12],  # Sample every 12 months
            x="Month",
            y=["Principal", "Interest"],
            title="EMI Breakdown (Yearly)",
            barmode="stack"
        )
        fig.update_layout(xaxis_title="Month", yaxis_title="Amount (₹)")
        st.plotly_chart(fig, use_container_width=True)
    
    # EMI Schedule
    st.subheader("EMI Schedule")
    
    # Display EMI schedule
    st.dataframe(df_schedule.style.format({
        "EMI": "₹{:.2f}",
        "Principal": "₹{:.2f}",
        "Interest": "₹{:.2f}",
        "Balance": "₹{:.2f}"
    }))
    
    # Download EMI schedule
    if st.button("Download EMI Schedule"):
        st.info("Generating EMI schedule... (This is a demo feature)")
