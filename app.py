import streamlit as st
from groq import Groq
import google.generativeai as genai
import io
import re
import os
import json
import shelve
import threading
import time
import urllib.parse
import contextlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PIL import Image

# ================= APP NAME & LOGO CONFIG =================
st.set_page_config(
    page_title="Harsh's Lex & Tech Suite | iOS Academic Ecosystem",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

ADMIN_EMAIL = "harshrajsoni92@gmail.com"
STORAGE_FILE = "user_memory_store.db"

# ================= PERSISTENT STORAGE ENGINE =================
def load_user_memory():
    default_data = {
        "last_course": "⚖️ Law",
        "last_subject": "🏛️ Constitution",
        "last_topic": "Fundamental Rights (Articles 14, 19 & 21)",
        "study_history": {},
        "ai_memory": {},
        "feedback_list": [],
        "xp_points": 120,
        "streak_days": 3
    }
    try:
        with shelve.open(STORAGE_FILE) as db:
            return dict(db.get("user_state", default_data))
    except Exception:
        return default_data

def save_user_memory():
    try:
        with shelve.open(STORAGE_FILE) as db:
            db["user_state"] = {
                "last_course": st.session_state.current_course,
                "last_subject": st.session_state.current_subject,
                "last_topic": st.session_state.current_topic,
                "study_history": st.session_state.study_history,
                "ai_memory": st.session_state.ai_memory,
                "feedback_list": st.session_state.feedback_list,
                "xp_points": st.session_state.xp_points,
                "streak_days": st.session_state.streak_days
            }
    except Exception:
        pass

saved_state = load_user_memory()

if "system_booted" not in st.session_state:
    st.session_state.system_booted = False

if "current_course" not in st.session_state:
    st.session_state.current_course = saved_state.get("last_course", "⚖️ Law")

if "current_subject" not in st.session_state:
    st.session_state.current_subject = saved_state.get("last_subject", "🏛️ Constitution")

if "current_topic" not in st.session_state:
    st.session_state.current_topic = saved_state.get("last_topic", "Fundamental Rights (Articles 14, 19 & 21)")

if "study_history" not in st.session_state:
    st.session_state.study_history = saved_state.get("study_history", {})

if "ai_memory" not in st.session_state:
    st.session_state.ai_memory = saved_state.get("ai_memory", {})

if "feedback_list" not in st.session_state:
    st.session_state.feedback_list = saved_state.get("feedback_list", [])

if "xp_points" not in st.session_state:
    st.session_state.xp_points = saved_state.get("xp_points", 120)

if "streak_days" not in st.session_state:
    st.session_state.streak_days = saved_state.get("streak_days", 3)

if "feedback_popup_shown" not in st.session_state:
    st.session_state.feedback_popup_shown = False

if "trigger_feedback_modal" not in st.session_state:
    st.session_state.trigger_feedback_modal = False

if "generated_gallery_sheets" not in st.session_state:
    st.session_state.generated_gallery_sheets = []

if "active_sheet_index" not in st.session_state:
    st.session_state.active_sheet_index = None

if "flashcards_data" not in st.session_state:
    st.session_state.flashcards_data = []

if "cheatsheet_html" not in st.session_state:
    st.session_state.cheatsheet_html = ""

if "active_exam_questions" not in st.session_state:
    st.session_state.active_exam_questions = []

if "exam_user_answers" not in st.session_state:
    st.session_state.exam_user_answers = {}

if "exam_submitted" not in st.session_state:
    st.session_state.exam_submitted = False

if "mock_page" not in st.session_state:
    st.session_state.mock_page = 0

if "dpp_questions" not in st.session_state:
    st.session_state.dpp_questions = []

if "dpp_user_answers" not in st.session_state:
    st.session_state.dpp_user_answers = {}

if "dpp_submitted" not in st.session_state:
    st.session_state.dpp_submitted = False

if "dpp_page" not in st.session_state:
    st.session_state.dpp_page = 0

if "pyq_questions" not in st.session_state:
    st.session_state.pyq_questions = []

if "pyq_user_answers" not in st.session_state:
    st.session_state.pyq_user_answers = {}

if "pyq_submitted" not in st.session_state:
    st.session_state.pyq_submitted = False

if "pyq_page" not in st.session_state:
    st.session_state.pyq_page = 0

if "notebook_cells" not in st.session_state:
    st.session_state.notebook_cells = [
        {
            "id": 1,
            "code": "# Python Cell 1: Verification & Environment\ndeveloper_name = 'Harsh Raj Soni'\ninstitution = 'MLK PG College, Balrampur'\nprint(f'Harsh\\'s Lex & Tech Suite Active | Developer: {developer_name} [{institution}]')",
            "output": "",
            "error": ""
        }
    ]

def add_student_xp(amount=25):
    st.session_state.xp_points = st.session_state.get("xp_points", 120) + amount
    save_user_memory()

def get_student_rank(xp):
    if xp < 250:
        return "🌱 Rising Aspirant"
    elif xp < 500:
        return "⚡ Pro Scholar"
    elif xp < 1000:
        return "🔥 Exam Conqueror"
    return "👑 Grandmaster Ranker"

# ================= ANTI-SLEEP KEEP ALIVE HEARTBEAT =================
def run_anti_sleep_heartbeat():
    while True:
        try:
            time.sleep(300)
        except Exception:
            pass

if "heartbeat_started" not in st.session_state:
    st.session_state.heartbeat_started = True
    t = threading.Thread(target=run_anti_sleep_heartbeat, daemon=True)
    t.start()

# ================= iOS 18 DYNAMIC MESH AURORA PALETTES =================
THEME_PALETTES = {
    "⚖️ Law": {
        "orb1": "#3B0A26",
        "orb2": "#1E1B4B",
        "base": "#080711",
        "accent": "#FF5E8E",
        "accent_sec": "#A855F7",
        "glow": "rgba(255, 94, 142, 0.30)",
        "glass": "rgba(24, 18, 38, 0.65)",
        "border": "rgba(255, 94, 142, 0.40)"
    },
    "🩺 NEET": {
        "orb1": "#063428",
        "orb2": "#0A283E",
        "base": "#040D12",
        "accent": "#2DD4BF",
        "accent_sec": "#38BDF8",
        "glow": "rgba(45, 212, 191, 0.28)",
        "glass": "rgba(10, 30, 36, 0.65)",
        "border": "rgba(45, 212, 191, 0.40)"
    },
    "⚙️ JEE": {
        "orb1": "#361909",
        "orb2": "#1E1B4B",
        "base": "#0B0813",
        "accent": "#FB923C",
        "accent_sec": "#F43F5E",
        "glow": "rgba(251, 146, 60, 0.28)",
        "glass": "rgba(30, 20, 28, 0.65)",
        "border": "rgba(251, 146, 60, 0.40)"
    },
    "💻 BCA": {
        "orb1": "#0C244E",
        "orb2": "#251042",
        "base": "#050814",
        "accent": "#38BDF8",
        "accent_sec": "#818CF8",
        "glow": "rgba(56, 189, 248, 0.30)",
        "glass": "rgba(14, 23, 46, 0.65)",
        "border": "rgba(56, 189, 248, 0.40)"
    },
    "🏛️ UPSC": {
        "orb1": "#261046",
        "orb2": "#0F2942",
        "base": "#070612",
        "accent": "#C084FC",
        "accent_sec": "#60A5FA",
        "glow": "rgba(192, 132, 252, 0.28)",
        "glass": "rgba(22, 16, 42, 0.65)",
        "border": "rgba(192, 132, 252, 0.40)"
    }
}

# Normalize legacy course name if stored in shelve
if st.session_state.current_course not in THEME_PALETTES:
    st.session_state.current_course = "⚖️ Law"

active_theme = THEME_PALETTES[st.session_state.current_course]

groq_key = st.secrets.get("GROQ_API_KEY", None)
gemini_key = st.secrets.get("GEMINI_API_KEY", None)
gmail_app_password = st.secrets.get("GMAIL_APP_PASSWORD", None)

# ================= AUTOMATIC BACKGROUND GMAIL SMTP SENDER =================
def send_auto_smtp_email(sender_name, student_email, stream_name, rating_str, feedback_text, app_pwd):
    if not app_pwd:
        return False, "No App Password"
    try:
        clean_pwd = app_pwd.replace(" ", "").strip()
        msg = MIMEMultipart("alternative")
        msg["From"] = f"Harsh's Lex & Tech Suite <{ADMIN_EMAIL}>"
        msg["To"] = ADMIN_EMAIL
        if student_email and "@" in student_email:
            msg["Reply-To"] = student_email
        msg["Subject"] = f"⭐ New Portal Rating ({rating_str.split(' ')[0]}) from {sender_name}"

        html_body = f"""
        <div style="font-family: -apple-system, sans-serif; max-width: 580px; border: 2px solid #38BDF8; border-radius: 16px; padding: 22px; background: #0F172A; color: #F8FAFC;">
            <h2 style="color: #38BDF8; margin-top: 0;">⚖️ Harsh's Lex & Tech Suite — Student Review</h2>
            <p style="font-size: 14px; color: #CBD5E1;">Hello <b>Harsh Raj Soni</b>, ek student ne aapke portal par naya review submit kiya hai:</p>
            <table style="width: 100%; border-collapse: collapse; margin: 14px 0; font-size: 14px; color: #F8FAFC;">
                <tr><td style="padding: 8px; border-bottom: 1px solid #334155;"><b>Student Name:</b></td><td style="padding: 8px; border-bottom: 1px solid #334155;">{sender_name}</td></tr>
                <tr><td style="padding: 8px; border-bottom: 1px solid #334155;"><b>Student Email:</b></td><td style="padding: 8px; border-bottom: 1px solid #334155;">{student_email if student_email else 'Not provided'}</td></tr>
                <tr><td style="padding: 8px; border-bottom: 1px solid #334155;"><b>Course:</b></td><td style="padding: 8px; border-bottom: 1px solid #334155;">{stream_name}</td></tr>
                <tr><td style="padding: 8px; border-bottom: 1px solid #334155;"><b>Rating:</b></td><td style="padding: 8px; border-bottom: 1px solid #334155; color: #FBBF24; font-weight: bold;">{rating_str}</td></tr>
            </table>
            <div style="background: #1E293B; border-left: 4px solid #38BDF8; padding: 12px 16px; border-radius: 8px; margin-top: 12px;">
                <div style="font-size: 12px; color: #94A3B8; margin-bottom: 4px;"><b>Feedback Message:</b></div>
                <div style="font-size: 14.5px; color: #FFFFFF; line-height: 1.5;">{feedback_text}</div>
            </div>
        </div>
        """
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=12) as server:
            server.login(ADMIN_EMAIL, clean_pwd)
            server.sendmail(ADMIN_EMAIL, ADMIN_EMAIL, msg.as_string())
        return True, "Delivered"
    except Exception as e:
        return False, str(e)

