import streamlit as st
import hashlib
import socket

# Set your username and password
USERNAME = "your_username"
PASSWORD_HASH = hashlib.sha256("your_password".encode()).hexdigest()

# Key to store the IP address once the device is registered
LOCKED_DEVICE_IP_KEY = "locked_device_ip"


# Get IP address of the current device
def get_device_ip():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except Exception as e:
        st.error(f"Unable to retrieve IP address: {e}")
        return None


def main():
    st.title("Single Device Streamlit App")

    # Check if the app is already locked to a specific device
    if LOCKED_DEVICE_IP_KEY in st.session_state:
        locked_ip = st.session_state[LOCKED_DEVICE_IP_KEY]
        current_ip = get_device_ip()

        # Deny access if the current device IP doesn't match the locked IP
        if current_ip != locked_ip:
            st.error("Access denied: This app is locked to another device.")
            return

    # If not locked to any device, prompt for login
    st.subheader("Login to access the app")

    # Input fields for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Verify username and password
    if st.button("Login"):
        if username == USERNAME and hashlib.sha256(password.encode()).hexdigest() == PASSWORD_HASH:
            # Lock the app to the current device's IP address
            st.session_state[LOCKED_DEVICE_IP_KEY] = get_device_ip()
            st.success("Login successful! The app is now locked to this device.")
        else:
            st.error("Incorrect username or password.")

    # Add your app's main content here, visible only after successful login and device lock
    if LOCKED_DEVICE_IP_KEY in st.session_state and st.session_state[LOCKED_DEVICE_IP_KEY] == get_device_ip():
        st.write("Welcome to the restricted app! This app is now locked to your device.")


if __name__ == "__main__":
    main()
