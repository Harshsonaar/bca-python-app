import streamlit as st
import google.generativeai as genai
import io
import contextlib

st.set_page_config(
    page_title="BCA Python Complete Hub | AI Master",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= APPLE FROSTED GLASS & MODERN UI CSS =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Plus Jakarta Sans", "SF Pro Display", sans-serif;
    }
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Ambient Apple Dark Background */
    .stApp {
        background: radial-gradient(circle at 50% 0%, rgba(30, 41, 69, 0.75) 0%, rgba(10, 13, 20, 0.98) 75%);
        color: #F1F5F9;
        padding-bottom: 120px !important; /* Space for floating dock */
    }

    /* Hero Banner (Apple Glass) */
    .hero-banner {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 24px 30px;
        border-radius: 20px;
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.45);
        margin-bottom: 24px;
    }
    .hero-title {
        font-size: 30px;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 0%, #A5B4FC 50%, #38BDF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }
    .hero-sub {
        font-size: 14px;
        color: #94A3B8;
        letter-spacing: 0.2px;
    }

    /* Apple Glass Action Box at Bottom */
    .apple-glass-card {
        background: rgba(255, 255, 255, 0.035);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px;
        padding: 24px;
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        box-shadow: 0 16px 36px rgba(0, 0, 0, 0.35);
        margin-top: 24px;
    }

    /* AI Response Glass Capsule */
    .ai-box {
        background: rgba(20, 24, 38, 0.75);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-left: 4px solid #8B5CF6;
        border-radius: 14px;
        padding: 20px;
        margin-top: 16px;
        color: #F8FAFC;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        line-height: 1.6;
    }

    /* Apple-style Gradient Buttons */
    .stButton>button {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.9) 0%, rgba(147, 51, 234, 0.9) 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        letter-spacing: 0.3px !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.25) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 12px 28px rgba(147, 51, 234, 0.4) !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
    }

    /* Floating Apple Dock at the Bottom */
    div[data-testid="stRadio"] {
        position: fixed;
        bottom: 18px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 999999;
        background: rgba(20, 24, 38, 0.65) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        padding: 8px 18px !important;
        border-radius: 36px !important;
        backdrop-filter: blur(35px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(35px) saturate(180%) !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), inset 0 1px 1px rgba(255, 255, 255, 0.15) !important;
        max-width: 95vw;
    }

    div[data-testid="stRadio"] > label {
        display: none !important;
    }

    div[data-testid="stRadio"] > div {
        flex-direction: row !important;
        gap: 10px !important;
        align-items: center !important;
        justify-content: center !important;
    }

    div[data-testid="stRadio"] label {
        background: transparent !important;
        border-radius: 20px !important;
        padding: 6px 14px !important;
        margin: 0 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        color: #CBD5E1 !important;
        transition: all 0.25s ease !important;
    }

    div[data-testid="stRadio"] label:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        color: #FFFFFF !important;
    }

    .badge-status {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
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
        st.markdown('<div class="badge-status">● AI Mentor Active</div>', unsafe_allow_html=True)
    else:
        with st.expander("🔑 Setup API Key", expanded=True):
            gemini_key = st.text_input("Gemini API Key:", type="password")
            if gemini_key:
                genai.configure(api_key=gemini_key)
                st.success("Connected!")
    st.caption("BCA Full Spectrum • Powered by Gemini 3.8 Flash")

# Fast AI Generator function
def get_ai_response(prompt):
    if not gemini_key:
        return "⚠️ Pehle Gemini API Key configure karein."
    try:
        model = genai.GenerativeModel(
            model_name="models/gemini-3.8-flash",
            generation_config={"temperature": 0.4, "max_output_tokens": 850}
        )
        response = model.generate_content(
            prompt,
            request_options={"timeout": 15.0}
        )
        return response.text
    except Exception as e:
        err_msg = str(e)
        if "429" in err_msg:
            return "⏳ **Free Tier Rate Limit (429):** Request limit reach ho chuki hai. Kripya 25-30 seconds wait karke dubara click karein."
        elif "timed out" in err_msg.lower():
            return "⚠️ **Connection Timeout:** Slow network response. Please try again."
        return f"AI Error: {err_msg}"

# ================= 1. ALL PYTHON TOPICS INTEGRATED =================
def render_syllabus():
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">BCA Python Encyclopedia & Complete Syllabus</div>
        <div class="hero-sub">Python ka har ek concept: Basic variables se lekar Advanced OOP, File I/O, Serialization aur Regex tak.</div>
    </div>
    """, unsafe_allow_html=True)

    modules = [
        "Module 1: Language Basics, Operators & Bitwise",
        "Module 2: Control Flow & Iteration (Branches & Loops)",
        "Module 3: Functions, Scopes, Lambdas & Recursion",
        "Module 4: In-Depth Data Structures (Lists, Tuples, Dicts, Sets)",
        "Module 5: Object-Oriented Programming (OOP Architecture)",
        "Module 6: File Handling, Context Managers & JSON/CSV",
        "Module 7: Exception Handling & Custom Errors",
        "Module 8: Standard Libraries, Regex & Date-Time"
    ]

    selected_module = st.selectbox("📚 Select Topic Module to Study:", modules)

    # ---------------- MODULE 1 ----------------
    if selected_module == "Module 1: Language Basics, Operators & Bitwise":
        st.markdown("### 🔹 Module 1: Core Fundamentals")
        with st.expander("1. Python Architecture, Bytecode & Dynamic Typing", expanded=True):
            st.write("""
            * **Architecture:** Python ek interpreted, high-level, dynamically typed language hai. Source code (`.py`) pehle Bytecode (`.pyc`) mein compile hota hai aur fir Python Virtual Machine (PVM) use execute karta hai.
            * **Dynamic Typing:** C language ki tarah pehle se data type declare nahi karna padta. Variable runtime par assigned value ke mutabik type acquire karta hai.
            """)
            st.code("""x = 101           # int
print(x, type(x))

x = "Raj Shraff"  # str (dynamically changed)
print(x, type(x))""", language="python")

        with st.expander("2. Type Casting & User Input Formatting", expanded=False):
            st.write("""
            * **Type Casting:** `int()`, `float()`, `str()`, `bool()`, `list()`.
            * **Input:** `input()` humesha string return karta hai; calculations ke liye type cast karna zaroori hota hai.
            * **f-Strings:** Python 3.6+ ka fastest aur cleanest formatting mechanism.
            """)
            st.code("""age_str = "25"
age_int = int(age_str)
cgpa = 8.75

print(f"Student Age: {age_int} years | CGPA: {cgpa:.2f}")""", language="python")

        with st.expander("3. Complete Operators (Arithmetic, Bitwise, Logical, Identity, Membership)", expanded=False):
            st.write("""
            * **Arithmetic:** `+`, `-`, `*`, `/`, `//` (floor division), `%` (modulus), `**` (power).
            * **Comparison:** `==`, `!=`, `>`, `<`, `>=`, `<=`.
            * **Logical:** `and`, `or`, `not`.
            * **Bitwise:** `&` (AND), `|` (OR), `^` (XOR), `~` (NOT), `<<` (Left shift), `>>` (Right shift).
            * **Membership & Identity:** `in`, `not in`, `is`, `is not`.
            """)
            st.code("""a, b = 10, 3
print("Floor Division (10 // 3):", a // b) # 3
print("Power (10 ** 3):", a ** b)          # 1000

# Bitwise
print("Bitwise AND (10 & 3):", a & b)       # 2

# Membership & Identity
lst = [1, 2, 3]
print("2 in lst:", 2 in lst)
print("a is b:", a is b)""", language="python")

    # ---------------- MODULE 2 ----------------
    elif selected_module == "Module 2: Control Flow & Iteration (Branches & Loops)":
        st.markdown("### 🔹 Module 2: Decision Making & Loops")
        with st.expander("1. Conditional Branching (if, elif, else, Ternary Operator)", expanded=True):
            st.write("""
            * Python curly braces `{}` use nahi karta; yeh **4 spaces indentation** par chalta hai.
            * **Ternary Operator (Conditional Expression):** `value_if_true if condition else value_if_false`.
            """)
            st.code("""marks = 78
grade = "A" if marks >= 75 else "B"
print(f"Grade: {grade}")

if marks >= 90:
    print("Distinction")
elif marks >= 60:
    print("First Division")
else:
    print("Pass")""", language="python")

        with st.expander("2. Loops (for, while, range() function)", expanded=False):
            st.write("""
            * **for loop:** Sequence (list, string, range) ke har element par traverse karta hai.
            * **while loop:** Jab tak di gayi condition `True` rehti hai tab tak repeat hota hai.
            * **`range(start, stop, step)`:** Efficient number generator.
            """)
            st.code("""# Range with step
print("Even numbers up to 10:")
for i in range(2, 11, 2):
    print(i, end=" ")
print()

# While loop
count = 3
while count > 0:
    print(f"Counter: {count}")
    count -= 1""", language="python")

        with st.expander("3. Loop Control Statements (break, continue, pass, for-else)", expanded=False):
            st.write("""
            * **`break`:** Loop se foran bahar nikal deta hai.
            * **`continue`:** Current round ko chhod kar next round par chala jata hai.
            * **`pass`:** Empty placeholder.
            * **`for-else` (Important for BCA Exams):** Loop ka `else` block tabhi chalta hai jab loop bina `break` ke poora complete ho!
            """)
            st.code("""# Prime number search using for-else
n = 13
for i in range(2, int(n**0.5) + 1):
    if n % i == 0:
        print(f"{n} is not prime")
        break
else:
    print(f"{n} is a Prime Number (Loop finished without break)!")""", language="python")

    # ---------------- MODULE 3 ----------------
    elif selected_module == "Module 3: Functions, Scopes, Lambdas & Recursion":
        st.markdown("### 🔹 Module 3: Modular Programming")
        with st.expander("1. Function Arguments (*args, **kwargs, Default Values)", expanded=True):
            st.write("""
            * **Default Arguments:** Agar caller value na de toh default value use hoti hai.
            * **`*args` (Variable-length positional arguments):** Tuple ke roop mein n number of arguments accept karta hai.
            * **`**kwargs` (Keyword arguments):** Dictionary ke roop mein key-value pairs accept karta hai.
            """)
            st.code("""def student_card(name, roll, *subjects, **metadata):
    print(f"Student: {name} (Roll: {roll})")
    print(f"Subjects: {subjects}")
    print(f"Extra Details: {metadata}")

student_card("Raj", 101, "Python", "Maths", "CSA", semester=1, shift="Morning")""", language="python")

        with st.expander("2. Scope Resolution (LEGB Rule) & Global / Nonlocal", expanded=False):
            st.write("""
            * Python scope resolve karne ke liye **LEGB Rule** follow karta hai:
              1. **L**ocal (Function ke andar)
              2. **E**nclosing (Nested function ka parent)
              3. **G**lobal (Module level)
              4. **B**uilt-in (Python reserved names jaise `print`, `len`)
            * Global variable modify karne ke liye `global` keyword zaroori hai.
            """)
            st.code("""counter = 0

def increment():
    global counter
    counter += 1

increment()
print("Global Counter:", counter)""", language="python")

        with st.expander("3. Anonymous Functions (Lambda), map(), filter(), reduce()", expanded=False):
            st.write("""
            * **Lambda:** Single-line inline anonymous functions: `lambda x: x*2`.
            * **`map(func, iter)`:** Har element par function apply karta hai.
            * **`filter(func, iter)`:** Condition pass karne wale elements filter karta hai.
            """)
            st.code("""from functools import reduce

nums = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, nums))
squares = list(map(lambda x: x**2, evens))
total_sum = reduce(lambda a, b: a + b, nums)