# ================= RATING & FEEDBACK POPUP DIALOG ENGINE =================
def render_feedback_form_contents(context_key="modal"):
    st.markdown(f"""
    <div class="ios-glass-card" style="padding:14px 18px; margin-bottom:12px;">
        <div style="font-size:16px; font-weight:700; color:{active_theme['accent']};">⭐ Rate & Share Your Experience</div>
        <div style="font-size:12px; color:#CBD5E1; margin-top:2px;">
            Submit karte hi aapka feedback seedhe Developer <b>Harsh Raj Soni</b> (<code>{ADMIN_EMAIL}</code>) ke Gmail inbox mein jayega.
        </div>
    </div>
    """, unsafe_allow_html=True)

    star_options = [
        "⭐⭐⭐⭐⭐ (5/5 - Super Smooth & Addictive!)",
        "⭐⭐⭐⭐ (4/5 - Bohot Badhiya Hai)",
        "⭐⭐⭐ (3/5 - Achha Hai)",
        "⭐⭐ (2/5 - Needs Improvement)",
        "⭐ (1/5 - Issue Aa Raha Hai)"
    ]
    chosen_stars = st.radio("Select Star Rating:", star_options, index=0, key=f"fb_stars_{context_key}")

    c_n, c_e = st.columns(2)
    with c_n:
        fb_name = st.text_input("Aapka Naam:", placeholder="e.g. Aman Verma", key=f"fb_name_{context_key}")
    with c_e:
        fb_user_email = st.text_input("Aapka Email (Optional):", placeholder="student@gmail.com", key=f"fb_uemail_{context_key}")

    fb_msg = st.text_area(
        "Aapka Feedback / Feature Idea:",
        placeholder="UI, Animations ya Notes kaise lage? Zaroor batayein...",
        height=90,
        key=f"fb_msg_{context_key}"
    )

    if st.button("🚀 Submit Rating & Send to Harsh", key=f"fb_sub_{context_key}", type="primary", use_container_width=True):
        sender = fb_name.strip() if fb_name.strip() else "Anonymous Student"
        u_mail = fb_user_email.strip()
        comment = fb_msg.strip() if fb_msg.strip() else "Loved the new iOS UI!"
        rating_short = chosen_stars.split(" ")[0]

        entry = {
            "name": sender,
            "email": u_mail,
            "course": st.session_state.current_course,
            "rating": rating_short,
            "full_rating": chosen_stars,
            "message": comment,
            "time": time.strftime("%d %b %Y, %I:%M %p")
        }
        st.session_state.feedback_list.insert(0, entry)
        st.session_state.feedback_popup_shown = True
        st.session_state.trigger_feedback_modal = False
        add_student_xp(50)

        active_pwd = gmail_app_password if gmail_app_password else st.session_state.get("manual_gmail_pwd", "")

        if active_pwd:
            with st.spinner("Sending feedback automatically to harshrajsoni92@gmail.com..."):
                sent_ok, _ = send_auto_smtp_email(
                    sender, u_mail, st.session_state.current_course, chosen_stars, comment, active_pwd
                )
            if sent_ok:
                st.balloons()
                st.success(f"✅ Shukriya {sender}! Aapka review `{ADMIN_EMAIL}` par deliver ho gaya (+50 XP)!")
                return

        subject_line = f"Portal Rating {rating_short} from {sender}"
        body_line = f"Student: {sender}\nStream: {st.session_state.current_course}\nRating: {chosen_stars}\n\nFeedback:\n{comment}"
        gmail_web_link = f"https://mail.google.com/mail/?view=cm&fs=1&to={ADMIN_EMAIL}&su={urllib.parse.quote(subject_line)}&body={urllib.parse.quote(body_line)}"

        st.success("🎉 Rating save ho gayi (+50 XP)! Instant Gmail dispatch ke liye niche tap karein:")
        st.markdown(f'<a href="{gmail_web_link}" target="_blank" style="background:#EA4335; color:#FFF; padding:8px 16px; border-radius:10px; font-weight:700; text-decoration:none; display:inline-block;">📧 Send via Gmail ({ADMIN_EMAIL})</a>', unsafe_allow_html=True)

if hasattr(st, "dialog"):
    @st.dialog("⭐ Rate & Feedback — Harsh's Lex & Tech Suite")
    def open_feedback_popup_dialog():
        render_feedback_form_contents(context_key="popup_dlg")
elif hasattr(st, "experimental_dialog"):
    @st.experimental_dialog("⭐ Rate & Feedback — Harsh's Lex & Tech Suite")
    def open_feedback_popup_dialog():
        render_feedback_form_contents(context_key="popup_dlg")
else:
    def open_feedback_popup_dialog():
        with st.expander("⭐ Rate & Feedback Popup", expanded=True):
            render_feedback_form_contents(context_key="popup_fallback")

# ================= CLEAN, SIMPLE & USER-FRIENDLY COURSE DATABASE =================
COURSE_DATABASE = {
    "⚖️ Law": {
        "full_title": "Law & Judiciary (LL.B • CLAT • PCS-J • AIBE)",
        "subjects": {
            "🏛️ Constitution": {
                "units": "Part I-II (Art 1–11) • Fundamental Rights (Art 12–35) • DPSP (Art 36–51A) • Union & State Judiciary • Emergency & Amendments (Art 352–368)",
                "topics": [
                    "Preamble & Basic Structure Doctrine (Kesavananda Bharati)",
                    "Fundamental Rights: Article 14, 19 & 21 (Golden Triangle)",
                    "Constitutional Writs: Article 32 vs Article 226 (5 Writs)",
                    "Freedom of Religion (Art 25–28) & Minority Rights (Art 29–30)",
                    "Supreme Court, High Courts & Collegium System",
                    "Emergency Provisions (Art 352, 356, 360) & Article 368 Amendment"
                ],
                "pyqs_years": ["CLAT 2025 Official Paper", "UP PCS-J Judiciary 2024", "AIBE XIX Official Paper", "DU / CUET LL.B 2024"]
            },
            "⚔️ Criminal Law": {
                "units": "Bharatiya Nyaya Sanhita (BNS 2023) vs IPC • BNSS 2023 vs CrPC • Bharatiya Sakshya Adhiniyam (BSA 2023) vs Evidence Act",
                "topics": [
                    "General Exceptions & Private Defence (Sec 14–44 BNS / Sec 76–106 IPC)",
                    "Culpable Homicide vs Murder (Sec 100–103 BNS / Sec 299–302 IPC)",
                    "Offences Against Women & Organised Crime (Sec 63–113 BNS)",
                    "Theft, Snatching, Extortion, Robbery & Dacoity (Sec 303–310 BNS)",
                    "Zero FIR, e-FIR, Arrest & Police Remand (Sec 173 & 187 BNSS)",
                    "Regular Bail & Anticipatory Bail (Sec 480–482 BNSS / Sec 438 CrPC)",
                    "Dying Declaration & Electronic Evidence (Sec 26 & 63 BSA 2023)"
                ],
                "pyqs_years": ["PCS-J Criminal Law 2024", "AIBE Criminal Law Paper", "CLAT PG Criminal Law", "UGC NET Law Paper"]
            },
            "📜 Contract & Property": {
                "units": "Indian Contract Act 1872 (Sec 1–238) • Specific Relief Act 1963 • Transfer of Property Act (TPA 1882)",
                "topics": [
                    "Offer, Acceptance, Consideration & Capacity (Mohori Bibee Case)",
                    "Free Consent: Coercion, Undue Influence, Fraud & Mistake (Sec 13–22)",
                    "Doctrine of Frustration (Sec 56) & Breach of Contract Damages (Sec 73–75)",
                    "Indemnity, Guarantee, Bailment, Pledge & Agency (Sec 124–238)",
                    "Transfer of Property: Ostensible Owner, Election & Lis Pendens (Sec 52)",
                    "Specific Performance & Injunctions (Specific Relief Act)"
                ],
                "pyqs_years": ["PCS-J Civil Law Paper 2024", "CLAT Legal Reasoning 2025", "AIBE Contract & Property"]
            },
            "⚖️ Civil & Torts": {
                "units": "Code of Civil Procedure (CPC 1908) • Limitation Act 1963 • Law of Torts & Consumer Protection 2019",
                "topics": [
                    "Res Sub Judice (Sec 10) & Constructive Res Judicata (Sec 11 CPC)",
                    "Stages of Civil Suit & Rejection of Plaint (Order VII Rule 11 CPC)",
                    "Temporary Injunctions (Order XXXIX) & Appeals, Reference, Revision",
                    "Law of Torts: Strict Liability (Rylands v Fletcher) vs Absolute Liability",
                    "Damnum Sine Injuria vs Injuria Sine Damno & Negligence",
                    "Consumer Protection Act 2019 & Product Liability"
                ],
                "pyqs_years": ["PCS-J CPC & Torts 2024", "CLAT Torts & Legal Maxims", "AIBE Civil Procedure"]
            },
            "👨‍👩‍👧 Family & Corporate": {
                "units": "Hindu Marriage & Succession Acts • Muslim Personal Law • NI Act Sec 138 • Companies Act & Arbitration",
                "topics": [
                    "Hindu Marriage Act 1955: Void Marriages, RCR (Sec 9) & Divorce (Sec 13)",
                    "Hindu Succession Act: Daughters' Coparcenary Rights (Vineeta Sharma Case)",
                    "Muslim Law: Nikah, Mahr, Triple Talaq (Shayara Bano) & Maintenance",
                    "Dishonour of Cheque (Section 138 Negotiable Instruments Act)",
                    "Corporate Veil, Indoor Management & Arbitration Act (Sec 9 & 34)"
                ],
                "pyqs_years": ["PCS-J Family Law 2024", "CLAT PG Corporate & Family Law", "AIBE Family & ADR"]
            }
        }
    },
    "🩺 NEET": {
        "full_title": "NEET Medical Entrance (Biology • Chemistry • Physics)",
        "subjects": {
            "🧬 Zoology": {
                "units": "Human Physiology • Neural & Chemical Coordination • Reproduction • Evolution & Genetics",
                "topics": [
                    "Nerve Impulse Generation & Synaptic Transmission (Action Potential)",
                    "Muscle Contraction: Sliding Filament Theory & Sarcomere",
                    "Cardiac Cycle, ECG Waves & Double Circulation",
                    "Human Reproduction: Gametogenesis & Menstrual Cycle",
                    "DNA Replication, Transcription & Lac Operon Model"
                ],
                "pyqs_years": ["NEET UG 2025 Official", "NEET UG 2024 Official", "NEET UG 2023 Official", "NEET UG 2022 Official"]
            },
            "🌿 Botany": {
                "units": "Plant Kingdom • Cell Biology • Photosynthesis & Respiration • Mendelian Genetics • Ecology",
                "topics": [
                    "Light Reaction: Z-Scheme & Cyclic vs Non-Cyclic Photophosphorylation",
                    "Calvin Cycle (C3) vs Hatch-Slack (C4) Pathway",
                    "Glycolysis, Krebs Cycle (TCA) & Electron Transport System",
                    "Mendelian Dihybrid Cross, Linkage & Pedigree Analysis",
                    "Double Fertilization in Angiosperms & Plant Hormones"
                ],
                "pyqs_years": ["NEET UG 2025 Official", "NEET UG 2024 Official", "NEET UG 2023 Official"]
            },
            "🧪 Chemistry": {
                "units": "Chemical Bonding • Organic Mechanisms • Coordination Compounds • Thermodynamics & Electrochemistry",
                "topics": [
                    "VSEPR Theory, Hybridization & Molecular Orbital Theory (MOT)",
                    "SN1 vs SN2 Reactions & Stereochemistry",
                    "Aldol Condensation, Cannizzaro & Named Organic Reactions",
                    "Coordination Compounds & Crystal Field Theory (CFT)",
                    "Thermodynamics, Gibbs Free Energy & Nernst Equation"
                ],
                "pyqs_years": ["NEET UG 2025 Chemistry", "NEET UG 2024 Chemistry", "NEET UG 2023 Chemistry"]
            },
            "⚛️ Physics": {
                "units": "Mechanics • Electrostatics & Current • Magnetism • Ray & Wave Optics • Modern Physics & Semiconductors",
                "topics": [
                    "Projectile Motion, NLM & Circular Motion Dynamics",
                    "Ray Optics: Lens Maker Formula, Prism & TIR",
                    "Current Electricity: Kirchhoff's Laws, Wheatstone & Potentiometer",
                    "Photoelectric Effect, Bohr Atomic Model & de Broglie Waves",
                    "Semiconductors, Logic Gates (AND, OR, NAND, NOR) & Diodes"
                ],
                "pyqs_years": ["NEET UG 2025 Physics", "NEET UG 2024 Physics", "NEET UG 2023 Physics"]
            }
        }
    },
    "⚙️ JEE": {
        "full_title": "JEE Main & Advanced (Mathematics • Physics • Chemistry)",
        "subjects": {
            "📐 Mathematics": {
                "units": "Calculus (Differential & Integral) • Coordinate Geometry • Matrices & Complex Numbers • Vectors & 3D",
                "topics": [
                    "Definite Integration: King's Property, Leibnitz Rule & Walli's Formula",
                    "Conic Sections: Parabola, Ellipse & Hyperbola Tangents",
                    "Matrices, Determinants & System of Linear Equations (Cramer's Rule)",
                    "Complex Numbers: De Moivre's Theorem & Roots of Unity",
                    "Vectors & 3D Geometry: Skew Lines & Planes"
                ],
                "pyqs_years": ["JEE Main 2025 Shifts", "JEE Advanced 2024 Paper", "JEE Main 2024 Shifts"]
            },
            "⚛️ Physics": {
                "units": "Rotational Mechanics • Electrodynamics • Magnetism & EMI • Thermodynamics • Optics & Modern Physics",
                "topics": [
                    "Rotational Motion: Moment of Inertia, Torque & Pure Rolling",
                    "Electrostatics: Gauss Law, Potential & Dielectrics in Capacitors",
                    "Moving Charges, Biot-Savart Law & Faraday's EMI",
                    "Wave Optics: Young's Double Slit Experiment (YDSE) & Diffraction",
                    "SHM, String Waves & Doppler Effect"
                ],
                "pyqs_years": ["JEE Main 2025 Physics", "JEE Advanced 2024 Physics", "JEE Main 2024 Physics"]
            },
            "🧪 Chemistry": {
                "units": "Physical Chemistry (Kinetics, Electro, Ionic) • Organic Reaction Mechanisms • Inorganic & Coordination",
                "topics": [
                    "Electrochemistry: Nernst Equation, Conductance & Kohlrausch Law",
                    "Chemical Kinetics: First Order Rate Law & Arrhenius Equation",
                    "Ionic Equilibrium: Buffer Solutions, pH & Salt Hydrolysis",
                    "GOC, Isomerism & Carbonyl Compounds Mechanisms"
                ],
                "pyqs_years": ["JEE Main 2025 Chemistry", "JEE Advanced 2024 Chemistry"]
            }
        }
    },
    "💻 BCA": {
        "full_title": "BCA Computer Applications (Python • CSA • Mathematics)",
        "subjects": {
            "🐍 Python": {
                "units": "Unit 1: Python Internals • Unit 2: Control Flow & Loops • Unit 3: Functions • Unit 4: Lists/Dicts • Unit 5: OOPs & Files",
                "topics": [
                    "Python Architecture, Bytecode (.pyc) & PVM Memory Management",
                    "Control Flow, Loops, For-Else Construct & Prime/Fibonacci Logic",
                    "Functions, LEGB Scope Rule, Recursion & Lambda Expressions",
                    "Data Structures: Lists, Tuples, Dictionaries & Sets Operations",
                    "Object Oriented Programming: Class, Inheritance & Polymorphism",
                    "File Handling (Read/Write) & Exception Handling (Try-Except)"
                ],
                "pyqs_years": ["BCA University Paper 2025", "BCA University Paper 2024", "BCA University Paper 2023"]
            },
            "🖥️ Computer Arch (CSA)": {
                "units": "Unit 1: Digital Logic Gates • Unit 2: K-Maps & Boolean Algebra • Unit 3: Adders & Flip-Flops • Unit 4: CPU & Cache",
                "topics": [
                    "Logic Gates, De-Morgan's Theorem & Universal Gates (NAND/NOR)",
                    "Half Adder & Full Adder Circuit Design with Truth Table",
                    "K-Map (Karnaugh Map) 4-Variable Minimization & Don't Care",
                    "Flip-Flops (SR, JK, D, T) & Master-Slave Race Around Condition",
                    "Instruction Cycle (Fetch-Decode-Execute) & Cache Memory Mapping"
                ],
                "pyqs_years": ["BCA CSA Paper 2025", "BCA CSA Paper 2024", "BCA CSA Paper 2023"]
            },
            "📐 BCA Maths": {
                "units": "Unit 1: Matrices & Rank • Unit 2: Differential Calculus • Unit 3: Set Theory & Relations • Unit 4: Numerical Methods",
                "topics": [
                    "Matrix Rank, Echelon Form & Cayley-Hamilton Theorem",
                    "L'Hopital's Rule for Limits & Leibnitz n-th Derivative Theorem",
                    "Equivalence Relations, POSET & Hasse Diagrams",
                    "Newton-Raphson & Bisection Numerical Root Methods"
                ],
                "pyqs_years": ["BCA Maths Paper 2025", "BCA Maths Paper 2024"]
            }
        }
    },
    "🏛️ UPSC": {
        "full_title": "UPSC Civil Services (Polity • Economy • Geography • History)",
        "subjects": {
            "📜 Indian Polity": {
                "units": "Constitutional Framework • Fundamental Rights & Duties • Parliament & State Legislature • Constitutional Bodies",
                "topics": [
                    "Fundamental Rights (Art 14–32) & Basic Structure Evolution",
                    "Parliamentary Committees, Money Bill vs Financial Bill",
                    "President vs Governor: Veto & Pardoning Powers",
                    "Panchayati Raj (73rd & 74th Amendments) & Election Commission"
                ],
                "pyqs_years": ["UPSC CSE Prelims 2025", "UPSC CSE Prelims 2024", "UPSC CSE Prelims 2023"]
            },
            "🌍 Economy & Geo": {
                "units": "RBI Monetary Policy & Banking • Fiscal Policy & Budget • Indian Monsoon & Geomorphology • Environment",
                "topics": [
                    "RBI Monetary Policy: Repo Rate, CRR, SLR & Open Market Operations",
                    "Balance of Payments (BoP), Fiscal Deficit & GST Council",
                    "Indian Monsoon Mechanism: El Niño, La Niña & Indian Ocean Dipole",
                    "Himalayan vs Peninsular River Systems & Plate Tectonics"
                ],
                "pyqs_years": ["UPSC CSE Prelims 2025", "UPSC CSE Prelims 2024"]
            }
        }
    }
}

