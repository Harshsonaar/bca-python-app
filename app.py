import streamlit as st
import google.generativeai as genai
import io
import contextlib
import time
from PIL import Image

st.set_page_config(
    page_title="BCA Master Ecosystem | MLK PG College Balrampur",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Session state initialization
if "app_entered" not in st.session_state:
    st.session_state.app_entered = False

if "selected_subject" not in st.session_state:
    st.session_state.selected_subject = "🐍 Python Programming"

if "current_note_page" not in st.session_state:
    st.session_state.current_note_page = 1

if "dynamic_pages_list" not in st.session_state:
    st.session_state.dynamic_pages_list = []

# ================= ULTRA-PREMIUM APPLE FROSTED GLASS & STRICT A4 REGISTER CSS =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Architects+Daughter&family=Patrick+Hand&display=swap');

    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Plus Jakarta Sans", "SF Pro Display", sans-serif;
    }
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Ambient Apple Dark Background */
    .stApp {
        background: radial-gradient(circle at 50% 0%, rgba(30, 41, 69, 0.75) 0%, rgba(10, 13, 20, 0.98) 75%);
        color: #F1F5F9;
    }

    /* Streamlit Host Header, Badges & Footers Elimination */
    header[data-testid="stHeader"] {display: none !important;}
    footer {display: none !important; visibility: hidden !important;}
    .viewerBadge_container__1QSob, 
    .viewerBadge_link__1QSob,
    [data-testid="stStatusWidget"], 
    .stDeployButton,
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"],
    #MainMenu,
    div[class*="viewerBadge"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    /* Page Bottom Padding */
    .block-container {
        padding-top: 15px !important;
        padding-bottom: 180px !important;
    }

    /* Splash Screen */
    .splash-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 65vh;
        text-align: center;
        margin-top: 30px;
    }
    .creator-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(139, 92, 246, 0.15);
        border: 1px solid rgba(168, 85, 247, 0.4);
        padding: 8px 24px;
        border-radius: 40px;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #C084FC;
        box-shadow: 0 0 25px rgba(168, 85, 247, 0.35);
        margin-bottom: 18px;
    }
    .splash-title {
        font-size: 52px;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 0%, #A5B4FC 35%, #38BDF8 70%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 12px;
        letter-spacing: -1.5px;
    }
    .splash-subtitle {
        font-size: 16px;
        color: #94A3B8;
        max-width: 680px;
        line-height: 1.6;
        margin-bottom: 24px;
    }
    .creator-signature {
        font-size: 22px;
        font-weight: 700;
        color: #38BDF8;
        background: rgba(255, 255, 255, 0.04);
        padding: 10px 28px;
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(16px);
        margin-bottom: 30px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
    }

    /* Hero Banner */
    .hero-banner {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 18px 24px;
        border-radius: 18px;
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.45);
        margin-bottom: 16px;
    }
    .hero-title {
        font-size: 24px;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 0%, #A5B4FC 50%, #38BDF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }
    .hero-sub {
        font-size: 13px;
        color: #94A3B8;
        letter-spacing: 0.2px;
    }

    /* Apple Glass Card */
    .apple-glass-card {
        background: rgba(255, 255, 255, 0.035);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px;
        padding: 24px;
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        box-shadow: 0 16px 36px rgba(0, 0, 0, 0.35);
        margin-top: 24px;
    }

    /* ================= CRISP GLITCH-FREE REGISTER CONTAINER ================= */
    .register-flip-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 10px;
        margin-bottom: 14px;
    }
    
    .register-outer-card {
        background-color: #ffffff !important;
        /* Ruled Red Vertical Margin + Precise 26px Blue Horizontal Lines */
        background-image: 
            linear-gradient(90deg, transparent 40px, #ef4444 40px, #ef4444 41.5px, transparent 41.5px),
            linear-gradient(#e2e8f0 1px, transparent 1px) !important;
        background-size: 100% 100%, 100% 26px !important;
        border-radius: 6px !important;
        padding: 20px 22px 20px 52px !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6) !important;
        width: 100% !important;
        max-width: 520px !important;
        aspect-ratio: 1 / 1.38 !important;
        overflow: hidden !important;
        box-sizing: border-box !important;
        position: relative !important;
    }

    /* Spiral Holes */
    .register-outer-card::before {
        content: '' !important;
        position: absolute !important;
        top: 12px !important;
        left: 11px !important;
        width: 10px !important;
        height: 94% !important;
        background-image: radial-gradient(circle, #cbd5e1 3.5px, transparent 4.5px) !important;
        background-size: 10px 26px !important;
        background-repeat: repeat-y !important;
    }

    /* High Clarity Student Ink Styling */
    .register-inner-content {
        font-family: 'Patrick Hand', 'Architects Daughter', cursive, sans-serif !important;
        color: #1e3a8a !important;
        font-size: 15.5px !important;
        line-height: 26px !important;
        word-break: break-word !important;
    }

    .register-inner-content h1, .register-inner-content h2, .register-inner-content h3 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #0f172a !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        margin-top: 4px !important;
        margin-bottom: 6px !important;
        border-bottom: 1.5px solid #ef4444 !important;
        padding-bottom: 2px !important;
        line-height: 22px !important;
    }

    .register-inner-content p, .register-inner-content li {
        font-family: 'Patrick Hand', cursive !important;
        color: #1e293b !important;
        font-size: 15.5px !important;
        line-height: 26px !important;
        margin-bottom: 4px !important;
        letter-spacing: 0.2px !important;
    }

    .register-inner-content strong, .register-inner-content b {
        color: #0f172a !important;
        font-weight: 700 !important;
    }

    .page-turn-pill {
        display: inline-block;
        background: #ef4444;
        color: #ffffff;
        font-size: 11px;
        font-weight: 700;
        padding: 1px 8px;
        border-radius: 8px;
        margin-bottom: 6px;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        letter-spacing: 0.5px;
    }

    /* AI Response Glass Box */
    .ai-box {
        background: rgba(20, 24, 38, 0.88);
        border: 1px solid rgba(139, 92, 246, 0.35);
        border-left: 4px solid #8B5CF6;
        border-radius: 14px;
        padding: 20px;
        margin-top: 14px;
        color: #F8FAFC;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        line-height: 1.65;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.45);
    }

    /* Apple-style Gradient Buttons */
    .stButton>button {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.9) 0%, rgba(147, 51, 234, 0.9) 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 7px 18px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        letter-spacing: 0.3px !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 6px 18px rgba(59, 130, 246, 0.25) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 10px 24px rgba(147, 51, 234, 0.4) !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
    }

    /* Radio circular selection dot hide */
    div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }

    /* ZERO-OVERLAP TOP STICKY NAVIGATION DOCK */
    div[data-testid="stRadio"] {
        position: sticky !important;
        top: 10px !important;
        z-index: 999999 !important;
        background: rgba(18, 24, 38, 0.94) !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        padding: 6px 14px !important;
        border-radius: 40px !important;
        backdrop-filter: blur(28px) saturate(190%) !important;
        -webkit-backdrop-filter: blur(28px) saturate(190%) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.75), inset 0 1px 1px rgba(255, 255, 255, 0.2) !important;
        margin: 8px auto 18px auto !important;
        width: max-content !important;
        max-width: 95vw !important;
    }

    div[data-testid="stRadio"] > label {
        display: none !important;
    }

    div[data-testid="stRadio"] > div {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 6px !important;
        align-items: center !important;
        justify-content: center !important;
    }

    div[data-testid="stRadio"] label {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 18px !important;
        padding: 6px 14px !important;
        margin: 0 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        color: #CBD5E1 !important;
        white-space: nowrap !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
    }

    div[data-testid="stRadio"] label:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        color: #FFFFFF !important;
    }

    /* MOBILE SCREEN SPECIFICS (< 768px) */
    @media (max-width: 768px) {
        .splash-title {
            font-size: 32px !important;
        }
        .hero-title {
            font-size: 19px !important;
        }
        div[data-testid="stRadio"] {
            top: 6px !important;
            padding: 5px 6px !important;
            width: 95vw !important;
            max-width: 95vw !important;
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
            scrollbar-width: none !important;
            margin-bottom: 14px !important;
        }
        div[data-testid="stRadio"]::-webkit-scrollbar {
            display: none !important;
        }
        div[data-testid="stRadio"] > div {
            display: inline-flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            gap: 5px !important;
            width: max-content !important;
            justify-content: flex-start !important;
            padding: 2px 4px !important;
        }
        div[data-testid="stRadio"] label {
            padding: 5px 10px !important;
            font-size: 12px !important;
            border-radius: 16px !important;
            flex-shrink: 0 !important;
        }
        .register-outer-card {
            padding: 16px 12px 16px 44px !important;
            max-width: 92vw !important;
            aspect-ratio: 1 / 1.38 !important;
        }
        .register-inner-content p, .register-inner-content li {
            font-size: 14px !important;
            line-height: 24px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ================= BACKGROUND API SETUP =================
gemini_key = None
if "GEMINI_API_KEY" in st.secrets:
    gemini_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=gemini_key)

with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")
    if gemini_key:
        st.markdown('<div class="badge-status">● Vision & Notes Active</div>', unsafe_allow_html=True)
    else:
        with st.expander("🔑 Setup API Key", expanded=True):
            gemini_key = st.text_input("Gemini API Key:", type="password")
            if gemini_key:
                genai.configure(api_key=gemini_key)
                st.success("Connected!")
    st.caption("Crafted with ❤️ by Raj • MLK PG College Balrampur")

def get_ai_response(prompt, image_input=None, forced_language=None, current_subject="Python"):
    if not gemini_key:
        return "⚠️ Pehle Gemini API Key configure karein."
    
    candidate_models = [
        "models/gemini-3.5-flash-lite",
        "models/gemini-3.8-flash",
        "models/gemini-2.0-flash"
    ]
    
    if forced_language:
        lang_instruction = f"Strictly generate the output in {forced_language}."
    else:
        lang_instruction = (
            "Detect user's input language naturally (English, Hinglish, Hindi in Devanagari) "
            "and match it with direct clarity."
        )

    optimized_prompt = f"""
    You are a senior computer science professor for BCA at MLK PG College, Balrampur (affiliated with Maa Pateshwari State University).
    Subject: {current_subject}
    {lang_instruction}

    TEACHING RULES (STRICT CLEANLINESS):
    1. Write in natural, clean student notebook register style.
    2. NEVER output raw markdown hashes like '###' or raw unformatted LaTeX with broken dollar signs. Write formulas simply (e.g. 0/0 form, limit x -> a).
    3. DO NOT write meta lines like '**Subject:** ...' or '**Author:** ...' or '**Instructor:** ...'. Jump straight to the point.
    4. Keep content tightly limited to 60-80 words per page to ensure zero vertical scrolling on a fixed A4 sheet.
    5. Separate every single page using the exact delimiter token '[PAGE_BREAK]'.

    Query:
    {prompt}
    """
    
    content_payload = [optimized_prompt]
    if image_input:
        content_payload.append(image_input)
    
    last_error = ""
    for model_name in candidate_models:
        for attempt in range(2):
            try:
                model = genai.GenerativeModel(
                    model_name=model_name,
                    generation_config={"temperature": 0.25}
                )
                response = model.generate_content(
                    content_payload,
                    request_options={"timeout": 60.0}
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                last_error = str(e)
                if "429" in last_error:
                    time.sleep(1.0)
                    break
                elif "504" in last_error or "deadline" in last_error.lower():
                    time.sleep(1.0)
                    continue

    return f"⏳ AI Engine Temporary Busy: {last_error}"

# ================= 0. OPENING SCREEN =================
if not st.session_state.app_entered:
    st.markdown("""
    <div class="splash-container">
        <div class="creator-badge">✨ Next-Gen BCA Ecosystem</div>
        <div class="splash-title">MLK BCA Academic Portal</div>
        <div class="creator-signature">Crafted & Created by Raj ⚡</div>
        <div class="splash-subtitle">
            Autonomous curriculum for MLK PG College, Balrampur (Maa Pateshwari State University).
            Complete syllabus coverage for Python Programming, CSA & Discrete Mathematics with Dynamic A4 Register Notes and Multimodal Vision.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        if st.button("🚀 Launch Portal & Start Studying", use_container_width=True):
            st.session_state.app_entered = True
            st.rerun()

else:
    # Top Bar Header
    top_col1, top_col2 = st.columns([1.6, 1.4])
    with top_col1:
        st.markdown("""
        <div style="padding-top: 10px;">
            <span style="font-size: 13px; color: #94A3B8;">🏛️ MLK PG College Balrampur (Maa Pateshwari Univ)</span><br>
            <span style="font-size: 14px; font-weight: 700; color: #38BDF8;">⚡ Created by Raj</span>
        </div>
        """, unsafe_allow_html=True)
    with top_col2:
        st.session_state.selected_subject = st.selectbox(
            "Select Subject Slot:",
            [
                "🐍 Python Programming",
                "🖥️ Computer System Architecture",
                "📐 Mathematics & Numerical Methods"
            ],
            index=0
        )

    # ================= TOP STICKY NAVIGATION BAR =================
    selected_tab = st.radio(
        label="Top Navigation Bar",
        options=[
            "📖 Syllabus",
            "📝 Handwritten Notes",
            "📝 Exam Engine",
            "🛠️ Projects",
            "🤖 AI Mentor",
            "🧪 Sandbox"
        ],
        horizontal=True,
        index=1
    )

    # ================= 1. MULTI-SUBJECT SYLLABUS HUB =================
    def render_syllabus():
        active_subj = st.session_state.selected_subject

        if active_subj == "🐍 Python Programming":
            st.markdown("""
            <div class="hero-banner">
                <div class="hero-title">Python Programming Encyclopedia</div>
                <div class="hero-sub">MLK PG College Balrampur • Full Theory, Solved Exam Questions & Practical Labs</div>
            </div>
            """, unsafe_allow_html=True)

            py_modules = [
                "Module 1: Language Basics, Operators & Bitwise",
                "Module 2: Control Flow & Iteration (Branches & Loops)",
                "Module 3: Functions, Scopes, Lambdas & Recursion",
                "Module 4: In-Depth Data Structures (Lists, Tuples, Dicts, Sets)",
                "Module 5: Object-Oriented Programming (OOP Architecture)",
                "Module 6: File Handling, Context Managers & JSON/CSV",
                "Module 7: Exception Handling & Custom Errors",
                "Module 8: Standard Libraries, Regex & Date-Time"
            ]
            sel_mod = st.selectbox("📚 Select Python Module:", py_modules)

            if sel_mod == "Module 1: Language Basics, Operators & Bitwise":
                with st.expander("1. Python Architecture, Bytecode Compilation & Dynamic Typing", expanded=True):
                    st.write("""
                    * Source code (`.py`) compile hokar **Bytecode (`.pyc`)** banta hai, aur fir **PVM** ise line-by-line run karti hai.
                    * **Dynamic Typing:** Variables runtime par value ke mutabik type acquire karte hain.
                    """)
                    st.code("""x = 101           # int
x = "Raj Shraff"  # dynamically becomes string
print(x, type(x))""", language="python")

            elif sel_mod == "Module 2: Control Flow & Iteration (Branches & Loops)":
                with st.expander("1. Decisions & for-else Loop Trick", expanded=True):
                    st.write("Loop ka `else` block tabhi run hota hai jab loop bina `break` statement ke naturally complete ho.")
                    st.code("""num = 29
for factor in range(2, int(num**0.5) + 1):
    if num % factor == 0:
        print(f"{num} is composite")
        break
else:
    print(f"{num} is Prime!")""", language="python")

            elif sel_mod == "Module 3: Functions, Scopes, Lambdas & Recursion":
                with st.expander("1. *args, **kwargs & Scopes", expanded=True):
                    st.code("""def register_student(name, *subjects, **stats):
    print(f"Student: {name} | Subjects: {subjects} | Stats: {stats}")

register_student("Raj", "Python", "CSA", sem=1)""", language="python")

            elif sel_mod == "Module 4: In-Depth Data Structures (Lists, Tuples, Dicts, Sets)":
                with st.expander("1. List Comprehensions & Dictionaries", expanded=True):
                    st.code("""scores = {"Python": 95, "CSA": 88, "Maths": 92}
high = {k: v for k, v in scores.items() if v >= 90}
print("High Scorers:", high)""", language="python")

            elif sel_mod == "Module 5: Object-Oriented Programming (OOP Architecture)":
                with st.expander("1. Classes, Encapsulation & Magic Methods", expanded=True):
                    st.code("""class BCAStudent:
    def __init__(self, name, roll):
        self.name = name
        self.__roll = roll
    def get_roll(self): return self.__roll

s = BCAStudent("Raj", 101)
print(s.name, s.get_roll())""", language="python")

            elif sel_mod == "Module 6: File Handling, Context Managers & JSON/CSV":
                with st.expander("1. File Modes & JSON", expanded=True):
                    st.code("""import json
data = {"name": "Raj", "degree": "BCA"}
print(json.dumps(data, indent=2))""", language="python")

            elif sel_mod == "Module 7: Exception Handling & Custom Errors":
                with st.expander("1. try-except-else-finally", expanded=True):
                    st.code("""try:
    val = 10 / 2
except ZeroDivisionError:
    print("Cannot divide by zero")
else:
    print("Success:", val)""", language="python")

            elif sel_mod == "Module 8: Standard Libraries, Regex & Date-Time":
                with st.expander("1. Regex Pattern Matching", expanded=True):
                    st.code("""import re
text = "Student Raj, Email: raj@example.com"
print(re.findall(r'[\w\.-]+@[\w\.-]+', text))""", language="python")

        elif active_subj == "🖥️ Computer System Architecture":
            st.markdown("""
            <div class="hero-banner">
                <div class="hero-title">Computer System Architecture (CSA) Master</div>
                <div class="hero-sub">MLK PG College Balrampur • Digital Logic, Adders, Memory & CPU Architecture</div>
            </div>
            """, unsafe_allow_html=True)

            csa_modules = [
                "Unit 1: Data Representation, Number Systems & 1's/2's Complements",
                "Unit 2: Logic Gates, Half Adder, Full Adder, K-Maps & Combinational Circuits",
                "Unit 3: Sequential Circuits, Flip-Flops, Registers & Counters",
                "Unit 4: Basic Computer Organization, Instruction Cycle & Bus Architecture",
                "Unit 5: Central Processing Unit (ALU, Addressing Modes & Pipeline)",
                "Unit 6: Memory Hierarchy (Cache Mapping, RAM/ROM & Virtual Memory)",
                "Unit 7: Input-Output Organization (Interrupts, DMA, Programmed I/O)"
            ]
            sel_mod = st.selectbox("📚 Select CSA Unit:", csa_modules)

            if sel_mod == "Unit 2: Logic Gates, Half Adder, Full Adder, K-Maps & Combinational Circuits":
                with st.expander("1. Half Adder & Full Adder Architecture", expanded=True):
                    st.write("""
                    * **Half Adder:** Sum = $A \\oplus B$, Carry = $A \\cdot B$.
                    * **Full Adder:** Sum = $A \\oplus B \\oplus C_{in}$, Carry = $AB + C_{in}(A \\oplus B)$.
                    * **Trick:** Ek Full Adder ko **2 Half Adders aur 1 OR gate** se banaya ja sakta hai!
                    """)
                    st.code("""def full_adder(a, b, cin):
    sum_bit = a ^ b ^ cin
    carry_bit = (a & b) | (cin & (a ^ b))
    return sum_bit, carry_bit

print("Full Adder (1, 1, 1):", full_adder(1, 1, 1))""", language="python")

        elif active_subj == "📐 Mathematics & Numerical Methods":
            st.markdown("""
            <div class="hero-banner">
                <div class="hero-title">Discrete Mathematics & Numerical Methods</div>
                <div class="hero-sub">MLK PG College Balrampur • Sets, Relations, Logic, Matrices, Calculus & Numerical Solvers</div>
            </div>
            """, unsafe_allow_html=True)

            math_modules = [
                "Unit 1: Set Theory, Relations, Functions & POSET",
                "Unit 2: Mathematical Logic, Truth Tables & Propositional Calculus",
                "Unit 3: Matrices, Determinants, Rank & System of Linear Equations",
                "Unit 4: Combinatorics, Pigeonhole Principle & Graph Theory",
                "Unit 5: Differential Calculus, Leibnitz's Theorem & Maxima/Minima",
                "Unit 6: Numerical Methods (Newton-Raphson, Bisection & Gauss Elimination)"
            ]
            sel_mod = st.selectbox("📚 Select Mathematics Unit:", math_modules)

            if sel_mod == "Unit 6: Numerical Methods (Newton-Raphson, Bisection & Gauss Elimination)":
                with st.expander("1. Newton-Raphson Method Formula & Code Solver", expanded=True):
                    st.write("""
                    * Formula: $x_{n+1} = x_n - \\frac{f(x_n)}{f'(x_n)}$ (Quadratic convergence, Order = 2).
                    """)
                    st.code("""f = lambda x: x**3 - x - 2
df = lambda x: 3*x**2 - 1
x = 1.5
for i in range(3):
    x = x - f(x)/df(x)
    print(f"Iter {i+1}: x = {x:.5f}")""", language="python")

        st.markdown(f"""
        <div class="apple-glass-card">
            <h3 style="margin-top:0; font-size:20px; font-weight:700;">🎯 AI University Exam Preparation & Viva Master ({active_subj})</h3>
            <p style="color:#94A3B8; font-size:13px; margin-bottom:14px;">MLK PG College exam questions aur viva points generate karein:</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔥 Generate Most Important Exam Questions & Viva Points", use_container_width=True):
            with st.spinner(f"AI Professor analyzing {active_subj}..."):
                prompt = f"""
                You are a senior BCA university examiner for MLK PG College, Balrampur.
                Subject: {active_subj}
                Provide top 3 high-weightage questions with step-by-step model answers and shortcut tricks.
                """
                ai_output = get_ai_response(prompt, current_subject=active_subj)
                st.markdown(f'<div class="ai-box">{ai_output}</div>', unsafe_allow_html=True)

    # ================= 2. CRISP GLITCH-FREE REGISTER NOTES =================
    def render_handwritten_notes():
        active_subj = st.session_state.selected_subject
        st.markdown(f"""
        <div class="hero-banner">
            <div class="hero-title">📝 Authentic A4 Register Sheets (Zero Glitch)</div>
            <div class="hero-sub">Subject Context: {active_subj} • Clean natural student ink notes on exact A4 sheets with zero scroll.</div>
        </div>
        """, unsafe_allow_html=True)

        if active_subj == "🐍 Python Programming":
            suggested_topics = [
                "Python Bytecode & Dynamic Typing vs Static Typing",
                "Operators Hierarchy & Bitwise Left/Right Shift Tricks",
                "Loop-Else Construct & Prime Number Logic",
                "*args, **kwargs & LEGB Scope Resolution Rules",
                "List vs Tuple Memory Architecture & Dict Hash Tables",
                "OOP Encapsulation, Mangling & Dunder Magic Methods",
                "File Handling seek(), tell() & Context Managers",
                "Regex Pattern Matching with re module"
            ]
        elif active_subj == "🖥️ Computer System Architecture":
            suggested_topics = [
                "Truth Table Chart of Full Adder & Circuit with 2 HA",
                "2's Complement Direct Trick & Overflow Detection",
                "Half Adder & Full Adder Design using 2 HA and 1 OR Gate",
                "K-Map 4-Variable Minimization & Grouping Strategy",
                "JK Flip-Flop Race-Around Condition & Master-Slave Solution",
                "Instruction Cycle Phases (T0-T4 Micro-operations)",
                "Addressing Modes Comparison with Real Examples",
                "Cache Memory Mapping (Direct vs Associative vs Set-Associative)",
                "DMA Controller Working: Cycle Stealing vs Burst Mode"
            ]
        else:
            suggested_topics = [
                "L'Hopital's Rule for Indeterminate Forms (0/0 and inf/inf)",
                "Equivalence Relations Proof (Reflexive, Symmetric, Transitive)",
                "POSET & Hasse Diagram Construction Rules",
                "Truth Table Proof of Conditional Equivalence (~p v q)",
                "Rank of Matrix using Echelon Form & Consistency of AX=B",
                "Cayley-Hamilton Theorem & Fast Inverse A^-1 Calculation",
                "Handshaking Theorem & Euler Planar Formula (V - E + R = 2)",
                "Leibnitz's Theorem for n-th Derivative with Product Trick",
                "Newton-Raphson Method with Step-by-Step Numerical Root"
            ]

        col1, col2 = st.columns([2, 1])
        with col1:
            chosen_topic = st.selectbox("Select Topic for Notes:", suggested_topics)
            custom_topic = st.text_input("Or enter custom topic from syllabus (Optional):", placeholder="e.g. L'Hopital's rule / Multiplexer cascading")
        with col2:
            notes_lang = st.selectbox("Notes Language:", ["Hinglish (Simple Student Language)", "English", "Hindi (हिन्दी)"])

        final_topic = custom_topic.strip() if custom_topic.strip() else chosen_topic

        if st.button("✍️ Write on A4 Register Sheets", use_container_width=True):
            st.session_state.current_note_page = 1
            with st.spinner(f"Creating glitch-free A4 register notes for {final_topic}..."):
                master_prompt = f"""
                You are a university topper writing authentic A4 register notes for '{final_topic}' in {active_subj}.
                Language: {notes_lang}.

                STRICT GUIDELINES:
                1. DO NOT output raw markdown tags like '###' or raw LaTeX backslashes that glitch.
                2. DO NOT write meta intro like 'Subject:', 'Instructor:', 'Author:' etc.
                3. Keep each page strictly between 50-70 words so that it fits completely on the A4 sheet without scrolling.
                4. Insert '[PAGE_BREAK]' between pages.
                5. Structure across pages:
                   - Page 1: Core Meaning & When to use (in 3 simple points).
                   - Page 2: Key Formula / Working Rule & Memory Trick.
                   - Page 3: Solved Exam Numerical / Question with steps.
                   - Page 4: Pitfalls to avoid in exams.
                """

                raw_notes = get_ai_response(master_prompt, forced_language=notes_lang, current_subject=active_subj)
                
                # Dynamic page split
                pages = [p.strip() for p in raw_notes.split("[PAGE_BREAK]") if p.strip()]
                if not pages:
                    pages = [raw_notes]

                # Clean any stray raw markdown hashes from start of lines
                clean_pages = []
                for pg in pages:
                    cleaned_lines = []
                    for line in pg.splitlines():
                        if line.startswith("### "):
                            line = f"**{line.replace('### ', '')}**"
                        elif line.startswith("## "):
                            line = f"**{line.replace('## ', '')}**"
                        elif line.startswith("# "):
                            line = f"**{line.replace('# ', '')}**"
                        cleaned_lines.append(line)
                    clean_pages.append("\n\n".join(cleaned_lines))

                st.session_state.dynamic_pages_list = clean_pages
                st.session_state.flip_notes_topic = final_topic

        # RENDER CRISP GLITCH-FREE REGISTER CARD
        if st.session_state.dynamic_pages_list:
            pages = st.session_state.dynamic_pages_list
            total_pages = len(pages)
            curr_pg = min(st.session_state.current_note_page, total_pages)

            current_page_text = pages[curr_pg - 1]

            st.markdown(f"""
            <div class="register-flip-container">
                <div class="register-outer-card">
                    <span class="page-turn-pill">A4 SHEET {curr_pg} OF {total_pages}</span>
                    <div style="font-family:'Plus Jakarta Sans', sans-serif; font-size:18px; font-weight:700; color:#0f172a; margin-bottom:2px; border-bottom:1.5px solid #ef4444; padding-bottom:2px;">
                        {st.session_state.get('flip_notes_topic')}
                    </div>
                    <div style="font-size:11px; color:#64748b; margin-bottom:8px; font-family:'Plus Jakarta Sans', sans-serif;">
                        <b>Subject:</b> {active_subj} | <b>MLK PG College Balrampur</b>
                    </div>
                    <div class="register-inner-content">
            """, unsafe_allow_html=True)

            # Native Streamlit rendering for crisp LaTeX & markdown without glitches
            st.markdown(current_page_text)

            st.markdown("""
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # SINGLE CLEAN PAGINATION CONTROLS
            c1, c2, c3 = st.columns([1.2, 1.6, 1.2])
            with c1:
                if st.button("◀ Previous Page", disabled=(curr_pg == 1), key="btn_prev", use_container_width=True):
                    st.session_state.current_note_page = max(1, curr_pg - 1)
                    st.rerun()
            with c2:
                st.markdown(f"""
                <div style="text-align:center; padding-top:6px;">
                    <span style="color:#94A3B8; font-size:12px; font-weight:600;">Sheet {curr_pg} of {total_pages}</span>
                </div>
                """, unsafe_allow_html=True)
            with c3:
                if st.button("Next Page ▶", disabled=(curr_pg == total_pages), key="btn_next", use_container_width=True):
                    st.session_state.current_note_page = min(total_pages, curr_pg + 1)
                    st.rerun()

    # ================= 3. EXAM ENGINE (WITH PHOTO ANSWER UPLOAD) =================
    def render_exam_engine():
        active_subj = st.session_state.selected_subject
        st.markdown(f"""
        <div class="hero-banner">
            <div class="hero-title">Automated Exam Engine ({active_subj})</div>
            <div class="hero-sub">MLK PG College Balrampur Paper Generator • Instant AI Checking with Text or Handwritten Answer Sheet Photo</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1.5, 1])
        with col1:
            test_scope = st.text_input(
                f"Enter Specific Topic / Chapter for {active_subj}:",
                placeholder="e.g. Cache Mapping / Full Adder / Eigenvalues / K-Maps"
            )
        with col2:
            test_lang = st.selectbox(
                "Paper Language:",
                ["English", "Hinglish (Hindi in Latin Script)", "Hindi (हिन्दी - देवनागरी)"]
            )
        
        if st.button("⚡ Generate University Test Paper", use_container_width=True):
            with st.spinner(f"Drafting fresh exam questions for {active_subj} in {test_lang}..."):
                topic_focus = test_scope if test_scope.strip() else "Entire University Syllabus"
                test_prompt = f"""
                Create a 15-mark university-standard BCA examination paper on '{active_subj}' focusing on '{topic_focus}'.
                Curriculum: MLK PG College, Balrampur (Maa Pateshwari State University).
                
                Paper Structure:
                - Section A (3 Marks): Short conceptual definition.
                - Section B (5 Marks): Output prediction, difference table, or conceptual diagram/derivation.
                - Section C (7 Marks): Comprehensive problem (Practical code for Python / Circuit-Tracing for CSA / Numerical for Maths).
                
                Strictly in {test_lang}. Do NOT give answers yet.
                """
                st.session_state.current_test = get_ai_response(test_prompt, forced_language=test_lang, current_subject=active_subj)
                st.session_state.test_lang_selected = test_lang
                st.session_state.test_subject_selected = active_subj

        if "current_test" in st.session_state:
            st.markdown(f'<div class="apple-glass-card"><h4>📄 Question Paper: {st.session_state.get("test_subject_selected")} ({st.session_state.get("test_lang_selected")})</h4>{st.session_state.current_test}</div>', unsafe_allow_html=True)

            st.markdown("#### ✍️ Submit Answers (Text or Upload Photo)")
            user_sol = st.text_area("Option A: Yahan apne answers type karein:", height=150, placeholder="Ans 1: ...\nAns 2: ...\nAns 3: ...")
            
            uploaded_answer_img = st.file_uploader("Option B: Ya fir Handwritten Answer Sheet ki Photo Upload Karein (JPG/PNG):", type=["png", "jpg", "jpeg"], key="exam_upload")
            pil_ans_img = None
            if uploaded_answer_img:
                pil_ans_img = Image.open(uploaded_answer_img)
                st.image(pil_ans_img, caption="Uploaded Answer Sheet Preview", width=250)

            if st.button("🚀 Submit Sheet For AI Checking", use_container_width=True):
                if not user_sol.strip() and not pil_ans_img:
                    st.warning("Please type your answer or upload a photo of your sheet.")
                else:
                    with st.spinner("AI Professor checking answer sheet (Vision Analysis Active)..."):
                        target_eval_lang = st.session_state.get("test_lang_selected", "English")
                        eval_prompt = f"""
                        You are a strict BCA university examiner at MLK PG College, Balrampur grading this answer sheet.
                        Subject: {st.session_state.get('test_subject_selected')}
                        Paper:
                        {st.session_state.current_test}

                        Student Text Answer (if any):
                        {user_sol}

                        Evaluate thoroughly in {target_eval_lang}:
                        1. Score out of 15 with section-wise marks breakdown.
                        2. Strengths and missing conceptual elements.
                        3. Complete university model answers.
                        """
                        scorecard = get_ai_response(eval_prompt, image_input=pil_ans_img, forced_language=target_eval_lang, current_subject=st.session_state.get('test_subject_selected'))
                        st.markdown(f'<div class="ai-box"><h3>📊 University Scorecard</h3>{scorecard}</div>', unsafe_allow_html=True)

    # ================= 4. GUIDED PROJECTS LAB =================
    def render_projects():
        active_subj = st.session_state.selected_subject
        st.markdown(f"""
        <div class="hero-banner">
            <div class="hero-title">Academic Capstone Projects & Lab Blueprints</div>
            <div class="hero-sub">Subject Context: {active_subj} • Production-grade architecture with verified logic and viva preparation.</div>
        </div>
        """, unsafe_allow_html=True)

        if active_subj == "🐍 Python Programming":
            proj_list = [
                "Student Management System (Console + File / SQLite)",
                "Banking Operations & ATM Simulator (OOPs Based)",
                "Supermarket Inventory & Automated Billing Engine",
                "Hospital Management & Patient Appointment Scheduler",
                "Library Book Circulation & Fine Calculation Engine"
            ]
        elif active_subj == "🖥️ Computer System Architecture":
            proj_list = [
                "Half & Full Adder Simulator with Ripple Carry Circuit",
                "4-Bit ALU Software Simulator (Logic Gates & Arithmetic)",
                "Direct-Mapped vs Set-Associative Cache Memory Simulator",
                "8-Bit Instruction Set Architecture (ISA) & CPU Emulator",
                "Booth's Multiplication Algorithm Simulator with Step Tracing"
            ]
        else:
            proj_list = [
                "Numerical Equation Solver (Newton-Raphson & Bisection Method)",
                "Matrix Linear System Solver & Eigenvalues Calculator",
                "Graph Theory Analyzer (Shortest Path Dijkstra & Euler Circuit)",
                "Boolean Truth Table & Logic Minimization Engine",
                "Statistical Curve Fitting & Regression Analysis Calculator"
            ]

        proj = st.selectbox(f"Choose Project for {active_subj}:", proj_list)

        st.markdown(f"""
        <div class="apple-glass-card">
            <h4 style="margin-top:0;">🏗️ Project Architecture: {proj}</h4>
            <p>Complete design pattern aligned with BCA Semester academic requirements and university practical viva.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Get Starter Architecture & Complete Code / Proof", use_container_width=True):
            with st.spinner("AI Architect designing codebase..."):
                blueprint_prompt = f"""
                Provide a complete, production-grade, well-commented implementation for: '{proj}' under the subject '{active_subj}'.
                Include design architecture, error checking, runnable implementation, and 3 expected examiner viva questions.
                """
                st.markdown(f'<div class="ai-box">{get_ai_response(blueprint_prompt, current_subject=active_subj)}</div>', unsafe_allow_html=True)

    # ================= 5. 24/7 AI CODE & SUBJECT MENTOR (WITH PHOTO UPLOAD) =================
    def render_mentor():
        active_subj = st.session_state.selected_subject
        st.markdown(f"""
        <div class="hero-banner">
            <div class="hero-title">24/7 AI Technical Mentor ({active_subj})</div>
            <div class="hero-sub">Resolve doubts, code logic errors, numerical proofs, or circuit diagrams. Type or upload a photo!</div>
        </div>
        """, unsafe_allow_html=True)

        user_q = st.text_area(
            f"Poochhein apna doubt for {active_subj} (Hindi, English, ya Hinglish mein):",
            height=120,
            placeholder=f"e.g. Is problem ko solve karo ya error explain karo for {active_subj}..."
        )
        
        uploaded_mentor_file = st.file_uploader(
            "📷 Question / Error / Circuit / Book Page ki Photo Upload Karein (Optional):",
            type=["png", "jpg", "jpeg"],
            key="mentor_upload"
        )
        pil_mentor_img = None
        if uploaded_mentor_file:
            pil_mentor_img = Image.open(uploaded_mentor_file)
            st.image(pil_mentor_img, caption="Uploaded Image Preview", width=280)

        if st.button("⚡ Ask AI Mentor", use_container_width=True):
            if not user_q.strip() and not pil_mentor_img:
                st.warning("Pehle apna sawal enter karein ya photo upload karein.")
            else:
                with st.spinner(f"AI Mentor analyzing query & image for {active_subj}..."):
                    ans = get_ai_response(user_q, image_input=pil_mentor_img, current_subject=active_subj)
                    st.markdown(f'<div class="ai-box">{ans}</div>', unsafe_allow_html=True)

    # ================= 6. LIVE RUNNER SANDBOX =================
    def render_runner():
        active_subj = st.session_state.selected_subject
        st.markdown(f"""
        <div class="hero-banner">
            <div class="hero-title">Interactive Python & Algorithm Sandbox</div>
            <div class="hero-sub">Test Python programs, numerical algorithms, or CSA binary logic simulations directly in your browser.</div>
        </div>
        """, unsafe_allow_html=True)

        if active_subj == "🐍 Python Programming":
            starter = """# BCA Python Interactive Sandbox
def greet(name, college):
    return f"Hello {name}, Welcome to {college} BCA Portal!"

print(greet("Raj", "MLK PG College Balrampur"))
"""
        elif active_subj == "🖥️ Computer System Architecture":
            starter = """# CSA Binary Half Adder & Bitwise Logic Simulator
def test_half_adder(a, b):
    sum_bit = a ^ b
    carry_bit = a & b
    return f"A={a}, B={b} -> Sum={sum_bit}, Carry={carry_bit}"

print(test_half_adder(1, 1))
"""
        else:
            starter = """# Numerical Methods: Newton-Raphson Method
# Solve f(x) = x^2 - 25 = 0
def f(x): return x**2 - 25
def df(x): return 2*x

x0 = 10.0
for i in range(5):
    x0 = x0 - f(x0)/df(x0)
    print(f"Iteration {i+1}: Approximation = {x0:.6f}")
"""
        code_input = st.text_area("Code Editor:", value=starter, height=200)
        
        c1, c2 = st.columns([1, 1])
        with c1:
            run_btn = st.button("▶ Run Script", use_container_width=True)
        with c2:
            st.download_button(
                label="💾 Download Code (.py)",
                data=code_input,
                file_name="bca_code.py",
                mime="text/plain",
                use_container_width=True
            )

        if run_btn:
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf):
                    exec(code_input, {})
                output_str = buf.getvalue()
                st.success("Execution Successful")
                st.text_area("Console Output:", output_str if output_str else "[Program finished with no output]", height=120)
            except Exception as ex:
                st.error(f"Traceback Error: {ex}")

    # ================= TAB ROUTING =================
    if selected_tab == "📖 Syllabus":
        render_syllabus()
    elif selected_tab == "📝 Handwritten Notes":
        render_handwritten_notes()
    elif selected_tab == "📝 Exam Engine":
        render_exam_engine()
    elif selected_tab == "🛠️ Projects":
        render_projects()
    elif selected_tab == "🤖 AI Mentor":
        render_mentor()
    elif selected_tab == "🧪 Sandbox":
        render_runner()
