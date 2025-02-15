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
st.set_page_config(page_title="Annalise's Gender Reveal Contest", page_icon="🎀💙", layout="centered")
st.image("https://github.com/entremotivator/baby/IMG_3136.jpeg", use_column_width=True)  # Replace with the actual GitHub image URL
st.markdown("""
    <h1 style='text-align: center; color: #ff66b2;'>🎉 Annalise's Gender Reveal Weight Contest 🎉</h1>
""", unsafe_allow_html=True)

# Initialize session state for storing guesses
if "guesses" not in st.session_state:
    st.session_state.guesses = pd.DataFrame(columns=["Name", "Email", "Gender", "Weight Guess (lbs)"])

# Function to send email
def send_email(to_email, name, weight_guess):
    subject = "Annalise's Gender Reveal - Guess Submitted"
    body = f"""
    Hello {name},

    Thank you for participating in Annalise's Gender Reveal Contest!
    Your weight guess: {weight_guess} lbs.

    Good luck!
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

# Apply theme colors
st.markdown("""
    <style>
        .stApp {
            background-color: #f0f8ff;
        }
        .stButton>button {
            background-color: #ff66b2;
            color: white;
            font-size: 16px;
        }
        .stDataFrame table {
            border: 2px solid #ff66b2;
        }
    </style>
""", unsafe_allow_html=True)

# User input form
with st.form("submission_form"):
    name = st.text_input("Enter your name:")
    email = st.text_input("Enter your email:")
    gender = st.radio("Choose a gender:", ("Boy", "Girl"))
    weight_guess = st.number_input("Enter your weight guess (lbs):", min_value=1.0, max_value=15.0, step=0.1)
    submit_button = st.form_submit_button("Submit Guess")

# Process the submission
if submit_button and name and email:
    new_entry = pd.DataFrame([[name, email, gender, weight_guess]], columns=["Name", "Email", "Gender", "Weight Guess (lbs)"])
    st.session_state.guesses = pd.concat([st.session_state.guesses, new_entry], ignore_index=True)
    send_email(email, name, weight_guess)
    st.success("Guess submitted successfully! Check your email for confirmation!")

# Display current guesses
st.subheader("📋 Current Guesses")
st.dataframe(st.session_state.guesses)

# Admin section to reveal actual weight
st.subheader("🎀 Reveal Actual Weight")
actual_weight = st.number_input("Enter the actual birth weight (lbs):", min_value=1.0, max_value=15.0, step=0.1)
if st.button("Find Closest Guess") and not st.session_state.guesses.empty:
    st.session_state.guesses["Difference"] = abs(st.session_state.guesses["Weight Guess (lbs)"] - actual_weight)
    winner = st.session_state.guesses.sort_values(by="Difference").iloc[0]
    st.success(f"🏆 The closest guess is {winner['Name']} ({winner['Email']}) with a guess of {winner['Weight Guess (lbs)']} lbs!")