print("Evens:", evens)
print("Squares of Evens:", squares)
print("Total Sum:", total_sum)""", language="python")

        with st.expander("4. Recursion & Recursion Limit", expanded=False):
            st.write("""
            * **Recursion:** Jab koi function khud ko call kare. Isme Base Case aur Recursive Step hona anivarya hai warna `RecursionError` aayega.
            """)
            st.code("""def factorial(n):
    if n <= 1: # Base case
        return 1
    return n * factorial(n - 1) # Recursive step

print("Factorial of 5:", factorial(5))""", language="python")

    # ---------------- MODULE 4 ----------------
    elif selected_module == "Module 4: In-Depth Data Structures (Lists, Tuples, Dicts, Sets)":
        st.markdown("### 🔹 Module 4: Data Structures & Comprehensions")
        with st.expander("1. Lists (Indexing, Slicing, Methods, Comprehensions)", expanded=True):
            st.write("""
            * **Characteristics:** Ordered, Mutable, Duplicates Allowed, Dynamic Size.
            * **Slicing:** `list[start:stop:step]` (Negative indexing starts from `-1`).
            """)
            st.code("""nums = [10, 20, 30, 40, 50, 60]
print("Reversed list:", nums[::-1])
print("Middle slice:", nums[2:5])

# List Comprehension with condition
squared_evens = [x**2 for x in nums if x % 20 == 0]
print("Squared:", squared_evens)""", language="python")

        with st.expander("2. Tuples (Immutability, Packing, Unpacking)", expanded=False):
            st.write("""
            * **Characteristics:** Ordered, Immutable, Fast memory access.
            * **Unpacking:** Single line multiple variable assignment.
            """)
            st.code("""point = (10, 20, 30)
