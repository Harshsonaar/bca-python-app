import json
import os
import re
import html
from typing import Any

import streamlit as st
import streamlit.components.v1 as components

try:
    from groq import Groq
except ImportError:
    Groq = None

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None


st.set_page_config(
    page_title="BCA Handwritten Notes Studio",
    page_icon="📒",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==================== CONFIGURATION ====================

def get_secret(name: str) -> str:
    try:
        value = st.secrets.get(name, "")
    except Exception:
        value = os.getenv(name, "")
    return str(value or "").strip()


if "notes_pages" not in st.session_state:
    st.session_state.notes_pages = []

if "opened_page" not in st.session_state:
    st.session_state.opened_page = None

if "last_topic" not in st.session_state:
    st.session_state.last_topic = ""

if "last_subject" not in st.session_state:
    st.session_state.last_subject = "Computer System Architecture"


# ==================== STYLING ====================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Patrick+Hand&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    :root {
        --ink: #173b86;
        --blue: #1676b8;
        --paper: #fffefa;
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background: linear-gradient(
            135deg, #eef4ff, #f8fafc 55%, #e8f2ff
        );
    }

    .block-container {
        max-width: 1250px;
        padding-top: 1.2rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 1.4rem;
        border-radius: 18px;
        background: linear-gradient(120deg, #102c61, #1d4f91);
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 10px 28px #173b8622;
    }

    .hero h1 {
        margin: 0;
        font-size: clamp(1.6rem, 3vw, 2.5rem);
    }

    .hero p {
        margin: .4rem 0 0;
        color: #dbeafe;
    }

    .page-card {
        background: white;
        border: 1px solid #d8e4f4;
        border-radius: 14px;
        padding: 8px;
        margin-bottom: 12px;
        overflow: hidden;
    }

    .stButton > button {
        border-radius: 9px;
        font-weight: 600;
    }

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="hero">
        <h1>📒 BCA Handwritten Notes Studio</h1>
        <p>
            AI-generated notebook notes • Grid gallery •
            Full-page reading • Print and save as PDF
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==================== AI PROMPT ====================

def build_prompt(
    topic: str,
    subject: str,
    language: str,
    page_count: int,
) -> str:

    return f"""
You are an expert BCA university teacher and handwritten-notes creator.

Create accurate, exam-oriented notes for the following topic.

TOPIC: {topic}
SUBJECT: {subject}
LANGUAGE: {language}
NUMBER OF PAGES: {page_count}

Return ONLY valid JSON. Do not use Markdown code fences.

Required JSON structure:

{{
  "title": "Main topic title",
  "pages": [
    {{
      "title": "Page heading",
      "sections": [
        {{
          "heading": "Definition",
          "paragraphs": ["Clear explanation"],
          "bullets": ["Important point"]
        }}
      ],
      "formula": "Formula or logic expression",
      "table": {{
        "headers": ["Column A", "Column B"],
        "rows": [["value", "value"]]
      }},
      "code": "Optional runnable code",
      "diagram": "Precise diagram description",
      "key_points": ["Exam point"]
    }}
  ]
}}

STRICT RULES:

1. Return exactly {page_count} pages.
2. Keep content concise enough to fit notebook pages.
3. Use simple, student-friendly {language}.
4. Use accurate definitions and university-exam terminology.
5. Do not repeat the same content across pages.
6. Never invent facts, formulas, truth-table values or results.
7. Include relevant diagrams, tables, formulas and worked examples.
8. If a table is irrelevant, use empty headers and rows.
9. If code is irrelevant, use an empty string for code.
10. If a diagram is irrelevant, use an empty string for diagram.
11. All JSON must be valid. Escape quotation marks and newlines
    correctly inside strings.

TOPIC-SPECIFIC REQUIREMENTS:

For Full Adder:
- Explain A, B, Cin, Sum and Cout.
- Sum = A XOR B XOR Cin.
- Cout = AB + ACin + BCin.
- Include the complete truth table with all 8 input combinations.
- Include the two-XOR and carry-generation circuit explanation.
- Ensure the truth table agrees with the equations.
- Explain that a Full Adder can be implemented using two Half
  Adders and an OR gate.

For other digital logic topics:
- Use correct logic symbols and Boolean expressions.
- Include the appropriate truth table when relevant.
- Describe input-output connections clearly.

For Python:
- Give runnable Python examples.
- Explain the code and expected output.
- Use correct indentation and syntax.

For mathematics:
- Show correct formulas and step-by-step solved examples.
- Verify calculations before returning the result.

Return JSON only.
"""


# ==================== JSON PARSER ====================

def extract_json(raw: str) -> dict:

    raw = (raw or "").strip()

    raw = re.sub(
        r"^```(?:json)?\s*",
        "",
        raw,
        flags=re.IGNORECASE,
    )

    raw = re.sub(r"\s*```$", "", raw)

    start = raw.find("{")
    end = raw.rfind("}")

    if start == -1 or end <= start:
        raise ValueError(
            "AI response valid JSON mein nahi aaya. Dobara try karo."
        )

    data = json.loads(raw[start:end + 1])

    if not isinstance(data, dict):
        raise ValueError("AI response ka JSON structure galat hai.")

    return data


# ==================== GROQ ENGINE ====================

def call_groq(api_key: str, prompt: str) -> str:

    if Groq is None:
        raise RuntimeError(
            "Groq package missing hai. requirements.txt install karo."
        )

    client = Groq(api_key=api_key)

    models = [
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b",
        "llama-3.3-70b-versatile",
    ]

    errors = []

    for model in models:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an accurate academic notes creator. "
                            "Follow the requested JSON structure strictly."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.2,
                max_tokens=6500,
            )

            result = response.choices[0].message.content

            if result and result.strip():
                return result.strip()

            errors.append(f"{model}: Empty response")

        except Exception as exc:
            errors.append(f"{model}: {str(exc)}")

    raise RuntimeError(
        "Groq ke kisi model se response nahi mila: "
        + " | ".join(errors[-2:])
    )


