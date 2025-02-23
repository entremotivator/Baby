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

# Admin email to receive notifications
ADMIN_EMAIL = "Entremotivator@gmail.com"

# App title and header
st.set_page_config(page_title="Unlocking the Secrets to Deepening Your Intimate Relationships", layout="centered")
st.markdown("""
    <h1 style='text-align: center; color: #ff66b2;'>💖 Unlocking the Secrets to Deepening Your Intimate Relationships 💖</h1>
    <h3 style='text-align: center;'>Join us on March 1st for an unforgettable event!</h3>
    <h4 style='text-align: center;'>📅 Date: March 1st | ⏰ Time: 3:00 - 5:00 PM PST | 📍 Location: Zoom (link will be sent upon registration)</h4>
    <p style='text-align: center;'>💑 Strengthen your connection, communicate effectively, and build lasting intimacy.</p>
""", unsafe_allow_html=True)

# Learning Points
st.markdown("""
### 🌟 What You'll Learn:
✅ Effective Communication Techniques 💬  
✅ Understanding Love Languages ❤️  
✅ Building Emotional and Physical Intimacy 🤗  
✅ Conflict Resolution for a Stronger Bond 🕊️  
✅ Secrets to Lasting Passion 🔥  
""", unsafe_allow_html=True)

# Initialize session state for storing registrations
if "registrations" not in st.session_state:
    st.session_state.registrations = pd.DataFrame(columns=["Name", "Email"])

# Function to send confirmation email to the attendee
def send_confirmation_email(to_email, name):
    subject = "🎉 You're Registered! Unlocking the Secrets to Deepening Your Intimate Relationships"
    body = f"""
    Dear {name},

    Congratulations! You are officially registered for our transformative event:  
    **"Unlocking the Secrets to Deepening Your Intimate Relationships"** 💖  

    📅 **Date:** Friday, March 1st  
    ⏰ **Time:** 3:00 - 5:00 PM PST (Pacific Standard Time)  
    📍 **Location:** Zoom (link will be sent closer to the event)  

    During this engaging and insightful session, you will:  
    ✅ Discover the key to effective communication 💬  
    ✅ Understand and apply love languages ❤️  
    ✅ Deepen emotional and physical intimacy 🤗  
    ✅ Learn conflict resolution techniques for a stronger bond 🕊️  
    ✅ Rekindle passion and connection 🔥  

    🎁 **BONUS:** All attendees will receive an **exclusive relationship workbook** to continue their journey beyond the event!  

    **Next Steps:**  
    - Keep an eye on your inbox for the Zoom link and additional event details.  
    - Mark your calendar and get ready for an unforgettable experience.  
    - Feel free to invite a partner or friend who could benefit from this session!  

    If you have any questions, reply to this email. We're excited to have you join us!  

    Warm regards,  
    **The Event Team**  
    EntreMotivator  
    """

    send_email(to_email, subject, body)

# Function to send notification email to the admin
def send_admin_notification(name, email):
    subject = "📢 New Event Registration Received"
    body = f"""
    Hello EntreMotivator Team,

    A new registration has been received for the event **"Unlocking the Secrets to Deepening Your Intimate Relationships"**.

    📝 **Registrant Details:**  
    - **Name:** {name}  
    - **Email:** {email}  

    Please keep track of this new attendee.  

    Best,  
    Your Automated Registration System  
    """

    send_email(ADMIN_EMAIL, subject, body)

# Function to send emails
def send_email(to_email, subject, body):
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
        st.success(f"📩 Email successfully sent to {to_email}")
    except Exception as e:
        st.error(f"❌ Failed to send email: {e}")

# Registration form
st.subheader("🔹 Register Now!")
with st.form("registration_form"):
    name = st.text_input("Enter your name:")
    email = st.text_input("Enter your email:")
    submit_button = st.form_submit_button("Register")

# Process the registration
if submit_button and name and email:
    new_entry = pd.DataFrame([[name, email]], columns=["Name", "Email"])
    st.session_state.registrations = pd.concat([st.session_state.registrations, new_entry], ignore_index=True)

    # Send confirmation email to attendee
    send_confirmation_email(email, name)

    # Send notification email to admin
    send_admin_notification(name, email)

    st.success("🎉 Registration successful! Check your email for confirmation.")

# Display registered attendees
st.subheader("📋 Registered Attendees")
st.dataframe(st.session_state.registrations)


