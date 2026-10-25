import streamlit as st
from groq import Groq
import google.generativeai as genai
import io
import re
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

# ================= EXECUTIVE STYLING & CLEAN NEAT REGISTER CSS =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Kalam:wght@400;700&family=Patrick+Hand&display=swap');

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
        padding-top: 0.6rem !important;
        padding-bottom: 5rem !important;
        max-width: 1040px !important;
    }

    .formal-top-banner {
        background: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 10px 18px;
        backdrop-filter: blur(20px);
        margin-bottom: 12px;
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
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11.5px;
        font-weight: 700;
        color: #60A5FA;
        box-shadow: 0 0 16px rgba(37, 99, 235, 0.3);
    }

    div[data-testid="stExpander"] {
        background: rgba(15, 23, 42, 0.85) !important;
        border: 1.5px solid #3B82F6 !important;
        border-radius: 12px !important;
        box-shadow: 0 0 18px rgba(37, 99, 235, 0.3), 0 8px 24px rgba(0, 0, 0, 0.5) !important;
        margin-bottom: 12px !important;
    }

    div[data-testid="stRadio"] {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 5px 8px !important;
        border-radius: 35px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45) !important;
        margin: 0 auto 14px auto !important;
        width: 100% !important;
        max-width: 940px !important;
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
        padding: 5px 12px !important;
        font-size: 12px !important;
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
        padding: 5px 14px !important;
        font-weight: 600 !important;
        font-size: 12.5px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5) !important;
    }

    .register-outer-center {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-top: 4px;
        margin-bottom: 10px;
    }

    .real-notebook-sheet {
        background-color: #fbfbf8 !important;
        background-image: 
            linear-gradient(90deg, transparent 36px, #ef4444 36px, #ef4444 37.5px, transparent 37.5px),
            linear-gradient(#e2e8f0 1px, transparent 1px) !important;
        background-size: 100% 100%, 100% 22px !important;
        border-radius: 8px !important;
        padding: 14px 14px 16px 44px !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.5) !important;
        width: 100% !important;
        max-width: 440px !important;
        box-sizing: border-box !important;
        font-family: 'Patrick Hand', 'Kalam', cursive !important;
        color: #1e3a8a !important;
        font-size: 14.5px !important;
        line-height: 22px !important;
        position: relative !important;
        overflow: hidden !important;
    }

    .real-notebook-sheet::before {
        content: '' !important;
        position: absolute !important;
        top: 10px !important;
        left: 8px !important;
        width: 10px !important;
        height: 96% !important;
        background-image: radial-gradient(circle, #94a3b8 3px, transparent 4px) !important;
        background-size: 10px 22px !important;
        background-repeat: repeat-y !important;
    }

    .nb-title-h1 {
        font-family: 'Kalam', cursive !important;
        font-size: 19px !important;
        font-weight: 700 !important;
        color: #1e1b4b !important;
        background: #fdf2f8 !important;
        padding: 1px 10px !important;
        border-radius: 4px !important;
        display: inline-block !important;
        border-bottom: 2px dashed #ec4899 !important;
        margin-bottom: 3px !important;
        line-height: 23px !important;
    }

    .nb-subhead {
        font-weight: 700 !important;
        color: #0369a1 !important;
        font-size: 15px !important;
        text-decoration: underline !important;
        margin-top: 4px !important;
        display: block !important;
    }

    .table-container {
        width: 100% !important;
        overflow-x: auto !important;
        margin: 4px 0 !important;
        box-sizing: border-box !important;
    }
    .nb-table {
        border-collapse: collapse !important;
        font-family: 'Patrick Hand', cursive !important;
        font-size: 13.5px !important;
        line-height: 18px !important;
        background: #ffffff !important;
        border: 1.5px solid #1e3a8a !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    .nb-table th, .nb-table td {
        border: 1px solid #1e3a8a !important;
        padding: 2px 4px !important;
        text-align: center !important;
        word-break: break-word !important;
    }
    .nb-table th {
        background: #e0f2fe !important;
        color: #0369a1 !important;
        font-weight: 700 !important;
    }

    .nb-keypoints-box {
        border: 1.5px dashed #16a34a !important;
        background: #f0fdf4 !important;
        border-radius: 8px !important;
        padding: 5px 10px !important;
        margin-top: 6px !important;
        color: #14532d !important;
        font-size: 13.5px !important;
        line-height: 19px !important;
    }

    @media (max-width: 768px) {
        .real-notebook-sheet {
            padding: 12px 10px 14px 38px !important;
            font-size: 13.5px !important;
            line-height: 20px !important;
            background-size: 100% 100%, 100% 20px !important;
            max-width: 96vw !important;
        }
        .nb-title-h1 {
            font-size: 17.5px !important;
        }
        .nb-table {
            font-size: 12.5px !important;
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

def execute_ai_query(system_role, user_prompt, max_budget=4096, image_input=None):
    """Executes prompt with dynamic high token limit (4096) to prevent cutting"""
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
                    max_tokens=max_budget
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

def fix_unclosed_html(html_str):
    """Auto-closes broken HTML tags if output was cut"""
    open_divs = html_str.count("<div")
    close_divs = html_str.count("</div>")
    if open_divs > close_divs:
        html_str += "</div>" * (open_divs - close_divs)
        
    if "<table" in html_str and "</table" not in html_str:
        html_str += "</table>"
    if "<p" in html_str and "</p" not in html_str:
        html_str += "</p>"
    return html_str

def generate_multi_sheets_html(topic, subject_name, notes_lang):
    system_role = (
        "You are an esteemed university professor for BCA at MLK PG College, Balrampur. "
        "Strictly maintain academic dignity. Never use slang or informal abusive words. "
        "Output EXACTLY 3 TO 4 INDIVIDUAL COMPLETE LECTURE SHEETS separated strictly by the token '===SHEET_SPLIT==='. "
        "Every single sheet MUST be 100% complete with all 4 sections fully finished: "
        "1. Definition & Core Concept, "
        "2. Truth Table / Formulation / Rules (must include full table rows, never leave table empty), "
        "3. Logic Expressions / Step-by-Step Working, "
        "4. Key Exam Points. "
        "DO NOT USE CODE BLOCKS OR MARKDOWN TICKS (never output ```html or ```). Start directly with <div class='register-outer-center'>."
    )
    user_prompt = f"""
    Create a complete 3 to 4-sheet lecture register for '{topic}' in {subject_name} ({notes_lang}).
    Ensure each sheet has its full truth table completed with all output rows, full logic working steps, and key exam points.

    TEMPLATE FOR EACH SHEET (Separate sheets strictly by ===SHEET_SPLIT===):
    <div class="register-outer-center">
        <div class="real-notebook-sheet">
            <div class="nb-title-h1">{topic} [Part X]</div>
            <div style="font-size:10.5px; color:#6b7280; margin-bottom:3px;">{subject_name} • MLK PG College Balrampur</div>

            <span class="nb-subhead">1. Definition & Core Concept :</span>
            <p style="margin: 2px 0 4px 0;">[2 clear concise explanation lines in {notes_lang}]</p>

            <span class="nb-subhead">2. Truth Table / Formulation / Rules :</span>
            <div class="table-container">
                <table class="nb-table">
                    <tr><th>Input A</th><th>Input B</th><th>Output</th><th>Status</th></tr>
                    <tr><td>0</td><td>0</td><td>0</td><td>Low</td></tr>
                    <tr><td>0</td><td>1</td><td>1</td><td>High</td></tr>
                    <tr><td>1</td><td>0</td><td>1</td><td>High</td></tr>
                    <tr><td>1</td><td>1</td><td>0</td><td>Invert</td></tr>
                </table>
            </div>

            <span class="nb-subhead">3. Logic Expressions / Step-by-Step Working :</span>
            <p style="margin: 2px 0 4px 0;">
                • Step 1: Core working logic and operation<br>
                • Step 2: Signal/Bytecode execution path<br>
                • Step 3: Practical implementation rule
            </p>

            <div class="nb-keypoints-box">
                <b>✳ Key Exam Points :</b><br>
                • Important semester exam rule & common pitfall<br>
                • High priority formula
            </div>
            <div style="font-size:10px; color:#9ca3af; text-align:right; margin-top:4px;">Harsh Raj Soni • BCA Ecosystem</div>
        </div>
    </div>
    """
    raw_res = execute_ai_query(system_role, user_prompt, max_budget=4096)
    
    clean_text = raw_res.replace("```html", "").replace("```HTML", "").replace("```", "").strip()
    clean_text = re.sub(r"^`+|`+$", "", clean_text)
    
    raw_sheets = [s.strip() for s in clean_text.split("===SHEET_SPLIT===") if s.strip()]
    
    sanitized_sheets = []
    for s in raw_sheets:
        fixed = fix_unclosed_html(s)
        sanitized_sheets.append(fixed)
        
    return sanitized_sheets if sanitized_sheets else [clean_text]

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
            <div>• Real Ruled Handwriting Register Sheet Engine (Auto-Fit & Compact)</div>
            <div>• Dynamic Token Engine (Complete Non-Truncated Sheets)</div>
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
            label = f"✔ {s}" if is_active else f"➔ Sw
