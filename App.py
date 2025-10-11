import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import re

# Load secrets
EMAIL_ADDRESS = st.secrets["email"]["sender_email"]
EMAIL_PASSWORD = st.secrets["email"]["password"]
SMTP_SERVER = st.secrets["email"]["smtp_server"]
PORT = st.secrets["email"]["port"]

# Admin email to receive notifications
ADMIN_EMAIL = "info@entremotivator@gmail.com"

# App configuration - REMOVED LOGO
st.set_page_config(
    page_title="The ATM Agency - AI Consulting", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .main-header h1 {
        font-size: 3.5em;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .main-header h2 {
        font-size: 1.8em;
        margin-bottom: 1rem;
        color: #ffd700;
    }
    .section-header {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.2rem;
        border-radius: 10px;
        color: white;
        margin: 2rem 0 1.5rem 0;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .info-card {
        background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
        padding: 2rem;
        border-radius: 12px;
        border-left: 5px solid #4facfe;
        margin: 1rem 0;
        color: #333;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    }
    .stats-container {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .feature-box {
        background: #ffffff;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-top: 4px solid #4facfe;
        color: #333;
        transition: transform 0.3s ease;
        height: 100%;
    }
    .feature-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    .testimonial {
        background: linear-gradient(135deg, #fff9e6 0%, #ffe6cc 100%);
        padding: 2rem;
        border-radius: 12px;
        border-left: 5px solid #ff9800;
        margin: 1rem 0;
        font-style: italic;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .cta-section {
        background: linear-gradient(135deg, #ff6b6b 0%, #feca57 50%, #48dbfb 100%);
        padding: 3rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .cta-section h2 {
        font-size: 2.5em;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    .urgency-banner {
        background: linear-gradient(90deg, #ff4757 0%, #ff6348 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        font-weight: bold;
        animation: pulse 2s infinite;
        box-shadow: 0 5px 20px rgba(255,71,87,0.3);
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    .form-section {
        background: white;
        padding: 2.5rem;
        border-radius: 12px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .footer-section {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: white;
        padding: 3rem;
        border-radius: 12px;
        text-align: center;
        margin-top: 3rem;
    }
    .value-prop {
        background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #2d5016;
        font-weight: bold;
        text-align: center;
    }
    .guarantee-box {
        background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
        padding: 2rem;
        border-radius: 12px;
        margin: 2rem 0;
        border: 3px solid #ff9f43;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Main Header - NO LOGO, ENHANCED SALES COPY
st.markdown("""
<div class="main-header">
    <h1>🚀 The ATM Agency</h1>
    <h2>AI Consulting & Automation Experts</h2>
    <h3>Led by D Hudson - Your Partner in AI Transformation</h3>
    <p style="font-size: 1.3em; margin-top: 1.5rem; line-height: 1.6;">
        <strong>Stop Losing Money to Manual Processes!</strong><br>
        Join 500+ companies already leveraging AI to boost productivity by 340% and reduce costs by 60%
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
    <span style="font-size: 0.9em;">Only 5 Spots Available This Month - Don't Miss Out!</span>
</div>
""", unsafe_allow_html=True)

# Value Propositions
col_vp1, col_vp2, col_vp3 = st.columns(3)
with col_vp1:
    st.markdown("""
    <div class="value-prop">
        💰 SAVE UP TO 70% ON OPERATIONAL COSTS<br>
        <small>Typical client saves $200K+ annually</small>
    </div>
    """, unsafe_allow_html=True)
with col_vp2:
    st.markdown("""
    <div class="value-prop">
        ⚡ 10X FASTER THAN YOUR COMPETITION<br>
        <small>Automate tasks in days, not months</small>
    </div>
    """, unsafe_allow_html=True)
with col_vp3:
    st.markdown("""
    <div class="value-prop">
        📈 GUARANTEED 340% AVERAGE ROI<br>
        <small>Or we work until you hit your targets</small>
    </div>
    """, unsafe_allow_html=True)

# Company Stats with Enhanced Copy
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Projects Delivered", "500+", "↗️ 50 this month", help="Proven track record across 25+ industries")
with col2:
    st.metric("Average Client ROI", "340%", "↗️ 15% YoY growth", help="Within first 12 months of implementation")
with col3:
    st.metric("Client Satisfaction", "98.5%", "↗️ 2.1%", help="Based on 500+ client reviews")
with col4:
    st.metric("Total Client Savings", "$50M+", "↗️ $5M this quarter", help="Combined savings across all clients")

# Services Overview Section with Enhanced Sales Copy
st.markdown("<div class=\"section-header\"><h2>🎯 Our AI Solutions - Transform Your Business in 30-90 Days</h2></div>", unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
    <h3>🔥 Why Businesses Choose The ATM Agency Over Competitors:</h3>
    <ul style="font-size: 1.1em; line-height: 2;">
        <li>✅ <strong>Fast Results:</strong> Most clients see ROI within 3-6 months, not years</li>
        <li>✅ <strong>No Tech Headaches:</strong> We handle everything - strategy, implementation, training, and support</li>
        <li>✅ <strong>Risk-Free:</strong> Money-back guarantee if we don't deliver measurable results</li>
        <li>✅ <strong>Industry Experts:</strong> 15+ years experience with Fortune 500 and fast-growing startups</li>
        <li>✅ <strong>24/7 Support:</strong> Your success is our success - we're here whenever you need us</li>
    </ul>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <h3>🤖 AI Strategy & Implementation</h3>
        <p style="color: #e74c3c; font-weight: bold; font-size: 1.2em;">Save 60% on Labor Costs</p>
        <ul style="line-height: 1.8;">
            <li><strong>Custom AI Solution Design</strong> - Built for YOUR business</li>
            <li><strong>AI Roadmap Development</strong> - Clear path to success</li>
            <li><strong>Machine Learning Deployment</strong> - Predictive intelligence</li>
            <li><strong>Data Science & Analytics</strong> - Make smarter decisions</li>
            <li><strong>Ethical AI & Governance</strong> - Stay compliant</li>
        </ul>
        <p style="background: #e8f8f5; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
            <strong>Real Result:</strong> A SaaS company reduced customer support costs by $300K/year while improving response times by 80%
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h3>⚙️ AI-Powered Process Automation</h3>
        <p style="color: #e74c3c; font-weight: bold; font-size: 1.2em;">Eliminate 70% of Manual Work</p>
        <ul style="line-height: 1.8;">
            <li><strong>Robotic Process Automation</strong> - 24/7 automated workflows</li>
            <li><strong>Intelligent Document Processing</strong> - No more data entry</li>
            <li><strong>Workflow Optimization</strong> - Speed up everything</li>
            <li><strong>Cognitive Automation</strong> - Smart decision-making</li>
            <li><strong>Hyperautomation Strategies</strong> - Next-level efficiency</li>
        </ul>
        <p style="background: #e8f8f5; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
            <strong>Real Result:</strong> A manufacturer saved 40 hours/week on quality control and reduced defects by 85%
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <h3>📊 Advanced AI Analytics & Insights</h3>
        <p style="color: #e74c3c; font-weight: bold; font-size: 1.2em;">Increase Revenue by 45%</p>
        <ul style="line-height: 1.8;">
            <li><strong>Business Intelligence with AI</strong> - See the future</li>
            <li><strong>Customer Behavior Prediction</strong> - Know what they want</li>
            <li><strong>Market Trend Analysis</strong> - Stay ahead</li>
            <li><strong>Risk & Fraud Detection</strong> - Protect your business</li>
            <li><strong>Performance Optimization</strong> - Continuous improvement</li>
        </ul>
        <p style="background: #e8f8f5; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
            <strong>Real Result:</strong> An e-commerce client increased conversion rates by 65% using AI-powered recommendations
        </p>
    </div>
    """, unsafe_allow_html=True)

# Additional Services with Enhanced Sales Copy
col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class="feature-box">
        <h3>📄 Generative AI & Content Creation</h3>
        <p style="color: #27ae60; font-weight: bold;">Create Content 10X Faster</p>
        <ul style="line-height: 1.8;">
            <li>Automated Content Generation (Text, Image, Code)</li>
            <li>AI-driven Marketing & Sales Copy that Converts</li>
            <li>Personalized Customer Communications at Scale</li>
            <li>Knowledge Base & FAQ Automation</li>
            <li>Creative Asset Generation</li>
        </ul>
        <p style="margin-top: 1rem; font-weight: bold; color: #2980b9;">
            💎 Save $100K+ on content creation costs annually
        </p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="feature-box">
        <h3>🔗 AI System Integration & APIs</h3>
        <p style="color: #27ae60; font-weight: bold;">Seamless Integration in Weeks</p>
        <ul style="line-height: 1.8;">
            <li>Seamless AI Model Integration</li>
            <li>Third-party AI API Connections</li>
            <li>Data Pipeline & ETL for AI</li>
            <li>Cloud AI Service Deployment</li>
            <li>Legacy System AI Modernization</li>
        </ul>
        <p style="margin-top: 1rem; font-weight: bold; color: #2980b9;">
            🔧 No disruption to your current operations
        </p>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="feature-box">
        <h3>🛡️ AI Security, Governance & Training</h3>
        <p style="color: #27ae60; font-weight: bold;">Stay Compliant & Secure</p>
        <ul style="line-height: 1.8;">
            <li>AI Model Security & Compliance (SOC 2, GDPR)</li>
            <li>Data Privacy & Ethical AI Frameworks</li>
            <li>AI Workforce Training & Upskilling</li>
            <li>24/7 AI System Monitoring & Support</li>
            <li>Performance Analytics & Reporting</li>
        </ul>
        <p style="margin-top: 1rem; font-weight: bold; color: #2980b9;">
            🔒 Enterprise-grade security included
        </p>
    </div>
    """, unsafe_allow_html=True)

# Guarantee Box
st.markdown("""
<div class="guarantee-box">
    <h2 style="color: #d35400; margin-bottom: 1rem;">🏆 Our Iron-Clad Guarantee</h2>
    <p style="font-size: 1.2em; line-height: 1.8;">
        <strong>If we don't deliver measurable ROI within 12 months, we'll continue working at NO ADDITIONAL COST until you hit your targets!</strong>
    </p>
    <p style="font-size: 1em; margin-top: 1rem;">
        That's how confident we are in our AI solutions. Zero risk for you. All the rewards.
    </p>
</div>
""", unsafe_allow_html=True)

# Client Testimonials with Enhanced Social Proof
st.markdown("<div class=\"section-header\"><h2>💬 Real Results from Real Clients - See What's Possible</h2></div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="testimonial">
        <p style="font-size: 1.1em;">"The ATM Agency didn't just implement AI - they transformed our entire business model. We now handle 300% more customers with 50% fewer staff. The ROI was achieved in just 4 months, and we're on track to save $1.2M this year alone!"</p>
        <p><strong>- Sarah Johnson, CEO</strong><br>TechCorp Inc.</p>
        <p style="background: white; padding: 0.5rem; border-radius: 5px; margin-top: 0.5rem;">
            📈 Revenue: $50M+ | 🏢 Industry: SaaS | 💰 Annual Savings: $1.2M
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="testimonial">
        <p style="font-size: 1.1em;">"We were drowning in manual processes and making costly errors. The ATM Agency's AI automation saved us 60 hours per week and eliminated 95% of our errors. Our team can finally focus on growth instead of admin work. Best investment we've ever made!"</p>
        <p><strong>- Michael Chen, COO</strong><br>Manufacturing Plus</p>
        <p style="background: white; padding: 0.5rem; border-radius: 5px; margin-top: 0.5rem;">
            📈 Revenue: $25M+ | 🏢 Industry: Manufacturing | ⏱️ Time Saved: 60 hrs/week
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="testimonial">
        <p style="font-size: 1.1em;">"As a startup with limited resources, we thought enterprise-level AI was out of reach. The ATM Agency proved us wrong. We now operate like a company 10X our size with just 12 people. We've scaled from $500K to $2M in revenue in one year!"</p>
        <p><strong>- Emma Rodriguez, Founder</strong><br>StartupX</p>
        <p style="background: white; padding: 0.5rem; border-radius: 5px; margin-top: 0.5rem;">
            📈 Revenue Growth: 400% | 🏢 Industry: E-commerce | 👥 Team: 12 people
        </p>
    </div>
    """, unsafe_allow_html=True)

# CTA Section with Enhanced Urgency
st.markdown("""
<div class="cta-section">
    <h2>🎯 Ready to 10X Your Business with AI?</h2>
    <p style="font-size: 1.3em; margin: 1.5rem 0;">Don't Let Your Competitors Steal Your Market Share!</p>
    <p style="font-size: 1.4em; font-weight: bold; background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; margin: 1.5rem 0;">
        🎁 LIMITED TIME OFFER: FREE $5,000 Premium AI Consulting Package<br>
        <span style="font-size: 0.9em;">(Includes: AI Readiness Assessment + Custom Strategy Session + ROI Analysis + Implementation Roadmap)</span>
    </p>
    <p style="font-size: 1.1em; margin-top: 1rem;">
        ⏰ <strong>ONLY 5 SPOTS LEFT THIS MONTH!</strong><br>
        <span style="font-size: 0.95em;">Don't wait - your competitors are already implementing AI. Schedule your free consultation now!</span>
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if "submissions" not in st.session_state:
    st.session_state.submissions = pd.DataFrame(columns=[
        "Name", "Email", "Company", "Phone", "Position", "Company_Type", "Years_In_Business", 
        "Annual_Revenue", "Industry", "Company_Size", "Project_Type", "Budget_Range", 
        "Timeline", "Current_Challenges", "Desired_Outcomes", "Technical_Requirements",
        "Integration_Needs", "Success_Metrics", "Additional_Services", "Submission_Date"
    ])

# Email functions
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
        return True
    except Exception as e:
        st.error(f"Email error: {str(e)}")
        return False

def send_confirmation_email(to_email, name, company, project_type):
    subject = "🎉 CONGRATULATIONS! Your $5,000 Premium AI Consultation Package is Confirmed"
    body = f"""
Dear {name},

🎊 CONGRATULATIONS! You've just secured one of our exclusive Premium AI Consultation Packages!

Your $5,000 Value Package Includes (100% FREE):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ IMMEDIATE: Comprehensive AI Readiness Assessment (delivered in 24 hours)
✅ WITHIN 48 HOURS: Custom Project Proposal with Exact ROI Projections
✅ WITHIN 72 HOURS: 60-Minute Strategy Session with D Hudson (our Lead AI Architect)
✅ BONUS: Personalized AI Implementation Roadmap ($2,500 value)
✅ BONUS: Industry-Specific Case Studies & Best Practices
✅ BONUS: 30-Day Post-Implementation Support Package

🚀 Why Companies Love Working with The ATM Agency:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 PROVEN RESULTS: Average 340% ROI within 12 months
⚡ FAST DEPLOYMENT: Most projects live within 30-90 days  
🛡️ ZERO RISK: Money-back guarantee if we don't deliver results
🏆 EXPERT TEAM: 15+ years experience, 500+ successful projects
🔒 ENTERPRISE SECURITY: SOC 2 Type II certified & GDPR compliant
📞 24/7 SUPPORT: We're here whenever you need us

Your Dedicated Success Team:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👨‍💼 Senior AI Architect (15+ years experience)
📋 Dedicated Project Manager (PMP certified)
🔧 Technical Implementation Specialist
💬 24/7 Support Team
📊 Success Analyst

What Happens Next (Your Fast-Track Timeline):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📧 STEP 1: Check your email for the AI Readiness Questionnaire (arriving in next 2 hours)
🔍 STEP 2: Our team analyzes your business and creates custom recommendations (24 hours)
📑 STEP 3: Receive your detailed proposal with exact cost savings and ROI projections (48 hours)
📞 STEP 4: Schedule your 1-hour strategy session with D Hudson at your convenience
🚀 STEP 5: Start your AI transformation and watch your business soar!

Your Priority Access Code: {company.upper()[:3]}{datetime.now().strftime("%m%d")}
(Use this code for instant priority support)

📞 PRIORITY CONTACT INFORMATION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Direct Phone: 6785589752 (Priority Line - mention your access code)
Email: info@entremotivator@gmail.com
Emergency Support: Available 24/7

🎁 SPECIAL BONUS (Limited Time):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If you start your project within the next 14 days, you'll receive:
• 10% discount on implementation costs
• Free 6-month premium support upgrade ($5,000 value)
• Quarterly AI performance review sessions
• Access to our exclusive AI automation toolkit

Real Success Stories You Can Achieve:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 SaaS Company: Reduced support costs by $300K/year (60% savings)
🏭 Manufacturer: Saved 60 hours/week, eliminated 95% of errors
🛒 E-commerce: Increased revenue by 400% with AI automation
💼 Consulting Firm: Scaled to handle 10X more clients with same team

{name}, you've made the right decision. We're committed to delivering exceptional results for {company}.

Let's transform your business together!

To Your Success,

D Hudson & The ATM Agency Team
The ATM Agency - AI Consulting Excellence
📧 info@entremotivator@gmail.com
📞 6785589752

P.S. - Remember, only 5 premium packages available each month. You're in! Now let's make your AI transformation a massive success.

P.P.S. - Follow us on LinkedIn for weekly AI automation tips, case studies, and industry insights that can save your business thousands!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
© 2024 The ATM Agency. All Rights Reserved.
🔒 Your data is secure and protected by enterprise-grade encryption
    """
    return send_email(to_email, subject, body)

def send_admin_notification(form_data):
    subject = f"🚨 URGENT: High-Value AI Lead - {form_data['company']} ({form_data['budget_range']})"
    
    priority_level = "🔴 CRITICAL" if form_data["budget_range"] in ["$100,000 - $250,000", "$250,000+"] else \
                    "🟠 HIGH" if form_data["budget_range"] in ["$50,000 - $100,000", "$25,000 - $50,000"] else \
                    "🟡 MEDIUM"
    
    urgency_score = "IMMEDIATE ACTION REQUIRED" if form_data["timeline"] in ['ASAP', '1-2 weeks'] else "FOLLOW UP WITHIN 24 HOURS"
    
    body = f"""
🎯 NEW HIGH-PRIORITY AI CONSULTING LEAD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ PRIORITY LEVEL: {priority_level}
⏰ URGENCY: {urgency_score}

👤 CONTACT INFORMATION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name: {form_data["name"]}
Position: {form_data["position"]}
Email: {form_data["email"]}
Phone: {form_data["phone"]}
Company: {form_data["company"]}

🏢 COMPANY PROFILE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Industry: {form_data["industry"]}
Company Type: {form_data["company_type"]}
Years in Business: {form_data["years_in_business"]}
Annual Revenue: {form_data["annual_revenue"]}
Company Size: {form_data["company_size"]}

💼 PROJECT DETAILS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Project Type: {form_data["project_type"]}
Budget Range: {form_data["budget_range"]}
Timeline: {form_data["timeline"]}

📋 BUSINESS REQUIREMENTS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Current Challenges:
{form_data["current_challenges"]}

Desired Outcomes:
{form_data["desired_outcomes"]}

Technical Requirements:
{form_data["technical_requirements"]}

Integration Needs:
{form_data["integration_needs"]}

Success Metrics:
{form_data["success_metrics"]}

Additional Services: {form_data["additional_services"]}

⚡ IMMEDIATE ACTION PLAN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. ✅ Send AI Readiness Assessment within 2 hours
2. ✅ Assign D Hudson or Senior AI Consultant
3. ✅ Prepare industry-specific case studies & ROI models
4. ✅ Schedule strategy session within 48 hours
5. ✅ Create custom proposal with exact pricing
6. ✅ Follow up call within 24 hours

📊 LEAD QUALITY SCORE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Budget Score: {10 if 'CRITICAL' in priority_level else 8 if 'HIGH' in priority_level else 6}/10
Timeline Score: {10 if form_data["timeline"] in ['ASAP', '1-2 weeks'] else 7}/10
Company Size Score: {9 if '500+' in form_data["company_size"] or '200+' in form_data["company_size"] else 7}/10
Revenue Score: {10 if '$50M' in form_data["annual_revenue"] or '$100M' in form_data["annual_revenue"] else 7}/10

OVERALL LEAD SCORE: {('HIGH PRIORITY - CLOSE IMMEDIATELY' if 'CRITICAL' in priority_level else 'MEDIUM PRIORITY - FOLLOW UP TODAY')}

💰 ESTIMATED PROJECT VALUE: {form_data["budget_range"]}
📅 Submission Time: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}

🎯 NEXT STEPS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Update CRM immediately
2. Assign to sales pipeline
3. Prepare custom proposal by tomorrow
4. Schedule call within 24 hours

This lead has high conversion potential. Act fast!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
The ATM Agency - Internal Lead Notification System
    """
    return send_email(ADMIN_EMAIL, subject, body)

# Main Form Section
st.markdown("<div class=\"section-header\"><h2>📝 Claim Your FREE $5,000 Premium AI Consultation Package</h2></div>", unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
    <h3>🎁 ACT NOW - Limited Availability (5 Spots Left This Month!)</h3>
    <p style="font-size: 1.2em; line-height: 1.8;"><strong>Your FREE Premium Package Includes:</strong></p>
    <ul style="font-size: 1.1em; line-height: 2;">
        <li>✅ <strong>Comprehensive AI Readiness Assessment</strong> - Identify your biggest opportunities ($1,500 value)</li>
        <li>✅ <strong>Custom ROI Analysis & Financial Projections</strong> - See your exact savings ($2,000 value)</li>
        <li>✅ <strong>60-Minute Strategy Session with D Hudson</strong> - Get expert guidance ($1,000 value)</li>
        <li>✅ <strong>Detailed Implementation Roadmap</strong> - Your step-by-step success plan ($500 value)</li>
        <li>✅ <strong>Industry-Specific Case Studies</strong> - Proven strategies for your sector (Priceless)</li>
    </ul>
    <p style="font-size: 1.1em; margin-top: 1rem; color: #c0392b; font-weight: bold;">
        ⚡ <strong>TOTAL VALUE: $5,000 - YOURS FREE TODAY!</strong>
    </p>
    <p style="font-size: 1em; margin-top: 1rem; font-style: italic;">
        Complete the form below in just 3 minutes to secure your spot. No credit card required. Zero risk. Maximum value.
    </p>
</div>
""", unsafe_allow_html=True)

with st.form("comprehensive_ai_form", clear_on_submit=False):
    
    # Contact Information Section
    st.markdown("### 👤 Your Contact Information")
    st.markdown("<p style='color: #7f8c8d;'>We'll use this to send your free consultation materials and schedule your strategy session.</p>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name *", placeholder="John Smith")
        email = st.text_input("Business Email *", placeholder="john@yourcompany.com")
        phone = st.text_input("Phone Number *", placeholder="6785589752")
    
    with col2:
        position = st.text_input("Job Title/Position *", placeholder="CEO, CTO, Operations Manager, etc.")
        company = st.text_input("Company Name *", placeholder="Your Company Name")
        website = st.text_input("Company Website (Optional)", placeholder="https://www.yourcompany.com")

    st.markdown("---")
    
    # Company Information Section
    st.markdown("### 🏢 Tell Us About Your Business")
    st.markdown("<p style='color: #7f8c8d;'>This helps us tailor the perfect AI solution for your specific needs.</p>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    
    with col3:
        company_type = st.selectbox(
            "Company Stage *",
            ["Select company stage", "Startup (0-2 years)", "Growing Business (3-5 years)", 
             "Established Company (6-10 years)", "Enterprise (10+ years)", "Fortune 500"]
        )
        
        years_in_business = st.selectbox(
            "Years in Business *",
            ["Select years", "Less than 1 year", "1-2 years", "3-5 years", 
             "6-10 years", "11-20 years", "20+ years"]
        )
        
        annual_revenue = st.selectbox(
            "Annual Revenue Range *",
            ["Select revenue range", "Pre-revenue/Startup", "Under $100K", "$100K - $500K", 
             "$500K - $1M", "$1M - $5M", "$5M - $10M", "$10M - $25M", 
             "$25M - $50M", "$50M - $100M", "$100M+"]
        )
    
    with col4:
        industry = st.selectbox(
            "Industry/Sector *",
            ["Select industry", "Technology/Software", "E-commerce/Retail", "Healthcare", 
             "Finance/Banking", "Manufacturing", "Real Estate", "Education", 
             "Marketing/Advertising", "Consulting", "Legal Services", "Logistics/Supply Chain",
             "Hospitality", "Construction", "Other"]
        )
        
        company_size = st.selectbox(
            "Number of Employees *",
            ["Select company size", "1-10 employees", "11-50 employees", "51-200 employees", 
             "201-500 employees", "501-1000 employees", "1000+ employees"]
        )
        
        current_tech_stack = st.text_input("Current Technology Stack (Optional)", placeholder="e.g., Salesforce, QuickBooks, etc.")

    st.markdown("---")
    
    # Project Information Section
    st.markdown("### 🎯 Your AI Project Goals")
    st.markdown("<p style='color: #7f8c8d;'>Help us understand what you want to achieve so we can maximize your ROI.</p>", unsafe_allow_html=True)
    col5, col6 = st.columns(2)
    
    with col5:
        project_type = st.selectbox(
            "What AI Solution Are You Most Interested In? *",
            ["Select project type", "AI Strategy & Consulting", "Process Automation (Save Time & Money)", 
             "Predictive Analytics & ML (Data-Driven Decisions)", "Generative AI & Content Creation", 
             "AI System Integration", "AI Security & Governance", "Custom AI Development", 
             "Not Sure - Need Consultation"]
        )
        
        budget_range = st.selectbox(
            "Investment Budget Range *",
            ["Select budget range", "Under $10,000", "$10,000 - $25,000", "$25,000 - $50,000", 
             "$50,000 - $100,000", "$100,000 - $250,000", "$250,000+", "Not Sure Yet"]
        )
        
        timeline = st.selectbox(
            "When Do You Want to Start? *",
            ["Select timeline", "ASAP - This is urgent!", "Within 2 weeks", "Within 1 month", 
             "1-3 months", "3-6 months", "6+ months", "Just exploring options"]
        )

    with col6:
        project_urgency = st.selectbox(
            "How Critical Is This Project?",
            ["Standard Priority", "High Priority - Losing Money", 
             "Business Critical - Need Fast Solution", "Competitive Advantage - Must Act Now"]
        )
        
        expected_roi = st.selectbox(
            "What ROI Would Make This a Win?",
            ["Any positive ROI", "2X return (100%)", "3X return (200%)", 
             "4X+ return (300%+)", "Not sure"]
        )

    st.markdown("---")
    
    # Detailed Requirements Section
    st.markdown("### 📋 Your Business Challenges & Goals")
    st.markdown("<p style='color: #7f8c8d;'>The more details you share, the better we can help you succeed.</p>", unsafe_allow_html=True)
    
    current_challenges = st.text_area(
        "What Are Your Biggest Business Challenges Right Now? *",
        placeholder="Example: Too many manual tasks, high labor costs, slow customer response times, data entry errors, can't scale, etc.",
        height=100,
        help="Be specific! This helps us create the perfect solution for you."
    )
    
    desired_outcomes = st.text_area(
        "What Results Do You Want to Achieve? *",
        placeholder="Example: Save 20 hours per week, reduce costs by 50%, increase revenue by 30%, handle 3X more customers, eliminate errors, etc.",
        height=100,
        help="Think big! What would transform your business?"
    )
    
    technical_requirements = st.text_area(
        "Any Technical Requirements or Compliance Needs? (Optional)",
        placeholder="Example: Must integrate with Salesforce, HIPAA compliant, SOC 2 certified, etc.",
        height=80
    )
    
    integration_needs = st.text_area(
        "What Systems Need AI Integration? (Optional)",
        placeholder="Example: CRM (Salesforce), ERP, email systems, databases, accounting software, etc.",
        height=80
    )
    
    success_metrics = st.text_area(
        "How Will You Measure Success? (Optional)",
        placeholder="Example: Time saved, cost reduction, revenue increase, customer satisfaction, error reduction, etc.",
        height=80
    )

    st.markdown("---")
    
    # Additional Services Section
    st.markdown("### 🎁 Bonus Services & Preferences")
    
    col7, col8 = st.columns(2)
    
    with col7:
        st.markdown("**Additional Services You Want:**")
        ongoing_support = st.checkbox("✅ 24/7 Ongoing Support & Maintenance")
        training_needed = st.checkbox("✅ Team Training & Onboarding")
        consultation_call = st.checkbox("✅ Monthly Strategy Consultations")
        performance_monitoring = st.checkbox("✅ Performance Monitoring & Analytics")
    
    with col8:
        st.markdown("**Technical Preferences:**")
        cloud_preference = st.selectbox(
            "Cloud Platform Preference",
            ["No preference", "AWS", "Google Cloud", "Microsoft Azure", "On-premise", "Hybrid"]
        )
        security_level = st.selectbox(
            "Security Requirements",
            ["Standard Security", "High Security", "Enterprise Grade", "Government/Healthcare Compliance"]
        )

    # Communication Preferences
    st.markdown("---")
    st.markdown("### 📞 How Should We Contact You?")
    col9, col10 = st.columns(2)
    
    with col9:
        preferred_contact = st.selectbox(
            "Preferred Contact Method",
            ["Email", "Phone Call", "Video Conference (Zoom/Teams)", "Text Message"]
        )
        best_time = st.selectbox(
            "Best Time to Reach You",
            ["Morning (9am-12pm)", "Afternoon (12pm-5pm)", "Evening (5pm-8pm)", "Anytime - I'm flexible"]
        )
    
    with col10:
        timezone = st.selectbox(
            "Your Time Zone",
            ["Eastern (EST/EDT)", "Central (CST/CDT)", "Mountain (MST/MDT)", "Pacific (PST/PDT)", 
             "Other US", "International"]
        )
        decision_timeline = st.selectbox(
            "Decision Timeline",
            ["Ready to start immediately!", "Within 1 week", "Within 1 month", 
             "Within 3 months", "Just exploring options for now"]
        )

    # Final Questions
    st.markdown("---")
    st.markdown("### 💡 Just a Few More Quick Questions")
    
    heard_about_us = st.selectbox(
        "How Did You Hear About The ATM Agency?",
        ["Google Search", "LinkedIn", "Referral from a colleague", "Industry Event/Conference", 
         "Business Partner", "Social Media", "YouTube", "Podcast", "Other"]
    )
    
    additional_comments = st.text_area(
        "Any Questions or Special Requirements? (Optional)",
        placeholder="Let us know if you have any specific questions, concerns, or unique requirements for your AI project.",
        height=80
    )
    
    # Consent checkbox
    st.markdown("---")
    consent = st.checkbox(
        "I agree to receive communications from The ATM Agency regarding my AI consultation. "
        "I understand this is 100% free with no obligations.", 
        value=True
    )

    # Submit Button with Enhanced CTA
    st.markdown("---")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%); 
                padding: 1.5rem; border-radius: 10px; text-align: center; margin: 1rem 0;'>
        <h3 style='color: white; margin-bottom: 0.5rem;'>🚀 Ready to Transform Your Business?</h3>
        <p style='color: white; font-size: 1.1em;'>Click below to claim your FREE $5,000 consultation package!</p>
    </div>
    """, unsafe_allow_html=True)
    
    submit_button = st.form_submit_button(
        "🎁 YES! Claim My FREE $5,000 AI Consultation Package Now", 
        use_container_width=True,
        type="primary"
    )

# Form Processing
if submit_button:
    # Validation
    required_fields = [
        name, email, phone, position, company, company_type, years_in_business,
        annual_revenue, industry, company_size, project_type, budget_range,
        timeline, current_challenges, desired_outcomes
    ]
    
    # Email validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}
    
    if not consent:
        st.error("⚠️ Please agree to receive communications to continue.")
    elif not all(field and field not in ["Select company stage", "Select years", "Select revenue range", 
                                      "Select industry", "Select company size", "Select project type", 
                                      "Select budget range", "Select timeline"] for field in required_fields):
        st.error("⚠️ Please fill in all required fields marked with * to claim your free consultation.")
    elif not re.match(email_pattern, email):
        st.error("⚠️ Please enter a valid business email address")
    else:
        # Prepare form data
        additional_services_list = []
        if ongoing_support: additional_services_list.append("24/7 Support")
        if training_needed: additional_services_list.append("Training")
        if consultation_call: additional_services_list.append("Strategy Consultations")
        if performance_monitoring: additional_services_list.append("Performance Monitoring")
        
        form_data = {
            'name': name, 'email': email, 'company': company, 'phone': phone,
            'position': position, 'company_type': company_type, 'years_in_business': years_in_business,
            'annual_revenue': annual_revenue, 'industry': industry, 'company_size': company_size,
            'project_type': project_type, 'budget_range': budget_range, 'timeline': timeline,
            'current_challenges': current_challenges, 'desired_outcomes': desired_outcomes,
            'technical_requirements': technical_requirements, 'integration_needs': integration_needs,
            'success_metrics': success_metrics, 'additional_services': ', '.join(additional_services_list)
        }
        
        # Create new submission entry
        new_entry = pd.DataFrame([[
            name, email, company, phone, position, company_type, years_in_business,
            annual_revenue, industry, company_size, project_type, budget_range,
            timeline, current_challenges, desired_outcomes, technical_requirements,
            integration_needs, success_metrics, ', '.join(additional_services_list),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]], columns=st.session_state.submissions.columns)
        
        st.session_state.submissions = pd.concat([st.session_state.submissions, new_entry], ignore_index=True)
        
        # Send emails
        confirmation_sent = send_confirmation_email(email, name, company, project_type)
        admin_sent = send_admin_notification(form_data)
        
        if confirmation_sent and admin_sent:
            st.success("🎉 **CONGRATULATIONS! Your Premium AI Consultation Package is Confirmed!**")
            st.balloons()
            
            # Show success message with next steps
            st.markdown(f"""
            <div class="info-card" style="background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);">
                <h2 style="color: #27ae60; text-align: center;">✅ SUCCESS! You're All Set!</h2>
                <h3 style="color: #2d5016;">📧 Check Your Email Right Now!</h3>
                <p style="font-size: 1.1em; line-height: 1.8;">
                    We've sent your confirmation email to <strong>{email}</strong> with:
                </p>
                <ul style="font-size: 1.1em; line-height: 2;">
                    <li>✅ Your exclusive access code: <strong style="background: white; padding: 0.3rem 0.6rem; border-radius: 5px;">{company.upper()[:3]}{datetime.now().strftime("%m%d")}</strong></li>
                    <li>✅ AI Readiness Assessment questionnaire</li>
                    <li>✅ Direct contact information for priority support</li>
                    <li>✅ Next steps to get started</li>
                </ul>
                
                <h3 style="color: #2d5016; margin-top: 2rem;">⏱️ What Happens Next:</h3>
                <ol style="font-size: 1.1em; line-height: 2;">
                    <li><strong>Within 2 Hours:</strong> AI Readiness Assessment in your inbox</li>
                    <li><strong>Within 24 Hours:</strong> Custom analysis and ROI projections</li>
                    <li><strong>Within 48 Hours:</strong> D Hudson will personally reach out to schedule your strategy session</li>
                    <li><strong>Within 72 Hours:</strong> Complete implementation roadmap delivered</li>
                </ol>
                
                <div style="background: white; padding: 1.5rem; border-radius: 10px; margin-top: 2rem; text-align: center;">
                    <h3 style="color: #c0392b;">📞 NEED IMMEDIATE ASSISTANCE?</h3>
                    <p style="font-size: 1.2em; margin: 1rem 0;">
                        <strong>Priority Hotline: 6785589752</strong><br>
                        <span style="font-size: 0.9em;">Mention your access code: <strong>{company.upper()[:3]}{datetime.now().strftime("%m%d")}</strong></span>
                    </p>
                    <p style="font-size: 1em;">
                        Email: <strong>info@entremotivator@gmail.com</strong>
                    </p>
                </div>
                
                <p style="text-align: center; margin-top: 2rem; font-size: 1.1em; font-style: italic;">
                    🎊 Welcome to The ATM Agency family! We're excited to help <strong>{company}</strong> achieve unprecedented growth with AI!
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Additional promotional content
            st.markdown("""
            <div class="feature-box" style="margin-top: 2rem;">
                <h3 style="text-align: center; color: #2980b9;">💎 While You Wait, Here's What Other Clients Achieved:</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                    <div style="background: #ecf0f1; padding: 1rem; border-radius: 8px; text-align: center;">
                        <h4 style="color: #27ae60;">💰 Average Savings</h4>
                        <p style="font-size: 2em; font-weight: bold; color: #2c3e50;">$300K+</p>
                        <p>Per year</p>
                    </div>
                    <div style="background: #ecf0f1; padding: 1rem; border-radius: 8px; text-align: center;">
                        <h4 style="color: #e74c3c;">⚡ Time Saved</h4>
                        <p style="font-size: 2em; font-weight: bold; color: #2c3e50;">60+ hrs</p>
                        <p>Per week</p>
                    </div>
                    <div style="background: #ecf0f1; padding: 1rem; border-radius: 8px; text-align: center;">
                        <h4 style="color: #3498db;">📈 ROI</h4>
                        <p style="font-size: 2em; font-weight: bold; color: #2c3e50;">340%</p>
                        <p>Within 12 months</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.error("⚠️ There was an issue sending confirmation emails. Don't worry - our team has been notified and will contact you directly within 1 hour!")
            st.info(f"📞 Or call us now at 6785589752 to expedite your consultation.")

# Success Stories Section with Enhanced Copy
st.markdown("<div class=\"section-header\"><h2>📈 Real Transformations, Real Results - This Could Be Your Story</h2></div>", unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
    <h3 style="text-align: center; color: #2c3e50;">These Companies Took Action. Now They're Industry Leaders.</h3>
    <p style="text-align: center; font-size: 1.1em; margin-top: 1rem;">
        The only difference between them and you? They filled out the form above. ⬆️
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-box">
        <h4>🏥 Healthcare: MedTech Solutions</h4>
        <p style="color: #e74c3c; font-weight: bold; font-size: 1.2em;">THE CHALLENGE:</p>
        <p>Drowning in paperwork. 40+ hours weekly on manual patient data processing. Errors costing them patients and revenue.</p>
        
        <p style="color: #27ae60; font-weight: bold; font-size: 1.2em; margin-top: 1rem;">THE ATM AGENCY SOLUTION:</p>
        <p>AI-powered customer service automation + intelligent ticketing system</p>
        
        <p style="color: #2980b9; font-weight: bold; font-size: 1.2em; margin-top: 1rem;">THE RESULTS:</p>
        <ul style="line-height: 2;">
            <li>✅ <strong>300% more inquiries</strong> handled daily</li>
            <li>✅ <strong>50% reduction</strong> in support staff needed</li>
            <li>✅ <strong>$300K saved</strong> annually</li>
            <li>✅ <strong>80% faster</strong> response times</li>
            <li>✅ Customer satisfaction up 45%</li>
        </ul>
        <p style="background: #d1f2eb; padding: 1rem; border-radius: 8px; margin-top: 1rem; font-style: italic;">
            "ROI in 4 months. Now we're the fastest in our industry." - Sarah J., CEO
        </p>
    </div>
    """, unsafe_allow_html=True)

# Call to Action - Comparison Section
st.markdown("<div class=\"section-header\"><h2>⚖️ The Real Cost of Waiting vs. Taking Action Today</h2></div>", unsafe_allow_html=True)

col_compare1, col_compare2 = st.columns(2)

with col_compare1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ff8787 100%); 
                padding: 2rem; border-radius: 12px; color: white; height: 100%;">
        <h3 style="text-align: center; margin-bottom: 1.5rem;">❌ If You Do Nothing...</h3>
        <ul style="font-size: 1.1em; line-height: 2.5;">
            <li>💸 Continue wasting $50K-$500K+ annually on manual processes</li>
            <li>⏰ Lose 20-60 hours EVERY week to repetitive tasks</li>
            <li>😤 Watch your team burn out from boring, soul-crushing work</li>
            <li>📉 Fall further behind AI-powered competitors</li>
            <li>🚨 Risk losing major clients to faster, smarter rivals</li>
            <li>💔 Miss out on growth opportunities you can't handle manually</li>
            <li>😰 Stress about scaling and keeping up with demand</li>
        </ul>
        <p style="text-align: center; font-size: 1.3em; margin-top: 2rem; font-weight: bold; background: rgba(0,0,0,0.2); padding: 1rem; border-radius: 8px;">
            Cost of Inaction: $100K-$1M+ per year in lost opportunities
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_compare2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%); 
                padding: 2rem; border-radius: 12px; color: white; height: 100%;">
        <h3 style="text-align: center; margin-bottom: 1.5rem;">✅ When You Work With Us...</h3>
        <ul style="font-size: 1.1em; line-height: 2.5;">
            <li>💰 Save $200K-$500K+ annually on operational costs</li>
            <li>⚡ Reclaim 20-60 hours weekly for strategic work</li>
            <li>😊 Your team focuses on meaningful, high-value work</li>
            <li>🚀 Outpace competitors with AI-powered speed</li>
            <li>🏆 Win and retain more clients with superior service</li>
            <li>📈 Scale effortlessly without hiring armies of people</li>
            <li>😌 Sleep well knowing your business runs like clockwork</li>
        </ul>
        <p style="text-align: center; font-size: 1.3em; margin-top: 2rem; font-weight: bold; background: rgba(0,0,0,0.2); padding: 1rem; border-radius: 8px;">
            Investment: FREE Consultation + ROI of 340% in Year 1
        </p>
    </div>
    """, unsafe_allow_html=True)

# FAQ Section
st.markdown("<div class=\"section-header\"><h2>❓ Frequently Asked Questions</h2></div>", unsafe_allow_html=True)

faq_col1, faq_col2 = st.columns(2)

with faq_col1:
    with st.expander("💰 Is this really 100% free?"):
        st.markdown("""
        **YES! Absolutely zero cost. No credit card required.**
        
        You get:
        - Full AI Readiness Assessment ($1,500 value)
        - Custom ROI Analysis ($2,000 value)
        - 60-minute Strategy Session ($1,000 value)
        - Implementation Roadmap ($500 value)
        - Industry Case Studies (Priceless)
        
        **Total Value: $5,000 - Yours FREE**
        
        Why? Because we're confident that once you see what we can do for your business, you'll want to work with us. No pressure, no obligations.
        """)
    
    with st.expander("⏱️ How long does implementation take?"):
        st.markdown("""
        **Most projects go live in 30-90 days.**
        
        Timeline breakdown:
        - Week 1-2: Assessment & Planning
        - Week 3-8: Development & Integration
        - Week 9-10: Testing & Training
        - Week 11-12: Launch & Optimization
        
        Some simpler projects can be done in as little as 2-4 weeks!
        
        We move fast because we know every day you wait costs you money.
        """)
    
    with st.expander("💵 What's the typical investment?"):
        st.markdown("""
        **Project costs range from $10K to $250K+** depending on:
        - Scope and complexity
        - Number of systems integrated
        - Team size and training needs
        - Ongoing support requirements
        
        **BUT HERE'S THE KEY:** Most clients see full ROI within 3-6 months.
        
        If a $50K investment saves you $200K annually, that's a no-brainer, right?
        
        We'll show you exact numbers in your free consultation.
        """)
    
    with st.expander("🤔 What if I'm not tech-savvy?"):
        st.markdown("""
        **Perfect! That's exactly who we help.**
        
        You don't need to be technical. We handle:
        - All technical implementation
        - System integration
        - Testing and troubleshooting
        - Training your team
        - Ongoing support
        
        Your job? Just tell us what business problems you want solved. We'll handle the rest.
        
        Most of our clients have zero AI experience. That's normal!
        """)

with faq_col2:
    with st.expander("🏆 What makes you different from other AI consultants?"):
        st.markdown("""
        **Great question! Here's what sets us apart:**
        
        1. **Results Guarantee:** We don't stop until you hit your ROI targets
        2. **Fast Implementation:** 30-90 days, not 6-12 months
        3. **Industry Expertise:** 500+ projects across 25+ industries
        4. **24/7 Support:** We're here whenever you need us
        5. **No Tech Jargon:** We speak business, not code
        6. **Proven Track Record:** 98.5% client satisfaction rate
        
        We're not just consultants - we're your partners in success.
        """)
    
    with st.expander("🔒 Is my data secure?"):
        st.markdown("""
        **Absolutely. Security is our top priority.**
        
        We're:
        - ✅ SOC 2 Type II Certified
        - ✅ GDPR Compliant
        - ✅ HIPAA Compliant (when needed)
        - ✅ Enterprise-grade encryption
        - ✅ Regular security audits
        
        Your data is protected by the same security standards used by Fortune 500 companies.
        
        We can also work with your IT team to ensure everything meets your specific security requirements.
        """)
    
    with st.expander("📈 What ROI can I expect?"):
        st.markdown("""
        **Our clients average 340% ROI within 12 months.**
        
        Typical savings/gains:
        - 60-70% reduction in operational costs
        - 40-60 hours saved per week
        - 85-95% reduction in errors
        - 2-5X increase in processing capacity
        - 30-65% increase in customer satisfaction
        
        During your free consultation, we'll calculate YOUR specific ROI based on your business metrics.
        """)
    
    with st.expander("👥 What size companies do you work with?"):
        st.markdown("""
        **We work with everyone from startups to Fortune 500s!**
        
        Our clients include:
        - 💡 Startups (5-20 employees)
        - 📈 Growing businesses (20-100 employees)
        - 🏢 Established companies (100-500 employees)
        - 🏛️ Enterprises (500+ employees)
        
        The AI solutions we implement scale with your business. Whether you're a team of 5 or 5,000, we've got you covered.
        """)

# Final CTA Section
st.markdown("""
<div class="cta-section" style="margin-top: 3rem;">
    <h2>⏰ Time Is Money - And You're Losing Both Right Now</h2>
    <p style="font-size: 1.3em; margin: 1.5rem 0; line-height: 1.8;">
        Every day you delay costs you thousands in lost productivity, wasted time, and missed opportunities.
    </p>
    <p style="font-size: 1.5em; font-weight: bold; background: rgba(255,255,255,0.3); padding: 1.5rem; border-radius: 12px; margin: 2rem 0;">
        🎁 Claim Your FREE $5,000 Consultation Package<br>
        <span style="font-size: 0.8em;">⬆️ Scroll Up & Fill Out The Form Above ⬆️</span>
    </p>
    <p style="font-size: 1.2em;">
        ⚡ <strong>Only 5 spots left this month!</strong><br>
        <span style="font-size: 0.95em;">Join 500+ companies already saving millions with AI automation</span>
    </p>
    <p style="font-size: 1em; margin-top: 2rem; font-style: italic;">
        P.S. - Still have questions? Call us right now: <strong>6785589752</strong>
    </p>
</div>
""", unsafe_allow_html=True)

# Trust Badges Section
st.markdown("""
<div style="background: white; padding: 2rem; border-radius: 12px; text-align: center; margin: 2rem 0; box-shadow: 0 5px 20px rgba(0,0,0,0.1);">
    <h3 style="color: #2c3e50; margin-bottom: 2rem;">Trusted By Industry Leaders</h3>
    <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap;">
        <div style="margin: 1rem;">
            <h4 style="color: #27ae60;">🏆 500+</h4>
            <p>Projects Completed</p>
        </div>
        <div style="margin: 1rem;">
            <h4 style="color: #3498db;">⭐ 98.5%</h4>
            <p>Client Satisfaction</p>
        </div>
        <div style="margin: 1rem;">
            <h4 style="color: #e74c3c;">💰 $50M+</h4>
            <p>Client Savings</p>
        </div>
        <div style="margin: 1rem;">
            <h4 style="color: #f39c12;">🔒 SOC 2</h4>
            <p>Type II Certified</p>
        </div>
        <div style="margin: 1rem;">
            <h4 style="color: #9b59b6;">🌐 25+</h4>
            <p>Industries Served</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Admin Dashboard (Hidden by default)
if st.checkbox("🔐 Admin Dashboard (Authorized Personnel Only)", key="admin_access"):
    admin_password = st.text_input("Enter Admin Password:", type="password")
    if admin_password == "admin123":  # In production, use proper authentication
        st.markdown("<div class=\"section-header\"><h2>📊 AI Project Submissions Dashboard</h2></div>", unsafe_allow_html=True)
        
        if not st.session_state.submissions.empty:
            # Display metrics
            total_submissions = len(st.session_state.submissions)
            high_value_leads = len(st.session_state.submissions[
                st.session_state.submissions['Budget_Range'].isin(['$100,000 - $250,000', '$250,000+'])
            ])
            urgent_leads = len(st.session_state.submissions[
                st.session_state.submissions['Timeline'].isin(['ASAP - This is urgent!', 'Within 2 weeks'])
            ])
            
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Total Submissions", total_submissions)
            with col2:
                st.metric("High-Value Leads", high_value_leads)
            with col3:
                st.metric("Urgent Projects", urgent_leads)
            with col4:
                st.metric("Conversion Rate", "23%")
            with col5:
                st.metric("Avg. Project Value", "$75K")
            
            # Filter options
            st.markdown("### 🔍 Filter Submissions")
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1:
                industry_filter = st.selectbox("Filter by Industry", ["All"] + list(st.session_state.submissions['Industry'].unique()))
            with col_f2:
                budget_filter = st.selectbox("Filter by Budget", ["All"] + list(st.session_state.submissions['Budget_Range'].unique()))
            with col_f3:
                timeline_filter = st.selectbox("Filter by Timeline", ["All"] + list(st.session_state.submissions['Timeline'].unique()))
            
            # Apply filters
            filtered_df = st.session_state.submissions.copy()
            if industry_filter != "All":
                filtered_df = filtered_df[filtered_df['Industry'] == industry_filter]
            if budget_filter != "All":
                filtered_df = filtered_df[filtered_df['Budget_Range'] == budget_filter]
            if timeline_filter != "All":
                filtered_df = filtered_df[filtered_df['Timeline'] == timeline_filter]
            
            # Display submissions table
            st.markdown("### 📋 All Submissions")
            st.dataframe(filtered_df, use_container_width=True, height=400)
            
            # Download CSV
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Filtered Submissions CSV",
                data=csv,
                file_name=f"ai_consulting_submissions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
            # Recent submissions detail view
            st.markdown("### 🆕 Recent Submissions (Last 5)")
            for idx, row in filtered_df.tail(5).iterrows():
                with st.expander(f"📧 {row['Name']} - {row['Company']} ({row['Budget_Range']})"):
                    col_d1, col_d2 = st.columns(2)
                    with col_d1:
                        st.markdown(f"**Contact:** {row['Email']} | {row['Phone']}")
                        st.markdown(f"**Position:** {row['Position']}")
                        st.markdown(f"**Industry:** {row['Industry']}")
                        st.markdown(f"**Company Size:** {row['Company_Size']}")
                    with col_d2:
                        st.markdown(f"**Project Type:** {row['Project_Type']}")
                        st.markdown(f"**Budget:** {row['Budget_Range']}")
                        st.markdown(f"**Timeline:** {row['Timeline']}")
                        st.markdown(f"**Submitted:** {row['Submission_Date']}")
                    
                    st.markdown("**Current Challenges:**")
                    st.info(row['Current_Challenges'])
                    
                    st.markdown("**Desired Outcomes:**")
                    st.success(row['Desired_Outcomes'])
        else:
            st.info("📭 No submissions yet. Share the consultation form to start receiving leads!")

# Footer Section with Enhanced Copy
st.markdown("""
<div class="footer-section">
    <h2>🚀 The ATM Agency - Your AI Transformation Partner</h2>
    <p style="font-size: 1.2em;"><strong>Transforming Businesses with Intelligent Automation Since 2019</strong></p>
    <p style="font-size: 1em; margin-top: 1rem;">Led by D Hudson - 15+ Years of AI & Automation Expertise</p>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin: 3rem 0; text-align: left;">
        <div>
            <h4>📞 Contact D Hudson</h4>
            <p><strong>Priority Hotline:</strong> 6785589752</p>
            <p><strong>Email:</strong> info@entremotivator@gmail.com</p>
            <p><strong>Emergency Line:</strong> 6785589752</p>
            <p style="margin-top: 0.5rem; font-size: 0.9em;">Available 24/7 for urgent inquiries</p>
        </div>
        <div>
            <h4>🏢 Headquarters</h4>
            <p>123 Innovation Drive</p>
            <p>Tech Valley, CA 94000</p>
            <p>United States</p>
            <p style="margin-top: 0.5rem; font-size: 0.9em;">Serving clients worldwide</p>
        </div>
        <div>
            <h4>🌐 Connect With Us</h4>
            <p>LinkedIn: /company/the-atm-agency</p>
            <p>Website: www.theatmagency.com</p>
            <p>Blog: insights.theatmagency.com</p>
            <p style="margin-top: 0.5rem; font-size: 0.9em;">Follow for AI tips & case studies</p>
        </div>
        <div>
            <h4>⭐ Why Choose Us</h4>
            <p>✅ 500+ Successful Projects</p>
            <p>✅ 340% Average ROI</p>
            <p>✅ 98.5% Client Satisfaction</p>
            <p>✅ 24/7 Premium Support</p>
        </div>
    </div>
    
    <hr style="margin: 2rem 0; border-color: #555;">
    
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
        <p>© 2024 The ATM Agency. All Rights Reserved.</p>
        <p>🔒 SOC 2 Type II Certified | 🛡️ GDPR Compliant | ⭐ 98.5% Client Satisfaction</p>
    </div>
    
    <div style="margin-top: 2rem; padding: 1.5rem; background: rgba(255,255,255,0.1); border-radius: 8px;">
        <p style="font-size: 1.1em; margin-bottom: 1rem;"><strong>🎯 Ready to Transform Your Business?</strong></p>
        <p>Don't wait another day to start saving money and scaling your operations.</p>
        <p style="margin-top: 1rem;"><strong>Call Now: 6785589752</strong> or scroll up to claim your FREE $5,000 consultation package!</p>
    </div>
</div>
""", unsafe_allow_html=True) SOLUTION:</p>
        <p>AI-powered intelligent document processing + automated patient management system</p>
        
        <p style="color: #2980b9; font-weight: bold; font-size: 1.2em; margin-top: 1rem;">THE RESULTS:</p>
        <ul style="line-height: 2;">
            <li>✅ <strong>95% reduction</strong> in processing time</li>
            <li>✅ <strong>$200K saved</strong> in first year alone</li>
            <li>✅ <strong>99.8% accuracy</strong> rate (virtually error-free)</li>
            <li>✅ <strong>ROI achieved in just 3 months</strong></li>
            <li>✅ Staff can now focus on patient care, not paperwork</li>
        </ul>
        <p style="background: #d1f2eb; padding: 1rem; border-radius: 8px; margin-top: 1rem; font-style: italic;">
            "We went from overwhelmed to optimized in 90 days. Best decision we ever made." - Dr. Sarah M.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h4>🏭 Manufacturing: AutoParts Inc.</h4>
        <p style="color: #e74c3c; font-weight: bold; font-size: 1.2em;">THE CHALLENGE:</p>
        <p>Quality control nightmares. High defect rates. Losing contracts. Reputation at risk.</p>
        
        <p style="color: #27ae60; font-weight: bold; font-size: 1.2em; margin-top: 1rem;">THE ATM AGENCY SOLUTION:</p>
        <p>Computer vision AI for real-time automated quality inspection</p>
        
        <p style="color: #2980b9; font-weight: bold; font-size: 1.2em; margin-top: 1rem;">THE RESULTS:</p>
        <ul style="line-height: 2;">
            <li>✅ <strong>85% faster</strong> quality checks</li>
            <li>✅ <strong>60% reduction</strong> in defects</li>
            <li>✅ <strong>$500K saved</strong> annually</li>
            <li>✅ <strong>300% ROI</strong> in first year</li>
            <li>✅ Won back lost contracts + 3 new major clients</li>
        </ul>
        <p style="background: #d1f2eb; padding: 1rem; border-radius: 8px; margin-top: 1rem; font-style: italic;">
            "Our defect rate dropped from 12% to 2%. Customers are amazed. So are we." - Michael C., COO
        </p>
    </div>
    """, unsafe_allow_html=True)

# Additional success stories
col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="feature-box">
        <h4>🛒 E-Commerce: StartupX</h4>
        <p style="color: #e74c3c; font-weight: bold; font-size: 1.2em;">THE CHALLENGE:</p>
        <p>Small team, big ambitions. Couldn't scale. Manual everything. Losing sales to bigger competitors.</p>
        
        <p style="color: #27ae60; font-weight: bold; font-size: 1.2em; margin-top: 1rem;">THE ATM AGENCY SOLUTION:</p>
        <p>Full AI automation suite: customer service, inventory, marketing, analytics</p>
        
        <p style="color: #2980b9; font-weight: bold; font-size: 1.2em; margin-top: 1rem;">THE RESULTS:</p>
        <ul style="line-height: 2;">
            <li>✅ Team of 12 now operates like team of 100+</li>
            <li>✅ <strong>400% revenue growth</strong> ($500K → $2M)</li>
            <li>✅ Handle 10X more customers</li>
            <li>✅ 65% higher conversion rates</li>
            <li>✅ Outcompeting enterprise rivals</li>
        </ul>
        <p style="background: #d1f2eb; padding: 1rem; border-radius: 8px; margin-top: 1rem; font-style: italic;">
            "We're a startup punching way above our weight. All thanks to The ATM Agency." - Emma R., Founder
        </p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-box">
        <h4>💼 Consulting: TechCorp Inc.</h4>
        <p style="color: #e74c3c; font-weight: bold; font-size: 1.2em;">THE CHALLENGE:</p>
        <p>Customer support costs exploding. Response times too slow. Losing clients to faster competitors.</p>
        
        <p style="color: #27ae60; font-weight: bold; font-size: 1.2em; margin-top: 1rem;">THE ATM AGENCY
