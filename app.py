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

# ================= ULTRA-PREMIUM APPLE FROSTED GLASS & MODERN UI CSS =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

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

    /* Streamlit Host Header, Badges & Footers Hide */
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

    /* Extra Page Bottom Padding - No content will ever get cut off */
    .block-container {
        padding-top: 20px !important;
        padding-bottom: 180px !important;
    }

    /* Premium Splash Screen Container */
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

    /* Hero Banner (Apple Glass) */
    .hero-banner {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 24px 30px;
        border-radius: 20px;
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.45);
        margin-bottom: 24px;
    }
    .hero-title {
        font-size: 30px;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 0%, #A5B4FC 50%, #38BDF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }
    .hero-sub {
        font-size: 14px;
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

    /* AI Response Glass Box */
    .ai-box {
        background: rgba(20, 24, 38, 0.88);
        border: 1px solid rgba(139, 92, 246, 0.35);
        border-left: 4px solid #8B5CF6;
        border-radius: 14px;
        padding: 22px;
        margin-top: 16px;
        color: #F8FAFC;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        line-height: 1.65;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.45);
    }

    /* Exam Question Callout Box */
    .solved-box {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(56, 189, 248, 0.4);
        border-left: 4px solid #38BDF8;
        padding: 16px 20px;
        border-radius: 12px;
        margin-top: 14px;
        margin-bottom: 14px;
    }

    /* Apple-style Gradient Buttons */
    .stButton>button {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.9) 0%, rgba(147, 51, 234, 0.9) 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        letter-spacing: 0.3px !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.25) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 12px 28px rgba(147, 51, 234, 0.4) !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
    }

    /* Radio circular selection dot hide (clean button look) */
    div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }

    /* ================= ZERO-OVERLAP TOP STICKY NAVIGATION DOCK ================= */
    div[data-testid="stRadio"] {
        position: sticky !important;
        top: 12px !important;
        z-index: 999999 !important;
        background: rgba(18, 24, 38, 0.94) !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        padding: 8px 16px !important;
        border-radius: 40px !important;
        backdrop-filter: blur(28px) saturate(190%) !important;
        -webkit-backdrop-filter: blur(28px) saturate(190%) !important;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.75), inset 0 1px 1px rgba(255, 255, 255, 0.2) !important;
        margin: 12px auto 26px auto !important;
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
        gap: 8px !important;
        align-items: center !important;
        justify-content: center !important;
    }

    div[data-testid="stRadio"] label {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 20px !important;
        padding: 7px 16px !important;
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

    /* MOBILE AUTO-DETECTION (< 768px Viewport) */
    @media (max-width: 768px) {
        .splash-title {
            font-size: 32px !important;
        }
        .hero-title {
            font-size: 20px !important;
        }
        .hero-banner {
            padding: 14px 16px !important;
        }
        .apple-glass-card {
            padding: 16px !important;
        }

        div[data-testid="stRadio"] {
            top: 8px !important;
            padding: 6px 8px !important;
            width: 95vw !important;
            max-width: 95vw !important;
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
            scrollbar-width: none !important;
            margin-bottom: 18px !important;
        }
        div[data-testid="stRadio"]::-webkit-scrollbar {
            display: none !important;
        }
        div[data-testid="stRadio"] > div {
            display: inline-flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            gap: 6px !important;
            width: max-content !important;
            justify-content: flex-start !important;
            padding: 2px 4px !important;
        }
        div[data-testid="stRadio"] label {
            padding: 6px 12px !important;
            font-size: 12px !important;
            border-radius: 18px !important;
            flex-shrink: 0 !important;
        }
    }

    .badge-status {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
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
        st.markdown('<div class="badge-status">● Vision & AI Mentor Active</div>', unsafe_allow_html=True)
    else:
        with st.expander("🔑 Setup API Key", expanded=True):
            gemini_key = st.text_input("Gemini API Key:", type="password")
            if gemini_key:
                genai.configure(api_key=gemini_key)
                st.success("Connected!")
    st.caption("Crafted with ❤️ by Raj • MLK PG College Balrampur")

# Multimodal Dynamic Auto-Tokens Engine with Vision Support & Subject Context
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
            "Detect the user's input language automatically (English, Hinglish, Hindi in Devanagari, etc.) "
            "and respond in the exact same language and script naturally."
        )

    optimized_prompt = f"""
    You are a distinguished university professor for BCA curriculum at MLK PG College, Balrampur (Affiliated with Maa Pateshwari State University).
    Current Active Subject Context: {current_subject}
    {lang_instruction}
    
    TEACHING RULES:
    1. Explain concepts in the most crystal-clear, intuitive, and easy language so the student never needs to re-read twice.
    2. Provide step-by-step methods, exam tricks/shortcuts, and direct formulas for every question.
    3. If an image is provided, thoroughly analyze handwritten questions, circuits, codes, or numerical formulas and solve completely.
    4. Provide verified code or mathematical steps without cutting off. No filler fluff.
    
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

    return f"⏳ AI Engine Temporary Busy. Details: {last_error}"

# ================= 0. OPENING SCREEN (CREATED BY RAJ) =================
if not st.session_state.app_entered:
    st.markdown("""
    <div class="splash-container">
        <div class="creator-badge">✨ Next-Gen BCA Ecosystem</div>
        <div class="splash-title">MLK BCA Academic Portal</div>
        <div class="creator-signature">Crafted & Created by Raj ⚡</div>
        <div class="splash-subtitle">
            Autonomous curriculum for MLK PG College, Balrampur (Maa Pateshwari State University).
            Complete syllabus coverage for Python Programming, Computer System Architecture & Discrete Mathematics with Exam Solved Questions, Tricks & Multimodal Vision.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        if st.button("🚀 Launch Portal & Start Studying", use_container_width=True):
            st.session_state.app_entered = True
            st.rerun()

else:
    # Top Bar with Right Corner Subject Switcher
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

    # ================= ZERO-OVERLAP TOP STICKY NAVIGATION DOCK =================
    selected_tab = st.radio(
        label="Top Navigation Bar",
        options=[
            "📖 Syllabus",
            "📝 Exam Engine",
            "🛠️ Projects",
            "🤖 AI Mentor",
            "🧪 Sandbox"
        ],
        horizontal=True,
        index=0
    )

    # ================= 1. MULTI-SUBJECT SYLLABUS HUB =================
    def render_syllabus():
        active_subj = st.session_state.selected_subject

        # ------------------- 1. PYTHON SYLLABUS -------------------
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
                    **Samjhein Seedhi Bhasha Mein:**
                    * Python hybrid language hai: Pehle Source Code (`.py`) compile hokar **Bytecode (`.pyc`)** banta hai, aur fir **Python Virtual Machine (PVM)** is bytecode ko line-by-line machine binary (0s aur 1s) mein convert karke run karti hai.
                    * **Dynamic Typing Trick:** C language ki tarah `int a;` nahi likhna padta. Jo value doge, variable wahi ban jayega!
                    """)
                    st.markdown("""
                    <div class="solved-box">
                        <b>📝 Exam Question:</b> Python dynamically typed kaise hai aur 'is' vs '==' mein kya antar hota hai? (5 Marks)<br>
                        <b>⚡ Trick to Remember:</b> <code>==</code> sirf <b>Value</b> dekhta hai, jabki <code>is</code> memory address (<b>ID</b>) dekhta hai!
                    </div>
                    """, unsafe_allow_html=True)
                    st.code("""# Demonstration of Dynamic Typing & Object Identity
x = 101
print(f"Value: {x} | Type: {type(x)} | Memory ID: {id(x)}")

x = "Raj Shraff"
print(f"Value: {x} | Type: {type(x)} | Memory ID: {id(x)}")

a = [1, 2, 3]
b = [1, 2, 3]
print("a == b (Values same hain):", a == b)      # True
print("a is b (Memory address alag hai):", a is b) # False""", language="python")

                with st.expander("2. Identifiers, Type Casting & Formatted I/O", expanded=False):
                    st.write("""
                    **Naming Rules & Shortcuts:**
                    * Variable name kabhi number se shuru nahi ho sakta (`1st_num` ❌, `num_1` ✅).
                    * **Type Casting:** `int()`, `float()`, `str()`. User input by-default hamesha `string` hoti hai, isliye number calculations ke liye `int(input())` lagana compulsory hai.
                    """)
                    st.code("""# Explicit Type Casting & Modern f-string trick
marks_input = "88"
converted = int(marks_input)
total = converted + 5
print(f"Student Marks: {converted} | With Grace: {total}")""", language="python")

                with st.expander("3. Complete Operators (Arithmetic, Bitwise, Logical)", expanded=False):
                    st.write("""
                    * Floor Division `//`: Decimal ko kaat kar quotient integer deta hai (`14 // 4 = 3`).
                    * Modulus `%`: Hamesha remainder deta hai (`14 % 4 = 2`).
                    * Bitwise Shortcuts: `x << n` ka matlab $x \\times 2^n$, aur `x >> n` ka matlab $x // 2^n$.
                    """)
                    st.code("""a, b = 14, 4
print("14 // 4 (Quotient):", a // b)
print("14 % 4  (Remainder):", a % b)
print("4 << 1  (4 * 2):", b << 1)
print("14 >> 1 (14 // 2):", a >> 1)""", language="python")

            elif sel_mod == "Module 2: Control Flow & Iteration (Branches & Loops)":
                with st.expander("1. Decisions & for-else Loop Trick", expanded=True):
                    st.write("""
                    * **Ternary Operator:** `pass_status = "Pass" if marks >= 40 else "Fail"`
                    * **Viva Trick (for-else):** Loop ke saath laga hua `else` block tabhi run hota hai jab loop bina `break` ke poora natural condition par end ho!
                    """)
                    st.markdown("""
                    <div class="solved-box">
                        <b>📝 Exam Question:</b> Write a program using loop-else construct to check if a number is prime. (5 Marks)
                    </div>
                    """, unsafe_allow_html=True)
                    st.code("""# Prime Number check via for-else
num = 29
for factor in range(2, int(num**0.5) + 1):
    if num % factor == 0:
        print(f"{num} is composite (divisible by {factor})")
        break
else:
    print(f"{num} is a Verified Prime Number (No break triggered)!")""", language="python")

            elif sel_mod == "Module 3: Functions, Scopes, Lambdas & Recursion":
                with st.expander("1. *args, **kwargs, Scopes & Recursion", expanded=True):
                    st.write("""
                    * `*args`: Jab pata na ho kitne arguments aayenge, ye unhe **Tuple** bana deta hai.
                    * `**kwargs`: Keyword arguments ko **Dictionary** bana deta hai.
                    * **LEGB Rule Shortcut:** Local $\\rightarrow$ Enclosing $\\rightarrow$ Global $\\rightarrow$ Built-in.
                    """)
                    st.code("""def register_student(name, *subjects, **stats):
    print(f"Student: {name}")
    print("Subjects Tuple:", subjects)
    print("Stats Dict:", stats)

register_student("Raj", "Python", "CSA", sem=1, college="MLK PG")""", language="python")

            elif sel_mod == "Module 4: In-Depth Data Structures (Lists, Tuples, Dicts, Sets)":
                with st.expander("1. List Comprehensions & Dictionary Hash Maps", expanded=True):
                    st.code("""matrix = [[1, 2], [3, 4]]
flattened = [item for row in matrix for item in row]
print("Flattened:", flattened)

scores = {"Python": 95, "CSA": 88, "Maths": 92}
high = {k: v for k, v in scores.items() if v >= 90}
print("High Scorers:", high)""", language="python")

            elif sel_mod == "Module 5: Object-Oriented Programming (OOP Architecture)":
                with st.expander("1. Classes, Encapsulation, Inheritance & Dunder Methods", expanded=True):
                    st.write("""
                    * Class = Blueprint, Object = Real Memory Instance.
                    * Private variables start with `__` (double underscore).
                    """)
                    st.code("""class BCAStudent:
    def __init__(self, name, roll):
        self.name = name
        self.__roll = roll

    def get_roll(self): return self.__roll

s = BCAStudent("Raj", 101)
print(f"Student: {s.name} | Roll: {s.get_roll()}")""", language="python")

            elif sel_mod == "Module 6: File Handling, Context Managers & JSON/CSV":
                with st.expander("1. File Modes, seek(), tell() & JSON", expanded=True):
                    st.code("""import json
data = {"name": "Raj", "degree": "BCA", "sem": 1}
json_str = json.dumps(data, indent=2)
print("Serialized JSON:\\n", json_str)""", language="python")

            elif sel_mod == "Module 7: Exception Handling & Custom Errors":
                with st.expander("1. try-except-else-finally & Custom Exceptions", expanded=True):
                    st.code("""class MarksError(Exception): pass
def verify(m):
    if m < 0 or m > 100: raise MarksError("Invalid Marks Range")
    return "Valid"

try:
    print(verify(95))
except MarksError as e:
    print("Error:", e)""", language="python")

            elif sel_mod == "Module 8: Standard Libraries, Regex & Date-Time":
                with st.expander("1. math, datetime, re Regex", expanded=True):
                    st.code("""import re, math
print("Square Root 144:", math.isqrt(144))
sample = "Contact raj@example.com, Phone: +91-9876543210"
print("Found Emails:", re.findall(r'[\w\.-]+@[\w\.-]+', sample))""", language="python")

        # ------------------- 2. COMPUTER ARCHITECTURE (CSA) SYLLABUS -------------------
        elif active_subj == "🖥️ Computer System Architecture":
            st.markdown("""
            <div class="hero-banner">
                <div class="hero-title">Computer System Architecture (CSA) Master</div>
                <div class="hero-sub">MLK PG College Balrampur • Complete Digital Logic, Adders, Circuits, Memory & CPU with Solved Questions & Tricks</div>
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

            # CSA UNIT 1
            if sel_mod == "Unit 1: Data Representation, Number Systems & 1's/2's Complements":
                with st.expander("1. Radix Conversions & 2's Complement Arithmetic", expanded=True):
                    st.write("""
                    **Samjhein Seedhi Bhasha Mein:**
                    * Computer data 4 number systems mein process karta hai: Binary (Base 2), Octal (Base 8), Decimal (Base 10), Hexadecimal (Base 16).
                    * **1's Complement:** Har bit ko ulta kar do ($0 \\rightarrow 1, 1 \\rightarrow 0$).
                    * **2's Complement:** $2's = (1's\\text{ Complement}) + 1$.
                    * **Examiner Secret Trick (Direct 2's Complement):** Right side (LSB) se check karo, jab tak pehla `1` na mile waisa hi rehne do, us pehle `1` ke baad ke saare left bits ko invert kar do!
                    """)
                    st.markdown("""
                    <div class="solved-box">
                        <b>📝 Solved Exam Question:</b> Represent -13 in 8-bit 2's Complement binary form. (5 Marks)<br>
                        <b>Step 1:</b> +13 in 8-bit binary = <code>0000 1101</code><br>
                        <b>Step 2 (1's Complement):</b> <code>1111 0010</code><br>
                        <b>Step 3 (Add 1):</b> <code>1111 0010 + 1 = 1111 0011</code><br>
                        <b>⚡ Quick Verification Trick:</b> Sign bit (leftmost) 1 hai, yaani number negative hai!
                    </div>
                    """, unsafe_allow_html=True)
                    st.code("""# CSA Radix & 2's Complement Simulator
def to_twos_comp(n, bits=8):
    if n >= 0:
        return bin(n)[2:].zfill(bits)
    return bin((1 << bits) + n)[2:]

val = -13
print(f"Decimal: {val}")
print(f"8-Bit 2's Complement: {to_twos_comp(val, 8)}")""", language="python")

            # CSA UNIT 2 (HALF ADDER & FULL ADDER THOROUGHLY EXPLAINED)
            elif sel_mod == "Unit 2: Logic Gates, Half Adder, Full Adder, K-Maps & Combinational Circuits":
                with st.expander("1. Half Adder & Full Adder Architecture (Complete Detailed Guide)", expanded=True):
                    st.write("""
                    **Samjhein Seedhi Bhasha Mein:**
                    * **Half Adder (HA):** Yeh do 1-bit binary inputs ($A$ aur $B$) ko add karta hai aur do outputs generate karta hai: **Sum ($S$)** aur **Carry ($C$)**.
                      * **Truth Table:**
                        * $A=0, B=0 \\implies Sum=0, Carry=0$
                        * $A=0, B=1 \\implies Sum=1, Carry=0$
                        * $A=1, B=0 \\implies Sum=1, Carry=0$
                        * $A=1, B=1 \\implies Sum=0, Carry=1$ ($1+1 = 10_2$)
                      * **Logic Formulas:**
                        * $$Sum = A \\oplus B = A'B + AB'$$ (XOR Gate)
                        * $$Carry = A \\cdot B$$ (AND Gate)
                      * **Limitation:** Half adder pichle stage se aane wale carry ko add nahi kar sakta.

                    ---
                    * **Full Adder (FA):** Yeh teen 1-bit binary inputs ($A$, $B$, aur previous carry $C_{in}$) ko add karta hai.
                      * **Logic Formulas:**
                        * $$Sum = A \\oplus B \\oplus C_{in}$$ (3-input XOR Gate)
                        * $$Carry_{out} = AB + BC_{in} + AC_{in} = AB + C_{in}(A \\oplus B)$$
                    * **Master Design Trick:** Ek Full Adder ko **2 Half Adders aur 1 OR Gate** se banaya ja sakta hai!
                    """)
                    st.markdown("""
                    <div class="solved-box">
                        <b>📝 Solved Exam Question:</b> Design a Full Adder using two Half Adders and an OR gate. Draw the logic block diagram and verify for $A=1, B=1, C_{in}=1$. (10 Marks)<br>
                        <b>Step 1 (First Half Adder):</b> Inputs $A, B$. Output $S_1 = A \\oplus B = 1 \\oplus 1 = 0$, $C_1 = A \\cdot B = 1 \\cdot 1 = 1$.<br>
                        <b>Step 2 (Second Half Adder):</b> Inputs $S_1$ and $C_{in}$. Output $Sum = S_1 \\oplus C_{in} = 0 \\oplus 1 = \\mathbf{1}$. Second carry $C_2 = S_1 \\cdot C_{in} = 0 \\cdot 1 = 0$.<br>
                        <b>Step 3 (OR Gate for Carry):</b> $C_{out} = C_1 + C_2 = 1 + 0 = \\mathbf{1}$.<br>
                        <b>Final Output:</b> $Sum = 1, Carry = 1$ (Jo ki $1 + 1 + 1 = 3 = 11_2$ bilkul sahi hai!).
                    </div>
                    """, unsafe_allow_html=True)
                    st.code("""# Interactive Full Adder Logic Simulator
def half_adder(a, b):
    sum_bit = a ^ b      # XOR gate
    carry_bit = a & b    # AND gate
    return sum_bit, carry_bit

def full_adder_using_two_ha(a, b, cin):
    s1, c1 = half_adder(a, b)
    final_sum, c2 = half_adder(s1, cin)
    final_carry = c1 | c2  # OR gate combines carries
    return final_sum, final_carry

print("Full Adder Verification Table:")
print("A | B | Cin | Sum | Carry")
print("-" * 27)
for a in [0, 1]:
    for b in [0, 1]:
        for cin in [0, 1]:
            s, c = full_adder_using_two_ha(a, b, cin)
            print(f"{a} | {b} |  {cin}  |  {s}  |   {c}")""", language="python")

                with st.expander("2. K-Map Minimization, Multiplexers (MUX) & Decoders", expanded=False):
                    st.write("""
                    * **K-Map (Karnaugh Map):** Gray code ordering (`00, 01, 11, 10`) par chalta hai taaki consecutive cells ke beech sirf 1 bit ka change ho.
                    * **Grouping Priority Trick:** Hamesha sabse bada group dhundho: 16 (Octet) $\\rightarrow$ 8 $\\rightarrow$ 4 (Quad) $\\rightarrow$ 2 (Pair). Bada group = Kam variables ki simplified equation!
                    * **Multiplexer (Data Selector):** $2^n$ inputs, $n$ select lines, 1 output.
                    * **Decoder:** $n$ inputs, $2^n$ outputs.
                    """)
                    st.code("""# Multiplexer (4:1 MUX) Simulator
def mux_4to1(i0, i1, i2, i3, s1, s0):
    lines = [i0, i1, i2, i3]
    select_index = (s1 << 1) | s0
    return lines[select_index]

print("MUX Output with S1=1, S0=0 selecting I2:", mux_4to1("D0", "D1", "Selected D2", "D3", 1, 0))""", language="python")

            # CSA UNIT 3
            elif sel_mod == "Unit 3: Sequential Circuits, Flip-Flops, Registers & Counters":
                with st.expander("1. Flip-Flops & The Famous Race-Around Condition", expanded=True):
                    st.write("""
                    * **Combinational vs Sequential:** Combinational ka output sirf current input par depend karta hai; Sequential mein **Memory (feedback loop)** hoti hai.
                    * **JK Flip-Flop Race Around Condition:** Jab $J=1, K=1$ ho aur clock pulse width ($t_p$) flip-flop ke propagation delay ($t_{pd}$) se badi ho, toh output toggle hota rehta hai aur unstable ho jata hai.
                    * **Solution Trick:** Use **Master-Slave JK Flip-Flop** ya **Edge-Triggering**!
                    """)
                    st.markdown("""
                    <div class="solved-box">
                        <b>📝 Exam Question:</b> How Master-Slave JK Flip-Flop eliminates race-around condition? (5 Marks)<br>
                        <b>Answer Shortcut:</b> Clock High par sirf Master active hota hai aur input save karta hai, jab Clock Low hoti hai tab Slave trigger hokar output deta hai. Dono ek saath active nahi hote!
                    </div>
                    """, unsafe_allow_html=True)

            # CSA UNIT 4
            elif sel_mod == "Unit 4: Basic Computer Organization, Instruction Cycle & Bus Architecture":
                with st.expander("1. Instruction Cycle & Common Bus System", expanded=True):
                    st.write("""
                    **Samjhein Seedhi Bhasha Mein:**
                    * **Common Bus:** Bahut saare registers (PC, MAR, MDR, AC) ko ek common data highway provide karta hai multiplexers ke zariye.
                    * **Instruction Cycle ke 4 Steps:**
                      1. **Fetch:** Instruction memory se IR mein aati hai ($PC \\rightarrow MAR$, $M[MAR] \\rightarrow IR$, $PC + 1$).
                      2. **Decode:** Opcode decoder check karta hai konsa task hai.
                      3. **Effective Address:** Indirect addressing ho toh actual memory address read hota hai.
                      4. **Execute:** ALU operation complete karta hai.
                    """)
                    st.markdown("""
                    <div class="solved-box">
                        <b>📝 Solved Exam Question:</b> Write register transfer micro-operations for Fetch phase. (5 Marks)<br>
                        <b>Step 1 ($T_0$):</b> $AR \\leftarrow PC$<br>
                        <b>Step 2 ($T_1$):</b> $IR \\leftarrow M[AR], PC \\leftarrow PC + 1$<br>
                        <b>Step 3 ($T_2$):</b> Decode $IR(12-14)$, $AR \\leftarrow IR(0-11)$, $I \\leftarrow IR(15)$
                    </div>
                    """, unsafe_allow_html=True)

            # CSA UNIT 5
            elif sel_mod == "Unit 5: Central Processing Unit (ALU, Addressing Modes & Pipeline)":
                with st.expander("1. Addressing Modes Shortcuts & Pipeline Hazards", expanded=True):
                    st.write("""
                    **Addressing Modes Tricks:**
                    * **Immediate:** Operand instruction ke andar hi hai (`MOV R1, #25`).
                    * **Direct:** Address direct diya hai (`ADD 2000`).
                    * **Indirect:** Address ke andar dusra address hai (`ADD @2000`).
                    * **Pipeline Speedup Formula:** $Speedup = \\frac{n \\times k}{k + n - 1}$, jahan $k$ = pipeline stages, $n$ = instructions.
                    """)
                    st.markdown("""
                    <div class="solved-box">
                        <b>📝 Solved Numerical:</b> Ek 5-stage pipeline mein 100 instructions execute karne par speedup ratio kya hoga? (7 Marks)<br>
                        <b>Calculation:</b> $k = 5, n = 100$<br>
                        Non-pipeline time = $n \\times k = 100 \\times 5 = 500$ cycles.<br>
                        Pipeline time = $k + n - 1 = 5 + 100 - 1 = 104$ cycles.<br>
                        <b>Speedup:</b> $500 / 104 = 4.807$ (Lagbhag 5x faster!).
                    </div>
                    """, unsafe_allow_html=True)
                    st.code("""# Pipeline Speedup Calculator
def calculate_speedup(k_stages, n_instructions):
    non_pipe = k_stages * n_instructions
    pipe = k_stages + n_instructions - 1
    return non_pipe / pipe

print("Pipeline Speedup (k=5, n=100):", round(calculate_speedup(5, 100), 3))""", language="python")

            # CSA UNIT 6
            elif sel_mod == "Unit 6: Memory Hierarchy (Cache Mapping, RAM/ROM & Virtual Memory)":
                with st.expander("1. Cache Mapping Formulas & Locality of Reference", expanded=True):
                    st.write("""
                    **Locality of Reference:**
                    * **Temporal Locality:** Jo data abhi use hua hai, wo jaldi hi dobara use hoga (Loops).
                    * **Spatial Locality:** Jo data abhi use hua hai, uske bagal wala memory location agle cycle mein use hoga (Arrays).
                    * **Direct Cache Mapping Trick:** Main memory address divides into: **[Tag | Index (Line) | Offset (Word)]**.
                    """)
                    st.markdown("""
                    <div class="solved-box">
                        <b>📝 Solved Exam Question:</b> Agar Main Memory 64 KB aur Cache Memory 4 KB hai with 16-byte block size, toh Direct Mapping fields calculate karein. (7 Marks)<br>
                        <b>Step 1 (Word Offset):</b> Block size 16 bytes = $2^4 \\implies$ <b>4 bits</b>.<br>
                        <b>Step 2 (Cache Lines/Index):</b> $4\\text{ KB} / 16\\text{ B} = 4096 / 16 = 256 = 2^8 \\implies$ <b>8 bits</b>.<br>
                        <b>Step 3 (Tag):</b> Total memory 64 KB = $2^{16} \\implies$ 16 bits total address.<br>
                        $\\text{Tag Bits} = 16 - (8 + 4) =$ <b>4 bits</b>!
                    </div>
                    """, unsafe_allow_html=True)

            # CSA UNIT 7
            elif sel_mod == "Unit 7: Input-Output Organization (Interrupts, DMA, Programmed I/O)":
                with st.expander("1. DMA (Direct Memory Access) Data Transfer", expanded=True):
                    st.write("""
                    * **Programmed I/O:** CPU baar-baar puchta rehta hai (Polling / Busy Waiting). CPU ka time waste hota hai.
                    * **Interrupt I/O:** Jab data ready ho, device CPU ko interrupt bhejti hai.
                    * **DMA (Master Trick):** CPU ko beech se hata do! Hard disk direct RAM se baat karegi. CPU sirf transfer shuru karta hai aur finish hone par interrupt leta hai.
                    """)
                    st.markdown("""
                    <div class="solved-box">
                        <b>📝 Exam Question:</b> Differentiate between Cycle Stealing and Burst Mode DMA. (5 Marks)<br>
                        <b>Shortcut:</b> <b>Cycle Stealing</b> mein DMA controller CPU se 1 bus cycle chheen kar 1 byte bhejta hai; <b>Burst Mode</b> mein poora block bhejne tak bus CPU ko nahi milti.
                    </div>
                    """, unsafe_allow_html=True)

        # ------------------- 3. MATHEMATICS SYLLABUS -------------------
        elif active_subj == "📐 Mathematics & Numerical Methods":
            st.markdown("""
            <div class="hero-banner">
                <div class="hero-title">Discrete Mathematics & Numerical Methods</div>
                <div class="hero-sub">MLK PG College Balrampur • Sets, Relations, Logic, Matrices, Calculus & Numerical Solvers with Tricks</div>
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

            # MATH UNIT 1
            if sel_mod == "Unit 1: Set Theory, Relations, Functions & POSET":
                with st.expander("1. Equivalence Relations & Partial Order (POSET)", expanded=True):
                    st.write("""
                    **Samjhein Seedhi Bhasha Mein:**
                    * **Reflexive:** Khud ka relation khud se ($a R a$).
                    * **Symmetric:** Agar $a R b$ hai toh $b R a$ bhi hona chahiye.
                    * **Transitive:** Agar $a R b$ aur $b R c$ hai toh $a R c$ hona zaroori hai.
                    * **Equivalence Relation:** Jo relation Reflexive, Symmetric aur Transitive teeno ho.
                    * **POSET (Partial Order Set):** Reflexive + **Antisymmetric** ($a R b$ aur $b R a \\implies a = b$) + Transitive.
                    """)
                    st.markdown("""
                    <div class="solved-box">
                        <b>📝 Solved Exam Question:</b> Show that relation $R = \\{(a, b) : a - b \\text{ is divisible by 3}\\}$ on integers $\\mathbb{Z}$ is an Equivalence Relation. (7 Marks)<br>
                        <b>1. Reflexive:</b> $a - a = 0 = 3 \\times 0$ (divisible by 3) $\\implies (a, a) \\in R$.<br>
                        <b>2. Symmetric:</b> Agar $a - b = 3k$ toh $b - a = -3k = 3(-k)$ (divisible by 3) $\\implies (b, a) \\in R$.<br>
                        <b>3. Transitive:</b> $a - b = 3k_1$ aur $b - c = 3k_2$. Add both: $(a - b) + (b - c) = a - c = 3(k_1 + k_2) \\implies (a, c) \\in R$.<br>
                        <b>Verdict:</b> Hence, it is an Equivalence Relation!
                    </div>
                    """, unsafe_allow_html=True)

            # MATH UNIT 2
            elif sel_mod == "Unit 2: Mathematical Logic, Truth Tables & Propositional Calculus":
                with st.expander("1. Logic Connectives, Tautology & Modus Ponens", expanded=True):
                    st.write("""
                    * Conjunction $\\land$ (AND): Dono True honge tabhi True.
                    * Disjunction $\\lor$ (OR): Ek bhi True hoga toh True.
                    * Conditional $p \\rightarrow q$ (Implies): **Sirf tabhi False hota hai jab $p$ True ho aur $q$ False ho ($T \\rightarrow F = F$)**, baaki sabhi case mein True!
                    * **Tautology:** Statement column mein saare values `True` hon.
                    """)
                    st.markdown("""
                    <div class="solved-box">
                        <b>📝 Solved Exam Question:</b> Prove that $(p \\rightarrow q) \\equiv (\\neg p \\lor q)$ using Truth Table. (5 Marks)<br>
                        <b>Shortcut:</b> Column values match: Dono columns mein truth values <code>[T, F, T, T]</code> aati hain, isliye mathematically logically equivalent hain!
                    </div>
                    """, unsafe_allow_html=True)
                    st.code("""# Truth Table Generator in Python
print("p  | q  | p -> q | ~p v q")
print("------------------------")
for p in [True, False]:
    for q in [True, False]:
        implies = (not p) or q
        equiv = (not p) or q
        print(f"{int(p)}  | {int(q)}  |   {int(implies)}    |   {int(equiv)}")""", language="python")

            # MATH UNIT 3
            elif sel_mod == "Unit 3: Matrices, Determinants, Rank & System of Linear Equations":
                with st.expander("1. Rank of Matrix, Rouche-Capelli Consistency & Cayley-Hamilton", expanded=True):
                    st.write("""
                    **Consistency Trick (Rouche-Capelli Theorem):**
                    * $AX = B$ mein Augmented Matrix $[A|B]$ banate hain aur Echelon form mein convert karte hain:
                      1. $Rank(A) = Rank(A|B) = n$ (variables) $\\implies$ **Unique Solution**.
                      2. $Rank(A) = Rank(A|B) < n \\implies$ **Infinitely Many Solutions**.
                      3. $Rank(A) \\neq Rank(A|B) \\implies$ **Inconsistent (No Solution)**.
                    * **Cayley-Hamilton Theorem Shortcut:** Har square matrix apni characteristic equation $|A - \\lambda I| = 0$ ko satisfy karti hai! Isse $A^{-1}$ bina adjoint calculate kiye 2 minute mein nikalta hai!
                    """)
                    st.markdown("""
                    <div class="solved-box">
                        <b>📝 Solved Exam Question:</b> Find the eigenvalues of matrix $A = \\begin{pmatrix} 2 & 1 \\\\ 1 & 2 \\end{pmatrix}$. (5 Marks)<br>
                        <b>Formula:</b> $|A - \\lambda I| = 0 \\implies (2 - \\lambda)(2 - \\lambda) - (1)(1) = 0$<br>
                        $\\lambda^2 - 4\\lambda + 3 = 0 \\implies (\\lambda - 1)(\\lambda - 3) = 0$<br>
                        <b>Eigenvalues:</b> $\\lambda = 1, 3$.<br>
                        <b>⚡ Super Verification Trick:</b> Sum of eigenvalues ($1 + 3 = 4$) hamesha matrix ke trace (diagonal sum $2 + 2 = 4$) ke barabar hota hai!
                    </div>
                    """, unsafe_allow_html=True)

            # MATH UNIT 4
            elif sel_mod == "Unit 4: Combinatorics, Pigeonhole Principle & Graph Theory":
                with st.expander("1. Handshaking Theorem & Euler Planar Formula", expanded=True):
                    st.write("""
                    * **Handshaking Theorem:** Graph ke saare vertices ki degree ka sum hamesha number of edges ke double ke barabar hota hai:
                      $$\\sum_{v \\in V} deg(v) = 2E$$
                    * **Euler's Planar Formula Trick:** Kisi bhi connected planar graph mein:
                      $$V - E + R = 2$$
                      (Vertices - Edges + Regions = 2).
                    """)
                    st.markdown("""
                    <div class="solved-box">
                        <b>📝 Solved Exam Question:</b> Ek graph mein 12 edges hain aur har vertex ki degree 3 hai. Total kitne vertices honge? (5 Marks)<br>
                        <b>Step:</b> Handshaking Theorem se $\\sum deg(v) = 2E = 2 \\times 12 = 24$.<br>
                        Agar $n$ vertices hain: $3 \\times n = 24 \\implies n = 8$ vertices!
                    </div>
                    """, unsafe_allow_html=True)

            # MATH UNIT 5
            elif sel_mod == "Unit 5: Differential Calculus, Leibnitz's Theorem & Maxima/Minima":
                with st.expander("1. Leibnitz's Theorem for n-th Derivative", expanded=True):
                    st.write("""
                    * Agar do functions multiply ho rahe hon ($y = u \\cdot v$), toh $n$-th derivative ka formula:
                      $$y_n = ^nC_0 u_n v + ^nC_1 u_{n-1} v_1 + ^nC_2 u_{n-2} v_2 + \\dots + ^nC_n u v_n$$
                    * **Trick:** $v$ hamesha us function ko maano jo 2-3 baar differentiate hone par zero ho jaye (jaise $x^2$ ya $x^3$), taaki aage ke saare terms khatam ho jayein!
                    """)
                    st.markdown("""
                    <div class="solved-box">
                        <b>📝 Solved Exam Question:</b> Find the $n$-th derivative of $y = x^2 e^{ax}$. (7 Marks)<br>
                        <b>Choose:</b> $u = e^{ax}$ (infinite derivatives) aur $v = x^2$ ($v_1 = 2x, v_2 = 2, v_3 = 0$).<br>
                        $y_n = a^n e^{ax} \\cdot x^2 + n a^{n-1} e^{ax} \\cdot (2x) + \\frac{n(n-1)}{2} a^{n-2} e^{ax} \\cdot 2$<br>
                        $= a^{n-2} e^{ax} [a^2 x^2 + 2nax + n(n-1)]$.
                    </div>
                    """, unsafe_allow_html=True)

            # MATH UNIT 6
            elif sel_mod == "Unit 6: Numerical Methods (Newton-Raphson, Bisection & Gauss Elimination)":
                with st.expander("1. Newton-Raphson Method Formula & Code Solver", expanded=True):
                    st.write("""
                    **Samjhein Seedhi Bhasha Mein:**
                    * Equations ka root (solution) nikalne ke liye tangent line use karta hai.
                    * **Formula:**
                      $$x_{n+1} = x_n - \\frac{f(x_n)}{f'(x_n)}$$
                    * **Order of Convergence:** Quadratic (Order = 2), yaani har step mein decimal places double accuracy se aate hain!
                    """)
                    st.markdown("""
                    <div class="solved-box">
                        <b>📝 Solved Numerical:</b> Find root of $x^3 - x - 2 = 0$ using Newton-Raphson starting with $x_0 = 1.5$. (7 Marks)<br>
                        $f(x) = x^3 - x - 2 \\implies f'(x) = 3x^2 - 1$<br>
                        $f(1.5) = 3.375 - 1.5 - 2 = -0.125$<br>
                        $f'(1.5) = 3(2.25) - 1 = 5.75$<br>
                        $x_1 = 1.5 - \\frac{-0.125}{5.75} = 1.5 + 0.02174 = \\mathbf{1.5217}$!
                    </div>
                    """, unsafe_allow_html=True)
                    st.code("""# Complete Newton-Raphson Solver
def newton_raphson(f, df, x0, tol=1e-5, max_iter=10):
    x = x0
    for i in range(max_iter):
        fx = f(x)
        dfx = df(x)
        x_new = x - fx / dfx
        print(f"Iteration {i+1}: x = {x_new:.6f}")
        if abs(x_new - x) < tol:
            return x_new
        x = x_new
    return x

# Testing x^3 - x - 2 = 0
f = lambda x: x**3 - x - 2
df = lambda x: 3*x**2 - 1
root = newton_raphson(f, df, 1.5)
print("Converged Root:", round(root, 5))""", language="python")

        # Bottom AI Action Container
        st.markdown(f"""
        <div class="apple-glass-card">
            <h3 style="margin-top:0; font-size:20px; font-weight:700;">🎯 AI University Exam Preparation & Viva Master ({active_subj})</h3>
            <p style="color:#94A3B8; font-size:13px; margin-bottom:14px;">MLK PG College / Maa Pateshwari University exam ke top expected questions, viva points aur tricks generate karein:</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔥 Generate Most Important Exam Questions & Viva Points", use_container_width=True):
            with st.spinner(f"AI Professor analyzing {active_subj} for MLK PG College Balrampur..."):
                prompt = f"""
                You are a senior BCA university examiner for MLK PG College, Balrampur (affiliated with Maa Pateshwari State University).
                Subject: {active_subj}
                Active Unit/Topic: {sel_mod}
                
                1. Provide the top 3 high-weightage theory examination questions (5-10 marks format) with complete step-by-step model answers and shortcut tricks.
                2. Provide 3 tricky Viva-Voce questions with short, precise, examiner-winning answers.
                3. Highlight 2 critical practical/numerical pitfalls students usually make in university exams and how to avoid them easily.
                Format cleanly using bolding and clear bullet points.
                """
                ai_output = get_ai_response(prompt, current_subject=active_subj)
                st.markdown(f'<div class="ai-box">{ai_output}</div>', unsafe_allow_html=True)

    # ================= 2. EXAM ENGINE (WITH PHOTO ANSWER UPLOAD) =================
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

    # ================= 3. GUIDED PROJECTS LAB =================
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

    # ================= 4. 24/7 AI CODE & SUBJECT MENTOR (WITH PHOTO UPLOAD) =================
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

    # ================= 5. LIVE RUNNER SANDBOX =================
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
    elif selected_tab == "📝 Exam Engine":
        render_exam_engine()
    elif selected_tab == "🛠️ Projects":
        render_projects()
    elif selected_tab == "🤖 AI Mentor":
        render_mentor()
    elif selected_tab == "🧪 Sandbox":
        render_runner()
