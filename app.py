import streamlit as st
from openai import OpenAI
import google.generativeai as genai
import io
import contextlib

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

if "notebook_rendered_html" not in st.session_state:
    st.session_state.notebook_rendered_html = ""

# Colab Notebook Multi-Cell Storage (Python Only)
if "notebook_cells" not in st.session_state:
    st.session_state.notebook_cells = [
        {
            "id": 1,
            "code": "# Python Cell 1: Verification\ndeveloper_name = 'Harsh Raj Soni'\ninstitution = 'MLK PG College, Balrampur'\nprint(f'Portal Active | Developer: {developer_name} [{institution}]')",
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

# ================= EXECUTIVE STYLING & REAL HANDWRITTEN PAPER CSS =================
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
        max-width: 1080px !important;
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

    /* REAL NOTEBOOK VECTOR SHEET (CRISP, NON-BLURRY, DYNAMIC HEIGHT) */
    .real-notebook-sheet {
        background-color: #fcfbf7 !important;
        background-image: 
            linear-gradient(90deg, transparent 46px, #ef4444 46px, #ef4444 47.5px, transparent 47.5px),
            linear-gradient(#e5e7eb 1px, transparent 1px) !important;
        background-size: 100% 100%, 100% 32px !important;
        border-radius: 10px !important;
        padding: 24px 28px 24px 62px !important;
        border: 1px solid #d1d5db !important;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.55) !important;
        width: 100% !important;
        max-width: 680px !important;
        margin: 0 auto 20px auto !important;
        box-sizing: border-box !important;
        font-family: 'Patrick Hand', cursive !important;
        color: #1e3a8a !important;
        font-size: 18px !important;
        line-height: 32px !important;
        position: relative !important;
    }

    .real-notebook-sheet::before {
        content: '' !important;
        position: absolute !important;
        top: 14px !important;
        left: 14px !important;
        width: 12px !important;
        height: 96% !important;
        background-image: radial-gradient(circle, #9ca3af 4px, transparent 5px) !important;
        background-size: 12px 32px !important;
        background-repeat: repeat-y !important;
    }

    .nb-title-h1 {
        font-family: 'Caveat', cursive !important;
        font-size: 32px !important;
        font-weight: 700 !important;
        color: #1e1b4b !important;
        background: #fdf2f8 !important;
        padding: 2px 14px !important;
        border-radius: 6px !important;
        display: inline-block !important;
        border-bottom: 2px dashed #ec4899 !important;
        margin-bottom: 8px !important;
        line-height: 34px !important;
    }

    .nb-subhead {
        font-weight: 700 !important;
        color: #0369a1 !important;
        font-size: 20px !important;
        text-decoration: underline !important;
        margin-top: 6px !important;
        display: block !important;
    }

    .nb-table {
        border-collapse: collapse !important;
        margin: 8px 0 !important;
        font-family: 'Patrick Hand', cursive !important;
        font-size: 17px !important;
        background: #ffffff !important;
        border: 1.5px solid #1e3a8a !important;
        width: auto !important;
    }
    .nb-table th, .nb-table td {
        border: 1.5px solid #1e3a8a !important;
        padding: 2px 14px !important;
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
        padding: 8px 16px !important;
        margin-top: 10px !important;
        color: #14532d !important;
        font-size: 17px !important;
    }

    @media (max-width: 768px) {
        .real-notebook-sheet {
            padding: 16px 14px 20px 48px !important;
            font-size: 16.5px !important;
            line-height: 28px !important;
            background-size: 100% 100%, 100% 28px !important;
        }
        .nb-title-h1 {
            font-size: 26px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ================= UNIVERSAL AI ENGINE (CHATGPT & GEMINI) =================
openai_key = st.secrets.get("OPENAI_API_KEY", None)
gemini_key = st.secrets.get("GEMINI_API_KEY", None)

with st.sidebar:
    st.markdown("### 🏛️ Academic AI Engine")
    ai_choice = st.radio("Choose AI Engine:", ["OpenAI (ChatGPT)", "Google Gemini"], index=0)
    
    if ai_choice == "OpenAI (ChatGPT)":
        if not openai_key:
            openai_key = st.text_input("OpenAI API Key:", type="password", placeholder="sk-...")
        if openai_key:
            st.success("● ChatGPT (GPT-4o-mini) Active")
        else:
            st.warning("Please provide OpenAI API Key")
    else:
        if not gemini_key:
            gemini_key = st.text_input("Gemini API Key:", type="password")
        if gemini_key:
            genai.configure(api_key=gemini_key)
            st.success("● Gemini Active")
            
    st.markdown("---")
    st.caption("⚡ Developed by **Harsh Raj Soni**")
    st.caption("🏛️ MLK PG College, Balrampur")

def execute_ai_query(system_role, user_prompt):
    """Executes prompt via ChatGPT (default) or Gemini fallback"""
    if ai_choice == "OpenAI (ChatGPT)" and openai_key:
        try:
            client = OpenAI(api_key=openai_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_role},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.25,
                max_tokens=1500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"OpenAI Error: {e}"

    elif gemini_key:
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("models/gemini-2.0-flash")
            response = model.generate_content(f"{system_role}\n\n{user_prompt}")
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            return f"Gemini Error: {e}"
            
    return "⚠️ Pehle Sidebar mein OpenAI ya Gemini ki API Key add karein."

def get_handwritten_notes_html(topic, subject_name, notes_lang):
    system_role = f"You are an expert professor for BCA at MLK PG College. Output ONLY clean raw HTML without markdown hashes or ```html blocks."
    user_prompt = f"""
    Create a clean handwritten lecture note on '{topic}' for {subject_name} in {notes_lang}.
    
    OUTPUT FORMAT (EXACT HTML ONLY):
    <div class="real-notebook-sheet">
        <div class="nb-title-h1">{topic}</div>
        <div style="font-size:12px; color:#6b7280; margin-bottom:8px;">{subject_name} • MLK PG College Balrampur</div>

        <span class="nb-subhead">1. Definition & Core Concept :</span>
        <p style="margin: 4px 0 10px 0;">[Explain in 2-3 concise lines]</p>

        <span class="nb-subhead">2. Key Formulation / Rules / Truth Table :</span>
        [Provide either a clean <table class="nb-table"> or 3-4 clean logic lines]

        <span class="nb-subhead">3. Step-by-Step Logic / Working :</span>
        <p style="margin: 4px 0 10px 0;">• Step 1 with clear explanation<br>• Step 2 with clear explanation<br>• Step 3 with clear explanation</p>

        <div class="nb-keypoints-box">
            <b>✳ Key Exam Points :</b><br>
            • Most important university exam rule<br>
            • Crucial takeaway
        </div>
        <div style="font-size:11px; color:#9ca3af; text-align:right; margin-top:8px;">Harsh Raj Soni • BCA Ecosystem</div>
    </div>
    """
    res = execute_ai_query(system_role, user_prompt)
    return res.replace("```html", "").replace("```", "").strip()

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
            <div>• Dual AI Engine Architecture: ChatGPT (GPT-4o) & Google Gemini</div>
            <div>• Real Ruled Handwriting Register Sheet Engine</div>
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
                st.session_state.notebook_rendered_html = ""
                st.rerun()

    active_subj = st.session_state.selected_subject

    # Navigation Dock
    nav_options = [
        "📝 Notes",
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

    # ================= 1. NOTES MODULE =================
    if selected_nav == "📝 Notes":
        st.markdown(f"#### 📖 Lecture Notes Register — {active_subj}")
        st.caption("Clean ruled paper layout with handwritten typography, tables, and formula highlights.")

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
            custom_topic = st.text_input("Custom query (optional):", placeholder="e.g. Master-slave JK flip-flop working")
        with c2:
            notes_lang = st.selectbox("Language:", ["Hinglish", "English", "Hindi"])

        final_topic = custom_topic.strip() if custom_topic.strip() else chosen_topic

        if st.button("Generate Notes", use_container_width=True):
            with st.spinner(f"Writing lecture sheet for {final_topic}..."):
                st.session_state.notebook_rendered_html = get_handwritten_notes_html(final_topic, active_subj, notes_lang)

        if st.session_state.notebook_rendered_html:
            st.markdown(st.session_state.notebook_rendered_html, unsafe_allow_html=True)

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
        exam_topic = st.text_input("Topic Scope:", placeholder="e.g. Cache Mapping / L'Hopital Rule")
        if st.button("Generate Paper", use_container_width=True):
            sys_prompt = "You are a university exam creator."
            st.session_state.ex_res = execute_ai_query(sys_prompt, f"Create a 15-mark university test paper on {exam_topic if exam_topic else 'Full Syllabus'} for {active_subj}")
        if "ex_res" in st.session_state:
            st.write(st.session_state.ex_res)

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
                sys_prompt = "You are an engineering mentor. Provide working code and steps."
                res = execute_ai_query(sys_prompt, f"Provide complete working code and documentation for project: '{sel_p}' in {active_subj}.")
                st.markdown(res)

    # ================= 7. AI MENTOR =================
    elif selected_nav == "🤖 AI Mentor":
        st.markdown(f"#### 🤖 Doubt Clearance — {active_subj}")
        q = st.text_input("Ask Question:")
        if st.button("Submit") and q:
            sys_prompt = "You are a helpful BCA professor. Explain step-by-step."
            st.write(execute_ai_query(sys_prompt, q))

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
                    sys_prompt = "Optimize this python code cleanly."
                    cell["output"] = execute_ai_query(sys_prompt, f"Analyze:\n{cell['code']}")
                    cell["error"] = ""

            if cell["output"]:
                st.code(cell["output"])
            if cell["error"]:
                st.error(cell["error"])
                if st.button("Auto-Fix", key=f"afix_{cell['id']}"):
                    sys_prompt = "Fix this python error."
                    st.info(execute_ai_query(sys_prompt, f"Fix this code error:\n{cell['code']}\nError: {cell['error']}"))
