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
import urllib.request
import contextlib
from PIL import Image

st.set_page_config(
    page_title="Universal Academic & Competitive Suite | Harsh Raj Soni",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= PERSISTENT STORAGE =================
STORAGE_FILE = "user_memory_store.db"

def load_user_memory():
    default_data = {
        "last_course": "🩺 NEET (Medical Entrance)",
        "last_subject": "🧬 Zoology & Human Physiology",
        "last_topic": "Generation & Conduction of Nerve Impulse (Action Potential)",
        "study_history": {},
        "ai_memory": {}
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
                "ai_memory": st.session_state.ai_memory
            }
    except Exception:
        pass

# Initialize Session State
saved_state = load_user_memory()

if "system_booted" not in st.session_state:
    st.session_state.system_booted = False

if "current_course" not in st.session_state:
    st.session_state.current_course = saved_state.get("last_course", "🩺 NEET (Medical Entrance)")

if "current_subject" not in st.session_state:
    st.session_state.current_subject = saved_state.get("last_subject", "🧬 Zoology & Human Physiology")

if "current_topic" not in st.session_state:
    st.session_state.current_topic = saved_state.get("last_topic", "")

if "study_history" not in st.session_state:
    st.session_state.study_history = saved_state.get("study_history", {})

if "ai_memory" not in st.session_state:
    st.session_state.ai_memory = saved_state.get("ai_memory", {})

if "generated_gallery_sheets" not in st.session_state:
    st.session_state.generated_gallery_sheets = []

if "active_sheet_index" not in st.session_state:
    st.session_state.active_sheet_index = None

if "active_exam_questions" not in st.session_state:
    st.session_state.active_exam_questions = []

if "exam_submitted" not in st.session_state:
    st.session_state.exam_submitted = False

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

# ================= THEME PALETTES (EYE-FRIENDLY SOFT DARK GRADIENTS) =================
THEME_PALETTES = {
    "🎓 BCA (Computer Applications)": {
        "grad_top": "#0B132B",
        "grad_mid": "#080D1A",
        "grad_base": "#020617",
        "accent": "#38BDF8",
        "accent_dark": "#0284C7",
        "glow": "rgba(56, 189, 248, 0.25)",
        "card_bg": "rgba(15, 23, 42, 0.8)",
        "border": "#0284C7"
    },
    "🩺 NEET (Medical Entrance)": {
        "grad_top": "#062016",
        "grad_mid": "#04150E",
        "grad_base": "#020B07",
        "accent": "#34D399",
        "accent_dark": "#059669",
        "glow": "rgba(52, 211, 153, 0.22)",
        "card_bg": "rgba(6, 32, 22, 0.8)",
        "border": "#059669"
    },
    "⚙️ JEE (Main & Advanced)": {
        "grad_top": "#1C1308",
        "grad_mid": "#140D05",
        "grad_base": "#0A0602",
        "accent": "#FB923C",
        "accent_dark": "#EA580C",
        "glow": "rgba(251, 146, 60, 0.22)",
        "card_bg": "rgba(28, 19, 8, 0.8)",
        "border": "#EA580C"
    },
    "🏛️ UPSC / Civil Services (CSAT & GS)": {
        "grad_top": "#1A0B2E",
        "grad_mid": "#110720",
        "grad_base": "#090311",
        "accent": "#C084FC",
        "accent_dark": "#9333EA",
        "glow": "rgba(192, 132, 252, 0.22)",
        "card_bg": "rgba(26, 11, 46, 0.8)",
        "border": "#9333EA"
    }
}

active_theme = THEME_PALETTES.get(st.session_state.current_course, THEME_PALETTES["🩺 NEET (Medical Entrance)"])

# ================= MASTER ACADEMIC & COMPETITIVE DATABASE =================
COURSE_DATABASE = {
    "🩺 NEET (Medical Entrance)": {
        "icon": "🩺",
        "subjects": {
            "🧬 Zoology & Human Physiology": {
                "units": "Unit 1: Neural Control & Coordination | Unit 2: Chemical Coordination | Unit 3: Circulation & Body Fluids | Unit 4: Reproduction & Genetics",
                "topics": [
                    "Generation & Conduction of Nerve Impulse (Action Potential)",
                    "Sliding Filament Theory of Muscle Contraction",
                    "Cardiac Cycle, ECG Waveforms & Blood Pressure Regulation",
                    "Mendelian Dihybrid Cross, Linkage & Recombination",
                    "DNA Replication, Transcription & Genetic Code",
                    "Spermatogenesis vs Oogenesis & Hormonal Feedback Cycles"
                ],
                "pyqs_years": ["NEET 2024", "NEET 2023", "NEET 2022", "NEET 2021", "NEET 2020"]
            },
            "🌿 Botany & Plant Biology": {
                "units": "Unit 1: Plant Kingdom & Anatomy | Unit 2: Photosynthesis | Unit 3: Respiration | Unit 4: Plant Growth Regulators",
                "topics": [
                    "Light Reaction: Z-Scheme, Cyclic vs Non-Cyclic Photophosphorylation",
                    "Calvin Cycle (C3) vs Hatch-Slack Pathway (C4 Plants)",
                    "Glycolysis, Krebs Cycle (TCA) & Chemiosmotic Hypothesis",
                    "Double Fertilization & Embryo Sac Development in Angiosperms",
                    "Auxin, Cytokinin, Gibberellin Action & Photoperiodism"
                ],
                "pyqs_years": ["NEET 2024", "NEET 2023", "NEET 2022", "NEET 2021", "NEET 2020"]
            },
            "🧪 NEET Chemistry (Organic & Inorganic)": {
                "units": "Unit 1: Chemical Bonding | Unit 2: Periodic Table | Unit 3: Reaction Mechanisms | Unit 4: Biomolecules",
                "topics": [
                    "VSEPR Theory, Hybridization & Molecular Orbital Theory (MOT)",
                    "SN1 vs SN2 Reaction Mechanisms with Stereochemistry",
                    "Aldol Condensation, Cannizzaro Reaction & Mechanisms",
                    "Coordination Compounds, Werner Theory & Crystal Field Splitting (CFT)",
                    "Thermodynamics: Hess's Law, Gibbs Free Energy & Spontaneity"
                ],
                "pyqs_years": ["NEET 2024", "NEET 2023", "NEET 2022", "NEET 2021", "NEET 2020"]
            },
            "⚛️ NEET Physics": {
                "units": "Unit 1: Kinematics & Mechanics | Unit 2: Electrodynamics | Unit 3: Optics & Modern Physics",
                "topics": [
                    "Projectile Motion & Relative Velocity in 2D",
                    "Newton's Laws, Friction & Circular Motion Dynamics",
                    "Ray Optics: Lens Maker Formula, Prism & Total Internal Reflection",
                    "Photoelectric Effect, de Broglie Wavelength & Bohr Model"
                ],
                "pyqs_years": ["NEET 2024", "NEET 2023", "NEET 2022", "NEET 2021", "NEET 2020"]
            }
        }
    },
    "⚙️ JEE (Main & Advanced)": {
        "icon": "⚙️",
        "subjects": {
            "📐 JEE Mathematics": {
                "units": "Unit 1: Coordinate Geometry | Unit 2: Calculus | Unit 3: Algebra & Vectors | Unit 4: Probability",
                "topics": [
                    "Conic Sections: Parabola, Ellipse & Tangent-Normal Equations",
                    "Definite Integration: King's Property, Leibnitz Rule & Reduction",
                    "Matrices, Determinants & System of Linear Equations (Cramer's Rule)",
                    "Complex Numbers: De Moivre Theorem, Geometry & Roots of Unity",
                    "Vectors & 3D Geometry: Shortest Distance Between Skew Lines"
                ],
                "pyqs_years": ["JEE Main 2024 (Jan/Apr)", "JEE Main 2023", "JEE Adv 2023", "JEE Main 2022"]
            },
            "⚛️ JEE Physics": {
                "units": "Unit 1: Rotational Dynamics | Unit 2: Electromagnetism | Unit 3: Thermodynamics & SHM | Unit 4: Wave Optics",
                "topics": [
                    "Moment of Inertia, Parallel-Perpendicular Axis Theorems & Rolling",
                    "Gauss Law, Electrostatic Potential & Capacitance with Dielectrics",
                    "Ampere's Circuital Law, Biot-Savart & Magnetic Dipoles",
                    "Electromagnetic Induction, Faraday's Law & LC Oscillations",
                    "Wave Optics: Young's Double Slit Experiment (YDSE) & Phase Shift"
                ],
                "pyqs_years": ["JEE Main 2024", "JEE Main 2023", "JEE Adv 2023", "JEE Main 2022"]
            },
            "🧪 JEE Chemistry (Physical & Inorganic)": {
                "units": "Unit 1: Chemical Equilibrium & Kinetics | Unit 2: Electrochemistry | Unit 3: Coordination Chemistry",
                "topics": [
                    "Nernst Equation, Electrochemical Cells & Kohlrausch's Law",
                    "Chemical Kinetics: Integrated Rate Laws & Arrhenius Equation",
                    "Ionic Equilibrium: Buffer Solutions, pH Calculation & Solubility Product",
                    "Metallurgy: Ellingham Diagram & Extraction Principles"
                ],
                "pyqs_years": ["JEE Main 2024", "JEE Main 2023", "JEE Adv 2023", "JEE Main 2022"]
            }
        }
    },
    "🎓 BCA (Computer Applications)": {
        "icon": "🎓",
        "subjects": {
            "🐍 Python Programming": {
                "units": "Unit 1: Bytecode & Internals | Unit 2: Loops & Logic | Unit 3: Functions & Scope | Unit 4: Data Structures | Unit 5: OOPs & Inheritance | Unit 6: File I/O",
                "topics": [
                    "Python Architecture, Bytecode & Memory Management",
                    "Control Flow, Loops, For-Else Logic & Prime Verification",
                    "Functions, Scopes, LEGB Resolution & Lambda Expressions",
                    "Data Structures: Lists, Tuples, Dictionaries & Sets",
                    "Object Oriented Programming: Encapsulation & Inheritance",
                    "File Handling, Context Managers & Exception Hierarchy"
                ],
                "pyqs_years": ["University Exam 2024", "University Exam 2023", "University Exam 2022"]
            },
            "🖥️ Computer System Architecture": {
                "units": "Unit 1: Binary Logic | Unit 2: Boolean Algebra & K-Maps | Unit 3: Combinational & Sequential Circuits | Unit 4: CPU Registers | Unit 5: Cache & Pipeline",
                "topics": [
                    "Full Adder Circuit, Logic Gates & Truth Table",
                    "Half Adder & Full Adder Design using 2 HA and 1 OR Gate",
                    "Number Systems, Complements & Binary Operations",
                    "K-Map 4-Variable Minimization & Grouping Rules",
                    "Flip-Flops, Master-Slave JK & Race-Around Condition",
                    "Instruction Cycle Phases & Cache Memory Mapping"
                ],
                "pyqs_years": ["University Exam 2024", "University Exam 2023", "University Exam 2022"]
            },
            "📐 Mathematics & Numerical Methods": {
                "units": "Unit 1: Matrices & Rank | Unit 2: Differential Calculus | Unit 3: Integral Calculus | Unit 4: Discrete Structures | Unit 5: Numerical Iterations",
                "topics": [
                    "Matrix Rank, Echelon Forms & Rouche-Capelli Consistency",
                    "L'Hopital's Rule for Indeterminate Forms with Solved Limit",
                    "Equivalence Relations Proof & POSET Hasse Diagrams",
                    "Eigenvalues, Eigenvectors & Cayley-Hamilton Theorem",
                    "Leibnitz Theorem for n-th Derivatives & Formula Matrix",
                    "Newton-Raphson Method & Numerical Convergence"
                ],
                "pyqs_years": ["University Exam 2024", "University Exam 2023", "University Exam 2022"]
            }
        }
    },
    "🏛️ UPSC / Civil Services (CSAT & GS)": {
        "icon": "🏛️",
        "subjects": {
            "📜 Indian Polity & Constitution": {
                "units": "Unit 1: Fundamental Rights | Unit 2: Parliament & Executive | Unit 3: Judiciary & Constitutional Bodies",
                "topics": [
                    "Fundamental Rights (Articles 14 to 32) & Basic Structure Doctrine",
                    "President vs Governor: Pardoning Powers & Discretionary Jurisdictions",
                    "Panchayati Raj (73rd & 74th Amendments) & Decentralization",
                    "Judicial Review, PIL & Collegium System Dynamics"
                ],
                "pyqs_years": ["UPSC Prelims 2024", "UPSC Prelims 2023", "UPSC Prelims 2022", "UPSC Prelims 2021"]
            },
            "🌍 Indian Economy & Geography": {
                "units": "Unit 1: Monetary & Fiscal Policy | Unit 2: Physical & Human Geography | Unit 3: Sustainable Development",
                "topics": [
                    "Inflation Targeting, Repo Rate & RBI Monetary Policy Tools",
                    "Fiscal Deficit, FRBM Act & Direct Tax Reforms (GST Architecture)",
                    "Monsoon Mechanism: Jet Streams, El Niño, La Niña & IOD"
                ],
                "pyqs_years": ["UPSC Prelims 2024", "UPSC Prelims 2023", "UPSC Prelims 2022", "UPSC Prelims 2021"]
            }
        }
    }
}

# ================= DYNAMIC EYE-FRIENDLY CSS =================
DYNAMIC_THEME_CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Kalam:wght@400;700&family=Patrick+Hand&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }}
    code, pre {{
        font-family: 'JetBrains Mono', monospace !important;
    }}

    .stApp {{
        background: radial-gradient(circle at 50% 0%, {active_theme['grad_top']} 0%, {active_theme['grad_mid']} 60%, {active_theme['grad_base']} 100%) !important;
        color: #F8FAFC;
        transition: background 0.5s ease-in-out;
    }}

    header[data-testid="stHeader"] {{display: none !important;}}
    footer {{display: none !important; visibility: hidden !important;}}
    .viewerBadge_container__1QSob, 
    .viewerBadge_link__1QSob,
    [data-testid="stStatusWidget"], 
    .stDeployButton,
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"],
    #MainMenu,
    div[class*="viewerBadge"] {{
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }}

    .block-container {{
        padding-top: 0.6rem !important;
        padding-bottom: 5rem !important;
        max-width: 1080px !important;
    }}

    .formal-top-banner {{
        background: {active_theme['card_bg']};
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 14px;
        padding: 12px 20px;
        backdrop-filter: blur(20px);
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        transition: all 0.4s ease;
    }}
    .formal-author-pill {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid {active_theme['accent']};
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 11.5px;
        font-weight: 700;
        color: {active_theme['accent']};
        box-shadow: 0 0 16px {active_theme['glow']};
    }}

    .resume-state-card {{
        background: {active_theme['card_bg']};
        border: 1px dashed {active_theme['accent']};
        border-radius: 10px;
        padding: 8px 16px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 12.5px;
        color: {active_theme['accent']};
    }}

    /* Paper Question Card (OMR Style) */
    .question-card {{
        background: {active_theme['card_bg']};
        border: 1.5px solid rgba(255, 255, 255, 0.1);
        border-left: 4.5px solid {active_theme['accent']};
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }}
    .question-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        padding-bottom: 6px;
    }}
    .q-number-tag {{
        background: {active_theme['glow']};
        border: 1px solid {active_theme['accent']};
        color: {active_theme['accent']};
        font-size: 12px;
        font-weight: 700;
        padding: 2px 10px;
        border-radius: 14px;
    }}
    .q-marks-tag {{
        font-size: 11px;
        color: #94A3B8;
        font-family: 'JetBrains Mono', monospace;
    }}
    .q-text {{
        font-size: 15px;
        font-weight: 600;
        line-height: 1.55;
        color: #F8FAFC;
        margin-bottom: 12px;
    }}

    div[data-testid="stExpander"] {{
        background: {active_theme['card_bg']} !important;
        border: 1.5px solid {active_theme['border']} !important;
        border-radius: 12px !important;
        box-shadow: 0 0 18px {active_theme['glow']}, 0 8px 24px rgba(0, 0, 0, 0.5) !important;
        margin-bottom: 12px !important;
    }}

    div[data-testid="stRadio"] {{
        background: {active_theme['card_bg']} !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 6px 12px !important;
        border-radius: 20px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
        margin-bottom: 8px !important;
    }}

    .stButton>button {{
        background: linear-gradient(135deg, {active_theme['accent_dark']} 0%, {active_theme['grad_top']} 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid {active_theme['accent']} !important;
        border-radius: 8px !important;
        padding: 6px 16px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 14px {active_theme['glow']} !important;
    }}
    .stButton>button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 6px 20px {active_theme['glow']} !important;
    }}

    .register-outer-center {{
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-top: 6px;
        margin-bottom: 12px;
    }}

    .real-notebook-sheet {{
        background-color: #fbfbf8 !important;
        background-image: 
            linear-gradient(90deg, transparent 36px, #ef4444 36px, #ef4444 37.5px, transparent 37.5px),
            linear-gradient(#e2e8f0 1px, transparent 1px) !important;
        background-size: 100% 100%, 100% 22px !important;
        border-radius: 8px !important;
        padding: 14px 14px 16px 44px !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.5) !important;
        width: 100% !important;
        max-width: 480px !important;
        box-sizing: border-box !important;
        font-family: 'Patrick Hand', 'Kalam', cursive !important;
        color: #1e3a8a !important;
        font-size: 14.5px !important;
        line-height: 22px !important;
        position: relative !important;
        overflow: hidden !important;
    }}

    .real-notebook-sheet::before {{
        content: '' !important;
        position: absolute !important;
        top: 10px !important;
        left: 8px !important;
        width: 10px !important;
        height: 96% !important;
        background-image: radial-gradient(circle, #94a3b8 3px, transparent 4px) !important;
        background-size: 10px 22px !important;
        background-repeat: repeat-y !important;
    }}

    .nb-title-h1 {{
        font-family: 'Kalam', cursive !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #1e1b4b !important;
        background: #fdf2f8 !important;
        padding: 1px 10px !important;
        border-radius: 4px !important;
        display: inline-block !important;
        border-bottom: 2px dashed #ec4899 !important;
        margin-bottom: 3px !important;
        line-height: 23px !important;
    }}

    .nb-subhead {{
        font-weight: 700 !important;
        color: #0369a1 !important;
        font-size: 14.5px !important;
        text-decoration: underline !important;
        margin-top: 4px !important;
        display: block !important;
    }}

    .table-container {{
        width: 100% !important;
        overflow-x: auto !important;
        margin: 4px 0 !important;
        box-sizing: border-box !important;
    }}
    .nb-table {{
        border-collapse: collapse !important;
        font-family: 'Patrick Hand', cursive !important;
        font-size: 13.5px !important;
        line-height: 18px !important;
        background: #ffffff !important;
        border: 1.5px solid #1e3a8a !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }}
    .nb-table th, .nb-table td {{
        border: 1px solid #1e3a8a !important;
        padding: 3px 5px !important;
        text-align: center !important;
        word-break: break-word !important;
    }}
    .nb-table th {{
        background: #e0f2fe !important;
        color: #0369a1 !important;
        font-weight: 700 !important;
    }}

    .nb-keypoints-box {{
        border: 1.5px dashed #16a34a !important;
        background: #f0fdf4 !important;
        border-radius: 8px !important;
        padding: 6px 10px !important;
        margin-top: 6px !important;
        color: #14532d !important;
        font-size: 13px !important;
        line-height: 19px !important;
    }}
</style>
"""
st.markdown(DYNAMIC_THEME_CSS, unsafe_allow_html=True)

# ================= UNIVERSAL AI ENGINE =================
groq_key = st.secrets.get("GROQ_API_KEY", None)
gemini_key = st.secrets.get("GEMINI_API_KEY", None)

with st.sidebar:
    st.markdown("### ⚡ AI Engine & System")
    ai_choice = st.radio("Active Engine:", ["⚡ Groq LPU (Ultra Fast)", "Google Gemini"], index=0)

    if ai_choice == "⚡ Groq LPU (Ultra Fast)":
        if not groq_key:
            groq_key = st.text_input("Groq API Key:", type="password", placeholder="gsk_...")
        if groq_key:
            st.success("● Groq LPU Active")
        else:
            st.info("console.groq.com se free key lein")
    else:
        if not gemini_key:
            gemini_key = st.text_input("Gemini API Key:", type="password")
        if gemini_key:
            genai.configure(api_key=gemini_key)
            st.success("● Gemini Multimodal Active")

    st.markdown("---")
    st.caption("⚡ Developed by **Harsh Raj Soni**")
    st.caption("🏛️ MLK PG College, Balrampur")

def execute_ai_query(system_role, user_prompt, max_budget=4096, image_input=None):
    if image_input and gemini_key:
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("models/gemini-2.0-flash")
            response = model.generate_content([system_role + "\n\n" + user_prompt, image_input])
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            return "Gemini Vision Error: " + str(e)

    if "Groq" in ai_choice and groq_key:
        client = Groq(api_key=groq_key)
        active_models = [
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
            "llama-3.1-8b-instant"
        ]
        
        last_err = ""
        for model_id in active_models:
            try:
                completion = client.chat.completions.create(
                    model=model_id,
                    messages=[
                        {"role": "system", "content": system_role},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.2,
                    max_tokens=max_budget
                )
                return completion.choices[0].message.content.strip()
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
        return "Engine Error: " + str(last_err)

    elif gemini_key:
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("models/gemini-2.0-flash")
            response = model.generate_content(system_role + "\n\n" + user_prompt)
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            return "Gemini Error: " + str(e)

    return "⚠️ Pehle Sidebar mein Groq ya Gemini ki API Key add karein."

def fix_unclosed_html(html_str):
    open_divs = html_str.count("<div")
    close_divs = html_str.count("</div>")
    if open_divs > close_divs:
        html_str += "</div>" * (open_divs - close_divs)
    if "<table" in html_str and "</table" not in html_str:
        html_str += "</table>"
    if "<p" in html_str and "</p" not in html_str:
        html_str += "</p>"
    return html_str

def generate_multi_sheets_html(topic, subject_name, course_name, notes_lang):
    token_budget = 4096 if len(topic) < 30 else 5500
    last_ai_ctx = st.session_state.ai_memory.get(course_name, {}).get("last_summary", "No previous context.")

    system_role = (
        "You are an esteemed professor and entrance mentor specializing in " + course_name + ". "
        "Strictly maintain academic dignity. "
        "Student Context Memory: " + last_ai_ctx + ". "
        "Output EXACTLY 3 TO 4 INDIVIDUAL COMPLETE LECTURE SHEETS separated strictly by the token '===SHEET_SPLIT==='. "
        "Every single sheet MUST be 100% complete with all 4 sections fully finished: "
        "1. Definition & Core Concept, "
        "2. Truth Table / Formulation / Comparison Matrix, "
        "3. Step-by-Step Working / Derivation, "
        "4. Key Exam Points / Formulas / Shortcuts. "
        "DO NOT USE CODE BLOCKS OR MARKDOWN TICKS. Start directly with <div class='register-outer-center'>."
    )
    user_prompt = (
        "Create a complete 3 to 4-sheet lecture register for '" + topic + "' under " + course_name + " -> " + subject_name + " (" + notes_lang + ").\n"
        "Ensure full tables and working steps are filled.\n\n"
        "TEMPLATE FOR EACH SHEET (Separate sheets strictly by ===SHEET_SPLIT===):\n"
        "<div class=\"register-outer-center\">\n"
        "    <div class=\"real-notebook-sheet\">\n"
        "        <div class=\"nb-title-h1\">" + topic + " [Part X]</div>\n"
        "        <div style=\"font-size:10.5px; color:#6b7280; margin-bottom:3px;\">" + course_name + " • " + subject_name + "</div>\n\n"
        "        <span class=\"nb-subhead\">1. Definition & Core Concept :</span>\n"
        "        <p style=\"margin: 2px 0 4px 0;\">[2 concise explanation lines in " + notes_lang + "]</p>\n\n"
        "        <span class=\"nb-subhead\">2. Formulation / Table / Matrix :</span>\n"
        "        <div class=\"table-container\">\n"
        "            <table class=\"nb-table\">\n"
        "                <tr><th>Key Factor</th><th>Parameter / Condition</th><th>Result / Output</th></tr>\n"
        "                <tr><td>Condition 1</td><td>Value Alpha</td><td>Stable</td></tr>\n"
        "                <tr><td>Condition 2</td><td>Value Beta</td><td>Optimal</td></tr>\n"
        "            </table>\n"
        "        </div>\n\n"
        "        <span class=\"nb-subhead\">3. Step-by-Step Working / Derivation :</span>\n"
        "        <p style=\"margin: 2px 0 4px 0;\">\n"
        "            • Step 1: Core working logic and operation<br>\n"
        "            • Step 2: Signal/Formula execution path<br>\n"
        "            • Step 3: Practical problem solving rule\n"
        "        </p>\n\n"
        "        <div class=\"nb-keypoints-box\">\n"
        "            <b>✳ Key Exam Points & Shortcuts :</b><br>\n"
        "            • High priority question rule<br>\n"
        "            • Key shortcut formula\n"
        "        </div>\n"
        "        <div style=\"font-size:10px; color:#9ca3af; text-align:right; margin-top:4px;\">Harsh Raj Soni • Universal Portal</div>\n"
        "    </div>\n"
        "</div>"
    )
    raw_res = execute_ai_query(system_role, user_prompt, max_budget=token_budget)
    
    clean_text = raw_res.replace("```html", "").replace("```HTML", "").replace("```", "").strip()
    clean_text = re.sub(r"^`+|`+$", "", clean_text)
    
    raw_sheets = [s.strip() for s in clean_text.split("===SHEET_SPLIT===") if s.strip()]
    
    sanitized_sheets = []
    for s in raw_sheets:
        fixed = fix_unclosed_html(s)
        sanitized_sheets.append(fixed)
        
    if course_name not in st.session_state.ai_memory:
        st.session_state.ai_memory[course_name] = {}
    st.session_state.ai_memory[course_name]["last_topic"] = topic
    st.session_state.ai_memory[course_name]["last_summary"] = "Recently studied " + topic + " in " + subject_name
    save_user_memory()
    
    return sanitized_sheets if sanitized_sheets else [clean_text]

# ================= STRUCTURED EXAM / PYQ GENERATOR =================
def generate_interactive_paper(exam_topic, course_name, subject_name, is_pyq=False, pyq_year=""):
    context_type = f"Authentic Previous Year Exam Paper ({pyq_year})" if is_pyq else "Standard National Examination Test"
    sys_prompt = (
        "You are the Chief Examination Controller and Question Paper Setter for " + course_name + ". "
        "Strictly output EXACTLY 5 high-yield multiple choice questions as a valid JSON array. "
        "DO NOT output Markdown tables or HTML tables. Output ONLY raw JSON array. "
        "JSON Schema for each object in the array:\n"
        "{\n"
        '  "q_no": 1,\n'
        '  "year_tag": "NEET 2023" or "Expected Mock",\n'
        '  "question": "Clear scientific question text here",\n'
        '  "options": ["A. Option text", "B. Option text", "C. Option text", "D. Option text"],\n'
        '  "correct_option": "A. Option text",\n'
        '  "explanation": "Clear step-by-step logic and concept justification"\n'
        "}"
    )
    user_prompt = f"Create 5 high-standard MCQs for '{exam_topic}' in {subject_name} under {course_name}. {context_type}."
    
    raw_json = execute_ai_query(sys_prompt, user_prompt, max_budget=3500)
    raw_json = re.sub(r"^```json\s*", "", raw_json, flags=re.IGNORECASE)
    raw_json = re.sub(r"^```\s*", "", raw_json)
    raw_json = re.sub(r"\s*```$", "", raw_json).strip()

    try:
        data = json.loads(raw_json)
        if isinstance(data, list) and len(data) > 0:
            return data
    except Exception:
        pass

    # Safe fallback if AI wraps json awkwardly
    match = re.search(r'\[\s*\{.*\}\s*\]', raw_json, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            pass

    return []

# ================= 0. INTRO SCREEN =================
if not st.session_state.system_booted:
    st.markdown(f"""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:70vh; text-align:center;">
        <div style="display:inline-flex; align-items:center; gap:8px; background:rgba(255,255,255,0.06); border:1px solid {active_theme['accent']}; padding:6px 20px; border-radius:30px; font-size:13px; font-weight:700; color:{active_theme['accent']}; margin-bottom:14px; box-shadow:0 0 16px {active_theme['glow']};">
            🎓 UNIVERSAL ACADEMIC & ENTRANCE SUITE
        </div>
        <div style="font-size:32px; font-weight:800; color:#F8FAFC; letter-spacing:-0.5px; margin-bottom:6px;">
            Created & Designed by Harsh Raj Soni
        </div>
        <div style="font-size:14px; color:#94A3B8; margin-bottom:24px;">
            NEET • JEE • BCA • UPSC | MLK PG College, Balrampur
        </div>
        <div style="background:{active_theme['card_bg']}; border:1px solid rgba(255,255,255,0.1); border-left:4px solid {active_theme['accent']}; border-radius:10px; padding:16px 22px; max-width:560px; width:100%; text-align:left; font-size:13px; color:#CBD5E1; line-height:1.6; margin-bottom:24px;">
            <div style="color:{active_theme['accent']}; font-weight:700; margin-bottom:4px;">New Capabilities:</div>
            <div>• 📚 Authentic Year-wise PYQ Papers with OMR Simulator</div>
            <div>• Clean Question Cards with Radio/Checkbox Option Selectors</div>
            <div>• Instant Auto-Evaluation with Marks & Explanation</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        if st.button("Enter Learning Ecosystem", use_container_width=True):
            st.session_state.system_booted = True
            st.rerun()

else:
    # Top Executive Bar
    st.markdown(f"""
    <div class="formal-top-banner">
        <div>
            <div style="font-size: 18px; font-weight: 700; color: #F8FAFC;">
                Universal Academic & Competitive Portal
            </div>
            <div style="font-size: 12px; color: #94A3B8;">
                Dynamic Stream Atmosphere • Interactive OMR Test Engine
            </div>
        </div>
        <div class="formal-author-pill">
            Developer: Harsh Raj Soni
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Persistent Resume Notification
    if st.session_state.current_topic:
        st.markdown(
            '<div class="resume-state-card">'
            '<span>📌 <b>Resumed Session:</b> ' + st.session_state.current_course + ' ➔ ' + st.session_state.current_subject + ' (Last Topic: <i>' + st.session_state.current_topic + '</i>)</span>'
            '<span>Auto-Saved ●</span>'
            '</div>',
            unsafe_allow_html=True
        )

    # ================= COURSE SWITCHER =================
    curr_course = st.session_state.current_course
    with st.expander("🎓 Active Stream: " + curr_course + " (Tap to Switch)", expanded=False):
        c_list = list(COURSE_DATABASE.keys())
        cols = st.columns(len(c_list))
        for idx, crs in enumerate(c_list):
            with cols[idx]:
                is_active = (crs == curr_course)
                if st.button(crs, key="course_btn_" + str(idx), use_container_width=True, type="primary" if is_active else "secondary"):
                    st.session_state.current_course = crs
                    st.session_state.current_subject = list(COURSE_DATABASE[crs]["subjects"].keys())[0]
                    st.session_state.current_topic = ""
                    st.session_state.generated_gallery_sheets = []
                    st.session_state.active_sheet_index = None
                    st.session_state.active_exam_questions = []
                    st.session_state.exam_submitted = False
                    save_user_memory()
                    st.rerun()

    active_course_data = COURSE_DATABASE[st.session_state.current_course]

    # Subject Selector
    available_subjects = list(active_course_data["subjects"].keys())
    if st.session_state.current_subject not in available_subjects:
        st.session_state.current_subject = available_subjects[0]

    with st.expander("📚 Active Subject: " + st.session_state.current_subject + " (Tap to Switch)", expanded=False):
        sub_cols = st.columns(len(available_subjects))
        for s_idx, s_name in enumerate(available_subjects):
            with sub_cols[s_idx]:
                is_sub_active = (s_name == st.session_state.current_subject)
                if st.button(s_name, key="sub_btn_" + str(s_idx), use_container_width=True, type="primary" if is_sub_active else "secondary"):
                    st.session_state.current_subject = s_name
                    st.session_state.current_topic = ""
                    st.session_state.generated_gallery_sheets = []
                    st.session_state.active_sheet_index = None
                    st.session_state.active_exam_questions = []
                    st.session_state.exam_submitted = False
                    save_user_memory()
                    st.rerun()

    active_course = st.session_state.current_course
    active_subj = st.session_state.current_subject
    subject_details = active_course_data["subjects"][active_subj]

    # Navigation Dock (Added PYQs Option)
    nav_options = [
        "📝 Notes Gallery",
        "🎯 Mock Exam",
        "📚 PYQs Vault",
        "📖 Syllabus",
        "🔬 Formula & Lab",
        "🤖 AI Mentor"
    ]
    if "Python" in active_subj:
        nav_options.append("💻 Sandbox")

    selected_nav = st.radio(
        label="Navigation Section",
        options=nav_options,
        horizontal=True,
        index=0
    )

    # ================= SECTION 1: NOTES GALLERY =================
    if selected_nav == "📝 Notes Gallery":
        st.markdown("#### 📖 Lecture Notes Register Gallery — " + active_subj)
        st.caption("Classmate ruled paper layout with tables, formulas, and key points in a mobile gallery grid.")

        c1, c2 = st.columns([2.5, 1])
        with c1:
            suggested = subject_details.get("topics", [])
            chosen_topic = st.selectbox("Curated Topic List:", suggested)
            custom_topic = st.text_input("Or Type ANY Custom Topic / Concept:", placeholder="e.g. Action potential in cardiac muscle / K-Map with Don't Care")
        with c2:
            notes_lang = st.selectbox("Language:", ["Hinglish", "English", "Hindi"])

        final_topic = custom_topic.strip() if custom_topic.strip() else chosen_topic

        if st.button("Generate Lecture Register Sheets", use_container_width=True):
            st.session_state.current_topic = final_topic
            st.session_state.active_sheet_index = None
            save_user_memory()

            with st.spinner("Writing complete lecture sheets for '" + final_topic + "' under " + active_course + "..."):
                st.session_state.generated_gallery_sheets = generate_multi_sheets_html(
                    final_topic, active_subj, active_course, notes_lang
                )

        if st.session_state.generated_gallery_sheets:
            sheets = st.session_state.generated_gallery_sheets
            total_sheets = len(sheets)

            if st.session_state.active_sheet_index is not None:
                cur_i = st.session_state.active_sheet_index
                st.markdown("##### 🔍 Viewing Sheet " + str(cur_i + 1) + " of " + str(total_sheets))
                st.html(sheets[cur_i])

                nav_c1, nav_c2, nav_c3 = st.columns([1.5, 2, 1.5])
                with nav_c1:
                    if st.button("‹ Previous Sheet", disabled=(cur_i == 0), use_container_width=True):
                        st.session_state.active_sheet_index = max(0, cur_i - 1)
                        st.rerun()
                with nav_c2:
                    if st.button("📁 Close & Back to Gallery Grid", use_container_width=True):
                        st.session_state.active_sheet_index = None
                        st.rerun()
                with nav_c3:
                    if st.button("Next Sheet ›", disabled=(cur_i == total_sheets - 1), use_container_width=True):
                        st.session_state.active_sheet_index = min(total_sheets - 1, cur_i + 1)
                        st.rerun()
            else:
                st.markdown("##### 📸 Register Sheets Gallery (" + str(total_sheets) + " Sheets)")
                st.caption("Kisi bhi sheet par tap karein full-size padhne ke liye:")
                grid_cols = st.columns(3)
                for idx, sheet_code in enumerate(sheets):
                    with grid_cols[idx % 3]:
                        if st.button("📄 Sheet " + str(idx + 1) + " (Tap to Open)", key="sheet_btn_" + str(idx), use_container_width=True):
                            st.session_state.active_sheet_index = idx
                            st.rerun()
                        card_thumb = f"""
                        <div style="border:1.5px solid {active_theme['accent']}; border-radius:8px; padding:10px; background:{active_theme['card_bg']}; text-align:center; margin-bottom:12px; box-shadow:0 0 10px {active_theme['glow']};">
                            <span style="font-size:13.5px; color:{active_theme['accent']}; font-weight:700;">Sheet #{idx + 1}</span><br>
                            <span style="font-size:11px; color:#94A3B8;">Ruled Lecture Register</span>
                        </div>
                        """
                        st.markdown(card_thumb, unsafe_allow_html=True)

    # ================= SECTION 2: PROPER MOCK EXAM (INTERACTIVE OPTIONS) =================
    elif selected_nav == "🎯 Mock Exam":
        st.markdown(f"#### 🎯 Competitive Exam Paper — {active_course}")
        st.caption("Clean Question Paper Layout with Interactive Option Selector & Instant OMR Evaluation.")

        c1, c2 = st.columns([2.5, 1])
        with c1:
            exam_topic = st.text_input("Scope / Chapter for Test:", value=st.session_state.current_topic if st.session_state.current_topic else active_subj)
        with c2:
            paper_diff = st.selectbox("Exam Standard:", ["Entrance Standard (Moderate-High)", "Challenging (Top Rankers)"])

        if st.button("Generate Question Paper", use_container_width=True):
            with st.spinner("Generating clean MCQ examination paper..."):
                st.session_state.active_exam_questions = generate_interactive_paper(
                    exam_topic, active_course, active_subj, is_pyq=False
                )
                st.session_state.exam_submitted = False
                st.rerun()

        # Render Question Paper
        if st.session_state.active_exam_questions:
            q_list = st.session_state.active_exam_questions
            st.markdown("---")
            st.markdown(f"### 📋 SECTION-A : Multiple Choice Questions (+4, -1 Scheme)")

            user_answers = {}

            for idx, q_data in enumerate(q_list):
                q_num = idx + 1
                st.markdown(f"""
                <div class="question-card">
                    <div class="question-header">
                        <span class="q-number-tag">Question {q_num}</span>
                        <span class="q-marks-tag">Marks: +4 / -1</span>
                    </div>
                    <div class="q-text">{q_data.get('question', '')}</div>
                </div>
                """, unsafe_allow_html=True)

                opts = q_data.get("options", [])
                user_answers[idx] = st.radio(
                    f"Select Answer for Q.{q_num}:",
                    options=opts,
                    key=f"mock_q_{idx}",
                    index=None
                )

                if st.session_state.exam_submitted:
                    correct = q_data.get("correct_option", "")
                    selected = user_answers.get(idx)

                    if selected == correct:
                        st.success(f"✔ **Correct!** Answer: {correct}")
                    else:
                        st.error(f"✖ **Incorrect / Skipped.** Correct: {correct} (You chose: {selected if selected else 'None'})")

                    with st.expander(f"💡 View Explanation for Q.{q_num}", expanded=True):
                        st.write(q_data.get("explanation", "Standard conceptual derivation applies."))
                
                st.write("")

            col_sub1, col_sub2 = st.columns([2, 1])
            with col_sub1:
                if st.button("📝 Submit Test & Check Scorecard", type="primary", use_container_width=True):
                    st.session_state.exam_submitted = True
                    st.rerun()

            if st.session_state.exam_submitted:
                total_q = len(q_list)
                correct_cnt = sum(1 for idx, q in enumerate(q_list) if user_answers.get(idx) == q.get("correct_option"))
                wrong_cnt = sum(1 for idx, q in enumerate(q_list) if user_answers.get(idx) and user_answers.get(idx) != q.get("correct_option"))
                unattempted = total_q - (correct_cnt + wrong_cnt)
                total_marks = (correct_cnt * 4) - (wrong_cnt * 1)
                max_marks = total_q * 4

                st.markdown(f"""
                <div style="background:{active_theme['card_bg']}; border:2px solid {active_theme['accent']}; border-radius:12px; padding:18px 24px; text-align:center; margin-top:20px; box-shadow:0 0 20px {active_theme['glow']};">
                    <h3 style="color:{active_theme['accent']}; margin-bottom:6px;">📊 Test Result & Performance Summary</h3>
                    <div style="font-size:24px; font-weight:800; color:#F8FAFC; margin-bottom:12px;">Score: {total_marks} / {max_marks}</div>
                    <div style="display:flex; justify-content:center; gap:20px; font-size:13px; color:#CBD5E1;">
                        <span>✔ Correct: <b style="color:#34D399;">{correct_cnt}</b></span>
                        <span>✖ Wrong: <b style="color:#EF4444;">{wrong_cnt}</b></span>
                        <span>⚪ Unattempted: <b style="color:#94A3B8;">{unattempted}</b></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ================= SECTION 3: AUTHENTIC PYQS VAULT =================
    elif selected_nav == "📚 PYQs Vault":
        st.markdown(f"#### 📚 Previous Years Questions (PYQs) — {active_course}")
        st.caption("Real official exam questions sorted by past examination years.")

        pyqs_list = subject_details.get("pyqs_years", ["Past 5 Years Comprehensive"])
        
        c1, c2 = st.columns([2, 1])
        with c1:
            chosen_year = st.selectbox("Select Exam Year / Series:", pyqs_list)
            pyq_topic = st.text_input("Filter by Topic (Optional):", placeholder="e.g. Action Potential / Thermodynamics")
        with c2:
            st.info(f"Targeting: **{active_subj}**")

        target_topic = pyq_topic.strip() if pyq_topic.strip() else active_subj

        if st.button("Load Official PYQs Paper", use_container_width=True):
            with st.spinner(f"Extracting official questions from {chosen_year}..."):
                st.session_state.active_exam_questions = generate_interactive_paper(
                    target_topic, active_course, active_subj, is_pyq=True, pyq_year=chosen_year
                )
                st.session_state.exam_submitted = False
                st.rerun()

        # Render PYQ Question Paper
        if st.session_state.active_exam_questions:
            q_list = st.session_state.active_exam_questions
            st.markdown("---")
            st.markdown(f"### 🏛️ {chosen_year} Official Question Paper — {active_subj}")

            user_pyq_answers = {}

            for idx, q_data in enumerate(q_list):
                q_num = idx + 1
                st.markdown(f"""
                <div class="question-card">
                    <div class="question-header">
                        <span class="q-number-tag">Q.{q_num} • {q_data.get('year_tag', chosen_year)}</span>
                        <span class="q-marks-tag">+4 for Correct | -1 for Wrong</span>
                    </div>
                    <div class="q-text">{q_data.get('question', '')}</div>
                </div>
                """, unsafe_allow_html=True)

                opts = q_data.get("options", [])
                user_pyq_answers[idx] = st.radio(
                    f"Your Answer for PYQ #{q_num}:",
                    options=opts,
                    key=f"pyq_q_{idx}",
                    index=None
                )

                if st.session_state.exam_submitted:
                    correct = q_data.get("correct_option", "")
                    selected = user_pyq_answers.get(idx)

                    if selected == correct:
                        st.success(f"✔ **Correct!** Answer: {correct}")
                    else:
                        st.error(f"✖ **Incorrect / Skipped.** Official Key: {correct} (You chose: {selected if selected else 'None'})")

                    with st.expander(f"💡 View Official Solution & Concept Note #{q_num}", expanded=True):
                        st.write(q_data.get("explanation", "Official solution applies standard syllabus rationale."))
                
                st.write("")

            if st.button("📝 Submit PYQ Sheet & Evaluate", type="primary", use_container_width=True):
                st.session_state.exam_submitted = True
                st.rerun()

            if st.session_state.exam_submitted:
                total_q = len(q_list)
                correct_cnt = sum(1 for idx, q in enumerate(q_list) if user_pyq_answers.get(idx) == q.get("correct_option"))
                wrong_cnt = sum(1 for idx, q in enumerate(q_list) if user_pyq_answers.get(idx) and user_pyq_answers.get(idx) != q.get("correct_option"))
                total_marks = (correct_cnt * 4) - (wrong_cnt * 1)
                max_marks = total_q * 4

                st.markdown(f"""
                <div style="background:{active_theme['card_bg']}; border:2px solid {active_theme['accent']}; border-radius:12px; padding:18px 24px; text-align:center; margin-top:20px; box-shadow:0 0 20px {active_theme['glow']};">
                    <h3 style="color:{active_theme['accent']}; margin-bottom:6px;">📊 PYQ Mock Assessment</h3>
                    <div style="font-size:24px; font-weight:800; color:#F8FAFC; margin-bottom:12px;">Score: {total_marks} / {max_marks}</div>
                    <div style="display:flex; justify-content:center; gap:20px; font-size:13px; color:#CBD5E1;">
                        <span>✔ Correct: <b style="color:#34D399;">{correct_cnt}</b></span>
                        <span>✖ Negative: <b style="color:#EF4444;">{wrong_cnt}</b></span>
                        <span>🎯 Accuracy: <b>{int((correct_cnt/total_q)*100) if total_q else 0}%</b></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ================= SECTION 4: SYLLABUS BREAKDOWN =================
    elif selected_nav == "📖 Syllabus":
        st.markdown("#### 📚 Curriculum Breakdown — " + active_course)
        st.info("Current Subject: **" + active_subj + "**")
        st.write(subject_details.get("units", "Comprehensive syllabus mapped to entrance standards."))

        with st.expander("📌 View All Units in " + active_course):
            for s_k, s_v in active_course_data["subjects"].items():
                st.markdown("**" + s_k + "**")
                st.caption(s_v.get("units", ""))

    # ================= SECTION 5: FORMULA & BLUEPRINTS =================
    elif selected_nav == "🔬 Formula & Lab":
        st.markdown("#### 🔬 Formula & Concepts Compendium — " + active_subj)
        with st.expander("⚡ Core Formulation & Important Matrix"):
            if "Math" in active_subj:
                st.latex(r"\frac{d}{dx}\left(\frac{u}{v}\right) = \frac{v u' - u v'}{v^2}")
                st.latex(r"\lim_{x \to a} \frac{f(x)}{g(x)} = \lim_{x \to a} \frac{f'(x)}{g'(x)}")
            elif "Physics" in active_subj:
                st.latex(r"\vec{F} = \frac{d\vec{p}}{dt}, \quad E = mc^2")
                st.latex(r"V = IR, \quad B = \frac{\mu_0 I}{2\pi r}")
            elif "Chemistry" in active_subj:
                st.latex(r"\Delta G = \Delta H - T\Delta S")
                st.latex(r"E_{cell} = E^\circ_{cell} - \frac{RT}{nF} \ln Q")
            else:
                st.latex(r"Sum = A \oplus B \oplus C_{in}, \quad Carry = AB + C_{in}(A \oplus B)")

    # ================= SECTION 6: AI MENTOR =================
    elif selected_nav == "🤖 AI Mentor":
        st.markdown("#### 🤖 1-on-1 AI Faculty Mentor — " + active_course)
        past_ctx = st.session_state.ai_memory.get(active_course, {}).get("last_summary", "Starting fresh discussion.")
        st.caption("AI Memory Context: *" + past_ctx + "*")

        q = st.text_input("Ask Any Doubt / Paste Question:")
        q_img = st.file_uploader("Upload Problem Image (Optional):", type=["png", "jpg", "jpeg"])
        pil_q = Image.open(q_img) if q_img else None

        if st.button("Clear Doubt", use_container_width=True):
            if q.strip() or pil_q:
                with st.spinner("AI faculty analyzing with memory context..."):
                    sys_prompt = (
                        "You are a master mentor for " + active_course + " (" + active_subj + "). "
                        "Remember previous progress: " + past_ctx + ". "
                        "Explain step-by-step with derivation and exam tricks."
                    )
                    ans = execute_ai_query(sys_prompt, q, image_input=pil_q)
                    st.write(ans)
                    
                    if active_course not in st.session_state.ai_memory:
                        st.session_state.ai_memory[active_course] = {}
                    st.session_state.ai_memory[active_course]["last_summary"] = "Discussed: " + q[:60]
                    save_user_memory()
            else:
                st.warning("Please type a question or upload image.")

    # ================= SECTION 7: COLAB SANDBOX (PYTHON) =================
    elif selected_nav == "💻 Sandbox" and "Python" in active_subj:
        st.markdown("#### 💻 Colab Notebook // Python Only")

        tb1, tb2 = st.columns([1, 1])
        with tb1:
            if st.button("Add Cell", use_container_width=True):
                new_id = len(st.session_state.notebook_cells) + 1
                st.session_state.notebook_cells.append({
                    "id": new_id,
                    "code": "# Python Cell\n",
                    "output": "",
                    "error": ""
                })
                st.rerun()
        with tb2:
            if st.button("Clear Outputs", use_container_width=True):
                for cell in st.session_state.notebook_cells:
                    cell["output"] = ""
                    cell["error"] = ""
                st.rerun()

        for idx, cell in enumerate(st.session_state.notebook_cells):
            st.markdown("**[ " + str(idx + 1) + " ]** In [ ]:")
            c_ed, c_act = st.columns([8.5, 1.5])
            with c_ed:
                cell["code"] = st.text_area("Cell " + str(cell['id']), value=cell["code"], height=120, label_visibility="collapsed")
            with c_act:
                run_btn = st.button("Run", key="run_" + str(cell['id']), use_container_width=True)
                assist_btn = st.button("Assist", key="as_" + str(cell['id']), use_container_width=True)

            if run_btn:
                buf = io.StringIO()
                try:
                    with contextlib.redirect_stdout(buf):
                        exec(cell["code"], {})
                    cell["output"] = buf.getvalue() if buf.getvalue() else "[Finished with zero return output]"
                    cell["error"] = ""
                except Exception as ex:
                    cell["output"] = ""
                    cell["error"] = str(ex)

            if assist_btn:
                with st.spinner("AI checking cell..."):
                    sys_prompt = "Optimize this python code cleanly and suggest best practices."
                    cell["output"] = execute_ai_query(sys_prompt, "Analyze:\n" + cell['code'])
                    cell["error"] = ""

            if cell["output"]:
                st.code(cell["output"])
            if cell["error"]:
                st.error(cell["error"])
