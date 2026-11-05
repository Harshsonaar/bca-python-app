import streamlit as st
from groq import Groq
import google.generativeai as genai
import io
import re
import os
import json
import shelve
import threading
import time
import urllib.parse
import contextlib
from PIL import Image

st.set_page_config(
    page_title="Universal Academic & Competitive Suite | Harsh Raj Soni",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= PERSISTENT STORAGE =================
STORAGE_FILE = "user_memory_store.db"

def load_user_memory():
    default_data = {
        "last_course": "⚖️ Law & Judiciary (LL.B / CLAT / PCS-J)",
        "last_subject": "🏛️ Constitutional Law of India",
        "last_topic": "Fundamental Rights: Article 14 (Equality), Art 19 (Freedoms) & Art 21 (Life & Personal Liberty)",
        "study_history": {},
        "ai_memory": {}
    }
    try:
        with shelve.open(STORAGE_FILE) as db:
            return dict(db.get("user_state", default_data))
    except Exception:
        return default_data

def save_user_memory():
    try:
        with shelve.open(STORAGE_FILE) as db:
            db["user_state"] = {
                "last_course": st.session_state.current_course,
                "last_subject": st.session_state.current_subject,
                "last_topic": st.session_state.current_topic,
                "study_history": st.session_state.study_history,
                "ai_memory": st.session_state.ai_memory
            }
    except Exception:
        pass

# Initialize Session States
saved_state = load_user_memory()

if "system_booted" not in st.session_state:
    st.session_state.system_booted = False

if "current_course" not in st.session_state:
    st.session_state.current_course = saved_state.get("last_course", "⚖️ Law & Judiciary (LL.B / CLAT / PCS-J)")

if "current_subject" not in st.session_state:
    st.session_state.current_subject = saved_state.get("last_subject", "🏛️ Constitutional Law of India")

if "current_topic" not in st.session_state:
    st.session_state.current_topic = saved_state.get("last_topic", "")

if "study_history" not in st.session_state:
    st.session_state.study_history = saved_state.get("study_history", {})

if "ai_memory" not in st.session_state:
    st.session_state.ai_memory = saved_state.get("ai_memory", {})

if "generated_gallery_sheets" not in st.session_state:
    st.session_state.generated_gallery_sheets = []

if "active_sheet_index" not in st.session_state:
    st.session_state.active_sheet_index = None

if "active_exam_questions" not in st.session_state:
    st.session_state.active_exam_questions = []

if "exam_submitted" not in st.session_state:
    st.session_state.exam_submitted = False

if "dpp_questions" not in st.session_state:
    st.session_state.dpp_questions = []

if "dpp_user_answers" not in st.session_state:
    st.session_state.dpp_user_answers = {}

if "dpp_submitted" not in st.session_state:
    st.session_state.dpp_submitted = False

if "dpp_page" not in st.session_state:
    st.session_state.dpp_page = 0

if "pyq_questions" not in st.session_state:
    st.session_state.pyq_questions = []

if "pyq_user_answers" not in st.session_state:
    st.session_state.pyq_user_answers = {}

if "pyq_submitted" not in st.session_state:
    st.session_state.pyq_submitted = False

if "notebook_cells" not in st.session_state:
    st.session_state.notebook_cells = [
        {
            "id": 1,
            "code": "# Python Cell 1: Verification & Environment\ndeveloper_name = 'Harsh Raj Soni'\ninstitution = 'MLK PG College, Balrampur'\nprint(f'Academic Portal Active | Developer: {developer_name} [{institution}]')",
            "output": "",
            "error": ""
        }
    ]

# Anti-Sleep Keep Alive Heartbeat
def run_anti_sleep_heartbeat():
    while True:
        try:
            time.sleep(300)
        except Exception:
            pass

if "heartbeat_started" not in st.session_state:
    st.session_state.heartbeat_started = True
    t = threading.Thread(target=run_anti_sleep_heartbeat, daemon=True)
    t.start()

# ================= THEME PALETTES (EYE-FRIENDLY SOFT DARK GRADIENTS) =================
THEME_PALETTES = {
    "⚖️ Law & Judiciary (LL.B / CLAT / PCS-J)": {
        "grad_top": "#1F0D16",
        "grad_mid": "#14080E",
        "grad_base": "#090306",
        "accent": "#FB7185",
        "accent_dark": "#BE123C",
        "glow": "rgba(251, 113, 133, 0.22)",
        "card_bg": "rgba(31, 13, 22, 0.85)",
        "border": "#BE123C"
    },
    "🩺 NEET (Medical Entrance)": {
        "grad_top": "#062016",
        "grad_mid": "#04150E",
        "grad_base": "#020B07",
        "accent": "#34D399",
        "accent_dark": "#059669",
        "glow": "rgba(52, 211, 153, 0.22)",
        "card_bg": "rgba(6, 32, 22, 0.85)",
        "border": "#059669"
    },
    "⚙️ JEE (Main & Advanced)": {
        "grad_top": "#1C1308",
        "grad_mid": "#140D05",
        "grad_base": "#0A0602",
        "accent": "#FB923C",
        "accent_dark": "#EA580C",
        "glow": "rgba(251, 146, 60, 0.22)",
        "card_bg": "rgba(28, 19, 8, 0.85)",
        "border": "#EA580C"
    },
    "🎓 BCA (Computer Applications)": {
        "grad_top": "#0B132B",
        "grad_mid": "#080D1A",
        "grad_base": "#020617",
        "accent": "#38BDF8",
        "accent_dark": "#0284C7",
        "glow": "rgba(56, 189, 248, 0.25)",
        "card_bg": "rgba(15, 23, 42, 0.85)",
        "border": "#0284C7"
    },
    "🏛️ UPSC / Civil Services (CSAT & GS)": {
        "grad_top": "#1A0B2E",
        "grad_mid": "#110720",
        "grad_base": "#090311",
        "accent": "#C084FC",
        "accent_dark": "#9333EA",
        "glow": "rgba(192, 132, 252, 0.22)",
        "card_bg": "rgba(26, 11, 46, 0.85)",
        "border": "#9333EA"
    }
}

active_theme = THEME_PALETTES.get(st.session_state.current_course, THEME_PALETTES["⚖️ Law & Judiciary (LL.B / CLAT / PCS-J)"])

# ================= MASTER ACADEMIC & COMPETITIVE DATABASE =================
COURSE_DATABASE = {
    "⚖️ Law & Judiciary (LL.B / CLAT / PCS-J)": {
        "icon": "⚖️",
        "official_archive_url": "https://www.indiacode.nic.in/",
        "subjects": {
            "🏛️ Constitutional Law of India": {
                "units": (
                    "Part I-II (Art. 1–11): The Union, Territory & Citizenship | "
                    "Part III (Art. 12–35): Fundamental Rights & Prerogative Writs | "
                    "Part IV & IVA (Art. 36–51A): DPSP & Fundamental Duties | "
                    "Part V (Art. 52–151): President, Parliament, Supreme Court & CAG | "
                    "Part VI (Art. 152–237): Governor, State Legislature & High Courts | "
                    "Part XI–XII (Art. 245–300A): Centre-State Relations, Finance & Property | "
                    "Part XVIII & XX (Art. 352–368): Emergency Provisions & Constitutional Amendments | "
                    "Schedules 1 to 12 & Landmark Supreme Court Judgments"
                ),
                "topics": [
                    "Preamble, Basic Structure Doctrine (Kesavananda Bharati) & Article 368 Amendment Power",
                    "Fundamental Rights: Article 14 (Equality), Art 19 (Six Freedoms) & Art 21 (Life & Personal Liberty)",
                    "Constitutional Remedies: Article 32 vs Article 226 & 5 Prerogative Writs (Habeas Corpus to Quo Warranto)",
                    "Right to Freedom of Religion (Articles 25–28) & Cultural/Educational Rights (Articles 29–30)",
                    "Directive Principles (Art 36–51) vs Fundamental Rights Conflict & Harmonious Construction",
                    "Union & State Judiciary: Supreme Court (Art 124–147), High Courts (Art 214–231) & Collegium System",
                    "Emergency Provisions (Articles 352, 356, 360) & S.R. Bommai Guidelines",
                    "7th Schedule (Union, State, Concurrent Lists) & Doctrine of Pith and Substance / Colourable Legislation"
                ],
                "pyqs_years": [
                    "CLAT UG & PG 2025 (Official Consortium Paper)",
                    "UP PCS-J / Delhi Judicial Service 2024 (Official Paper)",
                    "All India Bar Examination (AIBE XIX / XVIII Official)",
                    "CUET LL.B / DU LL.B Entrance 2024 Official Paper"
                ]
            },
            "⚔️ Criminal Law (BNS, BNSS, BSA 2023 & IPC/CrPC/IEA)": {
                "units": (
                    "Bharatiya Nyaya Sanhita (BNS), 2023 [Sections 1–358] & Indian Penal Code (IPC), 1860 [Sections 1–511] | "
                    "Bharatiya Nagarik Suraksha Sanhita (BNSS), 2023 [Sections 1–531] & CrPC, 1973 [Sections 1–484] | "
                    "Bharatiya Sakshya Adhiniyam (BSA), 2023 [Sections 1–170] & Indian Evidence Act, 1872 [Sections 1–167] | "
                    "Special Criminal Statutes: POCSO Act, NDPS Act, PMLA & Juvenile Justice Act"
                ),
                "topics": [
                    "BNS 2023 vs IPC 1860: General Exceptions (Sec 14–44 BNS / Sec 76–106 IPC) & Right of Private Defence",
                    "Offences Affecting Human Body: Culpable Homicide vs Murder (Sec 100–103 BNS / Sec 299–302 IPC)",
                    "Offences Against Women & Children (Sec 63–99 BNS): Cruelty, Dowry Death & New Organised Crime/Terrorism (Sec 111–113 BNS)",
                    "Offences Against Property: Theft, Snatching (Sec 304 BNS), Extortion, Robbery, Dacoity & Criminal Breach of Trust (Sec 303–318 BNS)",
                    "Inchoate Offences & Joint Liability: Common Intention (Sec 3(5) BNS / Sec 34 IPC) vs Common Object (Sec 190 BNS / Sec 149 IPC)",
                    "BNSS 2023 (CrPC): Zero FIR, e-FIR (Sec 173 BNSS), Arrest, Police Custody/Remand (Sec 187 BNSS) & Mandatory Forensics (Sec 176(3) BNSS)",
                    "BNSS Bail Jurisprudence: Regular Bail, Anticipatory Bail (Sec 482 BNSS / 438 CrPC) & Default Bail",
                    "BSA 2023 (Evidence Act): Relevancy of Facts (Sec 3–50 BSA), Confessions, Dying Declaration (Sec 26 BSA / 32 IEA) & Electronic Evidence (Sec 61–63 BSA)"
                ],
                "pyqs_years": [
                    "Judiciary PCS-J Criminal Law 2025/2024 (BNS/BNSS/BSA & IPC/CrPC)",
                    "AIBE XIX / XVIII Criminal Law Official Paper",
                    "CLAT PG Criminal Jurisprudence Archive",
                    "UGC NET Law Paper-II Official Criminal Law"
                ]
            },
            "📜 Contract, Specific Relief & Property Law (ICA, SRA, TPA)": {
                "units": (
                    "Indian Contract Act, 1872 [Sec 1–75: General Principles; Sec 124–238: Indemnity, Guarantee, Bailment, Pledge & Agency] | "
                    "Specific Relief Act, 1963 (with 2018 Amendment) [Sec 1–44] | "
                    "Transfer of Property Act, 1882 [Sec 1–137: Sale, Mortgage, Lease, Exchange, Gift & Actionable Claims] | "
                    "Sale of Goods Act, 1930 [Sec 1–66] & Indian Partnership Act, 1932 [Sec 1–74]"
                ),
                "topics": [
                    "Indian Contract Act 1872 (Sec 1–30): Offer, Acceptance, Consideration (Sec 2(d)), Capacity (Mohori Bibee Case) & Free Consent (Sec 13–22)",
                    "Void, Voidable & Contingent Contracts (Sec 24–36), Doctrine of Frustration (Sec 56), Quasi-Contracts (Sec 68–72) & Breach Damages (Sec 73–75)",
                    "Special Contracts (Sec 124–238): Contract of Indemnity vs Guarantee, Bailment, Pledge & Principal-Agent Liability",
                    "Specific Relief Act 1963: Recovery of Possession (Sec 5–8), Specific Performance (Sec 10–24), Rectification, Rescission & Injunctions (Sec 36–42)",
                    "Transfer of Property Act 1882: Ostensible Owner (Sec 41), Doctrine of Election (Sec 35), Lis Pendens (Sec 52) & Part Performance (Sec 53A)",
                    "TPA Mortgages & Leases (Sec 58–117): Types of Mortgages, Right of Redemption (Once a Mortgage Always a Mortgage) & Determination of Lease"
                ],
                "pyqs_years": [
                    "PCS-J Civil Law Paper-I 2024 (Contract & TPA)",
                    "CLAT Legal Reasoning Official Paper 2025/2024",
                    "AIBE Contract, Specific Relief & Property Official Paper",
                    "AILET / Symbiosis SLAT Legal Aptitude Archive"
                ]
            },
            "⚖️ Civil Procedure (CPC), Limitation & Law of Torts": {
                "units": (
                    "Code of Civil Procedure (CPC), 1908 [Sections 1–158 & Schedule-I Orders I to LI] | "
                    "Limitation Act, 1963 [Sections 1–32 & Schedule of Periods] | "
                    "Law of Torts: General Defences, Negligence, Nuisance, Defamation, Strict & Absolute Liability | "
                    "Consumer Protection Act, 2019 [Sec 1–107] & Motor Vehicles Act, 1988"
                ),
                "topics": [
                    "CPC 1908 Jurisdiction & Res Judicata: Decree, Order, Mesne Profits (Sec 2), Res Sub Judice (Sec 10), Res Judicata (Sec 11) & Place of Suing (Sec 15–20)",
                    "CPC Stages of Civil Suit: Institution of Suit (Order IV), Summons (Order V), Pleadings (Order VI), Plaint Rejection (Order VII Rule 11) & Written Statement (Order VIII)",
                    "CPC Interim Orders & Execution: Temporary Injunctions (Order XXXIX Rules 1–5), Receiver (Order XL), Appeals (Sec 96–108), Review, Revision (Sec 113–115) & Execution (Order XXI)",
                    "Limitation Act 1963: Bar of Limitation (Sec 3), Condonation of Delay (Sec 5), Legal Disability (Sec 6–9) & Computation of Period (Sec 12–24)",
                    "Law of Torts: Damnum Sine Injuria vs Injuria Sine Damno, Volenti Non Fit Injuria, Strict Liability (Rylands v. Fletcher) vs Absolute Liability (M.C. Mehta Case)",
                    "Consumer Protection Act 2019: E-Commerce Rules, Product Liability (Sec 82–87) & Jurisdiction of District, State and National Commissions"
                ],
                "pyqs_years": [
                    "PCS-J Civil Procedure & Limitation Official Paper 2024",
                    "CLAT / AILET Law of Torts & Legal Maxims Paper",
                    "AIBE CPC & Consumer Protection Official Paper"
                ]
            },
            "👨‍👩‍👧 Family Law, Corporate Law, ADR & Jurisprudence": {
                "units": (
                    "Hindu Law: Hindu Marriage Act 1955 [Sec 1–30], Hindu Succession Act 1956 [Sec 1–31], Adoption & Maintenance Act 1956, Minority & Guardianship Act 1956 | "
                    "Muslim Law: Sources, Nikah, Mahr, Talaq, Dissolution of Muslim Marriages Act 1939, Waqf & Inheritance | "
                    "Corporate & Commercial Law: Companies Act 2013, Negotiable Instruments Act 1881 [Sec 138–148], Competition Act 2002 | "
                    "Arbitration & Conciliation Act 1996 [Sec 1–87], Intellectual Property Rights (Patents, Trademarks, Copyright) & Jurisprudence"
                ),
                "topics": [
                    "Hindu Marriage Act 1955: Conditions (Sec 5), Void/Voidable Marriages (Sec 11–12), Restitution of Conjugal Rights (Sec 9) & Divorce Grounds (Sec 13 & 13B Mutual Consent)",
                    "Hindu Succession Act 1956 (2005 Amendment): Mitakshara Coparcenary, Daughters as Coparceners (Sec 6 - Vineeta Sharma Judgment) & Female Intestate Succession (Sec 14–16)",
                    "Muslim Personal Law: Essentials of Nikah, Prompt vs Deferred Dower (Mahr), Triple Talaq Unconstitutionality (Shayara Bano Case) & Maintenance (Sec 144 BNSS / Danial Latifi)",
                    "Negotiable Instruments Act 1881: Promissory Note, Bill of Exchange, Cheque & Criminal Liability for Dishonour of Cheque (Sec 138–143A)",
                    "Companies Act 2013 & ADR: Doctrine of Lifting Corporate Veil, Indoor Management (Turquand Rule), Oppression/Mismanagement & Arbitration Act 1996 (Sec 7, 9, 11, 34)",
                    "Jurisprudence & Schools of Law: Analytical Positivism (Austin, Kelsen's Pure Theory, Hart), Historical (Savigny), Sociological (Roscoe Pound) & Natural Law"
                ],
                "pyqs_years": [
                    "PCS-J Family & Personal Law Official Paper 2024",
                    "CLAT PG Jurisprudence & Corporate Law Paper",
                    "AIBE Family Law, ADR & Company Law Official Paper"
                ]
            }
        }
    },
    "🩺 NEET (Medical Entrance)": {
        "icon": "🩺",
        "official_archive_url": "https://nta.ac.in/Downloads",
        "subjects": {
            "🧬 Zoology & Human Physiology": {
                "units": "Unit 1: Neural Control & Coordination | Unit 2: Chemical Coordination | Unit 3: Circulation & Body Fluids | Unit 4: Reproduction & Genetics",
                "topics": [
                    "Generation & Conduction of Nerve Impulse (Action Potential)",
                    "Sliding Filament Theory of Muscle Contraction",
                    "Cardiac Cycle, ECG Waveforms & Blood Pressure Regulation",
                    "Mendelian Dihybrid Cross, Linkage & Recombination",
                    "DNA Replication, Transcription & Genetic Code",
                    "Spermatogenesis vs Oogenesis & Hormonal Feedback Cycles"
                ],
                "pyqs_years": [
                    "NEET UG 2025 (Official Code Q/R/S/T)",
                    "NEET UG 2024 (Official Paper Set Q1-Q6)",
                    "NEET UG 2023 (Manipur & Main Official Paper)",
                    "NEET UG 2022 (Official NTA Paper)",
                    "NEET UG 2021 (Official Paper)"
                ]
            },
            "🌿 Botany & Plant Biology": {
                "units": "Unit 1: Plant Kingdom & Anatomy | Unit 2: Photosynthesis | Unit 3: Respiration | Unit 4: Plant Growth Regulators",
                "topics": [
                    "Light Reaction: Z-Scheme, Cyclic vs Non-Cyclic Photophosphorylation",
                    "Calvin Cycle (C3) vs Hatch-Slack Pathway (C4 Plants)",
                    "Glycolysis, Krebs Cycle (TCA) & Chemiosmotic Hypothesis",
                    "Double Fertilization & Embryo Sac Development in Angiosperms",
                    "Auxin, Cytokinin, Gibberellin Action & Photoperiodism"
                ],
                "pyqs_years": [
                    "NEET UG 2025 (Official Paper)",
                    "NEET UG 2024 (Official Paper)",
                    "NEET UG 2023 (Official Paper)",
                    "NEET UG 2022 (Official Paper)",
                    "NEET UG 2021 (Official Paper)"
                ]
            },
            "🧪 NEET Chemistry (Organic & Inorganic)": {
                "units": "Unit 1: Chemical Bonding | Unit 2: Periodic Table | Unit 3: Reaction Mechanisms | Unit 4: Biomolecules",
                "topics": [
                    "VSEPR Theory, Hybridization & Molecular Orbital Theory (MOT)",
                    "SN1 vs SN2 Reaction Mechanisms with Stereochemistry",
                    "Aldol Condensation, Cannizzaro Reaction & Mechanisms",
                    "Coordination Compounds, Werner Theory & Crystal Field Splitting (CFT)",
                    "Thermodynamics: Hess's Law, Gibbs Free Energy & Spontaneity"
                ],
                "pyqs_years": [
                    "NEET UG 2025 (Official Paper)",
                    "NEET UG 2024 (Official Paper)",
                    "NEET UG 2023 (Official Paper)",
                    "NEET UG 2022 (Official Paper)"
                ]
            },
            "⚛️ NEET Physics": {
                "units": "Unit 1: Kinematics & Mechanics | Unit 2: Electrodynamics | Unit 3: Optics & Modern Physics",
                "topics": [
                    "Projectile Motion & Relative Velocity in 2D",
                    "Newton's Laws, Friction & Circular Motion Dynamics",
                    "Ray Optics: Lens Maker Formula, Prism & Total Internal Reflection",
                    "Photoelectric Effect, de Broglie Wavelength & Bohr Model"
                ],
                "pyqs_years": [
                    "NEET UG 2025 (Official Paper)",
                    "NEET UG 2024 (Official Paper)",
                    "NEET UG 2023 (Official Paper)",
                    "NEET UG 2022 (Official Paper)"
                ]
            }
        }
    },
    "⚙️ JEE (Main & Advanced)": {
        "icon": "⚙️",
        "official_archive_url": "https://jeemain.nta.nic.in/",
        "subjects": {
            "📐 JEE Mathematics": {
                "units": "Unit 1: Coordinate Geometry | Unit 2: Calculus | Unit 3: Algebra & Vectors | Unit 4: Probability",
                "topics": [
                    "Conic Sections: Parabola, Ellipse & Tangent-Normal Equations",
                    "Definite Integration: King's Property, Leibnitz Rule & Reduction",
                    "Matrices, Determinants & System of Linear Equations (Cramer's Rule)",
                    "Complex Numbers: De Moivre Theorem, Geometry & Roots of Unity",
                    "Vectors & 3D Geometry: Shortest Distance Between Skew Lines"
                ],
                "pyqs_years": [
                    "JEE Main 2025 (Jan & April Shifts)",
                    "JEE Advanced 2024 (Paper 1 & Paper 2)",
                    "JEE Main 2024 (Jan 27 - Shift 1 & 2)",
                    "JEE Main 2023 (Official NTA Shifts)",
                    "JEE Advanced 2023 (Official Paper)"
                ]
            },
            "⚛️ JEE Physics": {
                "units": "Unit 1: Rotational Dynamics | Unit 2: Electromagnetism | Unit 3: Thermodynamics & SHM | Unit 4: Wave Optics",
                "topics": [
                    "Moment of Inertia, Parallel-Perpendicular Axis Theorems & Rolling",
                    "Gauss Law, Electrostatic Potential & Capacitance with Dielectrics",
                    "Ampere's Circuital Law, Biot-Savart & Magnetic Dipoles",
                    "Electromagnetic Induction, Faraday's Law & LC Oscillations",
                    "Wave Optics: Young's Double Slit Experiment (YDSE) & Phase Shift"
                ],
                "pyqs_years": [
                    "JEE Main 2025 (Jan & April Shifts)",
                    "JEE Advanced 2024 (Paper 1 & 2)",
                    "JEE Main 2024 (Official Shifts)",
                    "JEE Main 2023 (Official Shifts)"
                ]
            },
            "🧪 JEE Chemistry (Physical & Inorganic)": {
                "units": "Unit 1: Chemical Equilibrium & Kinetics | Unit 2: Electrochemistry | Unit 3: Coordination Chemistry",
                "topics": [
                    "Nernst Equation, Electrochemical Cells & Kohlrausch's Law",
                    "Chemical Kinetics: Integrated Rate Laws & Arrhenius Equation",
                    "Ionic Equilibrium: Buffer Solutions, pH Calculation & Solubility Product",
                    "Metallurgy: Ellingham Diagram & Extraction Principles"
                ],
                "pyqs_years": [
                    "JEE Main 2025 (Official Shifts)",
                    "JEE Advanced 2024 (Paper 1 & 2)",
                    "JEE Main 2024 (Official Shifts)",
                    "JEE Main 2023 (Official Shifts)"
                ]
            }
        }
    },
    "🎓 BCA (Computer Applications)": {
        "icon": "🎓",
        "official_archive_url": "https://www.eshiksha.mp.gov.in/",
        "subjects": {
            "🐍 Python Programming": {
                "units": "Unit 1: Bytecode & Internals | Unit 2: Loops & Logic | Unit 3: Functions & Scope | Unit 4: Data Structures | Unit 5: OOPs & Inheritance | Unit 6: File I/O",
                "topics": [
                    "Python Architecture, Bytecode & Memory Management",
                    "Control Flow, Loops, For-Else Logic & Prime Verification",
                    "Functions, Scopes, LEGB Resolution & Lambda Expressions",
                    "Data Structures: Lists, Tuples, Dictionaries & Sets",
                    "Object Oriented Programming: Encapsulation & Inheritance",
                    "File Handling, Context Managers & Exception Hierarchy"
                ],
                "pyqs_years": [
                    "BCA Semester Exam 2025 (Official University Paper)",
                    "BCA Semester Exam 2024 (Official University Paper)",
                    "BCA Semester Exam 2023 (Official University Paper)",
                    "BCA Semester Exam 2022 (Official University Paper)"
                ]
            },
            "🖥️ Computer System Architecture": {
                "units": "Unit 1: Binary Logic | Unit 2: Boolean Algebra & K-Maps | Unit 3: Combinational & Sequential Circuits | Unit 4: CPU Registers | Unit 5: Cache & Pipeline",
                "topics": [
                    "Full Adder Circuit, Logic Gates & Truth Table",
                    "Half Adder & Full Adder Design using 2 HA and 1 OR Gate",
                    "Number Systems, Complements & Binary Operations",
                    "K-Map 4-Variable Minimization & Grouping Rules",
                    "Flip-Flops, Master-Slave JK & Race-Around Condition",
                    "Instruction Cycle Phases & Cache Memory Mapping"
                ],
                "pyqs_years": [
                    "BCA CSA University Paper 2025",
                    "BCA CSA University Paper 2024",
                    "BCA CSA University Paper 2023"
                ]
            },
            "📐 Mathematics & Numerical Methods": {
                "units": "Unit 1: Matrices & Rank | Unit 2: Differential Calculus | Unit 3: Integral Calculus | Unit 4: Discrete Structures | Unit 5: Numerical Iterations",
                "topics": [
                    "Matrix Rank, Echelon Forms & Rouche-Capelli Consistency",
                    "L'Hopital's Rule for Indeterminate Forms with Solved Limit",
                    "Equivalence Relations Proof & POSET Hasse Diagrams",
                    "Eigenvalues, Eigenvectors & Cayley-Hamilton Theorem",
                    "Leibnitz Theorem for n-th Derivatives & Formula Matrix",
                    "Newton-Raphson Method & Numerical Convergence"
                ],
                "pyqs_years": [
                    "BCA Maths University Paper 2025",
                    "BCA Maths University Paper 2024",
                    "BCA Maths University Paper 2023"
                ]
            }
        }
    },
    "🏛️ UPSC / Civil Services (CSAT & GS)": {
        "icon": "🏛️",
        "official_archive_url": "https://upsc.gov.in/examinations/previous-question-papers",
        "subjects": {
            "📜 Indian Polity & Constitution": {
                "units": "Unit 1: Fundamental Rights | Unit 2: Parliament & Executive | Unit 3: Judiciary & Constitutional Bodies",
                "topics": [
                    "Fundamental Rights (Articles 14 to 32) & Basic Structure Doctrine",
                    "President vs Governor: Pardoning Powers & Discretionary Jurisdictions",
                    "Panchayati Raj (73rd & 74th Amendments) & Decentralization",
                    "Judicial Review, PIL & Collegium System Dynamics"
                ],
                "pyqs_years": [
                    "UPSC CSE Prelims 2025 (GS Paper-I Set A)",
                    "UPSC CSE Prelims 2024 (GS Paper-I Official)",
                    "UPSC CSE Prelims 2023 (GS Paper-I Official)",
                    "UPSC CSE Prelims 2022 (GS Paper-I Official)"
                ]
            },
            "🌍 Indian Economy & Geography": {
                "units": "Unit 1: Monetary & Fiscal Policy | Unit 2: Physical & Human Geography | Unit 3: Sustainable Development",
                "topics": [
                    "Inflation Targeting, Repo Rate & RBI Monetary Policy Tools",
                    "Fiscal Deficit, FRBM Act & Direct Tax Reforms (GST Architecture)",
                    "Monsoon Mechanism: Jet Streams, El Niño, La Niña & IOD"
                ],
                "pyqs_years": [
                    "UPSC CSE Prelims 2025 (GS Paper-I)",
                    "UPSC CSE Prelims 2024 (GS Paper-I)",
                    "UPSC CSE Prelims 2023 (GS Paper-I)"
                ]
            }
        }
    }
}

# ================= DYNAMIC EYE-FRIENDLY CSS =================
DYNAMIC_THEME_CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Kalam:wght@400;700&family=Patrick+Hand&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }}
    code, pre {{
        font-family: 'JetBrains Mono', monospace !important;
    }}

    .stApp {{
        background: radial-gradient(circle at 50% 0%, {active_theme['grad_top']} 0%, {active_theme['grad_mid']} 60%, {active_theme['grad_base']} 100%) !important;
        color: #F8FAFC;
        transition: background 0.5s ease-in-out;
    }}

    header[data-testid="stHeader"] {{display: none !important;}}
    footer {{display: none !important; visibility: hidden !important;}}
    .viewerBadge_container__1QSob, 
    .viewerBadge_link__1QSob,
    [data-testid="stStatusWidget"], 
    .stDeployButton,
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"],
    #MainMenu,
    div[class*="viewerBadge"] {{
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }}

    .block-container {{
        padding-top: 0.6rem !important;
        padding-bottom: 5rem !important;
        max-width: 1080px !important;
    }}

    .formal-top-banner {{
        background: {active_theme['card_bg']};
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 14px;
        padding: 12px 20px;
        backdrop-filter: blur(20px);
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }}
    .formal-author-pill {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid {active_theme['accent']};
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 11.5px;
        font-weight: 700;
        color: {active_theme['accent']};
        box-shadow: 0 0 16px {active_theme['glow']};
    }}

    .resume-state-card {{
        background: {active_theme['card_bg']};
        border: 1px dashed {active_theme['accent']};
        border-radius: 10px;
        padding: 8px 16px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 12.5px;
        color: {active_theme['accent']};
    }}

    /* Paper Question Card (OMR Style) */
    .question-card {{
        background: {active_theme['card_bg']};
        border: 1.5px solid rgba(255, 255, 255, 0.1);
        border-left: 4.5px solid {active_theme['accent']};
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 8px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.3);
    }}
    .question-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        padding-bottom: 6px;
    }}
    .q-number-tag {{
        background: {active_theme['glow']};
        border: 1px solid {active_theme['accent']};
        color: {active_theme['accent']};
        font-size: 12px;
        font-weight: 700;
        padding: 2px 10px;
        border-radius: 14px;
    }}
    .q-marks-tag {{
        font-size: 11px;
        color: #94A3B8;
        font-family: 'JetBrains Mono', monospace;
    }}
    .q-text {{
        font-size: 15px;
        font-weight: 600;
        line-height: 1.55;
        color: #F8FAFC;
        margin-bottom: 4px;
    }}

    .archive-link-box {{
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid {active_theme['accent']};
        border-radius: 10px;
        padding: 10px 16px;
        margin-bottom: 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px;
    }}
    .archive-link-box a {{
        color: {active_theme['accent']} !important;
        font-weight: 700;
        text-decoration: none;
        border: 1px solid {active_theme['accent']};
        padding: 4px 12px;
        border-radius: 6px;
        background: {active_theme['glow']};
        font-size: 12.5px;
    }}

    div[data-testid="stExpander"] {{
        background: {active_theme['card_bg']} !important;
        border: 1.5px solid {active_theme['border']} !important;
        border-radius: 12px !important;
        box-shadow: 0 0 18px {active_theme['glow']}, 0 8px 24px rgba(0, 0, 0, 0.5) !important;
        margin-bottom: 12px !important;
    }}

    div[data-testid="stRadio"] {{
        background: {active_theme['card_bg']} !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 6px 12px !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25) !important;
        margin-bottom: 12px !important;
    }}

    .stButton>button {{
        background: linear-gradient(135deg, {active_theme['accent_dark']} 0%, {active_theme['grad_top']} 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid {active_theme['accent']} !important;
        border-radius: 8px !important;
        padding: 6px 16px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 14px {active_theme['glow']} !important;
    }}
    .stButton>button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 6px 20px {active_theme['glow']} !important;
    }}

    .register-outer-center {{
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-top: 6px;
        margin-bottom: 12px;
    }}

    .real-notebook-sheet {{
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
        max-width: 480px !important;
        box-sizing: border-box !important;
        font-family: 'Patrick Hand', 'Kalam', cursive !important;
        color: #1e3a8a !important;
        font-size: 14.5px !important;
        line-height: 22px !important;
        position: relative !important;
        overflow: hidden !important;
    }}

    .real-notebook-sheet::before {{
        content: '' !important;
        position: absolute !important;
        top: 10px !important;
        left: 8px !important;
        width: 10px !important;
        height: 96% !important;
        background-image: radial-gradient(circle, #94a3b8 3px, transparent 4px) !important;
        background-size: 10px 22px !important;
        background-repeat: repeat-y !important;
    }}

    .nb-title-h1 {{
        font-family: 'Kalam', cursive !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #1e1b4b !important;
        background: #fdf2f8 !important;
        padding: 1px 10px !important;
        border-radius: 4px !important;
        display: inline-block !important;
        border-bottom: 2px dashed #ec4899 !important;
        margin-bottom: 3px !important;
        line-height: 23px !important;
    }}

    .nb-subhead {{
        font-weight: 700 !important;
        color: #0369a1 !important;
        font-size: 14.5px !important;
        text-decoration: underline !important;
        margin-top: 4px !important;
        display: block !important;
    }}

    .table-container {{
        width: 100% !important;
        overflow-x: auto !important;
        margin: 4px 0 !important;
        box-sizing: border-box !important;
    }}
    .nb-table {{
        border-collapse: collapse !important;
        font-family: 'Patrick Hand', cursive !important;
        font-size: 13.5px !important;
        line-height: 18px !important;
        background: #ffffff !important;
        border: 1.5px solid #1e3a8a !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }}
    .nb-table th, .nb-table td {{
        border: 1px solid #1e3a8a !important;
        padding: 3px 5px !important;
        text-align: center !important;
        word-break: break-word !important;
    }}
    .nb-table th {{
        background: #e0f2fe !important;
        color: #0369a1 !important;
        font-weight: 700 !important;
    }}

    .nb-keypoints-box {{
        border: 1.5px dashed #16a34a !important;
        background: #f0fdf4 !important;
        border-radius: 8px !important;
        padding: 6px 10px !important;
        margin-top: 6px !important;
        color: #14532d !important;
        font-size: 13px !important;
        line-height: 19px !important;
    }}
</style>
"""
st.markdown(DYNAMIC_THEME_CSS, unsafe_allow_html=True)

# ================= UNIVERSAL AI ENGINE =================
groq_key = st.secrets.get("GROQ_API_KEY", None)
gemini_key = st.secrets.get("GEMINI_API_KEY", None)

with st.sidebar:
    st.markdown("### ⚡ AI Engine & System")
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
    if image_input and gemini_key:
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("models/gemini-2.0-flash")
            response = model.generate_content([system_role + "\n\n" + user_prompt, image_input])
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            return "Gemini Vision Error: " + str(e)

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
                res = model.generate_content(system_role + "\n\n" + user_prompt)
                if res and res.text:
                    return res.text.strip()
            except Exception:
                pass
        return "Engine Error: " + str(last_err)

    elif gemini_key:
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("models/gemini-2.0-flash")
            response = model.generate_content(system_role + "\n\n" + user_prompt)
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            return "Gemini Error: " + str(e)

    return "⚠️ Pehle Sidebar mein Groq ya Gemini ki API Key add karein."

def fix_unclosed_html(html_str):
    open_divs = html_str.count("<div")
    close_divs = html_str.count("</div>")
    if open_divs > close_divs:
        html_str += "</div>" * (open_divs - close_divs)
    if "<table" in html_str and "</table" not in html_str:
        html_str += "</table>"
    if "<p" in html_str and "</p" not in html_str:
        html_str += "</p>"
    return html_str

def generate_multi_sheets_html(topic, subject_name, course_name, notes_lang):
    token_budget = 4500 if len(topic) < 30 else 6000
    last_ai_ctx = st.session_state.ai_memory.get(course_name, {}).get("last_summary", "No previous context.")

    law_instruction = ""
    if "Law" in course_name:
        law_instruction = (
            "Since this is Indian Law, strictly cite exact Bare Act Sections, Articles, BNS/BNSS/BSA 2023 equivalents alongside IPC/CrPC/IEA, "
            "and landmark Supreme Court case laws (with year) in the tables and key exam points. "
        )

    system_role = (
        "You are an esteemed professor and entrance mentor specializing in " + course_name + ". "
        "Strictly maintain academic dignity. " + law_instruction +
        "Student Context Memory: " + last_ai_ctx + ". "
        "Output EXACTLY 3 TO 4 INDIVIDUAL COMPLETE LECTURE SHEETS separated strictly by the token '===SHEET_SPLIT==='. "
        "Every single sheet MUST be 100% complete with all 4 sections fully finished: "
        "1. Definition & Core Statutory Provision, "
        "2. Bare Act Section / Formulation / Comparison Matrix, "
        "3. Step-by-Step Legal Ingredients / Derivation / Case Law Application, "
        "4. Key Exam Points / Landmark Judgments / Shortcuts. "
        "DO NOT USE CODE BLOCKS OR MARKDOWN TICKS. Start directly with <div class='register-outer-center'>."
    )
    user_prompt = (
        "Create a complete 3 to 4-sheet lecture register for '" + topic + "' under " + course_name + " -> " + subject_name + " (" + notes_lang + ").\n"
        "Ensure full tables and working steps are filled.\n\n"
        "TEMPLATE FOR EACH SHEET (Separate sheets strictly by ===SHEET_SPLIT===):\n"
        "<div class=\"register-outer-center\">\n"
        "    <div class=\"real-notebook-sheet\">\n"
        "        <div class=\"nb-title-h1\">" + topic + " [Part X]</div>\n"
        "        <div style=\"font-size:10.5px; color:#6b7280; margin-bottom:3px;\">" + course_name + " • " + subject_name + "</div>\n\n"
        "        <span class=\"nb-subhead\">1. Definition & Core Concept :</span>\n"
        "        <p style=\"margin: 2px 0 4px 0;\">[2 concise explanation lines in " + notes_lang + "]</p>\n\n"
        "        <span class=\"nb-subhead\">2. Statutory Sections / Table / Matrix :</span>\n"
        "        <div class=\"table-container\">\n"
        "            <table class=\"nb-table\">\n"
        "                <tr><th>Provision / Factor</th><th>Section / Parameter</th><th>Legal Effect / Output</th></tr>\n"
        "                <tr><td>Provision 1</td><td>Sec / Art Alpha</td><td>Binding / Valid</td></tr>\n"
        "                <tr><td>Provision 2</td><td>Sec / Art Beta</td><td>Exception</td></tr>\n"
        "            </table>\n"
        "        </div>\n\n"
        "        <span class=\"nb-subhead\">3. Essential Ingredients / Step-by-Step Working :</span>\n"
        "        <p style=\"margin: 2px 0 4px 0;\">\n"
        "            • Step 1: Core statutory ingredient or working logic<br>\n"
        "            • Step 2: Judicial interpretation / Formula execution path<br>\n"
        "            • Step 3: Practical problem / Case law rule\n"
        "        </p>\n\n"
        "        <div class=\"nb-keypoints-box\">\n"
        "            <b>✳ Key Exam Points & Landmark Cases :</b><br>\n"
        "            • High priority exam rule / Landmark SC Judgment<br>\n"
        "            • Key section / formula shortcut\n"
        "        </div>\n"
        "        <div style=\"font-size:10px; color:#9ca3af; text-align:right; margin-top:4px;\">Harsh Raj Soni • Universal Portal</div>\n"
        "    </div>\n"
        "</div>"
    )
    raw_res = execute_ai_query(system_role, user_prompt, max_budget=token_budget)
    
    clean_text = raw_res.replace("```html", "").replace("```HTML", "").replace("```", "").strip()
    clean_text = re.sub(r"^`+|`+$", "", clean_text)
    
    raw_sheets = [s.strip() for s in clean_text.split("===SHEET_SPLIT===") if s.strip()]
    
    sanitized_sheets = []
    for s in raw_sheets:
        fixed = fix_unclosed_html(s)
        sanitized_sheets.append(fixed)
        
    if course_name not in st.session_state.ai_memory:
        st.session_state.ai_memory[course_name] = {}
    st.session_state.ai_memory[course_name]["last_topic"] = topic
    st.session_state.ai_memory[course_name]["last_summary"] = "Recently studied " + topic + " in " + subject_name
    save_user_memory()
    
    return sanitized_sheets if sanitized_sheets else [clean_text]

# ================= JSON PARSER HELPER =================
def parse_mcq_json(raw_json):
    raw_json = re.sub(r"^```json\s*", "", raw_json, flags=re.IGNORECASE)
    raw_json = re.sub(r"^```\s*", "", raw_json)
    raw_json = re.sub(r"\s*```$", "", raw_json).strip()
    try:
        data = json.loads(raw_json)
        if isinstance(data, list):
            return data
    except Exception:
        pass
    match = re.search(r'\[\s*\{.*\}\s*\]', raw_json, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            pass
    return []

# ================= STRUCTURED EXAM / REAL PYQ / 90-100 DPP GENERATOR =================
def generate_batch_questions(topic, course_name, subject_name, count=15, batch_num=1, is_pyq=False, pyq_year=""):
    law_context = ""
    if "Law" in course_name:
        law_context = "Include exact Indian Bare Act Section numbers (including BNS/BNSS/BSA 2023 & IPC/CrPC/IEA where applicable), Constitutional Articles, Legal Maxims, and Landmark Supreme Court judgments."

    if is_pyq:
        mode_desc = (
            f"STRICTLY RECALL AND OUTPUT REAL VERBATIM QUESTIONS THAT APPEARED IN OFFICIAL {pyq_year} ({course_name}). "
            f"Include exact year and exam name in 'year_tag'. {law_context}"
        )
    else:
        sub_focus = [
            "Core Statutory Provisions, Bare Act Sections & Direct Principles",
            "Fact-Situation Legal Reasoning & Case Law Application",
            "Assertion-Reason & Statement-Based Analytical Questions",
            "Landmark Supreme Court Judgments, Maxims & Exceptions",
            "Advanced Judiciary / Rank-Decider Edge-Case Questions"
        ][(batch_num - 1) % 5]
        mode_desc = f"DPP Batch #{batch_num} focusing on: {sub_focus}. {law_context} Do not repeat previous questions."

    sys_prompt = (
        f"You are the Chief Question Paper Setter for {course_name}. "
        f"Output EXACTLY {count} multiple choice questions as a valid JSON array. "
        "NEVER output markdown tables or HTML. Output ONLY raw JSON array. "
        "Keep explanations crisp (1-2 lines citing exact section/case/formula) so all JSON objects fit cleanly. "
        "JSON Schema:\n"
        "[\n"
        "  {\n"
        '    "q_no": 1,\n'
        '    "year_tag": "DPP Set" or "CLAT/PCS-J Official",\n'
        '    "question": "Question text here",\n'
        '    "options": ["A. Option 1", "B. Option 2", "C. Option 3", "D. Option 4"],\n'
        '    "correct_option": "A. Option 1",\n'
        '    "explanation": "Concise section/case/formula explanation"\n'
        "  }\n"
        "]"
    )
    user_prompt = (
        f"Generate {count} distinct, high-yield MCQs for '{topic}' in {subject_name} ({course_name}). "
        f"Instruction: {mode_desc}"
    )
    raw_res = execute_ai_query(sys_prompt, user_prompt, max_budget=6000)
    return parse_mcq_json(raw_res)

def generate_90_100_dpp_marathon(topic, course_name, subject_name, target_count=90):
    all_questions = []
    batch_size = 18
    total_batches = (target_count + batch_size - 1) // batch_size

    progress_bar = st.progress(0, text=f"Initializing {target_count}-Question DPP Engine...")
    status_box = st.empty()

    for b in range(1, total_batches + 1):
        status_box.info(f"⚡ Compiling DPP Batch {b} of {total_batches} ({len(all_questions)}/{target_count} Questions Ready)...")
        batch_qs = generate_batch_questions(
            topic, course_name, subject_name, count=batch_size, batch_num=b, is_pyq=False
        )
        if batch_qs:
            for q in batch_qs:
                q["q_no"] = len(all_questions) + 1
                if "year_tag" not in q or not q["year_tag"]:
                    q["year_tag"] = f"DPP Batch-{b}"
                all_questions.append(q)
        progress_bar.progress(min(b / total_batches, 1.0), text=f"Loaded {len(all_questions)} Questions...")

    progress_bar.empty()
    status_box.empty()
    return all_questions

# ================= 0. INTRO SCREEN =================
if not st.session_state.system_booted:
    st.markdown(f"""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:70vh; text-align:center;">
        <div style="display:inline-flex; align-items:center; gap:8px; background:rgba(255,255,255,0.06); border:1px solid {active_theme['accent']}; padding:6px 20px; border-radius:30px; font-size:13px; font-weight:700; color:{active_theme['accent']}; margin-bottom:14px; box-shadow:0 0 16px {active_theme['glow']};">
            🎓 UNIVERSAL ACADEMIC, LAW & ENTRANCE SUITE
        </div>
        <div style="font-size:32px; font-weight:800; color:#F8FAFC; letter-spacing:-0.5px; margin-bottom:6px;">
            Created & Designed by Harsh Raj Soni
        </div>
        <div style="font-size:14px; color:#94A3B8; margin-bottom:24px;">
            LAW (LL.B/CLAT/PCS-J) • NEET • JEE • BCA • UPSC | MLK PG College, Balrampur
        </div>
        <div style="background:{active_theme['card_bg']}; border:1px solid rgba(255,255,255,0.1); border-left:4px solid {active_theme['accent']}; border-radius:10px; padding:16px 22px; max-width:600px; width:100%; text-align:left; font-size:13px; color:#CBD5E1; line-height:1.6; margin-bottom:24px;">
            <div style="color:{active_theme['accent']}; font-weight:700; margin-bottom:4px;">Enterprise Features Active:</div>
            <div>• ⚖️ Complete Indian Law Stream (Constitution, BNS/BNSS/BSA 2023, IPC/CrPC, Contract, CPC, Torts, Family Law)</div>
            <div>• 🔥 90–100 Questions DPP Marathon Generator (All Streams)</div>
            <div>• 📚 Real Official PYQ Papers + India Code & NTA Direct Archives</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        if st.button("Enter Learning Ecosystem", use_container_width=True):
            st.session_state.system_booted = True
            st.rerun()

else:
    # Top Executive Bar
    st.markdown(f"""
    <div class="formal-top-banner">
        <div>
            <div style="font-size: 18px; font-weight: 700; color: #F8FAFC;">
                Universal Academic, Law & Competitive Portal
            </div>
            <div style="font-size: 12px; color: #94A3B8;">
                Indian Law Bare Acts • 90–100 Qs DPP Engine • Real Internet PYQ Vault
            </div>
        </div>
        <div class="formal-author-pill">
            Developer: Harsh Raj Soni
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Persistent Resume Notification
    if st.session_state.current_topic:
        st.markdown(
            '<div class="resume-state-card">'
            '<span>📌 <b>Resumed Session:</b> ' + st.session_state.current_course + ' ➔ ' + st.session_state.current_subject + ' (Last Topic: <i>' + st.session_state.current_topic + '</i>)</span>'
            '<span>Auto-Saved ●</span>'
            '</div>',
            unsafe_allow_html=True
        )

    # ================= COURSE SWITCHER =================
    curr_course = st.session_state.current_course
    with st.expander("🎓 Active Stream: " + curr_course + " (Tap to Switch)", expanded=False):
        c_list = list(COURSE_DATABASE.keys())
        cols = st.columns(len(c_list))
        for idx, crs in enumerate(c_list):
            with cols[idx]:
                is_active = (crs == curr_course)
                if st.button(crs, key="course_btn_" + str(idx), use_container_width=True, type="primary" if is_active else "secondary"):
                    st.session_state.current_course = crs
                    st.session_state.current_subject = list(COURSE_DATABASE[crs]["subjects"].keys())[0]
                    st.session_state.current_topic = ""
                    st.session_state.generated_gallery_sheets = []
                    st.session_state.active_sheet_index = None
                    st.session_state.active_exam_questions = []
                    st.session_state.dpp_questions = []
                    st.session_state.pyq_questions = []
                    save_user_memory()
                    st.rerun()

    active_course_data = COURSE_DATABASE[st.session_state.current_course]

    # Subject Selector
    available_subjects = list(active_course_data["subjects"].keys())
    if st.session_state.current_subject not in available_subjects:
        st.session_state.current_subject = available_subjects[0]

    with st.expander("📚 Active Subject: " + st.session_state.current_subject + " (Tap to Switch)", expanded=False):
        sub_cols = st.columns(len(available_subjects))
        for s_idx, s_name in enumerate(available_subjects):
            with sub_cols[s_idx]:
                is_sub_active = (s_name == st.session_state.current_subject)
                if st.button(s_name, key="sub_btn_" + str(s_idx), use_container_width=True, type="primary" if is_sub_active else "secondary"):
                    st.session_state.current_subject = s_name
                    st.session_state.current_topic = ""
                    st.session_state.generated_gallery_sheets = []
                    st.session_state.active_sheet_index = None
                    st.session_state.active_exam_questions = []
                    st.session_state.dpp_questions = []
                    st.session_state.pyq_questions = []
                    save_user_memory()
                    st.rerun()

    active_course = st.session_state.current_course
    active_subj = st.session_state.current_subject
    subject_details = active_course_data["subjects"][active_subj]

    # Navigation Dock
    ref_tab_label = "⚖️ Bare Acts & Maxims" if "Law" in active_course else "🔬 Formula & Lab"
    nav_options = [
        "📝 Notes Gallery",
        "🔥 DPP (90-100 Qs)",
        "📚 Real PYQs Vault",
        "🎯 Mock Exam",
        "📖 Syllabus & Acts",
        ref_tab_label,
        "🤖 AI Mentor"
    ]
    if "Python" in active_subj:
        nav_options.append("💻 Sandbox")

    selected_nav = st.radio(
        label="Navigation Section",
        options=nav_options,
        horizontal=True,
        index=0
    )

    # ================= SECTION 1: NOTES GALLERY =================
    if selected_nav == "📝 Notes Gallery":
        st.markdown("#### 📖 Lecture Notes Register Gallery — " + active_subj)
        st.caption("Classmate ruled paper layout with Bare Act sections, tables, formulas, and key exam points.")

        c1, c2 = st.columns([2.5, 1])
        with c1:
            suggested = subject_details.get("topics", [])
            chosen_topic = st.selectbox("Curated Topic List:", suggested)
            custom_topic = st.text_input("Or Type ANY Custom Topic / Section / Act:", placeholder="e.g. Section 103 BNS vs 302 IPC / Article 21 / Doctrine of Eclipse")
        with c2:
            notes_lang = st.selectbox("Language:", ["Hinglish", "English", "Hindi"])

        final_topic = custom_topic.strip() if custom_topic.strip() else chosen_topic

        if st.button("Generate Lecture Register Sheets", use_container_width=True):
            st.session_state.current_topic = final_topic
            st.session_state.active_sheet_index = None
            save_user_memory()

            with st.spinner("Writing complete lecture sheets for '" + final_topic + "' under " + active_course + "..."):
                st.session_state.generated_gallery_sheets = generate_multi_sheets_html(
                    final_topic, active_subj, active_course, notes_lang
                )

        if st.session_state.generated_gallery_sheets:
            sheets = st.session_state.generated_gallery_sheets
            total_sheets = len(sheets)

            if st.session_state.active_sheet_index is not None:
                cur_i = st.session_state.active_sheet_index
                st.markdown("##### 🔍 Viewing Sheet " + str(cur_i + 1) + " of " + str(total_sheets))
                st.html(sheets[cur_i])

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
            else:
                st.markdown("##### 📸 Register Sheets Gallery (" + str(total_sheets) + " Sheets)")
                st.caption("Kisi bhi sheet par tap karein full-size padhne ke liye:")
                grid_cols = st.columns(3)
                for idx, sheet_code in enumerate(sheets):
                    with grid_cols[idx % 3]:
                        if st.button("📄 Sheet " + str(idx + 1) + " (Tap to Open)", key="sheet_btn_" + str(idx), use_container_width=True):
                            st.session_state.active_sheet_index = idx
                            st.rerun()
                        card_thumb = f"""
                        <div style="border:1.5px solid {active_theme['accent']}; border-radius:8px; padding:10px; background:{active_theme['card_bg']}; text-align:center; margin-bottom:12px; box-shadow:0 0 10px {active_theme['glow']};">
                            <span style="font-size:13.5px; color:{active_theme['accent']}; font-weight:700;">Sheet #{idx + 1}</span><br>
                            <span style="font-size:11px; color:#94A3B8;">Ruled Lecture Register</span>
                        </div>
                        """
                        st.markdown(card_thumb, unsafe_allow_html=True)

    # ================= SECTION 2: DPP (90-100 QUESTIONS MARATHON ENGINE) =================
    elif selected_nav == "🔥 DPP (90-100 Qs)":
        st.markdown(f"#### 🔥 Daily Practice Problems (DPP Marathon) — {active_subj}")
        st.caption("Full chapter practice sheet with 90–100 questions, OMR option tick, and paginated smooth view.")

        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            dpp_topic_list = subject_details.get("topics", [])
            sel_dpp_topic = st.selectbox("Select Chapter / Act for DPP:", dpp_topic_list)
            custom_dpp = st.text_input("Or Enter Custom Act / Chapter:", placeholder="e.g. Complete BNS 2023 Offences / Indian Contract Act Sec 1-75")
        with c2:
            dpp_target_count = st.selectbox("DPP Sheet Size:", [90, 100, 50], index=0)
        with c3:
            page_size = st.selectbox("Questions Per Page:", [20, 25, 50, 100], index=1)

        final_dpp_topic = custom_dpp.strip() if custom_dpp.strip() else sel_dpp_topic

        col_btn1, col_btn2 = st.columns([2, 1])
        with col_btn1:
            if st.button(f"🚀 Generate Full {dpp_target_count}-Question DPP Sheet", use_container_width=True):
                st.session_state.current_topic = final_dpp_topic
                save_user_memory()
                st.session_state.dpp_questions = generate_90_100_dpp_marathon(
                    final_dpp_topic, active_course, active_subj, target_count=dpp_target_count
                )
                st.session_state.dpp_user_answers = {}
                st.session_state.dpp_submitted = False
                st.session_state.dpp_page = 0
                st.rerun()
        with col_btn2:
            if st.session_state.dpp_questions and len(st.session_state.dpp_questions) < 100:
                if st.button("➕ Append 20 More Questions", use_container_width=True):
                    with st.spinner("Adding 20 more questions to current DPP..."):
                        extra = generate_batch_questions(
                            final_dpp_topic, active_course, active_subj, count=20,
                            batch_num=(len(st.session_state.dpp_questions) // 18) + 1
                        )
                        for q in extra:
                            q["q_no"] = len(st.session_state.dpp_questions) + 1
                            st.session_state.dpp_questions.append(q)
                        st.rerun()

        if st.session_state.dpp_questions:
            dpp_list = st.session_state.dpp_questions
            total_dpp = len(dpp_list)
            total_pages = max(1, (total_dpp + page_size - 1) // page_size)
            cur_page = min(st.session_state.dpp_page, total_pages - 1)

            start_idx = cur_page * page_size
            end_idx = min(start_idx + page_size, total_dpp)

            answered_count = len([v for v in st.session_state.dpp_user_answers.values() if v is not None])
            st.markdown(f"**📋 Active DPP Sheet:** `{final_dpp_topic}` | **Total Questions:** `{total_dpp}` | **Attempted:** `{answered_count}/{total_dpp}` | **Page:** `{cur_page + 1}/{total_pages}`")

            p_c1, p_c2, p_c3 = st.columns([1, 2, 1])
            with p_c1:
                if st.button("⬅️ Previous Page", disabled=(cur_page == 0), key="dpp_prev_top", use_container_width=True):
                    st.session_state.dpp_page = max(0, cur_page - 1)
                    st.rerun()
            with p_c3:
                if st.button("Next Page ➡️", disabled=(cur_page >= total_pages - 1), key="dpp_next_top", use_container_width=True):
                    st.session_state.dpp_page = min(total_pages - 1, cur_page + 1)
                    st.rerun()

            for idx in range(start_idx, end_idx):
                q_data = dpp_list[idx]
                q_num = idx + 1
                st.markdown(f"""
                <div class="question-card">
                    <div class="question-header">
                        <span class="q-number-tag">DPP Q.{q_num} • {q_data.get('year_tag', 'Core DPP')}</span>
                        <span class="q-marks-tag">+4 / -1 OMR</span>
                    </div>
                    <div class="q-text">{q_data.get('question', '')}</div>
                </div>
                """, unsafe_allow_html=True)

                opts = q_data.get("options", [])
                prev_choice = st.session_state.dpp_user_answers.get(idx, None)
                opt_index = opts.index(prev_choice) if prev_choice in opts else None

                chosen = st.radio(
                    f"Tick Option for Q.{q_num}:",
                    options=opts,
                    index=opt_index,
                    key=f"dpp_radio_{idx}"
                )
                st.session_state.dpp_user_answers[idx] = chosen

                if st.session_state.dpp_submitted:
                    correct = q_data.get("correct_option", "")
                    if chosen == correct:
                        st.success(f"✔ **Correct!** ({correct})")
                    else:
                        st.error(f"✖ **Incorrect / Unattempted.** Official Key: {correct} | Your Tick: {chosen if chosen else 'None'}")
                    with st.expander(f"💡 Solution for Q.{q_num}", expanded=False):
                        st.write(q_data.get("explanation", "Refer to statutory section / standard derivation."))

            b_c1, b_c2, b_c3 = st.columns([1, 2, 1])
            with b_c1:
                if st.button("⬅️ Prev Page", disabled=(cur_page == 0), key="dpp_prev_bot", use_container_width=True):
                    st.session_state.dpp_page = max(0, cur_page - 1)
                    st.rerun()
            with b_c2:
                if st.button("📝 Submit Entire DPP & Calculate Rank Score", type="primary", use_container_width=True):
                    st.session_state.dpp_submitted = True
                    st.rerun()
            with b_c3:
                if st.button("Next Page ➡️", disabled=(cur_page >= total_pages - 1), key="dpp_next_bot", use_container_width=True):
                    st.session_state.dpp_page = min(total_pages - 1, cur_page + 1)
                    st.rerun()

            if st.session_state.dpp_submitted:
                correct_cnt = sum(1 for i, q in enumerate(dpp_list) if st.session_state.dpp_user_answers.get(i) == q.get("correct_option"))
                wrong_cnt = sum(1 for i, q in enumerate(dpp_list) if st.session_state.dpp_user_answers.get(i) and st.session_state.dpp_user_answers.get(i) != q.get("correct_option"))
                unattempted = total_dpp - (correct_cnt + wrong_cnt)
                total_marks = (correct_cnt * 4) - (wrong_cnt * 1)
                max_marks = total_dpp * 4

                st.markdown(f"""
                <div style="background:{active_theme['card_bg']}; border:2px solid {active_theme['accent']}; border-radius:12px; padding:18px 24px; text-align:center; margin-top:20px; box-shadow:0 0 20px {active_theme['glow']};">
                    <h3 style="color:{active_theme['accent']}; margin-bottom:6px;">📊 DPP Marathon Scorecard ({total_dpp} Questions)</h3>
                    <div style="font-size:24px; font-weight:800; color:#F8FAFC; margin-bottom:12px;">Score: {total_marks} / {max_marks}</div>
                    <div style="display:flex; justify-content:center; gap:20px; font-size:13px; color:#CBD5E1;">
                        <span>✔ Correct: <b style="color:#34D399;">{correct_cnt}</b></span>
                        <span>✖ Wrong: <b style="color:#EF4444;">{wrong_cnt}</b></span>
                        <span>⚪ Left: <b style="color:#94A3B8;">{unattempted}</b></span>
                        <span>🎯 Accuracy: <b>{int((correct_cnt/total_dpp)*100) if total_dpp else 0}%</b></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ================= SECTION 3: REAL INTERNET PYQS VAULT =================
    elif selected_nav == "📚 Real PYQs Vault":
        st.markdown(f"#### 📚 Official Past Question Papers (Internet Archive + Interactive OMR) — {active_course}")
        st.caption("Download real original PDF papers & Bare Acts from the internet or solve verbatim official past questions right here.")

        pyqs_list = subject_details.get("pyqs_years", ["2024 Official Paper"])
        c1, c2 = st.columns([2, 1])
        with c1:
            chosen_year = st.selectbox("Select Official Exam Paper:", pyqs_list)
            pyq_topic = st.text_input("Specific Act / Chapter Filter (Leave blank for Full Paper):", placeholder="e.g. Fundamental Rights / BNS & IPC / Contract Act")
        with c2:
            pyq_count = st.selectbox("Questions to Load:", [20, 40, 60], index=0)

        encoded_query = urllib.parse.quote(f"{chosen_year} {active_subj} official question paper pdf download")
        google_pdf_url = f"https://www.google.com/search?q={encoded_query}"
        official_portal_url = active_course_data.get("official_archive_url", "https://www.indiacode.nic.in/")

        archive_btn_label = "🏛️ India Code (Official Bare Acts)" if "Law" in active_course else "🏛️ Official Exam Archive"

        st.markdown(f"""
        <div class="archive-link-box">
            <div>
                <div style="font-size:13.5px; font-weight:700; color:#F8FAFC;">🌐 Direct Internet Official Question Paper PDFs ({chosen_year})</div>
                <div style="font-size:11.5px; color:#94A3B8;">Open original scanned exam booklet PDFs and official Government portals:</div>
            </div>
            <div style="display:flex; gap:10px;">
                <a href="{google_pdf_url}" target="_blank">📄 Download {chosen_year} PDF</a>
                <a href="{official_portal_url}" target="_blank">{archive_btn_label}</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

        target_topic = pyq_topic.strip() if pyq_topic.strip() else f"Full {active_subj} Syllabus"

        if st.button(f"📥 Load {pyq_count} Verbatim Questions from {chosen_year} (Interactive OMR)", use_container_width=True):
            all_pyqs = []
            batches = (pyq_count + 19) // 20
            prog = st.progress(0, text=f"Fetching verbatim questions from {chosen_year}...")
            for b in range(1, batches + 1):
                chunk = generate_batch_questions(
                    target_topic, active_course, active_subj, count=min(20, pyq_count - len(all_pyqs)),
                    batch_num=b, is_pyq=True, pyq_year=chosen_year
                )
                for q in chunk:
                    q["q_no"] = len(all_pyqs) + 1
                    all_pyqs.append(q)
                prog.progress(min(b / batches, 1.0))
            prog.empty()
            st.session_state.pyq_questions = all_pyqs
            st.session_state.pyq_user_answers = {}
            st.session_state.pyq_submitted = False
            st.rerun()

        if st.session_state.pyq_questions:
            q_list = st.session_state.pyq_questions
            st.markdown(f"### 🏛️ {chosen_year} — Interactive OMR Booklet ({len(q_list)} Questions)")

            for idx, q_data in enumerate(q_list):
                q_num = idx + 1
                st.markdown(f"""
                <div class="question-card">
                    <div class="question-header">
                        <span class="q-number-tag">Q.{q_num} • {q_data.get('year_tag', chosen_year)}</span>
                        <span class="q-marks-tag">Official Marking: +4 / -1</span>
                    </div>
                    <div class="q-text">{q_data.get('question', '')}</div>
                </div>
                """, unsafe_allow_html=True)

                opts = q_data.get("options", [])
                prev_ans = st.session_state.pyq_user_answers.get(idx, None)
                opt_i = opts.index(prev_ans) if prev_ans in opts else None

                sel_ans = st.radio(
                    f"Tick OMR Answer for PYQ #{q_num}:",
                    options=opts,
                    index=opt_i,
                    key=f"pyq_radio_{idx}"
                )
                st.session_state.pyq_user_answers[idx] = sel_ans

                if st.session_state.pyq_submitted:
                    correct = q_data.get("correct_option", "")
                    if sel_ans == correct:
                        st.success(f"✔ **Correct!** Official Key: {correct}")
                    else:
                        st.error(f"✖ **Incorrect / Skipped.** Official Key: {correct} (You ticked: {sel_ans if sel_ans else 'None'})")

                    with st.expander(f"💡 View Official Solution #{q_num}", expanded=True):
                        st.write(q_data.get("explanation", "Standard statutory provision & case law rationale."))

            if st.button("📝 Submit Official PYQ Paper & Check Score", type="primary", use_container_width=True):
                st.session_state.pyq_submitted = True
                st.rerun()

            if st.session_state.pyq_submitted:
                total_q = len(q_list)
                correct_cnt = sum(1 for i, q in enumerate(q_list) if st.session_state.pyq_user_answers.get(i) == q.get("correct_option"))
                wrong_cnt = sum(1 for i, q in enumerate(q_list) if st.session_state.pyq_user_answers.get(i) and st.session_state.pyq_user_answers.get(i) != q.get("correct_option"))
                total_marks = (correct_cnt * 4) - (wrong_cnt * 1)
                max_marks = total_q * 4

                st.markdown(f"""
                <div style="background:{active_theme['card_bg']}; border:2px solid {active_theme['accent']}; border-radius:12px; padding:18px 24px; text-align:center; margin-top:20px; box-shadow:0 0 20px {active_theme['glow']};">
                    <h3 style="color:{active_theme['accent']}; margin-bottom:6px;">📊 {chosen_year} Performance Report</h3>
                    <div style="font-size:24px; font-weight:800; color:#F8FAFC; margin-bottom:12px;">Score: {total_marks} / {max_marks}</div>
                    <div style="display:flex; justify-content:center; gap:20px; font-size:13px; color:#CBD5E1;">
                        <span>✔ Correct: <b style="color:#34D399;">{correct_cnt}</b></span>
                        <span>✖ Negative: <b style="color:#EF4444;">{wrong_cnt}</b></span>
                        <span>🎯 Accuracy: <b>{int((correct_cnt/total_q)*100) if total_q else 0}%</b></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ================= SECTION 4: QUICK MOCK EXAM =================
    elif selected_nav == "🎯 Mock Exam":
        st.markdown(f"#### 🎯 Rapid Mock Test — {active_course}")
        c1, c2 = st.columns([2.5, 1])
        with c1:
            exam_topic = st.text_input("Scope / Act / Chapter for Test:", value=st.session_state.current_topic if st.session_state.current_topic else active_subj)
        with c2:
            mock_q_cnt = st.selectbox("Questions:", [10, 15, 25], index=1)

        if st.button("Generate Quick Mock Paper", use_container_width=True):
            with st.spinner("Generating clean MCQ examination paper..."):
                st.session_state.active_exam_questions = generate_batch_questions(
                    exam_topic, active_course, active_subj, count=mock_q_cnt, batch_num=1, is_pyq=False
                )
                st.session_state.exam_submitted = False
                st.rerun()

        if st.session_state.active_exam_questions:
            q_list = st.session_state.active_exam_questions
            user_answers = {}

            for idx, q_data in enumerate(q_list):
                q_num = idx + 1
                st.markdown(f"""
                <div class="question-card">
                    <div class="question-header">
                        <span class="q-number-tag">Question {q_num}</span>
                        <span class="q-marks-tag">Marks: +4 / -1</span>
                    </div>
                    <div class="q-text">{q_data.get('question', '')}</div>
                </div>
                """, unsafe_allow_html=True)

                opts = q_data.get("options", [])
                user_answers[idx] = st.radio(
                    f"Select Answer for Q.{q_num}:",
                    options=opts,
                    key=f"mock_q_{idx}",
                    index=None
                )

                if st.session_state.exam_submitted:
                    correct = q_data.get("correct_option", "")
                    selected = user_answers.get(idx)
                    if selected == correct:
                        st.success(f"✔ **Correct!** Answer: {correct}")
                    else:
                        st.error(f"✖ **Incorrect / Skipped.** Correct: {correct}")
                    with st.expander(f"💡 Explanation for Q.{q_num}", expanded=True):
                        st.write(q_data.get("explanation", ""))

            if st.button("📝 Submit Mock Test", type="primary", use_container_width=True):
                st.session_state.exam_submitted = True
                st.rerun()

    # ================= SECTION 5: SYLLABUS & ACTS BREAKDOWN =================
    elif selected_nav == "📖 Syllabus & Acts":
        st.markdown("#### 📚 Complete Statutory & Curriculum Breakdown — " + active_course)
        st.info("Active Subject: **" + active_subj + "**")
        st.write(subject_details.get("units", "Comprehensive syllabus mapped to national standards."))

        with st.expander("📌 View Complete Stream Breakdown (" + active_course + ")", expanded=True):
            for s_k, s_v in active_course_data["subjects"].items():
                st.markdown(f"**{s_k}**")
                st.caption(s_v.get("units", ""))
                st.markdown("---")

    # ================= SECTION 6: BARE ACTS & MAXIMS / FORMULA LAB =================
    elif selected_nav == ref_tab_label:
        if "Law" in active_course:
            st.markdown("#### ⚖️ Indian Bare Acts, BNS-IPC Section Mapper & Legal Maxims")
            with st.expander("⚔️ New Criminal Laws (2023) vs Old Laws — Master Section Comparison", expanded=True):
                st.markdown("""
                * **Common Intention:** `Section 3(5) BNS 2023` ⬅️ *Earlier Section 34 IPC 1860*
                * **Private Defence of Body & Property:** `Sections 34 to 44 BNS 2023` ⬅️ *Earlier Sections 96 to 106 IPC 1860*
                * **Culpable Homicide & Murder:** `Sections 100 & 101 BNS 2023` ⬅️ *Earlier Sections 299 & 300 IPC 1860*
                * **Punishment for Murder:** `Section 103 BNS 2023` ⬅️ *Earlier Section 302 IPC 1860*
                * **Causing Death by Negligence:** `Section 106 BNS 2023` ⬅️ *Earlier Section 304A IPC 1860*
                * **Organised Crime & Terrorist Act (New):** `Sections 111 & 113 BNS 2023`
                * **Defamation:** `Section 356 BNS 2023` ⬅️ *Earlier Section 499/500 IPC 1860*
                * **Zero FIR & e-FIR Registration:** `Section 173 BNSS 2023` ⬅️ *Earlier Section 154 CrPC 1973*
                * **Order for Maintenance of Wives, Children & Parents:** `Section 144 BNSS 2023` ⬅️ *Earlier Section 125 CrPC 1973*
                * **Anticipatory Bail:** `Section 482 BNSS 2023` ⬅️ *Earlier Section 438 CrPC 1973*
                * **Dying Declaration:** `Section 26(a) BSA 2023` ⬅️ *Earlier Section 32(1) Indian Evidence Act 1872*
                * **Electronic & Digital Records Admissibility:** `Sections 61 & 63 BSA 2023` ⬅️ *Earlier Section 65B Evidence Act*
                """)

            with st.expander("🏛️ High-Yield Latin Legal Maxims for CLAT / Judiciary"):
                st.markdown("""
                * **Actus Non Facit Reum Nisi Mens Sit Rea:** An act does not make a person guilty unless there is a guilty mind.
                * **Ubi Jus Ibi Remedium:** Where there is a right, there is a remedy (*Ashby v. White*).
                * **Injuria Sine Damno:** Infringement of an absolute legal right without actual physical damage (Actionable).
                * **Damnum Sine Injuria:** Actual financial/physical loss without infringement of a legal right (Not actionable — *Gloucester Grammar School Case*).
                * **Volenti Non Fit Injuria:** To a willing person, injury is not done (Defence of consent in Torts).
                * **Res Ipsa Loquitur:** The thing speaks for itself (Presumption of negligence).
                * **Nemo Judex In Causa Sua & Audi Alteram Partem:** No one shall be a judge in their own cause & Hear the other side (Principles of Natural Justice).
                * **Ignorantia Facti Excusat, Ignorantia Juris Non Excusat:** Ignorance of fact is an excuse, ignorance of law is no excuse (Sec 14 & 17 BNS / Sec 76 & 79 IPC).
                """)

            st.markdown("##### 🔍 Instant Bare Act Section / Article / Case Law Finder")
            bare_query = st.text_input("Enter any Section, Article, or Act (e.g. 'Section 138 NI Act', 'Article 21', 'Section 103 BNS'):")
            if st.button("Fetch Exact Bare Act Text & Landmark Cases", use_container_width=True):
                if bare_query.strip():
                    with st.spinner("Searching Indian Statutory Database..."):
                        sys_p = "You are an Indian Legal Encyclopedia & Senior Advocate. Provide the exact Bare Act text, essential ingredients, punishment/remedy, BNS/IPC parallel (if criminal), and top 2 Supreme Court landmark judgments."
                        st.info(execute_ai_query(sys_p, f"Explain Indian Law provision: {bare_query}"))
        else:
            st.markdown("#### 🔬 Formula & Concepts Compendium — " + active_subj)
            with st.expander("⚡ Core Formulation & Important Matrix", expanded=True):
                if "Math" in active_subj:
                    st.latex(r"\frac{d}{dx}\left(\frac{u}{v}\right) = \frac{v u' - u v'}{v^2}")
                    st.latex(r"\lim_{x \to a} \frac{f(x)}{g(x)} = \lim_{x \to a} \frac{f'(x)}{g'(x)}")
                elif "Physics" in active_subj:
                    st.latex(r"\vec{F} = \frac{d\vec{p}}{dt}, \quad E = mc^2")
                    st.latex(r"V = IR, \quad B = \frac{\mu_0 I}{2\pi r}")
                elif "Chemistry" in active_subj:
                    st.latex(r"\Delta G = \Delta H - T\Delta S")
                    st.latex(r"E_{cell} = E^\circ_{cell} - \frac{RT}{nF} \ln Q")
                else:
                    st.latex(r"Sum = A \oplus B \oplus C_{in}, \quad Carry = AB + C_{in}(A \oplus B)")

    # ================= SECTION 7: AI MENTOR =================
    elif selected_nav == "🤖 AI Mentor":
        st.markdown("#### 🤖 1-on-1 AI Faculty Mentor — " + active_course)
        past_ctx = st.session_state.ai_memory.get(active_course, {}).get("last_summary", "Starting fresh discussion.")
        st.caption("AI Memory Context: *" + past_ctx + "*")

        q = st.text_input("Ask Any Doubt / Case Law / Section / Numerical:")
        q_img = st.file_uploader("Upload Problem Image (Optional):", type=["png", "jpg", "jpeg"])
        pil_q = Image.open(q_img) if q_img else None

        if st.button("Clear Doubt", use_container_width=True):
            if q.strip() or pil_q:
                with st.spinner("AI faculty analyzing with memory context..."):
                    sys_prompt = (
                        "You are a master mentor for " + active_course + " (" + active_subj + "). "
                        "Remember previous progress: " + past_ctx + ". "
                        "Explain step-by-step with statutory sections, case laws, or derivations."
                    )
                    ans = execute_ai_query(sys_prompt, q, image_input=pil_q)
                    st.write(ans)
                    
                    if active_course not in st.session_state.ai_memory:
                        st.session_state.ai_memory[active_course] = {}
                    st.session_state.ai_memory[active_course]["last_summary"] = "Discussed: " + q[:60]
                    save_user_memory()
            else:
                st.warning("Please type a question or upload image.")

    # ================= SECTION 8: COLAB SANDBOX (PYTHON) =================
    elif selected_nav == "💻 Sandbox" and "Python" in active_subj:
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
            st.markdown("**[ " + str(idx + 1) + " ]** In [ ]:")
            c_ed, c_act = st.columns([8.5, 1.5])
            with c_ed:
                cell["code"] = st.text_area("Cell " + str(cell['id']), value=cell["code"], height=120, label_visibility="collapsed")
            with c_act:
                run_btn = st.button("Run", key="run_" + str(cell['id']), use_container_width=True)
                assist_btn = st.button("Assist", key="as_" + str(cell['id']), use_container_width=True)

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
                    cell["output"] = execute_ai_query(sys_prompt, "Analyze:\n" + cell['code'])
                    cell["error"] = ""

            if cell["output"]:
                st.code(cell["output"])
            if cell["error"]:
                st.error(cell["error"])
