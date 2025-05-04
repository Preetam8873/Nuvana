import streamlit as st
import pandas as pd
from datetime import datetime
import json
from utils.db import load_user_data, save_user_data
from utils.auth import change_password, toggle_2fa
from utils.security import validate_input

def show_settings(user_data):
    st.title("Settings")
    
    # Create tabs for different settings
    tab1, tab2, tab3 = st.tabs(["Profile", "Security", "Preferences"])
    
    with tab1:
        show_profile_settings(user_data)
    
    with tab2:
        show_security_settings(user_data)
    
    with tab3:
        show_preferences_settings(user_data)

def show_profile_settings(user_data):
    st.subheader("Profile Settings")
    
    # Display current profile information
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='profile-info'>", unsafe_allow_html=True)
        st.markdown("<h3>Personal Information</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Name:</strong> {user_data.get('full_name', '')}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Email:</strong> {user_data.get('email', '')}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Phone:</strong> {user_data.get('phone', '')}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Date of Birth:</strong> {user_data.get('dob', '')}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>PAN:</strong> {user_data.get('pan', '')}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Aadhar:</strong> {user_data.get('aadhar', '')}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Address:</strong> {user_data.get('address', '')}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='profile-info'>", unsafe_allow_html=True)
        st.markdown("<h3>Account Information</h3>", unsafe_allow_html=True)
        
        # Get primary account
        if "accounts" in user_data and len(user_data["accounts"]) > 0:
            primary_account = user_data["accounts"][0]
            st.markdown(f"<p><strong>Account Number:</strong> {primary_account.get('account_number', '')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Account Type:</strong> {primary_account.get('account_type', '')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Status:</strong> {primary_account.get('status', '')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Created At:</strong> {primary_account.get('created_at', '')}</p>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Edit profile form
    st.subheader("Edit Profile")
    
    with st.form("edit_profile_form"):
        # Only allow editing of certain fields
        phone = st.text_input("Phone Number", value=user_data.get("phone", ""))
        address = st.text_area("Address", value=user_data.get("address", ""))
        
        # Submit button
        submit_button = st.form_submit_button("Update Profile")
        
        if submit_button:
            # Validate inputs
            is_valid_phone, phone_message = validate_input(phone, "phone")
            
            if not is_valid_phone:
                st.error(phone_message)
            else:
                # Update user data
                user_data["phone"] = phone
                user_data["address"] = address
                
                # Save user data
                success, message = save_user_data(user_data)
                
                if success:
                    st.success("Profile updated successfully")
                    
                    # Refresh user data
                    st.session_state.user_data = load_user_data(user_data["user_id"])
                else:
                    st.error(message)

def show_security_settings(user_data):
    st.subheader("Security Settings")
    
    # Change password form
    st.markdown("<h3>Change Password</h3>", unsafe_allow_html=True)
    
    with st.form("change_password_form"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        # Submit button
        submit_button = st.form_submit_button("Change Password")
        
        if submit_button:
            if not current_password or not new_password or not confirm_password:
                st.error("Please fill in all fields")
            elif new_password != confirm_password:
                st.error("New passwords do not match")
            elif len(new_password) < 8:
                st.error("Password must be at least 8 characters long")
            else:
                # Change password
                success, message = change_password(user_data["user_id"], current_password, new_password)
                
                if success:
                    st.success(message)
                    
                    # Refresh user data
                    st.session_state.user_data = load_user_data(user_data["user_id"])
                else:
                    st.error(message)
    
    # Two-factor authentication
    st.markdown("<h3>Two-Factor Authentication</h3>", unsafe_allow_html=True)
    
    # Get current 2FA status
    is_2fa_enabled = user_data.get("security", {}).get("2fa_enabled", False)
    
    if is_2fa_enabled:
        st.info("Two-factor authentication is currently enabled")
        if st.button("Disable 2FA"):
            success, message = toggle_2fa(user_data["user_id"], False)
            
            if success:
                st.success(message)
                
                # Refresh user data
                st.session_state.user_data = load_user_data(user_data["user_id"])
                st.rerun()
            else:
                st.error(message)
    else:
        st.info("Two-factor authentication is currently disabled")
        if st.button("Enable 2FA"):
            success, message = toggle_2fa(user_data["user_id"], True)
            
            if success:
                st.success(message)
                
                # Refresh user data
                st.session_state.user_data = load_user_data(user_data["user_id"])
                st.rerun()
            else:
                st.error(message)
    
    # Session management
    st.markdown("<h3>Session Management</h3>", unsafe_allow_html=True)
    
    if st.button("Logout from All Devices"):
        st.info("This feature is not implemented in the demo")

def show_preferences_settings(user_data):
    st.subheader("Preferences")
    
    # Theme settings
    st.markdown("<h3>Theme</h3>", unsafe_allow_html=True)
    
    # Get current theme
    current_theme = user_data.get("preferences", {}).get("theme", "light")
    
    theme = st.selectbox(
        "Theme",
        ["Light", "Dark"],
        index=0 if current_theme == "light" else 1
    )
    
    # Notification settings
    st.markdown("<h3>Notifications</h3>", unsafe_allow_html=True)
    
    # Get current notification settings
    notifications = user_data.get("preferences", {}).get("notifications", {})
    
    email_notifications = st.checkbox(
        "Email Notifications",
        value=notifications.get("email", True)
    )
    
    sms_notifications = st.checkbox(
        "SMS Notifications",
        value=notifications.get("sms", True)
    )
    
    # Save preferences button
    if st.button("Save Preferences"):
        # Update user data
        if "preferences" not in user_data:
            user_data["preferences"] = {}
        
        user_data["preferences"]["theme"] = "light" if theme == "Light" else "dark"
        
        if "notifications" not in user_data["preferences"]:
            user_data["preferences"]["notifications"] = {}
        
        user_data["preferences"]["notifications"]["email"] = email_notifications
        user_data["preferences"]["notifications"]["sms"] = sms_notifications
        
        # Save user data
        success, message = save_user_data(user_data)
        
        if success:
            st.success("Preferences saved successfully")
            
            # Update session theme
            st.session_state.theme = user_data["preferences"]["theme"]
            
            # Refresh user data
            st.session_state.user_data = load_user_data(user_data["user_id"])
            st.rerun()
        else:
            st.error(message)
