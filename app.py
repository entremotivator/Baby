import streamlit as st
from streamlit_drawable_canvas import st_canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    HRFlowable, Table, TableStyle, KeepTogether
)
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.colors import HexColor, white, black
import tempfile, os, re, io
from datetime import datetime
from PIL import Image
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from contract_templates import (
    build_sales_rep_text,
    build_app_dev_text,
    build_ai_startup_text,
    build_ai_agent_text,
    build_website_text,
    build_funnel_text,
)

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ATM Agency – Contract Portal",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Email Credentials ─────────────────────────────────────────────────────────
try:
    EMAIL_ADDRESS  = st.secrets["email"]["sender_email"]
    EMAIL_PASSWORD = st.secrets["email"]["password"]
    SMTP_SERVER    = st.secrets["email"]["smtp_server"]
    PORT           = int(st.secrets["email"]["port"])
    ADMIN_EMAIL    = "Entremotivator@gmail.com"
except Exception:
    EMAIL_ADDRESS = None

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main { background: #f0f4f8; }

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #050d1a 0%, #0a1f4e 45%, #0055b3 100%);
    border-radius: 1.25rem;
    padding: 3.5rem 2rem 3rem;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 12px 40px rgba(0,85,179,0.35);
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute; top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(ellipse at center, rgba(0,150,255,0.1) 0%, transparent 70%);
    pointer-events: none;
}
.hero h1 { color: #fff !important; font-size: 2.8rem !important; font-weight: 800 !important;
           margin: 0 0 .5rem !important; letter-spacing: -0.5px; }
