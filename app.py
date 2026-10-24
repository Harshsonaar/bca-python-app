import streamlit as st
import google.generativeai as genai
import io
import contextlib

st.set_page_config(
    page_title="BCA Python Master Pro | AI Mentor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= PREMIUM MODERN UI STYLING =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Main background & Card styling */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(20, 24, 40, 0.95), rgba(10, 12, 22, 1));
        color: #E2E8F0;
    }

    /* Sidebar container */
    [data-testid="stSidebar"] {
        background: rgba(15, 18, 30, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(16px);
    }

    /* Glassmorphism Metric / Hero Card */
    .hero-banner {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.25) 0%, rgba(147, 51, 234, 0.25) 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 24px 28px;
        border-radius: 18px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        margin-bottom: 24px;
        backdrop-filter: blur(12px);
    }
    .hero-title {
        font-size: 30px;
        font-weight: 800;
        background: linear-gradient(90deg, #60A5FA, #C084FC, #F472B6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }
    .hero-sub {
        font-size: 15px;
        color: #94A3B8;
        letter-spacing: 0.3px;
    }

    /* Feature Glass Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 16px;
        transition: all 0.25s ease;
    }
    .glass-card:hover {
        border-color: rgba(96, 165, 250, 0.4);
        box-shadow: 0 8px 24px -6px rgba(37, 99, 235, 0.2);
        transform: translateY(-2px);
    }

    /* Custom AI Response Box */
    .ai-box {
        background: rgba(15, 23, 42, 0.8);
        border-left: 4px solid #8B5CF6;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 0 12px 12px 0;
        padding: 20px;
        margin: 16px 0;
    }

    /* Buttons enhancement */
    .stButton>button {
        background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 14px 0 rgba(124, 58, 237, 0.39) !important;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px 0 rgba(37, 99, 235, 0.55) !important;
    }

    /* Form & Input Fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 10px !important;
        color: #F8FAFC !important;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #60A5FA !important;
        box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.2) !important;
    }

    /* Badge indicators */
    .badge-status {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR CONFIGURATION =================
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
        <span style="font-size: 28px;">⚡</span>
        <div>
            <h3 style="margin: 0; font-size: 20px; font-weight: 800; color: #F8FAFC;">BCA Python AI</h3>
            <span style="font-size: 11px; color: #94A3B8; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">Autonomous Portal</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # API Key Handling (Secrets First)
    if "GEMINI_API_KEY" in st.secrets:
        gemini_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=gemini_key)
        st.markdown('<div class="badge-status">● AI Mentor Active</div>', unsafe_allow_html=True)
    else:
        with st.expander("🔑 Gemini Setup", expanded=True):
            gemini_key = st.text_input("API Key daalein:", type="password")
            if gemini_key:
                genai.configure(api_key=gemini_key)
                st.success("Connected!")

    st.markdown("---")
    menu = st.radio(
        "STUDY WORKFLOW",
        [
            "📖 Syllabus & AI Prep",
            "📝 AI Smart Exam Engine",
            "🛠️ Guided Projects Lab",
            "🤖 24/7 AI Code Mentor",
            "🧪 Live Code Runner"
        ]
    )
    st.markdown("---")
    st.caption("BCA University Core Curriculum • Powered by Gemini 3.8 Flash")

# Helper function with exact verified model
def get_ai_response(prompt):
    if not gemini_key:
        return "⚠️ Pehle Gemini API Key configure karein."
    try:
        model = genai.GenerativeModel("models/gemini-3.8-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {e}"

# ================= 1. SYLLABUS & AI PREP =================
if menu == "📖 Syllabus & AI Prep":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Academic Curriculum & Smart Prep</div>
        <div class="hero-sub">Unit-wise university modules with instant AI-powered exam questions and viva master tips.</div>
    </div>
    """, unsafe_allow_html=True)

    units_data = {
        "Unit 1: Fundamentals, Control Flow & Loops": {
            "desc": "Dynamic typing, Identifiers, Operators precedence, Conditional branching, for/while loops, nested loops, break/continue.",
            "code": """# Factorial & Prime check demonstration
num = 7
is_prime = True

for i in range(2, int(num**0.5) + 1):
    if num % i == 0:
        is_prime = False
        break

print(f"{num} is Prime: {is_prime}")"""
        },
        "Unit 2: Data Structures (Lists, Tuples, Dictionaries, Sets)": {
            "desc": "List comprehension, immutability of tuples, hashing in dictionaries, set union/intersection, slicing operations.",
            "code": """# List Comprehension & Student Records
marks = [72, 85, 43, 91, 65]
passed_students = [m for m in marks if m >= 50]
print("Pass list:", passed_students)

records = {"001": {"name": "Raj", "sem": 1}, "002": {"name": "Aman", "sem": 1}}
print("Student 1:", records["001"]["name"])"""
        },
        "Unit 3: Object-Oriented Programming (OOP)": {
            "desc": "Classes, Instance vs Class variables, __init__ constructor, Encapsulation, Single & Multiple Inheritance, Method overriding.",
            "code": """class BCAStudent:
    university = "UP Board / Affiliated University"

    def __init__(self, name, roll_no):
        self.name = name
        self.roll_no = roll_no

    def get_details(self):
        return f"Roll: {self.roll_no} | Student: {self.name}"

s1 = BCAStudent("Raj Shraff", 101)
print(s1.get_details())"""
        },
        "Unit 4: File Handling & Exception Handling": {
            "desc": "File modes (r, w, a, rb, wb), context manager (with open), try-except-finally blocks, Custom defined exceptions.",
            "code": """try:
    with open("university_log.txt", "w") as f:
        f.write("BCA Semester 1 - Examination Record 2026\\n")
    print("Log recorded successfully.")
except IOError as err:
    print("Disk Error:", err)"""
        }
    }

    selected_unit = st.selectbox("Select Study Module:", list(units_data.keys()))
    cur = units_data[selected_unit]

    c1, c2 = st.columns([1, 1], gap="medium")
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📌 Key Exam Concepts")
        st.write(cur["desc"])
        st.markdown("#### 💻 Standard Lab Reference Code")
        st.code(cur["code"], language="python")
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🎯 AI Exam Preparation Assistant")
        st.write("Generate University semester test paper questions & external viva questions for this unit:")
        if st.button("🔥 Generate Most Important Exam Questions"):
            with st.spinner("AI Professor analyzing syllabus & trends..."):
                prompt = f"""
                You are a senior computer science examiner for BCA students.
                For the unit: '{selected_unit}' with concepts: '{cur['desc']}':
                1. Provide the top 3 high-weightage theory examination questions.
                2. Provide 2 tricky Viva-Voce questions with short, precise answers.
                3. Highlight 1 critical coding pitfall students make in lab exams.
                Format cleanly using bolding and clear bullet points.
                """
                out = get_ai_response(prompt)
                st.markdown(f'<div class="ai-box">{out}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ================= 2. AI SMART EXAM ENGINE =================
elif menu == "📝 AI Smart Exam Engine":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Automated Exam & Evaluation Suite</div>
        <div class="hero-sub">Generate unique semester exam papers on the fly and get instant grading with line-by-line feedback.</div>
    </div>
    """, unsafe_allow_html=True)

    t_col1, t_col2 = st.columns([1, 2], gap="large")
    with t_col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📋 Exam Setup")
        t_unit = st.selectbox("Exam Module:", [
            "Unit 1: Fundamentals & Control Flow",
            "Unit 2: Collections & Data Structures",
            "Unit 3: Object-Oriented Programming (OOP)",
            "Unit 4: File I/O & Exception Handling"
        ])
        
        if st.button("⚡ Generate New Test Paper"):
            with st.spinner("Drafting fresh exam questions..."):
                test_prompt = f"""
                Create a 10-mark mini examination paper for BCA students on '{t_unit}'.
                - Question 1 (2 Marks): Conceptual definition.
                - Question 2 (3 Marks): Output prediction or short difference.
                - Question 3 (5 Marks): Real-world coding question.
                Keep questions strict and university-grade. Do NOT give solutions.
                """
                st.session_state.current_test = get_ai_response(test_prompt)
        st.markdown('</div>', unsafe_allow_html=True)

    with t_col2:
        if "current_test" in st.session_state:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 📄 Current Question Paper")
            st.markdown(st.session_state.current_test)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("#### ✍️ Write & Submit Answers")
            user_sol = st.text_area("Yahan apne answers aur codes type karein:", height=220, placeholder="Q1: ...\nQ2: ...\nQ3 (Code): ...")
            if st.button("🚀 Submit Sheet For AI Checking"):
                if not user_sol.strip():
                    st.warning("Please type your answer before submission.")
                else:
                    with st.spinner("AI Evaluator calculating score & marks..."):
                        eval_prompt = f"""
                        You are a strict BCA university examiner grading a student's answer sheet.
                        Paper:
                        {st.session_state.current_test}

                        Student Answer:
                        {user_sol}

                        Evaluate thoroughly:
                        1. Score out of 10 with clear division.
                        2. Detailed remarks: strengths and missing elements.
                        3. Perfect model answer/corrected code.
                        """
                        scorecard = get_ai_response(eval_prompt)
                        st.markdown(f'<div class="ai-box"><h3>📊 Examiner Evaluation</h3>{scorecard}</div>', unsafe_allow_html=True)

# ================= 3. GUIDED PROJECTS LAB =================
elif menu == "🛠️ Guided Projects Lab":
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
            "Supermarket Inventory & Automated Billing Engine"
        ]
    )

    p1, p2 = st.columns([1, 1], gap="medium")
    with p1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"#### 🏗️ Architecture: {proj}")
        if "Student" in proj:
            st.markdown("""
            * **Phase 1:** Data Modeling (Student records with Roll, Name, Marks).
            * **Phase 2:** CRUD Operations (Add, View, Search, Delete).
            * **Phase 3:** Persistence via File System or SQLite.
            * **Phase 4:** Grade calculation logic and report generation.
            """)
        elif "Banking" in proj:
            st.markdown("""
            * **Phase 1:** `Account` Base class with Encapsulated balance.
            * **Phase 2:** Authentication (4-digit PIN verification).
            * **Phase 3:** Transaction methods (`deposit`, `withdraw`).
            * **Phase 4:** Custom Exception handling for Overdraft/Min-balance.
            """)
        else:
            st.markdown("""
            * **Phase 1:** Product Catalog dictionary with prices and stock.
            * **Phase 2:** Interactive cart system.
            * **Phase 3:** 18% GST calculation and discount schemes.
            * **Phase 4:** Receipt formatting with timestamp.
            """)
        st.markdown('</div>', unsafe_allow_html=True)

    with p2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### ⚡ AI Project Architect")
        st.write("Generate clean starter blueprint code ready to expand for submissions:")
        if st.button("🚀 Get Starter Architecture & Code"):
            with st.spinner("AI Architect designing codebase..."):
                blueprint_prompt = f"""
                You are a Senior Project Guide for BCA students.
                Provide a complete, well-commented, professional Python starter project for: '{proj}'.
                Include OOP classes, error checks, and interactive menu loop.
                """
                st.markdown(f'<div class="ai-box">{get_ai_response(blueprint_prompt)}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ================= 4. 24/7 AI CODE MENTOR =================
elif menu == "🤖 24/7 AI Code Mentor":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">24/7 BCA Technical Mentor</div>
        <div class="hero-sub">Resolve coding doubts, syntax comparisons with C language, or logic errors in seconds.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    user_q = st.text_area("Poochhein apna doubt ya code paste karein:", height=150, placeholder="e.g. C language ke Pointers ka alternative Python mein kya hota hai?")
    if st.button("⚡ Ask AI Mentor"):
        if not user_q.strip():
            st.warning("Pehle sawal likhein.")
        else:
            with st.spinner("AI Mentor is analyzing..."):
                ans = get_ai_response(f"You are a BCA Computer Science professor. Answer clearly with clean code examples:\n\n{user_q}")
                st.markdown(f'<div class="ai-box">{ans}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ================= 5. LIVE CODE RUNNER =================
elif menu == "🧪 Live Code Runner":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Integrated Python Sandbox</div>
        <div class="hero-sub">Write, test, and execute Python code with console output directly in your browser.</div>
    </div>
    """, unsafe_allow_html=True)

    c_box, c_info = st.columns([2, 1], gap="medium")
    with c_box:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        starter = """# BCA Python Interactive Sandbox
def greet(name, sem):
    return f"Hello {name}, Welcome to BCA Semester {sem}!"

msg = greet("Raj", 1)
print(msg)
"""
        code_input = st.text_area("Code Editor:", value=starter, height=220)
        
        run_btn = st.button("▶ Run Script")
        if run_btn:
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf):
                    exec(code_input, {})
                output_str = buf.getvalue()
                st.success("Execution Successful")
                st.text_area("Console Output:", output_str if output_str else "[Program finished with no output]", height=130)
            except Exception as ex:
                st.error(f"Traceback Error: {ex}")

        st.download_button(
            label="💾 Download Code (.py)",
            data=code_input,
            file_name="bca_code.py",
            mime="text/plain"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with c_info:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 💡 Sandbox Controls")
        st.markdown("""
        * **Full Standard Library:** `math`, `random`, `re`, `datetime` support.
        * **I/O Redirection:** `print()` statements capture automatically.
        * **Download Support:** Save scripts locally for practical submissions.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
