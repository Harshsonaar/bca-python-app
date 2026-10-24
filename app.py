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

        /* Top Sticky Navigation on Mobile - Smooth Horizontal Touch Scroll */
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
    
    IMPORTANT RULES:
    1. If an image is provided, carefully examine the handwritten question, code snippet, error screenshot, circuit diagram, or mathematical formula in the image and provide a thorough, accurate solution.
    2. Focus all solutions, viva queries, and explanations strictly on the currently active subject ({current_subject}).
    3. Complete all diagrams, code blocks, or mathematical proofs without cutting off.
    4. Do not add conversational fluff or meta-announcements.
    
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
            Complete syllabus coverage for Python Programming, Computer System Architecture & Discrete Mathematics with Multimodal Vision Intelligence.
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
                <div class="hero-sub">MLK PG College Balrampur • BCA University Syllabus (Full Theory, Viva & Practical Code)</div>
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

            # MODULE 1
            if sel_mod == "Module 1: Language Basics, Operators & Bitwise":
                with st.expander("1. Python Architecture, Bytecode Compilation & Dynamic Typing", expanded=True):
                    st.write("""
                    **Conceptual Architecture:**
                    * Python interpreted aur high-level programming language hai. Source code (`.py`) pehle platform-independent Bytecode (`.pyc`) mein compile hota hai.
                    * Bytecode ko Python Virtual Machine (PVM) line-by-line machine code (binary) mein translate karke execute karta hai.
                    * **Dynamic Typing vs Static Typing:** C ya C++ mein variable declare karte waqt data type batana padta hai (`int a = 10;`). Python dynamically typed hai; variable runtime par assigned value ke mutabik type acquire karta hai. Variables heap memory mein allocated objects ke references hote hain.
                    * **Garbage Collection:** Python memory allocation aur deallocation automatically **Reference Counting** aur **Generational Garbage Collector** ke zariye handle karta hai.
                    """)
                    st.code("""# Dynamic Typing & Object Reference Demonstration
x = 101
print(f"Value: {x} | Data Type: {type(x)} | Memory Address (ID): {id(x)}")

# Same identifier ab naye string object ko point karega
x = "Raj Shraff"
print(f"Value: {x} | Data Type: {type(x)} | Memory Address (ID): {id(x)}")

# Multiple references pointing to identical immutable object (Integer Caching: -5 to 256)
a = 250
b = 250
print("a is b (Memory Identity Match):", a is b) # True""", language="python")

                with st.expander("2. Identifiers, Reserved Keywords, Fundamental Data Types & Explicit Type Casting", expanded=False):
                    st.write("""
                    **Rules for Identifiers:**
                    * Alphabets (`a-z`, `A-Z`), digits (`0-9`), aur underscore (`_`) allow hote hain.
                    * Kabhi bhi digit se shuru nahi ho sakta (`1st_name` invalid hai, `first_name` valid hai).
                    * Reserved Keywords (jaise `def`, `class`, `if`, `while`, `pass`, `yield`) identifiers ke taur par use nahi kiye ja sakte.
                    
                    **Built-in Data Types:**
                    * **Numeric:** `int`, `float`, `complex` (e.g. `3 + 4j`).
                    * **Sequence:** `str`, `list`, `tuple`, `range`.
                    * **Mapping:** `dict` | **Set Types:** `set`, `frozenset` | **Boolean:** `bool`.
                    """)
                    st.code("""# Complex numbers & Explicit Type Casting Demonstration
c_num = 4 + 7j
print("Real Part:", c_num.real, "| Imaginary Part:", c_num.imag)

raw_val = "180"
converted_val = int(raw_val)
tax_percentage = 0.18
grand_total = converted_val + (converted_val * tax_percentage)

print(f"Raw Input: '{raw_val}' ({type(raw_val)})")
print(f"Parsed Integer: {converted_val} ({type(converted_val)})")
print(f"Grand Total with 18% GST: INR {grand_total:.2f}")""", language="python")

                with st.expander("3. Complete Operators (Arithmetic, Relational, Logical, Bitwise, Identity & Membership)", expanded=False):
                    st.write("""
                    **Operators Hierarchy & Mechanics:**
                    * **Arithmetic:** `+`, `-`, `*`, `/` (float quotient), `//` (floor division), `%` (modulus remainder), `**` (exponentiation).
                    * **Bitwise Operators:** `&` (AND), `|` (OR), `^` (XOR), `~` (NOT), `<<` (Left shift), `>>` (Right shift).
                    * **Identity (`is`, `is not`):** Checks memory location equality (`id(x) == id(y)`).
                    * **Membership (`in`, `not in`):** Checks sequence container inclusion.
                    """)
                    st.code("""a = 14  # Binary: 1110
b = 4   # Binary: 0100

print("Floor Division (14 // 4):", a // b) # 3
print("Modulus Remainder (14 % 4):", a % b) # 2
print("Exponentiation (14 ** 2):", a ** 2)  # 196

# Bitwise Operations
print("Bitwise AND (14 & 4):", a & b)      # 4
print("Bitwise XOR (14 ^ 4):", a ^ b)      # 10
print("Left Shift (4 << 2):", b << 2)      # 16

# Identity vs Equality
seq1, seq2 = [10, 20], [10, 20]
print("seq1 == seq2 (Value):", seq1 == seq2)     # True
print("seq1 is seq2 (Memory):", seq1 is seq2)    # False""", language="python")

            # MODULE 2
            elif sel_mod == "Module 2: Control Flow & Iteration (Branches & Loops)":
                with st.expander("1. Conditional Branching (if, elif, else, Nested if, Ternary Operator)", expanded=True):
                    st.write("""
                    * Indentation (standard 4 spaces) execution block define karta hai.
                    * **Ternary Operator:** `result = true_val if condition else false_val`
                    """)
                    st.code("""marks = 86
division = "Distinction" if marks >= 80 else "Regular Pass"
print("Status:", division)

if marks >= 90:
    print("Grade: O")
elif marks >= 60:
    print("Grade: A")
else:
    print("Grade: Pass")""", language="python")

                with st.expander("2. Loops in Python (for, while, range() internal step mechanism)", expanded=False):
                    st.write("""
                    * `range(start, stop, step)` memory efficient generator return karta hai.
                    """)
                    st.code("""print("Reverse Counting with step -2:")
for val in range(10, 0, -2):
    print(val, end=" -> ")
print("LAUNCH")""", language="python")

                with st.expander("3. Loop Control Statements (break, continue, pass, for-else construct)", expanded=False):
                    st.write("""
                    * **for-else:** Loop ka `else` block tabhi run hota hai jab loop natural end tak pahuche, yaani beech mein **kisi `break` statement se terminate na hua ho**.
                    """)
                    st.code("""test_number = 37
for divisor in range(2, int(test_number**0.5) + 1):
    if test_number % divisor == 0:
        print(f"{test_number} is composite, divided by {divisor}")
        break
else:
    print(f"{test_number} is a VERIFIED PRIME NUMBER (Loop completed without break)!")""", language="python")

            # MODULE 3
            elif sel_mod == "Module 3: Functions, Scopes, Lambdas & Recursion":
                with st.expander("1. Function Architecture, Positional, Keyword, *args & **kwargs", expanded=True):
                    st.write("""
                    * `*args`: Extra positional arguments ko **Tuple** mein pack karta hai.
                    * `**kwargs`: Extra keyword arguments ko **Dictionary** mein pack karta hai.
                    """)
                    st.code("""def register_student(name, roll, *subjects, college="MLK PG", **scores):
    print(f"Student: {name} (Roll: {roll}) | College: {college}")
    print("Enrolled Subjects:", subjects)
    print("Marks Recorded:", scores)

register_student("Raj Shraff", 101, "Python", "CSA", "Maths", Python=95, CSA=88)""", language="python")

                with st.expander("2. Scope Resolution (LEGB Rule), global and nonlocal keywords", expanded=False):
                    st.write("""
                    * **LEGB Hierarchy:** Local $\\rightarrow$ Enclosing $\\rightarrow$ Global $\\rightarrow$ Built-in.
                    * `global`: Module level variable modify karne ke liye.
                    * `nonlocal`: Closures aur nested functions mein enclosing variable mutate karne ke liye.
                    """)
                    st.code("""univ = "Maa Pateshwari Univ"

def outer():
    campus = "Main Campus"
    def inner():
        nonlocal campus
        campus = "Balrampur Campus"
        global univ
        univ = "Maa Pateshwari State University"
    inner()
    print("Enclosing Campus:", campus)

outer()
print("Global Univ:", univ)""", language="python")

                with st.expander("3. Anonymous Functions (Lambda), map(), filter(), reduce()", expanded=False):
                    st.write("""
                    * **Lambda:** Inline anonymous function (`lambda args: expr`).
                    * `map()`, `filter()`, aur `reduce()` functional programming tools provide karte hain.
                    """)
                    st.code("""from functools import reduce
scores = [45, 88, 72, 91, 54, 63, 98]

first_class = list(filter(lambda m: m >= 60, scores))
grace_marks = list(map(lambda m: m + 5 if m < 60 else m, scores))
total_sum = reduce(lambda a, b: a + b, scores)

print("First Class:", first_class)
print("Grace Added:", grace_marks)
print("Aggregate:", total_sum)""", language="python")

                with st.expander("4. Recursion, Call Stack Mechanics & Base Cases", expanded=False):
                    st.write("""
                    * **GCD (Euclidean Algorithm) & Tower of Hanoi.** Base case na hone par stack overflow aur `RecursionError` throw hota hai.
                    """)
                    st.code("""def compute_gcd(a, b):
    return a if b == 0 else compute_gcd(b, a % b)

print("GCD of 48 and 18:", compute_gcd(48, 18))""", language="python")

            # MODULE 4
            elif sel_mod == "Module 4: In-Depth Data Structures (Lists, Tuples, Dicts, Sets)":
                with st.expander("1. Lists (Memory Architecture, Slicing, List Comprehensions)", expanded=True):
                    st.write("""
                    * Dynamic array of pointers. Heterogeneous data types support karta hai.
                    """)
                    st.code("""matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [val for row in matrix for val in row]
even_squares = [x**2 for x in flattened if x % 2 == 0]
print("Flattened Matrix:", flattened)
print("Even Squares:", even_squares)""", language="python")

                with st.expander("2. Tuples (Immutability, Asterisk Unpacking & Memory Efficiency)", expanded=False):
                    st.write("""
                    * Lightweight and hashable. Can be used as dictionary keys.
                    """)
                    st.code("""record = ("Raj Shraff", "BCA", 1, 89.5, 92.0, 95.0)
name, degree, sem, *grades = record
print(f"Candidate: {name} | Grades: {grades}")""", language="python")

                with st.expander("3. Dictionaries (Hash Maps, Lookups, Dict Comprehensions)", expanded=False):
                    st.write("""
                    * $O(1)$ average time complexity.
                    """)
                    st.code("""marks = {"Python": 95, "CSA": 88, "Calculus": 79, "Discrete": 92}
honors = {k: v for k, v in marks.items() if v >= 85}
print("Honors Qualified:", honors)""", language="python")

                with st.expander("4. Sets (Set Theory Operations & Frozenset)", expanded=False):
                    st.write("""
                    * Mathematical operations: Union (`|`), Intersection (`&`), Difference (`-`), Symmetric Difference (`^`).
                    """)
                    st.code("""python_std = {"Raj", "Aman", "Rohan"}
csa_std = {"Aman", "Khushi", "Raj"}
print("Both Courses (Intersection):", python_std & csa_std)
print("Only in Python (Difference):", python_std - csa_std)""", language="python")

            # MODULE 5
            elif sel_mod == "Module 5: Object-Oriented Programming (OOP Architecture)":
                with st.expander("1. Classes, Objects, __init__ Constructor & self", expanded=True):
                    st.write("""
                    * Classes act as blueprints; objects act as heap memory instances.
                    """)
                    st.code("""class BCAStudent:
    college = "MLK PG College Balrampur"
    def __init__(self, name, roll):
        self.name = name
        self.roll = roll
    def profile(self):
        return f"{self.name} (Roll: {self.roll}) - {BCAStudent.college}"

s = BCAStudent("Raj Shraff", 101)
print(s.profile())""", language="python")

                with st.expander("2. Encapsulation, Private Specifiers & @property Decorator", expanded=False):
                    st.write("""
                    * Private variables use double underscore (`__var`) leading to Name Mangling (`_ClassName__var`).
                    """)
                    st.code("""class Account:
    def __init__(self, balance):
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, amt):
        if amt < 0: raise ValueError("Cannot be negative")
        self.__balance = amt

acc = Account(15000)
acc.balance = 20000
print("Balance verified:", acc.balance)""", language="python")

                with st.expander("3. Inheritance (Single, Multiple, Multilevel, MRO & super())", expanded=False):
                    st.write("""
                    * MRO uses C3 Linearization algorithm to resolve diamond problem in multiple inheritance.
                    """)
                    st.code("""class Person:
    def __init__(self, name): self.name = name

class Tech:
    def __init__(self, stack): self.stack = stack

class Developer(Person, Tech):
    def __init__(self, name, stack, roll):
        Person.__init__(self, name)
        Tech.__init__(self, stack)
        self.roll = roll

dev = Developer("Raj", "Python & CSA", 101)
print(f"Dev: {dev.name} | Stack: {dev.stack} | Roll: {dev.roll}")
print("MRO:", Developer.__mro__)""", language="python")

                with st.expander("4. Polymorphism, Overriding & Dunder Methods (__str__, __len__, __add__)", expanded=False):
                    st.write("""
                    * Magic/Dunder methods operator overloading provide karte hain.
                    """)
                    st.code("""class Module:
    def __init__(self, title, hours):
        self.title = title
        self.hours = hours
    def __str__(self): return f"'{self.title}' ({self.hours}h)"
    def __len__(self): return self.hours
    def __add__(self, other): return self.hours + other.hours

m1 = Module("Python Core", 45)
m2 = Module("CSA Architecture", 40)
print(str(m1))
print("Combined Hours:", m1 + m2)""", language="python")

            # MODULE 6
            elif sel_mod == "Module 6: File Handling, Context Managers & JSON/CSV":
                with st.expander("1. File Modes, seek(), tell() & with Context Manager", expanded=True):
                    st.write("""
                    * `with` automatically calls `__enter__()` and `__exit__()` to guarantee resource cleanup.
                    """)
                    st.code("""with open("sample.txt", "w+") as f:
    f.write("BCA Semester 1 - Python\\nMLK PG College Balrampur")
    print("Cursor at:", f.tell())
    f.seek(0)
    print("Read content:\\n" + f.read())""", language="python")

                with st.expander("2. JSON Serialization & Deserialization", expanded=False):
                    st.code("""import json
data = {"name": "Raj", "degree": "BCA", "verified": True}
json_str = json.dumps(data, indent=2)
print("Serialized JSON:\\n", json_str)
parsed = json.loads(json_str)
print("Parsed Object Name:", parsed["name"])""", language="python")

            # MODULE 7
            elif sel_mod == "Module 7: Exception Handling & Custom Errors":
                with st.expander("1. try-except-else-finally & Custom Exceptions", expanded=True):
                    st.write("""
                    * `else` block runs only when no exception occurs. `finally` runs unconditionally.
                    """)
                    st.code("""class InvalidMarksError(Exception): pass

def submit_score(score):
    if score < 0 or score > 100:
        raise InvalidMarksError(f"Marks {score} out of bounds (0-100)")
    return f"Score {score}% accepted."

try:
    print(submit_score(92))
    print(submit_score(115))
except InvalidMarksError as e:
    print("Caught:", e)
finally:
    print("Verification complete.")""", language="python")

            # MODULE 8
            elif sel_mod == "Module 8: Standard Libraries, Regex & Date-Time":
                with st.expander("1. math, random, datetime & re (Regex Pattern Matching)", expanded=True):
                    st.code("""import math, random, re
from datetime import datetime

print("GCD(36, 60):", math.gcd(36, 60))
print("Current Time:", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

text = "Student Raj Shraff, Roll 101, Contact: raj@example.com, Phone: +91-9876543210"
print("Email:", re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text))
print("Phone:", re.findall(r'\+91-\d{10}', text))""", language="python")

        # ------------------- 2. COMPUTER ARCHITECTURE SYLLABUS -------------------
        elif active_subj == "🖥️ Computer System Architecture":
            st.markdown("""
            <div class="hero-banner">
                <div class="hero-title">Computer System Architecture (CSA)</div>
                <div class="hero-sub">MLK PG College Balrampur • BCA University Syllabus (Digital Logic, ALU, Memory & CPU Design)</div>
            </div>
            """, unsafe_allow_html=True)

            csa_modules = [
                "Unit 1: Data Representation, Number Systems & Logic Gates",
                "Unit 2: Boolean Algebra, K-Maps & Combinational Circuits",
                "Unit 3: Sequential Circuits, Flip-Flops, Registers & Counters",
                "Unit 4: Basic Computer Organization, Instruction Cycles & Bus Architecture",
                "Unit 5: Central Processing Unit (ALU, Stack, Addressing Modes & Pipeline)",
                "Unit 6: Memory Hierarchy (Cache Mapping, RAM/ROM, Virtual Memory)",
                "Unit 7: Input-Output Organization (Interrupts, DMA, Programmed I/O)"
            ]
            sel_mod = st.selectbox("📚 Select CSA Unit:", csa_modules)

            if sel_mod == "Unit 1: Data Representation, Number Systems & Logic Gates":
                with st.expander("1. Number Systems & Binary Complements", expanded=True):
                    st.write("""
                    * **Radix Conversions:** Binary (Base 2), Octal (Base 8), Decimal (Base 10), Hexadecimal (Base 16).
                    * **1's & 2's Complement:** Signed numbers representation. $2's\\text{ Complement} = (1's\\text{ Complement}) + 1$.
                    * **Fixed & Floating Point (IEEE 754):** Sign bit (1 bit), Exponent (8 bits), Mantissa (23 bits).
                    """)
                    st.code("""# Number system conversion demonstration
num = 45
print("Binary:", bin(num))
print("Octal:", oct(num))
print("Hexadecimal:", hex(num))""", language="python")

            elif sel_mod == "Unit 2: Boolean Algebra, K-Maps & Combinational Circuits":
                with st.expander("1. DeMorgan's Laws, K-Map Minimization & Adders", expanded=True):
                    st.write("""
                    * **DeMorgan's Laws:** $(A + B)' = A' \\cdot B'$ aur $(A \\cdot B)' = A' + B'$.
                    * **K-Map:** Gray code ordering ke sath Boolean function minimization.
                    * **Half Adder:** Sum = $A \\oplus B$, Carry = $A \\cdot B$.
                    * **Full Adder:** Sum = $A \\oplus B \\oplus C_{in}$, Carry = $A B + B C_{in} + A C_{in}$.
                    * **Multiplexers (MUX) & Decoders:** Data selectors ($2^n \\times 1$).
                    """)

            elif sel_mod == "Unit 3: Sequential Circuits, Flip-Flops, Registers & Counters":
                with st.expander("1. Latches, Flip-Flops (SR, JK, D, T) & Master-Slave", expanded=True):
                    st.write("""
                    * **Sequential Circuit:** Output current input aur past memory history dono par depend karta hai.
                    * **SR Flip-Flop:** $S=1, R=1$ invalid/forbidden state.
                    * **JK Flip-Flop & Race-Around:** $J=1, K=1$ par condition occur hoti hai jab pulse duration propagation delay se badi ho.
                    * **Master-Slave Flip-Flop:** Race-around condition ko eliminate karta hai.
                    """)

            elif sel_mod == "Unit 4: Basic Computer Organization, Instruction Cycles & Bus Architecture":
                with st.expander("1. Common Bus System, Control Unit & Instruction Cycle", expanded=True):
                    st.write("""
                    * **Registers:** PC, MAR, MDR, AC, IR.
                    * **Instruction Cycle:** Fetch ($PC \\rightarrow MAR$, $M[MAR] \\rightarrow IR$), Decode, Read Effective Address, Execute.
                    """)

            elif sel_mod == "Unit 5: Central Processing Unit (ALU, Stack, Addressing Modes & Pipeline)":
                with st.expander("1. Addressing Modes & Instruction Pipelining", expanded=True):
                    st.write("""
                    * **Addressing Modes:** Immediate, Direct, Indirect, Register Indirect, Indexed, Relative.
                    * **Instruction Pipeline:** IF, ID, OF, EX, WB stages.
                    * **Hazards:** Structural, Data (RAW, WAR, WAW), Control/Branch hazards.
                    """)

            elif sel_mod == "Unit 6: Memory Hierarchy (Cache Mapping, RAM/ROM, Virtual Memory)":
                with st.expander("1. Cache Memory Mapping & Virtual Memory", expanded=True):
                    st.write("""
                    * **Hierarchy:** Registers $\\rightarrow$ Cache (L1, L2) $\\rightarrow$ RAM $\\rightarrow$ Secondary SSD/HDD.
                    * **Locality of Reference:** Temporal Locality aur Spatial Locality.
                    * **Cache Mapping:** Direct Mapping, Associative Mapping, Set-Associative Mapping.
                    * **Virtual Memory:** Paging, Page Faults, TLB (Translation Lookaside Buffer).
                    """)

            elif sel_mod == "Unit 7: Input-Output Organization (Interrupts, DMA, Programmed I/O)":
                with st.expander("1. I/O Modes & Direct Memory Access (DMA)", expanded=True):
                    st.write("""
                    * **Programmed I/O vs Interrupt-Initiated I/O.**
                    * **DMA (Direct Memory Access):** CPU ko bypass karke high-speed data transfer: Bus Request (BR) aur Bus Grant (BG).
                    """)

        # ------------------- 3. MATHEMATICS SYLLABUS -------------------
        elif active_subj == "📐 Mathematics & Numerical Methods":
            st.markdown("""
            <div class="hero-banner">
                <div class="hero-title">BCA Discrete Mathematics & Numerical Methods</div>
                <div class="hero-sub">MLK PG College Balrampur • BCA University Syllabus (Sets, Logic, Matrices, Calculus & Numerical Algorithms)</div>
            </div>
            """, unsafe_allow_html=True)

            math_modules = [
                "Unit 1: Set Theory, Relations, Functions & Partially Ordered Sets (Posets)",
                "Unit 2: Mathematical Logic, Propositional Calculus & Truth Tables",
                "Unit 3: Matrices, Determinants, Rank & System of Linear Equations",
                "Unit 4: Combinatorics, Permutations & Graph Theory Basics",
                "Unit 5: Differential & Integral Calculus (Limits, Continuity, Maxima/Minima)",
                "Unit 6: Numerical Methods (Bisection, Newton-Raphson, Gauss Elimination)"
            ]
            sel_mod = st.selectbox("📚 Select Mathematics Unit:", math_modules)

            if sel_mod == "Unit 1: Set Theory, Relations, Functions & Partially Ordered Sets (Posets)":
                with st.expander("1. Relations, Equivalence Classes & POSET", expanded=True):
                    st.write("""
                    * **Equivalence Relation:** Reflexive, Symmetric aur Transitive relation.
                    * **POSET (Partially Ordered Set):** Reflexive, Antisymmetric aur Transitive relation. Hasse Diagrams.
                    """)

            elif sel_mod == "Unit 2: Mathematical Logic, Propositional Calculus & Truth Tables":
                with st.expander("1. Propositions, Tautology, Fallacy & Inference Rules", expanded=True):
                    st.write("""
                    * Connectives: Negation ($\\neg$), Conjunction ($\\land$), Disjunction ($\\lor$), Implication ($\\rightarrow$).
                    * Modus Ponens, Modus Tollens.
                    """)

            elif sel_mod == "Unit 3: Matrices, Determinants, Rank & System of Linear Equations":
                with st.expander("1. Rank of Matrix, Consistency & Cayley-Hamilton Theorem", expanded=True):
                    st.write("""
                    * **Consistency Theorem (Rouche-Capelli):**
                      * $Rank(A) = Rank(A|B) = n \\implies$ Unique Solution.
                      * $Rank(A) = Rank(A|B) < n \\implies$ Infinite Solutions.
                      * $Rank(A) \\neq Rank(A|B) \\implies$ Inconsistent.
                    * **Eigenvalues:** $|A - \\lambda I| = 0$. Cayley-Hamilton theorem states every square matrix satisfies its own characteristic equation.
                    """)

            elif sel_mod == "Unit 4: Combinatorics, Permutations & Graph Theory Basics":
                with st.expander("1. Pigeonhole Principle & Planar Graphs", expanded=True):
                    st.write("""
                    * Handshaking Theorem: $\\sum deg(v) = 2E$.
                    * Euler's Formula for Planar Graphs: $V - E + R = 2$.
                    """)

            elif sel_mod == "Unit 5: Differential & Integral Calculus (Limits, Continuity, Maxima/Minima)":
                with st.expander("1. Successive Differentiation & Taylor / Maclaurin Series", expanded=True):
                    st.write("""
                    * Leibnitz's Theorem for $n$-th derivative. Maxima/Minima test: $rt - s^2 > 0$.
                    """)

            elif sel_mod == "Unit 6: Numerical Methods (Bisection, Newton-Raphson, Gauss Elimination)":
                with st.expander("1. Newton-Raphson & Root Finding Algorithms", expanded=True):
                    st.write("""
                    * Newton-Raphson Formula:
                      $$x_{n+1} = x_n - \\frac{f(x_n)}{f'(x_n)}$$
                      (Quadratic convergence, order = 2).
                    """)

        # Bottom AI Action Container
        st.markdown(f"""
        <div class="apple-glass-card">
            <h3 style="margin-top:0; font-size:20px; font-weight:700;">🎯 AI University Exam Preparation & Viva Master ({active_subj})</h3>
            <p style="color:#94A3B8; font-size:13px; margin-bottom:14px;">MLK PG College / Maa Pateshwari University exam ke top expected questions aur viva points generate karein:</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔥 Generate Most Important Exam Questions & Viva Points", use_container_width=True):
            with st.spinner(f"AI Professor analyzing {active_subj} for MLK PG College Balrampur..."):
                prompt = f"""
                You are a senior BCA university examiner for MLK PG College, Balrampur (affiliated with Maa Pateshwari State University).
                Subject: {active_subj}
                Active Unit/Topic: {sel_mod}
                
                1. Provide the top 3 high-weightage theory examination questions (5-10 marks format) with complete model answers.
                2. Provide 3 tricky Viva-Voce questions with short, precise, examiner-winning answers.
                3. Highlight 2 critical practical/numerical pitfalls students usually make in university exams and how to avoid them.
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
                placeholder="e.g. Cache Mapping / Polymorphism / Eigenvalues / K-Maps"
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
                "4-Bit ALU Software Simulator (Logic Gates & Arithmetic)",
                "Direct-Mapped vs Set-Associative Cache Memory Simulator",
                "8-Bit Instruction Set Architecture (ISA) & CPU Emulator",
                "Booth's Multiplication Algorithm Simulator with Step Tracing",
                "Virtual Memory Page Replacement Simulator (FIFO, LRU, Optimal)"
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
            starter = """# CSA Binary & Bitwise Logic Simulator
a = 0b1100  # 12 in binary
b = 0b1010  # 10 in binary

print("A (Binary):", bin(a))
print("B (Binary):", bin(b))
print("Bitwise AND (A & B):", bin(a & b))
print("Bitwise OR  (A | B):", bin(a | b))
print("Bitwise XOR (A ^ B):", bin(a ^ b))
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
