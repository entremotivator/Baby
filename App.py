import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import re
import requests
import json

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="The AI Meet Up",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# SECRETS / CONFIG
# ─────────────────────────────────────────────
try:
    EMAIL_ADDRESS = st.secrets["email"]["sender_email"]
    EMAIL_PASSWORD = st.secrets["email"]["password"]
    SMTP_SERVER   = st.secrets["email"]["smtp_server"]
    PORT          = int(st.secrets["email"]["port"])
    EMAIL_ENABLED = True
except Exception:
    EMAIL_ADDRESS = ""
    EMAIL_PASSWORD = ""
    SMTP_SERVER   = "smtp.gmail.com"
    PORT          = 587
    EMAIL_ENABLED = False

ADMIN_EMAIL    = "entremotivator@gmail.com"
N8N_WEBHOOK_URL = "https://agentonline-u29564.vm.elestio.app/webhook-test/Consultaientre"
FLYER_URL      = "https://raw.githubusercontent.com/entremotivator/aimeetup/main/ai_meetup_flyer_letter.png"
EVENT_URL      = "https://entremotivator.com/events/the-ai-meet-up/"
PHONE          = "6785589752"

TODAY_DATE     = "February 20, 2026"
TODAY_TIME     = "5:00 – 8:00 PM"
TODAY_LOCATION = "Ellenwood, GA"
TODAY_HOST     = "Donmenico Hudson / EntreMotivator"
NEXT_DATE      = "March 27, 2026"
NEXT_TIME      = "5:00 – 8:00 PM"
NEXT_LOCATION  = "Ellenwood, GA"

