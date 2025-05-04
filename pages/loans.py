import streamlit as st

def show_offers():
    st.title("🌟 Current Loan Offers")
    st.markdown("Explore our limited-time offers on various loans and get the best deals!")

    # --- Welcome Offer Section ---
    st.markdown("## 🎉 Welcome Offer for New Customers")
    st.markdown("""
    - **Get up to ₹5,000 Cashback** on your first loan application of ₹10,000 or more.
    - **Waiver of First Loan Processing Fee** on any Personal/Home/Car Loan.
    - **Zero Account Maintenance Charges** for the first 6 months.
    """)

    st.markdown("---")

    # --- Loan Offers Section ---
    st.markdown("## 💰 Special Loan Offers")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 🚗 Car Loan Offer")
        st.markdown("""
        - Interest Rate: **6.99% p.a.** (Limited Period)
        - Processing Fee Waiver
        - Flexible Tenure from 1 to 7 years
        """)
        if st.button("Apply for Car Loan", key="car_loan"):
            st.success("Redirecting you to Car Loan Application...")

    with col2:
        st.markdown("#### 🏠 Home Loan Offer")
        st.markdown("""
        - Interest Rate: **6.50% p.a.** (Capped)
        - Free CIBIL Score Check
        - Up to ₹25,000 Waiver on Processing Fees
        """)
        if st.button("Apply for Home Loan", key="home_loan"):
            st.success("Redirecting you to Home Loan Application...")

    with col3:
        st.markdown("#### 💼 Personal Loan Offer")
        st.markdown("""
        - Instant Approval up to ₹10 Lakh
        - Interest Rate: **9.99% p.a.**
        - No Documentation Required for loans under ₹2 Lakh
        """)
        if st.button("Apply for Personal Loan", key="personal_loan"):
            st.success("Redirecting you to Personal Loan Application...")

    # --- Additional Info ---
    st.markdown("---")
    st.markdown("For more details or to apply, visit the **Loans** section or contact our support team.")

# To test this independently
if __name__ == "__main__":
    show_offers()