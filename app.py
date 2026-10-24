import streamlit as st
import google.generativeai as genai
import io
import contextlib

st.set_page_config(
    page_title="BCA Python Master Ecosystem | Created by Raj",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Session state for Opening Splash Screen
if "app_entered" not in st.session_state:
    st.session_state.app_entered = False

# ================= APPLE FROSTED GLASS & MODERN UI CSS =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

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
        padding-bottom: 120px !important;
    }

    /* Premium Intro Splash Screen */
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

    /* AI Response Glass Capsule */
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

    /* Floating Apple Dock at the Bottom */
    div[data-testid="stRadio"] {
        position: fixed;
        bottom: 18px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 999999;
        background: rgba(20, 24, 38, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        padding: 8px 18px !important;
        border-radius: 36px !important;
        backdrop-filter: blur(35px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(35px) saturate(180%) !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), inset 0 1px 1px rgba(255, 255, 255, 0.15) !important;
        max-width: 95vw;
    }
    div[data-testid="stRadio"] > label {
        display: none !important;
    }
    div[data-testid="stRadio"] > div {
        flex-direction: row !important;
        gap: 10px !important;
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
        transition: all 0.25s ease !important;
    }
    div[data-testid="stRadio"] label:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        color: #FFFFFF !important;
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
    st.caption("Crafted with ❤️ by Raj • Gemini 3.8 Flash")

# Fast AI Generator function (60s timeout to prevent 504 Deadline Exceeded)
def get_ai_response(prompt):
    if not gemini_key:
        return "⚠️ Pehle Gemini API Key configure karein."
    try:
        model = genai.GenerativeModel(
            model_name="models/gemini-3.8-flash",
            generation_config={"temperature": 0.4, "max_output_tokens": 850}
        )
        response = model.generate_content(
            prompt,
            request_options={"timeout": 60.0}
        )
        return response.text
    except Exception as e:
        err_msg = str(e)
        if "429" in err_msg:
            return "⏳ **Free Tier Rate Limit (429):** Request limit exceed ho chuki hai. Kripya 25-30 seconds wait karke dubara try karein."
        elif "504" in err_msg or "deadline expired" in err_msg.lower():
            return "⚠️ **Server Busy:** Response aane mein samay lag raha hai, kripya dubara click karein."
        elif "timed out" in err_msg.lower():
            return "⚠️ **Connection Timeout:** Network slow hai, dubara try karein."
        return f"AI Error: {err_msg}"

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
                * Python ek interpreted aur high-level programming language hai. Source code (`.py`) pehle Bytecode (`.pyc`) mein compile hota hai, jo platform-independent hota hai.
                * Bytecode ko Python Virtual Machine (PVM) line-by-line machine code (binary) mein translate karke execute karta hai.
                * **Dynamic Typing vs Static Typing:** C ya C++ mein variable declare karte samay type batana padta hai (`int a = 10;`). Python dynamically typed hai; variable runtime par assigned value ke hisab se type acquire karta hai. Variable references create karta hai heap objects par.
                """)
                st.code("""# Dynamic Typing & Object Reference Example
x = 101
print(f"Value: {x} | Type: {type(x)} | Memory ID: {id(x)}")

# Same identifier ab naye string object ko point karega
x = "Raj Shraff"
print(f"Value: {x} | Type: {type(x)} | Memory ID: {id(x)}")""", language="python")

            with st.expander("2. Identifiers, Keywords, Data Types & Type Casting", expanded=False):
                st.write("""
                **Rules for Identifiers:**
                * Alphabets (`a-z`, `A-Z`), digits (`0-9`), aur underscore (`_`) allow hote hain.
                * Kabhi bhi digit se start nahi ho sakta (`1name` invalid hai, `name_1` valid hai).
                * Keywords (jaise `def`, `class`, `if`, `while`, `pass`) identifiers ke rup mein use nahi ho sakte.
                
                **Type Casting:**
                * **Implicit:** Python automatic small data type ko large type mein promote karta hai (e.g. `int + float -> float`).
                * **Explicit:** Programmer manually `int()`, `float()`, `str()`, `bool()`, ya `list()` functions se cast karta hai.
                """)
                st.code("""# Type Casting & Formatting
raw_str = "150"
converted = int(raw_str)
tax_rate = 0.18
final_amt = converted + (converted * tax_rate)

print(f"Original: {raw_str} ({type(raw_str)})")
print(f"Converted: {converted} ({type(converted)})")
print(f"Final with 18% GST: INR {final_amt:.2f}")""", language="python")

            with st.expander("3. Complete Operators (Arithmetic, Relational, Logical, Bitwise, Identity, Membership)", expanded=False):
                st.write("""
                **Operators Hierarchy:**
                * **Arithmetic:** `+`, `-`, `*`, `/` (float division), `//` (floor division - quotient integer deta hai), `%` (remainder), `**` (exponentiation).
                * **Bitwise:** Binary bits par direct compute karta hai (`&` AND, `|` OR, `^` XOR, `~` NOT, `<<` Left shift, `>>` Right shift).
                * **Identity (`is`, `is not`):** Check karta hai kya dono variables memory mein exact same object point kar rahe hain (`id(a) == id(b)`).
                * **Membership (`in`, `not in`):** Kisi sequence (list, string, tuple) ke andar value exist karti hai ya nahi.
                """)
                st.code("""a = 14  # Binary: 1110
b = 4   # Binary: 0100

print("Floor Division (14 // 4):", a // b) # 3
print("Modulus Remainder (14 % 4):", a % b) # 2
print("Power Exponent (14 ** 2):", a ** 2)  # 196

# Bitwise Operations
print("Bitwise AND (14 & 4):", a & b)      # 4
print("Bitwise XOR (14 ^ 4):", a ^ b)      # 10
print("Left Shift (4 << 1):", b << 1)      # 8

# Identity vs Equality
list1 = [1, 2, 3]
list2 = [1, 2, 3]
print("list1 == list2 (Values match):", list1 == list2) # True
print("list1 is list2 (Same memory address):", list1 is list2) # False""", language="python")

        # ---------------- MODULE 2 ----------------
        elif selected_module == "Module 2: Control Flow & Iteration (Branches & Loops)":
            st.markdown("### 🔹 Module 2: Decision Making & Loops")
            
            with st.expander("1. Conditional Branching (if, elif, else, Nested if, Ternary Operator)", expanded=True):
                st.write("""
                **Control Flow Architecture:**
                * Python mein branching code blocks ko define karne ke liye curly braces `{}` ke badle **4 spaces indentation** compulsory hoti hai.
                * **Ternary Operator (Conditional Expression):** Single-line decision making ke liye:
                  `result = true_value if condition else false_value`
                """)
                st.code("""marks = 84

# Inline Ternary Evaluation
verdict = "Distinction" if marks >= 80 else "Regular Pass"
print(f"Status: {verdict}")

# Multi-way branching
if marks >= 90:
    print("Grade: O (Outstanding)")
elif marks >= 75:
    print("Grade: A+ (First Class with Distinction)")
elif marks >= 60:
    print("Grade: A (First Class)")
elif marks >= 40:
    print("Grade: B (Second Class)")
else:
    print("Grade: F (Fail/Re-appear)")""", language="python")

            with st.expander("2. Loops in Python (for, while, range() internal step mechanism)", expanded=False):
                st.write("""
                * **`for` loop:** Sequence iteration ke liye banaya gaya hai. Internally Iterator Protocol (`__iter__()` aur `__next__()`) follow karta hai.
                * **`while` loop:** Condition-based indefinite execution ke liye use hota hai. Jab tak condition truthy rehti hai loop chalta hai.
                * **`range(start, stop, step)`:** Memory efficient generator sequence banata hai bina poori list memory mein allocate kiye.
                """)
                st.code("""# For loop traversing with step decrement
print("Countdown Sequence:")
for i in range(10, 0, -2):
    print(i, end=" -> ")
print("LIFT OFF")

# While loop with accumulator logic
acc = 1
val = 5
while val > 0:
    acc *= val
    val -= 1
print("Factorial computed via while:", acc)""", language="python")

            with st.expander("3. Loop Control Statements (break, continue, pass, for-else construct)", expanded=False):
                st.write("""
                * **`break`:** Loop ko immediately terminate kar deta hai aur control loop ke bahar transfer karta hai.
                * **`continue`:** Current round ko chhod deta hai aur agle iteration par jump karta hai.
                * **`pass`:** No-operation statement (Syntactic requirement poori karne ke liye).
                * **`for-else` / `while-else` (Important BCA Viva Concept):** Loop ka `else` block tabhi run hota hai jab loop normal end tak pahuche, yaani beech mein koi `break` statement trigger na hua ho!
                """)
                st.code("""# Searching prime number using for-else
candidate = 29

for factor in range(2, int(candidate**0.5) + 1):
    if candidate % factor == 0:
        print(f"{candidate} is composite, divisible by {factor}")
        break
else:
    # Yeh block tabhi chalta hai jab loop bina break ke khatam ho
    print(f"{candidate} is verified PRIME NUMBER!")""", language="python")

        # ---------------- MODULE 3 ----------------
        elif selected_module == "Module 3: Functions, Scopes, Lambdas & Recursion":
            st.markdown("### 🔹 Module 3: Modular Programming")
            
            with st.expander("1. Function Architecture, Positional, Keyword, *args & **kwargs", expanded=True):
                st.write("""
                **Function Mechanics:**
                * Functions code reusability aur modular design provide karte hain.
                * **`*args` (Variable positional):** Caller ke extra positional arguments ko ek **Tuple** mein pack kar leta hai.
                * **`**kwargs` (Variable keyword):** Caller ke key-value arguments ko ek **Dictionary** mein pack kar leta hai.
                """)
                st.code("""def register_student(name, roll, *subjects, email="Not Provided", **sem_records):
    print(f"=== Student Profile: {name} (Roll: {roll}) ===")
    print(f"Primary Email: {email}")
    print("Registered Subjects:", ", ".join(subjects))
    print("Semester GPA Records:")
    for sem, gpa in sem_records.items():
        print(f"  {sem.upper()}: {gpa}")

register_student(
    "Raj Shraff", 101, 
    "Python Programming", "Computer System Architecture", "Discrete Mathematics",
    email="raj@bca.edu", 
    sem1=8.9, sem2=9.1
)""", language="python")

            with st.expander("2. Scope Resolution (LEGB Rule), global and nonlocal keywords", expanded=False):
                st.write("""
                * **LEGB Hierarchy:**
                  1. **L**ocal: Function ke body ke andar defined variables.
                  2. **E**nclosing: Outer nested function ke variables (nonlocal).
                  3. **G**lobal: Module level par defined variables.
                  4. **B**uilt-in: Python ke pre-loaded names (e.g., `len`, `range`, `print`).
                * Kisi function ke andar global variable ko re-assign karne ke liye `global var_name` declare karna anivarya hota hai.
                """)
                st.code("""univ_name = "State Technical Board"

def outer():
    campus = "Main Campus"
    
    def inner():
        nonlocal campus # Enclosing scope modify karna
        campus = "South Satellite Campus"
        global univ_name
        univ_name = "Autonomous State University"
        print("Inner modified campus:", campus)
        
    inner()
    print("Outer observed campus:", campus)

outer()
print("Global updated university:", univ_name)""", language="python")

            with st.expander("3. Lambda Expressions, map(), filter(), reduce()", expanded=False):
                st.write("""
                * **Lambda:** Inline anonymous functions jinhe bina `def` keyword ke single expression ke sath define kiya jata hai: `lambda x, y: x + y`.
                * **`map(function, iterable)`:** Iterable ke har element par function apply karta hai.
                * **`filter(function, iterable)`:** Function ke boolean output ke basis par items select karta hai.
                * **`reduce(function, iterable)`:** `functools` module ka function jo poore sequence ko single scalar value mein combine karta hai.
                """)
                st.code("""from functools import reduce

scores = [45, 88, 72, 91, 53, 62, 98]

# Filter passed students (>= 60)
passed = list(filter(lambda x: x >= 60, scores))
print("Passed Scores:", passed)

# Map: Add 5 grace marks
grace_added = list(map(lambda x: x + 5 if x < 60 else x, scores))
print("Grace Updated:", grace_added)

# Reduce: Total sum calculation
aggregate = reduce(lambda a, b: a + b, scores)
print(f"Total Aggregate Marks: {aggregate} / {len(scores)*100}")""", language="python")

            with st.expander("4. Recursion, Call Stack Mechanics & Base Cases", expanded=False):
                st.write("""
                * **Recursion:** Function jab self-reference karke khud ko call kare.
                * Har recursive call system call stack mein stack frame add karti hai.
                * **Base Case:** Stopping condition hona mandatory hai; otherwise stack overflow ho jayega aur Python `RecursionError` throw karega.
                """)
                st.code("""# Tower of Hanoi or Fibonacci via recursion
def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

print("First 8 Fibonacci numbers:")
for i in range(8):
    print(fibonacci(i), end=" ")
print()""", language="python")

        # ---------------- MODULE 4 ----------------
        elif selected_module == "Module 4: In-Depth Data Structures (Lists, Tuples, Dicts, Sets)":
            st.markdown("### 🔹 Module 4: Data Structures & Memory Layout")
            
            with st.expander("1. Lists (Memory Architecture, Slicing, List Comprehensions)", expanded=True):
                st.write("""
                **List Internal Structure:**
                * Python lists internally contiguous array of pointers hoti hain. Isliye heterogeneous elements allow karti hain.
                * **Mutable:** In-place modification allow karti hain (`append`, `extend`, `insert`, `pop`, `sort`).
                * **Slicing:** `list[start:stop:step]` (Negative indexing last element ko `-1` manti hai).
                """)
                st.code("""matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Flatten matrix using nested list comprehension
flattened = [val for row in matrix for val in row]
print("Flattened List:", flattened)

# Slicing trick: Reverse entire list
rev = flattened[::-1]
print("Reversed:", rev)""", language="python")

            with st.expander("2. Tuples (Immutability, Packing, Unpacking & Memory Efficiency)", expanded=False):
                st.write("""
                * **Tuples vs Lists:** Tuple immutable hote hain. Python tuples ko over-allocate nahi karta, isliye yeh lists ke comparison mein lightweight aur fast hote hain.
                * Dictionary keys banne ke liye tuple eligible hai (kyunki yeh hashable hota hai), jabki list nahi ban sakti.
                """)
                st.code("""# Tuple unpacking with asterisk rest collector
record = ("Raj Shraff", "BCA", 1, "Semester A", 88.5, 92.0)
name, course, sem, *academic_stats = record

print(f"Name: {name}")
print(f"Degree: {course} (Sem {sem})")
print(f"Remaining Academic Stats collected in list: {academic_stats}")""", language="python")

            with st.expander("3. Dictionaries (Hash Maps, Collision Resolution, Dict Comprehensions)", expanded=False):
                st.write("""
                * **Dictionary Architecture:** Key-value mapping jo hash table par based hoti hai. Average lookup time $O(1)$ rehta hai.
                * Keys compulsory immutable (string, int, tuple) aur hashable honi chahiye.
                * Methods: `.get(key, default)`, `.setdefault()`, `.update()`, `.items()`.
                """)
                st.code("""student_records = {
    "101": {"name": "Raj", "sub": "Python", "marks": 94},
    "102": {"name": "Aman", "sub": "CSA", "marks": 78},
    "103": {"name": "Pooja", "sub": "Python", "marks": 89}
}

# Dict Comprehension: Filter students scoring >= 80
high_scorers = {k: v["name"] for k, v in student_records.items() if v["marks"] >= 80}
print("Distinction Holders:", high_scorers)""", language="python")

            with st.expander("4. Sets (Hashing, Set Theory Operations)", expanded=False):
                st.write("""
                * **Set Characteristics:** Unordered collection jo sirf unique elements rakhta hai (duplicates automatic discard hote hain).
                * Sets mutable hote hain par unke andar store hone wale elements immutable hone chahiye.
                * Operations: Union (`|`), Intersection (`&`), Difference (`-`), Symmetric Difference (`^`).
                """)
                st.code("""python_students = {"Raj", "Aman", "Rohan", "Khushi"}
c_students = {"Aman", "Khushi", "Vikram", "Neha"}

print("Enrolled in both (Intersection):", python_students & c_students)
print("Only in Python (Difference):", python_students - c_students)
print("All unique students (Union):", python_students | c_students)""", language="python")

        # ---------------- MODULE 5 ----------------
        elif selected_module == "Module 5: Object-Oriented Programming (OOP Architecture)":
            st.markdown("### 🔹 Module 5: Object-Oriented Programming Architecture")
            
            with st.expander("1. Classes, Objects, __init__ Constructor & self Keyword", expanded=True):
                st.write("""
                **OOP Core Principles:**
                * **Class:** Logical blueprint ya user-defined data type.
                * **Object:** Physical manifestation (instance) jo heap memory allocate karti hai.
                * **`__init__()`:** Magic constructor jo object instantiation ke waqt attributes bind karta hai.
                * **`self`:** Explicit parameter jo current calling instance ki memory ko point karta hai.
                """)
                st.code("""class BCAStudent:
    # Class Variable (Shared across all instances)
    institution = "UP Board Affiliated University"

    def __init__(self, name, roll_no, stream):
        # Instance Variables (Unique to each object)
        self.name = name
        self.roll_no = roll_no
        self.stream = stream

    def get_summary(self):
        return f"[{self.roll_no}] {self.name} | Stream: {self.stream} | College: {BCAStudent.institution}"

student1 = BCAStudent("Raj Shraff", 101, "Computer Applications")
print(student1.get_summary())""", language="python")

            with st.expander("2. Encapsulation, Data Hiding & Access Specifiers", expanded=False):
                st.write("""
                * **Public Attributes:** Har jagah se accessible (`self.var`).
                * **Protected Attributes:** Single underscore convention (`self._var`) jo subclassing ke liye suggest hota hai.
                * **Private Attributes:** Double underscore (`self.__var`) jo **Name Mangling** apply karta hai (`_ClassName__var`).
                """)
                st.code("""class SecureAccount:
    def __init__(self, owner, starting_balance):
        self.owner = owner
        self.__balance = starting_balance # Private data

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return True
        return False

    def check_balance(self):
        return f"Current Balance: INR {self.__balance:.2f}"

acc = SecureAccount("Raj", 15000)
acc.deposit(2500)
print(acc.check_balance())
# print(acc.__balance) -> AttributeError throw karega""", language="python")

            with st.expander("3. Types of Inheritance (Single, Multiple, Multilevel, MRO & super())", expanded=False):
                st.write("""
                * **Types:**
                  1. Single: Child -> Parent
                  2. Multilevel: Child -> Parent -> Grandparent
                  3. Multiple: Child -> ParentA, ParentB (Diamond Problem resolve hota hai **Method Resolution Order - MRO** se).
                * **`super()`:** Parent class ke constructors aur overridden methods ko elegantly execute karta hai.
                """)
                st.code("""class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class TechnicalSpecialist:
    def __init__(self, stack):
        self.stack = stack

# Multiple Inheritance
class DeveloperStudent(Person, TechnicalSpecialist):
    def __init__(self, name, age, stack, roll):
        Person.__init__(self, name, age)
        TechnicalSpecialist.__init__(self, stack)
        self.roll = roll

    def display(self):
        return f"{self.name} (Roll: {self.roll}) | Stack: {self.stack}"

dev = DeveloperStudent("Raj", 25, "Python & C", 101)
print(dev.display())
print("Method Resolution Order (MRO):", DeveloperStudent.__mro__)""", language="python")

            with st.expander("4. Polymorphism, Method Overriding & Dunder / Magic Methods", expanded=False):
                st.write("""
                * **Polymorphism:** Same interface, different behavior.
                * **Method Overriding:** Child class parent ke method signature ko retain karke implementation badalti hai.
                * **Dunder Methods (Double Underscore):** Operator overloading aur custom string representations (`__str__`, `__repr__`, `__len__`, `__add__`).
                """)
                st.code("""class CourseCurriculum:
    def __init__(self, title, total_lectures):
        self.title = title
        self.total_lectures = total_lectures

    def __str__(self):
        return f"Curriculum Module: '{self.title}'"

    def __len__(self):
        return self.total_lectures

    def __add__(self, other):
        return self.total_lectures + other.total_lectures

c1 = CourseCurriculum("Python Programming", 45)
c2 = CourseCurriculum("Computer Architecture", 40)

print(str(c1))
print("Lectures in c1:", len(c1))
print("Combined Lectures for Semester:", c1 + c2)""", language="python")

        # ---------------- MODULE 6 ----------------
        elif selected_module == "Module 6: File Handling, Context Managers & JSON/CSV":
            st.markdown("### 🔹 Module 6: Persistence & Serialization")
            
            with st.expander("1. File Modes, seek(), tell() & with context manager", expanded=True):
                st.write("""
                **File Mechanics:**
                * **Modes:** `'r'` (read), `'w'` (truncate write), `'a'` (append), `'r+'` (read/write), `'b'` (binary format).
                * **`with open()`:** Context manager jo internally `__enter__()` aur `__exit__()` use karke file handles ko automatically clean aur close karta hai.
                * **`tell()`:** Current file pointer cursor position return karta hai.
                * **`seek(offset, whence)`:** File pointer position ko modify karta hai.
                """)
                st.code("""# Demonstration of File Cursor Navigation
filename = "bca_demo.txt"

with open(filename, "w+") as f:
    f.write("BCA Semester 1 - Python Master Notes\\nUniversity Core Prep.")
    print("Cursor after write:", f.tell())
    
    # Cursor ko start par reset karein
    f.seek(0)
    print("Cursor reset to:", f.tell())
    first_line = f.readline()
    print("Read Line:", first_line.strip())""", language="python")

            with st.expander("2. JSON Serialization & Deserialization (json module)", expanded=False):
                st.write("""
                * **Serialization (Encoding):** Python objects ko JSON string (`json.dumps()`) ya file stream (`json.dump()`) mein convert karna.
                * **Deserialization (Decoding):** JSON string (`json.loads()`) ya file stream (`json.load()`) ko native Python dictionaries mein convert karna.
                """)
                st.code("""import json

student_payload = {
    "roll_no": 101,
    "name": "Raj Shraff",
    "verified": True,
    "courses": ["Python", "DSA", "Maths"],
    "score": 92.5
}

# Serialize to JSON string
json_data = json.dumps(student_payload, indent=2)
print("Serialized JSON format:\\n", json_data)

# Deserialize back to Python dict
parsed = json.loads(json_data)
print("Extracted Name:", parsed["name"])
print("Verified Status:", parsed["verified"])""", language="python")

        # ---------------- MODULE 7 ----------------
        elif selected_module == "Module 7: Exception Handling & Custom Errors":
            st.markdown("### 🔹 Module 7: Error Resilience & Exceptions")
            
            with st.expander("1. Complete try-except-else-finally Architecture", expanded=True):
                st.write("""
                **Exception Pipeline:**
                * **`try`:** Is block ke andar risky operations rakhe jate hain jahan runtime error aane ka khatra ho.
                * **`except ExceptionType`:** Matching error ko catch karke handle karta hai bina program crash kiye.
                * **`else`:** Tabhi run hota hai jab try block bina kisi exception ke smoothly complete ho.
                * **`finally`:** Chahe error aaye ya na aaye, cleanup tasks (jaise database/file close karna) ke liye guaranteed execute hota hai.
                """)
                st.code("""def safe_divide(numerator, denominator):
    try:
        result = numerator / denominator
    except ZeroDivisionError as zde:
        print(f"Error Caught: Division by zero is undefined! ({zde})")
        return None
    except TypeError:
        print("Error Caught: Numeric arguments required!")
        return None
    else:
        print("Division calculated successfully without errors.")
        return result
    finally:
        print("Closing calculation pipeline.")

print("Test 1:", safe_divide(10, 2))
print("---")
print("Test 2:", safe_divide(10, 0))""", language="python")

            with st.expander("2. Raising Exceptions & Creating Custom User-Defined Exception Classes", expanded=False):
                st.write("""
                * **`raise`:** Manually logic-based exceptions trigger karne ke liye use hota hai.
                * **Custom Exceptions:** Built-in `Exception` base class ko inherit karke university-grade projects mein standard exception banaye jate hain.
                """)
                st.code("""class InvalidMarksError(Exception):
    def __init__(self, marks, message="Marks must be between 0 and 100"):
        self.marks = marks
        self.message = message
        super().__init__(f"{message} -> Got {marks}")

def record_exam_score(score):
    if score < 0 or score > 100:
        raise InvalidMarksError(score)
    return f"Score of {score}% submitted successfully."

try:
    print(record_exam_score(88))
    print(record_exam_score(115)) # Invalid
except InvalidMarksError as err:
    print("Custom Validation Caught:", err)""", language="python")

        # ---------------- MODULE 8 ----------------
        elif selected_module == "Module 8: Standard Libraries, Regex & Date-Time":
            st.markdown("### 🔹 Module 8: Batteries-Included Standard Libraries")
            
            with st.expander("1. Standard Modules (math, random, datetime, sys, os)", expanded=True):
                st.write("""
                * **`math`:** Mathematical operations, trigonometrics, square root, logarithms.
                * **`random`:** Pseudo-random number generation, shuffling sequences.
                * **`datetime`:** Date parsing, timestamp formatting, arithmetic with dates.
                """)
                st.code("""import math
import random
from datetime import datetime, timedelta

# Math
print("Hypotenuse (3, 4):", math.hypot(3, 4)) # 5.0
print("Factorial (6):", math.factorial(6))     # 720

# Random
lottery = ["Raj", "Aman", "Rohan", "Pooja"]
print("Random Winner:", random.choice(lottery))

# Datetime
now = datetime.now()
print("Current Formatted Date:", now.strftime("%A, %d %B %Y - %I:%M %p"))
future = now + timedelta(days=45)
print("Semester Exam Starts in 45 Days on:", future.strftime("%d-%b-%Y"))""", language="python")

            with st.expander("2. Regular Expressions (re module pattern matching)", expanded=False):
                st.write("""
                **Regex Syntactical Components:**
                * `re.search()`: String ke kisi bhi hisse mein pehla match dhundhta hai.
                * `re.findall()`: Saare matching patterns ki list deta hai.
                * `re.sub()`: Matched patterns ko replace karta hai.
                * `\d` (digit), `\w` (word character), `+` (1 ya zyada), `*` (0 ya zyada), `^` (start), `$` (end).
                """)
                st.code("""import re

document = \"\"\"
Candidate: Raj Shraff (Roll: 101)
Email: raj.shraff@university.ac.in
Phone: +91-9876543210
Secondary Contact: helpdesk@bca-portal.org
\"\"\"

# Extracting all emails
email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
emails_found = re.findall(email_regex, document)
print("Extracted Valid Emails:", emails_found)

# Phone number pattern verification
phone_match = re.search(r'\+91-\d{10}', document)
if phone_match:
    print("Verified Indian Phone Number:", phone_match.group())""", language="python")

        # Bottom AI Action Container (60s Timeout Protected)
        st.markdown("""
        <div class="apple-glass-card">
            <h3 style="margin-top:0; font-size:20px; font-weight:700;">🎯 AI University Exam Preparation & Viva Master</h3>
            <p style="color:#94A3B8; font-size:13px; margin-bottom:14px;">Selected module ke expected university exam questions aur viva points generate karein:</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔥 Generate Most Important Exam Questions & Viva Points", use_container_width=True):
            with st.spinner("AI Professor analyzing syllabus & trends..."):
                prompt = f"""
                You are a senior BCA university examiner.
                For the module: '{selected_module}':
                1. Provide the top 3 high-weightage theory examination questions (5-10 marks format).
                2. Provide 2 tricky Viva-Voce questions with short, precise 1-line answers.
                3. Highlight 1 critical practical coding pitfall/mistake students usually make in university lab exams.
                Keep language clear, concise, and formatted with clean bullet points.
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
                        1. Score out of 10.
                        2. Remarks: strengths and mistakes.
                        3. Correct model answer.
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
                Provide a complete, well-commented, professional Python starter project for: '{proj}'.
                Include OOP classes, error checks, and interactive menu loop.
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
