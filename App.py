import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load secrets
EMAIL_ADDRESS = st.secrets["email"]["sender_email"]
EMAIL_PASSWORD = st.secrets["email"]["password"]
SMTP_SERVER = st.secrets["email"]["smtp_server"]
PORT = st.secrets["email"]["port"]

# App title and header
st.set_page_config(page_title="Unlocking the Secrets to Deepening Your Intimate Relationships", layout="centered")
st.markdown("""
    <h1 style='text-align: center; color: #ff66b2;'>💖 Unlocking the Secrets to Deepening Your Intimate Relationships 💖</h1>
    <h3 style='text-align: center;'>Join us on March 1st for an unforgettable event!</h3>
""", unsafe_allow_html=True)

# Initialize session state for storing registrations
if "registrations" not in st.session_state:
    st.session_state.registrations = pd.DataFrame(columns=["Name", "Email"])

# Function to send confirmation email
def send_email(to_email, name):
    subject = "Event Registration Confirmation - Deepening Your Intimate Relationships"
    body = f"""
    Hello {name},

    Thank you for registering for our event: "Unlocking the Secrets to Deepening Your Intimate Relationships."
    
    📅 Date: March 1st
    📍 Location: [Insert Location Here]
    ⏰ Time: [Insert Time Here]

    We're excited to have you join us!
    
    Best,
    Event Team
    """
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    
    try:
        with smtplib.SMTP(SMTP_SERVER, PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
    except Exception as e:
        st.error(f"Failed to send email: {e}")

# Registration form
with st.form("registration_form"):
    name = st.text_input("Enter your name:")
    email = st.text_input("Enter your email:")
    submit_button = st.form_submit_button("Register")

# Process the registration
if submit_button and name and email:
    new_entry = pd.DataFrame([[name, email]], columns=["Name", "Email"])
    st.session_state.registrations = pd.concat([st.session_state.registrations, new_entry], ignore_index=True)
    send_email(email, name)
    st.success("Registration successful! Check your email for confirmation.")

# Display registered attendees
st.subheader("📋 Registered Attendees")
st.dataframe(st.session_state.registrations)
