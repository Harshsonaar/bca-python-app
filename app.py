import streamlit as st
import google.generativeai as genai
import io
import contextlib
import time
from PIL import Image

st.set_page_config(
    page_title="BCA OS | MLK PG College Balrampur",
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

# ================= NEXT-GEN MINIMALIST LUXURY STUDIO UI CSS =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Caveat:wght@600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', -apple-system, sans-serif;
    }
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Ambient Obsidian Charcoal Canvas */
    .stApp {
        background: radial-gradient(circle at 10% 0%, #171923 0%, #0d0f17 50%, #05070a 100%);
        color: #E2E8F0;
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
        padding-top: 10px !important;
        padding-bottom: 160px !important;
        max-width: 1200px !important;
    }

    /* Top Utility Pill Header */
    .top-app-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 10px 20px;
        backdrop-filter: blur(20px);
        margin-bottom: 20px;
    }
    .app-brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .brand-icon {
        background: linear-gradient(135deg, #38BDF8, #818CF8);
        color: #0F172A;
        font-weight: 800;
        font-size: 16px;
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .brand-text {
        font-size: 15px;
        font-weight: 700;
        color: #F8FAFC;
        letter-spacing: -0.3px;
    }

    /* Tab Control Hub */
    div[data-testid="stRadio"] {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        padding: 4px 6px !important;
        border-radius: 30px !important;
        margin: 0 auto 24px auto !important;
        width: max-content !important;
        max-width: 95vw !important;
        backdrop-filter: blur(20px) !important;
    }
    div[data-testid="stRadio"] > label {display: none !important;}
    div[data-testid="stRadio"] > div {
        display: flex !important;
        flex-direction: row !important;
        gap: 6px !important;
        align-items: center !important;
    }
    div[data-testid="stRadio"] label {
        background: transparent !important;
        border-radius: 20px !important;
        padding: 6px 16px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        color: #94A3B8 !important;
        transition: all 0.2s ease !important;
        margin: 0 !important;
    }
    div[data-testid="stRadio"] label:hover {
        color: #FFFFFF !important;
        background: rgba(255, 255, 255, 0.06) !important;
    }

    /* ================= REAL HARDCOVER REGISTER WORKSPACE ================= */
    .binder-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 10px 0;
        perspective: 1200px;
    }

    .notebook-binder {
        background: #FDFBF7 !important;
        background-image: 
            linear-gradient(90deg, transparent 48px, #F87171 48px, #F87171 50px, transparent 50px),
            linear-gradient(#E2E8F0 1px, transparent 1px) !important;
        background-size: 100% 100%, 100% 26px !important;
        width: 100% !important;
        max-width: 560px !important;
        min-height: 520px !important;
        border-radius: 6px 16px 16px 6px !important;
        border: 1px solid #CBD5E1 !important;
        padding: 24px 24px 30px 64px !important;
        position: relative !important;
        box-shadow: 
            -15px 0 25px -10px rgba(0, 0, 0, 0.6), 
            15px 20px 40px rgba(0, 0, 0, 0.4),
            inset 8px 0 12px -6px rgba(0, 0, 0, 0.15) !important;
        color: #1E3A8A !important;
    }

    /* Left Ring Binder Rings */
    .notebook-binder::before {
        content: '' !important;
        position: absolute !important;
        top: 20px !important;
        left: 14px !important;
        width: 16px !important;
        height: 92% !important;
        background-image: radial-gradient(circle, #94A3B8 5px, transparent 6px) !important;
        background-size: 16px 32px !important;
        background-repeat: repeat-y !important;
    }

    .notebook-header-band {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid #EF4444;
        padding-bottom: 4px;
        margin-bottom: 12px;
    }
    .notebook-topic-title {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        color: #0F172A !important;
    }
    .notebook-page-chip {
        font-size: 11px !important;
        font-weight: 700 !important;
        background: #EF4444 !important;
        color: #FFFFFF !important;
        padding: 2px 8px !important;
        border-radius: 10px !important;
    }

    .notebook-body {
        font-family: 'Caveat', cursive !important;
        font-size: 20px !important;
        line-height: 26px !important;
        color: #1E3A8A !important;
        white-space: pre-wrap !important;
        word-break: break-word !important;
    }

    /* Studio Card Panels */
    .studio-panel {
        background: rgba(255, 255, 255, 0.025);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px;
        backdrop-filter: blur(20px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }

    /* Streamlit Default Buttons Customization */
    .stButton>button {
        background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 10px !important;
        padding: 8px 18px !important;
        font-weight: 600 !important;
        font-size: 13.5px !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.3) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 24px rgba(124, 58, 237, 0.4) !important;
    }

    /* Compact Arrow Controls Row */
    div.flip-dock {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 16px;
        margin-top: 12px;
    }

    @media (max-width: 768px) {
        .notebook-binder {
            padding: 18px 16px 24px 50px !important;
            min-height: 440px !important;
            background-size: 100% 100%, 100% 24px !important;
        }
        .notebook-body {
            font-size: 18px !important;
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
        st.success("● AI Engine & Vision Connected")
    else:
        with st.expander("🔑 Setup API Key", expanded=True):
            gemini_key = st.text_input("Gemini API Key:", type="password")
            if gemini_key:
                genai.configure(api_key=gemini_key)
                st.success("Connected!")
    st.caption("Crafted by Raj • MLK PG College Balrampur")

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
    Current Subject Context: {current_subject}
    {lang_instruction}

    RULES FOR REGISTER NOTES:
    1. Write in natural, clean, readable student register notes format.
    2. No markdown hashes like '###' or raw LaTeX dollars like '$0/0$'. Use clean readable expressions like '0/0 form' or 'lim x->a [f(x)/g(x)]'.
    3. Strictly restrict each page to 50-70 words so that it fits completely on the notebook sheet without scrolling or cutoffs.
    4. Separate every page strictly with '[PAGE_BREAK]'.
    5. No metadata boilerplate (no 'Subject:', 'Instructor:', etc.). Start directly with point 1.

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

# ================= TOP APPLICATION BAR =================
st.markdown("""
<div class="top-app-bar">
    <div class="app-brand">
        <div class="brand-icon">⚡</div>
        <div>
            <div class="brand-text">BCA Academic Studio</div>
            <div style="font-size: 11px; color: #94A3B8;">MLK PG College Balrampur • Maa Pateshwari Univ</div>
        </div>
    </div>
    <div style="font-size: 12px; color: #38BDF8; font-weight: 600;">
        Created by Raj
    </div>
</div>
""", unsafe_allow_html=True)

# Subject Slot Bar
sub_col1, sub_col2 = st.columns([2, 1.2])
with sub_col1:
    selected_tab = st.radio(
        label="Navigation Menu",
        options=[
            "📝 Handwritten Notes",
            "📖 Syllabus Explorer",
            "📝 Exam Engine",
            "🛠️ Projects Lab",
            "🤖 AI Mentor",
            "🧪 Code Sandbox"
        ],
        horizontal=True,
        index=0
    )
with sub_col2:
    st.session_state.selected_subject = st.selectbox(
        "Active Stream Subject:",
        [
            "🐍 Python Programming",
            "🖥️ Computer System Architecture",
            "📐 Mathematics & Numerical Methods"
        ],
        index=0
    )

active_subj = st.session_state.selected_subject

# ================= 1. DYNAMIC HANDWRITTEN REGISTER FLIPPER =================
if selected_tab == "📝 Handwritten Notes":
    st.markdown(f"#### 📖 Real Notebook Register ({active_subj})")

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

    c1, c2 = st.columns([2.5, 1.2])
    with c1:
        chosen_topic = st.selectbox("Pick Topic to Write:", suggested_topics)
        custom_topic = st.text_input("Or enter syllabus query:", placeholder="e.g. DeMorgan's laws derivation")
    with c2:
        notes_lang = st.selectbox("Register Script Register:", ["Hinglish (Natural Notes)", "English", "Hindi (हिन्दी)"])

    final_topic = custom_topic.strip() if custom_topic.strip() else chosen_topic

    if st.button("✍️ Write on Register Pages", use_container_width=True):
        st.session_state.current_note_page = 1
        with st.spinner(f"AI Student Topper writing notes for {final_topic}..."):
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

    # DISPLAY REAL NOTEBOOK PAGE
    if st.session_state.dynamic_pages_list:
        pages = st.session_state.dynamic_pages_list
        total_pages = len(pages)
        curr_pg = min(st.session_state.current_note_page, total_pages)
        page_text = pages[curr_pg - 1].replace("\n", "<br>")

        st.markdown(f"""
        <div class="binder-container">
            <div class="notebook-binder">
                <div class="notebook-header-band">
                    <span class="notebook-topic-title">{st.session_state.get('flip_notes_topic')}</span>
                    <span class="notebook-page-chip">Page {curr_pg} of {total_pages}</span>
                </div>
                <div class="notebook-body">
{page_text}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # UNIFIED FLIP CONTROLS
        ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1.5, 3, 1.5])
        with ctrl_col1:
            if st.button("‹ Prev Page", disabled=(curr_pg == 1), use_container_width=True):
                st.session_state.current_note_page = max(1, curr_pg - 1)
                st.rerun()
        with ctrl_col2:
            st.markdown(f"""
            <div style="text-align: center; color: #94A3B8; font-size: 13px; padding-top: 6px;">
                Sheet {curr_pg} of {total_pages} • MLK PG College Balrampur
            </div>
            """, unsafe_allow_html=True)
        with ctrl_col3:
            if st.button("Next Page ›", disabled=(curr_pg == total_pages), use_container_width=True):
                st.session_state.current_note_page = min(total_pages, curr_pg + 1)
                st.rerun()

# ================= 2. SYLLABUS EXPLORER =================
elif selected_tab == "📖 Syllabus Explorer":
    st.markdown(f"#### 📚 Syllabus Blueprint: {active_subj}")
    
    if active_subj == "🐍 Python Programming":
        units = {
            "Module 1": "Language Basics, Bytecode & Operators",
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
            st.write(f"Comprehensive breakdown aligned with Maa Pateshwari State University syllabus.")
            if st.button(f"✨ Deep Dive {u_key}", key=f"btn_{u_key}"):
                with st.spinner("AI Professor summarizing core points..."):
                    summary = get_ai_response(f"Provide complete exam summary for {u_title} under {active_subj}.", current_subject=active_subj)
                    st.info(summary)

# ================= 3. EXAM ENGINE =================
elif selected_tab == "📝 Exam Engine":
    st.markdown(f"#### 📝 University Examination Simulator ({active_subj})")

    c1, c2 = st.columns([2, 1])
    with c1:
        exam_topic = st.text_input("Examination Focus Topic:", placeholder="e.g. Cache Mapping / L'Hopital Rule / Polymorphism")
    with c2:
        exam_lang = st.selectbox("Paper Language:", ["English", "Hinglish", "Hindi (हिन्दी)"])

    if st.button("⚡ Generate University Paper", use_container_width=True):
        with st.spinner("Preparing official MLK PG College question paper..."):
            prompt = f"Create a 15-mark examination test for '{exam_topic if exam_topic else 'Full Syllabus'}' in {active_subj}."
            st.session_state.exam_paper = get_ai_response(prompt, forced_language=exam_lang, current_subject=active_subj)

    if "exam_paper" in st.session_state:
        st.markdown(f"""
        <div class="studio-panel" style="margin-top: 15px;">
            <div style="font-size: 16px; font-weight: 700; color: #38BDF8; margin-bottom: 8px;">Official Question Paper</div>
            {st.session_state.exam_paper}
        </div>
        """, unsafe_allow_html=True)

        user_ans = st.text_area("Your Solutions (Type here):", height=120)
        uploaded_ans = st.file_uploader("Or Upload Answer Sheet Photo (PNG/JPG):", type=["png", "jpg", "jpeg"])
        pil_img = Image.open(uploaded_ans) if uploaded_ans else None

        if st.button("🚀 Submit For AI Evaluation", use_container_width=True):
            if not user_ans.strip() and not pil_img:
                st.warning("Please type or upload your answer sheet.")
            else:
                with st.spinner("AI University Examiner evaluating answer sheet..."):
                    eval_res = get_ai_response("Grade this student paper out of 15 with score breakdown.", image_input=pil_img, current_subject=active_subj)
                    st.markdown(f"""
                    <div class="studio-panel" style="border-left: 4px solid #34D399; margin-top: 15px;">
                        <div style="font-size: 16px; font-weight: 700; color: #34D399; margin-bottom: 6px;">Evaluator Scorecard</div>
                        {eval_res}
                    </div>
                    """, unsafe_allow_html=True)

# ================= 4. PROJECTS LAB =================
elif selected_tab == "🛠️ Projects Lab":
    st.markdown(f"#### 🛠️ Academic Capstone Blueprints ({active_subj})")

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
            <div class="studio-panel" style="margin-top: 15px;">
                {res}
            </div>
            """, unsafe_allow_html=True)

# ================= 5. AI TECHNICAL MENTOR =================
elif selected_tab == "🤖 AI Mentor":
    st.markdown(f"#### 🤖 24/7 AI Academic Mentor ({active_subj})")
    
    doubt_text = st.text_area("Type your question or error code:", height=120)
    uploaded_doubt = st.file_uploader("Or upload screenshot / question photo:", type=["png", "jpg", "jpeg"])
    doubt_img = Image.open(uploaded_doubt) if uploaded_doubt else None

    if st.button("⚡ Solve With AI", use_container_width=True):
        if not doubt_text.strip() and not doubt_img:
            st.warning("Please enter your doubt or upload a picture.")
        else:
            with st.spinner("AI Mentor solving step-by-step..."):
                sol = get_ai_response(doubt_text, image_input=doubt_img, current_subject=active_subj)
                st.markdown(f"""
                <div class="studio-panel" style="border-left: 4px solid #8B5CF6; margin-top: 15px;">
                    {sol}
                </div>
                """, unsafe_allow_html=True)

# ================= 6. LIVE CODE SANDBOX =================
elif selected_tab == "🧪 Code Sandbox":
    st.markdown(f"#### 🧪 Live Interactive Python Sandbox")
    
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
