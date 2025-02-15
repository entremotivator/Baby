import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText

# Title
st.title("🎉 Gender Reveal Weight Submission Contest 🎉")

# Initialize session state for storing guesses if not already present
if "guesses" not in st.session_state:
    st.session_state.guesses = pd.DataFrame(columns=["Name", "Email", "Gender", "Weight Guess (lbs)"])

# Function to send email
def send_email(to_email, name, weight_guess):
    try:
        from_email = st.secrets["email"]["sender_email"]
        password = st.secrets["email"]["password"]
        smtp_server = st.secrets["email"]["smtp_server"]
        port = st.secrets["email"]["port"]

        subject = "Gender Reveal Contest - Guess Submitted"
        body = f"Hello {name},\n\nThank you for submitting your guess! You guessed {weight_guess} lbs.\n\nGood luck!"

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = to_email

        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())

        st.success(f"Email sent successfully to {to_email}!")

    except Exception as e:
        st.error(f"Failed to send email: {e}")

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
    st.success("Guess submitted successfully!")

# Display current guesses
st.subheader("Current Guesses")
st.dataframe(st.session_state.guesses)

# Admin section to reveal actual weight
st.subheader("Reveal Actual Weight")
actual_weight = st.number_input("Enter the actual birth weight (lbs):", min_value=1.0, max_value=15.0, step=0.1)
if st.button("Find Closest Guess") and not st.session_state.guesses.empty:
    st.session_state.guesses["Difference"] = abs(st.session_state.guesses["Weight Guess (lbs)"] - actual_weight)
    winner = st.session_state.guesses.sort_values(by="Difference").iloc[0]
    st.success(f"🏆 The closest guess is {winner['Name']} ({winner['Email']}) with a guess of {winner['Weight Guess (lbs)']} lbs!")
