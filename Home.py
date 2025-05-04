import streamlit as st
import json
import os
import hashlib
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import random
import time

# Set page configuration
st.set_page_config(
    page_title="Nuvana Bank",
    page_icon="🏦",
    layout="centered",  # Change from "wide" to "centered"
    initial_sidebar_state="expanded"
)

# Custom CSS for elegant UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #1E3A8A;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f8fafc;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 1rem;
    }
    .success-msg {
        padding: 0.75rem;
        border-radius: 0.25rem;
        background-color: #d1fae5;
        color: #065f46;
        margin-bottom: 1rem;
    }
    .error-msg {
        padding: 0.75rem;
        border-radius: 0.25rem;
        background-color: #fee2e2;
        color: #b91c1c;
        margin-bottom: 1rem;
    }
    .info-msg {
        padding: 0.75rem;
        border-radius: 0.25rem;
        background-color: #e0f2fe;
        color: #0369a1;
        margin-bottom: 1rem;
    }
    .btn-primary {
        background-color: #1E3A8A;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        border: none;
        cursor: pointer;
    }
    .btn-secondary {
        background-color: #6b7280;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        border: none;
        cursor: pointer;
    }
    .sidebar .sidebar-content {
        background-color: #1E3A8A;
        color: white;
        width: 200px; /* Adjust this value to make the sidebar narrower */
    }
    .account-balance {
        font-size: 2rem;
        font-weight: 700;
        color: #1E3A8A;
    }
    .transaction {
        padding: 0.75rem;
        border-bottom: 1px solid #e5e7eb;
    }
    .transaction-amount-credit {
        color: #047857;
        font-weight: 600;
    }
    .transaction-amount-debit {
        color: #b91c1c;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = "login"
if 'notification' not in st.session_state:
    st.session_state.notification = None
if 'notification_type' not in st.session_state:
    st.session_state.notification_type = None

# File paths
DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
ACCOUNTS_FILE = os.path.join(DATA_DIR, "accounts.json")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.json")

# Create data directory if it doesn't exist
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Initialize data files if they don't exist
def initialize_data_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump({}, f)
    
    if not os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'w') as f:
            json.dump({}, f)
    
    if not os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, 'w') as f:
            json.dump({}, f)

initialize_data_files()

# Helper functions
def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

def load_data(file_path):
    """Load data from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(data, file_path):
    """Save data to a JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def register_user(username, password, email, full_name, address, phone):
    """Register a new user."""
    users = load_data(USERS_FILE)
    
    if username in users:
        return False, "Username already exists"
    
    users[username] = {
        "password": hash_password(password),
        "email": email,
        "full_name": full_name,
        "address": address,
        "phone": phone,
        "created_at": datetime.datetime.now().isoformat()
    }
    
    save_data(users, USERS_FILE)
    
    # Create an account for the user
    accounts = load_data(ACCOUNTS_FILE)
    account_number = f"NB{random.randint(10000000, 99999999)}"
    
    accounts[username] = {
        "account_number": account_number,
        "balance": 0,
        "account_type": "Savings",
        "status": "Active",
        "created_at": datetime.datetime.now().isoformat()
    }
    
    save_data(accounts, ACCOUNTS_FILE)
    
    return True, "Registration successful"

def authenticate_user(username, password):
    """Authenticate a user."""
    users = load_data(USERS_FILE)
    
    if username not in users:
        return False, "Invalid username or password"
    
    if users[username]["password"] != hash_password(password):
        return False, "Invalid username or password"
    
    return True, "Login successful"

def get_account_details(username):
    """Get account details for a user."""
    accounts = load_data(ACCOUNTS_FILE)
    
    if username not in accounts:
        return None
    
    return accounts[username]

def get_user_details(username):
    """Get user details."""
    users = load_data(USERS_FILE)
    
    if username not in users:
        return None
    
    user_data = users[username].copy()
    user_data.pop("password", None)  # Remove password for security
    
    return user_data

def get_transactions(username):
    """Get transactions for a user."""
    transactions = load_data(TRANSACTIONS_FILE)
    
    if username not in transactions:
        return []
    
    return transactions[username]

