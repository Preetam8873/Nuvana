import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os
import json
from datetime import datetime
from utils.db import get_all_users

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
ACCOUNTS_FILE = os.path.join(DATA_DIR, 'accounts.json')
TRANSACTIONS_FILE = os.path.join(DATA_DIR, 'transactions.json')

def load_json_data(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        st.error(f"Error decoding JSON from {os.path.basename(file_path)}")
        return {}

def save_json_data(file_path, data):
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        return True, "Data saved successfully"
    except Exception as e:
        return False, f"Error saving data: {e}"

# Predefined admin credentials
ADMIN_CREDENTIALS = {
    "pk@pk.com": "123",
    "nv@nv.com": "123"
}

def show_login_form():
    st.subheader("Admin Login")
    with st.form("admin_login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if email in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[email] == password:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Invalid email or password")

def show_admin_page():
    st.title("Admin Panel")

    # Initialize login state if it doesn't exist
    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False

    if st.session_state.admin_logged_in:
        # Logout button
        if st.sidebar.button("Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()
        
        # Display admin panel content
        show_admin_panel_content()
    else:
        show_login_form()

def show_admin_panel_content():
    # Create tabs for different admin functions
    tab1, tab2, tab3 = st.tabs(["User Management", "Loan Approval", "Transaction Monitoring"])
    
    with tab1:
        show_user_management()
    
    with tab2:
        show_loan_approval()
    
    with tab3:
        show_transaction_monitoring()

def show_user_management():
    st.subheader("User Management")

    # Load data directly from JSON files
    users_data = load_json_data(USERS_FILE)
    accounts_data = load_json_data(ACCOUNTS_FILE)

    if not users_data:
        st.info("No users found in users.json")
        return

    # Create a list of user summaries
    user_summaries = []
    for user_id, user_info in users_data.items():
        # Get account balance from accounts_data
        balance = 0
        account_info = accounts_data.get(user_id)
        if account_info:
            balance = account_info.get("balance", 0)

        # Create user summary
        user_summary = {
            "user_id": user_id,
            "name": user_info.get("full_name", ""),
            "email": user_info.get("email", ""),
            "phone": user_info.get("phone", ""),
            "balance": balance,
            "status": user_info.get("status", "Active"), # Assuming status is stored in users.json
            "created_at": user_info.get("created_at", "")
        }
        user_summaries.append(user_summary)

    # Create DataFrame for display
    df = pd.DataFrame(user_summaries)

    # Format the DataFrame
    if not df.empty:
        # Ensure 'created_at' exists and handle potential errors
        if 'created_at' in df.columns:
            df["created_at_dt"] = pd.to_datetime(df["created_at"], errors='coerce')
            df["joined_date"] = df["created_at_dt"].dt.strftime("%Y-%m-%d")
        else:
            df["joined_date"] = "N/A"
            
        df["balance_formatted"] = df["balance"].apply(lambda x: f"₹{x:,.2f}")

        # Display users in a table
        st.dataframe(df[["name", "email", "phone", "balance_formatted", "status", "joined_date"]])

        # User details
        st.subheader("User Details")

        # Select user
        user_ids = list(users_data.keys())
        if not user_ids:
             st.warning("No users available for selection.")
             return
             
        selected_user_id = st.selectbox(
            "Select User",
            user_ids,
            format_func=lambda x: users_data.get(x, {}).get("full_name", x) # Show name or ID
        )

        if selected_user_id:
            user_data = users_data.get(selected_user_id)
            account_data = accounts_data.get(selected_user_id)

            if user_data:
                # Display user details
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("<div class='user-details'>", unsafe_allow_html=True)
                    st.markdown("<h3>Personal Information</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Name:</strong> {user_data.get('full_name', 'N/A')}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Email:</strong> {user_data.get('email', 'N/A')}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Phone:</strong> {user_data.get('phone', 'N/A')}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Date of Birth:</strong> {user_data.get('dob', 'N/A')}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>PAN:</strong> {user_data.get('pan', 'N/A')}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Aadhar:</strong> {user_data.get('aadhar', 'N/A')}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Address:</strong> {user_data.get('address', 'N/A')}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Joined:</strong> {user_data.get('created_at', 'N/A')}</p>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                with col2:
                    st.markdown("<div class='user-details'>", unsafe_allow_html=True)
                    st.markdown("<h3>Account Information</h3>", unsafe_allow_html=True)
                    if account_data:
                        st.markdown(f"<p><strong>Account Number:</strong> {account_data.get('account_number', 'N/A')}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p><strong>Account Type:</strong> {account_data.get('account_type', 'N/A')}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p><strong>Status:</strong> {account_data.get('status', 'N/A')}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p><strong>Balance:</strong> ₹{account_data.get('balance', 0):,.2f}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p><strong>Created At:</strong> {account_data.get('created_at', 'N/A')}</p>", unsafe_allow_html=True)
                    else:
                        st.markdown("<p>No account information found.</p>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                # User actions
                st.subheader("User Actions")
                col1, col2 = st.columns(2)

                with col1:
                    current_status = user_data.get("status", "Active") # Default to Active if status missing
                    # Block/Unblock user (assuming status is in users.json)
                    if current_status == "Blocked":
                        if st.button("Unblock User"):
                            users_data[selected_user_id]["status"] = "Active"
                            success, message = save_json_data(USERS_FILE, users_data)
                            if success:
                                st.success("User unblocked successfully")
                                st.rerun()
                            else:
                                st.error(message)
                    else:
                        if st.button("Block User"):
                            users_data[selected_user_id]["status"] = "Blocked"
                            success, message = save_json_data(USERS_FILE, users_data)
                            if success:
                                st.success("User blocked successfully")
                                st.rerun()
                            else:
                                st.error(message)

                with col2:
                    # Reset password
                    if st.button("Reset Password"):
                        st.info("Password reset feature not implemented.")
            else:
                st.warning(f"Could not find data for user ID: {selected_user_id}")

def show_loan_approval():
    st.subheader("Loan Approval")
    
    # Get all users
    users = get_all_users()
    
    if not users:
        st.info("No users found")
        return
    
    # Create a list of pending loans
    pending_loans = []
    
    for user_id, user_data in users.items():
        if "loans" in user_data:
            for loan in user_data["loans"]:
                if loan.get("status") == "pending":
                    # Add user information to loan
                    loan_with_user = loan.copy()
                    loan_with_user["user_id"] = user_id
                    loan_with_user["user_name"] = user_data.get("full_name", "")
                    loan_with_user["user_email"] = user_data.get("email", "")
                    
                    pending_loans.append(loan_with_user)
    
    if not pending_loans:
        st.info("No pending loans found")
        return
    
    # Create DataFrame for display
    df = pd.DataFrame(pending_loans)
    
    # Format the DataFrame
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["application_date"] = df["timestamp"].dt.strftime("%Y-%m-%d")
        df["amount_formatted"] = df["amount"].apply(lambda x: f"₹{x:,.2f}")
        
        # Display pending loans in a table
        st.dataframe(df[["loan_id", "user_name", "type", "amount_formatted", "application_date"]])
        
        # Loan details
        st.subheader("Loan Details")
        
        # Select loan
        selected_loan_id = st.selectbox(
            "Select Loan",
            df["loan_id"].tolist(),
            format_func=lambda x: f"{df[df['loan_id'] == x]['user_name'].iloc[0]} - {df[df['loan_id'] == x]['type'].iloc[0]} - {df[df['loan_id'] == x]['amount_formatted'].iloc[0]}"
        )
        
        if selected_loan_id:
            # Get loan details
            loan_details = df[df["loan_id"] == selected_loan_id].iloc[0]
            
            # Display loan details
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<div class='loan-details'>", unsafe_allow_html=True)
                st.markdown("<h3>Loan Information</h3>", unsafe_allow_html=True)
                st.markdown(f"<p><strong>Loan ID:</strong> {loan_details.get('loan_id', '')}</p>", unsafe_allow_html=True)
                st.markdown(f"<p><strong>Loan Type:</strong> {loan_details.get('type', '')}</p>", unsafe_allow_html=True)
                st.markdown(f"<p><strong>Amount:</strong> ₹{loan_details.get('amount', 0):,.2f}</p>", unsafe_allow_html=True)
                st.markdown(f"<p><strong>Interest Rate:</strong> {loan_details.get('interest_rate', 0)}%</p>", unsafe_allow_html=True)
                st.markdown(f"<p><strong>Tenure:</strong> {loan_details.get('tenure', 0)} months</p>", unsafe_allow_html=True)
                st.markdown(f"<p><strong>EMI:</strong> ₹{loan_details.get('emi', 0):,.2f}</p>", unsafe_allow_html=True)
                st.markdown(f"<p><strong>Purpose:</strong> {loan_details.get('purpose', '')}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<div class='loan-details'>", unsafe_allow_html=True)
                st.markdown("<h3>Applicant Information</h3>", unsafe_allow_html=True)
                st.markdown(f"<p><strong>Name:</strong> {loan_details.get('user_name', '')}</p>", unsafe_allow_html=True)
                st.markdown(f"<p><strong>Email:</strong> {loan_details.get('user_email', '')}</p>", unsafe_allow_html=True)
                
                # Get user data
                user_data = load_user_data(loan_details.get('user_id', ''))
                
                if user_data:
                    st.markdown(f"<p><strong>Phone:</strong> {user_data.get('phone', '')}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>PAN:</strong> {user_data.get('pan', '')}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Aadhar:</strong> {user_data.get('aadhar', '')}</p>", unsafe_allow_html=True)
                    
                    # Get primary account
                    if "accounts" in user_data and len(user_data["accounts"]) > 0:
                        primary_account = user_data["accounts"][0]
                        st.markdown(f"<p><strong>Account Balance:</strong> ₹{primary_account.get('balance', 0):,.2f}</p>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Loan actions
            st.subheader("Loan Actions")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Approve loan
                if st.button("Approve Loan"):
                    success, message = update_loan_status(loan_details.get('user_id', ''), selected_loan_id, "approved")
                    
                    if success:
                        st.success("Loan approved successfully")
                        st.rerun()
                    else:
                        st.error(message)
            
            with col2:
                # Reject loan
                if st.button("Reject Loan"):
                    success, message = update_loan_status(loan_details.get('user_id', ''), selected_loan_id, "rejected")
                    
                    if success:
                        st.success("Loan rejected successfully")
                        st.rerun()
                    else:
                        st.error(message)

def show_transaction_monitoring():
    st.subheader("Transaction Monitoring")
    
    # Load transaction data directly from JSON file
    all_transactions_dict = load_json_data(TRANSACTIONS_FILE)
    users_data = load_json_data(USERS_FILE) # Need user data for names

    if not all_transactions_dict:
        st.info("No transactions found in transactions.json")
        return

    processed_transactions = []
    # Assuming transactions_data structure is {transaction_id: {user_id: ..., account_number: ..., amount: ..., type: ..., timestamp: ..., description: ...}}
    for tx_id, tx_data in all_transactions_dict.items():
        tx_copy = dict(tx_data)
        tx_copy['transaction_id'] = tx_id # Ensure transaction_id is present

        user_id = tx_copy.get('user_id')
        user_info = users_data.get(user_id, {}) if user_id else {}
        user_name = user_info.get("full_name", "Unknown User")

        tx_copy['user_name'] = user_name
        # Ensure essential fields have defaults if missing in JSON
        tx_copy.setdefault('account_number', 'N/A')
        tx_copy.setdefault('type', 'N/A')
        tx_copy.setdefault('amount', 0)
        tx_copy.setdefault('description', 'N/A')
        tx_copy.setdefault('timestamp', None) # Handle None timestamp later

        processed_transactions.append(tx_copy)

    if not processed_transactions:
        st.info("No transactions available to display.")
        return

    # Create DataFrame for display
    df = pd.DataFrame(processed_transactions)

    # Post-processing checks for DataFrame (optional but safer)
    if df.empty:
        st.info("No processable transactions found.")
        return

    # Ensure essential columns exist after DataFrame creation, assign defaults if needed
    for col in ['transaction_id', 'user_name', 'account_number', 'type', 'description']:
        if col not in df.columns: df[col] = 'N/A'
    if 'amount' not in df.columns: df['amount'] = 0
    if 'timestamp' not in df.columns: df['timestamp'] = pd.NaT # Use NaT for missing timestamps
    
    # Format the DataFrame
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["date"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M")
        df["amount_formatted"] = df.apply(
            lambda row: f"+₹{row['amount']:,.2f}" if row["type"] == "credit" else f"-₹{row['amount']:,.2f}",
            axis=1
        )
        
        # Sort by timestamp (newest first)
        df = df.sort_values("timestamp", ascending=False)
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Date range filter
            date_range = st.selectbox(
                "Date Range",
                ["All Time", "Today", "Last 7 Days", "Last 30 Days", "Custom"]
            )
            
            if date_range == "Custom":
                start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
                end_date = st.date_input("End Date", datetime.now())
            else:
                # Set date range based on selection
                end_date = datetime.now()
                if date_range == "Today":
                    start_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
                elif date_range == "Last 7 Days":
                    start_date = end_date - timedelta(days=7)
                elif date_range == "Last 30 Days":
                    start_date = end_date - timedelta(days=30)
                else:  # All Time
                    start_date = datetime.min
        
        with col2:
            # Transaction type filter
            transaction_type = st.selectbox(
                "Transaction Type",
                ["All", "Credit", "Debit"]
            )
        
        with col3:
            # Amount filter
            min_amount = st.number_input("Minimum Amount", min_value=0.0, step=1000.0)
            max_amount = st.number_input("Maximum Amount", min_value=0.0, step=1000.0)
        
        # Apply filters
        filtered_df = df.copy()
        
        # Apply date filter
        if date_range != "All Time":
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.max.time())
            filtered_df = filtered_df[(filtered_df["timestamp"] >= start_datetime) & (filtered_df["timestamp"] <= end_datetime)]
        
        # Apply transaction type filter
        if transaction_type != "All":
            filtered_df = filtered_df[filtered_df["type"].str.lower() == transaction_type.lower()]
        
        # Apply amount filter
        if min_amount > 0:
            filtered_df = filtered_df[filtered_df["amount"] >= min_amount]
        
        if max_amount > 0:
            filtered_df = filtered_df[filtered_df["amount"] <= max_amount]
        
        # Display transactions
        if filtered_df.empty:
            st.info("No transactions found matching the filters")
        else:
            # Display transaction count
            st.markdown(f"<p>Showing {len(filtered_df)} transactions</p>", unsafe_allow_html=True)
            
            # Display transactions in a table
            st.dataframe(filtered_df[["transaction_id", "user_name", "account_number", "type", "amount_formatted", "description", "date"]])
            
            # Transaction analytics
            st.subheader("Transaction Analytics")
            
            # Create charts for transaction analysis
            if not filtered_df.empty:
                # Group by date and type
                filtered_df["date_only"] = filtered_df["timestamp"].dt.date
                
                # Create summary by type
                type_summary = filtered_df.groupby("type")["amount"].sum().reset_index()
                
                # Create summary by date
                date_summary = filtered_df.groupby(["date_only", "type"])["amount"].sum().reset_index()
                
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
            
            # Flag suspicious transactions
            st.subheader("Suspicious Transactions")
            
            # Find large transactions (over ₹50,000)
            large_transactions = filtered_df[filtered_df["amount"] > 50000]
            
            if large_transactions.empty:
                st.info("No suspicious transactions found")
            else:
                st.warning(f"Found {len(large_transactions)} potentially suspicious transactions (over ₹50,000)")
                
                # Display suspicious transactions
                st.dataframe(large_transactions[["transaction_id", "user_name", "account_number", "type", "amount_formatted", "description", "date"]])

# Call the main function to display the page based on login status
show_admin_page()
