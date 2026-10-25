import streamlit as st
import google.generativeai as genai
import io
import contextlib
from PIL import Image, ImageDraw, ImageFont

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

if "current_note_page" not in st.session_state:
    st.session_state.current_note_page = 1

if "generated_page_images" not in st.session_state:
    st.session_state.generated_page_images = []

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

# ================= EXECUTIVE STYLING CSS =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

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
        padding-top: 1rem !important;
        padding-bottom: 5rem !important;
        max-width: 1140px !important;
    }

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
        background: rgba(37, 99, 235, 0.15);
        border: 1px solid rgba(59, 130, 246, 0.5);
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 12.5px;
        font-weight: 700;
        color: #60A5FA;
        box-shadow: 0 0 16px rgba(37, 99, 235, 0.3);
    }

    div[data-testid="stExpander"] {
        background: rgba(15, 23, 42, 0.85) !important;
        border: 1.5px solid #3B82F6 !important;
        border-radius: 14px !important;
        box-shadow: 0 0 20px rgba(37, 99, 235, 0.35), 0 8px 24px rgba(0, 0, 0, 0.5) !important;
        margin-bottom: 18px !important;
    }

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

    div[data-testid="column"]:has(button[key="mini_p_prev"]),
    div[data-testid="column"]:has(button[key="mini_p_next"]) {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    button[key="mini_p_prev"], button[key="mini_p_next"] {
        width: 38px !important;
        height: 38px !important;
        min-width: 38px !important;
        min-height: 38px !important;
        border-radius: 50% !important;
        font-size: 19px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
</style>
""", unsafe_allow_html=True)

# ================= 7-PAGE HIGH DEFINITION A4 PHOTO RENDERER =================
def create_a4_sheet_image(topic, page_index, total_pages, text_content, subject_name):
    width, height = 750, 950
    image = Image.new("RGB", (width, height), "#FFFFFF")
    draw = ImageDraw.Draw(image)

    # Blue Ruled Lines
    line_spacing = 34
    for y in range(120, height - 30, line_spacing):
        draw.line([(0, y), (width, y)], fill="#E2E8F0", width=1)

    # Red Margin Line
    draw.line([(85, 0), (85, height)], fill="#EF4444", width=2)

    # Spiral Rings
    for ring_y in range(35, height - 20, 36):
        draw.ellipse([20, ring_y, 34, ring_y + 14], fill="#CBD5E1", outline="#94A3B8", width=1)

    # Header Card
    font_bold = ImageFont.load_default()
    draw.rectangle([(95, 25), (240, 52)], fill="#2563EB")
    draw.text((105, 32), f"A4 SHEET {page_index} OF {total_pages}", fill="#FFFFFF", font=font_bold)

    clean_topic = topic[:45]
    draw.text((95, 62), clean_topic, fill="#0F172A", font=font_bold)
    draw.line([(95, 82), (width - 40, 82)], fill="#EF4444", width=2)
    draw.text((95, 88), f"Discipline: {subject_name} | MLK PG College Balrampur", fill="#64748B", font=font_bold)

    # Word Wrap Engine
    start_y = 130
    x_pos = 100
    words = text_content.replace("\n", " [BREAK] ").split()
    current_line = []
    lines_to_draw = []
    
    for word in words:
        if word == "[BREAK]":
            lines_to_draw.append(" ".join(current_line))
            current_line = []
            continue
        test_line = " ".join(current_line + [word])
        if len(test_line) > 52:
            lines_to_draw.append(" ".join(current_line))
            current_line = [word]
        else:
            current_line.append(word)
    if current_line:
        lines_to_draw.append(" ".join(current_line))

    for idx, line_text in enumerate(lines_to_draw[:23]):
        y_coord = start_y + (idx * line_spacing)
        draw.text((x_pos, y_coord - 14), line_text, fill="#1E3A8A", font=font_bold)

    draw.text((95, height - 35), f"Created by Harsh Raj Soni • BCA Ecosystem • Sheet {page_index}", fill="#94A3B8", font=font_bold)
    return image

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

    optimized_prompt = f"""
    You are an esteemed university professor for the BCA program at MLK PG College, Balrampur.
    Subject Discipline: {current_subject}
    {lang_instruction}

    STRICT GUIDELINES:
    1. Maintain a respectful, dignified academic tone. NEVER use vulgarity, slang, or offensive Hindi words.
    2. If writing notes, generate EXACTLY 7 COMPLETE PAGES. Separate each page with '[PAGE_BREAK]'.
    3. Keep each page between 45 to 60 words so it fits properly on the A4 photo.
    4. Start directly with core educational concepts. No introductory boilerplate.

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
                    continue
                elif "504" in last_error or "deadline" in last_error.lower():
                    continue

    return f"⏳ AI Engine Temporary Busy: {last_error}"

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
            <div>• Core Curriculum Coverage: Python Programming, CSA & Discrete Mathematics</div>
            <div>• Real-time Ruled Register Notes & Formula Compendium</div>
            <div>• Interactive Evaluation & Sandbox Environment</div>
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
                st.session_state.generated_page_images = []
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

    # ================= 1. 7-PAGE PHOTO BINDER =================
    if selected_nav == "📝 Notes":
        st.markdown(f"#### 📖 7-Page HD Binder — {active_subj}")
        st.caption("Each sheet is rendered as a standalone high-definition photo. Zero text cutting or layout stretching.")

        if active_subj == "🐍 Python Programming":
            suggested_topics = [
                "Python Complete Architecture, Bytecode & Memory Management",
                "Control Flow, Loops, For-Else Logic & Prime Verification",
                "Functions, Scopes, LEGB Resolution & Lambda Expressions",
                "Data Structures: Lists, Tuples, Dictionaries & Sets",
                "Object Oriented Programming: Encapsulation, Mangling & MRO",
                "File Handling, Context Managers & Exception Hierarchy"
            ]
        elif active_subj == "🖥️ Computer System Architecture":
            suggested_topics = [
                "Number Systems, Complements & Binary Logic Operations",
                "Half Adder, Full Adder & K-Map 4-Variable Minimization",
                "Flip-Flops, Master-Slave JK & Race-Around Condition",
                "Instruction Cycle Phases, Addressing Modes & Micro-operations",
                "Cache Memory Mapping, Virtual Memory & Pipeline Hazards"
            ]
        else:
            suggested_topics = [
                "L'Hopital's Rule for Indeterminate Forms with Multi-Step Derivatives",
                "Equivalence Relations Proof & POSET Hasse Diagrams",
                "Matrix Rank, Echelon Forms & Rouche-Capelli Consistency",
                "Eigenvalues, Eigenvectors & Cayley-Hamilton Theorem",
                "Leibnitz Theorem for n-th Derivatives & Formula Matrix",
                "Newton-Raphson Method & Bisection Numerical Convergence"
            ]

        c1, c2 = st.columns([2.5, 1])
        with c1:
            chosen_topic = st.selectbox("Topic:", suggested_topics)
            custom_topic = st.text_input("Custom topic (optional):", placeholder="e.g. Master-slave JK flip-flop working")
        with c2:
            notes_lang = st.selectbox("Language:", ["Hinglish", "English", "Hindi"])

        final_topic = custom_topic.strip() if custom_topic.strip() else chosen_topic

        if st.button("Generate", use_container_width=True):
            st.session_state.current_note_page = 1
            st.session_state.generated_page_images = []
            
            with st.spinner(f"Rendering 7 distinct A4 sheets for {final_topic}..."):
                raw_output = get_ai_response(
                    f"Create comprehensive 7-page university notes on '{final_topic}' in {active_subj}.",
                    forced_language=notes_lang,
                    current_subject=active_subj
                )

                raw_pages = [p.strip() for p in raw_output.split("[PAGE_BREAK]") if p.strip()]
                while len(raw_pages) < 7:
                    raw_pages.append(f"Continued analysis of {final_topic} [Part {len(raw_pages)+1}]. Review syllabus guidelines, step proofs, and examiner marks distribution.")
                raw_pages = raw_pages[:7]

                photos = []
                for p_num, p_text in enumerate(raw_pages, start=1):
                    clean_text = p_text.replace("### ", "").replace("## ", "").replace("# ", "")
                    img = create_a4_sheet_image(final_topic, p_num, 7, clean_text, active_subj)
                    photos.append(img)

                st.session_state.generated_page_images = photos
                st.session_state.flip_notes_topic = final_topic

        # Display Photo Binder
        if st.session_state.generated_page_images:
            total_photos = len(st.session_state.generated_page_images)
            curr_p = max(1, min(st.session_state.current_note_page, total_photos))
            active_photo = st.session_state.generated_page_images[curr_p - 1]
            
            col_l, col_center, col_r = st.columns([1, 2.8, 1])
            with col_center:
                st.image(active_photo, caption=f"Sheet {curr_p} of {total_photos} — {st.session_state.get('flip_notes_topic')}", use_container_width=True)

            ctrl_c1, ctrl_c2, ctrl_c3 = st.columns([1.2, 2, 1.2])
            with ctrl_c1:
                if st.button("‹", key="mini_p_prev", disabled=(curr_p == 1), use_container_width=True):
                    st.session_state.current_note_page = max(1, curr_p - 1)
                    st.rerun()
            with ctrl_c2:
                st.markdown(f"""
                <div style="text-align: center; color: #60A5FA; font-size: 13px; font-weight: 700; padding-top: 6px;">
                    Sheet {curr_p} of {total_photos}
                </div>
                """, unsafe_allow_html=True)
            with ctrl_c3:
                if st.button("›", key="mini_p_next", disabled=(curr_p == total_photos), use_container_width=True):
                    st.session_state.current_note_page = min(total_photos, curr_p + 1)
                    st.rerun()

    # ================= 2. MATHS ENCYCLOPEDIA =================
    elif selected_nav == "📐 Maths Menu":
        st.markdown("#### 📐 Mathematics Formula Menu")
        with st.expander("⚡ Differentiation Rules"):
            st.latex(r"\frac{d}{dx}(x^n) = n x^{n-1}, \quad \frac{d}{dx}(u \cdot v) = u v' + v u'")
            st.latex(r"\frac{d}{dx}\left(\frac{u}{v}\right) = \frac{v u' - u v'}{v^2}, \quad \frac{d}{dx}(\sin x) = \cos x")
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
            st.write("Address division: Tag | Line Index | Word Offset")

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
            st.session_state.ex_res = get_ai_response(f"15-mark test on {exam_topic if exam_topic else 'Comprehensive'}", current_subject=active_subj)
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
                res = get_ai_response(f"Provide complete working code and documentation for project: '{sel_p}' in {active_subj}.", current_subject=active_subj)
                st.markdown(res)

    # ================= 7. AI MENTOR =================
    elif selected_nav == "🤖 AI Mentor":
        st.markdown(f"#### 🤖 Doubt Clearance — {active_subj}")
        q = st.text_input("Ask Question:")
        if st.button("Submit") and q:
            st.write(get_ai_response(q, current_subject=active_subj))

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
                    cell["output"] = get_ai_response(f"Quickly analyze and optimize:\n{cell['code']}", current_subject="Python")
                    cell["error"] = ""

            if cell["output"]:
                st.code(cell["output"])
            if cell["error"]:
                st.error(cell["error"])
                if st.button("Auto-Fix", key=f"afix_{cell['id']}"):
                    st.info(get_ai_response(f"Fix this code error:\n{cell['code']}\nError: {cell['error']}", current_subject="Python"))
