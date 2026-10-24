import streamlit as st
import google.generativeai as genai
import io
import contextlib
import time
from PIL import Image

st.set_page_config(
    page_title="BCA OS | Harsh Raj Soni",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session States
if "system_booted" not in st.session_state:
    st.session_state.system_booted = False

if "selected_subject" not in st.session_state:
    st.session_state.selected_subject = "🐍 Python Programming"

if "current_note_page" not in st.session_state:
    st.session_state.current_note_page = 1

if "dynamic_pages_list" not in st.session_state:
    st.session_state.dynamic_pages_list = []

# ================= CYBER CODER BLACK & ELECTRIC YELLOW CSS =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Patrick+Hand&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Ambient Obsidian & Electric Gold Canvas */
    .stApp {
        background: radial-gradient(circle at 50% -20%, rgba(255, 230, 0, 0.16) 0%, rgba(18, 16, 5, 0.6) 40%, #08080A 100%) !important;
        color: #F8FAFC;
    }

    /* Streamlit Host Overrides */
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
        padding-top: 1rem !important;
        padding-bottom: 5rem !important;
        max-width: 1180px !important;
    }

    /* ================= OPENING DEVELOPER BOOT SCREEN ================= */
    .splash-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 75vh;
        text-align: center;
        position: relative;
    }
    .system-status-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 230, 0, 0.1);
        border: 1px solid #FFE600;
        padding: 6px 20px;
        border-radius: 30px;
        font-size: 13px;
        font-weight: 800;
        color: #FFE600;
        letter-spacing: 2px;
        box-shadow: 0 0 25px rgba(255, 230, 0, 0.35);
        margin-bottom: 16px;
        font-family: 'JetBrains Mono', monospace;
    }
    .splash-author {
        font-size: 38px;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 0%, #FFE600 50%, #FFAA00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
        margin-bottom: 8px;
    }
    .splash-sub {
        font-size: 14px;
        color: #94A3B8;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 24px;
    }
    .coder-terminal-box {
        background: #0D0E12;
        border: 1px solid rgba(255, 230, 0, 0.3);
        border-left: 4px solid #FFE600;
        border-radius: 12px;
        padding: 16px 22px;
        max-width: 580px;
        width: 100%;
        text-align: left;
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
        color: #FFE600;
        box-shadow: 0 10px 35px rgba(0,0,0,0.8);
        margin-bottom: 24px;
        line-height: 1.6;
    }

    /* Cyber Coder Top Banner */
    .cyber-top-banner {
        background: rgba(13, 14, 18, 0.85);
        border: 1px solid rgba(255, 230, 0, 0.25);
        border-radius: 16px;
        padding: 14px 22px;
        backdrop-filter: blur(20px);
        margin-bottom: 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
    }
    .author-glow-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255, 230, 0, 0.12);
        border: 1px solid #FFE600;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        color: #FFE600;
        font-family: 'JetBrains Mono', monospace;
        box-shadow: 0 0 15px rgba(255, 230, 0, 0.25);
    }

    /* Top Navigation Dock */
    div[data-testid="stRadio"] {
        background: rgba(13, 14, 18, 0.9) !important;
        border: 1px solid rgba(255, 230, 0, 0.25) !important;
        padding: 6px 10px !important;
        border-radius: 35px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7) !important;
        margin: 0 auto 16px auto !important;
        width: 100% !important;
        max-width: 820px !important;
    }
    div[data-testid="stRadio"] > label {display: none !important;}
    div[data-testid="stRadio"] > div {
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        align-items: center !important;
        flex-wrap: wrap !important;
        gap: 4px !important;
    }
    div[data-testid="stRadio"] label {
        background: transparent !important;
        border-radius: 20px !important;
        padding: 6px 14px !important;
        font-size: 12.5px !important;
        font-weight: 700 !important;
        color: #94A3B8 !important;
        font-family: 'JetBrains Mono', monospace !important;
        transition: all 0.2s ease !important;
        margin: 0 !important;
    }
    div[data-testid="stRadio"] label:hover {
        background: rgba(255, 230, 0, 0.15) !important;
        color: #FFE600 !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }

    /* ================= REGISTER NOTEBOOK CARD ================= */
    .register-center-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        margin-top: 6px;
        margin-bottom: 12px;
    }
    .notebook-paper-a4 {
        background-color: #ffffff !important;
        background-image: 
            linear-gradient(90deg, transparent 42px, #f43f5e 42px, #f43f5e 43.5px, transparent 43.5px),
            linear-gradient(#e2e8f0 1px, transparent 1px) !important;
        background-size: 100% 100%, 100% 26px !important;
        border-radius: 8px !important;
        padding: 22px 24px 30px 56px !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: 0 16px 45px rgba(0, 0, 0, 0.8), 0 0 20px rgba(255, 230, 0, 0.15) !important;
        width: 100% !important;
        max-width: 530px !important;
        min-height: 480px !important;
        height: auto !important;
        position: relative !important;
        box-sizing: border-box !important;
        color: #1e3a8a !important;
    }

    /* Left Ring Binder */
    .notebook-paper-a4::before {
        content: '' !important;
        position: absolute !important;
        top: 14px !important;
        left: 11px !important;
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
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        background: #1e293b !important;
        color: #FFE600 !important;
        border: 1px solid rgba(255, 230, 0, 0.4) !important;
        padding: 2px 8px !important;
        border-radius: 6px !important;
    }

    .notebook-handwritten-text {
        font-family: 'Patrick Hand', cursive !important;
        font-size: 16.5px !important;
        line-height: 26px !important;
        color: #1e3a8a !important;
        word-break: break-word !important;
        white-space: pre-wrap !important;
    }

    /* Cyber Panels */
    .cyber-panel {
        background: rgba(13, 14, 18, 0.85);
        border: 1px solid rgba(255, 230, 0, 0.2);
        border-radius: 14px;
        padding: 22px;
        backdrop-filter: blur(20px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
        margin-top: 14px;
    }

    /* Electric Yellow Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #FFE600 0%, #EAB308 100%) !important;
        color: #0A0A0C !important;
        border: 1px solid #FFE600 !important;
        border-radius: 10px !important;
        padding: 8px 20px !important;
        font-weight: 800 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 13.5px !important;
        letter-spacing: 0.5px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 15px rgba(255, 230, 0, 0.3) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 230, 0, 0.6) !important;
    }

    @media (max-width: 768px) {
        .notebook-paper-a4 {
            padding: 16px 14px 22px 46px !important;
            max-width: 95vw !important;
            min-height: 440px !important;
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
    st.markdown("### ⚡ SYSTEM TERMINAL")
    if gemini_key:
        st.markdown('<span style="color:#FFE600; font-family:\'JetBrains Mono\'; font-weight:700;">● CORE STATUS: ACTIVE</span>', unsafe_allow_html=True)
    else:
        with st.expander("🔑 Setup API Key", expanded=True):
            gemini_key = st.text_input("Gemini API Key:", type="password")
            if gemini_key:
                genai.configure(api_key=gemini_key)
                st.success("Connected!")
    st.markdown("---")
    st.caption("⚡ Created by **Harsh Raj Soni**")
    st.caption("🏛️ MLK PG College Balrampur")

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
    You are a distinguished computer science professor for the BCA curriculum at MLK PG College, Balrampur (affiliated with Maa Pateshwari State University).
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

# ================= 0. CODER BOOT & LOADING SCREEN =================
if not st.session_state.system_booted:
    st.markdown("""
    <div class="splash-box">
        <div class="system-status-badge">⚡ BCA ACADEMIC SYSTEM v2.6</div>
        <div class="splash-author">CREATED & DESIGNED BY HARSH RAJ SONI</div>
        <div class="splash-sub">MLK PG COLLEGE BALRAMPUR • MAA PATESHWARI STATE UNIVERSITY</div>
        <div class="coder-terminal-box">
            <div><span style="color:#38BDF8;">root@harshraj-os:~$</span> initialize_environment</div>
            <div style="color:#A3E635;">✔ Initializing Neural Kernel & LLM Gateway...</div>
            <div style="color:#A3E635;">✔ Loading Syllabus Modules: [Python, CSA, Discrete Maths]</div>
            <div style="color:#A3E635;">✔ Vision Multimodal Pipeline: Online</div>
            <div style="color:#FFE600;">⚡ Status: Environment Ready. High-Performance Mode Engaged.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        if st.button("⚡ LAUNCH & ENTER SYSTEM", use_container_width=True):
            st.session_state.system_booted = True
            st.rerun()

else:
    # ================= TOP APP HEADER =================
    st.markdown("""
    <div class="cyber-top-banner">
        <div>
            <div style="font-size: 19px; font-weight: 800; color: #FFE600; letter-spacing: -0.5px; font-family:'JetBrains Mono';">
                ⚡ BCA ACADEMIC OS
            </div>
            <div style="font-size: 11px; color: #94A3B8; font-family:'JetBrains Mono';">
                MLK PG College Balrampur • Maa Pateshwari State Univ
            </div>
        </div>
        <div class="author-glow-pill">
            ⚡ Dev: Harsh Raj Soni
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Subject Selector Bar
    sub_col1, sub_col2 = st.columns([2, 1])
    with sub_col1:
        st.markdown("<span style='font-size:12px; color:#FFE600; font-family:JetBrains Mono;'>[ACTIVE_STREAM]</span>", unsafe_allow_html=True)
    with sub_col2:
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

    # Top Navigation Dock
    selected_nav = st.radio(
        label="Main Navigation",
        options=[
            "📝 Smart Register",
            "📖 Syllabus Explorer",
            "🎯 Exam Engine",
            "🔬 Projects Lab",
            "🤖 AI Mentor",
            "💻 Code Sandbox"
        ],
        horizontal=True,
        index=0
    )

    # ================= 1. SMART REGISTER NOTES =================
    if selected_nav == "📝 Smart Register":
        st.markdown(f"#### 📖 Handwritten Register Notebook // {active_subj}")

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
            custom_topic = st.text_input("Or enter custom query:", placeholder="e.g. Master-slave JK flip-flop working")
        with c2:
            notes_lang = st.selectbox("Script Register:", ["Hinglish (Natural Notes)", "English", "Hindi (हिन्दी)"])

        final_topic = custom_topic.strip() if custom_topic.strip() else chosen_topic

        if st.button("⚡ WRITE ON REGISTER SHEETS", use_container_width=True):
            st.session_state.current_note_page = 1
            with st.spinner(f"⚡ Inscribing notes for {final_topic}..."):
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

        # DISPLAY CLEAN REGISTER SHEET WITH ARROW-ONLY FLIPPER
        if st.session_state.dynamic_pages_list:
            pages = st.session_state.dynamic_pages_list
            total_pages = len(pages)
            curr_pg = min(st.session_state.current_note_page, total_pages)
            page_text = pages[curr_pg - 1].replace("\n", "<br>")

            st.markdown(f"""
            <div class="register-center-wrapper">
                <div class="notebook-paper-a4">
                    <div class="notebook-title-row">
                        <span class="notebook-title-text">{st.session_state.get('flip_notes_topic')}</span>
                        <span class="notebook-badge">SHEET {curr_pg} / {total_pages}</span>
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

            # ARROWS-ONLY FLIPPER DOCK
            ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1, 2, 1])
            with ctrl_col1:
                if st.button("‹", disabled=(curr_pg == 1), use_container_width=True, help="Previous Page"):
                    st.session_state.current_note_page = max(1, curr_pg - 1)
                    st.rerun()
            with ctrl_col2:
                st.markdown(f"""
                <div style="text-align: center; color: #FFE600; font-family:'JetBrains Mono'; font-size: 13px; font-weight: 700; padding-top: 8px;">
                    SHEET {curr_pg} OF {total_pages}
                </div>
                """, unsafe_allow_html=True)
            with ctrl_col3:
                if st.button("›", disabled=(curr_pg == total_pages), use_container_width=True, help="Next Page"):
                    st.session_state.current_note_page = min(total_pages, curr_pg + 1)
                    st.rerun()

    # ================= 2. SYLLABUS EXPLORER =================
    elif selected_nav == "📖 Syllabus Explorer":
        st.markdown(f"#### 📚 University Syllabus Matrix // {active_subj}")
        
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
                if st.button(f"⚡ Deep Dive {u_key}", key=f"btn_{u_key}"):
                    with st.spinner("Analyzing curriculum..."):
                        summary = get_ai_response(f"Provide complete exam summary for {u_title} under {active_subj}.", current_subject=active_subj)
                        st.info(summary)

    # ================= 3. EXAM ENGINE =================
    elif selected_nav == "🎯 Exam Engine":
        st.markdown(f"#### 🎯 Examination Simulator & Vision Evaluator // {active_subj}")

        c1, c2 = st.columns([2, 1])
        with c1:
            exam_topic = st.text_input("Target Examination Scope:", placeholder="e.g. Cache Mapping / L'Hopital Rule / Polymorphism")
        with c2:
            exam_lang = st.selectbox("Language Mode:", ["English", "Hinglish", "Hindi (हिन्दी)"])

        if st.button("⚡ GENERATE UNIVERSITY PAPER", use_container_width=True):
            with st.spinner("Compiling test paper..."):
                prompt = f"Create a 15-mark examination test for '{exam_topic if exam_topic else 'Full Syllabus'}' in {active_subj}."
                st.session_state.exam_paper = get_ai_response(prompt, forced_language=exam_lang, current_subject=active_subj)

        if "exam_paper" in st.session_state:
            st.markdown(f"""
            <div class="cyber-panel">
                <div style="font-size: 15px; font-weight: 700; color: #FFE600; font-family:'JetBrains Mono'; margin-bottom: 8px;">[EXAM_PAPER_LIVE]</div>
                {st.session_state.exam_paper}
            </div>
            """, unsafe_allow_html=True)

            user_ans = st.text_area("Your Solutions (Type here):", height=120)
            uploaded_ans = st.file_uploader("Or Upload Answer Sheet Photo (PNG/JPG):", type=["png", "jpg", "jpeg"])
            pil_img = Image.open(uploaded_ans) if uploaded_ans else None

            if st.button("⚡ SUBMIT FOR AI EVALUATION", use_container_width=True):
                if not user_ans.strip() and not pil_img:
                    st.warning("Please type your solution or upload a photo.")
                else:
                    with st.spinner("Evaluating scorecard..."):
                        eval_res = get_ai_response("Grade this student paper out of 15 with score breakdown.", image_input=pil_img, current_subject=active_subj)
                        st.markdown(f"""
                        <div class="cyber-panel" style="border-left: 4px solid #A3E635;">
                            <div style="font-size: 15px; font-weight: 700; color: #A3E635; font-family:'JetBrains Mono'; margin-bottom: 6px;">[EVALUATOR_SCORECARD]</div>
                            {eval_res}
                        </div>
                        """, unsafe_allow_html=True)

    # ================= 4. PROJECTS LAB =================
    elif selected_nav == "🔬 Projects Lab":
        st.markdown(f"#### 🔬 Academic Capstone Blueprints // {active_subj}")

        if active_subj == "🐍 Python Programming":
            projs = ["Student Management Portal (SQLite)", "Banking ATM Simulator (OOP)", "Inventory Billing Engine"]
        elif active_subj == "🖥️ Computer System Architecture":
            projs = ["Half & Full Adder Simulator", "4-Bit ALU Architecture", "Direct Mapped Cache Simulator"]
        else:
            projs = ["Newton-Raphson Equation Solver", "Matrix Rank Calculator", "Graph Theory Shortest Path"]

        selected_proj = st.selectbox("Select Project Blueprint:", projs)
        if st.button("⚡ GENERATE CODEBASE ARCHITECTURE", use_container_width=True):
            with st.spinner("Generating architecture..."):
                res = get_ai_response(f"Provide complete working code and documentation for project: '{selected_proj}' in {active_subj}.", current_subject=active_subj)
                st.markdown(f"""
                <div class="cyber-panel">
                    {res}
                </div>
                """, unsafe_allow_html=True)

    # ================= 5. AI MENTOR =================
    elif selected_nav == "🤖 AI Mentor":
        st.markdown(f"#### 🤖 24/7 AI Terminal Mentor // {active_subj}")
        
        doubt_text = st.text_area("Enter your query or stack trace:", height=120)
        uploaded_doubt = st.file_uploader("Or upload screenshot / question photo:", type=["png", "jpg", "jpeg"])
        doubt_img = Image.open(uploaded_doubt) if uploaded_doubt else None

        if st.button("⚡ EXECUTE AI DEBUGGER", use_container_width=True):
            if not doubt_text.strip() and not doubt_img:
                st.warning("Please enter your doubt or upload an image.")
            else:
                with st.spinner("Analyzing neural context..."):
                    sol = get_ai_response(doubt_text, image_input=doubt_img, current_subject=active_subj)
                    st.markdown(f"""
                    <div class="cyber-panel" style="border-left: 4px solid #FFE600;">
                        {sol}
                    </div>
                    """, unsafe_allow_html=True)

    # ================= 6. TERMINAL SANDBOX =================
    elif selected_nav == "💻 Code Sandbox":
        st.markdown(f"#### 💻 Interactive Python Terminal Engine")
        
        starter_code = """# Interactive Python Sandbox
def system_execution():
    developer = "Harsh Raj Soni"
    college = "MLK PG College Balrampur"
    return f"⚡ [SUCCESS] Portal built by {developer} ({college})"

print(system_execution())
"""
        user_code = st.text_area("Terminal Editor:", value=starter_code, height=180)
        c1, c2 = st.columns([1, 1])
        with c1:
            run_code = st.button("▶ EXECUTE SCRIPT", use_container_width=True)
        with c2:
            st.download_button("💾 EXPORT (.PY)", data=user_code, file_name="bca_code.py", use_container_width=True)

        if run_code:
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf):
                    exec(user_code, {})
                st.success("Execution Successful")
                st.code(buf.getvalue() if buf.getvalue() else "[Program executed with no terminal output]")
            except Exception as err:
                st.error(f"Runtime Traceback: {err}")