x, y, z = point # Unpacking
print(f"X: {x}, Y: {y}, Z: {z}")""", language="python")

        with st.expander("3. Dictionaries (Hash Tables, Methods, Dict Comprehensions)", expanded=False):
            st.write("""
            * **Characteristics:** Key-Value store, Keys must be immutable (hashable), Fast $O(1)$ lookups.
            * **Methods:** `.keys()`, `.values()`, `.items()`, `.get(key, default)`.
            """)
            st.code("""marks = {"Python": 88, "CSA": 82, "Maths": 91}
print("Python marks:", marks.get("Python", "Not Found"))

# Dict Comprehension
passed = {k: v for k, v in marks.items() if v >= 85}
print("Distinction Subjects:", passed)""", language="python")

        with st.expander("4. Sets (Hashing, Mathematical Operations)", expanded=False):
            st.write("""
            * **Characteristics:** Unordered, Unique elements only, Fast membership testing.
            * **Operations:** Union (`|`), Intersection (`&`), Difference (`-`), Symmetric Difference (`^`).
            """)
            st.code("""a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print("Union:", a | b)
print("Intersection:", a & b)
print("Difference (A - B):", a - b)""", language="python")

    # ---------------- MODULE 5 ----------------
    elif selected_module == "Module 5: Object-Oriented Programming (OOP Architecture)":
        st.markdown("### 🔹 Module 5: Object-Oriented Programming")
        with st.expander("1. Classes, Objects, __init__ Constructor & self", expanded=True):
            st.write("""
            * **Class:** Real world entity ka blueprint.
            * **Object:** Class ka live instance memory mein.
            * **`__init__`:** Constructor jo object banate waqt state initialize karta hai.
            * **`self`:** Current object instance ka reference.
            """)
            st.code("""class BCAStudent:
    university = "UP Board / State University" # Class variable

    def __init__(self, name, roll):
        self.name = name       # Instance variable
        self.roll = roll

    def info(self):
        return f"{self.name} (Roll: {self.roll}) - {BCAStudent.university}"