# ==================== GEMINI ENGINE ====================

def call_gemini(api_key: str, prompt: str) -> str:

    if genai is None:
        raise RuntimeError(
            "Google GenAI package missing hai. requirements.txt install karo."
        )

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            response_mime_type="application/json",
        ),
    )

    result = response.text

    if not result or not result.strip():
        raise RuntimeError("Gemini ne empty response diya.")

    return result.strip()


# ==================== NOTES GENERATOR ====================

def generate_notes(
    topic: str,
    subject: str,
    language: str,
    page_count: int,
    provider: str,
    groq_key: str,
    gemini_key: str,
) -> list[dict[str, Any]]:

    prompt = build_prompt(
        topic,
        subject,
        language,
        page_count,
    )

    if provider == "Groq":
        engines = [
            ("Groq", groq_key),
            ("Gemini", gemini_key),
        ]
    else:
        engines = [
            ("Gemini", gemini_key),
            ("Groq", groq_key),
        ]

    errors = []

    for name, key in engines:

        if not key:
            continue

        try:
            if name == "Groq":
                raw = call_groq(key, prompt)
            else:
                raw = call_gemini(key, prompt)

            data = extract_json(raw)

            pages = data.get("pages")

            if not isinstance(pages, list) or not pages:
                raise ValueError("AI response mein pages nahi mile.")

            clean_pages = []

            for page in pages[:page_count]:
                if not isinstance(page, dict):
                    continue

                page.setdefault("title", topic)
                page.setdefault("sections", [])
                page.setdefault("formula", "")
                page.setdefault("table", {})
                page.setdefault("code", "")
                page.setdefault("diagram", "")
                page.setdefault("key_points", [])

                clean_pages.append(page)

            if not clean_pages:
                raise ValueError("Valid notebook pages generate nahi hue.")

            return clean_pages

        except Exception as exc:
            errors.append(f"{name}: {str(exc)}")

    if not errors:
        raise RuntimeError(
            "Sidebar mein Groq ya Gemini API key enter karo."
        )

    raise RuntimeError(
        "Notes generate nahi hue.\n\n" + "\n\n".join(errors)
    )


# ==================== SAFE HTML HELPERS ====================

