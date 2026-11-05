import streamlit as st
from groq import Groq
import google.generativeai as genai
import io
import re
import os
import shelve
import threading
import time
import urllib.parse
import contextlib
from PIL import Image

# ================= APP NAME & LOGO CONFIG =================
st.set_page_config(
    page_title="Harsh's Lex & Tech Suite",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

ADMIN_EMAIL = "harshrajsoni92@gmail.com"

# PERSISTENT STORAGE
STORAGE_FILE = "user_memory_store.db"

def load_user_memory():
    default_data = {
        "last_course": "⚖️ Law & Judiciary (LL.B / CLAT / PCS-J)",
        "last_subject": "🏛️ Constitutional Law of India",
        "last_topic": "Fundamental Rights: Article 14 (Equality), Art 19 (Six Freedoms) & Art 21 (Life & Personal Liberty)",
        "study_history": {},
        "ai_memory": {},
        "feedback_list": []
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
                "feedback_list": st.session_state.feedback_list
            }
    except Exception:
        pass

# Initialize Session States
saved_state = load_user_memory()

if "system_booted" not in st.session_state:
    st.session_state.system_booted = False

if "current_course" not in st.session_state:
    st.session_state.current_course = saved_state.get("last_course", "⚖️ Law & Judiciary (LL.B / CLAT / PCS-J)")

if "current_subject" not in st.session_state:
    st.session_state.current_subject = saved_state.get("last_subject", "🏛️ Constitutional Law of India")

if "current_topic" not in st.session_state:
    st.session_state.current_topic = saved_state.get("last_topic", "")

if "study_history" not in st.session_state:
    st.session_state.study_history = saved_state.get("study_history", {})

if "ai_memory" not in st.session_state:
    st.session_state.ai_memory = saved_state.get("ai_memory", {})

if "feedback_list" not in st.session_state:
    st.session_state.feedback_list = saved_state.get("feedback_list", [])

if "feedback_popup_shown" not in st.session_state:
    st.session_state.feedback_popup_shown = False

if "trigger_feedback_modal" not in st.session_state:
    st.session_state.trigger_feedback_modal = False

if "generated_gallery_sheets" not in st.session_state:
    st.session_state.generated_gallery_sheets = []

if "active_sheet_index" not in st.session_state:
    st.session_state.active_sheet_index = None

if "active_exam_questions" not in st.session_state:
    st.session_state.active_exam_questions = []

if "exam_user_answers" not in st.session_state:
    st.session_state.exam_user_answers = {}

if "exam_submitted" not in st.session_state:
    st.session_state.exam_submitted = False

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

if "notebook_cells" not in st.session_state:
    st.session_state.notebook_cells = [
        {
            "id": 1,
            "code": "# Python Cell 1: Verification & Environment\ndeveloper_name = 'Harsh Raj Soni'\ninstitution = 'MLK PG College, Balrampur'\nprint(f'Academic Portal Active | Developer: {developer_name} [{institution}]')",
            "output": "",
            "error": ""
        }
    ]

# Anti-Sleep Keep Alive Heartbeat
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

# THEME PALETTES
THEME_PALETTES = {
    "⚖️ Law & Judiciary (LL.B / CLAT / PCS-J)": {
        "grad_top": "#1F0D16",
        "grad_mid": "#14080E",
        "grad_base": "#090306",
        "accent": "#FB7185",
        "accent_dark": "#BE123C",
        "glow": "rgba(251, 113, 133, 0.22)",
        "card_bg": "rgba(31, 13, 22, 0.85)",
        "border": "#BE123C"
    },
    "🩺 NEET (Medical Entrance)": {
        "grad_top": "#062016",
        "grad_mid": "#04150E",
        "grad_base": "#020B07",
        "accent": "#34D399",
        "accent_dark": "#059669",
        "glow": "rgba(52, 211, 153, 0.22)",
        "card_bg": "rgba(6, 32, 22, 0.85)",
        "border": "#059669"
    },
    "⚙️ JEE (Main & Advanced)": {
        "grad_top": "#1C1308",
        "grad_mid": "#140D05",
        "grad_base": "#0A0602",
        "accent": "#FB923C",
        "accent_dark": "#EA580C",
        "glow": "rgba(251, 146, 60, 0.22)",
        "card_bg": "rgba(28, 19, 8, 0.85)",
        "border": "#EA580C"
    },
    "🎓 BCA (Computer Applications)": {
        "grad_top": "#0B132B",
        "grad_mid": "#080D1A",
        "grad_base": "#020617",
        "accent": "#38BDF8",
        "accent_dark": "#0284C7",
        "glow": "rgba(56, 189, 248, 0.25)",
        "card_bg": "rgba(15, 23, 42, 0.85)",
        "border": "#0284C7"
    },
    "🏛️ UPSC / Civil Services (CSAT & GS)": {
        "grad_top": "#1A0B2E",
        "grad_mid": "#110720",
        "grad_base": "#090311",
        "accent": "#C084FC",
        "accent_dark": "#9333EA",
        "glow": "rgba(192, 132, 252, 0.22)",
        "card_bg": "rgba(26, 11, 46, 0.85)",
        "border": "#9333EA"
    }
}

active_theme = THEME_PALETTES.get(st.session_state.current_course, THEME_PALETTES["⚖️ Law & Judiciary (LL.B / CLAT / PCS-J)"])

groq_key = st.secrets.get("GROQ_API_KEY", None)
gemini_key = st.secrets.get("GEMINI_API_KEY", None)
gmail_app_password = st.secrets.get("GMAIL_APP_PASSWORD", None)

def render_feedback_form_contents(context_key="modal"):
    st.markdown(f"""
    <div style="background:{active_theme['card_bg']}; border:1.5px solid {active_theme['accent']}; border-radius:12px; padding:14px 18px; margin-bottom:12px;">
        <div style="font-size:16px; font-weight:700; color:{active_theme['accent']};">⭐ Rate & Share Your Feedback</div>
        <div style="font-size:12px; color:#CBD5E1; margin-top:2px;">
            Aapka feedback seedhe Developer <b>Harsh Raj Soni</b> (<code>{ADMIN_EMAIL}</code>) tak jayega.
        </div>
    </div>
    """, unsafe_allow_html=True)

    star_options = [
        "⭐⭐⭐⭐⭐ (5/5 - Mind Blowing & Super Helpful!)",
        "⭐⭐⭐⭐ (4/5 - Bohot Achha Hai)",
        "⭐⭐⭐ (3/5 - Sahi Hai, Aur Improve Kar Sakte Hain)",
        "⭐⭐ (2/5 - Thoda Issue Aa Raha Hai)",
        "⭐ (1/5 - Needs Major Fix)"
    ]
    chosen_stars = st.radio("Select Rating:", star_options, index=0, key=f"fb_stars_{context_key}")

    c_n, c_e = st.columns(2)
    with c_n:
        fb_name = st.text_input("Aapka Naam:", placeholder="e.g. Aman Verma", key=f"fb_name_{context_key}")
    with c_e:
        fb_user_email = st.text_input("Aapka Email (Optional):", placeholder="student@gmail.com", key=f"fb_uemail_{context_key}")

    fb_stream = st.text_input("Course / Exam:", value=st.session_state.current_course, key=f"fb_crs_{context_key}")
    fb_msg = st.text_area("Aapka Feedback / Suggestion:", placeholder="App kaisa laga?...", height=95, key=f"fb_msg_{context_key}")

    if st.button("🚀 Submit Rating", key=f"fb_sub_{context_key}", type="primary", use_container_width=True):
        sender = fb_name.strip() if fb_name.strip() else "Anonymous Student"
        comment = fb_msg.strip() if fb_msg.strip() else "Rated the portal."
        rating_short = chosen_stars.split(" ")[0]

        entry = {
            "name": sender,
            "email": fb_user_email.strip(),
            "course": fb_stream,
            "rating": rating_short,
            "full_rating": chosen_stars,
            "message": comment,
            "time": time.strftime("%d %b %Y, %I:%M %p")
        }
        st.session_state.feedback_list.insert(0, entry)
        st.session_state.feedback_popup_shown = True
        st.session_state.trigger_feedback_modal = False
        save_user_memory()
        st.success("✅ Shukriya! Aapka feedback save ho gaya hai.")

if hasattr(st, "dialog"):
    @st.dialog("⭐ Rate & Feedback — Harsh's Suite")
    def open_feedback_popup_dialog():
        render_feedback_form_contents(context_key="popup_dlg")
elif hasattr(st, "experimental_dialog"):
    @st.experimental_dialog("⭐ Rate & Feedback — Harsh's Suite")
    def open_feedback_popup_dialog():
        render_feedback_form_contents(context_key="popup_dlg")
else:
    def open_feedback_popup_dialog():
        with st.expander("⭐ Rate & Feedback Popup", expanded=True):
            render_feedback_form_contents(context_key="popup_fallback")

COURSE_DATABASE = {
    "⚖️ Law & Judiciary (LL.B / CLAT / PCS-J)": {
        "icon": "⚖️",
        "subjects": {
            "🏛️ Constitutional Law of India": {
                "units": "Part I to IV, Fundamental Rights, Directive Principles, Judiciary & Amendments",
                "topics": [
                    "Preamble, Basic Structure Doctrine (Kesavananda Bharati) & Article 368",
                    "Fundamental Rights: Article 14 (Equality), Art 19 (Freedoms) & Art 21 (Life & Liberty)",
                    "Constitutional Remedies: Article 32 vs Article 226 & 5 Prerogative Writs",
                    "Union & State Judiciary: Supreme Court, High Courts & Collegium System"
                ],
                "pyqs_years": ["CLAT UG & PG 2025", "UP PCS-J 2024", "AIBE XIX Official", "DU LL.B 2024"]
            },
            "⚔️ Criminal Law (BNS, BNSS, BSA 2023 & IPC/CrPC)": {
                "units": "BNS 2023, BNSS 2023, BSA 2023 vs IPC, CrPC, IEA",
                "topics": [
                    "BNS 2023 vs IPC 1860: General Exceptions & Right of Private Defence",
                    "Offences Affecting Human Body: Culpable Homicide vs Murder (Sec 100-103 BNS)",
                    "Offences Against Women & Organised Crime (Sec 63-99 & 111 BNS)",
                    "BNSS 2023 (CrPC): Zero FIR, e-FIR, Arrest & Police Custody Remand"
                ],
                "pyqs_years": ["Judiciary PCS-J Criminal Law 2025/2024", "AIBE Criminal Law Paper", "CLAT PG Jurisprudence"]
            }
        }
    },
    "🩺 NEET (Medical Entrance)": {
        "icon": "🩺",
        "subjects": {
            "🧬 Zoology & Human Physiology": {
                "units": "Neural Control, Chemical Coordination, Circulation & Genetics",
                "topics": [
                    "Generation & Conduction of Nerve Impulse (Action Potential)",
                    "Sliding Filament Theory of Muscle Contraction",
                    "Cardiac Cycle, ECG Waveforms & Blood Pressure Regulation"
                ],
                "pyqs_years": ["NEET UG 2025", "NEET UG 2024", "NEET UG 2023", "NEET UG 2022"]
            }
        }
    },
    "⚙️ JEE (Main & Advanced)": {
        "icon": "⚙️",
        "subjects": {
            "📐 JEE Mathematics": {
                "units": "Coordinate Geometry, Calculus, Algebra & Vectors",
                "topics": [
                    "Conic Sections: Parabola, Ellipse & Tangent-Normal Equations",
                    "Definite Integration: King's Property, Leibnitz Rule & Reduction",
                    "Matrices, Determinants & System of Linear Equations"
                ],
                "pyqs_years": ["JEE Main 2025", "JEE Advanced 2024", "JEE Main 2024"]
            }
        }
    },
    "🎓 BCA (Computer Applications)": {
        "icon": "🎓",
        "subjects": {
            "🐍 Python Programming": {
                "units": "Bytecode, Control Flow, Functions & OOPs",
                "topics": [
                    "Python Architecture, Bytecode & Memory Management",
                    "Control Flow, Loops, For-Else Logic & Prime Verification",
                    "Data Structures: Lists, Tuples, Dictionaries & Sets"
                ],
                "pyqs_years": ["BCA Semester Exam 2025", "BCA Semester Exam 2024"]
            }
        }
    },
    "🏛️ UPSC / Civil Services (CSAT & GS)": {
        "icon": "🏛️",
        "subjects": {
            "📜 Indian Polity & Constitution": {
                "units": "Fundamental Rights, Parliament, Judiciary & Panchayati Raj",
                "topics": [
                    "Fundamental Rights (Articles 14 to 32) & Basic Structure",
                    "President vs Governor: Pardoning Powers & Discretion",
                    "Judicial Review, PIL & Collegium System Dynamics"
                ],
                "pyqs_years": ["UPSC CSE Prelims 2025", "UPSC CSE Prelims 2024", "UPSC CSE Prelims 2023"]
            }
        }
    }
}

DYNAMIC_THEME_CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Kalam:wght@400;700&family=Patrick+Hand&display=swap');
    html, body, [class*="css"] {{ font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; }}
    code, pre {{ font-family: 'JetBrains Mono', monospace !important; }}
    .stApp {{
        background: radial-gradient(circle at 50% 0%, {active_theme['grad_top']} 0%, {active_theme['grad_mid']} 60%, {active_theme['grad_base']} 100%) !important;
        color: #F8FAFC;
    }}
    header[data-testid="stHeader"] {{display: none !important;}}
    footer {{display: none !important; visibility: hidden !important;}}
    .block-container {{ padding-top: 0.6rem !important; padding-bottom: 5rem !important; max-width: 1080px !important; }}
    .formal-top-banner {{
        background: {active_theme['card_bg']};
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 14px;
        padding: 12px 20px;
        backdrop-filter: blur(20px);
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }}
    .formal-author-pill {{
        display: inline-flex; align-items: center; gap: 6px;
        background: rgba(255, 255, 255, 0.06); border: 1px solid {active_theme['accent']};
        padding: 5px 14px; border-radius: 20px; font-size: 11.5px; font-weight: 700; color: {active_theme['accent']};
    }}
    .resume-state-card {{
        background: {active_theme['card_bg']}; border: 1px dashed {active_theme['accent']};
        border-radius: 10px; padding: 8px 16px; margin-bottom: 12px;
        display: flex; align-items: center; justify-content: space-between; font-size: 12.5px; color: {active_theme['accent']};
    }}
    .question-card {{
        background: {active_theme['card_bg']}; border: 1.5px solid rgba(255, 255, 255, 0.1);
        border-left: 4.5px solid {active_theme['accent']}; border-radius: 12px; padding: 14px 18px; margin-bottom: 8px;
    }}
    .question-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 6px; }}
    .q-number-tag {{ background: {active_theme['glow']}; border: 1px solid {active_theme['accent']}; color: {active_theme['accent']}; font-size: 12px; font-weight: 700; padding: 2px 10px; border-radius: 14px; }}
    .q-marks-tag {{ font-size: 11px; color: #94A3B8; font-family: 'JetBrains Mono', monospace; }}
    .q-text {{ font-size: 15px; font-weight: 600; line-height: 1.55; color: #F8FAFC; margin-bottom: 4px; }}
    .inapp-paper-booklet {{ background: #FDFBF7; color: #1E293B; border: 2px solid {active_theme['accent']}; border-radius: 12px; padding: 24px 28px; margin: 14px 0; }}
    .booklet-header {{ text-align: center; border-bottom: 2px double #334155; padding-bottom: 12px; margin-bottom: 18px; }}
    .booklet-q-item {{ border-bottom: 1px dashed #CBD5E1; padding: 12px 0; color: #0F172A; }}
    div[data-testid="stExpander"] {{ background: {active_theme['card_bg']} !important; border: 1.5px solid {active_theme['border']} !important; border-radius: 12px !important; margin-bottom: 12px !important; }}
    .stButton>button {{
        background: linear-gradient(135deg, {active_theme['accent_dark']} 0%, {active_theme['grad_top']} 100%) !important;
        color: #FFFFFF !important; border: 1px solid {active_theme['accent']} !important; border-radius: 8px !important; font-weight: 600 !important;
    }}
</style>
"""
st.markdown(DYNAMIC_THEME_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.subheader("⚡ AI Engine & System")
    ai_choice = st.radio("Active Engine:", ["⚡ Groq LPU (Ultra Fast)", "Google Gemini"], index=0)

    if ai_choice == "⚡ Groq LPU (Ultra Fast)":
        if not groq_key:
            groq_key = st.text_input("Groq API Key:", type="password", placeholder="gsk_...")
        if groq_key:
            st.success("● Groq LPU Active")
        else:
            st.warning("⚠️ Groq API Key required")
    else:
        if not gemini_key:
            gemini_key = st.text_input("Gemini API Key:", type="password")
        if gemini_key:
            genai.configure(api_key=gemini_key)
            st.success("● Gemini Active")

    st.divider()
    if st.button("⭐ Rate & Give Feedback", key="sidebar_fb_btn", use_container_width=True):
        open_feedback_popup_dialog()
    st.caption("⚡ Developed by **Harsh Raj Soni**")
    st.caption("🏛️ MLK PG College, Balrampur")

def execute_ai_query(system_role, user_prompt, max_budget=2000):
    if "Groq" in ai_choice and groq_key:
        client = Groq(api_key=groq_key)
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_role}, {"role": "user", "content": user_prompt}],
                temperature=0.2, max_tokens=max_budget
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            return f"API_ERROR: {str(e)}"
    elif gemini_key:
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("models/gemini-2.0-flash")
            res = model.generate_content(system_role + "\n\n" + user_prompt)
            if res and res.text:
                return res.text.strip()
        except Exception as e:
            return f"API_ERROR: {str(e)}"
    return "API_ERROR: API Key enter karein left sidebar mein."

def parse_mcq_blocks(raw_text):
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

            questions.append({
                "q_no": len(questions) + 1,
                "year_tag": tag_m.group(1).strip() if tag_m else "Exam Set",
                "question": q_txt,
                "options": opts,
                "correct_option": correct_opt,
                "explanation": exp_m.group(1).strip() if exp_m else "Standard rule applies."
            })
    return questions

# FAST PYQ & MOCK GENERATOR (NO FREEZE)
def generate_fast_questions(topic, course_name, subject_name, count=10, is_pyq=False, pyq_year=""):
    tag_lbl = pyq_year if is_pyq else "Mock Set"
    sys_prompt = (
        f"You are Examiner for {course_name}. Output EXACTLY {count} MCQs using ONLY this block format:\n"
        "===Q_START===\n"
        f"TAG: {tag_lbl}\n"
        "Q: [Question]\n"
        "A: [Opt A]\n"
        "B: [Opt B]\n"
        "C: [Opt C]\n"
        "D: [Opt D]\n"
        "ANS: [A/B/C/D]\n"
        "EXP: [Explanation]\n"
        "===Q_END==="
    )
    raw = execute_ai_query(sys_prompt, f"Generate {count} questions for '{topic}' in {subject_name}.", max_budget=2000)
    return parse_mcq_blocks(raw)

# INTRO SCREEN
if not st.session_state.system_booted:
    st.markdown(f"""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:70vh; text-align:center;">
        <div style="font-size:32px; font-weight:800; color:#F8FAFC; margin-bottom:6px;">
            Harsh's Lex & Tech Suite ⚖️
        </div>
        <div style="font-size:14px; color:#94A3B8; margin-bottom:24px;">
            Law • Medical • Engineering • BCA • UPSC Portal
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Enter Portal", use_container_width=True):
        st.session_state.system_booted = True
        st.rerun()
else:
    if st.session_state.trigger_feedback_modal and not st.session_state.feedback_popup_shown:
        st.session_state.trigger_feedback_modal = False
        open_feedback_popup_dialog()

    top_c1, top_c2 = st.columns([3.8, 1.2])
    with top_c1:
        st.markdown(f"""
        <div class="formal-top-banner">
            <div>
                <div style="font-size: 18px; font-weight: 700; color: #F8FAFC;">Harsh's Lex & Tech Suite</div>
                <div style="font-size: 12px; color: #94A3B8;">Fast In-App PYQs • Fast DPP Engine • OMR Mode</div>
            </div>
            <div class="formal-author-pill">Harsh Raj Soni</div>
        </div>
        """, unsafe_allow_html=True)
    with top_c2:
        st.write("")
        if st.button("⭐ Rate & Feedback", key="top_rate_btn", use_container_width=True):
            open_feedback_popup_dialog()

    # COURSE SWITCHER
    curr_course = st.session_state.current_course
    with st.expander("🎓 Active Stream: " + curr_course + " (Tap to Switch)", expanded=False):
        c_list = list(COURSE_DATABASE.keys())
        cols = st.columns(len(c_list))
        for idx, crs in enumerate(c_list):
            with cols[idx]:
                if st.button(crs, key=f"crs_{idx}", use_container_width=True):
                    st.session_state.current_course = crs
                    st.session_state.current_subject = list(COURSE_DATABASE[crs]["subjects"].keys())[0]
                    st.session_state.pyq_questions = []
                    save_user_memory()
                    st.rerun()

    active_course_data = COURSE_DATABASE[st.session_state.current_course]
    available_subjects = list(active_course_data["subjects"].keys())
    if st.session_state.current_subject not in available_subjects:
        st.session_state.current_subject = available_subjects[0]

    with st.expander("📚 Active Subject: " + st.session_state.current_subject + " (Tap to Switch)", expanded=False):
        for s_name in available_subjects:
            if st.button(s_name, key=f"sub_{s_name}", use_container_width=True):
                st.session_state.current_subject = s_name
                st.session_state.pyq_questions = []
                save_user_memory()
                st.rerun()

    active_course = st.session_state.current_course
    active_subj = st.session_state.current_subject
    subject_details = active_course_data["subjects"][active_subj]

    nav_options = [
        "🔥 Fast DPP (15 Qs)",
        "📚 In-App PYQs Vault",
        "🎯 Mock Exam",
        "⚖️ Bare Acts & Maxims",
        "⭐ Feedback"
    ]
    selected_nav = st.radio("Navigation", nav_options, horizontal=True, index=0)

    # 1. FAST DPP
    if selected_nav == "🔥 Fast DPP (15 Qs)":
        st.subheader(f"🔥 Daily Practice Problems — {active_subj}")
        dpp_topic = st.selectbox("Select Topic:", subject_details.get("topics", []))
        if st.button("🚀 Generate 15 Qs Fast DPP", use_container_width=True):
            with st.spinner("Generating DPP instantly..."):
                st.session_state.dpp_questions = generate_fast_questions(dpp_topic, active_course, active_subj, count=15)
                st.session_state.dpp_submitted = False
                st.rerun()

        if st.session_state.dpp_questions:
            for idx, q in enumerate(st.session_state.dpp_questions):
                st.markdown(f"""
                <div class="question-card">
                    <div class="question-header">
                        <span class="q-number-tag">Q.{idx+1}</span>
                    </div>
                    <div class="q-text">{q['question']}</div>
                </div>
                """, unsafe_allow_html=True)
                st.radio(f"Answer Q.{idx+1}:", options=q['options'], key=f"dpp_{idx}", index=None)
                if st.session_state.dpp_submitted:
                    st.info(f"Correct: {q['correct_option']} | Exp: {q['explanation']}")
            if st.button("Submit DPP", type="primary"):
                st.session_state.dpp_submitted = True
                st.rerun()

    # 2. IN-APP PYQS VAULT (FAST & NO EXTERNAL WEBSITE)
    elif selected_nav == "📚 In-App PYQs Vault":
        st.subheader(f"📚 Official Past Papers In-App Viewer — {active_course}")
        pyqs_list = subject_details.get("pyqs_years", ["2024 Paper"])
        chosen_year = st.selectbox("Select Exam Year:", pyqs_list)
        view_mode = st.selectbox("Display Mode:", ["📝 Interactive OMR Mode", "📄 Full Booklet Reader Mode"])

        if st.button(f"📥 Load {chosen_year} Inside App Instantly", use_container_width=True):
            with st.spinner("Loading official paper directly inside app..."):
                st.session_state.pyq_questions = generate_fast_questions(
                    f"Official paper {chosen_year}", active_course, active_subj, count=12, is_pyq=True, pyq_year=chosen_year
                )
                st.session_state.pyq_submitted = False
                st.rerun()

        if st.session_state.pyq_questions:
            q_list = st.session_state.pyq_questions
            if view_mode == "📄 Full Booklet Reader Mode":
                booklet = f"""
                <div class="inapp-paper-booklet">
                    <div class="booklet-header">
                        <h3>{chosen_year} — OFFICIAL EXAMINATION BOOKLET</h3>
                        <p>{active_course} | {active_subj}</p>
                    </div>
                """
                for i, q in enumerate(q_list):
                    opts_s = "".join([f"<div>{o}</div>" for o in q['options']])
                    booklet += f"""
                    <div class="booklet-q-item">
                        <b>Q.{i+1}: {q['question']}</b>
                        {opts_s}
                        <p style="color: #0284C7; margin-top:5px;"><b>Key:</b> {q['correct_option']} | {q['explanation']}</p>
                    </div>
                    """
                booklet += "</div>"
                st.markdown(booklet, unsafe_allow_html=True)
            else:
                for idx, q in enumerate(q_list):
                    st.markdown(f"""
                    <div class="question-card">
                        <div class="question-header"><span class="q-number-tag">Q.{idx+1} • {q['year_tag']}</span></div>
                        <div class="q-text">{q['question']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.radio(f"Select PYQ Answer {idx+1}:", options=q['options'], key=f"pyq_{idx}", index=None)
                    if st.session_state.pyq_submitted:
                        st.info(f"Official Key: {q['correct_option']} | {q['explanation']}")
                if st.button("Submit PYQ Sheet", type="primary"):
                    st.session_state.pyq_submitted = True
                    st.rerun()

    # 3. MOCK EXAM
    elif selected_nav == "🎯 Mock Exam":
        st.subheader("🎯 Rapid Mock Exam")
        if st.button("Generate Mock Test", use_container_width=True):
            with st.spinner("Generating test..."):
                st.session_state.active_exam_questions = generate_fast_questions("Mock Test", active_course, active_subj, count=10)
                st.session_state.exam_submitted = False
                st.rerun()
        if st.session_state.active_exam_questions:
            for idx, q in enumerate(st.session_state.active_exam_questions):
                st.markdown(f"""
                <div class="question-card">
                    <div class="question-header"><span class="q-number-tag">Q.{idx+1}</span></div>
                    <div class="q-text">{q['question']}</div>
                </div>
                """, unsafe_allow_html=True)
                st.radio(f"Answer Mock {idx+1}:", options=q['options'], key=f"mock_{idx}", index=None)
                if st.session_state.exam_submitted:
                    st.success(f"Correct: {q['correct_option']}")
            if st.button("Submit Mock", type="primary"):
                st.session_state.exam_submitted = True
                st.rerun()

    # 4. BARE ACTS & MAXIMS
    elif selected_nav == "⚖️ Bare Acts & Maxims":
        st.subheader("⚖️ Indian Law Bare Acts & Maxims Reader")
        query = st.text_input("Search Bare Act Section / Article (e.g. 'Article 21', 'Section 103 BNS'):")
        if st.button("Read Provision Inside App", use_container_width=True) and query.strip():
            with st.spinner("Loading legal commentary..."):
                ans = execute_ai_query("You are a senior advocate. Explain Indian Law provision with case laws.", f"Explain {query}")
                st.info(ans)

    # 5. FEEDBACK
    elif selected_nav == "⭐ Feedback":
        render_feedback_form_contents(context_key="tab_view")