s1 = BCAStudent("Raj Shraff", 101)
print(s1.info())""", language="python")

        with st.expander("2. Encapsulation & Access Modifiers (Public, Protected, Private)", expanded=False):
            st.write("""
            * **Public:** `var` (Kahi se bhi accessible).
            * **Protected:** `_var` (Conventionally internal/subclass use).
            * **Private:** `__var` (Name mangling lagti hai, directly bahar se access nahi hota).
            """)
            st.code("""class BankAccount:
    def __init__(self, holder, balance):
        self.holder = holder
        self.__balance = balance # Private

    def deposit(self, amt):
        if amt > 0:
            self.__balance += amt

    def get_balance(self):
        return self.__balance

acc = BankAccount("Raj", 5000)
acc.deposit(1500)
print("Safe Balance:", acc.get_balance())
# print(acc.__balance) # Raises AttributeError""", language="python")

        with st.expander("3. Types of Inheritance & super()", expanded=False):
            st.write("""
            * **Types:** Single, Multiple, Multilevel, Hierarchical.
            * **`super()`:** Parent class ke constructor ya methods ko invoke karne ke liye.
            """)
            st.code("""class Person:
    def __init__(self, name):
        self.name = name

class Scholar(Person):
    def __init__(self, name, course):
        super().__init__(name) # Call parent
        self.course = course

    def introduce(self):
        return f"I am {self.name}, studying {self.course}"

s = Scholar("Raj", "BCA")
print(s.introduce())""", language="python")

        with st.expander("4. Polymorphism, Method Overriding & Dunder / Magic Methods", expanded=False):
            st.write("""
            * **Overriding:** Child class parent ke method ko naye logic ke sath reimplement karti hai.
            * **Dunder Methods:** `__str__`, `__len__`, `__add__` jo Python internal operations customize karte hain.
            """)
            st.code("""class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages

    def __str__(self):
        return f"Book: '{self.title}'"

    def __len__(self):
        return self.pages

b = Book("Python BCA Guide", 320)
print(str(b))
print("Total pages:", len(b))""", language="python")

    # ---------------- MODULE 6 ----------------
    elif selected_module == "Module 6: File Handling, Context Managers & JSON/CSV":
        st.markdown("### 🔹 Module 6: Persistence & File I/O")
        with st.expander("1. File Modes, seek(), tell() & with Statement", expanded=True):
            st.write("""
            * **Modes:** `'r'` (read), `'w'` (write/overwrite), `'a'` (append), `'b'` (binary).
            * **`with open()`:** Context manager jo automatically file close karta hai (even on error).
            * **`tell()`:** Current cursor position batata hai.
            * **`seek(offset)`:** Cursor ko desired byte index par shift karta hai.
            """)
            st.code("""# Writing & Reading
with open("test.txt", "w+") as f:
    f.write("BCA Semester 1\\nPython Core File")
    f.seek(0) # Cursor start par le jao
    print("Content:\\n", f.read())""", language="python")

        with st.expander("2. JSON Serialization & Deserialization", expanded=False):
            st.write("""
            * **`json.dumps()` / `json.dump()`:** Python dict to JSON string/file (Serialization).
            * **`json.loads()` / `json.load()`:** JSON string/file to Python dict (Deserialization).
            """)
            st.code("""import json

student_data = {"name": "Raj", "roll": 101, "skills": ["Python", "C"]}
json_str = json.dumps(student_data, indent=2)
print("Serialized JSON:\\n", json_str)

parsed_dict = json.loads(json_str)
print("Decoded Python Dict:", parsed_dict["name"])""", language="python")

    # ---------------- MODULE 7 ----------------
    elif selected_module == "Module 7: Exception Handling & Custom Errors":
        st.markdown("### 🔹 Module 7: Error Resilience")
        with st.expander("1. Complete try-except-else-finally Architecture", expanded=True):
            st.write("""
            * **`try`:** Risky code block.
            * **`except`:** Catch hone wale exceptions.
            * **`else`:** Tabhi run hota hai jab try block mein **koi error na aaye**.
            * **`finally`:** Chahe error aaye ya na aaye, yeh cleanup ke liye humesha run hota hai.
            """)
            st.code("""try:
    num = 10
    den = 2
    res = num / den
except ZeroDivisionError:
    print("Cannot divide by 0")
else:
    print(f"Division Successful: {res}")
finally:
    print("Cleanup completed.")""", language="python")

        with st.expander("2. Raising Exceptions & User-Defined Custom Exception Classes", expanded=False):
            st.write("""
            * **`raise`:** Manually exception trigger karne ke liye.
            * **Custom Exception:** Built-in `Exception` base class ko inherit karke banta hai.
            """)
            st.code("""class NegativeBalanceError(Exception):
    pass

def withdraw(balance, amt):
    if amt > balance:
        raise NegativeBalanceError("Insufficient Funds!")
    return balance - amt

try:
    withdraw(1000, 1500)
except NegativeBalanceError as err:
    print("Caught Custom Error:", err)""", language="python")

    # ---------------- MODULE 8 ----------------
    elif selected_module == "Module 8: Standard Libraries, Regex & Date-Time":
        st.markdown("### 🔹 Module 8: Built-in Modules & Regex")
        with st.expander("1. Standard Modules (math, random, datetime, sys, os)", expanded=True):
            st.write("""
            * Python ki battery-included standard libraries jo BCA projects mein sabse zyada use hoti hain.
            """)
            st.code("""import math
import random
from datetime import datetime

print("Square root of 144:", math.isqrt(144))
print("Random Roll No:", random.randint(101, 199))
print("Current Timestamp:", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))""", language="python")

        with st.expander("2. Regular Expressions (re module)", expanded=False):
            st.write("""
            * Pattern matching ke liye: `re.search()`, `re.findall()`, `re.match()`, `re.sub()`.
            * `\d` (digit), `\w` (alphanumeric), `+` (1 or more), `^` (start), `$` (end).
            """)
            st.code("""import re

text = "Student Raj, Roll 101, Email: raj@example.com"
email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

match = re.search(email_pattern, text)
if match:
    print("Extracted Email:", match.group())""", language="python")

    # ================= APPLE GLASS BOTTOM ACTION BAR =================
    st.markdown("""
    <div class="apple-glass-card">
        <h3 style="margin-top:0; font-size:20px; font-weight:700;"> AI University Exam Preparation & Viva Master</h3>
        <p style="color:#94A3B8; font-size:13px; margin-bottom:14px;">Iss module ke expected university exam questions aur viva points generate karein:</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔥 Generate Most Important Exam Questions & Viva Points", use_container_width=True):
        with st.spinner("AI Professor questions generate kar raha hai..."):
            prompt = f"""
            You are a senior BCA examiner. For the module: '{selected_module}':
            1. Provide the top 3 high-weightage theory examination questions.
            2. Provide 2 tricky Viva-Voce questions with short 1-line answers.
            3. Highlight 1 critical practical coding pitfall students make.
            Format cleanly using bolding and clear bullet points.
            """
            ai_output = get_ai_response(prompt)
            st.markdown(f'<div class="ai-box">{ai_output}</div>', unsafe_allow_html=True)

# ================= 2. AI SMART EXAM ENGINE =================
def render_exam_engine():
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Automated Exam & Evaluation Suite</div>
        <div class="hero-sub">Generate unique semester exam papers on the fly and get instant grading with line-by-line feedback.</div>
    </div>
    """, unsafe_allow_html=True)

    t_unit = st.selectbox("Exam Module:", [
        "Module 1: Language Basics, Operators & Bitwise",
        "Module 2: Control Flow & Iteration (Branches & Loops)",
        "Module 3: Functions, Scopes, Lambdas & Recursion",
        "Module 4: In-Depth Data Structures (Lists, Tuples, Dicts, Sets)",
        "Module 5: Object-Oriented Programming (OOP Architecture)",
        "Module 6: File Handling, Context Managers & JSON/CSV",
        "Module 7: Exception Handling & Custom Errors",
        "Module 8: Standard Libraries, Regex & Date-Time"
    ])
    
    if st.button("⚡ Generate New Test Paper", use_container_width=True):
        with st.spinner("Drafting fresh exam questions..."):
            test_prompt = f"""
            Create a 10-mark mini examination paper for BCA students on '{t_unit}'.
            - Question 1 (2 Marks): Conceptual definition.
            - Question 2 (3 Marks): Output prediction or short difference.
            - Question 3 (5 Marks): Real-world coding question.
            Keep questions strict and university-grade. Do NOT give solutions.
            """
            st.session_state.current_test = get_ai_response(test_prompt)

    if "current_test" in st.session_state:
        st.markdown(f'<div class="apple-glass-card"><h4>📄 Current Question Paper</h4>{st.session_state.current_test}</div>', unsafe_allow_html=True)

        st.markdown("#### ✍️ Write & Submit Answers")
        user_sol = st.text_area("Yahan apne answers aur codes type karein:", height=200, placeholder="Q1: ...\nQ2: ...\nQ3 (Code): ...")
        if st.button("🚀 Submit Sheet For AI Checking", use_container_width=True):
            if not user_sol.strip():
                st.warning("Please type your answer before submission.")
            else:
                with st.spinner("AI checking answers..."):
                    eval_prompt = f"""
                    You are a strict BCA university examiner grading a student's answer sheet.
                    Paper:
                    {st.session_state.current_test}

                    Student Answer:
                    {user_sol}

                    Evaluate thoroughly:
                    1. Score out of 10.
                    2. Remarks: strengths and mistakes.
                    3. Correct model answer.
                    """
                    scorecard = get_ai_response(eval_prompt)
                    st.markdown(f'<div class="ai-box"><h3>📊 Examination Scorecard</h3>{scorecard}</div>', unsafe_allow_html=True)

