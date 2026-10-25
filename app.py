import streamlit as st
import google.generativeai as genai
import io
import contextlib

st.set_page_config(
    page_title="BCA AI Python Pro Mentor",
    page_icon="🎓",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .main-heading { font-size: 26px; font-weight: bold; color: #1565C0; }
    .stButton>button { border-radius: 8px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Sidebar Setup
st.sidebar.title("🎓 BCA Python AI Hub")
st.sidebar.caption("Curriculum • Smart Tests • Real Projects • Gemini AI")

# API Key Handling (Sidebar)
with st.sidebar.expander("🔑 Gemini AI Setup", expanded=True):
    gemini_key = st.text_input("Gemini API Key daalein:", type="password", help="aistudio.google.com se free key milti hai")
    if gemini_key:
        genai.configure(api_key=gemini_key)
        st.success("Gemini Connected!")
    else:
        st.info("AI features ke liye API Key zaroori hai.")

menu = st.sidebar.radio(
    "Navigation Menu",
    [
        "📖 Unit Modules & AI Prep",
        "📝 Automated Unit Test Engine",
        "🛠️ BCA Guided Projects Lab",
        "🤖 24/7 AI Code Mentor",
        "🧪 Live Code Runner"
    ]
)

# Helper function for Gemini calls
def get_ai_response(prompt):
    if not gemini_key:
        return "⚠️ Pehle sidebar mein apni Gemini API Key paste karein."
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {e}"

# ================= 1. UNIT MODULES & AI PREP =================
if menu == "📖 Unit Modules & AI Prep":
    st.markdown('<div class="main-heading">BCA Syllabus & AI-Assisted Preparation</div>', unsafe_allow_html=True)
    st.write("Unit padhein aur unit khatam hote hi AI se University-level important questions prepare karein.")

    units_data = {
        "Unit 1: Basics, Control Flow & Loops": {
            "concepts": "Dynamic Typing, Variables, If-Else, Loops (For, While), Break & Continue, Pass statement.",
            "code": """# Pattern & Flow Control
for i in range(1, 5):
    print("*" * i)"""
        },
        "Unit 2: Data Structures (Lists, Tuples, Dicts, Sets)": {
            "concepts": "List Slicing & Methods, Tuple Immutability, Dictionary Operations, Set Operations.",
            "code": """# Student Details Dictionary
student = {"name": "Aman", "roll": 101, "marks": [80, 85, 90]}
avg = sum(student["marks"]) / len(student["marks"])
print(f"Average of {student['name']}: {avg}")"""
        },
        "Unit 3: Object-Oriented Programming (OOP)": {
            "concepts": "Classes, Objects, __init__ constructor, Self keyword, Inheritance, Method Overriding.",
            "code": """class BCAStudent:
    def __init__(self, name, roll):
        self.name = name
        self.roll = roll

    def display(self):
        return f"Roll: {self.roll}, Name: {self.name}"

s1 = BCAStudent("Raj", 101)
print(s1.display())"""
        },
        "Unit 4: File Handling & Exception Handling": {
            "concepts": "Try, Except, Finally, File modes ('r', 'w', 'a'), with open() statement.",
            "code": """try:
    with open("sample.txt", "w") as f:
        f.write("Hello BCA Python")
    print("File saved successfully.")
except Exception as e:
    print(f"Error: {e}")"""
        }
    }

    selected_unit = st.selectbox("Choose Unit to Study:", list(units_data.keys()))
    current = units_data[selected_unit]

    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Core Topics Included")
        st.write(current["concepts"])
        st.markdown("#### Standard Practical Code")
        st.code(current["code"], language="python")

    with col2:
        st.subheader("🎯 AI Exam Preparation")
        st.write("Is unit ke most expected University long/short questions aur viva points generate karein:")
        if st.button("🔥 Generate Most Important Exam Questions"):
            with st.spinner("Gemini questions generate kar raha hai..."):
                prompt = f"""
                You are a senior BCA university computer science professor.
                For this syllabus unit: '{selected_unit}' with topics '{current['concepts']}':
                1. Provide the top 3 high-weightage theory exam questions asked in semester exams.
                2. Provide 2 common external viva questions with sharp, 1-line answers.
                3. Highlight 1 critical coding mistake students usually make in this unit.
                Keep language simple, direct, and focused on Indian university BCA exams.
                """
                ai_output = get_ai_response(prompt)
                st.markdown(ai_output)

# ================= 2. AUTOMATED UNIT TEST ENGINE =================
elif menu == "📝 Automated Unit Test Engine":
    st.markdown('<div class="main-heading">📝 AI Smart Unit Exam & Evaluation</div>', unsafe_allow_html=True)
    st.write("Unit select karein, naya test generate karein, aur apna answer check karwayein.")

    test_unit = st.selectbox("Kaunse Unit ka test dena hai?", [
        "Unit 1: Fundamentals & Loops",
        "Unit 2: Lists, Dictionaries & Sets",
        "Unit 3: Object-Oriented Programming (OOP)",
        "Unit 4: File Handling & Exceptions"
    ])

    if st.button("⚡ Generate New Test Paper"):
        with st.spinner("Gemini test paper bana raha hai..."):
            prompt = f"""
            Create a mini-test for BCA Semester students on '{test_unit}'.
            Include:
            1. Two 2-mark conceptual questions.
            2. One 5-mark coding question.
            Do not provide answers immediately.
            """
            st.session_state.current_test = get_ai_response(prompt)

    if "current_test" in st.session_state:
        st.markdown("### 📋 Question Paper")
        st.markdown(st.session_state.current_test)

        st.markdown("---")
        st.subheader("Apna Solution Submit Karein")
        student_ans = st.text_area("Yahan apna complete answer aur code likhein:", height=200)

        if st.button("Submit for AI Checking & Marks"):
            if not student_ans.strip():
                st.warning("Pehle answer box mein kuch likhein.")
            else:
                with st.spinner("Examiner AI paper check kar raha hai..."):
                    eval_prompt = f"""
                    You are evaluating a BCA student's exam sheet.
                    Question Paper:
                    {st.session_state.current_test}

                    Student Answer:
                    {student_ans}

                    Evaluate strictly and provide:
                    1. Score out of 10.
                    2. Line-by-line feedback on what was correct and what was missing.
                    3. The corrected version of their code if there were mistakes.
                    """
                    result = get_ai_response(eval_prompt)
                    st.markdown("### 📊 Test Evaluation & Scorecard")
                    st.markdown(result)

# ================= 3. GUIDED PROJECTS LAB =================
elif menu == "🛠️ BCA Guided Projects Lab":
    st.markdown('<div class="main-heading">🛠️ Semester End Guided Project Lab</div>', unsafe_allow_html=True)
    st.write("Real-world BCA submission projects banayein step-by-step guidance ke saath.")

    project = st.selectbox(
        "Choose Project:",
        [
            "Project 1: Student Management System (Console + File/SQLite)",
            "Project 2: Bank Account / ATM Simulator (OOPs Based)",
            "Project 3: Pharmacy / Supermarket Billing App"
        ]
    )

    st.info(f"Active Project: **{project}**")
    
    col_p1, col_p2 = st.columns([1, 1])
    with col_p1:
        st.markdown("#### Project Roadmap")
        if project == "Project 1: Student Management System (Console + File/SQLite)":
            st.markdown("""
            - **Phase 1:** Add, View, and Delete students.
            - **Phase 2:** Save data inside a file or SQLite database.
            - **Phase 3:** Calculate Grade and CGPA automatically.
            - **Phase 4:** Search by Roll Number.
            """)
        elif project == "Project 2: Bank Account / ATM Simulator (OOPs Based)":
            st.markdown("""
            - **Phase 1:** Create `Account` class with balance.
            - **Phase 2:** Methods for `deposit()`, `withdraw()`, and PIN verification.
            - **Phase 3:** Custom Exceptions for Insufficient Balance.
            """)
        elif project == "Project 3: Pharmacy / Supermarket Billing App":
            st.markdown("""
            - **Phase 1:** Item catalog using dictionary.
            - **Phase 2:** Add to cart, calculate 18% GST and total.
            - **Phase 3:** Generate printed text receipt.
            """)

    with col_p2:
        st.markdown("#### AI Project Architect")
        st.write("Project start karne ke liye starter architecture ya code review maangein:")
        if st.button("🚀 Get Full Architecture & Starter Code"):
            with st.spinner("AI project outline plan kar raha hai..."):
                prompt = f"""
                You are a practical project mentor for BCA students.
                Provide a complete, well-commented, beginner-friendly starter template in Python for: '{project}'.
                Include clear class definitions, main menu loop, and instructions on how the student can extend it for their final project submission.
                """
                st.markdown(get_ai_response(prompt))

    st.markdown("---")
    st.subheader("Project Code Review")
    user_proj_code = st.text_area("Apna project code yahan paste karke check karwayein:", height=180)
    if st.button("🔍 Review My Project Code"):
        with st.spinner("Code audit chal raha hai..."):
            prompt = f"Review this BCA student's project code for '{project}'. Check for bugs, structure, and suggest 2 features to impress the external examiner:\n\n{user_proj_code}"
            st.markdown(get_ai_response(prompt))

# ================= 4. 24/7 AI CODE MENTOR =================
elif menu == "🤖 24/7 AI Code Mentor":
    st.markdown('<div class="main-heading">🤖 Personal BCA Python Doubt Solver</div>', unsafe_allow_html=True)
    st.write("C language se comparison, syllabus doubts, ya coding errors—kuch bhi poochhein.")

    user_query = st.text_area("Apna sawal ya error yahan likhein:", placeholder="e.g. C language ke arrays aur Python lists mein difference kya hai?")
    if st.button("Poochho Gemini Se"):
        if not user_query.strip():
            st.warning("Pehle sawal likhein.")
        else:
            with st.spinner("Gemini answer ready kar raha hai..."):
                prompt = f"You are a friendly, encouraging computer science tutor helping a BCA student. Answer clearly with clean examples:\n\n{user_query}"
                st.markdown(get_ai_response(prompt))

# ================= 5. LIVE CODE RUNNER =================
elif menu == "🧪 Live Code Runner":
    st.markdown('<div class="main-heading">🧪 Python Scratchpad & Sandbox</div>', unsafe_allow_html=True)
    st.write("Code run karke direct output check karein.")

    code_to_run = st.text_area("Code Editor:", value='print("BCA Python Ready!")', height=160)
    if st.button("▶ Run Code"):
        capture = io.StringIO()
        try:
            with contextlib.redirect_stdout(capture):
                exec(code_to_run, {})
            st.success("Execution Completed")
            st.text_area("Output:", capture.getvalue(), height=120)
        except Exception as e:
            st.error(f"Error: {e}")