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

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(20, 24, 40, 0.95), rgba(10, 12, 22, 1));
        color: #E2E8F0;
    }
    [data-testid="stSidebar"] {
        background: rgba(15, 18, 30, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(16px);
    }
    .hero-banner {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.25) 0%, rgba(147, 51, 234, 0.25) 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 22px 26px;
        border-radius: 16px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        margin-bottom: 22px;
    }
    .hero-title {
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(90deg, #60A5FA, #C084FC, #F472B6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }
    .hero-sub {
        font-size: 14px;
        color: #94A3B8;
    }
    .ai-box {
        background: rgba(15, 23, 42, 0.85);
        border-left: 4px solid #8B5CF6;
        border-radius: 0 10px 10px 0;
        padding: 18px;
        margin-top: 14px;
        color: #F8FAFC;
    }
    .stButton>button {
        background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 9px 22px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 4px 14px 0 rgba(124, 58, 237, 0.35) !important;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 18px 0 rgba(37, 99, 235, 0.5) !important;
    }
    .badge-status {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
        <span style="font-size: 26px;">⚡</span>
        <div>
            <h3 style="margin: 0; font-size: 19px; font-weight: 800; color: #F8FAFC;">BCA Python AI</h3>
            <span style="font-size: 11px; color: #94A3B8; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">Autonomous Portal</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    gemini_key = None
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
            "📖 Syllabus & Detailed Prep",
            "📝 AI Smart Exam Engine",
            "🛠️ Guided Projects Lab",
            "🤖 24/7 AI Code Mentor",
            "🧪 Live Code Runner"
        ]
    )
    st.markdown("---")
    st.caption("BCA University Core Curriculum • Powered by Gemini 3.8 Flash")

# Helper function
def get_ai_response(prompt):
    if not gemini_key:
        return "⚠️ Pehle Gemini API Key configure karein."
    try:
        model = genai.GenerativeModel("models/gemini-3.8-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        err_msg = str(e)
        if "429" in err_msg:
            return "⏳ **Free Tier Rate Limit (429):** Request limit exceed ho gayi hai. Kripya 30-40 seconds wait karein aur fir click karein."
        return f"AI Error: {err_msg}"

# ================= 1. SYLLABUS & DETAILED PREP =================
if menu == "📖 Syllabus & Detailed Prep":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Academic Curriculum & In-Depth Notes</div>
        <div class="hero-sub">Har topic ka detailed explanation simple language mein, dedicated live code ke saath. Niche exam tools available hain.</div>
    </div>
    """, unsafe_allow_html=True)

    selected_unit = st.selectbox(
        "Select Unit to Study:",
        [
            "Unit 1: Fundamentals, Control Flow & Loops",
            "Unit 2: Data Structures (Lists, Tuples, Dictionaries, Sets)",
            "Unit 3: Object-Oriented Programming (OOP)",
            "Unit 4: File Handling & Exception Handling"
        ]
    )

    # DETAILED CURRICULUM WITH FULL TOPIC EXPLANATIONS & CODES
    if selected_unit == "Unit 1: Fundamentals, Control Flow & Loops":
        st.markdown("### 📚 Unit 1: Complete Study Topics")
        
        with st.expander("🔹 Topic 1: Dynamic Typing & Variables in Python", expanded=True):
            st.write("""
            **Explanation:**  
            C language ki tarah Python mein variable ka data type pehle se declare nahi karna padta (`int a = 10;` nahi likhna hota). Python run-time par automatically samajh jata hai ki variable kis type ka data store kar raha hai. Isiko **Dynamic Typing** kehte hain.
            """)
            st.code("""# Dynamic Typing Example
x = 10         # integer
print(type(x))

x = "Raj"      # same variable ab string ban gaya
print(type(x))""", language="python")

        with st.expander("🔹 Topic 2: Conditional Statements (if-elif-else)", expanded=True):
            st.write("""
            **Explanation:**  
            Jab program mein condition ke aadhar par decision lena ho tab `if`, `elif`, aur `else` ka use hota hai. Python mein curly braces `{}` ki jagah **Indentation (spaces)** ka use hota hai block define karne ke liye.
            """)
            st.code("""# Check Even, Odd ya Zero
num = int(input("Enter number: ") if False else 14)

if num == 0:
    print("Number is Zero")
elif num % 2 == 0:
    print(f"{num} is an Even Number")
else:
    print(f"{num} is an Odd Number")""", language="python")

        with st.expander("🔹 Topic 3: Loops in Python (for, while, range)", expanded=True):
            st.write("""
            **Explanation:**  
            * **for loop:** Sequence (list, string, range) par iterate karne ke liye use hota hai.
            * **while loop:** Jab tak di gayi condition `True` rehti hai tab tak execute hota hai.
            * **range(start, stop, step):** Numbers ki sequence generate karta hai.
            """)
            st.code("""# For Loop with range (Print 1 to 5)
print("For loop output:")
for i in range(1, 6):
    print(i, end=" ")

print("\\nWhile loop output:")
count = 3
while count > 0:
    print("Countdown:", count)
    count -= 1""", language="python")

        with st.expander("🔹 Topic 4: Loop Control (break, continue, pass)", expanded=True):
            st.write("""
            **Explanation:**  
            * **break:** Loop ko turant terminate (bahar) kar deta hai.
            * **continue:** Current iteration ko skip karke next round par chala jata hai.
            * **pass:** Null statement hota hai; jab syntactic requirement ho par code baad mein likhna ho.
            """)
            st.code("""for n in range(1, 10):
    if n == 3:
        continue # 3 ko skip karega
    if n == 7:
        break    # 7 par aate hi loop band
    print(n, end=" ")
# Output: 1 2 4 5 6""", language="python")

    elif selected_unit == "Unit 2: Data Structures (Lists, Tuples, Dictionaries, Sets)":
        st.markdown("### 📚 Unit 2: Complete Study Topics")

        with st.expander("🔹 Topic 1: Lists & List Comprehension", expanded=True):
            st.write("""
            **Explanation:**  
            List Python ka sabse popular data structure hai. Yeh **Ordered**, **Mutable (changeable)** aur duplicate elements allow karta hai. **List Comprehension** ek concise tarika hai list banane ka single line mein.
            """)
            st.code("""# List Operations & List Comprehension
fruits = ["Apple", "Banana", "Cherry"]
fruits.append("Mango")
print("Updated List:", fruits)

# List comprehension: 1 se 6 tak ke numbers ka square
squares = [x**2 for x in range(1, 7)]
print("Squares:", squares)""", language="python")

        with st.expander("🔹 Topic 2: Tuples (Immutable Sequence)", expanded=True):
            st.write("""
            **Explanation:**  
            Tuple bhi ordered collection hai par yeh **Immutable** hota hai, yaani ek baar banne ke baad iske elements ko change, add ya remove nahi kiya ja sakta. Yeh security aur fixed data (jaise roll number list, coordinates) ke liye ideal hai.
            """)
            st.code("""coordinates = (28.6139, 77.2090) # Delhi Lat/Long
print("Latitude:", coordinates[0])
# coordinates[0] = 30.0 -> TypeError dega (kyunki immutable hai)""", language="python")

        with st.expander("🔹 Topic 3: Dictionaries (Key-Value Pairs)", expanded=True):
            st.write("""
            **Explanation:**  
            Dictionary data ko `Key: Value` format mein store karti hai. Keys unique honi chahiye aur fast lookup provide karti hain. BCA exam ke viva mein hashing aur dict lookup time ($O(1)$) aksar pucha jata hai.
            """)
            st.code("""student = {
    "roll_no": 101,
    "name": "Raj Shraff",
    "course": "BCA",
    "subjects": ["Python", "CSA", "Maths"]
}
print("Student Name:", student["name"])
student["sem"] = 1 # Nayi key add karna
print("Complete Profile:", student)""", language="python")

        with st.expander("🔹 Topic 4: Sets (Unique Unordered Elements)", expanded=True):
            st.write("""
            **Explanation:**  
            Set ek unordered collection hai jo **sirf unique values** store karta hai (duplicates automatically remove ho jate hain). Isme Union, Intersection, aur Difference jaise mathematical operations easily hote hain.
            """)
            st.code("""set_a = {1, 2, 3, 4}
set_b = {3, 4, 5, 6}

print("Union (A | B):", set_a | set_b)
print("Intersection (A & B):", set_a & set_b)""", language="python")

    elif selected_unit == "Unit 3: Object-Oriented Programming (OOP)":
        st.markdown("### 📚 Unit 3: Complete Study Topics")

        with st.expander("🔹 Topic 1: Classes, Objects & __init__ Constructor", expanded=True):
            st.write("""
            **Explanation:**  
            * **Class:** Blueprint ya template hota hai.
            * **Object:** Class ka real-world instance hota hai.
            * **`__init__`:** Constructor method hota hai jo object bante hi automatically execute ho jata hai.
            * **`self`:** Current object instance ko refer karta hai.
            """)
            st.code("""class Student:
    def __init__(self, name, roll_no):
        self.name = name
        self.roll_no = roll_no

    def display(self):
        print(f"Name: {self.name}, Roll No: {self.roll_no}")

s1 = Student("Aman", 101)
s1.display()""", language="python")

        with st.expander("🔹 Topic 2: Inheritance & Method Overriding", expanded=True):
            st.write("""
            **Explanation:**  
            * **Inheritance:** Jab child class parent class ke properties aur methods ko inherit karti hai, code reusability badhti hai.
            * **Method Overriding:** Child class parent class ke kisi method ko apna naya implementation deti hai.
            """)
            st.code("""class Person:
    def role(self):
        return "I am a general person"

class BCAStudent(Person):
    def role(self): # Overriding
        return "I am a BCA Student learning Python"

obj = BCAStudent()
print(obj.role())""", language="python")

    elif selected_unit == "Unit 4: File Handling & Exception Handling":
        st.markdown("### 📚 Unit 4: Complete Study Topics")

        with st.expander("🔹 Topic 1: File Operations (Read, Write, Append)", expanded=True):
            st.write("""
            **Explanation:**  
            Python mein `open()` function se files handle hoti hain. Modes: `'r'` (read), `'w'` (write/overwrite), `'a'` (append). `with` statement use karne se file automatically close ho jati hai.
            """)
            st.code("""# Writing and reading file safely
with open("notes.txt", "w") as f:
    f.write("BCA Semester 1 Python Notes\\nImportant for Practical.")

with open("notes.txt", "r") as f:
    content = f.read()
    print("File Content:\\n", content)""", language="python")

        with st.expander("🔹 Topic 2: Exception Handling (try, except, finally)", expanded=True):
            st.write("""
            **Explanation:**  
            Program crash hone se bachane ke liye errors ko handle kiya jata hai:
            * **`try`:** Isme risky code likha jata hai jahan error aane ka chance ho.
            * **`except`:** Error aane par ye block execute hota hai.
            * **`finally`:** Chahe error aaye ya na aaye, ye block humesha execute hota hai (cleanup ke liye).
            """)
            st.code("""try:
    a = 10
    b = 0
    res = a / b
except ZeroDivisionError:
    print("Cannot divide a number by zero!")
finally:
    print("Execution complete (Finally block).")""", language="python")

    # ================= BOTTOM FIXED: AI EXAM PREPARATION ASSISTANT =================
    st.markdown("---")
    st.markdown("### 🎯 AI University Exam Preparation & Viva Master")
    st.caption("Pura unit padhne ke baad University level theory questions aur external viva questions generate karein:")

    with st.container(border=True):
        if st.button("🔥 Generate Most Important Exam Questions & Viva Points", use_container_width=True):
            with st.spinner("AI Professor syllabus analyze karke questions draft kar raha hai..."):
                prompt = f"""
                You are a senior computer science examiner for BCA university exams.
                For the unit: '{selected_unit}':
                1. Provide the top 3 high-weightage theory examination questions (5-10 marks format).
                2. Provide 2 tricky Viva-Voce questions with short, precise 1-line answers.
                3. Highlight 1 critical practical coding pitfall/mistake students usually make.
                Keep language simple, direct, and formatted cleanly with bolding and bullet points.
                """
                ai_output = get_ai_response(prompt)
                st.markdown(f'<div class="ai-box">{ai_output}</div>', unsafe_allow_html=True)

# ================= 2. AI SMART EXAM ENGINE =================
elif menu == "📝 AI Smart Exam Engine":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Automated Exam & Evaluation Suite</div>
        <div class="hero-sub">Generate unique semester exam papers on the fly and get instant grading with line-by-line feedback.</div>
    </div>
    """, unsafe_allow_html=True)

    t_unit = st.selectbox("Exam Module:", [
        "Unit 1: Fundamentals, Control Flow & Loops",
        "Unit 2: Collections & Data Structures",
        "Unit 3: Object-Oriented Programming (OOP)",
        "Unit 4: File I/O & Exception Handling"
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
        with st.container(border=True):
            st.markdown("#### 📄 Current Question Paper")
            st.markdown(st.session_state.current_test)

        st.markdown("#### ✍️ Write & Submit Answers")
        user_sol = st.text_area("Yahan apne answers aur codes type karein:", height=200, placeholder="Q1: ...\nQ2: ...\nQ3 (Code): ...")
        if st.button("🚀 Submit Sheet For AI Checking", use_container_width=True):
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

    with st.container(border=True):
        st.markdown(f"#### 🏗️ Architecture & Phases: {proj}")
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

    st.markdown("#### ⚡ AI Project Architect")
    if st.button("🚀 Get Starter Architecture & Complete Code", use_container_width=True):
        with st.spinner("AI Architect designing codebase..."):
            blueprint_prompt = f"""
            You are a Senior Project Guide for BCA students.
            Provide a complete, well-commented, professional Python starter project for: '{proj}'.
            Include OOP classes, error checks, and interactive menu loop.
            """
            st.markdown(f'<div class="ai-box">{get_ai_response(blueprint_prompt)}</div>', unsafe_allow_html=True)

# ================= 4. 24/7 AI CODE MENTOR =================
elif menu == "🤖 24/7 AI Code Mentor":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">24/7 BCA Technical Mentor</div>
        <div class="hero-sub">Resolve coding doubts, syntax comparisons with C language, or logic errors in seconds.</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        user_q = st.text_area("Poochhein apna doubt ya code paste karein:", height=140, placeholder="e.g. C language ke Pointers ka alternative Python mein kya hota hai?")
        if st.button("⚡ Ask AI Mentor", use_container_width=True):
            if not user_q.strip():
                st.warning("Pehle sawal likhein.")
            else:
                with st.spinner("AI Mentor is analyzing..."):
                    ans = get_ai_response(f"You are a BCA Computer Science professor. Answer clearly with clean code examples:\n\n{user_q}")
                    st.markdown(f'<div class="ai-box">{ans}</div>', unsafe_allow_html=True)

# ================= 5. LIVE CODE RUNNER =================
elif menu == "🧪 Live Code Runner":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Integrated Python Sandbox</div>
        <div class="hero-sub">Write, test, and execute Python code with console output directly in your browser.</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        starter = """# BCA Python Interactive Sandbox
def greet(name, sem):
    return f"Hello {name}, Welcome to BCA Semester {sem}!"

msg = greet("Raj", 1)
print(msg)
"""
        code_input = st.text_area("Code Editor:", value=starter, height=200)
        
        run_btn = st.button("▶ Run Script", use_container_width=True)
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

        st.download_button(
            label="💾 Download Code (.py)",
            data=code_input,
            file_name="bca_code.py",
            mime="text/plain",
            use_container_width=True
        )