# ================= iOS 18 / VISION-OS ULTRA-SMOOTH ANIMATED CSS =================
IOS_DYNAMIC_CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Kalam:wght@400;700&family=Patrick+Hand&display=swap');

    /* Keyframe Animations for Buttery Smooth iOS Feel */
    @keyframes iosAuroraShift {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    @keyframes springSlideUp {{
        0% {{ opacity: 0; transform: translateY(18px) scale(0.98); }}
        100% {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}

    @keyframes pulseGlow {{
        0%, 100% {{ box-shadow: 0 0 14px {active_theme['glow']}; }}
        50% {{ box-shadow: 0 0 26px {active_theme['glow']}; }}
    }}

    @keyframes islandFloat {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-2px); }}
    }}

    html, body, [class*="css"] {{
        font-family: -apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', sans-serif;
        scroll-behavior: smooth;
    }}
    code, pre {{
        font-family: 'JetBrains Mono', monospace !important;
    }}

    /* Dynamic Animated iOS 18 Mesh Background */
    .stApp {{
        background: 
            radial-gradient(circle at 15% 15%, {active_theme['orb1']} 0%, transparent 45%),
            radial-gradient(circle at 85% 25%, {active_theme['orb2']} 0%, transparent 50%),
            radial-gradient(circle at 50% 90%, {active_theme['orb1']} 0%, transparent 55%),
            {active_theme['base']} !important;
        background-size: 200% 200% !important;
        animation: iosAuroraShift 18s ease infinite !important;
        color: #F8FAFC;
        transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    header[data-testid="stHeader"], footer, #MainMenu,
    .viewerBadge_container__1QSob, [data-testid="stStatusWidget"],
    .stDeployButton, div[data-testid="stToolbar"], div[data-testid="stDecoration"] {{
        display: none !important;
        visibility: hidden !important;
    }}

    .block-container {{
        padding-top: 0.6rem !important;
        padding-bottom: 3rem !important;
        max-width: 1060px !important;
        animation: springSlideUp 0.55s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    /* iOS Dynamic Island Header */
    .ios-dynamic-island {{
        background: rgba(12, 14, 24, 0.78);
        backdrop-filter: blur(28px) saturate(180%);
        -webkit-backdrop-filter: blur(28px) saturate(180%);
        border: 1px solid {active_theme['border']};
        border-radius: 36px;
        padding: 10px 22px;
        margin: 0 auto 14px auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px;
        box-shadow: 0 14px 34px rgba(0, 0, 0, 0.55), 0 0 20px {active_theme['glow']};
        animation: islandFloat 5s ease-in-out infinite;
    }}

    .island-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid {active_theme['border']};
        padding: 4px 13px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        color: {active_theme['accent']};
        transition: all 0.3s ease;
    }}

    /* Frosted Glass Cards */
    .ios-glass-card {{
        background: {active_theme['glass']};
        backdrop-filter: blur(24px) saturate(160%);
        -webkit-backdrop-filter: blur(24px) saturate(160%);
        border: 1px solid rgba(255, 255, 255, 0.14);
        border-radius: 18px;
        padding: 14px 18px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
        transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        animation: springSlideUp 0.45s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .ios-glass-card:hover {{
        transform: translateY(-3px) scale(1.005);
        border-color: {active_theme['accent']};
        box-shadow: 0 14px 36px rgba(0, 0, 0, 0.45), 0 0 18px {active_theme['glow']};
    }}

    /* Question Cards */
    .question-card {{
        background: {active_theme['glass']};
        backdrop-filter: blur(22px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-left: 5px solid {active_theme['accent']};
        border-radius: 16px;
        padding: 14px 18px;
        margin-bottom: 8px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s ease;
        animation: springSlideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .question-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 12px 28px rgba(0,0,0,0.4), 0 0 16px {active_theme['glow']};
    }}
    .question-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        padding-bottom: 4px;
    }}
    .q-number-tag {{
        background: {active_theme['glow']};
        border: 1px solid {active_theme['accent']};
        color: {active_theme['accent']};
        font-size: 11.5px;
        font-weight: 700;
        padding: 2px 10px;
        border-radius: 14px;
    }}
    .q-marks-tag {{
        font-size: 11px;
        color: #CBD5E1;
        font-family: 'JetBrains Mono', monospace;
    }}
    .q-text {{
        font-size: 15px;
        font-weight: 600;
        line-height: 1.5;
        color: #F8FAFC;
    }}

    /* iOS Segmented Pill Navigation Bar */
    div[data-testid="stRadio"] {{
        background: rgba(15, 20, 35, 0.68) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        padding: 6px 12px !important;
        border-radius: 22px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3) !important;
        margin-bottom: 10px !important;
        transition: all 0.3s ease !important;
    }}

    /* Springy iOS Buttons */
    .stButton>button {{
        background: linear-gradient(135deg, {active_theme['accent']} 0%, {active_theme['accent_sec']} 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        border-radius: 14px !important;
        padding: 7px 16px !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        letter-spacing: 0.2px !important;
        transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 6px 18px {active_theme['glow']} !important;
    }}
    .stButton>button:hover {{
        transform: translateY(-2px) scale(1.015) !important;
        box-shadow: 0 10px 26px {active_theme['glow']} !important;
        filter: brightness(1.08);
    }}
    .stButton>button:active {{
        transform: translateY(1px) scale(0.98) !important;
    }}

    /* 3D Interactive Flip Flashcards */
    .flip-card-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 16px;
        margin: 14px 0;
    }}
    .flip-card {{
        background-color: transparent;
        height: 195px;
        perspective: 1000px;
        cursor: pointer;
    }}
    .flip-card-inner {{
        position: relative;
        width: 100%;
        height: 100%;
        text-align: center;
        transition: transform 0.65s cubic-bezier(0.16, 1, 0.3, 1);
        transform-style: preserve-3d;
        border-radius: 18px;
    }}
    .flip-card:hover .flip-card-inner, .flip-card:active .flip-card-inner {{
        transform: rotateY(180deg);
    }}
    .flip-card-front, .flip-card-back {{
        position: absolute;
        width: 100%;
        height: 100%;
        -webkit-backface-visibility: hidden;
        backface-visibility: hidden;
        border-radius: 18px;
        padding: 18px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 0 10px 26px rgba(0,0,0,0.4);
    }}
    .flip-card-front {{
        background: {active_theme['glass']};
        backdrop-filter: blur(20px);
        border: 1.5px solid {active_theme['border']};
        color: #F8FAFC;
    }}
    .flip-card-back {{
        background: linear-gradient(135deg, {active_theme['orb1']} 0%, {active_theme['orb2']} 100%);
        border: 2px solid {active_theme['accent']};
        color: #FFFFFF;
        transform: rotateY(180deg);
    }}

    /* FIXED RULED NOTEBOOK SHEET & BALANCED TABLE (NEVER SQUISHES COLUMNS!) */
    .register-outer-center {{
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-top: 8px;
        margin-bottom: 12px;
        animation: springSlideUp 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    .real-notebook-sheet {{
        background-color: #fbfbf8 !important;
        background-image: 
            linear-gradient(90deg, transparent 36px, #ef4444 36px, #ef4444 37.5px, transparent 37.5px),
            linear-gradient(#e2e8f0 1px, transparent 1px) !important;
        background-size: 100% 100%, 100% 23px !important;
        border-radius: 14px !important;
        padding: 20px 18px 18px 46px !important;
        border: 2px solid #cbd5e1 !important;
        box-shadow: 0 14px 36px rgba(0, 0, 0, 0.55) !important;
        width: 100% !important;
        max-width: 650px !important;
        height: auto !important;
        overflow: visible !important;
        box-sizing: border-box !important;
        font-family: 'Patrick Hand', 'Kalam', cursive !important;
        color: #1e3a8a !important;
        font-size: 15px !important;
        line-height: 23px !important;
        position: relative !important;
    }}

    .real-notebook-sheet::before {{
        content: '' !important;
        position: absolute !important;
        top: 12px !important;
        left: 10px !important;
        width: 10px !important;
        height: 94% !important;
        background-image: radial-gradient(circle, #94a3b8 3px, transparent 4px) !important;
        background-size: 10px 23px !important;
        background-repeat: repeat-y !important;
    }}

    .nb-title-h1 {{
        font-family: 'Kalam', cursive !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #1e1b4b !important;
        background: #fdf2f8 !important;
        padding: 2px 10px !important;
        border-radius: 6px !important;
        display: inline-block !important;
        border-bottom: 2px dashed #ec4899 !important;
        margin-top: 2px !important;
        margin-bottom: 4px !important;
        line-height: 24px !important;
    }}

    .nb-subhead {{
        font-weight: 700 !important;
        color: #0369a1 !important;
        font-size: 15px !important;
        text-decoration: underline !important;
        margin-top: 6px !important;
        display: block !important;
    }}

    .table-container {{
        width: 100% !important;
        margin: 6px 0 !important;
        box-sizing: border-box !important;
    }}

    /* Fixed Table Layout guarantees NO column gets squished to 1 letter wide */
    .nb-table {{
        border-collapse: collapse !important;
        table-layout: fixed !important;
        width: 100% !important;
        font-family: 'Patrick Hand', cursive !important;
        font-size: 13.5px !important;
        line-height: 18px !important;
        background: #ffffff !important;
        border: 1.5px solid #1e3a8a !important;
        box-sizing: border-box !important;
    }}
    .nb-table th, .nb-table td {{
        border: 1px solid #1e3a8a !important;
        padding: 5px 8px !important;
        text-align: left !important;
        vertical-align: top !important;
        word-break: normal !important;
        overflow-wrap: break-word !important;
    }}
    .nb-table th:nth-child(1), .nb-table td:nth-child(1) {{ width: 28% !important; font-weight: 700 !important; }}
    .nb-table th:nth-child(2), .nb-table td:nth-child(2) {{ width: 32% !important; }}
    .nb-table th:nth-child(3), .nb-table td:nth-child(3) {{ width: 40% !important; }}
    .nb-table th {{
        background: #e0f2fe !important;
        color: #0369a1 !important;
        font-weight: 700 !important;
        text-align: center !important;
    }}

    .nb-keypoints-box {{
        border: 1.5px dashed #16a34a !important;
        background: #f0fdf4 !important;
        border-radius: 8px !important;
        padding: 6px 10px !important;
        margin-top: 6px !important;
        color: #14532d !important;
        font-size: 13.5px !important;
        line-height: 19px !important;
    }}

    .inapp-paper-booklet {{
        background: #FDFBF7;
        color: #1E293B;
        border: 2px solid {active_theme['accent']};
        border-radius: 16px;
        padding: 18px 22px;
        margin: 10px 0;
        box-shadow: 0 12px 30px rgba(0,0,0,0.5);
    }}
</style>
"""
st.markdown(IOS_DYNAMIC_CSS, unsafe_allow_html=True)

# ================= SIDEBAR & AI ENGINE CONFIG =================
with st.sidebar:
    st.subheader("⚡ AI Engine & System")
    ai_choice = st.radio("Active Engine:", ["⚡ Groq LPU (Ultra Fast)", "Google Gemini"], index=0)

    if ai_choice == "⚡ Groq LPU (Ultra Fast)":
        if not groq_key:
            groq_key = st.text_input("Groq API Key:", type="password", placeholder="gsk_...")
        if groq_key:
            st.success("● Groq LPU Active")
        else:
            st.warning("⚠️ Sidebar mein Groq API Key daalein")
    else:
        if not gemini_key:
            gemini_key = st.text_input("Gemini API Key:", type="password")
        if gemini_key:
            genai.configure(api_key=gemini_key)
            st.success("● Gemini Multimodal Active")

    st.divider()
    st.subheader("📧 Auto-Email SMTP Status")
    if gmail_app_password:
        st.success(f"● Auto-SMTP Connected ({ADMIN_EMAIL})")
    else:
        manual_pwd = st.text_input("Gmail App Password (16-digit):", type="password", placeholder="xxxx xxxx xxxx xxxx")
        if manual_pwd:
            st.session_state["manual_gmail_pwd"] = manual_pwd
            st.success("● Auto-SMTP Active")

    if st.button("⭐ Rate & Give Feedback", key="sidebar_fb_btn", use_container_width=True):
        open_feedback_popup_dialog()
    st.caption(f"📧 Contact: **{ADMIN_EMAIL}**")
    st.caption("⚡ Developer: **Harsh Raj Soni**")

# ================= DYNAMIC MODEL AUTO-DISCOVERY ENGINE =================
def get_working_groq_models(client):
    preferred = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "gemma2-9b-it",
        "llama3-70b-8192",
        "llama3-8b-8192",
        "mixtral-8x7b-32768",
        "qwen-qwq-32b"
    ]
    try:
        live_list = [
            m.id for m in client.models.list().data
            if not any(skip in m.id.lower() for skip in ["whisper", "tts", "guard", "vision", "embed", "playai"])
        ]
        if not live_list:
            return preferred
        ordered = [m for m in preferred if m in live_list]
        for m in live_list:
            if m not in ordered:
                ordered.append(m)
        return ordered
    except Exception:
        return preferred

def execute_ai_query(system_role, user_prompt, max_budget=2600, image_input=None):
    safe_tokens = min(max_budget, 3200)

    if image_input and gemini_key:
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("models/gemini-2.0-flash")
            response = model.generate_content([system_role + "\n\n" + user_prompt, image_input])
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            return "API_ERROR: Gemini Vision Error: " + str(e)

    if "Groq" in ai_choice and groq_key:
        client = Groq(api_key=groq_key)
        candidate_models = get_working_groq_models(client)
        last_err = ""
        for model_id in candidate_models:
            try:
                completion = client.chat.completions.create(
                    model=model_id,
                    messages=[
                        {"role": "system", "content": system_role},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.25,
                    max_tokens=safe_tokens
                )
                res_text = completion.choices[0].message.content.strip()
                if res_text:
                    res_text = re.sub(r"<think>.*?</think>", "", res_text, flags=re.DOTALL).strip()
                    return res_text
            except Exception as e:
                last_err = str(e)
                continue

        if gemini_key:
            try:
                genai.configure(api_key=gemini_key)
                model = genai.GenerativeModel("models/gemini-2.0-flash")
                res = model.generate_content(system_role + "\n\n" + user_prompt)
                if res and res.text:
                    return res.text.strip()
            except Exception:
                pass
        return "API_ERROR: " + str(last_err)

    elif gemini_key:
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("models/gemini-2.0-flash")
            response = model.generate_content(system_role + "\n\n" + user_prompt)
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            return "API_ERROR: " + str(e)

    return "API_ERROR: Pehle left sidebar khol kar apni Groq ya Gemini API Key enter karein."

# ================= TABLE CELL TRIMMER (PREVENTS RUNAWAY NUMBER LISTS) =================
def sanitize_sheet_html(html_str):
    # Trim any runaway long text inside <td>...</td> to max 95 characters so table never stretches
    def trim_td(match):
        content = match.group(1).strip()
        if len(content) > 95:
            content = content[:90].rsplit(" ", 1)[0] + " etc."
        return f"<td>{content}</td>"

    html_str = re.sub(r"<td>(.*?)</td>", trim_td, html_str, flags=re.DOTALL)
    open_divs = html_str.count("<div")
    close_divs = html_str.count("</div>")
    if open_divs > close_divs:
        html_str += "</div>" * (open_divs - close_divs)
    if "<table" in html_str and "</table" not in html_str:
        html_str += "</table>"
    return html_str

def generate_multi_sheets_html(topic, subject_name, course_name, notes_lang):
    last_ai_ctx = st.session_state.ai_memory.get(course_name, {}).get("last_summary", "Fresh session.")

    system_role = (
        f"You are an elite professor for {course_name} ({subject_name}). "
        f"Student Memory: {last_ai_ctx}. "
        "Output EXACTLY 3 COMPACT LECTURE SHEETS separated strictly by '===SHEET_SPLIT==='. "
        "STRICT TABLE RULE: Every <td> cell in the table MUST contain AT MOST 6 to 10 words! "
        "NEVER list more than 3 article or section numbers in a table cell (e.g. write 'Art 15, 19, 21 etc.' — NEVER dump 50 numbers!). "
        "Keep each sheet crisp (under 90 words total) so it looks like a neat single notebook card. "
        "Start each sheet directly with <div class='register-outer-center'>."
    )
    user_prompt = (
        f"Create 3 neat single-page lecture sheets for '{topic}' in {subject_name} ({notes_lang}).\n"
        "Separate sheets strictly with ===SHEET_SPLIT===.\n\n"
        "TEMPLATE FOR EACH SHEET:\n"
        "<div class=\"register-outer-center\">\n"
        "    <div class=\"real-notebook-sheet\">\n"
        "        <div class=\"nb-title-h1\">" + topic + " [Page X]</div>\n"
        "        <div style=\"font-size:11px; color:#64748b; margin-bottom:4px;\">" + course_name + " • " + subject_name + "</div>\n"
        "        <span class=\"nb-subhead\">1. Core Concept :</span>\n"
        "        <p style=\"margin: 2px 0 4px 0;\">[1-2 clear sentences in " + notes_lang + "]</p>\n"
        "        <span class=\"nb-subhead\">2. Key Matrix (Max 8 words per cell) :</span>\n"
        "        <div class=\"table-container\">\n"
        "            <table class=\"nb-table\">\n"
        "                <tr><th>Category</th><th>Rule / Section</th><th>Key Example</th></tr>\n"
        "                <tr><td>Type 1</td><td>Simple / Sec A</td><td>2-3 examples only</td></tr>\n"
        "                <tr><td>Type 2</td><td>Special / Sec B</td><td>2-3 examples only</td></tr>\n"
        "            </table>\n"
        "        </div>\n"
        "        <span class=\"nb-subhead\">3. Essential Points :</span>\n"
        "        <p style=\"margin: 2px 0 4px 0;\">\n"
        "            • Point 1: Crisp working step or legal ingredient<br>\n"
        "            • Point 2: Practical application / case law\n"
        "        </p>\n"
        "        <div class=\"nb-keypoints-box\">\n"
        "            <b>✳ Golden Exam Trick :</b><br>\n"
        "            • 1 high-yield exam takeaway or shortcut\n"
        "        </div>\n"
        "    </div>\n"
        "</div>"
    )
    raw_res = execute_ai_query(system_role, user_prompt, max_budget=2000)
    if raw_res.startswith("API_ERROR:"):
        st.error(raw_res)
        return []

    clean_text = raw_res.replace("```html", "").replace("```HTML", "").replace("```", "").strip()
    clean_text = re.sub(r"^`+|`+$", "", clean_text)

    raw_sheets = [s.strip() for s in clean_text.split("===SHEET_SPLIT===") if s.strip()]

    if len(raw_sheets) == 1:
        if clean_text.count('class="register-outer-center"') > 1:
            parts = re.split(r'(?=<div\s+class=["\']register-outer-center["\']\s*>)', clean_text)
            raw_sheets = [p.strip() for p in parts if p.strip()]
        elif clean_text.count('class="real-notebook-sheet"') > 1:
            parts = re.split(r'(?=<div\s+class=["\']real-notebook-sheet["\']\s*>)', clean_text)
            raw_sheets = [f'<div class="register-outer-center">{p.strip()}</div>' for p in parts if p.strip() and "real-notebook-sheet" in p]

    sanitized_sheets = [sanitize_sheet_html(s) for s in raw_sheets]

    if course_name not in st.session_state.ai_memory:
        st.session_state.ai_memory[course_name] = {}
    st.session_state.ai_memory[course_name]["last_topic"] = topic
    st.session_state.ai_memory[course_name]["last_summary"] = f"Studied {topic} in {subject_name}"
    save_user_memory()

    return sanitized_sheets if sanitized_sheets else [sanitize_sheet_html(clean_text)]

# ================= 3D FLASHCARDS & MNEMONICS GENERATOR (NEW STUDENT ADDICTION!) =================
def generate_3d_flashcards(topic, subject_name, course_name):
    sys_p = (
        f"You are a memory coach for {course_name}. Generate 6 high-yield active-recall flashcards for '{topic}' ({subject_name}). "
        "Use ONLY this strict format for each card:\n"
        "===CARD===\n"
        "FRONT: [Short Question, Section Number, Formula Name, or Term - max 12 words]\n"
        "BACK: [Crisp Answer, Trick, Case Law, or Formula - max 22 words]\n"
        "===END==="
    )
    raw = execute_ai_query(sys_p, f"Create 6 flashcards for {topic}", max_budget=1500)
    cards = []
    for blk in raw.split("===CARD==="):
        blk = blk.split("===END===")[0].strip()
        f_m = re.search(r"FRONT:\s*(.+)", blk)
        b_m = re.search(r"BACK:\s*(.+)", blk, re.DOTALL)
        if f_m and b_m:
            cards.append({
                "front": f_m.group(1).strip(),
                "back": b_m.group(1).strip()
            })
    return cards

# ================= BULLETPROOF MCQ BLOCK PARSER =================
def parse_mcq_blocks(raw_text, default_tag="Official Set"):
    if not raw_text or raw_text.startswith("API_ERROR:"):
        return []

    questions = []
    blocks = raw_text.split("===Q_START===")
    for blk in blocks:
        blk = blk.split("===Q_END===")[0].strip()
        if not blk or ("Q:" not in blk and "A:" not in blk):
            continue

        tag_m = re.search(r"TAG:\s*(.+)", blk)
        q_m = re.search(r"Q:\s*(.+?)(?=\n\s*A:|\nA:)", blk, re.DOTALL)
        a_m = re.search(r"(?:^|\n)\s*A:\s*(.+)", blk)
        b_m = re.search(r"(?:^|\n)\s*B:\s*(.+)", blk)
        c_m = re.search(r"(?:^|\n)\s*C:\s*(.+)", blk)
        d_m = re.search(r"(?:^|\n)\s*D:\s*(.+)", blk)
        ans_m = re.search(r"(?:^|\n)\s*ANS:\s*([A-Da-d])", blk)
        exp_m = re.search(r"(?:^|\n)\s*EXP:\s*(.+)", blk, re.DOTALL)

        if q_m and a_m and b_m and c_m and d_m:
            q_txt = q_m.group(1).strip()
            opt_a = "A. " + re.sub(r"^[A-Da-d][\.\)]\s*", "", a_m.group(1).strip())
            opt_b = "B. " + re.sub(r"^[A-Da-d][\.\)]\s*", "", b_m.group(1).strip())
            opt_c = "C. " + re.sub(r"^[A-Da-d][\.\)]\s*", "", c_m.group(1).strip())
            opt_d = "D. " + re.sub(r"^[A-Da-d][\.\)]\s*", "", d_m.group(1).strip())
            opts = [opt_a, opt_b, opt_c, opt_d]

            ans_letter = ans_m.group(1).upper() if ans_m else "A"
            ans_map = {"A": opt_a, "B": opt_b, "C": opt_c, "D": opt_d}
            correct_opt = ans_map.get(ans_letter, opt_a)

            exp_txt = exp_m.group(1).strip() if exp_m else "Standard statutory / conceptual rule applies."
            tag_txt = tag_m.group(1).strip() if tag_m else default_tag

            questions.append({
                "q_no": len(questions) + 1,
                "year_tag": tag_txt,
                "question": q_txt,
                "options": opts,
                "correct_option": correct_opt,
                "explanation": exp_txt
            })

    return questions

def generate_batch_questions(topic, course_name, subject_name, count=15, batch_num=1, is_pyq=False, pyq_year=""):
    law_context = ""
    if "Law" in course_name:
        law_context = "Include exact Indian Bare Act Section numbers (BNS/BNSS/BSA 2023 & IPC/CrPC), Articles, and Landmark SC judgments."

    if is_pyq:
        tag_label = pyq_year
        mode_desc = f"STRICTLY OUTPUT REAL VERBATIM QUESTIONS FROM OFFICIAL {pyq_year} ({course_name}). {law_context}"
    else:
        tag_label = f"DPP Batch-{batch_num}"
        sub_focus = [
            "Core Concepts, Direct Sections & Formulas",
            "Practical Case / Numerical Application",
            "Assertion-Reason & Statement Analysis",
            "Landmark Cases / NCERT Exceptions",
            "Rank-Decider Tricky Questions"
        ][(batch_num - 1) % 5]
        mode_desc = f"Focus: {sub_focus}. {law_context}"

    sys_prompt = (
        f"You are Chief Examiner for {course_name}. Generate EXACTLY {count} MCQs using ONLY this block format:\n\n"
        "===Q_START===\n"
        f"TAG: {tag_label}\n"
        "Q: [Concise question statement]\n"
        "A: [Option A]\n"
        "B: [Option B]\n"
        "C: [Option C]\n"
        "D: [Option D]\n"
        "ANS: [Single letter A, B, C, or D]\n"
        "EXP: [1-line explanation]\n"
        "===Q_END==="
    )

    user_prompt = f"Output {count} MCQs for '{topic}' in {subject_name} ({course_name}). {mode_desc}"
    raw_res = execute_ai_query(sys_prompt, user_prompt, max_budget=3000)
    if raw_res.startswith("API_ERROR:"):
        st.error(raw_res)
        return []

    return parse_mcq_blocks(raw_res, default_tag=tag_label)

def generate_90_100_dpp_marathon(topic, course_name, subject_name, target_count=90):
    all_questions = []
    batch_size = 15
    total_batches = (target_count + batch_size - 1) // batch_size

    progress_bar = st.progress(0, text=f"Initializing {target_count}-Question DPP Engine...")
    status_box = st.empty()

    for b in range(1, total_batches + 1):
        status_box.info(f"⚡ Compiling DPP Batch {b} of {total_batches} ({len(all_questions)}/{target_count} Ready)...")
        batch_qs = generate_batch_questions(
            topic, course_name, subject_name, count=batch_size, batch_num=b, is_pyq=False
        )
        if batch_qs:
            for q in batch_qs:
                q["q_no"] = len(all_questions) + 1
                all_questions.append(q)
        else:
            break
        progress_bar.progress(min(b / total_batches, 1.0), text=f"Loaded {len(all_questions)} Questions...")

    progress_bar.empty()
    status_box.empty()
    return all_questions

# ================= 0. iOS VISION-OS LAUNCH SCREEN =================
if not st.session_state.system_booted:
    st.markdown(f"""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:70vh; text-align:center;">
        <div class="ios-dynamic-island" style="max-width:460px; justify-content:center; margin-bottom:20px;">
            <span style="font-size:13px; font-weight:700; color:{active_theme['accent']};">✨ iOS 18 Dynamic Academic Ecosystem</span>
        </div>
        <div style="font-size:38px; font-weight:800; color:#FFFFFF; letter-spacing:-0.8px; margin-bottom:8px;">
            Harsh's Lex & Tech Suite
        </div>
        <div style="font-size:15px; color:#CBD5E1; margin-bottom:26px;">
            ⚖️ Law • 🩺 NEET • ⚙️ JEE • 💻 BCA • 🏛️ UPSC — Designed by <b>Harsh Raj Soni</b>
        </div>
        <div class="ios-glass-card" style="max-width:580px; width:100%; text-align:left; font-size:13.5px; color:#E2E8F0; line-height:1.7; margin-bottom:26px;">
            <div style="color:{active_theme['accent']}; font-weight:700; font-size:14.5px; margin-bottom:6px;">🚀 What's New in iOS Dynamic Edition:</div>
            <div>• 🎨 <b>iOS 18 Aurora Mesh Background</b> & Buttery Spring Animations</div>
            <div>• 🃏 <b>3D Interactive Flip Flashcards</b> & Instant Desi Mnemonics Generator</div>
            <div>• 📄 <b>Fixed Balanced Notebook Tables</b> (Zero Column Squishing)</div>
            <div>• 🔥 <b>Gamified XP, Rank Levels & Daily Study Streak</b> in Dynamic Island</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        if st.button("🚀 Launch iOS Learning Suite", use_container_width=True):
            st.session_state.system_booted = True
            st.rerun()

else:
    if st.session_state.trigger_feedback_modal and not st.session_state.feedback_popup_shown:
        st.session_state.trigger_feedback_modal = False
        open_feedback_popup_dialog()

    # ================= iOS DYNAMIC ISLAND TOP BAR =================
    student_xp = st.session_state.get("xp_points", 120)
    student_rank = get_student_rank(student_xp)
    streak = st.session_state.get("streak_days", 3)

    isl_c1, isl_c2 = st.columns([4.2, 1])
    with isl_c1:
        st.markdown(f"""
        <div class="ios-dynamic-island">
            <div style="display:flex; align-items:center; gap:10px;">
                <span style="height:10px; width:10px; background:{active_theme['accent']}; border-radius:50%; display:inline-block; box-shadow:0 0 10px {active_theme['accent']};"></span>
                <span style="font-size:16px; font-weight:800; color:#FFFFFF;">Harsh's Lex & Tech Suite</span>
            </div>
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                <span class="island-badge">🔥 {streak} Day Streak</span>
                <span class="island-badge">⚡ {student_xp} XP • {student_rank}</span>
                <span class="island-badge">👨‍💻 Harsh Raj Soni</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with isl_c2:
        st.write("")
        if st.button("⭐ Rate App", key="top_rate_btn", use_container_width=True):
            open_feedback_popup_dialog()

    # ================= SUPER SIMPLE & CLEAR COURSE + SUBJECT SELECTOR BAR =================
    course_list = list(COURSE_DATABASE.keys())
    if st.session_state.current_course not in course_list:
        st.session_state.current_course = course_list[0]

    sel_c1, sel_c2 = st.columns([1, 1.2])
    with sel_c1:
        chosen_course = st.selectbox(
            "🎓 1. Select Course:",
            options=course_list,
            index=course_list.index(st.session_state.current_course)
        )
        if chosen_course != st.session_state.current_course:
            st.session_state.current_course = chosen_course
            st.session_state.current_subject = list(COURSE_DATABASE[chosen_course]["subjects"].keys())[0]
            st.session_state.generated_gallery_sheets = []
            st.session_state.flashcards_data = []
            st.session_state.dpp_questions = []
            st.session_state.pyq_questions = []
            save_user_memory()
            st.rerun()

    active_course_data = COURSE_DATABASE[st.session_state.current_course]
    available_subjects = list(active_course_data["subjects"].keys())
    if st.session_state.current_subject not in available_subjects:
        st.session_state.current_subject = available_subjects[0]

    with sel_c2:
        chosen_subj = st.selectbox(
            "📚 2. Select Subject:",
            options=available_subjects,
            index=available_subjects.index(st.session_state.current_subject)
        )
        if chosen_subj != st.session_state.current_subject:
            st.session_state.current_subject = chosen_subj
            st.session_state.generated_gallery_sheets = []
            st.session_state.flashcards_data = []
            st.session_state.dpp_questions = []
            st.session_state.pyq_questions = []
            save_user_memory()
            st.rerun()

    active_course = st.session_state.current_course
    active_subj = st.session_state.current_subject
    subject_details = active_course_data["subjects"][active_subj]

    # ================= iOS SEGMENTED NAVIGATION DOCK =================
    ref_tab_label = "⚖️ Bare Acts" if "Law" in active_course else "🔬 Formulas"
    nav_options = [
        "📝 Notes",
        "🃏 3D Flashcards",
        "🔥 DPP (90-100 Qs)",
        "📚 PYQs Vault",
        "🎯 Mock Test",
        ref_tab_label,
        "🤖 AI Mentor",
        "📖 Syllabus",
        "⭐ Feedback"
    ]
    if "Python" in active_subj or "BCA" in active_course:
        nav_options.append("💻 Code Lab")

    selected_nav = st.radio(
        label="Navigation Dock",
        options=nav_options,
        horizontal=True,
        index=0,
        label_visibility="collapsed"
    )

    # ================= SECTION 1: FIXED BALANCED NOTES GALLERY =================
    if selected_nav == "📝 Notes":
        st.markdown(f"""
        <div class="ios-glass-card" style="margin-bottom:12px;">
            <div style="font-size:18px; font-weight:800; color:#FFFFFF;">📖 Smart Handwritten Notes — {active_subj}</div>
            <div style="font-size:12.5px; color:#CBD5E1;">Balanced 3-column tables, zero squishing, aur single-screen notebook cards (+25 XP per topic).</div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns([2.6, 1])
        with c1:
            suggested = subject_details.get("topics", [])
            chosen_topic = st.selectbox("📌 Select Topic:", suggested)
            custom_topic = st.text_input("✨ Or Type Any Custom Topic:", placeholder="e.g. Article 368 Amendment / Section 103 BNS / Cardiac Cycle")
        with c2:
            notes_lang = st.selectbox("🌐 Language:", ["Hinglish", "English", "Hindi"])

        final_topic = custom_topic.strip() if custom_topic.strip() else chosen_topic

        if st.button("✨ Generate Smart Register Notes (+25 XP)", use_container_width=True):
            st.session_state.current_topic = final_topic
            st.session_state.active_sheet_index = 0
            add_student_xp(25)

            with st.spinner(f"Crafting balanced register cards for '{final_topic}'..."):
                sheets_out = generate_multi_sheets_html(
                    final_topic, active_subj, active_course_data["full_title"], notes_lang
                )
                if sheets_out:
                    st.session_state.generated_gallery_sheets = sheets_out
                    st.session_state.active_sheet_index = 0
                    if not st.session_state.feedback_popup_shown:
                        st.session_state.trigger_feedback_modal = True
                    st.rerun()

        if st.session_state.generated_gallery_sheets:
            sheets = st.session_state.generated_gallery_sheets
            total_sheets = len(sheets)

            if st.session_state.active_sheet_index is not None:
                cur_i = min(st.session_state.active_sheet_index, total_sheets - 1)
                nav_c1, nav_c2, nav_c3 = st.columns([1.2, 2, 1.2])
                with nav_c1:
                    if st.button("⬅️ Previous Page", disabled=(cur_i == 0), use_container_width=True):
                        st.session_state.active_sheet_index = max(0, cur_i - 1)
                        st.rerun()
                with nav_c2:
                    if st.button(f"🗂️ View All {total_sheets} Pages Grid (Page {cur_i + 1}/{total_sheets})", use_container_width=True):
                        st.session_state.active_sheet_index = None
                        st.rerun()
                with nav_c3:
                    if st.button("Next Page ➡️", disabled=(cur_i == total_sheets - 1), use_container_width=True):
                        st.session_state.active_sheet_index = min(total_sheets - 1, cur_i + 1)
                        st.rerun()

                st.html(sheets[cur_i])
            else:
                grid_cols = st.columns(3)
                for idx, _ in enumerate(sheets):
                    with grid_cols[idx % 3]:
                        st.markdown(f"""
                        <div class="ios-glass-card" style="text-align:center; margin-bottom:8px;">
                            <div style="font-size:15px; font-weight:800; color:{active_theme['accent']};">📄 Register Page #{idx + 1}</div>
                            <div style="font-size:11.5px; color:#CBD5E1; margin-top:4px;">{final_topic[:32]}...</div>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"Open Page #{idx + 1}", key=f"sheet_btn_{idx}", use_container_width=True):
                            st.session_state.active_sheet_index = idx
                            st.rerun()

    # ================= SECTION 2: 3D INTERACTIVE FLIP FLASHCARDS & MNEMONICS (NEW!) =================
    elif selected_nav == "🃏 3D Flashcards":
        st.markdown(f"""
        <div class="ios-glass-card" style="margin-bottom:12px;">
            <div style="font-size:18px; font-weight:800; color:#FFFFFF;">🃏 3D Active-Recall Flashcards & Desi Mnemonics — {active_subj}</div>
            <div style="font-size:12.5px; color:#CBD5E1;">Kisi bhi card par hover ya tap karein 3D mein flip karke answer dekhne ke liye!</div>
        </div>
        """, unsafe_allow_html=True)

        fc_c1, fc_c2 = st.columns([2, 1])
        with fc_c1:
            fc_topic = st.selectbox("Select Topic for Flashcards & Tricks:", subject_details.get("topics", []))
        with fc_c2:
            st.write("")
            if st.button("⚡ Generate 3D Flashcards (+30 XP)", use_container_width=True):
                add_student_xp(30)
                with st.spinner("Building 3D Interactive Flashcards & Mnemonics..."):
                    st.session_state.flashcards_data = generate_3d_flashcards(fc_topic, active_subj, active_course)
                    mnem_prompt = f"Create 2 funny, super-memorable Desi Hinglish Mnemonics / Short Tricks to memorize '{fc_topic}' ({active_subj}) in 4 crisp bullet lines."
                    st.session_state.cheatsheet_html = execute_ai_query("You are an exam memory wizard.", mnem_prompt, max_budget=600)
                st.rerun()

        if st.session_state.flashcards_data:
            cards_html = '<div class="flip-card-grid">'
            for i, c in enumerate(st.session_state.flashcards_data):
                cards_html += f"""
                <div class="flip-card">
                    <div class="flip-card-inner">
                        <div class="flip-card-front">
                            <div style="font-size:11px; font-weight:700; color:{active_theme['accent']}; text-transform:uppercase; letter-spacing:1px; margin-bottom:6px;">Flashcard #{i+1} • Tap/Hover to Flip ↻</div>
                            <div style="font-size:15px; font-weight:700; line-height:1.4;">{c['front']}</div>
                        </div>
                        <div class="flip-card-back">
                            <div style="font-size:11px; font-weight:700; color:#FDE047; margin-bottom:6px;">✔ Answer & Key Trick</div>
                            <div style="font-size:13.5px; line-height:1.45;">{c['back']}</div>
                        </div>
                    </div>
                </div>
                """
            cards_html += "</div>"
            st.markdown(cards_html, unsafe_allow_html=True)

        if st.session_state.cheatsheet_html:
            st.markdown(f"""
            <div class="ios-glass-card" style="margin-top:10px; border-left:5px solid {active_theme['accent']};">
                <div style="font-size:15px; font-weight:800; color:{active_theme['accent']}; margin-bottom:6px;">🧠 Instant Desi Mnemonics & Memory Hacks</div>
            </div>
            """, unsafe_allow_html=True)
            st.info(st.session_state.cheatsheet_html)

    # ================= SECTION 3: DPP (90-100 QUESTIONS MARATHON ENGINE) =================
    elif selected_nav == "🔥 DPP (90-100 Qs)":
        st.markdown(f"""
        <div class="ios-glass-card" style="margin-bottom:12px;">
            <div style="font-size:18px; font-weight:800; color:#FFFFFF;">🔥 Daily Practice Problems (DPP Marathon) — {active_subj}</div>
            <div style="font-size:12.5px; color:#CBD5E1;">Compact paginated OMR view — 3 ya 5 questions per screen.</div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            dpp_topic_list = subject_details.get("topics", [])
            sel_dpp_topic = st.selectbox("Select Chapter:", dpp_topic_list)
            custom_dpp = st.text_input("Or Custom Chapter:", placeholder="e.g. Complete BNS 2023 / Rotational Motion")
        with c2:
            dpp_target_count = st.selectbox("Total Questions:", [90, 100, 45, 15], index=3)
        with c3:
            page_size = st.selectbox("Qs Per Screen:", [3, 5, 10], index=0)

        final_dpp_topic = custom_dpp.strip() if custom_dpp.strip() else sel_dpp_topic

        col_btn1, col_btn2 = st.columns([2, 1])
        with col_btn1:
            if st.button(f"🚀 Generate {dpp_target_count}-Question DPP (+40 XP)", use_container_width=True):
                st.session_state.current_topic = final_dpp_topic
                add_student_xp(40)
                qs = generate_90_100_dpp_marathon(
                    final_dpp_topic, active_course_data["full_title"], active_subj, target_count=dpp_target_count
                )
                if qs:
                    st.session_state.dpp_questions = qs
                    st.session_state.dpp_user_answers = {}
                    st.session_state.dpp_submitted = False
                    st.session_state.dpp_page = 0
                    st.rerun()
        with col_btn2:
            if st.session_state.dpp_questions:
                if st.button("➕ Add 15 More Qs", use_container_width=True):
                    with st.spinner("Appending 15 more questions..."):
                        extra = generate_batch_questions(
                            final_dpp_topic, active_course_data["full_title"], active_subj, count=15,
                            batch_num=(len(st.session_state.dpp_questions) // 15) + 1
                        )
                        for q in extra:
                            q["q_no"] = len(st.session_state.dpp_questions) + 1
                            st.session_state.dpp_questions.append(q)
                        st.rerun()

        if st.session_state.dpp_questions:
            dpp_list = st.session_state.dpp_questions
            total_dpp = len(dpp_list)
            total_pages = max(1, (total_dpp + page_size - 1) // page_size)
            cur_page = min(st.session_state.dpp_page, total_pages - 1)

            start_idx = cur_page * page_size
            end_idx = min(start_idx + page_size, total_dpp)

            answered_count = len([v for v in st.session_state.dpp_user_answers.values() if v is not None])

            p_c1, p_c2, p_c3 = st.columns([1.2, 2.2, 1.2])
            with p_c1:
                if st.button("⬅️ Prev Page", disabled=(cur_page == 0), key="dpp_prev_top", use_container_width=True):
                    st.session_state.dpp_page = max(0, cur_page - 1)
                    st.rerun()
            with p_c2:
                st.markdown(f"<div style='text-align:center; padding-top:6px; font-size:13px;'><b>Page {cur_page + 1}/{total_pages}</b> (Qs {start_idx + 1}–{end_idx} of {total_dpp}) • Ticked: {answered_count}</div>", unsafe_allow_html=True)
            with p_c3:
                if st.button("Next Page ➡️", disabled=(cur_page >= total_pages - 1), key="dpp_next_top", use_container_width=True):
                    st.session_state.dpp_page = min(total_pages - 1, cur_page + 1)
                    st.rerun()

            for idx in range(start_idx, end_idx):
                q_data = dpp_list[idx]
                q_num = idx + 1
                st.markdown(f"""
                <div class="question-card">
                    <div class="question-header">
                        <span class="q-number-tag">DPP Q.{q_num} • {q_data.get('year_tag', 'Core DPP')}</span>
                        <span class="q-marks-tag">+4 / -1 OMR</span>
                    </div>
                    <div class="q-text">{q_data.get('question', '')}</div>
                </div>
                """, unsafe_allow_html=True)

                opts = q_data.get("options", [])
                prev_choice = st.session_state.dpp_user_answers.get(idx, None)
                opt_index = opts.index(prev_choice) if prev_choice in opts else None

                chosen = st.radio(
                    f"Tick Option for Q.{q_num}:",
                    options=opts,
                    index=opt_index,
                    key=f"dpp_radio_{idx}"
                )
                st.session_state.dpp_user_answers[idx] = chosen

                if st.session_state.dpp_submitted:
                    correct = q_data.get("correct_option", "")
                    if chosen == correct:
                        st.success(f"✔ **Correct!** ({correct}) — {q_data.get('explanation', '')}")
                    else:
                        st.error(f"✖ **Key:** {correct} | **Exp:** {q_data.get('explanation', '')}")

            if st.button("📝 Submit DPP & Calculate Rank Score (+50 XP)", type="primary", use_container_width=True):
                st.session_state.dpp_submitted = True
                add_student_xp(50)
                if not st.session_state.feedback_popup_shown:
                    st.session_state.trigger_feedback_modal = True
                st.rerun()

            if st.session_state.dpp_submitted:
                correct_cnt = sum(1 for i, q in enumerate(dpp_list) if st.session_state.dpp_user_answers.get(i) == q.get("correct_option"))
                wrong_cnt = sum(1 for i, q in enumerate(dpp_list) if st.session_state.dpp_user_answers.get(i) and st.session_state.dpp_user_answers.get(i) != q.get("correct_option"))
                unattempted = total_dpp - (correct_cnt + wrong_cnt)
                total_marks = (correct_cnt * 4) - (wrong_cnt * 1)
                st.info(f"📊 **DPP Score:** {total_marks} / {total_dpp * 4}  |  ✔ Correct: {correct_cnt}  |  ✖ Wrong: {wrong_cnt}  |  ⚪ Left: {unattempted}")

    # ================= SECTION 4: IN-APP PYQS VAULT =================
    elif selected_nav == "📚 PYQs Vault":
        st.markdown(f"""
        <div class="ios-glass-card" style="margin-bottom:12px;">
            <div style="font-size:18px; font-weight:800; color:#FFFFFF;">📚 Official Past Question Papers (In-App OMR & Booklet) — {active_subj}</div>
            <div style="font-size:12.5px; color:#CBD5E1;">Bina kisi external website par gaye seedhe app mein official PYQ papers solve karein.</div>
        </div>
        """, unsafe_allow_html=True)

        pyqs_list = subject_details.get("pyqs_years", ["2024 Official Paper"])
        c1, c2, c3, c4 = st.columns([2, 0.9, 0.9, 1.2])
        with c1:
            chosen_year = st.selectbox("Select Exam Paper:", pyqs_list)
        with c2:
            pyq_count = st.selectbox("Paper Qs:", [15, 30, 45], index=0)
        with c3:
            pyq_per_page = st.selectbox("Qs / Page:", [3, 5, 10], index=0)
        with c4:
            pyq_view_mode = st.selectbox("Mode:", ["📝 OMR Mode", "📄 Booklet Mode"])

        if st.button(f"📖 Open {chosen_year} Inside App (+30 XP)", use_container_width=True):
            add_student_xp(30)
            all_pyqs = []
            batch_sz = 15
            batches = (pyq_count + batch_sz - 1) // batch_sz
            prog = st.progress(0, text=f"Loading {chosen_year}...")
            for b in range(1, batches + 1):
                need = min(batch_sz, pyq_count - len(all_pyqs))
                if need <= 0:
                    break
                chunk = generate_batch_questions(
                    f"Full {active_subj}", active_course_data["full_title"], active_subj,
                    count=need, batch_num=b, is_pyq=True, pyq_year=chosen_year
                )
                if chunk:
                    for q in chunk:
                        q["q_no"] = len(all_pyqs) + 1
                        all_pyqs.append(q)
                else:
                    break
                prog.progress(min(b / batches, 1.0))
            prog.empty()
            if all_pyqs:
                st.session_state.pyq_questions = all_pyqs
                st.session_state.pyq_user_answers = {}
                st.session_state.pyq_submitted = False
                st.session_state.pyq_page = 0
                st.rerun()

        if st.session_state.pyq_questions:
            q_list = st.session_state.pyq_questions
            total_q = len(q_list)
            tot_pyq_pages = max(1, (total_q + pyq_per_page - 1) // pyq_per_page)
            cur_p = min(st.session_state.pyq_page, tot_pyq_pages - 1)
            s_i = cur_p * pyq_per_page
            e_i = min(s_i + pyq_per_page, total_q)

            nav1, nav2, nav3 = st.columns([1.2, 2.2, 1.2])
            with nav1:
                if st.button("⬅️ Prev Page", disabled=(cur_p == 0), key="pyq_p_prev", use_container_width=True):
                    st.session_state.pyq_page = max(0, cur_p - 1)
                    st.rerun()
            with nav2:
                st.markdown(f"<div style='text-align:center; padding-top:6px; font-size:13px;'><b>{chosen_year} — Page {cur_p + 1}/{tot_pyq_pages}</b> (Q.{s_i + 1}–{e_i})</div>", unsafe_allow_html=True)
            with nav3:
                if st.button("Next Page ➡️", disabled=(cur_p >= tot_pyq_pages - 1), key="pyq_p_next", use_container_width=True):
                    st.session_state.pyq_page = min(tot_pyq_pages - 1, cur_p + 1)
                    st.rerun()

            if pyq_view_mode == "📄 Booklet Mode":
                booklet_html = f'<div class="inapp-paper-booklet"><h4 style="margin:0 0 10px 0; color:#0F172A;">{chosen_year} — Official Booklet</h4>'
                for idx in range(s_i, e_i):
                    q_data = q_list[idx]
                    opts_html = "".join([f"<div style='margin:2px 0 2px 12px; font-size:13.5px;'>{o}</div>" for o in q_data.get("options", [])])
                    booklet_html += f"""
                    <div style="border-bottom:1px dashed #CBD5E1; padding:8px 0; color:#0F172A;">
                        <div style="font-size:14.5px; font-weight:700;">Q.{idx + 1}: {q_data.get('question', '')}</div>
                        {opts_html}
                        <details style="margin-top:5px; background:#F1F5F9; padding:4px 10px; border-radius:6px; font-size:12.5px; cursor:pointer;">
                            <summary style="font-weight:700; color:#0284C7;">✔ View Answer Key</summary>
                            <div><b>Key:</b> {q_data.get('correct_option', '')} — {q_data.get('explanation', '')}</div>
                        </details>
                    </div>
                    """
                booklet_html += "</div>"
                st.markdown(booklet_html, unsafe_allow_html=True)
            else:
                for idx in range(s_i, e_i):
                    q_data = q_list[idx]
                    q_num = idx + 1
                    st.markdown(f"""
                    <div class="question-card">
                        <div class="question-header">
                            <span class="q-number-tag">Q.{q_num} • {q_data.get('year_tag', chosen_year)}</span>
                            <span class="q-marks-tag">+4 / -1</span>
                        </div>
                        <div class="q-text">{q_data.get('question', '')}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    opts = q_data.get("options", [])
                    prev_ans = st.session_state.pyq_user_answers.get(idx, None)
                    opt_i = opts.index(prev_ans) if prev_ans in opts else None

                    sel_ans = st.radio(f"Tick OMR #{q_num}:", options=opts, index=opt_i, key=f"pyq_radio_{idx}")
                    st.session_state.pyq_user_answers[idx] = sel_ans

                    if st.session_state.pyq_submitted:
                        correct = q_data.get("correct_option", "")
                        if sel_ans == correct:
                            st.success(f"✔ **Correct!** ({correct}) — {q_data.get('explanation', '')}")
                        else:
                            st.error(f"✖ **Official Key:** {correct} — {q_data.get('explanation', '')}")

                if st.button("📝 Submit PYQ Paper & Check Score", type="primary", use_container_width=True):
                    st.session_state.pyq_submitted = True
                    add_student_xp(40)
                    st.rerun()

                if st.session_state.pyq_submitted:
                    correct_cnt = sum(1 for i, q in enumerate(q_list) if st.session_state.pyq_user_answers.get(i) == q.get("correct_option"))
                    wrong_cnt = sum(1 for i, q in enumerate(q_list) if st.session_state.pyq_user_answers.get(i) and st.session_state.pyq_user_answers.get(i) != q.get("correct_option"))
                    st.info(f"📊 **{chosen_year} Score:** {(correct_cnt * 4) - wrong_cnt} / {total_q * 4}  |  ✔ Correct: {correct_cnt}  |  ✖ Wrong: {wrong_cnt}")

    # ================= SECTION 5: MOCK TEST =================
    elif selected_nav == "🎯 Mock Test":
        st.markdown(f"""
        <div class="ios-glass-card" style="margin-bottom:12px;">
            <div style="font-size:18px; font-weight:800; color:#FFFFFF;">🎯 Rapid Mock Test — {active_subj}</div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns([2.2, 1, 1])
        with c1:
            exam_topic = st.text_input("Topic Scope:", value=st.session_state.current_topic if st.session_state.current_topic else active_subj)
        with c2:
            mock_q_cnt = st.selectbox("Questions:", [10, 15, 20], index=0)
        with c3:
            mock_per_page = st.selectbox("Qs / Page:", [3, 5, 10], index=0)

        if st.button("🚀 Start Mock Test (+25 XP)", use_container_width=True):
            add_student_xp(25)
            with st.spinner("Preparing Mock Paper..."):
                qs = generate_batch_questions(exam_topic, active_course_data["full_title"], active_subj, count=mock_q_cnt)
                if qs:
                    st.session_state.active_exam_questions = qs
                    st.session_state.exam_user_answers = {}
                    st.session_state.exam_submitted = False
                    st.session_state.mock_page = 0
                    st.rerun()

        if st.session_state.active_exam_questions:
            q_list = st.session_state.active_exam_questions
            tot_m = len(q_list)
            m_pages = max(1, (tot_m + mock_per_page - 1) // mock_per_page)
            cur_mp = min(st.session_state.mock_page, m_pages - 1)
            ms_i = cur_mp * mock_per_page
            me_i = min(ms_i + mock_per_page, tot_m)

            mc1, mc2, mc3 = st.columns([1.2, 2.2, 1.2])
            with mc1:
                if st.button("⬅️ Prev", disabled=(cur_mp == 0), key="m_prev", use_container_width=True):
                    st.session_state.mock_page = max(0, cur_mp - 1)
                    st.rerun()
            with mc2:
                st.markdown(f"<div style='text-align:center; padding-top:6px; font-size:13px;'><b>Page {cur_mp + 1}/{m_pages}</b></div>", unsafe_allow_html=True)
            with mc3:
                if st.button("Next ➡️", disabled=(cur_mp >= m_pages - 1), key="m_next", use_container_width=True):
                    st.session_state.mock_page = min(m_pages - 1, cur_mp + 1)
                    st.rerun()

            for idx in range(ms_i, me_i):
                q_data = q_list[idx]
                q_num = idx + 1
                st.markdown(f"""
                <div class="question-card">
                    <div class="question-header"><span class="q-number-tag">Question {q_num}</span><span class="q-marks-tag">+4 / -1</span></div>
                    <div class="q-text">{q_data.get('question', '')}</div>
                </div>
                """, unsafe_allow_html=True)
                opts = q_data.get("options", [])
                prev_m = st.session_state.exam_user_answers.get(idx, None)
                m_idx = opts.index(prev_m) if prev_m in opts else None
                sel_m = st.radio(f"Answer Q.{q_num}:", options=opts, key=f"mock_q_{idx}", index=m_idx)
                st.session_state.exam_user_answers[idx] = sel_m

                if st.session_state.exam_submitted:
                    correct = q_data.get("correct_option", "")
                    if sel_m == correct:
                        st.success(f"✔ **Correct!** ({correct}) — {q_data.get('explanation', '')}")
                    else:
                        st.error(f"✖ **Key:** {correct} — {q_data.get('explanation', '')}")

            if st.button("📝 Submit Mock Test", type="primary", use_container_width=True):
                st.session_state.exam_submitted = True
                st.rerun()

    # ================= SECTION 6: BARE ACTS & FORMULA LAB =================
    elif selected_nav == ref_tab_label:
        if "Law" in active_course:
            st.markdown("""
            <div class="ios-glass-card" style="margin-bottom:12px;">
                <div style="font-size:18px; font-weight:800; color:#FFFFFF;">⚖️ BNS 2023 vs IPC Section Mapper & Bare Act Reader</div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("⚔️ BNS/BNSS/BSA (2023) vs Old IPC/CrPC/IEA — Quick Chart", expanded=True):
                st.markdown("""
                * **Common Intention:** `Sec 3(5) BNS` ⬅️ *Sec 34 IPC*
                * **Private Defence:** `Sec 34–44 BNS` ⬅️ *Sec 96–106 IPC*
                * **Murder Punishment:** `Sec 103 BNS` ⬅️ *Sec 302 IPC*
                * **Organised Crime & Terrorism:** `Sec 111 & 113 BNS` *(New)*
                * **Zero FIR & e-FIR:** `Sec 173 BNSS` ⬅️ *Sec 154 CrPC*
                * **Maintenance of Wife/Parents:** `Sec 144 BNSS` ⬅️ *Sec 125 CrPC*
                * **Anticipatory Bail:** `Sec 482 BNSS` ⬅️ *Sec 438 CrPC*
                * **Electronic Records Evidence:** `Sec 61 & 63 BSA` ⬅️ *Sec 65B IEA*
                """)
            bare_query = st.text_input("🔍 Search Any Section, Article or Legal Maxim (e.g. 'Article 21', 'Section 103 BNS', 'Res Ipsa Loquitur'):")
            if st.button("Read Bare Act & Case Laws", use_container_width=True) and bare_query.strip():
                with st.spinner("Fetching statutory text..."):
                    st.info(execute_ai_query("You are an Indian Law Encyclopedia.", f"Explain concisely with landmark cases: {bare_query}", max_budget=1000))
        else:
            st.markdown(f"""
            <div class="ios-glass-card" style="margin-bottom:12px;">
                <div style="font-size:18px; font-weight:800; color:#FFFFFF;">🔬 High-Yield Formula Sheet — {active_subj}</div>
            </div>
            """, unsafe_allow_html=True)
            f_query = st.text_input("🔍 Type Chapter Name for Instant All-Formula Sheet:", value=active_subj)
            if st.button("⚡ Generate Chapter Formula Cheat-Sheet", use_container_width=True):
                with st.spinner("Generating formulas..."):
                    st.info(execute_ai_query("You are a senior entrance faculty.", f"Give a clean bulleted formula & shortcut sheet for {f_query}", max_budget=1200))

    # ================= SECTION 7: AI MENTOR =================
    elif selected_nav == "🤖 AI Mentor":
        st.markdown(f"""
        <div class="ios-glass-card" style="margin-bottom:12px;">
            <div style="font-size:18px; font-weight:800; color:#FFFFFF;">🤖 1-on-1 AI Personal Mentor — {active_subj}</div>
        </div>
        """, unsafe_allow_html=True)
        q = st.text_input("💬 Ask Any Doubt, Numerical, Case Law or Career Question:")
        q_img = st.file_uploader("📷 Upload Question Photo (Optional):", type=["png", "jpg", "jpeg"])
        pil_q = Image.open(q_img) if q_img else None

        if st.button("✨ Ask AI Mentor (+20 XP)", use_container_width=True):
            if q.strip() or pil_q:
                add_student_xp(20)
                with st.spinner("Mentor solving step-by-step..."):
                    ans = execute_ai_query(f"You are a friendly top faculty for {active_course} ({active_subj}). Explain clearly.", q, max_budget=1400, image_input=pil_q)
                    st.write(ans)

    # ================= SECTION 8: SYLLABUS =================
    elif selected_nav == "📖 Syllabus":
        st.markdown(f"""
        <div class="ios-glass-card" style="margin-bottom:12px;">
            <div style="font-size:18px; font-weight:800; color:#FFFFFF;">📖 Official Syllabus — {active_course_data['full_title']}</div>
            <div style="font-size:13.5px; color:#E2E8F0; margin-top:8px;"><b>{active_subj}:</b> {subject_details.get('units', '')}</div>
        </div>
        """, unsafe_allow_html=True)
        for s_k, s_v in active_course_data["subjects"].items():
            with st.expander(f"📌 {s_k} — Units & Topics", expanded=(s_k == active_subj)):
                st.write(s_v.get("units", ""))

    # ================= SECTION 9: FEEDBACK =================
    elif selected_nav == "⭐ Feedback":
        col_fb1, col_fb2 = st.columns([1.4, 1])
        with col_fb1:
            render_feedback_form_contents(context_key="main_tab")
        with col_fb2:
            st.markdown(f"""
            <div class="ios-glass-card">
                <div style="font-size:15px; font-weight:800; color:{active_theme['accent']};">📬 Developer Info</div>
                <div style="font-size:13.5px; color:#F8FAFC; margin-top:6px;"><b>Creator:</b> Harsh Raj Soni</div>
                <div style="font-size:13px; color:#CBD5E1; margin-top:2px;"><b>Email:</b> <code>{ADMIN_EMAIL}</code></div>
            </div>
            """, unsafe_allow_html=True)

    # ================= SECTION 10: PYTHON CODE LAB =================
    elif selected_nav == "💻 Code Lab":
        st.markdown("""
        <div class="ios-glass-card" style="margin-bottom:12px;">
            <div style="font-size:18px; font-weight:800; color:#FFFFFF;">💻 Interactive Python Code Lab</div>
        </div>
        """, unsafe_allow_html=True)
        tb1, tb2 = st.columns([1, 1])
        with tb1:
            if st.button("➕ Add Code Cell", use_container_width=True):
                st.session_state.notebook_cells.append({"id": len(st.session_state.notebook_cells) + 1, "code": "# Write Python code\n", "output": "", "error": ""})
                st.rerun()
        with tb2:
            if st.button("🧹 Clear Outputs", use_container_width=True):
                for cell in st.session_state.notebook_cells:
                    cell["output"], cell["error"] = "", ""
                st.rerun()

        for idx, cell in enumerate(st.session_state.notebook_cells):
            c_ed, c_act = st.columns([8.5, 1.5])
            with c_ed:
                cell["code"] = st.text_area(f"Cell {cell['id']}", value=cell["code"], height=105, label_visibility="collapsed")
            with c_act:
                run_btn = st.button("▶️ Run", key=f"run_{cell['id']}", use_container_width=True)
                assist_btn = st.button("✨ Fix", key=f"as_{cell['id']}", use_container_width=True)

            if run_btn:
                buf = io.StringIO()
                try:
                    with contextlib.redirect_stdout(buf):
                        exec(cell["code"], {})
                    cell["output"] = buf.getvalue() if buf.getvalue() else "[Executed successfully]"
                    cell["error"] = ""
                except Exception as ex:
                    cell["output"], cell["error"] = "", str(ex)
            if assist_btn:
                cell["output"] = execute_ai_query("Explain and optimize this Python code.", cell["code"], max_budget=900)
                cell["error"] = ""
            if cell["output"]:
                st.code(cell["output"])
            if cell["error"]:
                st.error(cell["error"])
