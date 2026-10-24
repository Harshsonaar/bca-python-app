import streamlit as st
import google.generativeai as genai
import io
import contextlib
import time
from PIL import Image

st.set_page_config(
    page_title="Colab BCA OS | Harsh Raj Soni",
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

# Colab Notebook Multi-Cell Storage
if "notebook_cells" not in st.session_state:
    st.session_state.notebook_cells = [
        {
            "id": 1,
            "code": "# Cell 1: System Boot & Verification\nname = 'Harsh Raj Soni'\ncollege = 'MLK PG College Balrampur'\nprint(f'⚡ Colab Engine Connected | Dev: {name} [{college}]')",
            "output": "",
            "error": ""
        },
        {
            "id": 2,
            "code": "# Cell 2: Quick Algorithm Test\ndef fibonacci(n):\n    a, b = 0, 1\n    series = []\n    for _ in range(n):\n        series.append(a)\n        a, b = b, a + b\n    return series\n\nprint('Fibonacci (8 terms):', fibonacci(8))",
            "output": "",
            "error": ""
        }
    ]

# Virtual File System for Colab
if "saved_notebooks" not in st.session_state:
    st.session_state.saved_notebooks = {
        "welcome_colab.ipynb": st.session_state.notebook_cells
    }

# ================= GOOGLE COLAB DARK + ELECTRIC YELLOW CSS =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Patrick+Hand&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    .stApp {
        background-color: #0b0c10 !important;
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
        padding-top: 0.6rem !important;
        padding-bottom: 5rem !important;
        max-width: 1200px !important;
    }

    /* Colab App Bar */
    .colab-menubar {
        background: #15181f;
        border: 1px solid rgba(255, 230, 0, 0.25);
        border-radius: 12px;
        padding: 10px 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 14px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    .colab-brand {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .colab-logo {
        background: #FFE600;
        color: #000;
        font-weight: 900;
        padding: 3px 8px;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
    }
    .colab-status-box {
        display: inline-flex;
        align-items: center;
        gap: 12px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        color: #A3E635;
        background: rgba(0,0,0,0.4);
        padding: 4px 12px;
        border-radius: 20px;
        border: 1px solid rgba(163, 230, 53, 0.3);
    }

    /* Colab Cell Container */
    .colab-cell-container {
        background: #111318;
        border: 1px solid #1f2430;
        border-left: 3px solid #FFE600;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 16px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.4);
        transition: border-color 0.2s ease;
    }
    .colab-cell-container:hover {
        border-color: rgba(255, 230, 0, 0.45);
    }
    .colab-cell-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        color: #94A3B8;
    }

    /* Output Console Area */
    .colab-output-box {
        background: #060709;
        border-top: 1px solid #1f2430;
        padding: 10px 14px;
        margin-top: 8px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
        color: #E2E8F0;
        white-space: pre-wrap;
    }

    /* Colab Code Area Override */
    textarea[aria-label*="Code Cell"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 14px !important;
        background-color: #0d0f14 !important;
        color: #F8FAFC !important;
        border: 1px solid #232836 !important;
        line-height: 22px !important;
        tab-size: 4 !important;
        padding-left: 10px !important;
        border-radius: 6px !important;
    }
    textarea[aria-label*="Code Cell"]:focus {
        border-color: #FFE600 !important;
    }

    /* Navigation Dock */
    div[data-testid="stRadio"] {
        background: #15181f !important;
        border: 1px solid rgba(255, 230, 0, 0.25) !important;
        padding: 6px 10px !important;
        border-radius: 35px !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.6) !important;
        margin: 0 auto 16px auto !important;
        width: 100% !important;
        max-width: 960px !important;
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
        padding: 6px 12px !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        color: #94A3B8 !important;
        font-family: 'JetBrains Mono', monospace !important;
        margin: 0 !important;
    }
    div[data-testid="stRadio"] label:hover {
        background: rgba(255, 230, 0, 0.15) !important;
        color: #FFE600 !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }

    /* Notebook Register Paper */
    .register-center-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        margin-top: 4px;
        margin-bottom: 10px;
    }
    .notebook-paper-a4 {
        background-color: #ffffff !important;
        background-image: 
            linear-gradient(90deg, transparent 40px, #f43f5e 40px, #f43f5e 41.5px, transparent 41.5px),
            linear-gradient(#e2e8f0 1px, transparent 1px) !important;
        background-size: 100% 100%, 100% 24px !important;
        border-radius: 8px !important;
        padding: 18px 20px 22px 52px !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: 0 14px 40px rgba(0, 0, 0, 0.8), 0 0 20px rgba(255, 230, 0, 0.15) !important;
        width: 100% !important;
        max-width: 480px !important;
        height: 440px !important;
        max-height: 440px !important;
        overflow: hidden !important;
        position: relative !important;
        box-sizing: border-box !important;
        color: #1e3a8a !important;
    }
    .notebook-paper-a4::before {
        content: '' !important;
        position: absolute !important;
        top: 12px !important;
        left: 10px !important;
        width: 10px !important;
        height: 94% !important;
        background-image: radial-gradient(circle, #94a3b8 3.5px, transparent 4.5px) !important;
        background-size: 10px 24px !important;
        background-repeat: repeat-y !important;
    }
    .notebook-title-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid #ef4444;
        padding-bottom: 2px;
        margin-bottom: 6px;
    }
    .notebook-title-text {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        color: #0f172a !important;
    }
    .notebook-badge {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 10.5px !important;
        font-weight: 700 !important;
        background: #1e293b !important;
        color: #FFE600 !important;
        border: 1px solid rgba(255, 230, 0, 0.4) !important;
        padding: 2px 7px !important;
        border-radius: 6px !important;
    }
    .notebook-handwritten-text {
        font-family: 'Patrick Hand', cursive !important;
        font-size: 15px !important;
        line-height: 24px !important;
        color: #1e3a8a !important;
        word-break: break-word !important;
        white-space: pre-wrap !important;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #FFE600 0%, #EAB308 100%) !important;
        color: #0A0A0C !important;
        border: 1px solid #FFE600 !important;
        border-radius: 8px !important;
        padding: 6px 14px !important;
        font-weight: 800 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 12.5px !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(255, 230, 0, 0.4) !important;
    }

    @media (max-width: 768px) {
        .notebook-paper-a4 {
            padding: 14px 12px 18px 42px !important;
            max-width: 90vw !important;
            height: 380px !important;
            max-height: 380px !important;
            overflow: hidden !important;
        }
        .colab-menubar {
            flex-direction: column;
            gap: 8px;
            align-items: flex-start;
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
    st.markdown("### ⚡ COLAB RUNTIME")
    if gemini_key:
        st.markdown('<span style="color:#A3E635; font-family:\'JetBrains Mono\'; font-weight:700;">● GPU: T4 Connected</span>', unsafe_allow_html=True)
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
    You are a distinguished professor for the BCA curriculum at MLK PG College, Balrampur (affiliated with Maa Pateshwari State University).
    Subject Context: {current_subject}
    {lang_instruction}

    STRICT CONSTRAINTS FOR NOTEBOOK PAGES:
    1. Write in clean, concise student register notes.
    2. IMPORTANT: Keep each page strictly to ONLY 40 to 50 WORDS so that it fits completely on the compact mobile screen without extending or cutting off.
    3. Separate individual pages using the exact token '[PAGE_BREAK]'.
    4. NEVER output raw markdown hashes like '###' or raw unparsed LaTeX with broken dollar signs. Write simple readable formulas (e.g. 0/0 form, lim (x -> a) [f'(x) / g'(x)]).
    5. DO NOT output metadata boilerplate ('Subject:', 'Author:', 'Instructor:'). Start straight with the study points.

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
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:75vh; text-align:center;">
        <div style="display:inline-flex; align-items:center; gap:8px; background:rgba(255,230,0,0.1); border:1px solid #FFE600; padding:6px 20px; border-radius:30px; font-size:13px; font-weight:800; color:#FFE600; font-family:'JetBrains Mono'; margin-bottom:16px;">
            ⚡ GOOGLE COLAB ENGINE v2.6
        </div>
        <div style="font-size:36px; font-weight:800; background:linear-gradient(135deg, #FFFFFF 0%, #FFE600 50%, #FFAA00 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:8px;">
            CREATED & DESIGNED BY HARSH RAJ SONI
        </div>
        <div style="font-size:14px; color:#94A3B8; font-family:'JetBrains Mono'; margin-bottom:24px;">
            MLK PG COLLEGE BALRAMPUR • MAA PATESHWARI STATE UNIVERSITY
        </div>
        <div style="background:#0D0E12; border:1px solid rgba(255,230,0,0.3); border-left:4px solid #FFE600; border-radius:12px; padding:16px 22px; max-width:580px; width:100%; text-align:left; font-family:'JetBrains Mono'; font-size:13px; color:#FFE600; line-height:1.6; margin-bottom:24px;">
            <div><span style="color:#38BDF8;">root@colab-node:~$</span> colab --connect-runtime</div>
            <div style="color:#A3E635;">✔ Initializing Python 3.10 Kernel & Cells Engine...</div>
            <div style="color:#A3E635;">✔ Allocated Virtual Memory: 12.7 GB / 100 GB Disk</div>
            <div style="color:#A3E635;">✔ Mounting Cell Execution Context & AI Copilot</div>
            <div style="color:#FFE600;">⚡ Status: Connected to Google Colab Notebook Runtime.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        if st.button("⚡ OPEN NOTEBOOK WORKSPACE", use_container_width=True):
            st.session_state.system_booted = True
            st.rerun()

else:
    # ================= GOOGLE COLAB NOTEBOOK MENU BAR =================
    st.markdown("""
    <div class="colab-menubar">
        <div class="colab-brand">
            <span class="colab-logo">CO</span>
            <span style="font-size:15px; font-weight:700; color:#F8FAFC; font-family:'JetBrains Mono';">BCA_Notebook.ipynb</span>
            <span style="font-size:11px; color:#94A3B8; font-family:'JetBrains Mono';">• MLK PG College</span>
        </div>
        <div class="colab-status-box">
            <span>● Connected (Python 3)</span>
            <span style="color:#64748b;">|</span>
            <span>RAM: 1.8/12.7 GB</span>
            <span style="color:#64748b;">|</span>
            <span style="color:#FFE600;">Dev: Harsh Raj Soni</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Subject Selector Buttons
    st.markdown("<span style='font-size:11px; color:#FFE600; font-family:JetBrains Mono; font-weight:700;'>[SELECT STREAM]</span>", unsafe_allow_html=True)
    sub_col1, sub_col2, sub_col3 = st.columns(3)
    with sub_col1:
        if st.button("🐍 Python Programming", use_container_width=True):
            st.session_state.selected_subject = "🐍 Python Programming"
            st.rerun()
    with sub_col2:
        if st.button("🖥️ Computer System Architecture", use_container_width=True):
            st.session_state.selected_subject = "🖥️ Computer System Architecture"
            st.rerun()
    with sub_col3:
        if st.button("📐 Mathematics & Numerical Methods", use_container_width=True):
            st.session_state.selected_subject = "📐 Mathematics & Numerical Methods"
            st.rerun()

    active_subj = st.session_state.selected_subject
    st.caption(f"Active Kernel Context: **{active_subj}**")

    # Dynamic Navigation Dock
    nav_options = [
        "💻 Colab Notebook",
        "📝 Smart Register",
        "📖 Syllabus Explorer",
        "🎯 Exam Engine",
        "🔬 Projects Lab",
        "🤖 AI Mentor"
    ]
    if active_subj == "📐 Mathematics & Numerical Methods":
        nav_options.insert(2, "📐 Maths Menu")
    elif active_subj == "🖥️ Computer System Architecture":
        nav_options.insert(2, "🖥️ CSA Circuit Menu")

    selected_nav = st.radio(
        label="Main Navigation",
        options=nav_options,
        horizontal=True,
        index=0
    )

    # ================= 1. PURE GOOGLE COLAB NOTEBOOK ENGINE =================
    if selected_nav == "💻 Colab Notebook":
        # Colab Toolbar (+ Code, + Text, Clear, Restart)
        tb_c1, tb_c2, tb_c3, tb_c4 = st.columns([1, 1, 1.2, 1.2])
        with tb_c1:
            if st.button("➕ Code Cell", use_container_width=True):
                new_id = len(st.session_state.notebook_cells) + 1
                st.session_state.notebook_cells.append({
                    "id": new_id,
                    "code": "# New Colab Code Cell\n",
                    "output": "",
                    "error": ""
                })
                st.rerun()
        with tb_c2:
            if st.button("🗑️ Clear Outputs", use_container_width=True):
                for cell in st.session_state.notebook_cells:
                    cell["output"] = ""
                    cell["error"] = ""
                st.rerun()
        with tb_c3:
            with st.expander("📁 File Storage", expanded=False):
                fname = st.text_input("Save As:", placeholder="my_notebook.ipynb")
                if st.button("💾 Save Notebook", use_container_width=True):
                    if fname.strip():
                        st.session_state.saved_notebooks[fname.strip()] = list(st.session_state.notebook_cells)
                        st.success(f"Saved: {fname.strip()}")
        with tb_c4:
            with st.expander("📚 Python Cheatsheet", expanded=False):
                st.markdown("""
                - `import math, re, json, datetime, collections, itertools`
                - Standard PEP-8 4-space indentation
                - `def func(*args, **kwargs):`
                """)

        st.markdown("---")

        # RENDER NOTEBOOK CELLS (COLAB STYLE)
        for idx, cell in enumerate(st.session_state.notebook_cells):
            cell_id = cell["id"]
            
            st.markdown(f"""
            <div class="colab-cell-container">
                <div class="colab-cell-header">
                    <span><b>[ {idx + 1} ]</b> In [ ]: Python 3 Cell</span>
                    <span>MLK_BCA_KERNEL</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            c_editor, c_btn = st.columns([9, 1.2])
            with c_editor:
                updated_code = st.text_area(
                    f"Code Cell {idx + 1}",
                    value=cell["code"],
                    height=140,
                    key=f"cell_code_{cell_id}",
                    label_visibility="collapsed"
                )
                cell["code"] = updated_code
            with c_btn:
                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                run_cell = st.button("▶ Run", key=f"run_btn_{cell_id}", use_container_width=True)
                copilot_cell = st.button("⚡ Copilot", key=f"copilot_{cell_id}", use_container_width=True)

            # Cell Run Logic
            if run_cell:
                buf = io.StringIO()
                try:
                    with contextlib.redirect_stdout(buf):
                        exec(cell["code"], {})
                    cell["output"] = buf.getvalue() if buf.getvalue() else "[Cell executed successfully with no output]"
                    cell["error"] = ""
                except Exception as ex:
                    cell["output"] = ""
                    cell["error"] = str(ex)

            # AI Copilot Logic for this cell
            if copilot_cell:
                with st.spinner("AI Copilot analyzing cell..."):
                    cop_prompt = f"Analyze this Python notebook cell code and suggest 1-line intent + optimization:\n```python\n{cell['code']}\n```"
                    cell["output"] = f"[AI Copilot Suggestion]:\n" + get_ai_response(cop_prompt, current_subject="Python")
                    cell["error"] = ""

            # Cell Output Block (Colab Out [X])
            if cell["output"]:
                st.markdown(f"""
                <div style="background:#07080a; border-left:3px solid #A3E635; padding:10px 14px; border-radius:4px; font-family:'JetBrains Mono'; font-size:13px; color:#F8FAFC; margin-bottom:12px;">
                    <span style="color:#A3E635; font-size:11px; display:block; margin-bottom:4px;">Out [ {idx + 1} ]:</span>
                    {cell['output']}
                </div>
                """, unsafe_allow_html=True)

            if cell["error"]:
                st.markdown(f"""
                <div style="background:#07080a; border-left:3px solid #EF4444; padding:10px 14px; border-radius:4px; font-family:'JetBrains Mono'; font-size:13px; color:#FCA5A5; margin-bottom:12px;">
                    <span style="color:#EF4444; font-size:11px; display:block; margin-bottom:4px;">Traceback (Runtime Error):</span>
                    {cell['error']}
                </div>
                """, unsafe_allow_html=True)
                
                # Single-click Colab Auto-Fixer
                if st.button("🛠️ Colab Auto-Fix Error", key=f"fix_{cell_id}"):
                    with st.spinner("AI Auto-Fixing cell error..."):
                        fix_res = get_ai_response(f"Fix this Python code error:\nCode:\n{cell['code']}\nError:\n{cell['error']}\nProvide only the fixed code.", current_subject="Python")
                        st.info(fix_res)

    # ================= 2. SMART REGISTER NOTES =================
    elif selected_nav == "📝 Smart Register":
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
                    <div style="font-size: 11px; color: #64748b; margin-bottom: 6px;">
                        <b>Subject:</b> {active_subj} | <b>MLK PG College Balrampur</b>
                    </div>
                    <div class="notebook-handwritten-text">
{page_text}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

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

    # ================= 3. MATHS MENU =================
    elif selected_nav == "📐 Maths Menu":
        st.markdown("#### 📐 Mathematics Formula Menu")
        with st.expander("⚡ Differentiation Rules"):
            st.latex(r"\frac{d}{dx}(x^n) = n x^{n-1}, \quad \frac{d}{dx}(u \cdot v) = u v' + v u'")
        with st.expander("🎯 L'Hopital's Rule"):
            st.latex(r"\lim_{x \to a} \frac{f(x)}{g(x)} = \lim_{x \to a} \frac{f'(x)}{g'(x)} \quad \left(\frac{0}{0} \text{ or } \frac{\infty}{\infty}\right)")
        with st.expander("🔢 Matrix & Echelon Rank"):
            st.write("Rank = Number of non-zero rows in Echelon form.")

    # ================= 4. CSA CIRCUIT MENU =================
    elif selected_nav == "🖥️ CSA Circuit Menu":
        st.markdown("#### 🖥️ CSA Circuit Equations")
        st.latex(r"Sum = A \oplus B \oplus C_{in}, \quad Carry = AB + C_{in}(A \oplus B)")

    # ================= 5. SYLLABUS EXPLORER =================
    elif selected_nav == "📖 Syllabus Explorer":
        st.markdown(f"#### 📚 Syllabus: {active_subj}")
        st.info("Full official syllabus modules for MLK PG College Balrampur.")

    # ================= 6. EXAM ENGINE =================
    elif selected_nav == "🎯 Exam Engine":
        st.markdown(f"#### 🎯 Exam Paper Generator ({active_subj})")
        if st.button("⚡ Generate Test Paper", use_container_width=True):
            st.session_state.exam_p = get_ai_response("Create 15-mark test", current_subject=active_subj)
        if "exam_p" in st.session_state:
            st.write(st.session_state.exam_p)

    # ================= 7. PROJECTS LAB =================
    elif selected_nav == "🔬 Projects Lab":
        st.markdown(f"#### 🔬 Academic Capstone Projects ({active_subj})")
        st.write("Production grade semester blueprints.")

    # ================= 8. AI MENTOR =================
    elif selected_nav == "🤖 AI Mentor":
        st.markdown(f"#### 🤖 24/7 AI Terminal Mentor ({active_subj})")
        q = st.text_input("Ask Doubt:")
        if st.button("Solve") and q:
            st.write(get_ai_response(q, current_subject=active_subj))
