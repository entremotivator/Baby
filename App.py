import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import re
import requests
import json

# Load secrets
EMAIL_ADDRESS = st.secrets["email"]["sender_email"]
EMAIL_PASSWORD = st.secrets["email"]["password"]
SMTP_SERVER = st.secrets["email"]["smtp_server"]
PORT = st.secrets["email"]["port"]
ADMIN_EMAIL = "info@entremotivator@gmail.com"
N8N_WEBHOOK_URL = "https://agentonline-u29564.vm.elestio.app/webhook-test/Consultaientre"

# App configuration
st.set_page_config(
    page_title="The ATM Agency - AI Consulting", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Gold & Black Theme
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main-header {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        padding: 2.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: #ffd700;
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.3);
        border: 2px solid #ffd700;
    }
    .main-header h1, .main-header h2, .main-header h3 {
        color: #ffd700;
    }
    .main-header p {
        color: #ffffff;
    }
    .section-header {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        padding: 1.2rem;
        border-radius: 10px;
        color: #ffd700;
        margin: 2rem 0 1.5rem 0;
        text-align: center;
        font-weight: bold;
        border: 2px solid #ffd700;
        box-shadow: 0 5px 15px rgba(255, 215, 0, 0.2);
    }
    .section-header h2 {
        color: #ffd700;
        margin: 0;
    }
    .info-card {
        background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
        padding: 2rem;
        border-radius: 12px;
        border-left: 5px solid #ffd700;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(255, 215, 0, 0.3);
        color: #ffffff;
    }
    .info-card h3 {
        color: #ffd700;
    }
    .feature-box {
        background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 5px 20px rgba(255, 215, 0, 0.3);
        margin: 1rem 0;
        border: 2px solid #ffd700;
        height: 100%;
        color: #ffffff;
    }
    .feature-box h3 {
        color: #ffd700;
    }
    .feature-box ul {
        color: #ffffff;
    }
    .urgency-banner {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        color: #ffd700;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        font-weight: bold;
        animation: pulse 2s infinite;
        border: 3px solid #ffd700;
        box-shadow: 0 5px 20px rgba(255, 215, 0, 0.4);
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); box-shadow: 0 5px 20px rgba(255, 215, 0, 0.4); }
        50% { transform: scale(1.02); box-shadow: 0 8px 30px rgba(255, 215, 0, 0.6); }
    }
    .cta-section {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        padding: 3rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        color: #ffd700;
        border: 3px solid #ffd700;
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.4);
    }
    .cta-section h2 {
        color: #ffd700;
    }
    .cta-section p {
        color: #ffffff;
    }
    /* Style metrics */
    [data-testid="stMetricValue"] {
        color: #ffd700;
        font-weight: bold;
    }
    [data-testid="stMetricLabel"] {
        color: #ffffff;
    }
    [data-testid="stMetricDelta"] {
        color: #ffd700;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🚀 The ATM Agency</h1>
    <h2>AI Consulting & Automation Experts</h2>
    <h3>Led by D Hudson - Your Partner in AI Transformation</h3>
    <p style="font-size: 1.3em; margin-top: 1.5rem;">
        <strong>Stop Losing Money to Manual Processes!</strong><br>
        Join 500+ companies already leveraging AI to boost productivity by 340%
    </p>
    <div style="margin-top: 1.5rem; font-size: 1.1em;">
        <span style="margin: 0 1rem;">⭐ 98.5% Client Satisfaction</span>
        <span style="margin: 0 1rem;">🏆 500+ Projects Completed</span>
        <span style="margin: 0 1rem;">💰 $50M+ Client Savings</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Urgency Banner
st.markdown("""
<div class="urgency-banner">
    ⚡ LIMITED TIME: Get a FREE $5,000 AI Strategy Package with Your First Project! ⚡<br>
    <span style="font-size: 0.9em;">Only 5 Spots Available This Month!</span>
</div>
""", unsafe_allow_html=True)

# Stats
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Projects Delivered", "500+", "↗️ 50 this month")
with col2:
    st.metric("Average Client ROI", "340%", "↗️ 15% YoY")
with col3:
    st.metric("Client Satisfaction", "98.5%", "↗️ 2.1%")
with col4:
    st.metric("Total Client Savings", "$50M+", "↗️ $5M this quarter")

# Services
st.markdown("<div class='section-header'><h2>🎯 Our AI Solutions</h2></div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <h3>🤖 AI Strategy & Implementation</h3>
        <p style="color: #e74c3c; font-weight: bold;">Save 60% on Labor Costs</p>
        <ul>
            <li>Custom AI Solution Design</li>
            <li>AI Roadmap Development</li>
            <li>Machine Learning Deployment</li>
            <li>Data Science & Analytics</li>
            <li>Ethical AI & Governance</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h3>⚙️ Process Automation</h3>
        <p style="color: #e74c3c; font-weight: bold;">Eliminate 70% of Manual Work</p>
        <ul>
            <li>Robotic Process Automation</li>
            <li>Document Processing</li>
            <li>Workflow Optimization</li>
            <li>Cognitive Automation</li>
            <li>Hyperautomation Strategies</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <h3>📊 Advanced Analytics</h3>
        <p style="color: #e74c3c; font-weight: bold;">Increase Revenue by 45%</p>
        <ul>
            <li>Business Intelligence with AI</li>
            <li>Customer Behavior Prediction</li>
            <li>Market Trend Analysis</li>
            <li>Risk & Fraud Detection</li>
            <li>Performance Optimization</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Initialize session state
if "submissions" not in st.session_state:
    st.session_state.submissions = pd.DataFrame(columns=[
        "Name", "Email", "Company", "Phone", "Position", "Industry", 
        "Company_Size", "Project_Type", "Budget_Range", "Timeline", 
        "Current_Challenges", "Desired_Outcomes", "Submission_Date"
    ])

# Email functions
def send_email(to_email, subject, body_html):
    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
    
    # Attach HTML version
    html_part = MIMEText(body_html, "html")
    msg.attach(html_part)
    
    try:
        with smtplib.SMTP(SMTP_SERVER, PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        return True
    except Exception as e:
        st.error(f"Email error: {str(e)}")
        return False

def send_confirmation_email(to_email, name, company):
    subject = "🎉 Your $5,000 Premium AI Consultation Package is Confirmed"
    body_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f4f4f4;
            }}
            .container {{
                background-color: #ffffff;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .header {{
                background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                color: #ffd700;
                padding: 30px;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 30px;
                border: 2px solid #ffd700;
            }}
            .header h1 {{
                margin: 0;
                color: #ffd700;
                font-size: 28px;
            }}
            .section {{
                margin: 25px 0;
                padding: 20px;
                background-color: #f9f9f9;
                border-radius: 8px;
                border-left: 4px solid #ffd700;
            }}
            .section h2 {{
                color: #1a1a1a;
                margin-top: 0;
                font-size: 20px;
            }}
            .cta-button {{
                display: inline-block;
                background-color: #ffd700;
                color: #1a1a1a;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 18px;
                margin: 20px 0;
                text-align: center;
            }}
            .cta-button:hover {{
                background-color: #ffed4e;
            }}
            .footer {{
                background-color: #1a1a1a;
                color: #ffd700;
                padding: 25px;
                border-radius: 8px;
                text-align: center;
                margin-top: 30px;
                border: 2px solid #ffd700;
            }}
            .footer img {{
                max-width: 100%;
                height: auto;
                margin: 15px 0;
                border-radius: 8px;
            }}
            ul {{
                padding-left: 20px;
            }}
            li {{
                margin: 10px 0;
            }}
            .contact-info {{
                background-color: #fff9e6;
                padding: 15px;
                border-radius: 8px;
                margin: 20px 0;
                border: 1px solid #ffd700;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎊 CONGRATULATIONS {name}!</h1>
                <p style="font-size: 18px; margin: 10px 0;">You've Secured Your Premium AI Consultation Package!</p>
            </div>
            
            <p style="font-size: 16px;">Dear {name},</p>
            
            <p>Welcome to The ATM Agency! We're thrilled to partner with <strong>{company}</strong> on your AI transformation journey.</p>
            
            <div class="section">
                <h2>💎 Your $5,000 Value Package Includes:</h2>
                <ul>
                    <li><strong>✅ Comprehensive AI Readiness Assessment</strong> ($1,500 value)</li>
                    <li><strong>✅ Custom Project Proposal with ROI Projections</strong> ($2,000 value)</li>
                    <li><strong>✅ 60-Minute Strategy Session with D Hudson</strong> ($1,000 value)</li>
                    <li><strong>✅ Personalized AI Implementation Roadmap</strong> ($500 value)</li>
                    <li><strong>✅ 30-Day Post-Implementation Support</strong> (Priceless)</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>⏱️ What Happens Next:</h2>
                <ol>
                    <li><strong>Within 2 Hours:</strong> AI Readiness Questionnaire in your inbox</li>
                    <li><strong>Within 24 Hours:</strong> Our team analyzes your business</li>
                    <li><strong>Within 48 Hours:</strong> Receive your detailed proposal with ROI projections</li>
                    <li><strong>This Week:</strong> Schedule your strategy session with D Hudson</li>
                    <li><strong>Next 30 Days:</strong> Start your AI transformation!</li>
                </ol>
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <h2 style="color: #1a1a1a;">🚀 READY TO GET STARTED?</h2>
                <p style="font-size: 16px; margin: 15px 0;">Don't wait for us to reach out - Schedule your consultation NOW and fast-track your project!</p>
                <a href="https://calendly.com/theatmagency/consultation" class="cta-button">
                    📅 SCHEDULE YOUR CONSULTATION NOW
                </a>
                <p style="font-size: 14px; color: #666;">Click the button above or copy this link:<br>
                <a href="https://calendly.com/theatmagency/consultation" style="color: #1a1a1a;">https://calendly.com/theatmagency/consultation</a></p>
            </div>
            
            <div class="contact-info">
                <h3 style="margin-top: 0; color: #1a1a1a;">📞 Contact Information:</h3>
                <p style="margin: 5px 0;"><strong>Direct Phone:</strong> <a href="tel:6785589752" style="color: #1a1a1a;">6785589752</a></p>
                <p style="margin: 5px 0;"><strong>Email:</strong> <a href="mailto:info@entremotivator@gmail.com" style="color: #1a1a1a;">info@entremotivator@gmail.com</a></p>
                <p style="margin: 15px 0 5px 0; font-size: 14px; font-style: italic;">📞 Call us directly at 6785589752 for immediate assistance!</p>
            </div>
            
            <div class="footer">
                <img src="https://entremotivator.com/wp-content/uploads/2025/10/IMG_0319.png" alt="The ATM Agency" style="max-width: 400px; width: 100%;">
                <h3 style="margin: 15px 0 5px 0;">THE ATM AGENCY</h3>
                <p style="margin: 5px 0;">AI Consulting & Automation Experts</p>
                <p style="margin: 5px 0;">Led by D Hudson</p>
                <p style="margin: 20px 0 5px 0; font-size: 14px;">📧 info@entremotivator@gmail.com | 📞 6785589752</p>
                <p style="margin: 15px 0 0 0; font-size: 12px; color: #ffd700;">© 2024 The ATM Agency. All Rights Reserved.</p>
            </div>
            
            <p style="text-align: center; font-size: 14px; color: #666; margin-top: 20px; font-style: italic;">
                P.S. - Don't wait! Schedule your call today and start saving money tomorrow.
            </p>
        </div>
    </body>
    </html>
    """
    return send_email(to_email, subject, body_html)

def send_admin_notification(form_data):
    subject = f"🚨 New AI Lead - {form_data['company']} ({form_data['budget_range']})"
    body_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333333;
                max-width: 700px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f4f4f4;
            }}
            .container {{
                background-color: #ffffff;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .header {{
                background: linear-gradient(135deg, #ff4757 0%, #ff6348 100%);
                color: white;
                padding: 25px;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 25px;
            }}
            .section {{
                margin: 20px 0;
                padding: 20px;
                background-color: #f9f9f9;
                border-radius: 8px;
                border-left: 4px solid #ffd700;
            }}
            .section h3 {{
                margin-top: 0;
                color: #1a1a1a;
            }}
            .info-row {{
                display: flex;
                margin: 10px 0;
                padding: 8px;
                background-color: white;
                border-radius: 5px;
            }}
            .info-label {{
                font-weight: bold;
                min-width: 150px;
                color: #1a1a1a;
            }}
            .info-value {{
                color: #333;
            }}
            .cta-button {{
                display: inline-block;
                background-color: #ffd700;
                color: #1a1a1a;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 16px;
                margin: 20px 0;
                text-align: center;
            }}
            .priority-high {{
                background-color: #ff4757;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                display: inline-block;
                font-weight: bold;
            }}
            .footer {{
                background-color: #1a1a1a;
                color: #ffd700;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                margin-top: 30px;
            }}
            .footer img {{
                max-width: 100%;
                height: auto;
                margin: 10px 0;
                border-radius: 8px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 style="margin: 0;">🚨 NEW AI CONSULTING LEAD</h1>
                <p style="margin: 10px 0; font-size: 18px;">High Priority - Action Required</p>
            </div>
            
            <div style="text-align: center; margin: 20px 0;">
                <span class="priority-high">⚡ PRIORITY LEAD - FOLLOW UP IMMEDIATELY</span>
            </div>
            
            <div class="section">
                <h3>👤 Contact Information</h3>
                <div class="info-row">
                    <span class="info-label">Name:</span>
                    <span class="info-value">{form_data["name"]}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Position:</span>
                    <span class="info-value">{form_data["position"]}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Email:</span>
                    <span class="info-value"><a href="mailto:{form_data["email"]}">{form_data["email"]}</a></span>
                </div>
                <div class="info-row">
                    <span class="info-label">Phone:</span>
                    <span class="info-value"><a href="tel:{form_data["phone"]}">{form_data["phone"]}</a></span>
                </div>
                <div class="info-row">
                    <span class="info-label">Company:</span>
                    <span class="info-value">{form_data["company"]}</span>
                </div>
            </div>
            
            <div class="section">
                <h3>🏢 Company Details</h3>
                <div class="info-row">
                    <span class="info-label">Industry:</span>
                    <span class="info-value">{form_data["industry"]}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Company Size:</span>
                    <span class="info-value">{form_data["company_size"]}</span>
                </div>
            </div>
            
            <div class="section">
                <h3>💼 Project Information</h3>
                <div class="info-row">
                    <span class="info-label">Project Type:</span>
                    <span class="info-value">{form_data["project_type"]}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Budget Range:</span>
                    <span class="info-value"><strong>{form_data["budget_range"]}</strong></span>
                </div>
                <div class="info-row">
                    <span class="info-label">Timeline:</span>
                    <span class="info-value">{form_data["timeline"]}</span>
                </div>
            </div>
            
            <div class="section">
                <h3>📋 Current Challenges</h3>
                <p style="background: white; padding: 15px; border-radius: 5px; margin: 10px 0;">{form_data["current_challenges"]}</p>
            </div>
            
            <div class="section">
                <h3>🎯 Desired Outcomes</h3>
                <p style="background: white; padding: 15px; border-radius: 5px; margin: 10px 0;">{form_data["desired_outcomes"]}</p>
            </div>
            
            <div style="text-align: center; margin: 30px 0; padding: 20px; background-color: #fff9e6; border-radius: 8px; border: 2px solid #ffd700;">
                <h3 style="margin-top: 0; color: #1a1a1a;">⚡ IMMEDIATE ACTION REQUIRED</h3>
                <p style="margin: 10px 0;">Schedule a call with this client immediately!</p>
                <a href="https://calendly.com/theatmagency/consultation" class="cta-button">
                    📅 SCHEDULE CLIENT CALL NOW
                </a>
            </div>
            
            <div style="background-color: #f0f0f0; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <p style="margin: 5px 0; font-size: 14px;"><strong>📅 Submission Time:</strong> {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
                <p style="margin: 5px 0; font-size: 14px;"><strong>🔔 Response Time:</strong> Contact within 24 hours for best conversion rate</p>
            </div>
            
            <div class="footer">
                <img src="https://entremotivator.com/wp-content/uploads/2025/10/IMG_0319.png" alt="The ATM Agency" style="max-width: 300px; width: 100%;">
                <h3 style="margin: 10px 0;">THE ATM AGENCY</h3>
                <p style="margin: 5px 0; font-size: 12px;">Internal Lead Notification System</p>
            </div>
        </div>
    </body>
    </html>
    """
    return send_email(ADMIN_EMAIL, subject, body_html)

def send_to_n8n(form_data):
    """Send form data to n8n webhook"""
    try:
        # Prepare payload
        payload = {
            "name": form_data["name"],
            "email": form_data["email"],
            "phone": form_data["phone"],
            "company": form_data["company"],
            "position": form_data["position"],
            "industry": form_data["industry"],
            "company_size": form_data["company_size"],
            "project_type": form_data["project_type"],
            "budget_range": form_data["budget_range"],
            "timeline": form_data["timeline"],
            "current_challenges": form_data["current_challenges"],
            "desired_outcomes": form_data["desired_outcomes"],
            "submission_date": datetime.now().isoformat(),
            "submission_timestamp": datetime.now().strftime("%B %d, %Y at %I:%M %p")
        }
        
        # Send POST request to n8n webhook
        response = requests.post(
            N8N_WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code in [200, 201, 204]:
            return True
        else:
            st.warning(f"n8n webhook returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        st.warning(f"Could not connect to n8n webhook: {str(e)}")
        return False
    except Exception as e:
        st.warning(f"Error sending to n8n: {str(e)}")
        return False

# Contact Form
st.markdown("<div class='section-header'><h2>📝 Claim Your FREE $5,000 Consultation Package</h2></div>", unsafe_allow_html=True)

# Add full-width logo at top of form
st.markdown("""
<div style="margin: 2rem 0; width: 100%;">
    <img src="https://entremotivator.com/wp-content/uploads/2025/10/IMG_0319.png" 
         alt="The ATM Agency Logo" 
         style="width: 100%; height: auto; border-radius: 15px; box-shadow: 0 8px 30px rgba(255, 215, 0, 0.4); border: 2px solid #ffd700;">
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
    <h3>🎁 Your FREE Package Includes:</h3>
    <ul style="font-size: 1.1em;">
        <li>✅ Comprehensive AI Readiness Assessment ($1,500 value)</li>
        <li>✅ Custom ROI Analysis ($2,000 value)</li>
        <li>✅ 60-Minute Strategy Session ($1,000 value)</li>
        <li>✅ Implementation Roadmap ($500 value)</li>
    </ul>
    <p style="font-size: 1.1em; color: #c0392b; font-weight: bold;">
        ⚡ TOTAL VALUE: $5,000 - YOURS FREE!
    </p>
</div>
""", unsafe_allow_html=True)

with st.form("ai_consultation_form", clear_on_submit=False):
    
    st.markdown("### 👤 Contact Information")
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name *", placeholder="John Smith")
        email = st.text_input("Business Email *", placeholder="john@company.com")
        phone = st.text_input("Phone Number *", placeholder="6785589752")
    
    with col2:
        position = st.text_input("Job Title *", placeholder="CEO, CTO, Manager")
        company = st.text_input("Company Name *", placeholder="Your Company")
        industry = st.selectbox(
            "Industry *",
            ["Select industry", "Technology", "E-commerce", "Healthcare", 
             "Finance", "Manufacturing", "Other"]
        )

    st.markdown("---")
    st.markdown("### 🏢 Company Details")
    
    col3, col4 = st.columns(2)
    with col3:
        company_size = st.selectbox(
            "Company Size *",
            ["Select size", "1-10", "11-50", "51-200", "201-500", "500+"]
        )
        project_type = st.selectbox(
            "Project Type *",
            ["Select type", "AI Strategy", "Process Automation", 
             "Analytics & ML", "Content Creation", "Not Sure"]
        )
    
    with col4:
        budget_range = st.selectbox(
            "Budget Range *",
            ["Select budget", "$10K-$25K", "$25K-$50K", 
             "$50K-$100K", "$100K-$250K", "$250K+"]
        )
        timeline = st.selectbox(
            "Timeline *",
            ["Select timeline", "ASAP", "Within 2 weeks", 
             "Within 1 month", "1-3 months", "3-6 months"]
        )

    st.markdown("---")
    st.markdown("### 📋 Project Details")
    
    current_challenges = st.text_area(
        "Current Challenges *",
        placeholder="What problems are you facing?",
        height=100
    )
    
    desired_outcomes = st.text_area(
        "Desired Outcomes *",
        placeholder="What results do you want?",
        height=100
    )
    
    consent = st.checkbox(
        "I agree to receive communications from The ATM Agency", 
        value=True
    )

    st.markdown("---")
    submit_button = st.form_submit_button(
        "🎁 Claim My FREE $5,000 Consultation Now", 
        use_container_width=True,
        type="primary"
    )

# Form Processing
if submit_button:
    required_fields = [name, email, phone, position, company, industry, 
                      company_size, project_type, budget_range, timeline,
                      current_challenges, desired_outcomes]
    
    # Simple email validation
    is_valid_email = "@" in email and "." in email.split("@")[1]
    
    if not consent:
        st.error("⚠️ Please agree to receive communications.")
    elif not all(field and "Select" not in str(field) for field in required_fields):
        st.error("⚠️ Please fill in all required fields marked with *")
    elif not is_valid_email:
        st.error("⚠️ Please enter a valid email address")
    else:
        form_data = {
            'name': name, 'email': email, 'company': company, 'phone': phone,
            'position': position, 'industry': industry, 'company_size': company_size,
            'project_type': project_type, 'budget_range': budget_range, 
            'timeline': timeline, 'current_challenges': current_challenges,
            'desired_outcomes': desired_outcomes
        }
        
        new_entry = pd.DataFrame([[
            name, email, company, phone, position, industry, company_size,
            project_type, budget_range, timeline, current_challenges,
            desired_outcomes, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]], columns=st.session_state.submissions.columns)
        
        st.session_state.submissions = pd.concat(
            [st.session_state.submissions, new_entry], ignore_index=True
        )
        
        # Send to n8n webhook
        n8n_sent = send_to_n8n(form_data)
        
        # Send emails
        confirmation_sent = send_confirmation_email(email, name, company)
        admin_sent = send_admin_notification(form_data)
        
        if confirmation_sent and admin_sent:
            st.success("🎉 **SUCCESS! Your consultation package is confirmed!**")
            st.balloons()
            
            if n8n_sent:
                st.info("✅ Your submission has been processed through our automated workflow system.")
            
            st.markdown(f"""
            <div class="info-card" style="background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);">
                <h2 style="text-align: center; color: #ffd700;">✅ Check Your Email!</h2>
                <p style="font-size: 1.2em; color: #ffffff;">
                    We've sent confirmation to <strong style="color: #ffd700;">{email}</strong>
                </p>
                <h3 style="color: #ffd700;">⏱️ What Happens Next:</h3>
                <ol style="font-size: 1.1em; line-height: 2; color: #ffffff;">
                    <li>Within 2 Hours: AI Readiness Assessment in your inbox</li>
                    <li>Within 24 Hours: Custom analysis and ROI projections</li>
                    <li>Within 48 Hours: D Hudson will schedule your strategy session</li>
                </ol>
                <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); padding: 1.5rem; border-radius: 10px; margin-top: 2rem; text-align: center; border: 2px solid #ffd700;">
                    <h3 style="color: #ffd700;">🚀 SCHEDULE YOUR CALL NOW!</h3>
                    <p style="font-size: 1.1em; color: #ffffff; margin: 1rem 0;">
                        Don't wait for us to reach out - Book your consultation immediately and fast-track your AI transformation!
                    </p>
                    <a href="https://calendly.com/theatmagency/consultation" target="_blank" style="display: inline-block; background: #ffd700; color: #1a1a1a; padding: 1rem 2rem; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 1.2em; margin: 1rem 0;">
                        📅 BOOK YOUR CONSULTATION NOW
                    </a>
                    <p style="font-size: 1em; color: #ffffff; margin-top: 1rem;">
                        Or call us directly: <strong style="color: #ffd700;">6785589752</strong>
                    </p>
                </div>
                <div style="background: #2d2d2d; padding: 1.5rem; border-radius: 10px; margin-top: 2rem; text-align: center; border: 1px solid #ffd700;">
                    <h3 style="color: #ffd700;">📞 Need Immediate Help?</h3>
                    <p style="font-size: 1.2em; color: #ffffff;">
                        <strong style="color: #ffd700;">Call: 6785589752</strong><br>
                        Email: <strong style="color: #ffd700;">info@entremotivator@gmail.com</strong>
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("⚠️ Issue sending emails. Our team will contact you within 1 hour!")
            st.info("📞 Call us: 6785589752")

# Footer
st.markdown("""
<div class="cta-section" style="margin-top: 3rem;">
    <h2>🚀 The ATM Agency</h2>
    <p style="font-size: 1.2em;">AI Consulting & Automation Experts</p>
    <p style="margin-top: 1rem;">
        📞 <strong>6785589752</strong><br>
        📧 info@entremotivator@gmail.com
    </p>
    <p style="margin-top: 2rem;">© 2024 The ATM Agency. All Rights Reserved.</p>
    <p>🔒 SOC 2 Type II Certified | 🛡️ GDPR Compliant</p>
</div>
""", unsafe_allow_html=True)
