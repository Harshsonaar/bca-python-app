import streamlit as st
import google.generativeai as genai
import io
import contextlib
import time
from PIL import Image

st.set_page_config(
    page_title="BCA OS | MLK PG College Balrampur",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session state initialization
if "selected_subject" not in st.session_state:
    st.session_state.selected_subject = "🐍 Python Programming"

if "current_note_page" not in st.session_state:
    st.session_state.current_note_page = 1

if "dynamic_pages_list" not in st.session_state:
    st.session_state.dynamic_pages_list = []

# ================= NEXT-GEN LUXURY DASHBOARD UI CSS =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Patrick+Hand&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Ambient Ultra-Dark Slate Canvas */
    .stApp {
        background: radial-gradient(circle at 20% -10%, #1e1b4b 0%, #0f172a 45%, #020617 100%);
        color: #F8FAFC;
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

    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 5rem !important;
        max-width: 1100px !important;
    }

    /* Custom Modern Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.85) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(24px) !important;
    }
    section[data-testid="stSidebar"] div.block-container {
        padding-top: 1.5rem !important;
    }

    /* Header Brand Card */
    .brand-banner {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 16px 20px;
        backdrop-filter: blur(20px);
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .brand-title {
        font-size: 20px;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 0%, #38BDF8 60%, #818CF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }

    /* ================= AUTHENTIC A4 REGISTER BINDER ================= */
    .binder-stage {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 15px 0;
        width: 100%;
    }
    .notebook-paper-a4 {
        background-color: #ffffff !important;
        background-image: 
            linear-gradient(90deg, transparent 42px, #ef4444 42px, #ef4444 43.5px, transparent 43.5px),
            linear-gradient(#e2e8f0 1px, transparent 1px) !important;
        background-size: 100% 100%, 100% 26px !important;
        border-radius: 8px !important;
        padding: 22px 24px 28px 56px !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: 0 16px 45px rgba(0, 0, 0, 0.7), 0 2px 8px rgba(0,0,0,0.15) !important;
        width: 100% !important;
        max-width: 530px !important;
        min-height: 480px !important;
        height: auto !important;
        position: relative !important;
        box-sizing: border-box !important;
        color: #1e3a8a !important;
    }

    /* Real Spiral Ring Binding */
    .notebook-paper-a4::before {
        content: '' !important;
        position: absolute !important;
        top: 16px !important;
        left: 12px !important;
        width: 12px !important;
        height: 94% !important;
        background-image: radial-gradient(circle, #94a3b8 4px, transparent 5px) !important;
        background-size: 12px 26px !important;
        background-repeat: repeat-y !important;
    }

    .notebook-title-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid #ef4444;
        padding-bottom: 4px;
        margin-bottom: 10px;
    }
    .notebook-title-text {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        color: #0f172a !important;
    }
    .notebook-badge {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        background: #ef4444 !important;
        color: #ffffff !important;
        padding: 2px 8px !important;
        border-radius: 8px !important;
    }

    .notebook-handwritten-text {
        font-family: 'Patrick Hand', cursive !important;
        font-size: 17px !important;
        line-height: 26px !important;
        color: #1e3a8a !important;
        word-break: break-word !important;
        white-space: pre-wrap !important;
    }

    /* Glass Studio Panel */
    .studio-panel {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(20px);
        box-shadow: 0 12px 36px rgba(0, 0, 0, 0.35);
        margin-top: 15px;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        padding: 8px 18px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 22px rgba(124, 58, 237, 0.45) !important;
    }

    /* Mobile Responsive */
    @media (max-width: 768px) {
        .notebook-paper-a4 {
            padding: 16px 14px 20px 46px !important;
            max-width: 95vw !important;
            min-height: 420px !important;
        }
        .notebook-handwritten-text {
            font-size: 15px !important;
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
    st.markdown("### 🏛️ BCA Academic Portal")
    st.caption("MLK PG College Balrampur • Maa Pateshwari State Univ")
    
    st.markdown("---")
    nav_option = st.radio(
        "Navigation Hub:",
        [
            "📝 Smart Register",
            "📖 Syllabus Explorer",
            "🎯 Exam Engine",
            "🔬 Projects Lab",
            "🤖 AI Mentor",
            "💻 Terminal Sandbox"
        ],
        index=0
    )
    st.markdown("---")
    
    if gemini_key:
        st.success("● AI Engine & Vision Active")
    else:
        with st.expander("🔑 API Setup", expanded=True):
            gemini_key = st.text_input("Gemini API Key:", type="password")
            if gemini_key:
                genai.configure(api_key=gemini_key)
                st.success("Connected!")
    
    st.caption("Crafted by Raj ⚡")

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
    You are a distinguished university professor for BCA curriculum at MLK PG College, Balrampur (affiliated with Maa Pateshwari State University).
    Subject: {current_subject}
    {lang_instruction}

    TEACHING RULES:
    1. Write in clean, concise student register notes.
    2. NEVER output raw markdown hashes like '###' or raw unparsed LaTeX with broken dollar signs ($0/0$). Write clean readable formulas (e.g. 0/0 form, lim (x -> a) [f'(x) / g'(x)]).
    3. DO NOT output metadata boilerplate ('Subject:', 'Author:', 'Instructor:'). Start straight with the study points.
    4. Keep content to 50-65 words per page so it fits completely without scrolling or cutting off.
    5. Separate individual pages with the exact token '[PAGE_BREAK]'.

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

# ================= TOP BRAND BANNER WITH CLEAN SUBJECT SELECTOR =================
b_col1, b_col2 = st.columns([1.8, 1.2])
with b_col1:
    st.markdown("""
    <div style="padding-top: 5px;">
        <div class="brand-title">BCA Academic OS</div>
        <div style="font-size: 12px; color: #94A3B8;">Autonomous Learning Suite • MLK PG College Balrampur</div>
    </div>
    """, unsafe_allow_html=True)
with b_col2:
    st.session_state.selected_subject = st.selectbox(
        "Current Stream:",
        [
            "🐍 Python Programming",
            "🖥️ Computer System Architecture",
            "📐 Mathematics & Numerical Methods"
        ],
        index=0,
        label_visibility="collapsed"
    )

active_subj = st.session_state.selected_subject

# ================= 1. SMART REGISTER NOTES =================
if nav_option == "📝 Smart Register":
    st.markdown(f"### 📖 Handwritten Register Notebook — {active_subj}")

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

    c1, c2 = st.columns([2.5, 1])
    with c1:
        chosen_topic = st.selectbox("Select Academic Topic:", suggested_topics)
        custom_topic = st.text_input("Or enter syllabus query:", placeholder="e.g. Master-slave JK flip-flop working")
    with c2:
        notes_lang = st.selectbox("Language Style:", ["Hinglish (Natural Notes)", "English", "Hindi (हिन्दी)"])

    final_topic = custom_topic.strip() if custom_topic.strip() else chosen_topic

    if st.button("✍️ Write on Register Pages", use_container_width=True):
        st.session_state.current_note_page = 1
        with st.spinner(f"Writing register notes for {final_topic}..."):
            raw_output = get_ai_response(
                f"Write concise register notes for '{final_topic}' in {active_subj}.",
                forced_language=notes_lang,
                current_subject=active_subj
            )

            pages = [p.strip() for p in raw_output.split("[PAGE_BREAK]") if p.strip()]
            if not pages:
                pages = [raw_output]

            clean_pages = []
            for pg in pages:
                lines = [line.replace("### ", "").replace("## ", "").replace("# ", "") for line in pg.splitlines()]
                clean_pages.append("\n".join(lines))

            st.session_state.dynamic_pages_list = clean_pages
            st.session_state.flip_notes_topic = final_topic

    # DISPLAY CLEAN A4 REGISTER SHEET
    if st.session_state.dynamic_pages_list:
        pages = st.session_state.dynamic_pages_list
        total_pages = len(pages)
        curr_pg = min(st.session_state.current_note_page, total_pages)
        page_text = pages[curr_pg - 1].replace("\n", "<br>")

        st.markdown(f"""
        <div class="binder-stage">
            <div class="notebook-paper-a4">
                <div class="notebook-title-row">
                    <span class="notebook-title-text">{st.session_state.get('flip_notes_topic')}</span>
                    <span class="notebook-badge">Sheet {curr_pg} of {total_pages}</span>
                </div>
                <div style="font-size: 11px; color: #64748b; margin-bottom: 8px;">
                    <b>Subject:</b> {active_subj} | <b>MLK PG College Balrampur</b>
                </div>
                <div class="notebook-handwritten-text">
{page_text}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # UNIFIED ROW FLIP CONTROLS
        ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1.2, 2.5, 1.2])
        with ctrl_col1:
            if st.button("‹ Prev Page", disabled=(curr_pg == 1), use_container_width=True):
                st.session_state.current_note_page = max(1, curr_pg - 1)
                st.rerun()
        with ctrl_col2:
            st.markdown(f"""
            <div style="text-align: center; color: #94A3B8; font-size: 13px; font-weight: 600; padding-top: 8px;">
                Sheet {curr_pg} of {total_pages}
            </div>
            """, unsafe_allow_html=True)
        with ctrl_col3:
            if st.button("Next Page ›", disabled=(curr_pg == total_pages), use_container_width=True):
                st.session_state.current_note_page = min(total_pages, curr_pg + 1)
                st.rerun()

# ================= 2. SYLLABUS EXPLORER =================
elif nav_option == "📖 Syllabus Explorer":
    st.markdown(f"### 📚 University Syllabus Guide — {active_subj}")
    
    if active_subj == "🐍 Python Programming":
        units = {
            "Module 1": "Language Basics, Bytecode Architecture & Operators",
            "Module 2": "Control Flow, Loops & for-else Construct",
            "Module 3": "Functions, Scopes, LEGB, Lambdas & Recursion",
            "Module 4": "Data Structures (Lists, Tuples, Sets, Dicts)",
            "Module 5": "OOP, Encapsulation, Mangling & Dunder Methods",
            "Module 6": "File Handling, seek(), tell() & JSON",
            "Module 7": "Exception Handling & Custom Errors",
            "Module 8": "Standard Libraries & Regex Patterns"
        }
    elif active_subj == "🖥️ Computer System Architecture":
        units = {
            "Unit 1": "Number Systems, Radix & 2's Complement",
            "Unit 2": "Logic Gates, Half/Full Adders & K-Maps",
            "Unit 3": "Sequential Logic, Flip-Flops & Master-Slave JK",
            "Unit 4": "Basic Computer Organization & Instruction Cycle",
            "Unit 5": "CPU Architecture, Addressing Modes & Pipelining",
            "Unit 6": "Memory Hierarchy, Cache Mapping & RAM",
            "Unit 7": "Input-Output Org, Interrupts & DMA Controller"
        }
    else:
        units = {
            "Unit 1": "Set Theory, Equivalence Relations & POSET",
            "Unit 2": "Mathematical Logic, Truth Tables & Inference",
            "Unit 3": "Matrices, Rank, Linear Equations & Cayley-Hamilton",
            "Unit 4": "Combinatorics, Pigeonhole & Graph Theory",
            "Unit 5": "Differential Calculus, Leibnitz's Theorem & Limits",
            "Unit 6": "Numerical Methods, Newton-Raphson & Bisection"
        }

    for u_key, u_title in units.items():
        with st.expander(f"{u_key}: {u_title}"):
            st.write("Complete breakdown aligned with Maa Pateshwari State University.")
            if st.button(f"✨ Deep Dive {u_key}", key=f"btn_{u_key}"):
                with st.spinner("Analyzing curriculum..."):
                    summary = get_ai_response(f"Provide complete exam summary for {u_title} under {active_subj}.", current_subject=active_subj)
                    st.info(summary)

# ================= 3. EXAM ENGINE =================
elif nav_option == "🎯 Exam Engine":
    st.markdown(f"### 🎯 Examination Generator & Evaluator — {active_subj}")

    c1, c2 = st.columns([2, 1])
    with c1:
        exam_topic = st.text_input("Examination Focus Topic:", placeholder="e.g. Cache Mapping / L'Hopital Rule / Polymorphism")
    with c2:
        exam_lang = st.selectbox("Language:", ["English", "Hinglish", "Hindi (हिन्दी)"])

    if st.button("⚡ Generate University Paper", use_container_width=True):
        with st.spinner("Drafting official question paper..."):
            prompt = f"Create a 15-mark examination test for '{exam_topic if exam_topic else 'Full Syllabus'}' in {active_subj}."
            st.session_state.exam_paper = get_ai_response(prompt, forced_language=exam_lang, current_subject=active_subj)

    if "exam_paper" in st.session_state:
        st.markdown(f"""
        <div class="studio-panel">
            <div style="font-size: 16px; font-weight: 700; color: #38BDF8; margin-bottom: 8px;">Official University Paper</div>
            {st.session_state.exam_paper}
        </div>
        """, unsafe_allow_html=True)

        user_ans = st.text_area("Your Solutions (Type here):", height=120)
        uploaded_ans = st.file_uploader("Or Upload Answer Sheet Photo (PNG/JPG):", type=["png", "jpg", "jpeg"])
        pil_img = Image.open(uploaded_ans) if uploaded_ans else None

        if st.button("🚀 Submit For AI Evaluation", use_container_width=True):
            if not user_ans.strip() and not pil_img:
                st.warning("Please type your solution or upload a photo.")
            else:
                with st.spinner("AI University Professor grading paper..."):
                    eval_res = get_ai_response("Grade this student paper out of 15 with score breakdown.", image_input=pil_img, current_subject=active_subj)
                    st.markdown(f"""
                    <div class="studio-panel" style="border-left: 4px solid #34D399;">
                        <div style="font-size: 16px; font-weight: 700; color: #34D399; margin-bottom: 6px;">Evaluator Scorecard</div>
                        {eval_res}
                    </div>
                    """, unsafe_allow_html=True)

# ================= 4. PROJECTS LAB =================
elif nav_option == "🔬 Projects Lab":
    st.markdown(f"### 🔬 Academic Capstone Projects — {active_subj}")

    if active_subj == "🐍 Python Programming":
        projs = ["Student Management Portal (SQLite)", "Banking ATM Simulator (OOP)", "Inventory Billing Engine"]
    elif active_subj == "🖥️ Computer System Architecture":
        projs = ["Half & Full Adder Simulator", "4-Bit ALU Architecture", "Direct Mapped Cache Simulator"]
    else:
        projs = ["Newton-Raphson Equation Solver", "Matrix Rank Calculator", "Graph Theory Shortest Path"]

    selected_proj = st.selectbox("Select Project Blueprint:", projs)
    if st.button("🏗️ Generate Architecture & Code", use_container_width=True):
        with st.spinner("Architecting full codebase..."):
            res = get_ai_response(f"Provide complete working code and documentation for project: '{selected_proj}' in {active_subj}.", current_subject=active_subj)
            st.markdown(f"""
            <div class="studio-panel">
                {res}
            </div>
            """, unsafe_allow_html=True)

# ================= 5. AI MENTOR =================
elif nav_option == "🤖 AI Mentor":
    st.markdown(f"### 🤖 24/7 AI Academic Mentor — {active_subj}")
    
    doubt_text = st.text_area("Type your question or error code:", height=120)
    uploaded_doubt = st.file_uploader("Or upload screenshot / question photo:", type=["png", "jpg", "jpeg"])
    doubt_img = Image.open(uploaded_doubt) if uploaded_doubt else None

    if st.button("⚡ Solve With AI", use_container_width=True):
        if not doubt_text.strip() and not doubt_img:
            st.warning("Please enter your doubt or upload an image.")
        else:
            with st.spinner("AI Mentor solving step-by-step..."):
                sol = get_ai_response(doubt_text, image_input=doubt_img, current_subject=active_subj)
                st.markdown(f"""
                <div class="studio-panel" style="border-left: 4px solid #8B5CF6;">
                    {sol}
                </div>
                """, unsafe_allow_html=True)

# ================= 6. TERMINAL SANDBOX =================
elif nav_option == "💻 Terminal Sandbox":
    st.markdown(f"### 💻 Live Python Terminal")
    
    starter_code = """# Interactive Python Sandbox
def greet(name, college):
    return f"Welcome {name} to {college} BCA Master Ecosystem!"

print(greet("Raj", "MLK PG College Balrampur"))
"""
    user_code = st.text_area("Python Editor:", value=starter_code, height=180)
    c1, c2 = st.columns([1, 1])
    with c1:
        run_code = st.button("▶ Run Script", use_container_width=True)
    with c2:
        st.download_button("💾 Export .py", data=user_code, file_name="bca_code.py", use_container_width=True)

    if run_code:
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                exec(user_code, {})
            st.success("Execution Successful")
            st.code(buf.getvalue() if buf.getvalue() else "[Program executed with no terminal output]")
        except Exception as err:
            st.error(f"Runtime Traceback: {err}")
