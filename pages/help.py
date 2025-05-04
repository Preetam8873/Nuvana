import streamlit as st
import pandas as pd
from datetime import datetime

def show_help():
    st.title("Help & Support")
    
    # Create tabs for different help sections
    tab1, tab2, tab3 = st.tabs(["FAQ", "Contact Us", "User Guide"])
    
    with tab1:
        show_faq()
    
    with tab2:
        show_contact_form()
    
    with tab3:
        show_user_guide()

def show_faq():
    st.subheader("Frequently Asked Questions")
    
    # FAQ categories
    categories = [
        "Account Management",
        "Transactions",
        "Loans",
        "Security",
        "Mobile Banking"
    ]
    
    # Select category
    category = st.selectbox("Select Category", categories)
    
    # FAQ questions and answers
    faqs = {
        "Account Management": [
            {
                "question": "How do I open a new account?",
                "answer": "To open a new account, click on the 'Register' button on the login page and fill in the required details. You'll need to provide your personal information, ID proof, and make an initial deposit."
            },
            {
                "question": "How can I update my personal information?",
                "answer": "You can update your personal information by going to Settings > Profile. From there, you can edit your phone number and address."
            },
            {
                "question": "What types of accounts does Nuvana Bank offer?",
                "answer": "Nuvana Bank offers Savings, Current, and Salary account types. Each account type has different features and benefits tailored to specific needs."
            },
            {
                "question": "How do I check my account balance?",
                "answer": "Your account balance is displayed on the Dashboard page. You can also view it in the sidebar of the application."
            },
            {
                "question": "Is there a minimum balance requirement?",
                "answer": "Yes, different account types have different minimum balance requirements. Savings accounts typically require a minimum balance of ₹1,000."
            }
        ],
        "Transactions": [
            {
                "question": "How do I transfer money to another account?",
                "answer": "To transfer money, go to the Transactions tab and select 'Transfer Money'. Enter the recipient's account number, name, amount, and description, then click 'Transfer'."
            },
            {
                "question": "Is there a limit on transaction amounts?",
                "answer": "Yes, there are daily and per-transaction limits for security purposes. The standard limit is ₹1,00,000 per day for online transfers."
            },
            {
                "question": "How long does it take for a transfer to be processed?",
                "answer": "Internal transfers (within Nuvana Bank) are processed immediately. External transfers may take 1-2 business days depending on the recipient's bank."
            },
            {
                "question": "How can I view my transaction history?",
                "answer": "You can view your transaction history by going to the Transactions tab and selecting 'Transaction History'. You can filter transactions by date, type, and amount."
            },
            {
                "question": "Can I schedule recurring transfers?",
                "answer": "This feature is coming soon. Currently, you can only make one-time transfers."
            }
        ],
        "Loans": [
            {
                "question": "What types of loans does Nuvana Bank offer?",
                "answer": "Nuvana Bank offers Personal Loans, Home Loans, Car Loans, Education Loans, and Business Loans with competitive interest rates."
            },
            {
                "question": "How do I apply for a loan?",
                "answer": "To apply for a loan, go to the Loans tab and select 'Apply for Loan'. Fill in the required details and submit your application."
            },
            {
                "question": "How long does the loan approval process take?",
                "answer": "The loan approval process typically takes 2-3 business days. You'll be notified via email once your loan is approved or rejected."
            },
            {
                "question": "How is the EMI calculated?",
                "answer": "EMI is calculated based on the loan amount, interest rate, and tenure. You can use our EMI Calculator to estimate your monthly payments."
            },
            {
                "question": "Can I repay my loan early?",
                "answer": "Yes, you can repay your loan early. However, some loan types may have prepayment penalties. Please check the loan terms for details."
            }
        ],
        "Security": [
            {
                "question": "How secure is online banking with Nuvana Bank?",
                "answer": "Nuvana Bank uses industry-standard encryption and security measures to protect your data. We also offer two-factor authentication for added security."
            },
            {
                "question": "What is two-factor authentication (2FA)?",
                "answer": "Two-factor authentication adds an extra layer of security by requiring a one-time password (OTP) in addition to your regular password when logging in."
            },
            {
                "question": "How do I enable two-factor authentication?",
                "answer": "You can enable two-factor authentication by going to Settings > Security and clicking on 'Enable 2FA'."
            },
            {
                "question": "What should I do if I suspect unauthorized access to my account?",
                "answer": "If you suspect unauthorized access, immediately change your password and contact our customer support. You can also use the 'Logout from All Devices' feature in Settings > Security."
            },
            {
                "question": "How often should I change my password?",
                "answer": "We recommend changing your password every 3 months for optimal security. Always use a strong password with a mix of letters, numbers, and special characters."
            }
        ],
        "Mobile Banking": [
            {
                "question": "Is there a mobile app for Nuvana Bank?",
                "answer": "Yes, Nuvana Bank offers a mobile app for both Android and iOS devices. You can download it from the Google Play Store or Apple App Store."
            },
            {
                "question": "What features are available on the mobile app?",
                "answer": "The mobile app offers all the features available on the web platform, including account management, transfers, loan applications, and more."
            },
            {
                "question": "How do I reset my password on the mobile app?",
                "answer": "You can reset your password on the mobile app by clicking on 'Forgot Password' on the login screen and following the instructions."
            },
            {
                "question": "Is the mobile app secure?",
                "answer": "Yes, the mobile app uses the same security measures as the web platform, including encryption and two-factor authentication."
            },
            {
                "question": "Can I use biometric authentication on the mobile app?",
                "answer": "Yes, the mobile app supports biometric authentication including fingerprint and face recognition for supported devices, making login faster and more secure."
            }
        ]
    }
    
    # Display FAQs for selected category
    if category in faqs:
        for faq in faqs[category]:
            with st.expander(faq["question"]):
                st.markdown(faq["answer"])
    
    # Can't find answer section
    st.markdown("---")
    st.markdown("### Can't find what you're looking for?")
    st.markdown("Contact our customer support team for assistance.")
    
    if st.button("Contact Support"):
        st.session_state.current_tab = "Contact Us"
        st.rerun()

