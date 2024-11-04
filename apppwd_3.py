import streamlit as st
import hashlib
import socket
import os

# Set your username and password
USERNAME = "bapin"
PASSWORD_HASH = hashlib.sha256("abcdef123".encode()).hexdigest()

# File path to store the locked device IP address
LOCKED_DEVICE_IP_FILE = "locked_device_ip.txt"

# Get IP address of the current device
def get_device_ip():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except Exception as e:
        st.error(f"Unable to retrieve IP address: {e}")
        return None

# Load the locked IP address from the file if it exists
def load_locked_ip():
    if os.path.exists(LOCKED_DEVICE_IP_FILE):
        with open(LOCKED_DEVICE_IP_FILE, "r") as file:
            return file.read().strip()
    return None

# Save the current device IP address to the file
def save_locked_ip(ip_address):
    with open(LOCKED_DEVICE_IP_FILE, "w") as file:
        file.write(ip_address)

def main():
    st.title("Single Device Streamlit App")

    # Load the locked IP from the file
    locked_ip = load_locked_ip()
    current_ip = get_device_ip()

    # Check if the app is already locked to a specific device
    if locked_ip:
        # Deny access if the current device IP doesn't match the locked IP
        if current_ip != locked_ip:
            st.error("Access denied: This app is locked to another device.")
            return
    else:
        st.subheader("Login to access the app")

        # Input fields for username and password
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        # Verify username and password
        if st.button("Login"):
            if username == USERNAME and hashlib.sha256(password.encode()).hexdigest() == PASSWORD_HASH:
                # Lock the app to the current device's IP address by saving it to the file
                save_locked_ip(current_ip)
                st.success("Login successful! The app is now locked to this device.")
            else:
                st.error("Incorrect username or password.")

    # Add your app's main content here, visible only after successful login and device lock
    if locked_ip == current_ip or (not locked_ip and "logged_in" in st.session_state):
        st.write("Welcome to the restricted app! This app is now locked to your device.")

if __name__ == "__main__":
    main()
