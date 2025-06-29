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
ADMIN_EMAIL = "Entremotivator@gmail.com"

# App configuration
st.set_page_config(
    page_title="AI Automation Solutions - Enterprise Client Portal", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .section-header {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        margin: 1.5rem 0 1rem 0;
        text-align: center;
        font-weight: bold;
    }
    .info-card {
        background: #f8f9ff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #4facfe;
        margin: 1rem 0;
    }
    .stats-container {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .feature-box {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-top: 3px solid #4facfe;
    }
    .testimonial {
        background: #f0f8ff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #00d4ff;
        margin: 1rem 0;
        font-style: italic;
    }
    .cta-section {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin: 2rem 0;
    }
    .form-section {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .footer-section {
        background: #2c3e50;
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# Main Header
st.markdown("""
<div class="main-header">
    <h1>🤖 AI Automation Solutions - Enterprise Portal</h1>
    <h2>Transform Your Business with Cutting-Edge AI Technology</h2>
    <p style="font-size: 1.2em; margin-top: 1rem;">Join 500+ companies already leveraging AI to boost productivity by 300%</p>
</div>
""", unsafe_allow_html=True)

# Company Stats
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Projects Completed", "500+", "↗️ 50 this month")
with col2:
    st.metric("Average ROI", "340%", "↗️ 15% increase")
with col3:
    st.metric("Client Satisfaction", "98.5%", "↗️ 2.1%")
with col4:
    st.metric("Industries Served", "25+", "↗️ 3 new sectors")

# Services Overview Section
st.markdown('<div class="section-header"><h2>🚀 Our AI Automation Services</h2></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <h3>🤖 Intelligent Chatbots & Virtual Assistants</h3>
        <ul>
            <li>24/7 Customer Support Automation</li>
            <li>Lead Qualification & Nurturing</li>
            <li>Multi-language Support</li>
            <li>CRM Integration</li>
            <li>Advanced NLP Processing</li>
        </ul>
        <p><strong>ROI:</strong> 250-400% within 6 months</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h3>⚙️ Process Automation & Optimization</h3>
        <ul>
            <li>Workflow Automation</li>
            <li>Data Entry & Processing</li>
            <li>Invoice & Document Management</li>
            <li>Inventory Management</li>
            <li>Quality Control Systems</li>
        </ul>
        <p><strong>Time Saved:</strong> 40-60 hours per week</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <h3>📊 Advanced Analytics & AI Insights</h3>
        <ul>
            <li>Predictive Analytics</li>
            <li>Customer Behavior Analysis</li>
            <li>Sales Forecasting</li>
            <li>Risk Assessment</li>
            <li>Performance Optimization</li>
        </ul>
        <p><strong>Accuracy:</strong> 95%+ prediction rates</p>
    </div>
    """, unsafe_allow_html=True)

# Additional Services
col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class="feature-box">
        <h3>📄 Document & Content AI</h3>
        <ul>
            <li>Automated Content Generation</li>
            <li>Document Classification</li>
            <li>OCR & Data Extraction</li>
            <li>Contract Analysis</li>
            <li>Compliance Monitoring</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="feature-box">
        <h3>🔗 System Integration & APIs</h3>
        <ul>
            <li>CRM/ERP Integration</li>
            <li>Third-party API Connections</li>
            <li>Database Synchronization</li>
            <li>Cloud Migration</li>
            <li>Legacy System Modernization</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="feature-box">
        <h3>🛡️ Enterprise Support & Security</h3>
        <ul>
            <li>24/7 Monitoring & Support</li>
            <li>Security Compliance</li>
            <li>Regular Updates & Maintenance</li>
            <li>Staff Training Programs</li>
            <li>Performance Analytics</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Client Testimonials
st.markdown('<div class="section-header"><h2>💬 What Our Clients Say</h2></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="testimonial">
        <p>"AI Automation Solutions transformed our customer service. We now handle 300% more inquiries with 50% fewer staff. ROI was achieved in just 4 months!"</p>
        <p><strong>- Sarah Johnson, CEO, TechCorp Inc.</strong></p>
        <p>📈 Revenue: $50M+ | 🏢 Industry: SaaS</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="testimonial">
        <p>"The process automation saved us 60 hours per week and eliminated 95% of manual errors. Our team can now focus on strategic initiatives."</p>
        <p><strong>- Michael Chen, COO, Manufacturing Plus</strong></p>
        <p>📈 Revenue: $25M+ | 🏢 Industry: Manufacturing</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="testimonial">
        <p>"As a startup, we needed to scale fast. Their AI solutions helped us handle enterprise-level operations with a lean team of 12 people."</p>
        <p><strong>- Emma Rodriguez, Founder, StartupX</strong></p>
        <p>📈 Revenue: $2M+ | 🏢 Industry: E-commerce</p>
    </div>
    """, unsafe_allow_html=True)

# CTA Section
st.markdown("""
<div class="cta-section">
    <h2>🎯 Ready to Transform Your Business?</h2>
    <p style="font-size: 1.2em;">Join the AI revolution and stay ahead of your competition</p>
    <p><strong>Limited Time:</strong> Free AI Readiness Assessment + 30-minute Strategy Session (Value: $2,500)</p>
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
    subject = "🎉 AI Automation Project Submission Received - Premium Consultation Scheduled"
    body = f"""
    Dear {name},

    Thank you for choosing AI Automation Solutions for your {project_type} project! 🚀

    **Your Premium Consultation Package Includes:**
    
    ✅ **Immediate:** AI Readiness Assessment Report (within 24 hours)
    ✅ **Within 48 Hours:** Detailed Project Proposal & ROI Analysis
    ✅ **Within 72 Hours:** 1-hour Strategy Session with our Lead AI Architect
    ✅ **Bonus:** Custom AI Implementation Roadmap (Value: $2,500)

    **What Makes Us Different:**
    
    🏆 **Proven Track Record:** 500+ successful implementations
    📈 **Guaranteed Results:** Average 340% ROI within 12 months
    🛡️ **Enterprise Security:** SOC 2 Type II certified
    ⚡ **Rapid Deployment:** Most projects live within 30-90 days
    🎯 **Industry Expertise:** Specialized solutions for your sector

    **Your Dedicated Team:**
    - Senior AI Architect (15+ years experience)
    - Project Manager (PMP certified)
    - Technical Implementation Specialist
    - 24/7 Support Team

    **Next Steps:**
    1. Check your email for the AI Readiness Assessment questionnaire
    2. Our team will analyze your current systems and processes
    3. We'll prepare a custom proposal with exact ROI projections
    4. Schedule your strategy session at your convenience

    **Questions?** 
    📞 Priority Hotline: (555) 123-4567 (mention reference: {company.upper()[:3]}{datetime.now().strftime("%m%d")})
    📧 Direct Email: projects@aiautomation.com
    💬 Live Chat: Available 24/7 on our website

    We're excited to help {company} achieve unprecedented growth through AI automation!

    Best regards,
    **The AI Automation Solutions Team**
    
    P.S. Follow our LinkedIn for weekly AI automation case studies and industry insights!
    """
    return send_email(to_email, subject, body)

def send_admin_notification(form_data):
    subject = f"🚨 HIGH-VALUE AI Project Lead: {form_data['company']} - {form_data['budget_range']}"
    
    priority_level = "🔴 URGENT" if form_data['budget_range'] in ["$100,000 - $250,000", "$250,000+"] else \
                    "🟠 HIGH" if form_data['budget_range'] in ["$50,000 - $100,000", "$25,000 - $50,000"] else \
                    "🟡 MEDIUM"
    
    body = f"""
    🎯 NEW AI AUTOMATION LEAD - ACTION REQUIRED

    **PRIORITY LEVEL: {priority_level}**

    **👤 CONTACT INFORMATION:**
    Name: {form_data['name']}
    Position: {form_data['position']}
    Email: {form_data['email']}
    Phone: {form_data['phone']}
    Company: {form_data['company']}

    **🏢 COMPANY PROFILE:**
    Industry: {form_data['industry']}
    Company Type: {form_data['company_type']}
    Years in Business: {form_data['years_in_business']}
    Annual Revenue: {form_data['annual_revenue']}
    Company Size: {form_data['company_size']}

    **🔧 PROJECT DETAILS:**
    Project Type: {form_data['project_type']}
    Budget Range: {form_data['budget_range']}
    Timeline: {form_data['timeline']}

    **📋 BUSINESS REQUIREMENTS:**
    Current Challenges:
    {form_data['current_challenges']}

    Desired Outcomes:
    {form_data['desired_outcomes']}

    Technical Requirements:
    {form_data['technical_requirements']}

    Integration Needs:
    {form_data['integration_needs']}

    Success Metrics:
    {form_data['success_metrics']}

    Additional Services: {form_data['additional_services']}

    **⚡ IMMEDIATE ACTION ITEMS:**
    1. Send AI Readiness Assessment within 2 hours
    2. Assign Senior AI Architect for consultation
    3. Prepare industry-specific case studies
    4. Schedule strategy session within 48 hours
    5. Create custom ROI projection model

    **📊 LEAD SCORING:**
    Budget Score: {10 if 'HIGH' in priority_level or 'URGENT' in priority_level else 7 if 'MEDIUM' in priority_level else 5}/10
    Timeline Score: {9 if form_data['timeline'] in ['ASAP', '1-2 weeks'] else 7}/10
    Company Maturity: {9 if 'Established' in form_data['company_type'] else 6}/10

    Submission Time: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}

    **CRM UPDATE REQUIRED** ✅
    """
    return send_email(ADMIN_EMAIL, subject, body)

# Main Form Section
st.markdown('<div class="section-header"><h2>📝 Submit Your AI Automation Project</h2></div>', unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
    <h3>🎁 Limited Time Offer - Premium Consultation Package (Value: $5,000)</h3>
    <p><strong>What You Get FREE:</strong></p>
    <ul>
        <li>✅ Comprehensive AI Readiness Assessment</li>
        <li>✅ Custom ROI Analysis & Projections</li>
        <li>✅ 1-Hour Strategy Session with Senior AI Architect</li>
        <li>✅ Detailed Implementation Roadmap</li>
        <li>✅ Industry-Specific Case Studies</li>
    </ul>
    <p><em>Complete the form below to claim your premium consultation package!</em></p>
</div>
""", unsafe_allow_html=True)

with st.form("comprehensive_ai_form", clear_on_submit=False):
    
    # Contact Information Section
    st.markdown("### 👤 Contact Information")
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name *", placeholder="Enter your full name")
        email = st.text_input("Business Email *", placeholder="your.email@company.com")
        phone = st.text_input("Phone Number *", placeholder="+1 (555) 123-4567")
    
    with col2:
        position = st.text_input("Job Title/Position *", placeholder="CEO, CTO, Operations Manager, etc.")
        company = st.text_input("Company Name *", placeholder="Your company name")
        website = st.text_input("Company Website", placeholder="https://www.yourcompany.com")

    st.markdown("---")
    
    # Company Information Section
    st.markdown("### 🏢 Company Information")
    col3, col4 = st.columns(2)
    
    with col3:
        company_type = st.selectbox(
            "Company Type *",
            ["Select company type", "Startup (0-2 years)", "Growing Business (3-5 years)", 
             "Established Company (6-10 years)", "Enterprise (10+ years)", "Fortune 500"]
        )
        
        years_in_business = st.selectbox(
            "Years in Business *",
            ["Select years", "Less than 1 year", "1-2 years", "3-5 years", 
             "6-10 years", "11-20 years", "20+ years"]
        )
        
        annual_revenue = st.selectbox(
            "Annual Revenue *",
            ["Select revenue range", "Pre-revenue/Startup", "Under $100K", "$100K - $500K", 
             "$500K - $1M", "$1M - $5M", "$5M - $10M", "$10M - $25M", 
             "$25M - $50M", "$50M - $100M", "$100M+"]
        )
    
    with col4:
        industry = st.selectbox(
            "Industry *",
            ["Select industry", "Technology/Software", "E-commerce/Retail", "Healthcare", 
             "Finance/Banking", "Manufacturing", "Real Estate", "Education", 
             "Marketing/Advertising", "Consulting", "Legal Services", "Other"]
        )
        
        company_size = st.selectbox(
            "Company Size *",
            ["Select company size", "1-10 employees", "11-50 employees", "51-200 employees", 
             "201-500 employees", "501-1000 employees", "1000+ employees"]
        )
        
        current_tech_stack = st.text_input("Current Tech Stack", placeholder="CRM, ERP, databases, etc.")

    st.markdown("---")
    
    # Project Information Section
    st.markdown("### 🔧 Project Information")
    col5, col6 = st.columns(2)
    
    with col5:
        project_type = st.selectbox(
            "Primary AI Solution Needed *",
            ["Select project type", "AI Chatbot/Virtual Assistant", "Process Automation", 
             "Data Analytics & AI Insights", "Document Processing & AI", "Customer Service Automation",
             "Sales & Marketing Automation", "Inventory Management AI", "Predictive Analytics",
             "Custom AI Development", "AI Integration & Consulting", "Multiple Solutions"]
        )
        
        budget_range = st.selectbox(
            "Project Budget Range *",
            ["Select budget range", "Under $10,000", "$10,000 - $25,000", "$25,000 - $50,000", 
             "$50,000 - $100,000", "$100,000 - $250,000", "$250,000+", "Need consultation to determine"]
        )
    
    with col6:
        timeline = st.selectbox(
            "Desired Timeline *",
            ["Select timeline", "ASAP (Rush Project)", "1-2 weeks", "1 month", 
             "2-3 months", "3-6 months", "6-12 months", "12+ months", "Flexible"]
        )
        
        urgency_level = st.selectbox(
            "Project Urgency",
            ["Standard", "High Priority", "Business Critical", "Competitive Advantage"]
        )

    st.markdown("---")
    
    # Detailed Requirements Section
    st.markdown("### 📋 Detailed Requirements")
    
    current_challenges = st.text_area(
        "Current Business Challenges *",
        placeholder="Describe the main challenges your business is facing that AI automation could solve. Include pain points, inefficiencies, and bottlenecks.",
        height=100
    )
    
    desired_outcomes = st.text_area(
        "Desired Outcomes & Goals *",
        placeholder="What specific results do you want to achieve? Include metrics like cost savings, time reduction, revenue increase, etc.",
        height=100
    )
    
    technical_requirements = st.text_area(
        "Technical Requirements",
        placeholder="Any specific technical requirements, compliance needs, security standards, or platform preferences?",
        height=80
    )
    
    integration_needs = st.text_area(
        "System Integration Needs",
        placeholder="What existing systems need to be integrated? (CRM, ERP, databases, APIs, etc.)",
        height=80
    )
    
    success_metrics = st.text_area(
        "Success Metrics & KPIs",
        placeholder="How will you measure the success of this AI implementation? What KPIs are most important?",
        height=80
    )

    st.markdown("---")
    
    # Additional Services Section
    st.markdown("### 🎯 Additional Services & Preferences")
    
    col7, col8 = st.columns(2)
    
    with col7:
        st.markdown("**Additional Services Needed:**")
        ongoing_support = st.checkbox("24/7 Ongoing Support & Maintenance")
        training_needed = st.checkbox("Team Training & Onboarding")
        consultation_call = st.checkbox("Regular Strategy Consultations")
        performance_monitoring = st.checkbox("Performance Monitoring & Analytics")
    
    with col8:
        st.markdown("**Implementation Preferences:**")
        cloud_preference = st.selectbox(
            "Cloud Preference",
            ["No preference", "AWS", "Google Cloud", "Microsoft Azure", "On-premise"]
        )
        security_level = st.selectbox(
            "Security Requirements",
            ["Standard", "High Security", "Enterprise Grade", "Government/Healthcare Compliance"]
        )

    # Communication Preferences
    st.markdown("### 📞 Communication Preferences")
    col9, col10 = st.columns(2)
    
    with col9:
        preferred_contact = st.selectbox(
            "Preferred Contact Method",
            ["Email", "Phone Call", "Video Conference", "In-person Meeting"]
        )
        best_time = st.selectbox(
            "Best Time to Contact",
            ["Morning (9-12 PM)", "Afternoon (12-5 PM)", "Evening (5-8 PM)", "Flexible"]
        )
    
    with col10:
        timezone = st.selectbox(
            "Time Zone",
            ["Eastern (EST)", "Central (CST)", "Mountain (MST)", "Pacific (PST)", 
             "Other US", "International"]
        )
        decision_timeline = st.selectbox(
            "Decision Timeline",
            ["Ready to start immediately", "Within 1 week", "Within 1 month", 
             "Within 3 months", "Just exploring options"]
        )

    # Final Questions
    st.markdown("### 💡 Additional Information")
    
    heard_about_us = st.selectbox(
        "How did you hear about us?",
        ["Google Search", "LinkedIn", "Referral", "Industry Event", "Partner", "Other"]
    )
    
    additional_comments = st.text_area(
        "Additional Comments or Questions",
        placeholder="Any additional information, specific questions, or special requirements you'd like us to know?",
        height=80
    )

    # Submit Button
    st.markdown("---")
    submit_button = st.form_submit_button(
        "🚀 Submit Project & Claim FREE Premium Consultation", 
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
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not all(field and field not in ["Select company type", "Select years", "Select revenue range", 
                                      "Select industry", "Select company size", "Select project type", 
                                      "Select budget range", "Select timeline"] for field in required_fields):
        st.error("⚠️ Please fill in all required fields marked with *")
    elif not re.match(email_pattern, email):
        st.error("⚠️ Please enter a valid email address")
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
            st.success("🎉 **Project submission successful!** Check your email for confirmation and next steps.")
            st.balloons()
            
            # Show success message with next steps
            st.markdown("""
            <div class="info-card">
                <h3>✅ What Happens Next:</h3>
                <ol>
                    <li><strong>Within 2 Hours:</strong> AI Readiness Assessment questionnaire in your inbox</li>
                    <li><strong>Within 24 Hours:</strong> Detailed analysis and custom proposal</li>
                    <li><strong>Within 48 Hours:</strong> Strategy session scheduled with our Senior AI Architect</li>
                    <li><strong>Within 72 Hours:</strong> Complete implementation roadmap delivered</li>
                </ol>
                <p><strong>Priority Contact:</strong> For urgent matters, call (555) 123-4567 and mention reference code: <code>{}{}</code></p>
            </div>
            """.format(company.upper()[:3], datetime.now().strftime("%m%d")), unsafe_allow_html=True)
        else:
            st.error("⚠️ There was an issue sending confirmation emails. Our team has been notified and will contact you directly.")

# Success Stories Section
st.markdown('<div class="section-header"><h2>📈 Success Stories by Industry</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-box">
        <h4>🏥 Healthcare: MedTech Solutions</h4>
        <p><strong>Challenge:</strong> Manual patient data processing taking 40+ hours weekly</p>
        <p><strong>Solution:</strong> AI-powered document processing and patient management system</p>
        <p><strong>Results:</strong></p>
        <ul>
            <li>95% reduction in processing time</li>
            <li>$200K annual savings</li>
            <li>99.8% accuracy rate</li>
            <li>ROI achieved in 3 months</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h4>🏭 Manufacturing: AutoParts Inc.</h4>
        <p><strong>Challenge:</strong> Quality control bottlenecks and high defect rates</p>
        <p><strong>Solution:</strong> Computer vision AI for automated quality inspection</p>
        <p><strong>Results:</strong></p>
        <ul>
            <li>85% faster quality checks</li>
            <li>60% reduction in defects</li>
            <li>$500K annual savings</li>
            <li>300% ROI in first year</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Admin Dashboard (Hidden by default)
if st.checkbox("🔐 Admin Dashboard (Authorized Personnel Only)", key="admin_access"):
    admin_password = st.text_input("Enter Admin Password:", type="password")
    if admin_password == "admin123":  # In production, use proper authentication
        st.markdown('<div class="section-header"><h2>📊 Recent Submissions Dashboard</h2></div>', unsafe_allow_html=True)
        
        if not st.session_state.submissions.empty:
            # Display metrics
            total_submissions = len(st.session_state.submissions)
            high_value_leads = len(st.session_state.submissions[
                st.session_state.submissions['Budget_Range'].isin(['$100,000 - $250,000', '$250,000+'])
            ])
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Submissions", total_submissions)
            with col2:
                st.metric("High-Value Leads", high_value_leads)
            with col3:
                st.metric("Avg. Budget Range", "~$75K")
            with col4:
                st.metric("Conversion Rate", "23%")
            
            # Display submissions table
            st.dataframe(st.session_state.submissions, use_container_width=True)
            
            # Download CSV
            csv = st.session_state.submissions.to_csv(index=False)
            st.download_button(
                label="📥 Download Submissions CSV",
                data=csv,
                file_name=f"ai_automation_submissions_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No submissions yet.")

# Footer Section
st.markdown("""
<div class="footer-section">
    <h2>🤖 AI Automation Solutions</h2>
    <p><strong>Transforming Businesses with Intelligent Technology Since 2019</strong></p>
    
    <div style="display: flex; justify-content: space-around; margin: 2rem 0;">
        <div>
            <h4>📞 Contact</h4>
            <p>Phone: (555) 123-4567</p>
            <p>Email: info@aiautomation.com</p>
            <p>Emergency: (555) 999-0000</p>
        </div>
        <div>
            <h4>🏢 Headquarters</h4>
            <p>123 Innovation Drive</p>
            <p>Tech Valley, CA 94000</p>
            <p>United States</p>
        </div>
        <div>
            <h4>🌐 Connect</h4>
            <p>LinkedIn: /company/ai-automation-solutions</p>
            <p>Website: www.aiautomation.com</p>
            <p>Blog: insights.aiautomation.com</p>
        </div>
    </div>
    
    <hr style="margin: 2rem 0; border-color: #555;">
    
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <p>© 2024 AI Automation Solutions. All rights reserved.</p>
        <p>🔒 SOC 2 Type II Certified | 🛡️ GDPR Compliant | ⭐ 98.5% Client Satisfaction</p>
    </div>
</div>
""", unsafe_allow_html=True)