def escape_text(value: Any) -> str:

    if value is None:
        return ""

    return html.escape(str(value)).replace("\n", "<br>")


def render_page(
    page: dict,
    page_no: int,
    topic: str,
    subject: str,
) -> str:

    title = escape_text(page.get("title") or topic)

    sections_html = []

    sections = page.get("sections", [])

    if isinstance(sections, list):

        for section in sections:

            if not isinstance(section, dict):
                continue

            heading = escape_text(
                section.get("heading", "Concept")
            )

            paragraphs = section.get("paragraphs", [])
            bullets = section.get("bullets", [])

            if not isinstance(paragraphs, list):
                paragraphs = []

            if not isinstance(bullets, list):
                bullets = []

            paragraph_html = "".join(
                f"<p>{escape_text(p)}</p>"
                for p in paragraphs
                if p
            )

            bullet_html = ""

            if bullets:
                bullet_html = (
                    "<ul>"
                    + "".join(
                        f"<li>{escape_text(item)}</li>"
                        for item in bullets
                        if item
                    )
                    + "</ul>"
                )

            sections_html.append(
                f"""
                <section>
                    <h3>{heading}</h3>
                    {paragraph_html}
                    {bullet_html}
                </section>
                """
            )

    # Render tables safely
    table_data = page.get("table") or {}

    if not isinstance(table_data, dict):
        table_data = {}

    headers = table_data.get("headers", [])
    rows = table_data.get("rows", [])

    if not isinstance(headers, list):
        headers = []

    if not isinstance(rows, list):
        rows = []

    table_html = ""

    if headers and rows:

        header_html = "".join(
            f"<th>{escape_text(item)}</th>"
            for item in headers
        )

        row_html = []

        for row in rows:

            if not isinstance(row, list):
                continue

            cells = "".join(
                f"<td>{escape_text(cell)}</td>"
                for cell in row
            )

            row_html.append(f"<tr>{cells}</tr>")

        table_html = f"""
        <h3>Truth Table / Reference Table</h3>
        <div class="table-wrap">
            <table>
                <thead>
                    <tr>{header_html}</tr>
                </thead>
                <tbody>
                    {"".join(row_html)}
                </tbody>
            </table>
        </div>
        """

    formula = page.get("formula", "")

    formula_html = ""

    if formula:
        formula_html = f"""
        <div class="formula">
            <b>Formula / Logic:</b><br>
            {escape_text(formula)}
        </div>
        """

    code = page.get("code", "")

    code_html = ""

    if code:
        code_html = f"""
        <h3>Code Example</h3>
        <pre>{escape_text(code)}</pre>
        """

    diagram = page.get("diagram", "")

    diagram_html = ""

    if diagram:
        diagram_html = f"""
        <div class="diagram">
            <b>Diagram / Circuit to draw:</b><br>
            {escape_text(diagram)}
        </div>
        """

    key_points = page.get("key_points", [])

    if not isinstance(key_points, list):
        key_points = []

    key_html = ""

    if key_points:
        key_html = """
        <div class="keybox">
            <b>✳ Key Exam Points</b>
            <ul>
                {}
            </ul>
        </div>
        """.format(
            "".join(
                f"<li>{escape_text(item)}</li>"
                for item in key_points
                if item
            )
        )

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <style>
        @import url(
            'https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Patrick+Hand&display=swap'
        );

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            padding: 10px;
            background: #e8edf5;
            color: #183b80;
            font-family: 'Patrick Hand', cursive;
        }}

        .sheet {{
            position: relative;
            margin: 0 auto;
            background-color: #fffefa;

            background-image:
                linear-gradient(
                    90deg,
                    transparent 47px,
                    #e87979 47px,
                    #e87979 49px,
                    transparent 49px
                ),
                linear-gradient(
                    #dbe7f4 1px,
                    transparent 1px
                );

            background-size:
                100% 100%,
                100% 28px;

            border: 1px solid #d1d5db;
            border-radius: 5px;
            box-shadow: 0 5px 20px #0f172a20;

            padding: 20px 18px 22px 62px;
            width: 100%;
            max-width: 720px;
            min-height: 720px;

            font-size: 17px;
            line-height: 1.55;
            overflow-wrap: anywhere;
        }}

        h1 {{
            font-family: 'Caveat', cursive;
            font-size: 34px;
            line-height: 1.1;
            color: #171b57;
            margin: 0 0 5px;
            border-bottom: 2px solid #252a7b;
            display: inline-block;
        }}

        .meta {{
            font: 11px Arial, sans-serif;
            color: #64748b;
            margin: 4px 0 10px;
        }}

        h3 {{
            font-family: 'Caveat', cursive;
            font-size: 24px;
            color: #075985;
            text-decoration: underline;
            margin: 8px 0 2px;
        }}

        p {{
            margin: 2px 0 5px;
        }}

        ul {{
            margin: 0 0 5px;
            padding-left: 20px;
        }}

        li {{
            padding-left: 1px;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            font-size: 15px;
            background: #fff;
            margin: 4px 0 8px;
        }}

        th, td {{
            border: 1px solid #24437d;
            padding: 3px 5px;
            text-align: center;
        }}

        th {{
            background: #e5f2ff;
            color: #075985;
        }}

        .table-wrap {{
            overflow-x: auto;
        }}

        .formula, .diagram {{
            border-left: 3px solid #eab308;
            background: #fffbea;
            padding: 6px 8px;
            margin: 7px 0;
            overflow-wrap: anywhere;
        }}

        pre {{
            font: 14px/1.4 monospace;
            white-space: pre-wrap;
            overflow-wrap: anywhere;
            background: #f1f5f9;
            border: 1px solid #cbd5e1;
            border-radius: 5px;
            padding: 8px;
            color: #111827;
        }}

        .keybox {{
            border: 2px dashed #16a34a;
            background: #f0fdf4;
            border-radius: 10px;
            padding: 5px 10px;
            margin-top: 8px;
            color: #14532d;
        }}

        .keybox ul {{
            margin: 2px 0;
        }}

        .footer {{
            font: 10px Arial, sans-serif;
            color: #94a3b8;
            text-align: right;
            margin-top: 8px;
        }}

        @media print {{
            body {{
                padding: 0;
                background: white;
            }}

            .sheet {{
                box-shadow: none;
                border: 0;
                max-width: none;
                min-height: 0;
            }}
        }}
        </style>
    </head>

    <body>
        <article class="sheet">
            <h1>{title}</h1>

            <div class="meta">
                {escape_text(subject)} • BCA Study Notes • Page {page_no}
            </div>

            {"".join(sections_html)}

            {table_html}
            {formula_html}
            {code_html}
            {diagram_html}
            {key_html}

            <div class="footer">
                Handwritten-style study sheet
            </div>
        </article>
    </body>
    </html>
    """


# ==================== SIDEBAR / API SETUP ====================

with st.sidebar:

    st.header("⚙️ AI Setup")

    provider = st.radio(
        "Preferred AI engine",
        ["Groq", "Gemini"],
        index=0,
    )

    groq_key = get_secret("GROQ_API_KEY")
    gemini_key = get_secret("GEMINI_API_KEY")

    if not groq_key:
        groq_key = st.text_input(
            "Groq API key",
            type="password",
            help="GROQ_API_KEY can also be set in Streamlit secrets.",
        )

    if not gemini_key:
        gemini_key = st.text_input(
            "Gemini API key",
            type="password",
            help="GEMINI_API_KEY can also be set in Streamlit secrets.",
        )

    st.divider()

    st.caption(
        "API keys ko public GitHub repository mein hardcode mat karo."
    )


# ==================== NOTES FORM ====================

st.subheader("📝 Create Handwritten Notes")

with st.form("notes_generation_form"):

    col1, col2 = st.columns([2, 1])

    with col1:

        topic = st.text_input(
            "Topic",
            value="Full Adder",
            placeholder="Full Adder, Python functions, matrices...",
        )

        subject = st.selectbox(
            "Subject",
            [
                "Computer System Architecture",
                "Python Programming",
                "Foundation of Mathematics",
                "Other",
            ],
        )

    with col2:

        language = st.selectbox(
            "Notes language",
            ["Hinglish", "English", "Hindi"],
        )

        page_count = st.slider(
            "Number of pages",
            min_value=1,
            max_value=5,
            value=4,
        )

    generate = st.form_submit_button(
        "✨ Generate Handwritten Notes",
        use_container_width=True,
    )


if generate:

    if not topic.strip():

        st.warning("Pehle topic enter karo.")

    else:

        try:

            with st.spinner("AI tumhare notes prepare kar raha hai..."):

                pages = generate_notes(
                    topic=topic.strip(),
                    subject=subject,
                    language=language,
                    page_count=page_count,
                    provider=provider,
                    groq_key=groq_key,
                    gemini_key=gemini_key,
                )

            st.session_state.notes_pages = pages
            st.session_state.last_topic = topic.strip()
            st.session_state.last_subject = subject
            st.session_state.opened_page = None

            st.success(
                f"{len(pages)} notebook pages successfully generated!"
            )

        except Exception as exc:

            st.error(str(exc))

            st.info(
                "API key, model availability, internet connection aur "
                "provider quota check karo. Zarurat ho to doosra AI engine "
                "select karke dobara try karo."
            )


# ==================== GRID GALLERY ====================

pages = st.session_state.notes_pages

if pages:

    st.divider()

    st.subheader(
        f"🗂️ Notes Gallery — {st.session_state.last_topic}"
    )

    opened = st.session_state.opened_page

    if opened is not None and opened >= len(pages):

        st.session_state.opened_page = None
        st.rerun()

    if st.session_state.opened_page is not None:

        idx = st.session_state.opened_page

        page = pages[idx]

        st.markdown(
            f"### Page {idx + 1} of {len(pages)}"
        )

        page_html = render_page(
            page=page,
            page_no=idx + 1,
            topic=st.session_state.last_topic,
            subject=st.session_state.last_subject,
        )

        components.html(
            page_html,
            height=900,
            scrolling=True,
        )

        left, middle, right = st.columns([1, 2, 1])

        with left:

            if st.button(
                "← Previous",
                disabled=(idx == 0),
                use_container_width=True,
            ):

                st.session_state.opened_page = idx - 1
                st.rerun()

        with middle:

            if st.button(
                "▦ Back to Grid",
                use_container_width=True,
            ):

                st.session_state.opened_page = None
                st.rerun()

        with right:

            if st.button(
                "Next →",
                disabled=(idx >= len(pages) - 1),
                use_container_width=True,
            ):

                st.session_state.opened_page = idx + 1
                st.rerun()

        st.caption(
            "Page ko print karne ke liye browser mein Ctrl+P dabao "
            "aur Save as PDF select karo."
        )

    else:

        st.caption(
            "Kisi bhi page ko open karke full-size notes padho."
        )

        columns = st.columns(3)

        for i, page in enumerate(pages):

            with columns[i % 3]:

                st.markdown(
                    '<div class="page-card">',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"**📄 Notebook Page {i + 1}**"
                )

                preview_html = render_page(
                    page=page,
                    page_no=i + 1,
                    topic=st.session_state.last_topic,
                    subject=st.session_state.last_subject,
                )

                components.html(
                    preview_html,
                    height=760,
                    scrolling=True,
                )

                if st.button(
                    f"Open Page {i + 1}",
                    key=f"open_page_{i}",
                    use_container_width=True,
                ):

                    st.session_state.opened_page = i
                    st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("Troubleshooting"):

        st.markdown(
            """
            - **API key missing:** Add `GROQ_API_KEY` or `GEMINI_API_KEY`
              in Streamlit secrets, or enter the key in the sidebar.
            - **Model error:** Check the provider's current model access.
            - **Quota error:** Check your API usage and limits.
            - **Fonts not loading:** Internet access is required for
              Google Fonts. The page remains usable without them.
            - **Save PDF:** Open a page and use browser print.
            """
        )

else:

    st.info(
        "Topic enter karo aur Generate Handwritten Notes dabao. "
        "Tumhare pages yahan grid gallery mein appear honge."
    )
