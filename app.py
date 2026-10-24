import streamlit as st
import google.generativeai as genai
import io
import contextlib
import time

st.set_page_config(
    page_title="BCA Python Master Ecosystem | Created by Raj",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Session state initialization
if "app_entered" not in st.session_state:
    st.session_state.app_entered = False

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
        padding-bottom: 125px !important;
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
        font-size: 54px;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 0%, #A5B4FC 35%, #38BDF8 70%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 12px;
        letter-spacing: -1.5px;
    }
    .splash-subtitle {
        font-size: 17px;
        color: #94A3B8;
        max-width: 640px;
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
        background: rgba(20, 24, 38, 0.85);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-left: 4px solid #8B5CF6;
        border-radius: 14px;
        padding: 22px;
        margin-top: 16px;
        color: #F8FAFC;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        line-height: 1.65;
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

    /* ================= ADAPTIVE AUTO-DETECTING FLOATING DOCK ================= */
    /* DESKTOP / LAPTOP DISPLAY */
    div[data-testid="stRadio"] {
        position: fixed !important;
        bottom: 20px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        z-index: 999999 !important;
        background: rgba(18, 22, 34, 0.78) !important;
        border: 1px solid rgba(255, 255, 255, 0.16) !important;
        padding: 8px 20px !important;
        border-radius: 40px !important;
        backdrop-filter: blur(30px) saturate(190%) !important;
        -webkit-backdrop-filter: blur(30px) saturate(190%) !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.65), inset 0 1px 1px rgba(255, 255, 255, 0.2) !important;
        width: auto !important;
        max-width: 90vw !important;
    }

    div[data-testid="stRadio"] > label {
        display: none !important;
    }

    div[data-testid="stRadio"] > div {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 12px !important;
        align-items: center !important;
        justify-content: center !important;
    }

    div[data-testid="stRadio"] label {
        background: transparent !important;
        border-radius: 20px !important;
        padding: 6px 14px !important;
        margin: 0 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        color: #CBD5E1 !important;
        white-space: nowrap !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
    }

    div[data-testid="stRadio"] label:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        color: #FFFFFF !important;
    }

    /* MOBILE AUTO-DETECTION (< 768px Viewport) */
    @media (max-width: 768px) {
        .splash-title {
            font-size: 36px !important;
        }
        .hero-title {
            font-size: 22px !important;
        }
        .hero-banner {
            padding: 16px 18px !important;
        }
        .apple-glass-card {
            padding: 16px !important;
        }

        /* Mobile Island Dock: Horizontal pill, no vertical wrapping */
        div[data-testid="stRadio"] {
            bottom: 12px !important;
            padding: 6px 10px !important;
            border-radius: 30px !important;
            width: 94vw !important;
            max-width: 94vw !important;
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
            scrollbar-width: none !important;
        }
        div[data-testid="stRadio"]::-webkit-scrollbar {
            display: none !important;
        }
        div[data-testid="stRadio"] > div {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            gap: 6px !important;
            width: max-content !important;
            justify-content: flex-start !important;
        }
        div[data-testid="stRadio"] label {
            padding: 5px 10px !important;
            font-size: 11px !important;
            border-radius: 16px !important;
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
        st.markdown('<div class="badge-status">● AI Mentor Active</div>', unsafe_allow_html=True)
    else:
        with st.expander("🔑 Setup API Key", expanded=True):
            gemini_key = st.text_input("Gemini API Key:", type="password")
            if gemini_key:
                genai.configure(api_key=gemini_key)
                st.success("Connected!")
    st.caption("Crafted with ❤️ by Raj • Gemini Autonomous Engine")

# Auto-Fallback Resilient AI Caller (Eliminates 429 & 504 Errors completely)
def get_ai_response(prompt):
    if not gemini_key:
        return "⚠️ Pehle Gemini API Key configure karein."
    
    # Priority Candidate Pool: Ek model 429 quota dega toh next available model turant handle karega
    candidate_models = [
        "models/gemini-3.8-flash",
        "models/gemini-3.5-flash-lite",
        "models/gemini-3.1-flash-lite",
        "models/gemini-2.0-flash"
    ]
    
    last_error = ""
    for model_name in candidate_models:
        for attempt in range(2):
            try:
                model = genai.GenerativeModel(
                    model_name=model_name,
                    generation_config={"temperature": 0.4, "max_output_tokens": 8192}
                )
                response = model.generate_content(
                    prompt,
                    request_options={"timeout": 60.0}
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                last_error = str(e)
                if "429" in last_error:
                    time.sleep(1.0)
                    break # Switch to next candidate model immediately
                elif "504" in last_error or "deadline" in last_error.lower():
                    time.sleep(1.0)
                    continue

    return f"⏳ AI Engine Temporary Busy. Details: {last_error}"

# ================= 0. OPENING SCREEN (CREATED BY RAJ) =================
if not st.session_state.app_entered:
    st.markdown("""
    <div class="splash-container">
        <div class="creator-badge">✨ Next-Gen Education Portal</div>
        <div class="splash-title">BCA Python AI Suite</div>
        <div class="creator-signature">Crafted & Created by Raj ⚡</div>
        <div class="splash-subtitle">
            Autonomous university curriculum, interactive smart testing engine, 
            production project blueprints, and 24/7 AI mentor intelligence.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        if st.button("🚀 Launch Portal & Start Studying", use_container_width=True):
            st.session_state.app_entered = True
            st.rerun()

else:
    # Top Creator Watermark Banner
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; padding: 7px 16px; background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; margin-bottom: 16px;">
        <span style="font-size: 13px; color: #94A3B8;">🎓 BCA Computer Science Ecosystem</span>
        <span style="font-size: 13px; font-weight: 700; color: #38BDF8;">⚡ Created by Raj</span>
    </div>
    """, unsafe_allow_html=True)

    def render_syllabus():
        st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">BCA Python Encyclopedia & Complete Syllabus</div>
            <div class="hero-sub">Python ka har ek concept: Basic variables se lekar Advanced OOP, File I/O, Serialization aur Regex tak.</div>
        </div>
        """, unsafe_allow_html=True)

        modules = [
            "Module 1: Language Basics, Operators & Bitwise",
            "Module 2: Control Flow & Iteration (Branches & Loops)",
            "Module 3: Functions, Scopes, Lambdas & Recursion",
            "Module 4: In-Depth Data Structures (Lists, Tuples, Dicts, Sets)",
            "Module 5: Object-Oriented Programming (OOP Architecture)",
            "Module 6: File Handling, Context Managers & JSON/CSV",
            "Module 7: Exception Handling & Custom Errors",
            "Module 8: Standard Libraries, Regex & Date-Time"
        ]

        selected_module = st.selectbox("📚 Select Topic Module to Study:", modules)

        # ---------------- MODULE 1 ----------------
        if selected_module == "Module 1: Language Basics, Operators & Bitwise":
            st.markdown("### 🔹 Module 1: Core Fundamentals")
            
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
                * **Binary:** `bytes`, `bytearray`, `memoryview`.
                * **Mapping:** `dict`.
                * **Set Types:** `set`, `frozenset`.
                * **Boolean:** `bool` (`True` / `False`).
                
                **Type Casting:**
                * **Implicit Casting:** Python automatic smaller data type ko larger type mein elevate karta hai (jaise `int + float -> float`).
                * **Explicit Casting:** Programmer manually `int()`, `float()`, `str()`, `bool()`, `list()`, `set()`, ya `tuple()` functions se data convert karta hai.
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
print(f"Grand Total with 18% GST: INR {grand_total:.2f}")

# Boolean Conversion rules
print("bool(0):", bool(0))         # False
print("bool('Hello'):", bool("Hello")) # True
print("bool([]):", bool([]))       # False (Empty collection)""", language="python")

            with st.expander("3. Complete Operators (Arithmetic, Relational, Logical, Bitwise, Identity & Membership)", expanded=False):
                st.write("""
                **Operators Hierarchy & Mechanics:**
                * **Arithmetic:** `+`, `-`, `*`, `/` (float quotient), `//` (floor division - removes fractional part), `%` (modulus remainder), `**` (exponentiation/power).
                * **Comparison / Relational:** `==`, `!=`, `>`, `<`, `>=`, `<=`.
                * **Logical:** `and` (both must be true), `or` (at least one true), `not` (inverts truth value). Short-circuit evaluation follow hoti hai.
                * **Bitwise Operators:** Individual bits par direct calculation:
                  * `&` (Bitwise AND)
                  * `|` (Bitwise OR)
                  * `^` (Bitwise XOR - odd parity)
                  * `~` (Bitwise NOT - 2's complement: `~x = -(x + 1)`)
                  * `<<` (Bitwise Left Shift - multiplies by $2^n$)
                  * `>>` (Bitwise Right Shift - floor divides by $2^n$)
                * **Identity Operators (`is`, `is not`):** Checks memory location equality (`id(x) == id(y)`).
                * **Membership Operators (`in`, `not in`):** Checks container inclusion.
                """)
                st.code("""a = 14  # Binary: 0000 1110
b = 4   # Binary: 0000 0100

print("Floor Division (14 // 4):", a // b) # 3
print("Modulus Remainder (14 % 4):", a % b) # 2
print("Exponentiation (14 ** 2):", a ** 2)  # 196

# Bitwise Operations
print("Bitwise AND (14 & 4):", a & b)      # 0100 -> 4
print("Bitwise OR  (14 | 4):", a | b)      # 1110 -> 14
print("Bitwise XOR (14 ^ 4):", a ^ b)      # 1010 -> 10
print("Bitwise NOT (~14):", ~a)            # -(14 + 1) -> -15
print("Left Shift (4 << 2):", b << 2)      # 4 * (2^2) -> 16
print("Right Shift (14 >> 1):", a >> 1)    # 14 // 2 -> 7

# Identity vs Value Equality Check
seq1 = [10, 20, 30]
seq2 = [10, 20, 30]
print("seq1 == seq2 (Value Equality):", seq1 == seq2)     # True
print("seq1 is seq2 (Memory Reference Equality):", seq1 is seq2) # False
print("20 in seq1 (Membership Test):", 20 in seq1)        # True""", language="python")

        # ---------------- MODULE 2 ----------------
        elif selected_module == "Module 2: Control Flow & Iteration (Branches & Loops)":
            st.markdown("### 🔹 Module 2: Decision Making & Loops")
            
            with st.expander("1. Conditional Branching (if, elif, else, Nested Branching, Ternary Operators)", expanded=True):
                st.write("""
                **Control Flow Architecture:**
                * Python curly braces `{}` ke bajaye **Indentation (standard 4 spaces)** use karta hai blocks of execution define karne ke liye.
                * **Ternary Operator (Conditional Expression):** Single line mein decision evaluation karta hai:
                  `result = expression_if_true if condition else expression_if_false`
                * **Truthy and Falsy values:** `0`, `0.0`, `""` (empty string), `None`, `[]`, `{}`, `()` sabhi `False` evaluate hote hain. Baki sab `True`.
                """)
                st.code("""marks = 86
attendance_percent = 78

# Inline Ternary Expression
hall_ticket_eligible = True if attendance_percent >= 75 else False
print("Admit Card Granted:", hall_ticket_eligible)

# Nested Decision Logic
if hall_ticket_eligible:
    if marks >= 90:
        division = "First Class with Distinction (Honors)"
    elif marks >= 75:
        division = "First Class"
    elif marks >= 50:
        division = "Second Class"
    else:
        division = "Pass Division"
    print(f"Academic Standing: {division}")
else:
    print("Detained due to attendance shortage (< 75%).")""", language="python")

            with st.expander("2. Loops in Python (for, while, range() internal step mechanism)", expanded=False):
                st.write("""
                **Iteration Mechanics:**
                * **`for` loop:** Collection ke items par iterate karta hai. Python ka `for` loop basically ek `for-each` construct hota hai jo internally `iter()` aur `next()` protocol follow karta hai.
                * **`while` loop:** Condition-controlled indefinite looping deta hai. Jab tak given boolean expression `True` rehta hai, block execute hota hai.
                * **`range(start, stop, step)`:** In-memory complete list create nahi karta; balki ek immutable sequence generator return karta hai jo memory efficient hota hai.
                """)
                st.code("""# Traverse sequence with negative step
print("Reverse Counting with step -2:")
for val in range(10, 0, -2):
    print(val, end=" -> ")
print("LAUNCH")

# Nested while loop for generating multiplication tables
num = 1
while num <= 3:
    multiplier = 1
    print(f"\\n--- Multiplication Table of {num} ---")
    while multiplier <= 5:
        print(f"{num} x {multiplier} = {num * multiplier}")
        multiplier += 1
    num += 1""", language="python")

            with st.expander("3. Loop Control Statements (break, continue, pass, for-else construct)", expanded=False):
                st.write("""
                **Control Jump Statements:**
                * **`break`:** Loop ko immediately terminate kar deta hai aur control loop ke bahar bhejta hai.
                * **`continue`:** Current round ki remaining lines ko skip karke agle iteration cycle par bhejta hai.
                * **`pass`:** No-operation placeholder statement (Syntactic requirement poori karne ke liye).
                * **`for-else` / `while-else` (Important BCA Viva Concept):** Loop ke sath attached `else` block tabhi run hota hai jab loop natural condition fail hone par khatam ho, yaani **kisi `break` statement se terminate na hua ho**!
                """)
                st.code("""# Searching prime number using for-else construct
test_number = 37

for divisor in range(2, int(test_number**0.5) + 1):
    if test_number % divisor == 0:
        print(f"{test_number} is composite, divided by {divisor}")
        break
else:
    # Yeh block tabhi execute hota hai jab loop poora chale aur break na lage
    print(f"{test_number} is a VERIFIED PRIME NUMBER (Loop completed without break)!")

# Demonstrate Continue & Pass
print("\\nOdd number print with continue:")
for n in range(1, 10):
    if n % 2 == 0:
        continue # Skip evens
    print(n, end=" ")
print()""", language="python")

        # ---------------- MODULE 3 ----------------
        elif selected_module == "Module 3: Functions, Scopes, Lambdas & Recursion":
            st.markdown("### 🔹 Module 3: Modular Programming")
            
            with st.expander("1. Function Architecture, Positional, Keyword, *args & **kwargs", expanded=True):
                st.write("""
                **Function Mechanics:**
                * Functions modularity, clean code separation, aur reusability facilitate karte hain.
                * **Positional Arguments:** Order matching ke hisab se parameter map hote hain.
                * **Keyword Arguments:** Parameter name specify karke pass kiye jate hain (order independent).
                * **Default Arguments:** Agar caller parameter pass na kare toh pre-assigned default value use hoti hai.
                * **`*args` (Arbitrary Positional):** Extra positional arguments ko ek **Tuple** mein pack kar leta hai.
                * **`**kwargs` (Arbitrary Keyword):** Extra named arguments ko ek **Dictionary** mein pack kar leta hai.
                """)
                st.code("""def register_student(name, roll, *registered_courses, college="BCA University", **exam_scores):
    print(f"=== Student Enrollment: {name} (Roll: {roll}) ===")
    print(f"Institution: {college}")
    print(f"Enrolled Courses ({len(registered_courses)}):", ", ".join(registered_courses))
    print("Course Marks Record:")
    for subject, score in exam_scores.items():
        print(f"  * {subject}: {score} / 100")

# Invocation with arbitrary positional (*args) and keyword arguments (**kwargs)
register_student(
    "Raj Shraff", 101,
    "Python Programming", "Computer System Architecture", "Discrete Mathematics",
    college="State IT Institute",
    Python=95, CSA=88, Discrete_Maths=91
)""", language="python")

            with st.expander("2. Scope Resolution (LEGB Rule), global and nonlocal keywords", expanded=False):
                st.write("""
                **Scope Hierarchy (LEGB Rule):**
                1. **L**ocal: Function ke body ke andar created variables.
                2. **E**nclosing: Outer nested enclosing function ke variables.
                3. **G**lobal: Module level par defined variables.
                4. **B**uilt-in: Python ke built-in names (jaise `print`, `len`, `range`, `Exception`).
                
                * **`global` keyword:** Function ke andar global variable ko modify karne ke liye use hota hai.
                * **`nonlocal` keyword:** Closures aur nested functions mein outer scope ke non-global variable ko mutate karne ke liye use hota hai.
                """)
                st.code("""portal_status = "Active"

def campus_registry():
    branch = "Lucknow Main Campus"
    
    def update_records():
        nonlocal branch # Modifies enclosing variable
        branch = "Noida Extension Campus"
        global portal_status # Modifies global variable
        portal_status = "Maintenance Mode"
        print("Inner scope updated branch to:", branch)
        
    update_records()
    print("Enclosing scope branch now reflects:", branch)

campus_registry()
print("Global portal status now reflects:", portal_status)""", language="python")

            with st.expander("3. Anonymous Functions (Lambda), map(), filter(), reduce()", expanded=False):
                st.write("""
                * **Lambda Expressions:** Inline single-line functions without `def`:
                  `lambda arguments: expression`
                * **`map(function, iterable)`:** Sequence ke har individual element par transformer apply karta hai.
                * **`filter(function, iterable)`:** Function ke boolean return value ke mutabik elements filter karta hai.
                * **`reduce(function, iterable)`:** `functools` package se imported function jo sequence ko pair-wise reduce karke single cumulative value return karta hai.
                """)
                st.code("""from functools import reduce

student_marks = [45, 88, 72, 91, 54, 63, 98, 41]

# 1. Filter students who scored First Class (>= 60)
first_class = list(filter(lambda mark: mark >= 60, student_marks))
print("First Class Scores:", first_class)

# 2. Map: Grant 5 grace marks to borderline passing scores (< 50)
grace_awarded = list(map(lambda m: m + 5 if m < 50 else m, student_marks))
print("Grace Marks Adjusted:", grace_awarded)

# 3. Reduce: Compute Aggregate Batch Total
batch_aggregate = reduce(lambda acc, val: acc + val, student_marks)
average_score = batch_aggregate / len(student_marks)
print(f"Batch Aggregate: {batch_aggregate} | Average Score: {average_score:.2f}")""", language="python")

            with st.expander("4. Recursion, Call Stack Mechanics, Base Cases & Recursion Limit", expanded=False):
                st.write("""
                **Recursive Function Theory:**
                * Recursion tab hota hai jab function khud ko bar-bar invoke kare jab tak terminal condition satisfy na ho jaye.
                * **Base Case:** Stopping condition jo infinite looping aur call stack overflow ko prevent karti hai.
                * **Call Stack:** Har function call system stack mein activation record (stack frame) allocate karti hai.
                * Python default recursion limit `1000` rakhta hai (`sys.getrecursionlimit()`). Limit exceed hone par `RecursionError` raise hota hai.
                """)
                st.code("""# Greatest Common Divisor (GCD / HCF) using Euclidean Recursive Algorithm
def compute_gcd(a, b):
    # Base Case
    if b == 0:
        return a
    # Recursive Case
    return compute_gcd(b, a % b)

num1, num2 = 48, 18
print(f"GCD of {num1} and {num2} via Recursion is: {compute_gcd(num1, num2)}")

# Tower of Hanoi Recursive Steps
def tower_of_hanoi(n, source, destination, auxiliary):
    if n == 1:
        print(f"Move disk 1 from rod {source} to rod {destination}")
        return
    tower_of_hanoi(n - 1, source, auxiliary, destination)
    print(f"Move disk {n} from rod {source} to rod {destination}")
    tower_of_hanoi(n - 1, auxiliary, destination, source)

print("\\nTower of Hanoi sequence for 3 Disks:")
tower_of_hanoi(3, 'A', 'C', 'B')""", language="python")

        # ---------------- MODULE 4 ----------------
        elif selected_module == "Module 4: In-Depth Data Structures (Lists, Tuples, Dicts, Sets)":
            st.markdown("### 🔹 Module 4: Data Structures & Memory Layout")
            
            with st.expander("1. Lists (Memory Architecture, Slicing, In-Place Methods, List Comprehensions)", expanded=True):
                st.write("""
                **List Internal Architecture:**
                * Python lists contiguous dynamic arrays of object pointers hoti hain. Heterogeneous data types store kar sakti hain.
                * **Mutable:** Memory address modify kiye bina elements update, insert, delete ho sakte hain.
                * **Slicing Mechanics:** `list[start:stop:step]` (Negative step poori list ko reverse karta hai).
                * **List Comprehension:** Declarative syntactic sugar jo loops ke comparison mein C-level speed par execute hoti hai.
                """)
                st.code("""# 2D Grid Matrix generation & manipulation
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Flatten 2D matrix into 1D list via nested list comprehension
flattened = [item for row in matrix for item in row]
print("Flattened List:", flattened)

# Extract only even squares
even_squares = [x**2 for x in flattened if x % 2 == 0]
print("Even Squares:", even_squares)

# In-place modifications
flattened.sort(reverse=True)
print("In-Place Descending Sort:", flattened)""", language="python")

            with st.expander("2. Tuples (Immutability, Packing, Asterisk Unpacking & Memory Efficiency)", expanded=False):
                st.write("""
                **Tuples vs Lists:**
                * Tuples immutable sequences hain. Ek baar create hone ke baad size ya contents alter nahi kiye ja sakte.
                * **Memory Efficiency:** Tuples fixed size ke karan lists se kam memory lete hain aur faster access time provide karte hain.
                * **Hashability:** Agar tuple ke sabhi elements immutable hon, toh tuple hashable hota hai aur dictionary key ban sakta hai.
                """)
                st.code("""# Advanced Tuple Unpacking with Extended Asterisk
student_record = ("Raj Shraff", "BCA", 1, "Semester A", 89.5, 92.0, 94.5, "Grade O")
name, degree, sem, section, *semester_marks, final_grade = student_record

print(f"Candidate: {name} | Course: {degree} (Sem {sem})")
print(f"Semester Marks Captured via *rest: {semester_marks}")
print(f"Final Standing: {final_grade}")

# Tuple as Dictionary Key (Coordinates / Composite IDs)
geo_nodes = {
    (28.6139, 77.2090): "New Delhi Head Office",
    (26.8467, 80.9462): "Lucknow Regional Campus"
}
print("Node at Coordinates:", geo_nodes[(26.8467, 80.9462)])""", language="python")

            with st.expander("3. Dictionaries (Hash Tables, Collision Resolution, Dict Comprehensions)", expanded=False):
                st.write("""
                **Dictionary Architecture:**
                * Hash table data structure par implemented key-value storage.
                * Average time complexity lookups, insertions aur deletions ke liye $O(1)$ hoti hai.
                * Keys unique aur strictly immutable honi chahiye. Values mutable ho sakti hain.
                * **Methods:** `.get(key, default)`, `.setdefault()`, `.pop()`, `.update()`, `.items()`.
                """)
                st.code("""curriculum_marks = {
    "Python": 95,
    "CSA": 88,
    "Calculus": 79,
    "Digital Electronics": 84,
    "Technical English": 91
}

# Safe Lookup with default fallback
print("DBMS Marks:", curriculum_marks.get("DBMS", "Not Registered Yet"))

# Dictionary Comprehension: High Achiever Subjects (Marks >= 85)
honors_subjects = {sub: mark for sub, mark in curriculum_marks.items() if mark >= 85}
print("Honors Qualified Subjects:", honors_subjects)

# Nested dictionary transformation
course_catalog = {
    "CS101": {"title": "Python Basics", "credits": 4},
    "CS102": {"title": "Computer Org", "credits": 3}
}
print("CS101 Credits:", course_catalog["CS101"]["credits"])""", language="python")

            with st.expander("4. Sets (Hashing, Mathematical Set Theory Operations, Frozenset)", expanded=False):
                st.write("""
                **Set Data Structure:**
                * Unordered, unindexed collection of unique elements. Duplicates automatically discard ho jate hain.
                * Elements must be hashable. Sets mutable hote hain jabki `frozenset` immutable set hota hai.
                * **Set Operations:** Union (`|`), Intersection (`&`), Difference (`-`), Symmetric Difference (`^`).
                """)
                st.code("""python_cohort = {"Raj", "Aman", "Rohan", "Khushi", "Vikram"}
c_cohort = {"Aman", "Khushi", "Sneha", "Karan", "Pooja"}

print("Enrolled in Both Subjects (Intersection):", python_cohort & c_cohort)
print("Only in Python (Difference):", python_cohort - c_cohort)
print("Unique across any subject (Symmetric Difference):", python_cohort ^ c_cohort)
print("Total Unique Roster (Union):", python_cohort | c_cohort)

# Immutable Frozenset
immutable_keys = frozenset(["ADMIN", "STUDENT", "EXAMINER"])
print("Frozenset:", immutable_keys)""", language="python")

        # ---------------- MODULE 5 ----------------
        elif selected_module == "Module 5: Object-Oriented Programming (OOP Architecture)":
            st.markdown("### 🔹 Module 5: Object-Oriented Programming Architecture")
            
            with st.expander("1. Classes, Objects, __init__ Constructor & self Parameter", expanded=True):
                st.write("""
                **Object-Oriented Paradigm:**
                * **Class:** User-defined prototype / blueprint jo real-world entity ki state aur behavior define karta hai.
                * **Object:** Heap memory mein class ka instantiated physical representation.
                * **`__init__()`:** Initializer method jo object creation ke samay instance variables ko bind karta hai.
                * **`self`:** Calling object ka direct memory reference.
                * **Class vs Instance Variables:** Class variables sabhi instances mein share hote hain, jabki instance variables har object ke unique hote hain.
                """)
                st.code("""class BCAStudent:
    # Class Attribute (Shared across entire batch)
    university_name = "State University of Technology"
    total_enrolled = 0

    def __init__(self, full_name, roll_no, semester=1):
        # Instance Attributes
        self.name = full_name
        self.roll = roll_no
        self.sem = semester
        BCAStudent.total_enrolled += 1

    def display_profile(self):
        return f"Roll: {self.roll} | Student: {self.name} | Sem: {self.sem} | Affiliation: {BCAStudent.university_name}"

s1 = BCAStudent("Raj Shraff", 101, 1)
s2 = BCAStudent("Aman Sharma", 102, 1)

print(s1.display_profile())
print(s2.display_profile())
print(f"Total Student Count: {BCAStudent.total_enrolled}")""", language="python")

            with st.expander("2. Encapsulation, Data Hiding, Getters/Setters & @property Decorator", expanded=False):
                st.write("""
                **Encapsulation Principles:**
                * Internal state ko direct accidental modification se protect karna.
                * **Public:** `self.name` (Directly accessible).
                * **Protected:** `self._marks` (Internal/subclass access convention).
                * **Private:** `self.__balance` (Name Mangling apply hoti hai: `_ClassName__variable`).
                * **`@property`:** Clean, Pythonic getter aur setter mechanism provide karta hai.
                """)
                st.code("""class FeeAccount:
    def __init__(self, student_name, initial_balance):
        self.student = student_name
        self.__balance = initial_balance # Private attribute

    @property
    def balance(self):
        \"\"\"Getter method\"\"\"
        return self.__balance

    @balance.setter
    def balance(self, new_amount):
        \"\"\"Setter method with validation\"\"\"
        if new_amount < 0:
            raise ValueError("Account balance cannot be negative!")
        self.__balance = new_amount

account = FeeAccount("Raj", 15000)
print(f"Fee Balance for {account.student}: INR {account.balance}")

account.balance = 20000 # Clean property setter
print("Updated Balance:", account.balance)""", language="python")

            with st.expander("3. Types of Inheritance (Single, Multiple, Multilevel, MRO & super())", expanded=False):
                st.write("""
                **Inheritance Architecture:**
                * Code reusability aur hierarchical classification provide karta hai.
                * **Single:** Child class single parent class ko inherit karti hai.
                * **Multilevel:** Base -> Intermediate -> Derived.
                * **Multiple:** Child ek se zyada parent classes inherit karti hai.
                * **Method Resolution Order (MRO):** C3 Linearization algorithm jo decide karta hai ki conflict hone par method kis class se resolve hoga.
                * **`super()`:** Parent class ke constructor aur methods ko seamlessly invoke karta hai.
                """)
                st.code("""class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Academics:
    def __init__(self, course, gpa):
        self.course = course
        self.gpa = gpa

# Multiple Inheritance
class Scholar(Person, Academics):
    def __init__(self, name, age, course, gpa, roll):
        Person.__init__(self, name, age)
        Academics.__init__(self, course, gpa)
        self.roll = roll

    def get_credentials(self):
        return f"Scholar {self.name} (Roll: {self.roll}) enrolled in {self.course} with GPA: {self.gpa}"

scholar1 = Scholar("Raj", 25, "BCA", 9.2, 101)
print(scholar1.get_credentials())
print("Method Resolution Order (MRO):", [cls.__name__ for cls in Scholar.__mro__])""", language="python")

            with st.expander("4. Polymorphism, Method Overriding & Dunder / Magic Methods", expanded=False):
                st.write("""
                * **Method Overriding:** Subclass parent ke method ko specialized implementation deti hai.
                * **Operator Overloading via Magic Methods:**
                  * `__str__()`: User-friendly printable string representation.
                  * `__repr__()`: Developer debugging representation.
                  * `__len__()`: Object par `len()` call hone par execute hota hai.
                  * `__add__()`: `+` operator ko custom logic deta hai.
                """)
                st.code("""class SyllabusModule:
    def __init__(self, title, total_hours):
        self.title = title
        self.hours = total_hours

    def __str__(self):
        return f"Curriculum Module: '{self.title}' ({self.hours} Hours)"

    def __len__(self):
        return self.hours

    def __add__(self, other):
        # Overloading '+' to combine teaching hours
        return self.hours + other.hours

mod1 = SyllabusModule("Python Core & OOP", 45)
mod2 = SyllabusModule("Computer System Architecture", 40)

print(str(mod1))
print("Hours in Module 1:", len(mod1))
print("Total Semester Teaching Hours:", mod1 + mod2)""", language="python")

        # ---------------- MODULE 6 ----------------
        elif selected_module == "Module 6: File Handling, Context Managers & JSON/CSV":
            st.markdown("### 🔹 Module 6: Persistence & Serialization")
            
            with st.expander("1. File Modes, seek(), tell() & with context manager", expanded=True):
                st.write("""
                **File Handling Fundamentals:**
                * **Modes:**
                  * `'r'`: Read only (file must exist).
                  * `'w'`: Truncate and write (creates new file if not present).
                  * `'a'`: Append at end of file.
                  * `'r+'`: Read and write.
                  * `'b'`: Binary mode (for images, compiled data).
                * **Context Manager (`with` statement):** Ensures file handles automatically close hote hain chahe exception raise ho.
                * **`tell()`:** Current file pointer byte index batata hai.
                * **`seek(offset, whence)`:** File pointer position shift karta hai (`0`: start, `1`: current, `2`: end).
                """)
                st.code("""test_file = "bca_sample_log.txt"

# Safe write and read operations
with open(test_file, "w+", encoding="utf-8") as f:
    f.write("Line 1: BCA Semester 1 Python Practical\\nLine 2: University Lab Session 2026")
    print("Byte cursor after write:", f.tell())
    
    # Reposition pointer back to beginning
    f.seek(0)
    print("Byte cursor after seek(0):", f.tell())
    content = f.read()
    print("Read File Content:\\n" + content)""", language="python")

            with st.expander("2. JSON Serialization & Deserialization (json module)", expanded=False):
                st.write("""
                * **Serialization (Encoding):** Python data structure ko JSON string format mein convert karna (`json.dumps()`) ya file stream mein write karna (`json.dump()`).
                * **Deserialization (Decoding):** JSON string ko Python native dictionary/list mein parse karna (`json.loads()`) ya file stream se load karna (`json.load()`).
                """)
                st.code("""import json

student_database = {
    "student_id": "BCA-2026-101",
    "personal_details": {
        "name": "Raj Shraff",
        "verified": True,
        "semester": 1
    },
    "registered_subjects": ["Python", "CSA", "Mathematics", "Discrete Logic"],
    "score_sheet": {"Python": 95, "CSA": 88}
}

# Serialize dictionary to formatted JSON string
json_formatted = json.dumps(student_database, indent=2)
print("Serialized JSON Output:\\n", json_formatted)

# Deserialize JSON back into Python Dictionary
parsed_obj = json.loads(json_formatted)
print("\\nParsed Student Name:", parsed_obj["personal_details"]["name"])
print("Enrolled Subject Count:", len(parsed_obj["registered_subjects"]))""", language="python")

        # ---------------- MODULE 7 ----------------
        elif selected_module == "Module 7: Exception Handling & Custom Errors":
            st.markdown("### 🔹 Module 7: Error Resilience & Exceptions")
            
            with st.expander("1. Complete try-except-else-finally Architecture", expanded=True):
                st.write("""
                **Exception Pipeline Mechanics:**
                * **`try`:** Risky code block jahan runtime errors expect kiye ja sakte hain.
                * **`except SpecificException as err`:** Matching exception type ko intercept karke graceful recovery deta hai.
                * **`else`:** Tabhi run hota hai jab try block mein **koi error na aaye**.
                * **`finally`:** Chahe error throw ho ya na ho, cleanup actions (jaise memory deallocation, connection closing) ke liye guaranteed execute hota hai.
                """)
                st.code("""def robust_division_engine(numerator, denominator):
    try:
        val = float(numerator) / float(denominator)
    except ZeroDivisionError as zde:
        print(f"[ERROR CATCH] Math Error: Cannot divide by zero ({zde})")
        return None
    except ValueError as ve:
        print(f"[ERROR CATCH] Type Error: Numeric conversion failed ({ve})")
        return None
    else:
        print("[SUCCESS] Division completed without any errors.")
        return val
    finally:
        print("[FINALLY] Execution pipeline terminated successfully.")

print("Test Case 1 (10 / 2):", robust_division_engine(10, 2))
print("---")
print("Test Case 2 (10 / 0):", robust_division_engine(10, 0))""", language="python")

            with st.expander("2. Raising Exceptions & Creating Custom User-Defined Exception Classes", expanded=False):
                st.write("""
                * **`raise` keyword:** Manually business logic error trigger karta hai.
                * **Custom Exceptions:** Standard built-in `Exception` base class ko subclass karke project-level specific errors create kiye jate hain.
                """)
                st.code("""class InvalidMarksRangeException(Exception):
    def __init__(self, marks, msg="Marks must reside between 0 and 100"):
        self.marks = marks
        self.msg = msg
        super().__init__(f"{msg} -> Provided: {marks}")

def validate_semester_marks(score):
    if score < 0 or score > 100:
        raise InvalidMarksRangeException(score)
    return f"Valid score of {score}% recorded in university ledger."

try:
    print(validate_semester_marks(92))
    print(validate_semester_marks(120)) # Out of bounds
except InvalidMarksRangeException as err:
    print("Custom Security Validation Caught:", err)""", language="python")

        # ---------------- MODULE 8 ----------------
        elif selected_module == "Module 8: Standard Libraries, Regex & Date-Time":
            st.markdown("### 🔹 Module 8: Batteries-Included Standard Libraries")
            
            with st.expander("1. Standard Modules (math, random, datetime, sys, os)", expanded=True):
                st.write("""
                * **`math`:** Trigonometry, logarithms, integer square root (`math.isqrt`), factorials.
                * **`random`:** Pseudo-random numbers, shuffling lists (`random.shuffle`), choice selection.
                * **`datetime`:** Timestamp generation, date parsing (`strptime`), formatting (`strftime`), time deltas.
                """)
                st.code("""import math
import random
from datetime import datetime, timedelta

# Math operations
print("GCD of 36 and 60:", math.gcd(36, 60))
print("Factorial of 6:", math.factorial(6))

# Random generation
lucky_draw = ["Raj", "Aman", "Rohan", "Pooja", "Khushi"]
print("Random Winner:", random.choice(lucky_draw))

# Datetime formatting & time calculations
current_time = datetime.now()
print("Current Formatted Date:", current_time.strftime("%A, %d-%B-%Y %I:%M:%S %p"))
exam_date = current_time + timedelta(days=60)
print("Semester Exams Start Date:", exam_date.strftime("%d %B %Y"))""", language="python")

            with st.expander("2. Regular Expressions (re module pattern matching)", expanded=False):
                st.write("""
                **Regex Syntactical Components:**
                * `re.search()`: String ke kisi bhi hisse mein first matching pattern dhundhta hai.
                * `re.findall()`: Saare matching occurrences ki list deta hai.
                * `re.sub()`: Matched substrings ko replacement string se replace karta hai.
                * `\d` (digit), `\w` (word character), `+` (1 ya zyada), `*` (0 ya zyada), `^` (start), `$` (end).
                """)
                st.code("""import re

document_data = \"\"\"
Candidate: Raj Shraff (Roll: 101)
Primary Email: raj.shraff@university.edu.in
Personal Email: rajshraff2001@gmail.com
Phone Contact: +91-9876543210
Alternate Contact: +91-8765432109
\"\"\"

# Extract all valid email addresses
email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
emails_found = re.findall(email_pattern, document_data)
print("Extracted Valid Emails:", emails_found)

# Extract phone numbers with international code
phone_pattern = r'\+91-\d{10}'
phones_found = re.findall(phone_pattern, document_data)
print("Extracted Indian Phone Numbers:", phones_found)""", language="python")

        # ================= APPLE GLASS BOTTOM ACTION BAR =================
        st.markdown("""
        <div class="apple-glass-card">
            <h3 style="margin-top:0; font-size:20px; font-weight:700;">🎯 AI University Exam Preparation & Viva Master</h3>
            <p style="color:#94A3B8; font-size:13px; margin-bottom:14px;">Iss module ke expected university exam questions aur viva points generate karein:</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔥 Generate Most Important Exam Questions & Viva Points", use_container_width=True):
            with st.spinner("AI Professor analyzing syllabus & trends (Max 8192 Tokens Enabled)..."):
                prompt = f"""
                You are a senior computer science examiner for BCA university exams.
                For the module: '{selected_module}':
                1. Provide the top 3 high-weightage theory examination questions (5-10 marks format) with complete model answers.
                2. Provide 3 tricky Viva-Voce questions with short, precise, examiner-winning answers.
                3. Highlight 2 critical practical coding pitfalls/mistakes students usually make in university lab exams and how to fix them.
                Format cleanly using bolding and clear bullet points.
                """
                ai_output = get_ai_response(prompt)
                st.markdown(f'<div class="ai-box">{ai_output}</div>', unsafe_allow_html=True)

    def render_exam_engine():
        st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">Automated Exam & Evaluation Suite</div>
            <div class="hero-sub">Generate unique semester exam papers on the fly and get instant grading with line-by-line feedback.</div>
        </div>
        """, unsafe_allow_html=True)

        t_unit = st.selectbox("Exam Module:", [
            "Module 1: Language Basics, Operators & Bitwise",
            "Module 2: Control Flow & Iteration (Branches & Loops)",
            "Module 3: Functions, Scopes, Lambdas & Recursion",
            "Module 4: In-Depth Data Structures (Lists, Tuples, Dicts, Sets)",
            "Module 5: Object-Oriented Programming (OOP Architecture)",
            "Module 6: File Handling, Context Managers & JSON/CSV",
            "Module 7: Exception Handling & Custom Errors",
            "Module 8: Standard Libraries, Regex & Date-Time"
        ])
        
        if st.button("⚡ Generate New Test Paper", use_container_width=True):
            with st.spinner("Drafting fresh exam questions..."):
                test_prompt = f"""
                Create a 10-mark mini examination paper for BCA students on '{t_unit}'.
                - Question 1 (2 Marks): Conceptual definition.
                - Question 2 (3 Marks): Output prediction or short difference.
                - Question 3 (5 Marks): Real-world coding question.
                Keep questions strict and university-grade. Do NOT give solutions.
                """
                st.session_state.current_test = get_ai_response(test_prompt)

        if "current_test" in st.session_state:
            st.markdown(f'<div class="apple-glass-card"><h4>📄 Current Question Paper</h4>{st.session_state.current_test}</div>', unsafe_allow_html=True)

            st.markdown("#### ✍️ Write & Submit Answers")
            user_sol = st.text_area("Yahan apne answers aur codes type karein:", height=200, placeholder="Q1: ...\nQ2: ...\nQ3 (Code): ...")
            if st.button("🚀 Submit Sheet For AI Checking", use_container_width=True):
                if not user_sol.strip():
                    st.warning("Please type your answer before submission.")
                else:
                    with st.spinner("AI checking answers..."):
                        eval_prompt = f"""
                        You are a strict BCA university examiner grading a student's answer sheet.
                        Paper:
                        {st.session_state.current_test}

                        Student Answer:
                        {user_sol}

                        Evaluate thoroughly:
                        1. Score out of 10 with clear breakdown.
                        2. Detailed remarks: strengths and missing elements.
                        3. Perfect model answer and corrected code.
                        """
                        scorecard = get_ai_response(eval_prompt)
                        st.markdown(f'<div class="ai-box"><h3>📊 Examination Scorecard</h3>{scorecard}</div>', unsafe_allow_html=True)

    def render_projects():
        st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">Semester Capstone Project Lab</div>
            <div class="hero-sub">Complete full-scale BCA projects step-by-step with architecture design and examiner-ready viva prep.</div>
        </div>
        """, unsafe_allow_html=True)

        proj = st.selectbox(
            "Choose Capstone Project:",
            [
                "Student Management System (Console + File / SQLite)",
                "Banking Operations & ATM Simulator (OOPs Based)",
                "Supermarket Inventory & Automated Billing Engine",
                "Hospital Management & Patient Appointment Scheduler",
                "Library Book Circulation & Fine Calculation Engine"
            ]
        )

        st.markdown(f"""
        <div class="apple-glass-card">
            <h4 style="margin-top:0;">🏗️ Architecture: {proj}</h4>
            <p>Complete multi-tiered design pattern with verified logic flow, data structures and error handling blocks.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Get Starter Architecture & Complete Code", use_container_width=True):
            with st.spinner("AI Architect designing codebase..."):
                blueprint_prompt = f"""
                Provide a complete, production-grade, well-commented Python starter project for: '{proj}'.
                Include OOP classes, error checks, persistent storage, and interactive menu loop.
                """
                st.markdown(f'<div class="ai-box">{get_ai_response(blueprint_prompt)}</div>', unsafe_allow_html=True)

    def render_mentor():
        st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">24/7 BCA Technical Mentor</div>
            <div class="hero-sub">Resolve coding doubts, syntax comparisons with C language, or logic errors in seconds.</div>
        </div>
        """, unsafe_allow_html=True)

        user_q = st.text_area("Poochhein apna doubt ya code paste karein:", height=140, placeholder="e.g. C Pointers ka alternative Python mein kya hota hai?")
        if st.button("⚡ Ask AI Mentor", use_container_width=True):
            if not user_q.strip():
                st.warning("Pehle sawal enter karein.")
            else:
                with st.spinner("AI Mentor analyzing..."):
                    ans = get_ai_response(f"You are a BCA Computer Science professor. Answer clearly with clean code examples:\n\n{user_q}")
                    st.markdown(f'<div class="ai-box">{ans}</div>', unsafe_allow_html=True)

    def render_runner():
        st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">Integrated Python Sandbox</div>
            <div class="hero-sub">Write, test, and execute Python code with console output directly in your browser.</div>
        </div>
        """, unsafe_allow_html=True)

        starter = """# BCA Python Interactive Sandbox
def greet(name, sem):
    return f"Hello {name}, Welcome to BCA Semester {sem}!"

msg = greet("Raj", 1)
print(msg)
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

    # ================= FLOATING APPLE DOCK NAVIGATION =================
    selected_tab = st.radio(
        label="Apple Dock Navigation",
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
