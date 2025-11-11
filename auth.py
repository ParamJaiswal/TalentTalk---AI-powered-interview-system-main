"""
Authentication helper functions for TalentTalk application.
Provides simple session-based authentication for Streamlit apps.

SECURITY NOTE: This is a simple authentication system for demonstration purposes.
In production, you should:
1. Use a proper password hashing library like bcrypt, argon2, or scrypt
2. Store credentials in a secure database, not in code
3. Implement rate limiting and account lockout
4. Use HTTPS for all connections
5. Add multi-factor authentication
"""

import streamlit as st
import hashlib
from typing import Optional, Dict

# Default user credentials (in production, these should be in a secure database)
# NOTE: SHA-256 is used here for simplicity in demo. Use bcrypt/argon2 in production.
DEFAULT_USERS = {
    "admin": {
        "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
        "name": "Administrator"
    },
    "param": {
        "password_hash": hashlib.sha256("param123".encode()).hexdigest(),
        "name": "Param Jaiswal"
    }
}


def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256.
    
    NOTE: This is for demo purposes only. In production, use bcrypt, argon2, or scrypt
    which are specifically designed for password hashing and are computationally expensive
    to prevent brute-force attacks.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def verify_credentials(username: str, password: str) -> bool:
    """
    Verify user credentials.
    
    Args:
        username: Username to verify
        password: Password to verify
        
    Returns:
        True if credentials are valid, False otherwise
    """
    if username not in DEFAULT_USERS:
        return False
    
    password_hash = hash_password(password)
    return DEFAULT_USERS[username]["password_hash"] == password_hash


def get_user_info(username: str) -> Optional[Dict[str, str]]:
    """
    Get user information.
    
    Args:
        username: Username to get info for
        
    Returns:
        Dictionary with user info or None if user doesn't exist
    """
    if username in DEFAULT_USERS:
        return {
            "username": username,
            "name": DEFAULT_USERS[username]["name"]
        }
    return None


def init_session_state():
    """Initialize session state variables for authentication."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "username" not in st.session_state:
        st.session_state.username = None
    if "user_info" not in st.session_state:
        st.session_state.user_info = None


def login(username: str, password: str) -> bool:
    """
    Perform login.
    
    Args:
        username: Username
        password: Password
        
    Returns:
        True if login successful, False otherwise
    """
    if verify_credentials(username, password):
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.user_info = get_user_info(username)
        return True
    return False


def logout():
    """Perform logout and clear session state."""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.user_info = None
    # Clear other session state variables
    for key in list(st.session_state.keys()):
        if key not in ["authenticated", "username", "user_info"]:
            del st.session_state[key]


def is_authenticated() -> bool:
    """Check if user is authenticated."""
    return st.session_state.get("authenticated", False)


def get_current_user() -> Optional[str]:
    """Get current authenticated username."""
    return st.session_state.get("username", None)


def require_auth():
    """
    Decorator/function to require authentication.
    Redirects to login page if not authenticated.
    """
    init_session_state()
    if not is_authenticated():
        st.warning("⚠️ Please login to access this page.")
        st.stop()


def render_login_page():
    """Render the login page UI."""
    init_session_state()
    
    st.markdown(
        """
        <style>
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 40px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Center column for login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("# 🎯 TalentTalk")
        st.markdown("### AI-Powered Interview System")
        st.markdown("---")
        
        # Login form
        with st.form("login_form"):
            st.markdown("#### Login")
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if username and password:
                    if login(username, password):
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                else:
                    st.warning("⚠️ Please enter both username and password")
        
        st.markdown("---")
        st.markdown(
            """
            <div style='text-align: center; color: gray; font-size: 0.8em;'>
            <p>Demo Credentials:</p>
            <p>Username: <code>admin</code> / Password: <code>admin123</code></p>
            <p>Username: <code>param</code> / Password: <code>param123</code></p>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_logout_button():
    """Render logout button in sidebar."""
    if is_authenticated():
        user_info = st.session_state.user_info
        with st.sidebar:
            st.markdown("---")
            st.markdown(f"👤 **{user_info['name']}**")
            if st.button("🚪 Logout", use_container_width=True):
                logout()
                st.rerun()