# ================= 3. GUIDED PROJECTS LAB =================
def render_projects():
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Semester Capstone Project Lab</div>
        <div class="hero-sub">Complete full-scale BCA projects step-by-step with architecture design and examiner-ready viva prep.</div>
    </div>
    """, unsafe_allow_html=True)

    proj = st.selectbox(
        "Choose Capstone Project:",
        [
            "Student Management System (Console + File / SQLite)",
            "Banking Operations & ATM Simulator (OOPs Based)",
            "Supermarket Inventory & Automated Billing Engine",
            "Hospital Management & Patient Appointment Scheduler",
            "Library Book Circulation & Fine Calculation Engine"
        ]
    )

    st.markdown(f"""
    <div class="apple-glass-card">
        <h4 style="margin-top:0;">🏗️ Architecture: {proj}</h4>
        <p>Complete multi-tiered design pattern with verified logic flow, data structures and error handling blocks.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Get Starter Architecture & Complete Code", use_container_width=True):
        with st.spinner("AI Architect designing codebase..."):
            blueprint_prompt = f"""
            Provide a complete, well-commented, professional Python starter project for: '{proj}'.
            Include OOP classes, error checks, and interactive menu loop.
            """
            st.markdown(f'<div class="ai-box">{get_ai_response(blueprint_prompt)}</div>', unsafe_allow_html=True)

