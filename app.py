import streamlit as st
import google.generativeai as genai
import io
import contextlib
import time
from PIL import Image

st.set_page_config(
    page_title="BCA Academic Suite | MLK PG College",
    page_icon="🎓",
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

# Colab Notebook Multi-Cell Storage (Python Only)
if "notebook_cells" not in st.session_state:
    st.session_state.notebook_cells = [
        {
            "id": 1,
            "code": "# Python Cell 1: Verification & Metadata\nstudent_name = 'Harsh Raj Soni'\ninstitution = 'MLK PG College, Balrampur'\nprint(f'Academic Portal Active | Scholar: {student_name} [{institution}]')",
            "output": "",
            "error": ""
        },
        {
            "id": 2,
            "code": "# Python Cell 2: Numerical & Algorithmic Logic\ndef is_prime(number):\n    if number <= 1:\n        return False\n    for divisor in range(2, int(number**0.5) + 1):\n        if number % divisor == 0:\n            return False\n    return True\n\nval = 37\nprint(f'Is {val} a prime number?:', is_prime(val))",
            "output": "",
            "error": ""
        }
    ]

# ================= EXECUTIVE SLATE & DEEP SAPPHIRE CSS =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Patrick+Hand&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Executive Navy Dark Background */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #0F172A 0%, #080D1A 60%, #020617 100%) !important;
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
        max-width: 1140px !important;
    }

    /* Executive Top Bar */
    .formal-top-banner {
        background: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 14px 22px;
        backdrop-filter: blur(20px);
        margin-bottom: 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }
    .formal-author-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(37, 99, 235, 0.12);
        border: 1px solid rgba(37, 99, 235, 0.35);
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        color: #60A5FA;
    }

    /* Subject Tiles Styling */
    .tile-label {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        color: #94A3B8;
        margin-bottom: 6px;
        display: block;
    }

    /* Formal Navigation Bar */
    div[data-testid="stRadio"] {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 6px 10px !important;
        border-radius: 35px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45) !important;
        margin: 0 auto 18px auto !important;
        width: 100% !important;
        max-width: 980px !important;
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
        font-weight: 600 !important;
        color: #94A3B8 !important;
        margin: 0 !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stRadio"] label:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        color: #FFFFFF !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }

    /* Academic Ruled Register */
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
            linear-gradient(90deg, transparent 40px, #ef4444 40px, #ef4444 41.5px, transparent 41.5px),
            linear-gradient(#e2e8f0 1px, transparent 1px) !important;
        background-size: 100% 100%, 100% 24px !important;
        border-radius: 8px !important;
        padding: 18px 20px 22px 52px !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: 0 14px 40px rgba(0, 0, 0, 0.65) !important;
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
        font-size: 10.5px !important;
        font-weight: 700 !important;
        background: #1e293b !important;
        color: #60A5FA !important;
        border: 1px solid rgba(96, 165, 250, 0.3) !important;
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

    /* Formal Card Panel */
    .formal-panel {
        background: rgba(30, 41, 59, 0.35);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 18px 20px;
        backdrop-filter: blur(20px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
        margin-top: 12px;
    }
    .formula-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-left: 3px solid #3B82F6;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 10px;
    }

    /* Colab Cells (Formal Navy Edition) */
    .colab-cell-box {
        background: #0E1526;
        border: 1px solid #1E293B;
        border-left: 3px solid #3B82F6;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 14px;
    }

    /* Primary Formal Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 8px !important;
        padding: 7px 16px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5) !important;
    }

    /* Phone Constraint (< 768px) */
    @media (max-width: 768px) {
        .notebook-paper-a4 {
            padding: 14px 12px 18px 42px !important;
            max-width: 90vw !important;
            height: 380px !important;
            max-height: 380px !important;
            overflow: hidden !important;
            background-size: 100% 100%, 100% 21px !important;
        }
        .notebook-handwritten-text {
            font-size: 13.5px !important;
            line-height: 21px !important;
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
    st.markdown("### 🏛️ Academic Environment")
    if gemini_key:
        st.success("● AI Engine & Vision Active")
    else:
        with st.expander("🔑 Setup API Key", expanded=True):
            gemini_key = st.text_input("Gemini API Key:", type="password")
            if gemini_key:
                genai.configure(api_key=gemini_key)
                st.success("Connected!")
    st.markdown("---")
    st.caption("⚡ Developed by **Harsh Raj Soni**")
    st.caption("🏛️ MLK PG College, Balrampur")

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

    # STRICT FORMAL MODERATION GUARDRAILS (NO SLANG / NO INFORMAL / NO ABUSIVE WORDS)
    optimized_prompt = f"""
    You are an esteemed university professor for the Bachelor of Computer Applications (BCA) program at MLK PG College, Balrampur (affiliated with Maa Pateshwari State University).
    Subject Discipline: {current_subject}
    {lang_instruction}

    STRICT ACADEMIC CONDUCT & LANGUAGE POLICY:
    1. STRICT RESTRICTION: Maintain an academic, respectful, and dignified tone suitable for college professors and students. NEVER use colloquial, street slang, or offensive Hindi words (such as 'pel', 'chutiya', 'bakchodi', etc.). Use formal terms like 'solve karein', 'dhyan dein', 'likhein', 'pariksha mein dhyan rakhein'.
    2. FOR REGISTER NOTES: Keep each page strictly to 40 to 50 words to perfectly fit the compact mobile notebook page without cutoff.
    3. Separate individual pages with the exact delimiter token '[PAGE_BREAK]'.
    4. Provide completed, verifiable code and derivations without truncation.

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

# ================= 0. FORMAL ACADEMIC INTRO SCREEN =================
if not st.session_state.system_booted:
    st.markdown("""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:72vh; text-align:center;">
        <div style="display:inline-flex; align-items:center; gap:8px; background:rgba(37,99,235,0.12); border:1px solid #3B82F6; padding:6px 20px; border-radius:30px; font-size:13px; font-weight:700; color:#60A5FA; margin-bottom:14px;">
            🎓 BCA ACADEMIC ECOSYSTEM
        </div>
        <div style="font-size:32px; font-weight:800; color:#F8FAFC; letter-spacing:-0.5px; margin-bottom:6px;">
            Created & Designed by Harsh Raj Soni
        </div>
        <div style="font-size:14px; color:#94A3B8; margin-bottom:24px;">
            MLK PG College, Balrampur • Affiliated with Maa Pateshwari State University
        </div>
        <div style="background:#0F172A; border:1px solid rgba(255,255,255,0.1); border-left:4px solid #3B82F6; border-radius:10px; padding:16px 22px; max-width:560px; width:100%; text-align:left; font-size:13px; color:#CBD5E1; line-height:1.6; margin-bottom:24px;">
            <div style="color:#60A5FA; font-weight:700; margin-bottom:4px;">Academic Portal Specification:</div>
            <div>• Core Curriculum Coverage: Python Programming, CSA & Discrete Mathematics</div>
            <div>• Real-time Ruled Register Notes & Formula Compendium</div>
            <div>• Interactive Evaluation & Sandbox Environment</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        if st.button("🚀 ENTER ACADEMIC PORTAL", use_container_width=True):
            st.session_state.system_booted = True
            st.rerun()

else:
    # ================= TOP EXECUTIVE BAR =================
    st.markdown("""
    <div class="formal-top-banner">
        <div>
            <div style="font-size: 18px; font-weight: 700; color: #F8FAFC;">
                BCA Academic Portal
            </div>
            <div style="font-size: 12px; color: #94A3B8;">
                MLK PG College, Balrampur • Maa Pateshwari State University
            </div>
        </div>
        <div class="formal-author-pill">
            Scholar: Harsh Raj Soni
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ================= SUBJECT TILES SWITCHER (FORMAL & CLEAN) =================
    st.markdown('<span class="tile-label">Academic Subject Discipline</span>', unsafe_allow_html=True)
    tile_col1, tile_col2, tile_col3 = st.columns(3)
    
    with tile_col1:
        is_py = (st.session_state.selected_subject == "🐍 Python Programming")
        btn_py = st.button("🐍 Python Programming", use_container_width=True, type="primary" if is_py else "secondary")
        if btn_py:
            st.session_state.selected_subject = "🐍 Python Programming"
            st.rerun()

    with tile_col2:
        is_csa = (st.session_state.selected_subject == "🖥️ Computer System Architecture")
        btn_csa = st.button("🖥️ Computer System Architecture", use_container_width=True, type="primary" if is_csa else "secondary")
        if btn_csa:
            st.session_state.selected_subject = "🖥️ Computer System Architecture"
            st.rerun()

    with tile_col3:
        is_math = (st.session_state.selected_subject == "📐 Mathematics & Numerical Methods")
        btn_math = st.button("📐 Mathematics & Numerical Methods", use_container_width=True, type="primary" if is_math else "secondary")
        if btn_math:
            st.session_state.selected_subject = "📐 Mathematics & Numerical Methods"
            st.rerun()

    active_subj = st.session_state.selected_subject

    # ================= DYNAMIC SUBJECT-SPECIFIC NAVIGATION DOCK =================
    nav_options = [
        "📝 Smart Register",
        "📖 Syllabus Explorer",
        "🎯 Exam Engine",
        "🔬 Projects Lab",
        "🤖 AI Academic Mentor"
    ]
    
    # Strict Subject-Specific Add-ons
    if active_subj == "🐍 Python Programming":
        nav_options.append("💻 Colab Notebook & Sandbox")
    elif active_subj == "📐 Mathematics & Numerical Methods":
        nav_options.insert(1, "📐 Maths Encyclopedia")
    elif active_subj == "🖥️ Computer System Architecture":
        nav_options.insert(1, "🖥️ CSA Circuit Matrix")

    selected_nav = st.radio(
        label="Navigation Section",
        options=nav_options,
        horizontal=True,
        index=0
    )

    # ================= 1. SMART REGISTER NOTES =================
    if selected_nav == "📝 Smart Register":
        st.markdown(f"#### 📖 Handwritten Register Notebook — {active_subj}")

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
            custom_topic = st.text_input("Or enter specific topic:", placeholder="e.g. Master-slave JK flip-flop working")
        with c2:
            notes_lang = st.selectbox("Language Preference:", ["Hinglish (Simple Academic Notes)", "English", "Hindi (हिन्दी)"])

        final_topic = custom_topic.strip() if custom_topic.strip() else chosen_topic

        if st.button("✍️ Write on Register Pages", use_container_width=True):
            st.session_state.current_note_page = 1
            with st.spinner(f"Inscribing formal notes for {final_topic}..."):
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

        # DISPLAY COMPACT REGISTER SHEET
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
                        <span class="notebook-badge">Sheet {curr_pg} / {total_pages}</span>
                    </div>
                    <div style="font-size: 11px; color: #64748b; margin-bottom: 6px;">
                        <b>Discipline:</b> {active_subj} | <b>MLK PG College Balrampur</b>
                    </div>
                    <div class="notebook-handwritten-text">
{page_text}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ARROW CONTROLS
            ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1, 2, 1])
            with ctrl_col1:
                if st.button("‹ Prev", disabled=(curr_pg == 1), use_container_width=True):
                    st.session_state.current_note_page = max(1, curr_pg - 1)
                    st.rerun()
            with ctrl_col2:
                st.markdown(f"""
                <div style="text-align: center; color: #94A3B8; font-size: 13px; font-weight: 600; padding-top: 8px;">
                    Sheet {curr_pg} of {total_pages}
                </div>
                """, unsafe_allow_html=True)
            with ctrl_col3:
                if st.button("Next ›", disabled=(curr_pg == total_pages), use_container_width=True):
                    st.session_state.current_note_page = min(total_pages, curr_pg + 1)
                    st.rerun()

    # ================= 2. MATHS ENCYCLOPEDIA (STRICTLY MATHEMATICS ONLY) =================
    elif selected_nav == "📐 Maths Encyclopedia":
        st.markdown("#### 📐 Mathematics & Numerical Methods Reference Compendium")
        st.caption("Standard differentiation rules, L'Hopital theorem, matrix consistency, and numerical methods.")

        math_tab1, math_tab2, math_tab3, math_tab4 = st.tabs([
            "⚡ Differentiation Rules",
            "🎯 L'Hopital & Limits",
            "🔢 Matrices & Consistency",
            "🕸️ Discrete & Numerical Solvers"
        ])

        with math_tab1:
            st.markdown("##### 📌 Standard Derivatives & Calculus Rules")
            diff_formulas = [
                ("Power Rule", r"\frac{d}{dx}(x^n) = n x^{n-1}", "Derivative of $x^5 = 5x^4$"),
                ("Product Rule (u · v)", r"\frac{d}{dx}(u \cdot v) = u \frac{dv}{dx} + v \frac{du}{dx}", "Derivative of $x^2 \sin x = x^2 \cos x + 2x \sin x$"),
                ("Quotient Rule (u / v)", r"\frac{d}{dx}\left(\frac{u}{v}\right) = \frac{v \frac{du}{dx} - u \frac{dv}{dx}}{v^2}", "Derivative of $\\frac{\\sin x}{x} = \\frac{x \\cos x - \\sin x}{x^2}$"),
                ("Chain Rule", r"\frac{d}{dx}[f(g(x))] = f'(g(x)) \cdot g'(x)", "Derivative of $\sin(x^3) = \cos(x^3) \cdot 3x^2$"),
                ("Exponential Functions", r"\frac{d}{dx}(e^{ax}) = a e^{ax}, \quad \frac{d}{dx}(a^x) = a^x \ln a", "Derivative of $e^{4x} = 4e^{4x}$"),
                ("Logarithmic Functions", r"\frac{d}{dx}(\ln x) = \frac{1}{x}, \quad \frac{d}{dx}(\log_a x) = \frac{1}{x \ln a}", "Derivative of $\ln(5x) = \\frac{1}{5x} \cdot 5 = \\frac{1}{x}$"),
                ("Trigonometric Derivatives", r"\frac{d}{dx}(\sin x) = \cos x, \quad \frac{d}{dx}(\cos x) = -\sin x, \quad \frac{d}{dx}(\tan x) = \sec^2 x", "Derivative of $\tan(2x) = 2\sec^2(2x)$"),
                ("Leibnitz's n-th Derivative", r"y_n = \sum_{r=0}^{n} {}^nC_r \, u_{n-r} \, v_r", "n-th derivative of $x^2 e^{ax} = a^{n-2} e^{ax}[a^2 x^2 + 2nax + n(n-1)]$")
            ]
            for name, formula, example in diff_formulas:
                with st.expander(f"🔹 {name}"):
                    st.latex(formula)
                    st.markdown(f"**Solved Example:** {example}")

        with math_tab2:
            st.markdown("##### 🎯 Indeterminate Forms & L'Hopital's Rule")
            st.latex(r"\lim_{x \to a} \frac{f(x)}{g(x)} = \lim_{x \to a} \frac{f'(x)}{g'(x)} \quad \text{if form is } \frac{0}{0} \text{ or } \frac{\infty}{\infty}")
            with st.expander("📝 Solved University Example: Evaluate lim (x -> 0) [sin(x) - x] / x^3"):
                st.markdown(r"""
                - **Step 1:** $\lim_{x \to 0} \frac{\sin x - x}{x^3} \implies \frac{0}{0}$.
                - **Step 2 (Differentiating):** $\lim_{x \to 0} \frac{\cos x - 1}{3x^2} \implies \frac{0}{0}$.
                - **Step 3 (Second L'Hopital):** $\lim_{x \to 0} \frac{-\sin x}{6x} = -\frac{1}{6} \cdot 1 = \mathbf{-\frac{1}{6}}$.
                """)

        with math_tab3:
            st.markdown("##### 🔢 Matrices, Rank & System of Equations (AX = B)")
            st.markdown(r"""
            - **Rouche-Capelli Criterion:**
              1. $Rank(A) = Rank(A|B) = n \implies$ **Unique Solution** (Consistent).
              2. $Rank(A) = Rank(A|B) < n \implies$ **Infinitely Many Solutions** (Consistent).
              3. $Rank(A) \neq Rank(A|B) \implies$ **Inconsistent (No Solution)**.
            - **Cayley-Hamilton Theorem:** Every square matrix satisfies its characteristic polynomial $|A - \lambda I| = 0$.
            """)

        with math_tab4:
            st.markdown("##### 🕸️ Discrete Mathematics & Numerical Methods")
            st.markdown("""
            <div class="formula-card">
                <b>Handshaking Theorem:</b> $\sum_{v \in V} \deg(v) = 2E$ (Sum of degrees equals twice the edges).
            </div>
            <div class="formula-card">
                <b>Newton-Raphson Method:</b> $x_{n+1} = x_n - \\frac{f(x_n)}{f'(x_n)}$ (Quadratic convergence, Order = 2).
            </div>
            """, unsafe_allow_html=True)

    # ================= 2. CSA CIRCUIT MATRIX (STRICTLY CSA ONLY) =================
    elif selected_nav == "🖥️ CSA Circuit Matrix":
        st.markdown("#### 🖥️ CSA Digital Logic & Microprocessor Architecture")
        with st.expander("⚡ Half Adder & Full Adder Architecture"):
            st.latex(r"Sum = A \oplus B \oplus C_{in}, \quad Carry = AB + C_{in}(A \oplus B)")
            st.write("Full Adder can be realized using 2 Half Adders and 1 OR Gate.")
        with st.expander("⚙️ Pipelining & Memory Mapping"):
            st.latex(r"Speedup = \frac{n \cdot k}{k + n - 1}")
            st.write("Address division: Tag | Line Index | Word Offset")

    # ================= 3. SYLLABUS EXPLORER =================
    elif selected_nav == "📖 Syllabus Explorer":
        st.markdown(f"#### 📚 Syllabus Blueprint — {active_subj}")
        if active_subj == "🐍 Python Programming":
            st.info("Module 1: Basics & Bytecode | Module 2: Control Flow & Loops | Module 3: Functions & Scopes | Module 4: Data Structures | Module 5: OOPs | Module 6: Files & JSON")
        elif active_subj == "🖥️ Computer System Architecture":
            st.info("Unit 1: Number Systems | Unit 2: Logic Gates & Adders | Unit 3: Flip-Flops & Registers | Unit 4: CPU Architecture | Unit 5: Memory Hierarchy | Unit 6: I/O Organization")
        else:
            st.info("Unit 1: Set Theory & POSET | Unit 2: Propositional Logic | Unit 3: Matrices & Rank | Unit 4: Graph Theory | Unit 5: Calculus & Limits | Unit 6: Numerical Methods")

    # ================= 4. EXAM ENGINE =================
    elif selected_nav == "🎯 Exam Engine":
        st.markdown(f"#### 🎯 Examination Simulator — {active_subj}")
        c1, c2 = st.columns([2, 1])
        with c1:
            exam_topic = st.text_input("Examination Topic Scope:", placeholder="e.g. Cache Mapping / L'Hopital Rule")
        with c2:
            exam_lang = st.selectbox("Language Mode:", ["English", "Hinglish", "Hindi (हिन्दी)"])

        if st.button("⚡ Generate University Test Paper", use_container_width=True):
            with st.spinner("Compiling academic examination paper..."):
                prompt = f"Create a 15-mark university exam paper for '{exam_topic if exam_topic else 'Comprehensive Syllabus'}' in {active_subj}."
                st.session_state.exam_paper = get_ai_response(prompt, forced_language=exam_lang, current_subject=active_subj)

        if "exam_paper" in st.session_state:
            st.markdown(f"""
            <div class="formal-panel">
                <div style="font-size: 15px; font-weight: 700; color: #60A5FA; margin-bottom: 8px;">Question Paper:</div>
                {st.session_state.exam_paper}
            </div>
            """, unsafe_allow_html=True)

            user_ans = st.text_area("Student Solution (Type here):", height=120)
            uploaded_ans = st.file_uploader("Or Upload Answer Sheet Photo:", type=["png", "jpg", "jpeg"])
            pil_img = Image.open(uploaded_ans) if uploaded_ans else None

            if st.button("🚀 Submit For Professor Evaluation", use_container_width=True):
                if not user_ans.strip() and not pil_img:
                    st.warning("Please type your answer or upload a photo.")
                else:
                    with st.spinner("Academic evaluator grading paper..."):
                        scorecard = get_ai_response("Grade this student paper out of 15 with detailed academic breakdown.", image_input=pil_img, current_subject=active_subj)
                        st.markdown(f"""
                        <div class="formal-panel" style="border-left: 4px solid #10B981;">
                            <div style="font-size: 15px; font-weight: 700; color: #10B981; margin-bottom: 6px;">Evaluation Scorecard:</div>
                            {scorecard}
                        </div>
                        """, unsafe_allow_html=True)

    # ================= 5. PROJECTS LAB =================
    elif selected_nav == "🔬 Projects Lab":
        st.markdown(f"#### 🔬 Academic Capstone Projects — {active_subj}")
        if active_subj == "🐍 Python Programming":
            projs = ["Student Record Management (SQLite)", "Banking System (OOP Architecture)", "Automated Billing Portal"]
        elif active_subj == "🖥️ Computer System Architecture":
            projs = ["Full Adder Ripple Carry Simulator", "4-Bit ALU Software Engine", "Direct Mapped Cache Simulator"]
        else:
            projs = ["Newton-Raphson Equation Solver", "Matrix Rank Calculator", "Dijkstra Shortest Path Engine"]

        selected_proj = st.selectbox("Select Project Blueprint:", projs)
        if st.button("⚡ Generate Architecture & Source Code", use_container_width=True):
            with st.spinner("Generating formal blueprint..."):
                res = get_ai_response(f"Provide complete working code and documentation for project: '{selected_proj}' in {active_subj}.", current_subject=active_subj)
                st.markdown(f'<div class="formal-panel">{res}</div>', unsafe_allow_html=True)

    # ================= 6. AI MENTOR =================
    elif selected_nav == "🤖 AI Academic Mentor":
        st.markdown(f"#### 🤖 Academic Doubt Clearance Portal — {active_subj}")
        doubt_text = st.text_area("Enter your academic doubt or code query:", height=110)
        uploaded_doubt = st.file_uploader("Or upload screenshot / question page photo:", type=["png", "jpg", "jpeg"])
        doubt_img = Image.open(uploaded_doubt) if uploaded_doubt else None

        if st.button("⚡ Request Faculty Explanation", use_container_width=True):
            if not doubt_text.strip() and not doubt_img:
                st.warning("Please enter your question or upload an image.")
            else:
                with st.spinner("Professor formulating step-by-step explanation..."):
                    sol = get_ai_response(doubt_text, image_input=doubt_img, current_subject=active_subj)
                    st.markdown(f'<div class="formal-panel" style="border-left: 4px solid #3B82F6;">{sol}</div>', unsafe_allow_html=True)

    # ================= 7. COLAB NOTEBOOK SANDBOX (STRICTLY PYTHON ONLY) =================
    elif selected_nav == "💻 Colab Notebook & Sandbox" and active_subj == "🐍 Python Programming":
        st.markdown("#### 💻 Interactive Colab Notebook & Sandbox Environment // Python Only")
        
        # Colab Action Toolbar
        tb_col1, tb_col2, tb_col3 = st.columns([1.2, 1.2, 2])
        with tb_col1:
            if st.button("➕ Add Code Cell", use_container_width=True):
                new_id = len(st.session_state.notebook_cells) + 1
                st.session_state.notebook_cells.append({
                    "id": new_id,
                    "code": "# Python Code Cell\n",
                    "output": "",
                    "error": ""
                })
                st.rerun()
        with tb_col2:
            if st.button("🗑️ Clear Outputs", use_container_width=True):
                for cell in st.session_state.notebook_cells:
                    cell["output"] = ""
                    cell["error"] = ""
                st.rerun()
        with tb_col3:
            st.caption("Standard Python 3.10 Kernel • PEP-8 4-Space Indentation Active")

        st.markdown("---")

        # RENDER NOTEBOOK CELLS (INTERACTIVE INPUT WORKING)
        for idx, cell in enumerate(st.session_state.notebook_cells):
            cell_id = cell["id"]
            
            st.markdown(f"""
            <div class="colab-cell-box">
                <div style="display:flex; justify-content:space-between; color:#94A3B8; font-size:12px; font-family:'JetBrains Mono'; margin-bottom:6px;">
                    <span><b>[ {idx + 1} ]</b> In [ ]: Code Cell</span>
                    <span>PYTHON_EXECUTION_NODE</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            c_editor, c_btn = st.columns([8.8, 1.4])
            with c_editor:
                updated_code = st.text_area(
                    f"Code Cell Editor {cell_id}",
                    value=cell["code"],
                    height=130,
                    key=f"cell_code_val_{cell_id}",
                    label_visibility="collapsed"
                )
                cell["code"] = updated_code
            with c_btn:
                st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
                run_cell = st.button("▶ Run", key=f"run_btn_{cell_id}", use_container_width=True)
                copilot_cell = st.button("⚡ Assist", key=f"copilot_{cell_id}", use_container_width=True)

            # Execution Logic
            if run_cell:
                buf = io.StringIO()
                try:
                    with contextlib.redirect_stdout(buf):
                        exec(cell["code"], {})
                    cell["output"] = buf.getvalue() if buf.getvalue() else "[Execution successful: zero return value]"
                    cell["error"] = ""
                except Exception as ex:
                    cell["output"] = ""
                    cell["error"] = str(ex)

            # AI Assist Logic
            if copilot_cell:
                with st.spinner("AI evaluating cell code..."):
                    assist_prompt = f"Analyze this Python code cell and suggest 1-line optimization or fix without slang:\n```python\n{cell['code']}\n```"
                    cell["output"] = "[Faculty Suggestion]:\n" + get_ai_response(assist_prompt, current_subject="Python")
                    cell["error"] = ""

            # Output Render
            if cell["output"]:
                st.markdown(f"""
                <div style="background:#070C18; border-left:3px solid #10B981; padding:10px 14px; border-radius:4px; font-family:'JetBrains Mono'; font-size:13px; color:#F8FAFC; margin-bottom:12px;">
                    <span style="color:#10B981; font-size:11px; display:block; margin-bottom:4px;">Out [ {idx + 1} ]:</span>
                    {cell['output']}
                </div>
                """, unsafe_allow_html=True)

            if cell["error"]:
                st.markdown(f"""
                <div style="background:#070C18; border-left:3px solid #EF4444; padding:10px 14px; border-radius:4px; font-family:'JetBrains Mono'; font-size:13px; color:#FCA5A5; margin-bottom:12px;">
                    <span style="color:#EF4444; font-size:11px; display:block; margin-bottom:4px;">Runtime Error:</span>
                    {cell['error']}
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("🛠️ Auto-Fix Error with Faculty AI", key=f"fix_btn_{cell_id}"):
                    with st.spinner("Faculty AI fixing error..."):
                        fix_res = get_ai_response(f"Fix this Python code error:\nCode:\n{cell['code']}\nError:\n{cell['error']}\nProvide the working code respectfully.", current_subject="Python")
                        st.info(fix_res)