def show_contact_form():
    st.subheader("Contact Us")
    
    # Contact information
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='contact-info'>", unsafe_allow_html=True)
        st.markdown("<h3>Customer Support</h3>", unsafe_allow_html=True)
        st.markdown("<p><strong>Phone:</strong> 1800-123-4567 (Toll Free)</p>", unsafe_allow_html=True)
        st.markdown("<p><strong>Email:</strong> support@nuvanabank.com</p>", unsafe_allow_html=True)
        st.markdown("<p><strong>Hours:</strong> 24x7 (All days)</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='contact-info'>", unsafe_allow_html=True)
        st.markdown("<h3>Head Office</h3>", unsafe_allow_html=True)
        st.markdown("<p><strong>Address:</strong> Nuvana Tower, 123 Financial Street, Mumbai 400001</p>", unsafe_allow_html=True)
        st.markdown("<p><strong>Phone:</strong> +91-22-1234-5678</p>", unsafe_allow_html=True)
        st.markdown("<p><strong>Email:</strong> info@nuvanabank.com</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Contact form
    st.markdown("### Submit a Support Ticket")
    
    with st.form("contact_form"):
        # Form fields
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        
        # Issue type
        issue_type = st.selectbox(
            "Issue Type",
            ["Account Issue", "Transaction Problem", "Loan Inquiry", "Technical Support", "Feedback", "Other"]
        )
        
        # Message
        message = st.text_area("Message")
        
        # Priority
        priority = st.select_slider(
            "Priority",
            options=["Low", "Medium", "High", "Urgent"]
        )
        
        # Submit button
        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            if not name or not email or not message:
                st.error("Please fill in all required fields")
            else:
                # In a real application, this would send the support ticket
                st.success("Support ticket submitted successfully. Our team will contact you shortly.")
                
                # Display ticket details
                st.markdown("<h3>Ticket Details</h3>", unsafe_allow_html=True)
                st.markdown("<div class='ticket-details'>", unsafe_allow_html=True)
                st.markdown(f"<p><strong>Ticket ID:</strong> TKT{datetime.now().strftime('%Y%m%d%H%M%S')}</p>", unsafe_allow_html=True)
                st.markdown(f"<p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>", unsafe_allow_html=True)
                st.markdown(f"<p><strong>Name:</strong> {name}</p>", unsafe_allow_html=True)
                st.markdown(f"<p><strong>Email:</strong> {email}</p>", unsafe_allow_html=True)
                st.markdown(f"<p><strong>Phone:</strong> {phone}</p>", unsafe_allow_html=True)
                st.markdown(f"<p><strong>Issue Type:</strong> {issue_type}</p>", unsafe_allow_html=True)
                st.markdown(f"<p><strong>Priority:</strong> {priority}</p>", unsafe_allow_html=True)
                st.markdown(f"<p><strong>Message:</strong> {message}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

def show_user_guide():
    st.subheader("User Guide")
    
    # User guide sections
    sections = [
        "Getting Started",
        "Dashboard",
        "Transactions",
        "Loans",
        "Settings",
        "Security Best Practices"
    ]
    
    # Select section
    section = st.selectbox("Select Section", sections)
    
    # Display selected section
    if section == "Getting Started":
        st.markdown("### Getting Started with Nuvana Bank")
        st.markdown("""
        Welcome to Nuvana Bank! This guide will help you get started with our online banking platform.
        
        #### Registration
        1. Click on the 'Register' button on the login page
        2. Fill in your personal details, including name, email, phone, address, PAN, and Aadhar
        3. Choose your account type and make an initial deposit
        4. Create a secure password
        5. Agree to the terms and conditions
        6. Submit your application
        
        #### Login
        1. Enter your email and password on the login page
        2. If you have enabled two-factor authentication, enter the OTP sent to your email
        3. You will be redirected to your dashboard
        
        #### Navigation
        - Use the sidebar menu to navigate between different sections
        - Your account balance is always visible in the sidebar
        - You can change the theme (Light/Dark) from the sidebar
        - Use the logout button in the sidebar to securely log out
        """)
    
    elif section == "Dashboard":
        st.markdown("### Dashboard Guide")
        st.markdown("""
        The dashboard provides an overview of your account and recent activities.
        
        #### Account Summary
        - View your current balance
        - See your account details
        - Access quick actions like transfers and loan applications
        
        #### Recent Transactions
        - View your 5 most recent transactions
        - Click on 'View All Transactions' to see your complete transaction history
        
        #### Spending Analytics
        - View your spending patterns by category
        - See pie and bar charts visualizing your spending habits
        
        #### Loan Summary
        - View your active loans
        - See loan status, amount, and other details
        - Click on 'View All Loans' to see your complete loan history
        """)
    
    elif section == "Transactions":
        st.markdown("### Transactions Guide")
        st.markdown("""
        The Transactions section allows you to manage all your money movements.
        
        #### Transaction History
        - View all your past transactions
        - Filter transactions by date, type, and amount
        - Sort transactions by different criteria
        - Download transaction statements in PDF or CSV format
        
        #### Transfer Money
        - Transfer funds to other accounts
        - Enter recipient's account number and name
        - Specify the amount and add a description
        - Review and confirm the transfer
        - Get a transaction receipt after successful transfer
        
        #### Mini Statement
        - View your last 5 transactions
        - See a summary of your account details
        - Download a mini statement for quick reference
        """)
    
    elif section == "Loans":
        st.markdown("### Loans Guide")
        st.markdown("""
        The Loans section helps you manage existing loans and apply for new ones.
        
        #### My Loans
        - View all your existing loans
        - See loan details including amount, interest rate, tenure, and EMI
        - Check loan status (pending, approved, rejected)
        - View EMI schedule for approved loans
        
        #### Apply for Loan
        - Select the loan type (Personal, Home, Car, Education, Business)
        - Specify the loan amount and tenure
        - View the applicable interest rate and calculated EMI
        - Provide the purpose of the loan
        - Submit your application
        
        #### EMI Calculator
        - Calculate EMI for different loan scenarios
        - Adjust loan amount, interest rate, and tenure
        - View detailed EMI breakdown
        - See amortization schedule
        - Visualize loan repayment through charts
        """)
    
    elif section == "Settings":
        st.markdown("### Settings Guide")
        st.markdown("""
        The Settings section allows you to manage your profile, security, and preferences.
        
        #### Profile Settings
        - View your personal and account information
        - Update your phone number and address
        - Other personal details like name, email, PAN, and Aadhar can only be updated by contacting customer support
        
        #### Security Settings
        - Change your password
        - Enable or disable two-factor authentication
        - Logout from all devices
        
        #### Preferences
        - Change the theme (Light/Dark)
        - Manage notification preferences for email and SMS
        """)
    
    elif section == "Security Best Practices":
        st.markdown("### Security Best Practices")
        st.markdown("""
        Follow these best practices to keep your account secure:
        
        #### Password Security
        - Use a strong password with at least 8 characters
        - Include a mix of uppercase and lowercase letters, numbers, and special characters
        - Change your password regularly (every 3 months)
        - Never share your password with anyone
        
        #### Two-Factor Authentication
        - Enable two-factor authentication for an extra layer of security
        - Always verify the OTP before entering it
        - Never share your OTP with anyone, even bank staff
        
        #### Safe Banking Habits
        - Always log out after your banking session
        - Use the 'Logout from All Devices' feature if you suspect unauthorized access
        - Regularly check your transaction history for any suspicious activities
        - Update your contact information to receive transaction alerts
        
        #### Device Security
        - Use updated antivirus software on your device
        - Avoid using public Wi-Fi for banking
        - Keep your browser and operating system updated
        - Clear your browser cache after banking sessions on shared computers
        """)
    
    # Download user guide
    if st.button("Download Complete User Guide"):
        st.info("Generating user guide PDF... (This is a demo feature)")