def add_transaction(username, transaction_type, amount, description):
    """Add a transaction for a user."""
    transactions = load_data(TRANSACTIONS_FILE)
    
    if username not in transactions:
        transactions[username] = []
    
    transaction = {
        "id": len(transactions[username]) + 1,
        "type": transaction_type,
        "amount": amount,
        "description": description,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    transactions[username].append(transaction)
    save_data(transactions, TRANSACTIONS_FILE)
    
    # Update account balance
    accounts = load_data(ACCOUNTS_FILE)
    
    if transaction_type == "credit":
        accounts[username]["balance"] += amount
    else:
        accounts[username]["balance"] -= amount
    
    save_data(accounts, ACCOUNTS_FILE)

def calculate_emi(principal, rate, time):
    """Calculate EMI."""
    rate = rate / (12 * 100)  # Monthly interest rate
    time = time * 12  # Total number of months
    
    emi = (principal * rate * (1 + rate) ** time) / ((1 + rate) ** time - 1)
    
    return emi

# Navigation functions
def navigate_to(page):
    st.session_state.current_page = page

def show_notification(message, type="info"):
    st.session_state.notification = message
    st.session_state.notification_type = type

# UI Components
def display_header():
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image("https://via.placeholder.com/150x150.png?text=NB", width=100)
    
    with col2:
        st.markdown('<h1 class="main-header">Nuvana Bank</h1>', unsafe_allow_html=True)
        st.markdown('<p>Your Trusted Financial Partner</p>', unsafe_allow_html=True)

def display_notification():
    if st.session_state.notification:
        if st.session_state.notification_type == "success":
            st.markdown(f'<div class="success-msg">{st.session_state.notification}</div>', unsafe_allow_html=True)
        elif st.session_state.notification_type == "error":
            st.markdown(f'<div class="error-msg">{st.session_state.notification}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="info-msg">{st.session_state.notification}</div>', unsafe_allow_html=True)
        
        # Clear notification after displaying
        st.session_state.notification = None
        st.session_state.notification_type = None

def display_sidebar():
    with st.sidebar:
        st.markdown('<h2 style="color: white;">Nuvana Bank</h2>', unsafe_allow_html=True)
        
        if st.session_state.logged_in:
            st.markdown(f'<p style="color: white;">Welcome, {st.session_state.username}</p>', unsafe_allow_html=True)
            
            if st.button("Home"):
                navigate_to("dashboard")
            
            if st.button("Account Details"):
                navigate_to("account_details")
            
            if st.button("Transactions"):
                navigate_to("transactions")
            
            if st.button("Transfer Money"):
                navigate_to("transfer")
            
            if st.button("EMI Calculator"):
                navigate_to("emi_calculator")
            
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.username = ""
                navigate_to("login")
                show_notification("Logged out successfully", "success")
        else:
            if st.button("Login"):
                navigate_to("login")
            
            if st.button("Register"):
                navigate_to("register")

# Page functions
def login_page():
    st.markdown('<h2 class="sub-header">Login to Your Account</h2>', unsafe_allow_html=True)
    
    # Use a single column for the form to make it narrower
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if not username or not password:
                show_notification("Please fill in all fields", "error")
            else:
                success, message = authenticate_user(username, password)
                
                if success:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    navigate_to("dashboard")
                    show_notification(message, "success")
                else:
                    show_notification(message, "error")
    
    st.markdown("Don't have an account? [Register here](#)")
    if st.button("Create New Account"):
        navigate_to("register")

def register_page():
    st.markdown('<h2 class="sub-header">Open a New Account</h2>', unsafe_allow_html=True)
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone Number")
        
        with col2:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
        
        address = st.text_area("Address")
        
        terms = st.checkbox("I agree to the terms and conditions")
        
        submit_button = st.form_submit_button("Register")
        
        if submit_button:
            if not all([full_name, email, phone, username, password, confirm_password, address]):
                show_notification("Please fill in all fields", "error")
            elif password != confirm_password:
                show_notification("Passwords do not match", "error")
            elif not terms:
                show_notification("Please agree to the terms and conditions", "error")
            else:
                success, message = register_user(username, password, email, full_name, address, phone)
                
                if success:
                    navigate_to("login")
                    show_notification(message, "success")
                else:
                    show_notification(message, "error")
    
    st.markdown("Already have an account? [Login here](#)")
    if st.button("Login to Existing Account"):
        navigate_to("login")

def dashboard_page():
    st.markdown('<h2 class="sub-header">Dashboard</h2>', unsafe_allow_html=True)
    
    account = get_account_details(st.session_state.username)
    
    if not account:
        show_notification("Account not found", "error")
        navigate_to("login")
        return
    
    # Account Overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3>Account Overview</h3>', unsafe_allow_html=True)
        st.markdown(f'<p>Account Number: {account["account_number"]}</p>', unsafe_allow_html=True)
        st.markdown(f'<p>Account Type: {account["account_type"]}</p>', unsafe_allow_html=True)
        st.markdown(f'<p>Status: {account["status"]}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3>Current Balance</h3>', unsafe_allow_html=True)
        st.markdown(f'<p class="account-balance">₹{account["balance"]:,.2f}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown('<h3>Quick Actions</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h4>Transfer Money</h4>', unsafe_allow_html=True)
        st.markdown('<p>Send money to another account</p>', unsafe_allow_html=True)
        if st.button("Transfer", key="transfer_btn"):
            navigate_to("transfer")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h4>EMI Calculator</h4>', unsafe_allow_html=True)
        st.markdown('<p>Calculate your loan EMI</p>', unsafe_allow_html=True)
        if st.button("Calculate", key="emi_btn"):
            navigate_to("emi_calculator")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h4>View Transactions</h4>', unsafe_allow_html=True)
        st.markdown('<p>Check your recent transactions</p>', unsafe_allow_html=True)
        if st.button("View", key="transactions_btn"):
            navigate_to("transactions")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent Transactions
    st.markdown('<h3>Recent Transactions</h3>', unsafe_allow_html=True)
    
    transactions = get_transactions(st.session_state.username)
    
    if not transactions:
        st.info("No transactions found")
    else:
        # Display only the 5 most recent transactions
        recent_transactions = sorted(transactions, key=lambda x: x["timestamp"], reverse=True)[:5]
        
        for transaction in recent_transactions:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f'<div class="transaction">', unsafe_allow_html=True)
                st.markdown(f'<p>{transaction["description"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p style="font-size: 0.8rem; color: #6b7280;">{transaction["timestamp"]}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown(f'<div class="transaction">', unsafe_allow_html=True)
                if transaction["type"] == "credit":
                    st.markdown(f'<p class="transaction-amount-credit">+₹{transaction["amount"]:,.2f}</p>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<p class="transaction-amount-debit">-₹{transaction["amount"]:,.2f}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown(f'<div class="transaction">', unsafe_allow_html=True)
                st.markdown(f'<p>{transaction["type"].capitalize()}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

def account_details_page():
    st.markdown('<h2 class="sub-header">Account Details</h2>', unsafe_allow_html=True)
    
    account = get_account_details(st.session_state.username)
    user = get_user_details(st.session_state.username)
    
    if not account or not user:
        show_notification("Account not found", "error")
        navigate_to("login")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3>Personal Information</h3>', unsafe_allow_html=True)
        st.markdown(f'<p><strong>Name:</strong> {user["full_name"]}</p>', unsafe_allow_html=True)
        st.markdown(f'<p><strong>Email:</strong> {user["email"]}</p>', unsafe_allow_html=True)
        st.markdown(f'<p><strong>Phone:</strong> {user["phone"]}</p>', unsafe_allow_html=True)
        st.markdown(f'<p><strong>Address:</strong> {user["address"]}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3>Account Information</h3>', unsafe_allow_html=True)
        st.markdown(f'<p><strong>Account Number:</strong> {account["account_number"]}</p>', unsafe_allow_html=True)
        st.markdown(f'<p><strong>Account Type:</strong> {account["account_type"]}</p>', unsafe_allow_html=True)
        st.markdown(f'<p><strong>Status:</strong> {account["status"]}</p>', unsafe_allow_html=True)
        st.markdown(f'<p><strong>Opening Date:</strong> {account["created_at"]}</p>', unsafe_allow_html=True)
        st.markdown(f'<p><strong>Current Balance:</strong> ₹{account["balance"]:,.2f}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Edit Profile
    st.markdown('<h3>Edit Profile</h3>', unsafe_allow_html=True)
    
    with st.form("edit_profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            email = st.text_input("Email", value=user["email"])
            phone = st.text_input("Phone", value=user["phone"])
        
        with col2:
            address = st.text_area("Address", value=user["address"])
        
        submit_button = st.form_submit_button("Update Profile")
        
        if submit_button:
            # Update user details
            users = load_data(USERS_FILE)
            users[st.session_state.username]["email"] = email
            users[st.session_state.username]["phone"] = phone
            users[st.session_state.username]["address"] = address
            
            save_data(users, USERS_FILE)
            
            show_notification("Profile updated successfully", "success")

def transactions_page():
    st.markdown('<h2 class="sub-header">Transaction History</h2>', unsafe_allow_html=True)
    
    transactions = get_transactions(st.session_state.username)
    
    if not transactions:
        st.info("No transactions found")
        return
    
    # Filter options
    col1, col2 = st.columns(2)
    
    with col1:
        transaction_type = st.selectbox("Filter by Type", ["All", "Credit", "Debit"])
    
    with col2:
        sort_by = st.selectbox("Sort by", ["Newest First", "Oldest First", "Amount (High to Low)", "Amount (Low to High)"])
    
    # Apply filters
    filtered_transactions = transactions.copy()
    
    if transaction_type != "All":
        filtered_transactions = [t for t in filtered_transactions if t["type"].lower() == transaction_type.lower()]
    
    # Apply sorting
    if sort_by == "Newest First":
        filtered_transactions = sorted(filtered_transactions, key=lambda x: x["timestamp"], reverse=True)
    elif sort_by == "Oldest First":
        filtered_transactions = sorted(filtered_transactions, key=lambda x: x["timestamp"])
    elif sort_by == "Amount (High to Low)":
        filtered_transactions = sorted(filtered_transactions, key=lambda x: x["amount"], reverse=True)
    elif sort_by == "Amount (Low to High)":
        filtered_transactions = sorted(filtered_transactions, key=lambda x: x["amount"])
    
    # Display transactions
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    for transaction in filtered_transactions:
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f'<div class="transaction">', unsafe_allow_html=True)
            st.markdown(f'<p>{transaction["description"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="font-size: 0.8rem; color: #6b7280;">{transaction["timestamp"]}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<div class="transaction">', unsafe_allow_html=True)
            if transaction["type"] == "credit":
                st.markdown(f'<p class="transaction-amount-credit">+₹{transaction["amount"]:,.2f}</p>', unsafe_allow_html=True)
            else:
                st.markdown(f'<p class="transaction-amount-debit">-₹{transaction["amount"]:,.2f}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'<div class="transaction">', unsafe_allow_html=True)
            st.markdown(f'<p>{transaction["type"].capitalize()}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Transaction Summary
    st.markdown('<h3>Transaction Summary</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Calculate total credits and debits
        total_credits = sum(t["amount"] for t in transactions if t["type"] == "credit")
        total_debits = sum(t["amount"] for t in transactions if t["type"] == "debit")
        
        # Create a pie chart
        fig, ax = plt.subplots()
        ax.pie([total_credits, total_debits], labels=["Credits", "Debits"], autopct='%1.1f%%', colors=["#047857", "#b91c1c"])
        ax.set_title("Credits vs Debits")
        st.pyplot(fig)
    
    with col2:
        # Create a bar chart of recent transactions
        recent_transactions = sorted(transactions, key=lambda x: x["timestamp"], reverse=True)[:5]
        
        amounts = []
        labels = []
        colors = []
        
        for t in recent_transactions:
            if t["type"] == "credit":
                amounts.append(t["amount"])
                colors.append("#047857")
            else:
                amounts.append(-t["amount"])
                colors.append("#b91c1c")
            
            # Truncate description if too long
            desc = t["description"]
            if len(desc) > 15:
                desc = desc[:12] + "..."
            
            labels.append(desc)
        
        fig, ax = plt.subplots()
        ax.bar(labels, amounts, color=colors)
        ax.set_title("Recent Transactions")
        ax.set_xticklabels(labels, rotation=45, ha="right")
        st.pyplot(fig)

def transfer_page():
    st.markdown('<h2 class="sub-header">Transfer Money</h2>', unsafe_allow_html=True)
    
    account = get_account_details(st.session_state.username)
    
    if not account:
        show_notification("Account not found", "error")
        navigate_to("login")
        return
    
    st.markdown(f'<p>Current Balance: <span class="account-balance">₹{account["balance"]:,.2f}</span></p>', unsafe_allow_html=True)
    
    with st.form("transfer_form"):
        recipient_account = st.text_input("Recipient Account Number")
        amount = st.number_input("Amount", min_value=1.0, step=100.0)
        description = st.text_input("Description")
        
        submit_button = st.form_submit_button("Transfer")
        
        if submit_button:
            if not recipient_account or amount <= 0:
                show_notification("Please fill in all fields with valid values", "error")
            elif amount > account["balance"]:
                show_notification("Insufficient balance", "error")
            else:
                # Add debit transaction for sender
                add_transaction(st.session_state.username, "debit", amount, f"Transfer to {recipient_account}: {description}")
                
                # For demo purposes, we'll just show a success message
                # In a real app, you would verify the recipient account and add a credit transaction for them
                show_notification(f"Successfully transferred ₹{amount:,.2f} to {recipient_account}", "success")
                
                # Refresh the page to show updated balance
                st.experimental_rerun()
    
    # Quick Transfer
    st.markdown('<h3>Quick Add Money (Demo)</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Add ₹1,000"):
            add_transaction(st.session_state.username, "credit", 1000, "Quick Add")
            show_notification("Added ₹1,000 to your account", "success")
            st.experimental_rerun()
    
    with col2:
        if st.button("Add ₹5,000"):
            add_transaction(st.session_state.username, "credit", 5000, "Quick Add")
            show_notification("Added ₹5,000 to your account", "success")
            st.experimental_rerun()
    
    with col3:
        if st.button("Add ₹10,000"):
            add_transaction(st.session_state.username, "credit", 10000, "Quick Add")
            show_notification("Added ₹10,000 to your account", "success")
            st.experimental_rerun()

def emi_calculator_page():
    st.markdown('<h2 class="sub-header">EMI Calculator</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        loan_amount = st.slider("Loan Amount (₹)", 10000, 10000000, 1000000, step=10000)
        interest_rate = st.slider("Interest Rate (%)", 1.0, 20.0, 8.5, step=0.1)
        loan_term = st.slider("Loan Term (Years)", 1, 30, 20, step=1)
        
        if st.button("Calculate EMI"):
            emi = calculate_emi(loan_amount, interest_rate, loan_term)
            total_payment = emi * loan_term * 12
            total_interest = total_payment - loan_amount
            
            st.markdown(f'<p class="account-balance">Monthly EMI: ₹{emi:,.2f}</p>', unsafe_allow_html=True)
            st.markdown(f'<p>Total Payment: ₹{total_payment:,.2f}</p>', unsafe_allow_html=True)
            st.markdown(f'<p>Total Interest: ₹{total_interest:,.2f}</p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3>EMI Breakdown</h3>', unsafe_allow_html=True)
        
        # Create a pie chart for EMI breakdown
        fig, ax = plt.subplots()
        
        # Calculate values for the chart
        emi = calculate_emi(loan_amount, interest_rate, loan_term)
        total_payment = emi * loan_term * 12
        total_interest = total_payment - loan_amount
        
        ax.pie([loan_amount, total_interest], labels=["Principal", "Interest"], autopct='%1.1f%%', colors=["#1E3A8A", "#6b7280"])
        ax.set_title("Loan Breakdown")
        st.pyplot(fig)
        
        # Create a line chart for amortization
        principal_remaining = loan_amount
        interest_paid = 0
        principal_paid = 0
        
        years = list(range(1, loan_term + 1))
        principal_values = []
        interest_values = []
        
        for year in years:
            for _ in range(12):  # 12 months in a year
                interest_for_month = principal_remaining * (interest_rate / (12 * 100))
                principal_for_month = emi - interest_for_month
                
                principal_remaining -= principal_for_month
                interest_paid += interest_for_month
                principal_paid += principal_for_month
            
            principal_values.append(principal_paid)
            interest_values.append(interest_paid)
        
        fig, ax = plt.subplots()
        ax.plot(years, principal_values, label="Principal Paid")
        ax.plot(years, interest_values, label="Interest Paid")
        ax.set_xlabel("Years")
        ax.set_ylabel("Amount (₹)")
        ax.set_title("Amortization Schedule")
        ax.legend()
        st.pyplot(fig)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Main app
def main():
    display_header()
    display_notification()
    display_sidebar()
    
    # Display the current page
    if st.session_state.current_page == "login":
        login_page()
    elif st.session_state.current_page == "register":
        register_page()
    elif st.session_state.current_page == "dashboard":
        if not st.session_state.logged_in:
            navigate_to("login")
            show_notification("Please login to continue", "info")
        else:
            dashboard_page()
    elif st.session_state.current_page == "account_details":
        if not st.session_state.logged_in:
            navigate_to("login")
            show_notification("Please login to continue", "info")
        else:
            account_details_page()
    elif st.session_state.current_page == "transactions":
        if not st.session_state.logged_in:
            navigate_to("login")
            show_notification("Please login to continue", "info")
        else:
            transactions_page()
    elif st.session_state.current_page == "transfer":
        if not st.session_state.logged_in:
            navigate_to("login")
            show_notification("Please login to continue", "info")
        else:
            transfer_page()
    elif st.session_state.current_page == "emi_calculator":
        if not st.session_state.logged_in:
            navigate_to("login")
            show_notification("Please login to continue", "info")
        else:
            emi_calculator_page()

if __name__ == "__main__":
    main()
