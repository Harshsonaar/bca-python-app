import streamlit as st
from groq import Groq
import google.generativeai as genai
import io
import contextlib
from PIL import Image

st.set_page_config(
    page_title="BCA Academic Suite | Harsh Raj Soni",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session States
if "system_booted" not in st.session_state:
    st.session_state.system_booted = False

if "selected_subject" not in st.session_state:
    st.session_state.selected_subject = "🐍 Python Programming"

if "generated_gallery_sheets" not in st.session_state:
    st.session_state.generated_gallery_sheets = []

if "active_sheet_index" not in st.session_state:
    st.session_state.active_sheet_index = None

# Colab Notebook Multi-Cell Storage (Python Only)
if "notebook_cells" not in st.session_state:
    st.session_state.notebook_cells = [
        {
            "id": 1,
            "code": "# Python Cell 1: Verification & Environment\ndeveloper_name = 'Harsh Raj Soni'\ninstitution = 'MLK PG College, Balrampur'\nprint(f'Academic Portal Active | Developer: {developer_name} [{institution}]')",
            "output": "",
            "error": ""
        },
        {
            "id": 2,
            "code": "# Python Cell 2: Numerical Logic\ndef is_prime(number):\n    if number <= 1:\n        return False\n    for divisor in range(2, int(number**0.5) + 1):\n        if number % divisor == 0:\n            return False\n    return True\n\nval = 37\nprint(f'Is {val} prime?:', is_prime(val))",
            "output": "",
            "error": ""
        }
    ]

# ================= EXECUTIVE STYLING & REAL REGISTER CANVAS CSS =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Caveat:wght@600;700&family=Patrick+Hand&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    .stApp {
        background: radial-gradient(circle at 50% 0%, #0F172A 0%, #080D1A 60%, #020617 100%) !important;
        color: #F8FAFC;
    }

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
        padding-top: 0.8rem !important;
        padding-bottom: 5rem !important;
        max-width: 1100px !important;
    }

    .formal-top-banner {
        background: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 12px 20px;
        backdrop-filter: blur(20px);
        margin-bottom: 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }
    .formal-author-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(37, 99, 235, 0.15);
        border: 1px solid rgba(59, 130, 246, 0.5);
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        color: #60A5FA;
        box-shadow: 0 0 16px rgba(37, 99, 235, 0.3);
    }

    div[data-testid="stExpander"] {
        background: rgba(15, 23, 42, 0.85) !important;
        border: 1.5px solid #3B82F6 !important;
        border-radius: 14px !important;
        box-shadow: 0 0 18px rgba(37, 99, 235, 0.3), 0 8px 24px rgba(0, 0, 0, 0.5) !important;
        margin-bottom: 14px !important;
    }

    div[data-testid="stRadio"] {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 6px 10px !important;
        border-radius: 35px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45) !important;
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

    .stButton>button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 8px !important;
        padding: 6px 16px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5) !important;
    }

    /* REAL NOTEBOOK VECTOR SHEET (CRISP, NON-BLURRY, DYNAMIC FIT) */
    .real-notebook-sheet {
        background-color: #fcfbf7 !important;
        background-image: 
            linear-gradient(90deg, transparent 46px, #ef4444 46px, #ef4444 47.5px, transparent 47.5px),
            linear-gradient(#e2e8f0 1px, transparent 1px) !important;
        background-size: 100% 100%, 100% 30px !important;
        border-radius: 10px !important;
        padding: 22px 24px 22px 60px !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
        width: 100% !important;
        box-sizing: border-box !important;
        font-family: 'Patrick Hand', cursive !important;
        color: #1e3a8a !important;
        font-size: 18px !important;
        line-height: 30px !important;
        position: relative !important;
        margin-bottom: 14px !important;
    }

    .real-notebook-sheet::before {
        content: '' !important;
        position: absolute !important;
        top: 14px !important;
        left: 12px !important;
        width: 12px !important;
        height: 96% !important;
        background-image: radial-gradient(circle, #94a3b8 4px, transparent 5px) !important;
        background-size: 12px 30px !important;
        background-repeat: repeat-y !important;
    }

    .nb-title-h1 {
        font-family: 'Caveat', cursive !important;
        font-size: 30px !important;
        font-weight: 700 !important;
        color: #1e1b4b !important;
        background: #fdf2f8 !important;
        padding: 2px 14px !important;
        border-radius: 6px !important;
        display: inline-block !important;
        border-bottom: 2px dashed #ec4899 !important;
        margin-bottom: 6px !important;
        line-height: 32px !important;
    }

    .nb-subhead {
        font-weight: 700 !important;
        color: #0369a1 !important;
        font-size: 19px !important;
        text-decoration: underline !important;
        margin-top: 6px !important;
        display: block !important;
    }

    .nb-table {
        border-collapse: collapse !important;
        margin: 8px 0 !important;
        font-family: 'Patrick Hand', cursive !important;
        font-size: 16.5px !important;
        background: #ffffff !important;
        border: 1.5px solid #1e3a8a !important;
        width: 100% !important;
        max-width: 440px !important;
    }
    .nb-table th, .nb-table td {
        border: 1.5px solid #1e3a8a !important;
        padding: 2px 10px !important;
        text-align: center !important;
    }
    .nb-table th {
        background: #e0f2fe !important;
        color: #0369a1 !important;
    }

    .nb-keypoints-box {
        border: 2px dashed #16a34a !important;
        background: #f0fdf4 !important;
        border-radius: 12px !important;
        padding: 8px 14px !important;
        margin-top: 10px !important;
        color: #14532d !important;
        font-size: 16px !important;
        line-height: 24px !important;
    }

    /* MINI CARD PREVIEW IN GALLERY */
    .gallery-preview-card {
        border: 1.5px solid #3B82F6;
        border-radius: 8px;
        background: rgba(30, 41, 59, 0.6);
        padding: 8px 12px;
        text-align: center;
        cursor: pointer;
        transition: transform 0.2s ease;
        margin-bottom: 10px;
    }
    .gallery-preview-card:hover {
        transform: translateY(-2px);
        background: rgba(59, 130, 246, 0.25);
    }

    @media (max-width: 768px) {
        .real-notebook-sheet {
            padding: 16px 14px 20px 46px !important;
            font-size: 16.5px !important;
            line-height: 26px !important;
            background-size: 100% 100%, 100% 26px !important;
        }
        .nb-title-h1 {
            font-size: 24px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ================= UNIVERSAL AI ENGINE =================
groq_key = st.secrets.get("GROQ_API_KEY", None)
gemini_key = st.secrets.get("GEMINI_API_KEY", None)

with st.sidebar:
    st.markdown("### ⚡ AI Engine Status")
    ai_choice = st.radio("Active Engine:", ["⚡ Groq LPU (Ultra Fast)", "Google Gemini"], index=0)

    if ai_choice == "⚡ Groq LPU (Ultra Fast)":
        if not groq_key:
            groq_key = st.text_input("Groq API Key:", type="password", placeholder="gsk_...")
        if groq_key:
            st.success("● Groq LPU Active")
        else:
            st.info("console.groq.com se free key lein")
    else:
        if not gemini_key:
            gemini_key = st.text_input("Gemini API Key:", type="password")
        if gemini_key:
            genai.configure(api_key=gemini_key)
            st.success("● Gemini Multimodal Active")

    st.markdown("---")
    st.caption("⚡ Developed by **Harsh Raj Soni**")
    st.caption("🏛️ MLK PG College, Balrampur")

def execute_ai_query(system_role, user_prompt, image_input=None):
    """Executes prompt via official recommended Groq replacement models or Gemini fallback"""
    if image_input and gemini_key:
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("models/gemini-2.0-flash")
            response = model.generate_content([f"{system_role}\n\n{user_prompt}", image_input])
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            return f"Gemini Vision Error: {e}"

    if "Groq" in ai_choice and groq_key:
        client = Groq(api_key=groq_key)
        
        # ACTIVE REPLACEMENT MODELS FROM GROQ CONSOLE DEPRECATION LIST
        active_models = [
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
            "llama-3.1-8b-instant"
        ]
        
        last_err = ""
        for model_id in active_models:
            try:
                completion = client.chat.completions.create(
                    model=model_id,
                    messages=[
                        {"role": "system", "content": system_role},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.25,
                    max_tokens=2000
                )
                return completion.choices[0].message.content.strip()
            except Exception as e:
                last_err = str(e)
                continue

        if gemini_key:
            try:
                genai.configure(api_key=gemini_key)
                model = genai.GenerativeModel("models/gemini-2.0-flash")
                res = model.generate_content(f"{system_role}\n\n{user_prompt}")
                if res and res.text:
                    return res.text.strip()
            except Exception:
                pass
        return f"Engine Error: {last_err}"

    elif gemini_key:
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("models/gemini-2.0-flash")
            response = model.generate_content(f"{system_role}\n\n{user_prompt}")
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            return f"Gemini Error: {e}"

    return "⚠️ Pehle Sidebar mein Groq ya Gemini ki API Key add karein."

def generate_multi_sheets_html(topic, subject_name, notes_lang):
    system_role = (
        "You are an esteemed university professor for BCA at MLK PG College, Balrampur. "
        "Strictly maintain academic dignity. Never use slang or informal abusive words. "
        "Output EXACTLY 4 TO 5 INDIVIDUAL COMPLETE LECTURE SHEETS separated strictly by the token '===SHEET_SPLIT==='. "
        "Each sheet must be formatted in clean raw HTML matching the classmate notebook register style (Definition, Block Diagram, Truth Table if applicable, Logic Expressions, and Key Points). "
        "DO NOT USE CODE BLOCKS OR MARKDOWN TICKS (no ```html)."
    )
    user_prompt = f"""
    Create a complete 4-sheet ruled lecture register for '{topic}' in {subject_name} ({notes_lang}).

    FORMAT FOR EACH SHEET (Separate each sheet by ===SHEET_SPLIT===):
    <div class="real-notebook-sheet">
        <div class="nb-title-h1">{topic} [Part X]</div>
        <div style="font-size:12px; color:#6b7280; margin-bottom:6px;">{subject_name} • MLK PG College Balrampur</div>

        <span class="nb-subhead">1. Definition & Core Concept :</span>
        <p style="margin: 2px 0 8px 0;">[Clear 2-3 lines explanation in {notes_lang}]</p>

        <span class="nb-subhead">2. Truth Table / Formulation / Key Rules :</span>
        <table class="nb-table">
            <tr><th>Input A</th><th>Input B</th><th>Output</th><th>Status</th></tr>
            <tr><td>0</td><td>0</td><td>0</td><td>Normal</td></tr>
            <tr><td>0</td><td>1</td><td>1</td><td>Active</td></tr>
            <tr><td>1</td><td>0</td><td>1</td><td>Active</td></tr>
            <tr><td>1</td><td>1</td><td>1</td><td>Max</td></tr>
        </table>

        <span class="nb-subhead">3. Logic Expressions / Step-by-Step Working :</span>
        <p style="margin: 2px 0 8px 0;">
            • Step 1: Core working logic and data flow<br>
            • Step 2: Key mathematical or architectural deduction<br>
            • Step 3: Practical exam consideration
        </p>

        <div class="nb-keypoints-box">
            <b>✳ Key Exam Points :</b><br>
            • Crucial university examination theorem / takeaway<br>
            • Examiner evaluation note
        </div>
        <div style="font-size:11px; color:#9ca3af; text-align:right; margin-top:6px;">Harsh Raj Soni • BCA Ecosystem</div>
    </div>
    """
    raw_res = execute_ai_query(system_role, user_prompt)
    clean_text = raw_res.replace("```html", "").replace("```", "").strip()
    sheets = [s.strip() for s in clean_text.split("===SHEET_SPLIT===") if s.strip()]
    return sheets if sheets else [clean_text]

# ================= 0. INTRO SCREEN =================
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
            <div>• Real Ruled Handwriting Register Sheet Engine (Auto-Fit)</div>
            <div>• Photos Style Gallery Grid with Direct Tap Zoom View</div>
            <div>• Full Python, CSA & Discrete Mathematics Compendium</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        if st.button("Enter Portal", use_container_width=True):
            st.session_state.system_booted = True
            st.rerun()

else:
    # Top Executive Bar
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
            Developer: Harsh Raj Soni
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Subject Selector Tile
    curr_sub = st.session_state.selected_subject
    with st.expander(f"Active Stream: {curr_sub} (Tap to Switch)", expanded=False):
        sub_list = [
            "🐍 Python Programming",
            "🖥️ Computer System Architecture",
            "📐 Mathematics & Numerical Methods"
        ]
        for s in sub_list:
            is_active = (s == curr_sub)
            label = f"✔ {s}" if is_active else f"➔ Switch to {s}"
            if st.button(label, key=f"switch_sub_{s}", use_container_width=True, type="primary" if is_active else "secondary"):
                st.session_state.selected_subject = s
                st.session_state.generated_gallery_sheets = []
                st.session_state.active_sheet_index = None
                st.rerun()

    active_subj = st.session_state.selected_subject

    # Navigation Dock
    nav_options = [
        "📝 Notes Gallery",
        "📖 Syllabus",
        "🎯 Exam Engine",
        "🔬 Projects",
        "🤖 AI Mentor"
    ]
    if active_subj == "🐍 Python Programming":
        nav_options.append("💻 Sandbox")
    elif active_subj == "📐 Mathematics & Numerical Methods":
        nav_options.insert(1, "📐 Maths Menu")
    elif active_subj == "🖥️ Computer System Architecture":
        nav_options.insert(1, "🖥️ CSA Menu")

    selected_nav = st.radio(
        label="Navigation Section",
        options=nav_options,
        horizontal=True,
        index=0
    )

    # ================= 1. NOTES GALLERY (GRID VIEW + ZOOM TAP) =================
    if selected_nav == "📝 Notes Gallery":
        st.markdown(f"#### 📖 Lecture Notes Register Gallery — {active_subj}")
        st.caption("Classmate ruled paper layout with tables, formulas, and key points in a mobile gallery grid.")

        if active_subj == "🐍 Python Programming":
            suggested_topics = [
                "Python Architecture, Bytecode & Memory Management",
                "Control Flow, Loops, For-Else Logic & Prime Verification",
                "Functions, Scopes, LEGB Resolution & Lambda Expressions",
                "Data Structures: Lists, Tuples, Dictionaries & Sets",
                "Object Oriented Programming: Encapsulation & Inheritance",
                "File Handling, Context Managers & Exception Hierarchy"
            ]
        elif active_subj == "🖥️ Computer System Architecture":
            suggested_topics = [
                "Full Adder Circuit, Logic Gates & Truth Table",
                "Half Adder & Full Adder Design using 2 HA and 1 OR Gate",
                "Number Systems, Complements & Binary Operations",
                "K-Map 4-Variable Minimization & Grouping Rules",
                "Flip-Flops, Master-Slave JK & Race-Around Condition",
                "Instruction Cycle Phases & Cache Memory Mapping"
            ]
        else:
            suggested_topics = [
                "L'Hopital's Rule for Indeterminate Forms with Solved Limit",
                "Equivalence Relations Proof & POSET Hasse Diagrams",
                "Matrix Rank, Echelon Forms & Rouche-Capelli Consistency",
                "Eigenvalues, Eigenvectors & Cayley-Hamilton Theorem",
                "Leibnitz Theorem for n-th Derivatives & Formula Matrix",
                "Newton-Raphson Method & Numerical Convergence"
            ]

        c1, c2 = st.columns([2.5, 1])
        with c1:
            chosen_topic = st.selectbox("Topic:", suggested_topics)
            custom_topic = st.text_input("Custom query (optional):", placeholder="e.g. Full Adder circuit diagram and truth table")
        with c2:
            notes_lang = st.selectbox("Language:", ["Hinglish", "English", "Hindi"])

        final_topic = custom_topic.strip() if custom_topic.strip() else chosen_topic

        if st.button("Generate Notes", use_container_width=True):
            st.session_state.active_sheet_index = None
            with st.spinner(f"Writing lecture sheets for {final_topic}..."):
                st.session_state.generated_gallery_sheets = generate_multi_sheets_html(final_topic, active_subj, notes_lang)

        # GALLERY & MODAL VIEW LOGIC
        if st.session_state.generated_gallery_sheets:
            sheets = st.session_state.generated_gallery_sheets
            total_sheets = len(sheets)

            # SINGLE SHEET ZOOM / FULL VIEW
            if st.session_state.active_sheet_index is not None:
                cur_i = st.session_state.active_sheet_index
                st.markdown(f"##### 🔍 Sheet {cur_i + 1} of {total_sheets}")

                # Display the real notebook sheet
                st.markdown(sheets[cur_i], unsafe_allow_html=True)

                nav_c1, nav_c2, nav_c3 = st.columns([1.5, 2, 1.5])
                with nav_c1:
                    if st.button("‹ Previous Sheet", disabled=(cur_i == 0), use_container_width=True):
                        st.session_state.active_sheet_index = max(0, cur_i - 1)
                        st.rerun()
                with nav_c2:
                    if st.button("📁 Close & Back to Gallery Grid", use_container_width=True):
                        st.session_state.active_sheet_index = None
                        st.rerun()
                with nav_c3:
                    if st.button("Next Sheet ›", disabled=(cur_i == total_sheets - 1), use_container_width=True):
                        st.session_state.active_sheet_index = min(total_sheets - 1, cur_i + 1)
                        st.rerun()

            # GALLERY GRID VIEW
            else:
                st.markdown(f"##### 📸 Register Sheets Gallery ({total_sheets} Sheets)")
                st.caption("Kisi bhi sheet par tap karein full-size padhne ke liye:")

                grid_cols = st.columns(3)
                for idx, sheet_code in enumerate(sheets):
                    with grid_cols[idx % 3]:
                        if st.button(f"📄 Sheet {idx + 1} (Tap to Open)", key=f"sheet_btn_{idx}", use_container_width=True):
                            st.session_state.active_sheet_index = idx
                            st.rerun()
                        # Compact card thumbnail
                        st.markdown(f"""
                        <div style="border:1px solid #334155; border-radius:8px; padding:10px; background:#0F172A; text-align:center; margin-bottom:12px;">
                            <span style="font-size:14px; color:#60A5FA; font-weight:700;">Sheet #{idx + 1}</span><br>
                            <span style="font-size:11px; color:#94A3B8;">Ruled Lecture Register</span>
                        </div>
                        """, unsafe_allow_html=True)

    # ================= 2. MATHS ENCYCLOPEDIA =================
    elif selected_nav == "📐 Maths Menu":
        st.markdown("#### 📐 Mathematics Formula Menu")
        with st.expander("⚡ Differentiation Rules"):
            st.latex(r"\frac{d}{dx}(x^n) = n x^{n-1}, \quad \frac{d}{dx}(u \cdot v) = u v' + v u'")
            st.latex(r"\frac{d}{dx}\left(\frac{u}{v}\right) = \frac{v u' - u v'}{v^2}")
        with st.expander("🎯 L'Hopital's Rule"):
            st.latex(r"\lim_{x \to a} \frac{f(x)}{g(x)} = \lim_{x \to a} \frac{f'(x)}{g'(x)} \quad \left(\frac{0}{0} \text{ or } \frac{\infty}{\infty}\right)")
        with st.expander("🔢 Matrix Rank & Consistency"):
            st.write("Rank(A) = Rank(A|B) = n implies Unique Solution.")
            st.write("Rank(A) = Rank(A|B) < n implies Infinite Solutions.")

    # ================= 3. CSA CIRCUIT MENU =================
    elif selected_nav == "🖥️ CSA Menu":
        st.markdown("#### 🖥️ CSA Digital Logic & Architecture")
        with st.expander("⚡ Half & Full Adder Equations"):
            st.latex(r"Sum = A \oplus B \oplus C_{in}, \quad Carry = AB + C_{in}(A \oplus B)")
        with st.expander("⚙️ Pipeline Speedup & Cache"):
            st.latex(r"Speedup = \frac{n \cdot k}{k + n - 1}")

    # ================= 4. SYLLABUS EXPLORER =================
    elif selected_nav == "📖 Syllabus":
        st.markdown(f"#### 📚 Curriculum Breakdown — {active_subj}")
        if active_subj == "🐍 Python Programming":
            st.info("Modules: 1. Architecture | 2. Control Flow | 3. Functions | 4. Data Structures | 5. OOPs | 6. File Handling")
        elif active_subj == "🖥️ Computer System Architecture":
            st.info("Units: 1. Number Systems | 2. Digital Logic | 3. Flip-Flops | 4. CPU & Instructions | 5. Memory | 6. I/O")
        else:
            st.info("Units: 1. Set Theory | 2. Logic | 3. Matrices & Rank | 4. Graphs | 5. Calculus | 6. Numerical Methods")

    # ================= 5. EXAM ENGINE =================
    elif selected_nav == "🎯 Exam Engine":
        st.markdown(f"#### 🎯 Examination Simulator — {active_subj}")
        c1, c2 = st.columns([2, 1])
        with c1:
            exam_topic = st.text_input("Topic Scope:", placeholder="e.g. Cache Mapping / L'Hopital Rule")
        with c2:
            exam_lang = st.selectbox("Exam Language:", ["English", "Hinglish", "Hindi"])

        if st.button("Generate Paper", use_container_width=True):
            sys_prompt = "You are a university examination creator. Provide a structured 15-mark test with marks distribution."
            st.session_state.ex_res = execute_ai_query(sys_prompt, f"Create a 15-mark university exam test on '{exam_topic if exam_topic else 'Full Syllabus'}' for {active_subj} in {exam_lang}.")

        if "ex_res" in st.session_state:
            st.markdown(st.session_state.ex_res)

            user_sol = st.text_area("Your Solution:", height=100)
            uploaded_paper = st.file_uploader("Upload Solution Photo (Optional):", type=["png", "jpg", "jpeg"])
            pil_p = Image.open(uploaded_paper) if uploaded_paper else None

            if st.button("Evaluate Paper", use_container_width=True):
                if not user_sol.strip() and not pil_p:
                    st.warning("Please type solution or upload photo.")
                else:
                    with st.spinner("Grading paper..."):
                        scorecard = execute_ai_query(
                            "You are a strict BCA professor. Grade the student's solution out of 15 with score breakdown.",
                            user_sol,
                            image_input=pil_p
                        )
                        st.info(scorecard)

    # ================= 6. PROJECTS LAB =================
    elif selected_nav == "🔬 Projects":
        st.markdown(f"#### 🔬 Academic Capstone Projects — {active_subj}")
        if active_subj == "🐍 Python Programming":
            projs = ["Student Management (SQLite)", "Banking Simulator (OOP)", "Billing Engine"]
        elif active_subj == "🖥️ Computer System Architecture":
            projs = ["Adder Simulator", "4-Bit ALU", "Cache Simulator"]
        else:
            projs = ["Newton-Raphson Solver", "Matrix Rank Calculator", "Dijkstra Engine"]

        sel_p = st.selectbox("Select Project:", projs)
        if st.button("Build Blueprint", use_container_width=True):
            with st.spinner("Generating code..."):
                sys_prompt = "You are an engineering mentor. Provide working code and step-by-step documentation."
                res = execute_ai_query(sys_prompt, f"Provide complete working code and documentation for project: '{sel_p}' in {active_subj}.")
                st.markdown(res)

    # ================= 7. AI MENTOR =================
    elif selected_nav == "🤖 AI Mentor":
        st.markdown(f"#### 🤖 Doubt Clearance — {active_subj}")
        q = st.text_input("Ask Question / Paste Error:")
        q_img = st.file_uploader("Upload Question Photo (Optional):", type=["png", "jpg", "jpeg"])
        pil_q = Image.open(q_img) if q_img else None

        if st.button("Submit Doubt", use_container_width=True):
            if q.strip() or pil_q:
                with st.spinner("Analyzing doubt..."):
                    sys_prompt = "You are a helpful BCA professor. Explain step-by-step with practical clarity."
                    st.write(execute_ai_query(sys_prompt, q, image_input=pil_q))
            else:
                st.warning("Please enter text or upload image.")

    # ================= 8. COLAB SANDBOX (PYTHON ONLY) =================
    elif selected_nav == "💻 Sandbox" and active_subj == "🐍 Python Programming":
        st.markdown("#### 💻 Colab Notebook // Python Only")

        tb1, tb2 = st.columns([1, 1])
        with tb1:
            if st.button("Add Cell", use_container_width=True):
                new_id = len(st.session_state.notebook_cells) + 1
                st.session_state.notebook_cells.append({
                    "id": new_id,
                    "code": "# Python Cell\n",
                    "output": "",
                    "error": ""
                })
                st.rerun()
        with tb2:
            if st.button("Clear Outputs", use_container_width=True):
                for cell in st.session_state.notebook_cells:
                    cell["output"] = ""
                    cell["error"] = ""
                st.rerun()

        for idx, cell in enumerate(st.session_state.notebook_cells):
            st.markdown(f"**[ {idx + 1} ]** In [ ]:")
            c_ed, c_act = st.columns([8.5, 1.5])
            with c_ed:
                cell["code"] = st.text_area(f"Cell {cell['id']}", value=cell["code"], height=120, label_visibility="collapsed")
            with c_act:
                run_btn = st.button("Run", key=f"run_{cell['id']}", use_container_width=True)
                assist_btn = st.button("Assist", key=f"as_{cell['id']}", use_container_width=True)

            if run_btn:
                buf = io.StringIO()
                try:
                    with contextlib.redirect_stdout(buf):
                        exec(cell["code"], {})
                    cell["output"] = buf.getvalue() if buf.getvalue() else "[Finished with zero return output]"
                    cell["error"] = ""
                except Exception as ex:
                    cell["output"] = ""
                    cell["error"] = str(ex)

            if assist_btn:
                with st.spinner("AI checking cell..."):
                    sys_prompt = "Optimize this python code cleanly and suggest best practices."
                    cell["output"] = execute_ai_query(sys_prompt, f"Analyze:\n{cell['code']}")
                    cell["error"] = ""

            if cell["output"]:
                st.code(cell["output"])
            if cell["error"]:
                st.error(cell["error"])
                if st.button("Auto-Fix", key=f"afix_{cell['id']}"):
                    sys_prompt = "Fix this python error and output 100% working code."
                    st.info(execute_ai_query(sys_prompt, f"Fix this code error:\n{cell['code']}\nError: {cell['error']}"))