# ================= 4. 24/7 AI CODE MENTOR =================
def render_mentor():
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">24/7 BCA Technical Mentor</div>
        <div class="hero-sub">Resolve coding doubts, syntax comparisons with C language, or logic errors in seconds.</div>
    </div>
    """, unsafe_allow_html=True)

    user_q = st.text_area("Poochhein apna doubt ya code paste karein:", height=140, placeholder="e.g. C Pointers ka alternative Python mein kya hota hai?")
    if st.button("⚡ Ask AI Mentor", use_container_width=True):
        if not user_q.strip():
            st.warning("Pehle sawal enter karein.")
        else:
            with st.spinner("AI Mentor analyzing..."):
                ans = get_ai_response(f"You are a BCA Computer Science professor. Answer clearly with clean code examples:\n\n{user_q}")
                st.markdown(f'<div class="ai-box">{ans}</div>', unsafe_allow_html=True)

# ================= 5. LIVE CODE RUNNER =================
def render_runner():
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Integrated Python Sandbox</div>
        <div class="hero-sub">Write, test, and execute Python code with console output directly in your browser.</div>
    </div>
    """, unsafe_allow_html=True)

    starter = """# BCA Python Interactive Sandbox
def greet(name, sem):
    return f"Hello {name}, Welcome to BCA Semester {sem}!"

msg = greet("Raj", 1)
print(msg)
"""
    code_input = st.text_area("Code Editor:", value=starter, height=200)
    
    c1, c2 = st.columns([1, 1])
    with c1:
        run_btn = st.button("▶ Run Script", use_container_width=True)
    with c2:
        st.download_button(
            label="💾 Download Code (.py)",
            data=code_input,
            file_name="bca_code.py",
            mime="text/plain",
            use_container_width=True
        )

    if run_btn:
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                exec(code_input, {})
            output_str = buf.getvalue()
            st.success("Execution Successful")
            st.text_area("Console Output:", output_str if output_str else "[Program finished with no output]", height=120)
        except Exception as ex:
            st.error(f"Traceback Error: {ex}")

# ================= FLOATING APPLE DOCK NAVIGATION CONTROLLER =================
selected_tab = st.radio(
    label="Apple Dock Navigation",
    options=[
        "📖 Syllabus",
        "📝 Exam Engine",
        "🛠️ Projects",
        "🤖 AI Mentor",
        "🧪 Sandbox"
    ],
    horizontal=True,
    index=0
)

# Route to respective view
if selected_tab == "📖 Syllabus":
    render_syllabus()
elif selected_tab == "📝 Exam Engine":
    render_exam_engine()
elif selected_tab == "🛠️ Projects":
    render_projects()
elif selected_tab == "🤖 AI Mentor":
    render_mentor()
elif selected_tab == "🧪 Sandbox":
    render_runner()