# ─────────────────────────────────────────────
# EMAIL UTILITIES
# ─────────────────────────────────────────────
def _send_email(to_email: str, subject: str, html_body: str) -> bool:
    """Core SMTP send function."""
    if not EMAIL_ENABLED:
        return False
    try:
        msg = MIMEMultipart("alternative")
        msg["From"]    = EMAIL_ADDRESS
        msg["To"]      = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(html_body, "html"))
        with smtplib.SMTP(SMTP_SERVER, PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        return True
    except Exception as e:
        st.warning(f"Email could not be sent: {e}")
        return False


def send_to_n8n(payload: dict) -> bool:
    """Forward form data to n8n webhook."""
    try:
        r = requests.post(
            N8N_WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        return r.status_code in [200, 201, 204]
    except Exception:
        return False


# ── Consultation emails ──────────────────────
def send_consult_confirmation(to_email: str, name: str, company: str) -> bool:
    subject = "✅ Your FREE $100 AI Consultation is Confirmed — We'll Reach Out in 24 Hours!"
    body = f"""
<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
  body{{font-family:Arial,sans-serif;background:#f4f4f4;color:#333;margin:0;padding:20px;}}
  .wrap{{max-width:600px;margin:auto;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,.1);}}
  .hdr{{background:linear-gradient(135deg,#1a1a1a,#2d2d2d);color:#ffd700;padding:30px;text-align:center;border-bottom:3px solid #ffd700;}}
  .hdr h1{{margin:0;font-size:26px;color:#ffd700;}}
  .body{{padding:30px;}}
  .card{{background:#f9f9f9;border-left:4px solid #ffd700;border-radius:8px;padding:18px;margin:18px 0;}}
  .card h3{{margin:0 0 8px;color:#1a1a1a;}}
  .btn{{display:inline-block;background:linear-gradient(135deg,#ffd700,#ffaa00);color:#1a1a1a;font-weight:800;
        padding:14px 32px;border-radius:50px;text-decoration:none;font-size:16px;margin:20px 0;}}
  .ftr{{background:#1a1a1a;color:#ffd700;padding:20px;text-align:center;font-size:13px;}}
</style></head><body>
<div class="wrap">
  <div class="hdr">
    <h1>🤖 The AI Meet Up</h1>
    <p style="margin:6px 0;color:#fff;">FREE $100 AI Consultation Confirmed</p>
  </div>
  <div class="body">
    <p>Hi <strong>{name}</strong>,</p>
    <p>Your <strong style="color:#b8860b;">FREE $100 AI Consultation</strong> request has been received!
       Our team will reach out within <strong>24 hours</strong> to schedule your session.</p>
    <div class="card">
      <h3>🎁 Your Consultation Includes:</h3>
      <ul>
        <li>✅ 30-Minute 1-on-1 AI Strategy Session</li>
        <li>✅ Personalized AI Readiness Assessment</li>
        <li>✅ Custom Quick-Win Recommendations</li>
        <li>✅ Follow-Up Action Plan via Email</li>
      </ul>
    </div>
    <div class="card">
      <h3>⏭ What Happens Next?</h3>
      <ol>
        <li>Our team reviews your submission</li>
        <li>We reach out within <strong>24 hours</strong></li>
        <li>We schedule your FREE 30-minute AI strategy call</li>
        <li>You walk away with a clear AI action plan</li>
      </ol>
    </div>
    <p style="text-align:center;">
      <a href="{EVENT_URL}" class="btn">🌐 Visit Our Event Page</a>
    </p>
    <p>Questions? Email us at <a href="mailto:{ADMIN_EMAIL}">{ADMIN_EMAIL}</a>
       or call <a href="tel:{PHONE}">{PHONE}</a>.</p>
  </div>
  <div class="ftr">
    🤖 The AI Meet Up &nbsp;|&nbsp; Presented by EntreMotivator &nbsp;|&nbsp; {ADMIN_EMAIL}
  </div>
</div>
</body></html>
"""
    return _send_email(to_email, subject, body)


def send_consult_admin_alert(form: dict) -> bool:
    subject = f"🚨 NEW FREE CONSULTATION REQUEST — {form['name']} | {form['company']}"
    body = f"""
<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
  body{{font-family:Arial,sans-serif;background:#f4f4f4;color:#333;margin:0;padding:20px;}}
  .wrap{{max-width:620px;margin:auto;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,.1);}}
  .hdr{{background:linear-gradient(135deg,#1a1a1a,#2d2d2d);color:#ffd700;padding:24px;text-align:center;border-bottom:3px solid #ffd700;}}
  .hdr h1{{margin:0;font-size:22px;color:#ffd700;}}
  .body{{padding:28px;}}
  .row{{display:flex;padding:8px 0;border-bottom:1px solid #eee;}}
  .lbl{{font-weight:700;color:#555;min-width:160px;}}
  .val{{color:#222;}}
  .priority{{background:#fff3cd;border:2px solid #ffd700;border-radius:8px;padding:14px;
             text-align:center;font-weight:800;font-size:15px;color:#856404;margin:16px 0;}}
  .btn{{display:inline-block;background:linear-gradient(135deg,#ffd700,#ffaa00);color:#1a1a1a;
        font-weight:800;padding:12px 28px;border-radius:50px;text-decoration:none;font-size:15px;}}
  .ftr{{background:#1a1a1a;color:#ffd700;padding:18px;text-align:center;font-size:12px;}}
</style></head><body>
<div class="wrap">
  <div class="hdr">
    <h1>🚨 NEW CONSULTATION LEAD</h1>
    <p style="margin:4px 0;color:#fff;">AI Meet Up — Free $100 Consultation Request</p>
  </div>
  <div class="body">
    <div class="priority">⚡ PRIORITY LEAD — FOLLOW UP WITHIN 24 HOURS ⚡</div>
    <h3>👤 Contact Information</h3>
    <div class="row"><span class="lbl">Name:</span><span class="val">{form['name']}</span></div>
    <div class="row"><span class="lbl">Email:</span><span class="val"><a href="mailto:{form['email']}">{form['email']}</a></span></div>
    <div class="row"><span class="lbl">Phone:</span><span class="val"><a href="tel:{form['phone']}">{form['phone']}</a></span></div>
    <div class="row"><span class="lbl">Job Title:</span><span class="val">{form['position']}</span></div>
    <div class="row"><span class="lbl">Company:</span><span class="val">{form['company']}</span></div>
    <h3>🏢 Business Details</h3>
    <div class="row"><span class="lbl">Industry:</span><span class="val">{form['industry']}</span></div>
    <div class="row"><span class="lbl">Company Size:</span><span class="val">{form['company_size']}</span></div>
    <div class="row"><span class="lbl">Project Type:</span><span class="val">{form['project_type']}</span></div>
    <div class="row"><span class="lbl">Budget:</span><span class="val"><strong>{form['budget_range']}</strong></span></div>
    <div class="row"><span class="lbl">Timeline:</span><span class="val">{form['timeline']}</span></div>
    <div class="row"><span class="lbl">Heard From:</span><span class="val">{form.get('heard_from','—')}</span></div>
    <h3>📋 Project Details</h3>
    <p><strong>Challenges:</strong><br>{form['current_challenges']}</p>
    <p><strong>Desired Outcomes:</strong><br>{form['desired_outcomes']}</p>
    <p style="text-align:center;margin-top:20px;">
      <a href="mailto:{form['email']}" class="btn">📧 Reply to Lead Now</a>
    </p>
    <p style="font-size:12px;color:#888;margin-top:16px;">
      Submitted: {datetime.now().strftime("%B %d, %Y at %I:%M %p")} &nbsp;|&nbsp;
      Respond within 24 hours for best conversion
    </p>
  </div>
  <div class="ftr">The AI Meet Up &nbsp;|&nbsp; Internal Lead Notification &nbsp;|&nbsp; EntreMotivator.com</div>
</div>
</body></html>
"""
    return _send_email(ADMIN_EMAIL, subject, body)


# ── RSVP emails ──────────────────────────────
def send_rsvp_confirmation(to_email: str, name: str) -> bool:
    subject = "🎟 You're Registered! The AI Meet Up — March 27, 2026"
    body = f"""
<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
  body{{font-family:Arial,sans-serif;background:#f4f4f4;color:#333;margin:0;padding:20px;}}
  .wrap{{max-width:600px;margin:auto;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,.1);}}
  .hdr{{background:linear-gradient(135deg,#1a1a1a,#2d2d2d);color:#ffd700;padding:30px;text-align:center;border-bottom:3px solid #ffd700;}}
  .hdr h1{{margin:0;font-size:26px;color:#ffd700;}}
  .body{{padding:30px;}}
  .card{{background:#f9f9f9;border-left:4px solid #ffd700;border-radius:8px;padding:18px;margin:18px 0;}}
  .card h3{{margin:0 0 8px;color:#1a1a1a;}}
  .btn{{display:inline-block;background:linear-gradient(135deg,#ffd700,#ffaa00);color:#1a1a1a;font-weight:800;
        padding:14px 32px;border-radius:50px;text-decoration:none;font-size:16px;margin:20px 0;}}
  .ftr{{background:#1a1a1a;color:#ffd700;padding:20px;text-align:center;font-size:13px;}}
</style></head><body>
<div class="wrap">
  <div class="hdr">
    <h1>🤖 The AI Meet Up</h1>
    <p style="margin:6px 0;color:#fff;">You're officially registered!</p>
  </div>
  <div class="body">
    <p>Hey <strong>{name}</strong>! 🎉</p>
    <p>You're on the list for <strong>The AI Meet Up — March 27, 2026</strong>!
       We can't wait to see you there.</p>
    <div class="card">
      <h3>📅 Event Details</h3>
      <p><strong>Date:</strong> March 27, 2026</p>
      <p><strong>Time:</strong> 5:00 PM – 8:00 PM</p>
      <p><strong>Location:</strong> Ellenwood, GA</p>
      <p><strong>Cost:</strong> FREE</p>
    </div>
    <div class="card">
      <h3>🔥 What to Expect</h3>
      <ul>
        <li>🎤 Expert Talks from AI leaders</li>
        <li>🖥 Live AI Demonstrations</li>
        <li>🛠 Hands-On Workshops</li>
        <li>🥂 Networking Mixer</li>
        <li>💡 Innovation Showcase</li>
        <li>🤖 AI Keynote Presentation</li>
      </ul>
    </div>
    <p style="text-align:center;">
      <a href="{EVENT_URL}" class="btn">🌐 View Event Page</a>
    </p>
    <p>Questions? Email <a href="mailto:{ADMIN_EMAIL}">{ADMIN_EMAIL}</a>
       or call <a href="tel:{PHONE}">{PHONE}</a>.</p>
  </div>
  <div class="ftr">
    🤖 The AI Meet Up &nbsp;|&nbsp; Presented by EntreMotivator &nbsp;|&nbsp; {ADMIN_EMAIL}
  </div>
</div>
</body></html>
"""
    return _send_email(to_email, subject, body)


def send_rsvp_admin_alert(form: dict) -> bool:
    subject = f"🎟 NEW RSVP — {form['name']} | {form.get('city','N/A')} | The AI Meet Up Mar 27"
    body = f"""
<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
  body{{font-family:Arial,sans-serif;background:#f4f4f4;color:#333;margin:0;padding:20px;}}
  .wrap{{max-width:600px;margin:auto;background:#fff;border-radius:12px;overflow:hidden;}}
  .hdr{{background:linear-gradient(135deg,#1a1a1a,#2d2d2d);color:#ffd700;padding:22px;text-align:center;border-bottom:3px solid #ffd700;}}
  .hdr h1{{margin:0;font-size:20px;color:#ffd700;}}
  .body{{padding:26px;}}
  .row{{display:flex;padding:8px 0;border-bottom:1px solid #eee;}}
  .lbl{{font-weight:700;color:#555;min-width:150px;}}
  .val{{color:#222;}}
  .ftr{{background:#1a1a1a;color:#ffd700;padding:16px;text-align:center;font-size:12px;}}
</style></head><body>
<div class="wrap">
  <div class="hdr"><h1>🎟 NEW RSVP — The AI Meet Up March 27</h1></div>
  <div class="body">
    <div class="row"><span class="lbl">Name:</span><span class="val">{form['name']}</span></div>
    <div class="row"><span class="lbl">Email:</span><span class="val"><a href="mailto:{form['email']}">{form['email']}</a></span></div>
    <div class="row"><span class="lbl">Phone:</span><span class="val">{form.get('phone','—')}</span></div>
    <div class="row"><span class="lbl">City:</span><span class="val">{form.get('city','—')}</span></div>
    <div class="row"><span class="lbl">Interests:</span><span class="val">{', '.join(form.get('interests', [])) or '—'}</span></div>
    <div class="row"><span class="lbl">Heard From:</span><span class="val">{form.get('how','—')}</span></div>
    <div class="row"><span class="lbl">Notes:</span><span class="val">{form.get('notes','—')}</span></div>
    <p style="font-size:12px;color:#888;margin-top:14px;">
      Submitted: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}
    </p>
  </div>
  <div class="ftr">The AI Meet Up &nbsp;|&nbsp; RSVP Notification &nbsp;|&nbsp; EntreMotivator.com</div>
</div>
</body></html>
"""
    return _send_email(ADMIN_EMAIL, subject, body)


# ─────────────────────────────────────────────
# GLOBAL STYLES — Gold & Black
# ─────────────────────────────────────────────
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0d0d0d; color: #f0f0f0;
}
[data-testid="stSidebar"] { background-color: #111111; }
#MainMenu, footer, header { visibility: hidden; }
h1, h2, h3, h4 { color: #ffd700 !important; }
p, li, label, span { color: #e8e8e8; }

.hero-banner {
    background: linear-gradient(160deg, #0d0d0d 0%, #1a1200 50%, #0d0d0d 100%);
    border: 2px solid #ffd700; border-radius: 20px; padding: 3rem 2rem;
    text-align: center; margin-bottom: 2rem; box-shadow: 0 0 60px rgba(255,215,0,0.25);
}
.hero-banner h1 {
    font-size: 3.2rem; font-weight: 900; color: #ffd700 !important;
    text-shadow: 0 0 30px rgba(255,215,0,0.6); margin: 0 0 0.5rem 0; letter-spacing: 2px;
}
.hero-banner .subtitle { font-size: 1.2rem; color: #ffffff; margin: 0.4rem 0; }
.hero-banner .event-pill {
    display: inline-block; background: #ffd700; color: #0d0d0d; font-weight: 800;
    font-size: 1.1rem; padding: 0.5rem 2rem; border-radius: 50px; margin-top: 1rem;
}
.hero-banner .event-meta { font-size: 1rem; color: #cccccc; margin-top: 0.6rem; }

.section-hdr {
    background: linear-gradient(90deg, #1a1200, #2a1f00, #1a1200);
    border-left: 5px solid #ffd700; border-right: 5px solid #ffd700;
    border-radius: 10px; padding: 1rem 1.5rem; margin: 2.5rem 0 1.5rem 0;
    text-align: center; box-shadow: 0 4px 20px rgba(255,215,0,0.2);
}
.section-hdr h2 { margin: 0; font-size: 1.8rem; color: #ffd700 !important; }

.gold-card {
    background: linear-gradient(145deg, #1a1a1a, #111111);
    border: 1px solid #ffd700; border-radius: 14px; padding: 1.5rem; margin: 0.8rem 0;
    box-shadow: 0 4px 20px rgba(255,215,0,0.15); color: #e8e8e8;
}
.gold-card h3 { color: #ffd700 !important; margin-top: 0; }

.agenda-row {
    display: flex; align-items: flex-start; gap: 1rem;
    padding: 1.1rem 0; border-bottom: 1px solid #2a2a2a;
}
.agenda-time {
    background: #ffd700; color: #0d0d0d; font-weight: 800; font-size: 0.88rem;
    padding: 0.35rem 0.9rem; border-radius: 20px; white-space: nowrap;
    min-width: 130px; text-align: center; flex-shrink: 0;
}
.agenda-title { font-weight: 700; color: #ffffff; font-size: 1.05rem; }
.agenda-desc  { color: #aaaaaa; font-size: 0.9rem; margin-top: 0.2rem; }

.feature-box {
    background: linear-gradient(145deg, #1a1a1a, #0f0f0f);
    border: 2px solid #ffd700; border-radius: 14px; padding: 1.4rem;
    text-align: center; height: 100%; box-shadow: 0 6px 25px rgba(255,215,0,0.2);
}
.feature-box .icon { font-size: 2.4rem; margin-bottom: 0.4rem; }
.feature-box h3   { color: #ffd700 !important; font-size: 1rem; margin: 0.4rem 0; }
.feature-box p    { color: #cccccc; font-size: 0.88rem; margin: 0; }

.pulse-banner {
    background: linear-gradient(135deg, #1a1200, #2a1f00);
    border: 3px solid #ffd700; border-radius: 12px; padding: 1.2rem 2rem;
    text-align: center; color: #ffd700; font-weight: 800; font-size: 1.1rem;
    animation: glow 2s ease-in-out infinite; margin: 1.5rem 0;
}
@keyframes glow {
    0%,100% { box-shadow: 0 0 15px rgba(255,215,0,0.3); }
    50%      { box-shadow: 0 0 40px rgba(255,215,0,0.7); }
}

.cta-btn {
    display: inline-block;
    background: linear-gradient(135deg, #ffd700, #ffaa00);
    color: #0d0d0d !important; font-weight: 900; font-size: 1.15rem;
    padding: 1rem 3rem; border-radius: 50px; text-decoration: none !important;
    box-shadow: 0 6px 25px rgba(255,215,0,0.5); letter-spacing: 1px;
}

.vote-city {
    background: #1a1a1a; border: 1px solid #333; border-radius: 10px;
    padding: 0.8rem 1rem; margin: 0.4rem 0; display: flex;
    align-items: center; gap: 0.8rem; color: #e8e8e8; font-size: 1rem;
}

.consult-banner {
    background: linear-gradient(135deg, #0d0d0d, #1a1200);
    border: 3px solid #ffd700; border-radius: 16px; padding: 2rem;
    text-align: center; margin: 1.5rem 0; box-shadow: 0 0 40px rgba(255,215,0,0.3);
}
.consult-banner h2  { color: #ffd700 !important; font-size: 2rem; margin: 0 0 0.5rem 0; }
.consult-banner .price {
    font-size: 3rem; font-weight: 900; color: #ffd700;
    text-shadow: 0 0 20px rgba(255,215,0,0.6);
}
.consult-banner .tagline { color: #cccccc; font-size: 1.05rem; margin-top: 0.5rem; }

[data-testid="stMetricValue"] { color: #ffd700 !important; font-weight: 800; }
[data-testid="stMetricLabel"] { color: #cccccc !important; }
.stButton > button {
    background: linear-gradient(135deg, #ffd700, #ffaa00) !important;
    color: #0d0d0d !important; font-weight: 800 !important; border: none !important;
    border-radius: 50px !important; padding: 0.7rem 2rem !important;
    font-size: 1rem !important; box-shadow: 0 4px 15px rgba(255,215,0,0.4) !important;
}
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background-color: #1a1a1a !important; color: #f0f0f0 !important;
    border: 1px solid #ffd700 !important; border-radius: 8px !important;
}
.stCheckbox > label { color: #e8e8e8 !important; }
[data-testid="stForm"] {
    background: #111111; border: 1px solid #2a2a2a;
    border-radius: 14px; padding: 1.5rem;
}
.stTabs [data-baseweb="tab-list"] { background: #111111; border-radius: 10px; gap: 4px; }
.stTabs [data-baseweb="tab"] {
    background: #1a1a1a; color: #ffd700; border-radius: 8px;
    font-weight: 700; border: 1px solid #333;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #ffd700, #ffaa00) !important;
    color: #0d0d0d !important;
}
hr { border-color: #2a2a2a; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "city_votes"        not in st.session_state: st.session_state.city_votes = {
    "Atlanta, GA": 0, "Houston, TX": 0, "Miami, FL": 0,
    "New York, NY": 0, "Los Angeles, CA": 0, "Chicago, IL": 0,
    "Dallas, TX": 0, "Charlotte, NC": 0, "Washington, DC": 0,
    "Detroit, MI": 0, "Philadelphia, PA": 0, "Nashville, TN": 0,
}
if "voted_city"        not in st.session_state: st.session_state.voted_city        = None
if "rsvp_submitted"    not in st.session_state: st.session_state.rsvp_submitted    = False
if "consult_submitted" not in st.session_state: st.session_state.consult_submitted = False

# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero-banner">
    <h1>🤖 The AI Meet Up</h1>
    <div class="subtitle">Presented by <strong>ENTREMOTIVATOR</strong></div>
    <div class="subtitle">Expert Talks &nbsp;·&nbsp; Live Demos &nbsp;·&nbsp; Networking Mixer &nbsp;·&nbsp; Hands-On Workshops &nbsp;·&nbsp; AI Keynote</div>
    <div class="event-pill">📅 {TODAY_DATE} &nbsp;|&nbsp; {TODAY_TIME}</div>
    <div class="event-meta">📍 {TODAY_LOCATION} &nbsp;|&nbsp; FREE EVENT</div>
    <div class="event-meta">🎤 Hosted by {TODAY_HOST}</div>
    <div class="event-meta" style="margin-top:0.5rem;">
        📧 {ADMIN_EMAIL} &nbsp;|&nbsp; 📞 {PHONE}
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="pulse-banner">
    ⚡ HAPPENING TODAY — February 20, 2026 &nbsp;|&nbsp; 5:00 – 8:00 PM &nbsp;|&nbsp; Ellenwood, GA ⚡
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Today's Event", "Feb 20, 2026", "LIVE TODAY")
c2.metric("Time", "5:00 – 8:00 PM", "Ellenwood, GA")
c3.metric("Format", "FREE Event", "In-Person")
c4.metric("Next Event", "Mar 27, 2026", "Register Now")

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎨 Flyer & About",
    "🗓 Today's Agenda",
    "🗳 Vote Your City",
    "💼 Free Consultation",
    "🎟 Sign Up — Next Event",
])

# ══════════════════════════════════════════════
# TAB 1 — FLYER & ABOUT
# ══════════════════════════════════════════════
with tab1:
    st.markdown("<div class='section-hdr'><h2>🎨 Official Event Flyer</h2></div>", unsafe_allow_html=True)
    col_img, col_info = st.columns([1, 1])
    with col_img:
        st.image(FLYER_URL, caption="The AI Meet Up — Official Flyer", use_container_width=True)
    with col_info:
        st.markdown("""
<div class="gold-card">
    <h3>🌍 About The Event</h3>
    <p>The AI Meet Up is a high-impact gathering for forward-thinking entrepreneurs,
    business leaders, developers, marketers, and creators serious about implementing
    AI into real-world business systems.</p>
    <p><strong style="color:#ffd700;">This is not theory. This is applied AI.</strong></p>
    <p>Expect live demonstrations, automation frameworks, and actionable strategies
    you can deploy immediately.</p>
</div>
<div class="gold-card">
    <h3>🔥 What's Happening Today</h3>
    <ul>
        <li>🎤 Expert Talks from AI leaders</li>
        <li>🖥 Live AI Demonstrations</li>
        <li>🛠 Hands-On Workshops</li>
        <li>🥂 Networking Mixer</li>
        <li>💡 Innovation Showcase</li>
        <li>🤖 AI Keynote Presentation</li>
    </ul>
</div>
<div class="gold-card">
    <h3>🎯 Who Should Attend</h3>
    <ul>
        <li>Entrepreneurs ready to scale with AI</li>
        <li>Business owners seeking automation</li>
        <li>Developers building AI tools</li>
        <li>Content creators using AI workflows</li>
        <li>Agency owners &amp; consultants</li>
    </ul>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div class='section-hdr'><h2>✨ Event Highlights</h2></div>", unsafe_allow_html=True)
    fcols = st.columns(6)
    features = [
        ("🎤","Expert Talks","Industry leaders sharing real-world AI insights"),
        ("🥂","Networking","Connect with builders & entrepreneurs"),
        ("🖥","Live Demos","See AI systems built in real time"),
        ("🛠","Workshops","Hands-on sessions you can apply immediately"),
        ("💡","Innovation","Showcase of cutting-edge AI tools"),
        ("🤖","AI Keynote","Vision for AI in business 2026 & beyond"),
    ]
    for col, (icon, title, desc) in zip(fcols, features):
        with col:
            st.markdown(f"""
<div class="feature-box">
    <div class="icon">{icon}</div>
    <h3>{title}</h3>
    <p>{desc}</p>
</div>""", unsafe_allow_html=True)

    st.markdown("<div class='section-hdr'><h2>❓ Frequently Asked Questions</h2></div>", unsafe_allow_html=True)
    with st.expander("Do I need technical experience?"):
        st.write("No. This event is designed for both technical and non-technical professionals.")
    with st.expander("Will there be live demonstrations?"):
        st.write("Yes — real AI systems will be built and shown live on stage.")
    with st.expander("Is networking included?"):
        st.write("Absolutely. Strategic networking is a major focus of The AI Meet Up.")
    with st.expander("Is this event really free?"):
        st.write("Yes! The AI Meet Up is a FREE event. Simply register to secure your spot.")
    with st.expander("Where is the event held?"):
        st.write(f"Ellenwood, GA. Contact {ADMIN_EMAIL} for exact venue details.")

# ══════════════════════════════════════════════
# TAB 2 — TODAY'S AGENDA
# ══════════════════════════════════════════════
with tab2:
    st.markdown("<div class='section-hdr'><h2>🗓 Today's Live Agenda — February 20, 2026</h2></div>",
                unsafe_allow_html=True)
    st.markdown(f"""
<div class="gold-card">
    <h3>📅 {TODAY_DATE} &nbsp;|&nbsp; {TODAY_TIME} &nbsp;|&nbsp; 📍 {TODAY_LOCATION}</h3>
    <p>🎤 Hosted by <strong style="color:#ffd700;">{TODAY_HOST}</strong> &nbsp;|&nbsp; EntreMotivator.com</p>
</div>
""", unsafe_allow_html=True)

    agenda = [
        ("5:00 – 5:30 PM", "Arrival & Registration",
         "Check in, grab your badge, and connect with fellow attendees"),
        ("5:30 – 6:00 PM", "Networking Mixer",
         "Strategic networking — meet entrepreneurs, builders & AI enthusiasts"),
        ("6:00 – 6:30 PM", "AI Keynote",
         "The AI shift: how artificial intelligence is reshaping business in 2026"),
        ("6:30 – 7:00 PM", "Expert Talks",
         "Industry leaders share real-world AI implementation strategies"),
        ("7:00 – 7:30 PM", "Live Demonstrations",
         "Watch AI-powered systems, funnels, and automation built live on stage"),
        ("7:30 – 7:45 PM", "Hands-On Workshop",
         "Interactive session — build your own AI workflow in real time"),
        ("7:45 – 8:00 PM", "Innovation Showcase",
         "Attendees and sponsors demo cutting-edge AI tools & solutions"),
    ]
    for time_slot, title, desc in agenda:
        st.markdown(f"""
<div class="agenda-row">
    <div class="agenda-time">{time_slot}</div>
    <div class="agenda-content">
        <div class="agenda-title">{title}</div>
        <div class="agenda-desc">{desc}</div>
    </div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-hdr'><h2>⏳ Time Until Today's Event</h2></div>",
                unsafe_allow_html=True)
    event_today = datetime(2026, 2, 20, 17, 0, 0)
    now = datetime.now()
    delta = event_today - now
    if delta.total_seconds() > 0:
        h = delta.seconds // 3600
        m = (delta.seconds % 3600) // 60
        s = delta.seconds % 60
        t1, t2, t3, t4 = st.columns(4)
        t1.metric("Days",    str(delta.days),  "until event")
        t2.metric("Hours",   str(h),           "hours")
        t3.metric("Minutes", str(m),           "minutes")
        t4.metric("Seconds", str(s),           "seconds")
        st.info("🔔 The event starts at 5:00 PM today — Ellenwood, GA!")
    else:
        st.success("🎉 The AI Meet Up is LIVE right now! Welcome — enjoy the event!")

# ══════════════════════════════════════════════
# TAB 3 — VOTE YOUR CITY
# ══════════════════════════════════════════════
with tab3:
    st.markdown("<div class='section-hdr'><h2>🗳 Vote — Where Should The AI Meet Up Tour Next?</h2></div>",
                unsafe_allow_html=True)
    st.markdown("""
<div class="gold-card">
    <h3>🌎 Help Us Plan The AI Meet Up City Tour!</h3>
    <p>The AI Meet Up is going on tour! Cast your vote for the city you want us to visit next.
    Top cities will be added to the 2026 tour schedule.</p>
</div>
""", unsafe_allow_html=True)

    col_vote, col_results = st.columns([1, 1])
    with col_vote:
        st.markdown("### 🗺 Cast Your Vote")
        with st.form("city_vote_form"):
            voter_name  = st.text_input("Your Name",  placeholder="Enter your name")
            voter_email = st.text_input("Your Email", placeholder="your@email.com")
            city_choice = st.selectbox("Which city should we visit next?",
                                       list(st.session_state.city_votes.keys()))
            why_vote    = st.text_area("Why this city? (Optional)",
                placeholder="Tell us why your city deserves The AI Meet Up...", height=90)
            also_attend = st.checkbox("I would attend if The AI Meet Up comes to this city!")
            submit_vote = st.form_submit_button("🗳 Cast My Vote!", use_container_width=True)

        if submit_vote:
            if not voter_name or not voter_email:
                st.error("Please enter your name and email to vote.")
            elif "@" not in voter_email:
                st.error("Please enter a valid email address.")
            elif st.session_state.voted_city:
                st.warning(f"You already voted for **{st.session_state.voted_city}**!")
            else:
                st.session_state.city_votes[city_choice] += 1
                st.session_state.voted_city = city_choice
                st.success(f"✅ Vote cast for **{city_choice}**! Thank you, {voter_name}!")
                st.balloons()

    with col_results:
        st.markdown("### 📊 Live Vote Results")
        votes_df = pd.DataFrame(
            list(st.session_state.city_votes.items()),
            columns=["City", "Votes"]
        ).sort_values("Votes", ascending=False).reset_index(drop=True)
        total = votes_df["Votes"].sum()
        st.markdown(f"**Total Votes Cast: {total}**")
        for _, row in votes_df.iterrows():
            city  = row["City"]
            votes = row["Votes"]
            pct   = (votes / total * 100) if total > 0 else 0
            lead  = votes == votes_df["Votes"].max() and votes > 0
            badge = " 🏆" if lead else ""
            bar   = "linear-gradient(90deg,#ffd700,#ffaa00)" if lead else "#555"
            st.markdown(f"""
<div class="vote-city">
    <span style="font-size:1.1rem;">📍</span>
    <div style="flex:1">
        <strong style="color:{'#ffd700' if lead else '#ffffff'}">{city}{badge}</strong>
        <div style="background:#2a2a2a;border-radius:10px;height:7px;margin-top:4px;">
            <div style="background:{bar};width:{pct}%;height:7px;border-radius:10px;"></div>
        </div>
    </div>
    <span style="color:#ffd700;font-weight:700;min-width:70px;text-align:right">
        {votes} vote{'s' if votes!=1 else ''} ({pct:.0f}%)
    </span>
</div>""", unsafe_allow_html=True)

    st.markdown("<div class='section-hdr'><h2>📋 City Tour Questionnaire</h2></div>",
                unsafe_allow_html=True)
    with st.form("tour_questionnaire"):
        st.markdown("**Help us plan the perfect event for your city!**")
        q1, q2 = st.columns(2)
        with q1:
            q_city  = st.text_input("Your City & State", placeholder="e.g. Houston, TX")
            q_size  = st.selectbox("Ideal event size?",
                ["Select...", "50–100 attendees", "100–250 attendees",
                 "250–500 attendees", "500+ attendees"])
            q_venue = st.selectbox("Preferred venue type?",
                ["Select...", "Hotel Conference Room", "Co-working Space",
                 "University Auditorium", "Convention Center", "Other"])
        with q2:
            q_day    = st.selectbox("Best day of week?",
                ["Select...", "Friday Evening", "Saturday", "Sunday", "Weekday Evening"])
            q_topics = st.multiselect("Top AI topics you want covered?",
                ["AI Automation", "ChatGPT & LLMs", "AI for Marketing", "AI for Sales",
                 "Machine Learning", "AI Agents", "Local AI Models",
                 "AI Content Creation", "AI Business Strategy"])
            q_sponsor = st.selectbox("Would you or your company sponsor?",
                ["Select...", "Yes, definitely!", "Maybe, tell me more", "No, just attending"])
        q_comments = st.text_area("Any other suggestions?", height=70)
        sub_q = st.form_submit_button("📤 Submit Questionnaire", use_container_width=True)
    if sub_q:
        if q_city and q_size != "Select..." and q_day != "Select...":
            st.success(f"🎉 Thank you! Preferences recorded for **{q_city}**.")
        else:
            st.error("Please fill in your city, event size, and preferred day.")

# ══════════════════════════════════════════════
# TAB 4 — FREE $100 CONSULTATION
# ══════════════════════════════════════════════
with tab4:
    st.markdown("""
<div class="consult-banner">
    <h2>💼 FREE AI Consultation</h2>
    <div class="price">$100 Value — Yours FREE</div>
    <div class="tagline">Book your complimentary 1-on-1 AI strategy session.<br>
    Our team will reach out within <strong style="color:#ffd700;">24 hours</strong> to confirm.</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="gold-card">
    <h3>🎁 Your FREE $100 Consultation Includes:</h3>
    <ul style="font-size:1.05rem;">
        <li>✅ 30-Minute 1-on-1 AI Strategy Session ($60 value)</li>
        <li>✅ Personalized AI Readiness Assessment ($25 value)</li>
        <li>✅ Custom Quick-Win Recommendations ($15 value)</li>
        <li>✅ Follow-Up Action Plan via Email</li>
    </ul>
    <p style="color:#ffd700;font-weight:700;font-size:1.05rem;">
        ⚡ TOTAL VALUE: $100 — COMPLETELY FREE. Our team reaches out within 24 hours!
    </p>
</div>
""", unsafe_allow_html=True)

    if st.session_state.consult_submitted:
        st.success("🎉 Request received! Our team will reach out within 24 hours. Check your email for confirmation.")
        st.markdown("""
<div class="gold-card" style="text-align:center;">
    <h3>✅ What Happens Next?</h3>
    <p>1️⃣ Our team reviews your submission</p>
    <p>2️⃣ We reach out within <strong style="color:#ffd700;">24 hours</strong></p>
    <p>3️⃣ We schedule your FREE 30-minute AI strategy call</p>
    <p>4️⃣ You walk away with a clear AI action plan</p>
</div>
""", unsafe_allow_html=True)
    else:
        with st.form("consultation_form", clear_on_submit=False):
            st.markdown("### 👤 Contact Information")
            ci1, ci2 = st.columns(2)
            with ci1:
                c_name     = st.text_input("Full Name *",          placeholder="Your full name")
                c_email    = st.text_input("Business Email *",     placeholder="you@company.com")
                c_phone    = st.text_input("Phone Number *",       placeholder="678-555-0000")
            with ci2:
                c_position = st.text_input("Job Title *",          placeholder="CEO, Founder, Manager...")
                c_company  = st.text_input("Company / Business *", placeholder="Your company name")
                c_industry = st.selectbox("Industry *",
                    ["Select industry", "Technology", "E-commerce", "Healthcare",
                     "Finance", "Real Estate", "Marketing / Agency", "Education",
                     "Manufacturing", "Retail", "Non-Profit", "Other"])

            st.markdown("---")
            st.markdown("### 🏢 Business Details")
            cd1, cd2 = st.columns(2)
            with cd1:
                c_size    = st.selectbox("Company Size *",
                    ["Select size", "Solo / Freelancer", "2–10", "11–50", "51–200", "200+"])
                c_project = st.selectbox("Primary Interest *",
                    ["Select...", "AI Automation & Workflows", "AI Chatbots & Assistants",
                     "Content Generation with AI", "AI Strategy & Roadmap",
                     "Process Automation", "Data Analytics & ML",
                     "AI for Marketing & Sales", "Not Sure — Need Guidance"])
            with cd2:
                c_budget   = st.selectbox("Monthly Budget *",
                    ["Select budget", "Under $500/mo", "$500–$1,500/mo",
                     "$1,500–$5,000/mo", "$5,000–$10,000/mo", "$10,000+/mo"])
                c_timeline = st.selectbox("When to start? *",
                    ["Select timeline", "Immediately / ASAP", "Within 2 weeks",
                     "Within 1 month", "1–3 months", "Just exploring"])

            st.markdown("---")
            st.markdown("### 📋 Tell Us About Your Goals")
            c_challenges = st.text_area("Biggest business challenges right now? *",
                placeholder="e.g. Too much manual work, need better customer follow-up...", height=90)
            c_outcomes   = st.text_area("What outcomes do you want from AI? *",
                placeholder="e.g. Save 10 hrs/week, automate lead follow-up...", height=90)
            c_heard      = st.selectbox("How did you hear about us?",
                ["Select...", "The AI Meet Up Event", "Social Media", "Referral",
                 "Google Search", "Entremotivator.com", "Other"])
            c_consent    = st.checkbox(
                "✅ I agree to receive communications from The ATM Agency / Entremotivator team",
                value=True)

            st.markdown("---")
            consult_submit = st.form_submit_button(
                "🎁 Claim My FREE $100 Consultation — Team Reaches Out in 24 Hours!",
                use_container_width=True, type="primary")

        if consult_submit:
            selects_ok = all(
                s not in ["Select industry","Select size","Select...","Select budget","Select timeline"]
                for s in [c_industry, c_size, c_project, c_budget, c_timeline]
            )
            email_ok = "@" in c_email and "." in c_email.split("@")[-1]

            if not all([c_name, c_email, c_phone, c_position, c_company]):
                st.error("⚠️ Please fill in all required fields marked with *")
            elif not selects_ok:
                st.error("⚠️ Please make a selection for all dropdown fields.")
            elif not email_ok:
                st.error("⚠️ Please enter a valid email address.")
            elif not c_challenges or not c_outcomes:
                st.error("⚠️ Please describe your challenges and desired outcomes.")
            elif not c_consent:
                st.error("⚠️ Please agree to receive communications.")
            else:
                form_data = {
                    "name": c_name, "email": c_email, "phone": c_phone,
                    "position": c_position, "company": c_company, "industry": c_industry,
                    "company_size": c_size, "project_type": c_project,
                    "budget_range": c_budget, "timeline": c_timeline,
                    "current_challenges": c_challenges, "desired_outcomes": c_outcomes,
                    "heard_from": c_heard,
                    "submission_date": datetime.now().isoformat(),
                    "consultation_type": "FREE $100 Consultation — AI Meet Up",
                    "note": "Team to reach out within 24 hours"
                }

                # 1. Send to n8n webhook
                send_to_n8n(form_data)

                # 2. Confirmation email to the lead
                sent_confirm = send_consult_confirmation(c_email, c_name, c_company)

                # 3. Admin alert email
                sent_admin = send_consult_admin_alert(form_data)

                st.session_state.consult_submitted = True

                if EMAIL_ENABLED:
                    if sent_confirm:
                        st.toast(f"✅ Confirmation email sent to {c_email}", icon="📧")
                    if sent_admin:
                        st.toast("✅ Admin notification sent", icon="🔔")

                st.rerun()

# ══════════════════════════════════════════════
# TAB 5 — SIGN UP FOR NEXT EVENT  (LAST TAB)
# ══════════════════════════════════════════════
with tab5:
    st.markdown("<div class='section-hdr'><h2>🎟 Sign Up for The Next AI Meet Up — March 27, 2026</h2></div>",
                unsafe_allow_html=True)

    next_event = datetime(2026, 3, 27, 17, 0, 0)
    delta_next = next_event - datetime.now()
    days_left  = delta_next.days if delta_next.total_seconds() > 0 else 0

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown(f"""
<div class="consult-banner">
    <h2>🤖 The AI Meet Up</h2>
    <div style="color:#ffffff;font-size:1.3rem;margin:0.6rem 0;">
        <strong style="color:#ffd700;">March 27, 2026</strong>
        &nbsp;|&nbsp; {NEXT_TIME}
        &nbsp;|&nbsp; 📍 {NEXT_LOCATION}
    </div>
    <div class="price">FREE EVENT</div>
    <div class="tagline" style="font-size:1.15rem;margin:0.8rem 0 1.5rem 0;">
        Spots are limited — register now on the official event page!
    </div>
    <a href="{EVENT_URL}" target="_blank" class="cta-btn"
       style="font-size:1.25rem;padding:1.1rem 3.5rem;letter-spacing:2px;">
        🎟 SIGN UP NOW
    </a>
    <div style="margin-top:1.2rem;color:#aaaaaa;font-size:0.95rem;">
        👉 <a href="{EVENT_URL}" target="_blank"
              style="color:#ffd700;text-decoration:underline;">
            entremotivator.com/events/the-ai-meet-up/
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

        st.markdown(f"""
<div class="gold-card">
    <h3>🔥 What's at The Next AI Meet Up?</h3>
    <ul style="font-size:1.05rem;line-height:2rem;">
        <li>🎤 Expert Talks from AI leaders</li>
        <li>🖥 Live AI Demonstrations</li>
        <li>🛠 Hands-On Workshops</li>
        <li>🥂 Networking Mixer</li>
        <li>💡 Innovation Showcase</li>
        <li>🤖 AI Keynote Presentation</li>
        <li>🎁 Community &amp; Resources Access</li>
    </ul>
</div>
""", unsafe_allow_html=True)

        st.markdown(f"""
<div style="text-align:center;padding:1.5rem 0;">
    <p style="color:#cccccc;font-size:1.05rem;margin-bottom:1rem;">
        Click below to register on the official event page:
    </p>
    <a href="{EVENT_URL}" target="_blank" class="cta-btn"
       style="font-size:1.1rem;padding:0.9rem 3rem;">
        🌐 Register at EntreMotivator.com
    </a>
    <p style="color:#888;font-size:0.9rem;margin-top:1rem;">
        📧 {ADMIN_EMAIL} &nbsp;|&nbsp; 📞 {PHONE}
    </p>
</div>
""", unsafe_allow_html=True)

    with col_right:
        st.markdown(f"""
<div class="gold-card" style="text-align:center;">
    <h3>📅 Event Details</h3>
    <p><strong style="color:#ffd700;">Date:</strong> March 27, 2026</p>
    <p><strong style="color:#ffd700;">Time:</strong> 5:00 PM – 8:00 PM</p>
    <p><strong style="color:#ffd700;">Location:</strong> Ellenwood, GA</p>
    <p><strong style="color:#ffd700;">Cost:</strong> 🆓 FREE</p>
    <p><strong style="color:#ffd700;">Host:</strong> Donmenico Hudson</p>
    <p><strong style="color:#ffd700;">Presented by:</strong> EntreMotivator</p>
</div>
""", unsafe_allow_html=True)

        if days_left > 0:
            st.markdown(f"""
<div class="gold-card" style="text-align:center;">
    <h3>⏳ Countdown</h3>
    <p style="font-size:3rem;font-weight:900;color:#ffd700;margin:0;">{days_left}</p>
    <p style="color:#cccccc;margin:0;">days until the next AI Meet Up!</p>
</div>
""", unsafe_allow_html=True)

        st.markdown(f"""
<div class="gold-card" style="text-align:center;">
    <h3>📞 Contact</h3>
    <p>📧 <a href="mailto:{ADMIN_EMAIL}" style="color:#ffd700;">{ADMIN_EMAIL}</a></p>
    <p>📞 <a href="tel:{PHONE}" style="color:#ffd700;">{PHONE}</a></p>
    <br>
    <a href="{EVENT_URL}" target="_blank" class="cta-btn"
       style="font-size:0.95rem;padding:0.7rem 1.8rem;">
        🎟 Register Now
    </a>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown(f"""
<div style="background:linear-gradient(135deg,#0d0d0d,#1a1200);
            border:2px solid #ffd700;border-radius:16px;
            padding:2.5rem;text-align:center;margin-top:2rem;
            box-shadow:0 0 40px rgba(255,215,0,0.2);">
    <h2 style="color:#ffd700;margin:0 0 0.5rem 0;">🤖 The AI Meet Up</h2>
    <p style="color:#cccccc;font-size:1.05rem;margin:0.3rem 0;">
        TODAY: {TODAY_DATE} &nbsp;|&nbsp; {TODAY_TIME} &nbsp;|&nbsp; {TODAY_LOCATION} &nbsp;|&nbsp; FREE EVENT
    </p>
    <p style="color:#aaaaaa;margin:0.5rem 0;">
        📧 <a href="mailto:{ADMIN_EMAIL}" style="color:#ffd700;">{ADMIN_EMAIL}</a>
        &nbsp;|&nbsp;
        📞 <a href="tel:{PHONE}" style="color:#ffd700;">{PHONE}</a>
    </p>
    <p style="margin-top:1rem;">
        <a href="{EVENT_URL}" target="_blank" class="cta-btn" style="font-size:1rem;padding:0.7rem 2rem;">
            🌐 Register for Next Event — March 27, 2026
        </a>
    </p>
    <p style="color:#555;font-size:0.85rem;margin-top:1.5rem;">
        Presented by Entremotivator.com &nbsp;|&nbsp; Hosted by Donmenico Hudson
    </p>
</div>
""", unsafe_allow_html=True)