.hero .sub { color: #7ab8f5; font-size: 1.05rem; margin: 0; }
.hero .tagline { color: #a8d4ff; font-size: 0.85rem; margin-top: .6rem;
                 letter-spacing: 1.5px; text-transform: uppercase; }
.hero .badge-row { display:flex; justify-content:center; gap:.75rem; margin-top:1.2rem; flex-wrap:wrap; }
.hero .badge { background: rgba(255,255,255,0.12); border:1px solid rgba(255,255,255,0.2);
               color:#e0f0ff; font-size:.78rem; font-weight:600; padding:.3rem .9rem;
               border-radius:2rem; letter-spacing:.5px; }

/* ── Step headers ── */
.step-row { display:flex; align-items:center; margin: 2rem 0 1rem; gap: .75rem; }
.step-num {
    width: 2.4rem; height: 2.4rem; border-radius: 50%;
    background: linear-gradient(135deg,#0066cc,#003d7a);
    color: white; font-weight: 800; font-size: 1rem;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; box-shadow: 0 4px 12px rgba(0,102,204,.4);
}
.step-title { font-size: 1.4rem; font-weight: 700; color: #0a1628; margin: 0; }

/* ── Contract cards ── */
.ccard {
    background: white; border: 2px solid #dde4ef;
    border-radius: 1rem; padding: 1.5rem 1.3rem 1.1rem;
    transition: all .2s; cursor: pointer;
    box-shadow: 0 2px 10px rgba(0,0,0,.06);
    min-height: 180px;
}
.ccard:hover { border-color: #0066cc; box-shadow: 0 8px 24px rgba(0,102,204,.2); transform: translateY(-3px); }
.ccard.active { border-color: #0066cc; background: linear-gradient(135deg,#eff6ff,#f0f9ff);
                box-shadow: 0 8px 24px rgba(0,102,204,.22); }
.ccard .icon { font-size: 2.4rem; margin-bottom: .6rem; }
.ccard .ctitle { font-weight: 700; font-size: .96rem; color: #0a1628; margin-bottom: .35rem; line-height: 1.3; }
.ccard .cdesc { font-size: .8rem; color: #64748b; line-height: 1.45; }
.ccard .cprice { font-size: .83rem; font-weight: 700; color: #0066cc; margin-top: .6rem;
                 background:#eff6ff; display:inline-block; padding:.2rem .7rem;
                 border-radius:1rem; border:1px solid #bfdbfe; }

/* ── Info boxes ── */
.box { padding: 1rem 1.25rem; border-radius: .7rem; margin: .75rem 0; font-size: .92rem; }
.box-info    { background:#eff6ff; border-left:4px solid #0066cc; color:#1e3a5f; }
.box-warn    { background:#fffbeb; border-left:4px solid #f59e0b; color:#78350f; }
.box-success { background:#f0fdf4; border-left:4px solid #22c55e; color:#14532d; }
.box-error   { background:#fef2f2; border-left:4px solid #ef4444; color:#7f1d1d; }

/* ── Agreement text ── */
.agr-text {
    background: #fff; border: 1px solid #dde4ef; border-radius: .7rem;
    padding: 2rem 2.25rem; font-size: .875rem; line-height: 1.9;
    max-height: 550px; overflow-y: auto; font-family: 'Georgia', serif;
    color: #1a1a2e; white-space: pre-wrap;
    box-shadow: inset 0 2px 8px rgba(0,0,0,.04);
}

/* ── Buttons ── */
.stButton>button {
    width: 100%; font-weight: 600; padding: .75rem 1rem;
    border-radius: .65rem; border: none; transition: all .25s;
    font-size: .95rem; letter-spacing: .01em;
}
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg,#0066cc,#003d7a);
    color: white;
}
div[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg,#0052a3,#002d5c);
    box-shadow: 0 6px 20px rgba(0,102,204,.45);
    transform: translateY(-1px);
}

/* ── Signature panel ── */
.sig-wrap { border: 2px dashed #0066cc; border-radius: .8rem; padding: .6rem; background: white; }
.sig-info { background: #f8fafc; border-radius: .7rem; padding: 1.3rem; border: 1px solid #e2e8f0; }
.sig-info p { margin: .35rem 0; font-size: .88rem; color: #334155; }
.sig-info strong { color: #0a1628; }

/* ── Section divider ── */
.sdiv { border: none; border-top: 2px solid #dde4ef; margin: 2.5rem 0; }

/* ── Footer ── */
.footer { text-align:center; color:#94a3b8; padding:2.5rem 0 1rem; font-size:.83rem; }
.footer strong { color:#64748b; }

/* ── Field labels ── */
label { font-weight: 600 !important; color: #334155 !important; font-size: .88rem !important; }

/* ── Expander ── */
details > summary { font-weight: 600; cursor: pointer; color: #0066cc; font-size: .95rem; }

/* ── Selected contract banner ── */
.ct-banner {
    display:flex; align-items:center; gap:.75rem; margin:.5rem 0 1.5rem;
    background: linear-gradient(135deg,#eff6ff,#f0f9ff);
    border:1px solid #bfdbfe; border-radius:.8rem; padding:.9rem 1.2rem;
}
.ct-banner .ct-icon { font-size:1.6rem; }
.ct-banner .ct-name { font-weight:700; color:#0055b3; font-size:1rem; }
.ct-banner .ct-price { background:#0066cc; color:white; font-size:.78rem; font-weight:700;
                        padding:.25rem .75rem; border-radius:1rem; margin-left:.5rem; }
</style>
""", unsafe_allow_html=True)

# ─── Session State ─────────────────────────────────────────────────────────────
DEFAULTS = {
    "contract_type":      None,
    "agreement_accepted": False,
    "client_name":        "",
    "client_email":       "",
    "client_business":    "",
    "client_address":     "",
    "client_phone":       "",
    "selected_package":   "",
    "project_fee":        "",
    "start_date":         "",
    "state_law":          "Florida",
    "extra_notes":        "",
    "pdf_ready":          False,
    "pdf_bytes":          None,
    "pdf_filename":       "",
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── Contract Registry ─────────────────────────────────────────────────────────
CONTRACTS = {
    "sales_rep": {
        "label":    "Independent AI Business Owner & Sales Rep Agreement",
        "icon":     "🤝",
        "color":    "#0066cc",
        "price":    "Commission-Based",
        "desc":     "For independent sales reps marketing ATM Agency's AI SaaS products. Covers commissions, bonuses, non-compete, and termination.",
        "fields":   ["name","email","phone","business"],
        "packages": [],
    },
    "app_dev": {
        "label":    "App Development & Publishing Agreement",
        "icon":     "📱",
        "color":    "#7c3aed",
        "price":    "From $2,997",
        "desc":     "For clients commissioning custom Web, Mobile, or AI application development and App Store publishing.",
        "fields":   ["name","email","phone","business","address","package","project_fee","start_date","state_law"],
        "packages": [
            "Web App Development – Starting at $2,997",
            "Mobile App Development & Publishing – Starting at $4,997+",
            "AI App Development – Starting at $5,997+",
            "Marketplace / Community Platform – Starting at $6,997+",
            "Full-Stack Web + Mobile Bundle – Starting at $8,997+",
        ],
    },
    "ai_startup": {
        "label":    "AI Agency Startup Program Agreement",
        "icon":     "🚀",
        "color":    "#059669",
        "price":    "From $1,997",
        "desc":     "For clients enrolling in the AI Agency Startup Program — Starter, Manager, or Partnership plan.",
        "fields":   ["name","email","phone","business","address","package","project_fee","state_law"],
        "packages": [
            "Starter Plan – $1,997",
            "Manager Plan – $4,997",
            "Partnership Plan – $9,997",
        ],
    },
    "ai_agent": {
        "label":    "AI Agent Building & Deployment Agreement",
        "icon":     "🤖",
        "color":    "#dc2626",
        "price":    "From $1,497",
        "desc":     "For clients commissioning custom AI agents — chatbots, voice agents, automation bots, call centers, and multi-agent systems.",
        "fields":   ["name","email","phone","business","address","package","project_fee","start_date","state_law"],
        "packages": [
            "Single AI Agent (Chatbot / Voice) – Starting at $1,497",
            "Multi-Agent System (Up to 5 Agents) – Starting at $3,997",
            "Enterprise AI Agent Fleet (10+ Agents) – Starting at $7,997+",
            "AI Call Center Setup (Voice Agents) – Starting at $5,497+",
            "Full AI Automation Suite – Starting at $9,997+",
        ],
    },
    "website": {
        "label":    "Website Design & Development Agreement",
        "icon":     "🌐",
        "color":    "#0891b2",
        "price":    "From $1,297",
        "desc":     "For clients commissioning professional website design — brochure sites, business sites, e-commerce, or enterprise portals.",
        "fields":   ["name","email","phone","business","address","package","project_fee","start_date","state_law"],
        "packages": [
            "Starter Business Website (Up to 5 Pages) – Starting at $1,297",
            "Professional Business Website (Up to 10 Pages) – Starting at $2,497",
            "E-Commerce Website – Starting at $3,997+",
            "Corporate / Enterprise Website – Starting at $5,997+",
            "Website Redesign & Optimization – Starting at $1,997+",
        ],
    },
    "funnel": {
        "label":    "Sales Funnel Design & Build Agreement",
        "icon":     "🎯",
        "color":    "#d97706",
        "price":    "From $1,497",
        "desc":     "For clients commissioning high-converting sales funnels — lead gen, product sales, high-ticket, or complete marketing ecosystems.",
        "fields":   ["name","email","phone","business","address","package","project_fee","start_date","state_law"],
        "packages": [
            "Lead Generation Funnel – Starting at $1,497",
            "Product / Service Sales Funnel – Starting at $2,997",
            "Full Funnel System (with Upsells & Downsells) – Starting at $4,997",
            "High-Ticket Application / Booking Funnel – Starting at $3,997",
            "Complete Marketing Ecosystem – Starting at $7,997+",
        ],
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# PDF GENERATOR
# ══════════════════════════════════════════════════════════════════════════════
def generate_pdf(contract_text, contract_label, client_name, client_email,
                 client_business, client_phone, sig_image_data):
    tmp_dir  = tempfile.gettempdir()
    pdf_path = os.path.join(tmp_dir, "atm_contract.pdf")
    sig_path = os.path.join(tmp_dir, "atm_signature.png")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=LETTER,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    BLUE   = HexColor("#0055b3")
    DARK   = HexColor("#0a1628")
    GRAY   = HexColor("#64748b")
    LGRAY  = HexColor("#e2e8f0")
    BGRAY  = HexColor("#f8fafc")
    WHITE  = white

    title_s = ParagraphStyle("T", fontSize=14, leading=20, alignment=TA_CENTER,
                              textColor=BLUE, spaceAfter=4, fontName="Helvetica-Bold")
    sub_s   = ParagraphStyle("S", fontSize=9,  leading=13, alignment=TA_CENTER,
                              textColor=GRAY, spaceAfter=16)
    sec_s   = ParagraphStyle("H", fontSize=10.5, leading=15, alignment=TA_LEFT,
                              textColor=BLUE, spaceBefore=14, spaceAfter=5,
                              fontName="Helvetica-Bold")
    body_s  = ParagraphStyle("B", fontSize=9.5, leading=15, alignment=TA_JUSTIFY,
                              textColor=DARK, spaceAfter=3)
    mono_s  = ParagraphStyle("M", fontSize=8.5, leading=13, alignment=TA_LEFT,
                              textColor=DARK, fontName="Courier", spaceAfter=2)
    sig_s   = ParagraphStyle("SG", fontSize=9.5, leading=13, fontName="Helvetica-Bold",
                              textColor=DARK, spaceAfter=2)
    foot_s  = ParagraphStyle("F", fontSize=7.5, alignment=TA_CENTER, textColor=GRAY)
    indent_s = ParagraphStyle("I", fontSize=9.5, leading=15, alignment=TA_LEFT,
                               textColor=DARK, spaceAfter=3, leftIndent=18)

    elements = []

    # ── Header ──
    elements.append(Paragraph("ATM Agency, LLC", title_s))
    elements.append(Paragraph(
        "Artificial Intelligence Technology Marketing Agency  ·  AITMAgency.com", sub_s))
    elements.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=12))
    elements.append(Paragraph(contract_label.upper(), title_s))
    elements.append(Spacer(1, 0.15 * inch))

    # ── Body ──
    for line in contract_text.split("\n"):
        stripped = line.strip()
        if not stripped:
            elements.append(Spacer(1, 0.04 * inch))
            continue
        # Section headers (numbered like "1. SCOPE" or ALL CAPS headers)
        if re.match(r'^\d{1,2}\.\s+[A-Z]', stripped) or \
           re.match(r'^[A-Z]{2,}[\s&/]+[A-Z]', stripped):
            elements.append(Paragraph(stripped, sec_s))
        # Divider lines
        elif stripped.startswith("━"):
            elements.append(HRFlowable(width="100%", thickness=0.5,
                                        color=LGRAY, spaceAfter=4, spaceBefore=4))
        # Table-like rows (box drawing)
        elif "│" in stripped or "┌" in stripped or "├" in stripped or "└" in stripped:
            elements.append(Paragraph(stripped, mono_s))
        # Sub-numbered items like 1.1, 5.2
        elif re.match(r'^\d+\.\d+\s+[A-Z]', stripped):
            elements.append(Paragraph(stripped, indent_s))
        # Lettered items (a), (b)...
        elif re.match(r'^\([a-z]\)', stripped):
            elements.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;{stripped}", body_s))
        # Bullet points
        elif stripped.startswith("•"):
            elements.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;{stripped}", body_s))
        else:
            elements.append(Paragraph(stripped, body_s))

    # ── Signature Page ──
    elements.append(PageBreak())
    elements.append(Paragraph("ATM Agency, LLC", title_s))
    elements.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=16))
    elements.append(Paragraph("ELECTRONIC SIGNATURE PAGE", title_s))
    elements.append(Spacer(1, 0.25 * inch))

    current_dt = datetime.now().strftime("%B %d, %Y at %I:%M %p EST")

    info_data = [
        ["Full Name:",      client_name],
        ["Email Address:",  client_email],
        ["Business Name:",  client_business if client_business else "N/A"],
        ["Phone:",          client_phone    if client_phone    else "N/A"],
        ["Agreement:",      contract_label],
        ["Date Signed:",    current_dt],
    ]
    info_table = Table(info_data, colWidths=[1.7*inch, 4.7*inch])
    info_table.setStyle(TableStyle([
        ("FONTNAME",       (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME",       (1,0), (1,-1), "Helvetica"),
        ("FONTSIZE",       (0,0), (-1,-1), 9.5),
        ("LEADING",        (0,0), (-1,-1), 14),
        ("TEXTCOLOR",      (0,0), (0,-1), BLUE),
        ("TEXTCOLOR",      (1,0), (1,-1), DARK),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [BGRAY, WHITE]),
        ("TOPPADDING",     (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",  (0,0), (-1,-1), 6),
        ("LEFTPADDING",    (0,0), (-1,-1), 10),
        ("RIGHTPADDING",   (0,0), (-1,-1), 10),
        ("BOX",            (0,0), (-1,-1), 0.5, LGRAY),
        ("INNERGRID",      (0,0), (-1,-1), 0.25, LGRAY),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("Client / Representative Signature:", sec_s))
    elements.append(Spacer(1, 0.1 * inch))

    sig_img = Image.fromarray(sig_image_data.astype("uint8"))
    sig_img.save(sig_path)

    from reportlab.platypus import Image as RLImage
    elements.append(RLImage(sig_path, width=3.5 * inch, height=1 * inch))
    elements.append(HRFlowable(width="55%", thickness=1, color=LGRAY, spaceAfter=4))
    elements.append(Paragraph(f"Electronically signed by: {client_name}", sig_s))
    elements.append(Spacer(1, 0.4 * inch))

    elements.append(Paragraph("ATM Agency, LLC — Authorized Representative:", sec_s))
    elements.append(Spacer(1, 0.8 * inch))
    elements.append(HRFlowable(width="55%", thickness=1, color=LGRAY, spaceAfter=4))
    elements.append(Paragraph("Authorized Signature — ATM Agency, LLC", sig_s))

    elements.append(Spacer(1, 0.5 * inch))
    elements.append(HRFlowable(width="100%", thickness=1, color=BLUE, spaceAfter=8))
    elements.append(Paragraph(
        "This document was electronically signed via the ATM Agency Contract Portal. "
        "It constitutes a legally binding agreement between the parties named herein "
        "under the E-SIGN Act and applicable state law. "
        "Unauthorized reproduction or distribution is strictly prohibited.",
        foot_s
    ))

    doc.build(elements)

    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    try:
        os.remove(pdf_path)
        os.remove(sig_path)
    except Exception:
        pass
    return pdf_bytes


def send_email(to_addr, subject, body_text, pdf_bytes, pdf_filename):
    if not EMAIL_ADDRESS:
        return False
    try:
        msg = MIMEMultipart()
        msg["From"]    = EMAIL_ADDRESS
        msg["To"]      = to_addr
        msg["Subject"] = subject
        msg.attach(MIMEText(body_text, "plain"))
        part = MIMEBase("application", "octet-stream")
        part.set_payload(pdf_bytes)
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={pdf_filename}")
        msg.attach(part)
        server = smtplib.SMTP(SMTP_SERVER, PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Email error: {str(e)}")
        return False


def is_valid_email(email):
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))


# ══════════════════════════════════════════════════════════════════════════════
# UI
# ══════════════════════════════════════════════════════════════════════════════

# ── Hero ──
st.markdown("""
<div class="hero">
  <h1>📄 ATM Agency Contract Portal</h1>
  <p class="sub">Artificial Intelligence Technology Marketing Agency &nbsp;·&nbsp; AITMAgency.com</p>
  <p class="tagline">Secure · Professional · Legally Binding Electronic Agreements</p>
  <div class="badge-row">
    <span class="badge">🔒 E-SIGN Act Compliant</span>
    <span class="badge">📋 6 Contract Types</span>
    <span class="badge">✍️ Digital Signature</span>
    <span class="badge">📥 Instant PDF Download</span>
    <span class="badge">📧 Email Delivery</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Step 1 — Select Contract ──────────────────────────────────────────────────
st.markdown("""
<div class="step-row">
  <div class="step-num">1</div>
  <p class="step-title">Select Your Contract Type</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="box box-info">📋 Choose the agreement that matches your service. Each contract is fully customized with detailed terms, deliverables, and legal protections.</div>',
            unsafe_allow_html=True)

# Row 1: first 3 contracts
row1_keys = ["sales_rep", "app_dev", "ai_startup"]
row2_keys = ["ai_agent", "website", "funnel"]

for row_keys in [row1_keys, row2_keys]:
    cols = st.columns(3)
    for idx, key in enumerate(row_keys):
        meta   = CONTRACTS[key]
        active = "active" if st.session_state.contract_type == key else ""
        with cols[idx]:
            st.markdown(f"""
            <div class="ccard {active}">
              <div class="icon">{meta['icon']}</div>
              <div class="ctitle">{meta['label']}</div>
              <div class="cdesc">{meta['desc']}</div>
              <div class="cprice">{meta['price']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Select  {meta['icon']}", key=f"sel_{key}", use_container_width=True):  # noqa
                for k, v in DEFAULTS.items():
                    st.session_state[k] = v
                st.session_state.contract_type = key
                st.rerun()

if not st.session_state.contract_type:
    st.markdown('<div class="box box-warn">👆 Please select a contract type above to get started.</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="footer">
      <strong>ATM Agency, LLC</strong> · AITMAgency.com<br>
      Artificial Intelligence Technology Marketing Agency
    </div>
    """, unsafe_allow_html=True)
    st.stop()

ct      = st.session_state.contract_type
ct_meta = CONTRACTS[ct]

st.markdown(f"""
<div class="ct-banner">
  <span class="ct-icon">{ct_meta['icon']}</span>
  <span class="ct-name">{ct_meta['label']}</span>
  <span class="ct-price">{ct_meta['price']}</span>
</div>
""", unsafe_allow_html=True)

# ── Step 2 — Review Agreement ─────────────────────────────────────────────────
st.markdown('<hr class="sdiv">', unsafe_allow_html=True)
st.markdown("""
<div class="step-row">
  <div class="step-num">2</div>
  <p class="step-title">Review the Full Agreement</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="box box-info">📋 Please read all terms and conditions carefully. This is a legally binding agreement. Expand the section below to view the full contract text.</div>',
            unsafe_allow_html=True)

current_date = datetime.now().strftime("%B %d, %Y")

if ct == "sales_rep":
    preview = build_sales_rep_text("[Your Name]", "[Your Business]", "[Your Phone]", current_date)
elif ct == "app_dev":
    preview = build_app_dev_text("[Your Name]","[Your Business]","[Your Address]","[Your Phone]",
                                  "[Selected Package]","[Project Fee]","[Start Date]","Florida",current_date)
elif ct == "ai_startup":
    preview = build_ai_startup_text("[Your Name]","[Your Business]","[Your Address]","[Your Phone]",
                                     "[Selected Package]","[Program Fee]","Florida",current_date)
elif ct == "ai_agent":
    preview = build_ai_agent_text("[Your Name]","[Your Business]","[Your Address]","[Your Phone]",
                                   "[Selected Package]","[Project Fee]","[Start Date]","Florida",current_date)
elif ct == "website":
    preview = build_website_text("[Your Name]","[Your Business]","[Your Address]","[Your Phone]",
                                  "[Selected Package]","[Project Fee]","[Start Date]","Florida",current_date)
elif ct == "funnel":
    preview = build_funnel_text("[Your Name]","[Your Business]","[Your Address]","[Your Phone]",
                                 "[Selected Package]","[Project Fee]","[Start Date]","Florida",current_date)

with st.expander("📜 Click to View Full Agreement Text", expanded=False):
    st.markdown(f'<div class="agr-text">{preview}</div>', unsafe_allow_html=True)

agree_cb = st.checkbox(
    "✅ I have carefully read and fully understand all terms and conditions of this agreement, "
    "and I agree to be legally bound by them.",
    value=st.session_state.agreement_accepted
)
st.session_state.agreement_accepted = agree_cb

if not st.session_state.agreement_accepted:
    st.markdown('<div class="box box-warn">⚠️ You must read and accept the agreement terms before proceeding to sign.</div>',
                unsafe_allow_html=True)
    st.stop()

# ── Step 3 — Enter Information ────────────────────────────────────────────────
st.markdown('<hr class="sdiv">', unsafe_allow_html=True)
st.markdown("""
<div class="step-row">
  <div class="step-num">3</div>
  <p class="step-title">Enter Your Information</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="box box-info">📝 All fields marked with <strong>*</strong> are required. Please use your full legal name as it will appear on the signed agreement.</div>',
            unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    client_name = st.text_input("Full Legal Name *", value=st.session_state.client_name,
                                 placeholder="Jane Doe")
    st.session_state.client_name = client_name
with col2:
    client_email = st.text_input("Email Address *", value=st.session_state.client_email,
                                  placeholder="jane.doe@example.com")
    st.session_state.client_email = client_email

col3, col4 = st.columns(2)
with col3:
    client_phone = st.text_input("Phone Number", value=st.session_state.client_phone,
                                  placeholder="+1 (555) 000-0000")
    st.session_state.client_phone = client_phone
with col4:
    client_business = st.text_input("Business / Company Name (Optional)",
                                     value=st.session_state.client_business,
                                     placeholder="Acme AI Solutions LLC")
    st.session_state.client_business = client_business

# Extra fields for project-based contracts
if ct in ("app_dev","ai_startup","ai_agent","website","funnel"):
    col5, col6 = st.columns(2)
    with col5:
        client_address = st.text_input("Business Address (Optional)",
                                        value=st.session_state.client_address,
                                        placeholder="123 Main St, Miami, FL 33101")
        st.session_state.client_address = client_address
    with col6:
        state_law = st.text_input("Governing State *",
                                   value=st.session_state.state_law if st.session_state.state_law else "Florida",
                                   placeholder="Florida")
        st.session_state.state_law = state_law

    col7, col8 = st.columns(2)
    with col7:
        pkg_options = ct_meta["packages"]
        cur_idx = 0
        if st.session_state.selected_package in pkg_options:
            cur_idx = pkg_options.index(st.session_state.selected_package) + 1
        selected_package = st.selectbox(
            "Selected Package *",
            options=["-- Select a Package --"] + pkg_options,
            index=cur_idx
        )
        if selected_package != "-- Select a Package --":
            st.session_state.selected_package = selected_package
        else:
            st.session_state.selected_package = ""
    with col8:
        project_fee = st.text_input("Total Project / Program Fee *",
                                     value=st.session_state.project_fee,
                                     placeholder="$4,997")
        st.session_state.project_fee = project_fee

    if ct != "ai_startup":
        col9, _ = st.columns(2)
        with col9:
            start_date = st.text_input("Desired Project Start Date",
                                        value=st.session_state.start_date,
                                        placeholder="March 1, 2026")
            st.session_state.start_date = start_date

    extra_notes = st.text_area(
        "Additional Notes / Special Requirements (Optional)",
        value=st.session_state.extra_notes,
        placeholder="Any specific requirements, integrations, custom features, or notes for the Developer...",
        height=90
    )
    st.session_state.extra_notes = extra_notes

# ── Validation ────────────────────────────────────────────────────────────────
email_valid = True
if st.session_state.client_email and not is_valid_email(st.session_state.client_email):
    st.markdown('<div class="box box-error">⚠️ Please enter a valid email address (e.g., name@domain.com).</div>',
                unsafe_allow_html=True)
    email_valid = False

required_ok = bool(st.session_state.client_name and st.session_state.client_email and email_valid)
if ct in ("app_dev","ai_startup","ai_agent","website","funnel"):
    required_ok = required_ok and bool(
        st.session_state.selected_package and
        st.session_state.project_fee and
        st.session_state.state_law
    )

if not required_ok:
    st.markdown('<div class="box box-warn">⚠️ Please complete all required fields marked with * before proceeding to sign.</div>',
                unsafe_allow_html=True)
    st.stop()

st.markdown('<div class="box box-success">✅ All required information has been entered. Please proceed to sign below.</div>',
            unsafe_allow_html=True)

# ── Step 4 — Digital Signature ────────────────────────────────────────────────
st.markdown('<hr class="sdiv">', unsafe_allow_html=True)
st.markdown("""
<div class="step-row">
  <div class="step-num">4</div>
  <p class="step-title">Digital Signature</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="box box-warn">
  ⚠️ <strong>Legal Notice:</strong> Your digital signature below constitutes a legally binding
  electronic signature on this agreement under the Electronic Signatures in Global and National
  Commerce Act (E-SIGN Act, 15 U.S.C. § 7001 et seq.) and applicable state electronic signature laws.
  By signing, you confirm that you have read, understood, and agreed to all terms of this agreement.
</div>
""", unsafe_allow_html=True)

sig_col, info_col = st.columns([3, 1])

with sig_col:
    st.markdown("**✍️ Draw your signature in the box below using your mouse or touchscreen:**")
    st.markdown('<div class="sig-wrap">', unsafe_allow_html=True)
    canvas_result = st_canvas(
        fill_color="rgba(255,255,255,0)",
        stroke_width=3,
        stroke_color="#0a1628",
        background_color="#FFFFFF",
        update_streamlit=True,
        height=200,
        width=660,
        drawing_mode="freedraw",
        key="signature_canvas",
    )
    st.markdown('</div>', unsafe_allow_html=True)
    st.caption("Draw your signature above. Click 'Clear Signature' to start over.")

with info_col:
    st.markdown('<div class="sig-info">', unsafe_allow_html=True)
    phone_line = f"<p>📞 {st.session_state.client_phone}</p>" if st.session_state.client_phone else ""
    biz_line   = f"<p>🏢 {st.session_state.client_business}</p>" if st.session_state.client_business else ""
    pkg_line   = f"<p>📦 {st.session_state.selected_package[:30]}...</p>" if st.session_state.get("selected_package") and len(st.session_state.selected_package) > 30 else (f"<p>📦 {st.session_state.selected_package}</p>" if st.session_state.get("selected_package") else "")
    st.markdown(f"""
    <p><strong>Signing as:</strong></p>
    <p>👤 <strong>{st.session_state.client_name}</strong></p>
    <p>📧 {st.session_state.client_email}</p>
    {phone_line}
    {biz_line}
    <p>📅 {datetime.now().strftime('%B %d, %Y')}</p>
    <p>📄 {ct_meta['icon']} {ct_meta['label'][:35]}...</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("")
    if st.button("🔄 Clear Signature", use_container_width=True):  # noqa
        st.rerun()

# ── Step 5 — Generate & Download ─────────────────────────────────────────────
st.markdown('<hr class="sdiv">', unsafe_allow_html=True)
st.markdown("""
<div class="step-row">
  <div class="step-num">5</div>
  <p class="step-title">Generate & Download Your Signed Agreement</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="box box-info">📥 Click the button below to generate your professionally formatted, signed PDF agreement. It will be available for immediate download and optionally emailed to you.</div>',
            unsafe_allow_html=True)

_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    generate_btn = st.button("📥 Generate Signed Agreement PDF", type="primary", use_container_width=True)  # noqa

if generate_btn:
    if canvas_result.image_data is None or canvas_result.image_data.sum() == 0:
        st.markdown('<div class="box box-warn">⚠️ Please draw your signature in the canvas above before generating the PDF.</div>',
                    unsafe_allow_html=True)
    else:
        with st.spinner("Building your professionally formatted signed agreement..."):
            try:
                cd = datetime.now().strftime("%B %d, %Y")

                if ct == "sales_rep":
                    contract_text = build_sales_rep_text(
                        st.session_state.client_name,
                        st.session_state.client_business,
                        st.session_state.client_phone,
                        cd
                    )
                elif ct == "app_dev":
                    contract_text = build_app_dev_text(
                        st.session_state.client_name,
                        st.session_state.client_business,
                        st.session_state.client_address,
                        st.session_state.client_phone,
                        st.session_state.selected_package,
                        st.session_state.project_fee,
                        st.session_state.start_date,
                        st.session_state.state_law,
                        cd
                    )
                elif ct == "ai_startup":
                    contract_text = build_ai_startup_text(
                        st.session_state.client_name,
                        st.session_state.client_business,
                        st.session_state.client_address,
                        st.session_state.client_phone,
                        st.session_state.selected_package,
                        st.session_state.project_fee,
                        st.session_state.state_law,
                        cd
                    )
                elif ct == "ai_agent":
                    contract_text = build_ai_agent_text(
                        st.session_state.client_name,
                        st.session_state.client_business,
                        st.session_state.client_address,
                        st.session_state.client_phone,
                        st.session_state.selected_package,
                        st.session_state.project_fee,
                        st.session_state.start_date,
                        st.session_state.state_law,
                        cd
                    )
                elif ct == "website":
                    contract_text = build_website_text(
                        st.session_state.client_name,
                        st.session_state.client_business,
                        st.session_state.client_address,
                        st.session_state.client_phone,
                        st.session_state.selected_package,
                        st.session_state.project_fee,
                        st.session_state.start_date,
                        st.session_state.state_law,
                        cd
                    )
                elif ct == "funnel":
                    contract_text = build_funnel_text(
                        st.session_state.client_name,
                        st.session_state.client_business,
                        st.session_state.client_address,
                        st.session_state.client_phone,
                        st.session_state.selected_package,
                        st.session_state.project_fee,
                        st.session_state.start_date,
                        st.session_state.state_law,
                        cd
                    )

                # Append extra notes
                if st.session_state.get("extra_notes"):
                    contract_text += f"\n\nADDITIONAL NOTES / SPECIAL REQUIREMENTS\n{'━'*77}\n\n{st.session_state.extra_notes}\n"

                pdf_bytes = generate_pdf(
                    contract_text,
                    ct_meta["label"],
                    st.session_state.client_name,
                    st.session_state.client_email,
                    st.session_state.client_business,
                    st.session_state.client_phone,
                    canvas_result.image_data,
                )

                safe_name = re.sub(r'[^a-zA-Z0-9]', '_', st.session_state.client_name)
                safe_ct   = ct.upper()
                filename  = f"ATM_Agency_{safe_ct}_Agreement_{safe_name}_{datetime.now().strftime('%Y%m%d')}.pdf"

                st.session_state.pdf_bytes    = pdf_bytes
                st.session_state.pdf_filename = filename
                st.session_state.pdf_ready    = True

                # Send emails
                if EMAIL_ADDRESS:
                    body = (
                        f"Dear {st.session_state.client_name},\n\n"
                        f"Thank you for signing the {ct_meta['label']} with ATM Agency.\n\n"
                        f"Please find your signed agreement attached to this email for your records.\n\n"
                        f"Agreement Details:\n"
                        f"  Contract: {ct_meta['label']}\n"
                        f"  Date Signed: {cd}\n"
                        f"  Email: {st.session_state.client_email}\n\n"
                        f"If you have any questions, please contact us at Entremotivator@gmail.com.\n\n"
                        f"Best regards,\nATM Agency, LLC\nAITMAgency.com"
                    )
                    send_email(st.session_state.client_email,
                               f"Your Signed Agreement – {ct_meta['label']} | ATM Agency",
                               body, pdf_bytes, filename)
                    send_email(ADMIN_EMAIL,
                               f"[NEW SIGNED CONTRACT] {ct_meta['label']} – {st.session_state.client_name}",
                               f"New signed contract received.\n\nClient: {st.session_state.client_name}\nEmail: {st.session_state.client_email}\nContract: {ct_meta['label']}\nDate: {cd}",
                               pdf_bytes, filename)

            except Exception as e:
                st.markdown(f'<div class="box box-error">❌ Error generating PDF: {str(e)}</div>',
                            unsafe_allow_html=True)

if st.session_state.pdf_ready and st.session_state.pdf_bytes:
    st.markdown('<div class="box box-success">✅ <strong>Your signed agreement has been generated successfully!</strong> Click the button below to download your PDF.</div>',
                unsafe_allow_html=True)

    dl_col1, dl_col2, dl_col3 = st.columns([1, 2, 1])
    with dl_col2:
        st.download_button(
            label="⬇️ Download Signed PDF Agreement",
            data=st.session_state.pdf_bytes,
            file_name=st.session_state.pdf_filename,
            mime="application/pdf",
            use_container_width=True,  # noqa
        )

    if EMAIL_ADDRESS:
        st.markdown(f'<div class="box box-info">📧 A copy of your signed agreement has been emailed to <strong>{st.session_state.client_email}</strong>.</div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<div class="box box-warn">📧 Email delivery is not configured. Please download your PDF using the button above and save it for your records.</div>',
                    unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <strong>ATM Agency, LLC</strong> · AITMAgency.com<br>
  Artificial Intelligence Technology Marketing Agency<br>
  All agreements are electronically signed and legally binding under the E-SIGN Act.
</div>
""", unsafe_allow_html=True)
