import streamlit as st

st.title("Contact Us")

# Contact form
with st.form("contact_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    message = st.text_area("Message")
    submit_button = st.form_submit_button("Send")

    if submit_button:
        if not all([name, email, message]):
            st.error("Please fill in all fields.")
        else:
            st.success("Thank you for your message!")

# Address details
st.subheader("Our Address")
st.markdown("123 Bank Street, Finance City, 45678")

# Social media links
st.subheader("Follow Us")
st.markdown("[Twitter](https://twitter.com) | [Facebook](https://facebook.com) | [LinkedIn](https://linkedin.com)")