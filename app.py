import streamlit as st
import io
import contextlib
import sqlite3

st.set_page_config(page_title="BCA Python Portal", page_icon="🐍", layout="wide")

st.sidebar.title("🐍 BCA Python Portal")
page = st.sidebar.radio("Menu:", ["1. Study Units", "2. Run Code Sandbox", "3. Database Lab"])

# --- 1. STUDY UNITS ---
if page == "1. Study Units":
    st.header("BCA Python Curriculum")
    unit = st.selectbox("Select Topic:", ["Unit 1: Basics & Conditions", "Unit 2: Lists & Dicts", "Unit 3: OOP"])
    
    if unit == "Unit 1: Basics & Conditions":
        st.subheader("Variables & Conditionals")
        st.code('''marks = 85
if marks >= 75:
    print("Distinction")
else:
    print("Pass")''', language="python")

    elif unit == "Unit 2: Lists & Dicts":
        st.subheader("Data Structures")
        st.code('''subjects = ["CSA", "C Programming", "Python"]
student = {"name": "Aman", "roll_no": 101}
print(f"Student: {student['name']}, Subjects: {subjects}")''', language="python")

    elif unit == "Unit 3: OOP":
        st.subheader("Classes & Objects")
        st.code('''class Student:
    def __init__(self, name, roll):
        self.name = name
        self.roll = roll

    def display(self):
        return f"Roll: {self.roll}, Name: {self.name}"

s1 = Student("Raj", 101)
print(s1.display())''', language="python")

# --- 2. RUN CODE SANDBOX ---
elif page == "2. Run Code Sandbox":
    st.header("🧪 Interactive Code Runner")
    user_code = st.text_area("Write Python code here:", value='print("Hello BCA!")', height=140)
    
    if st.button("Run Code"):
        stdout_capture = io.StringIO()
        try:
            with contextlib.redirect_stdout(stdout_capture):
                exec(user_code, {})
            st.success("Execution Output:")
            st.text_area("Console:", stdout_capture.getvalue(), height=100)
        except Exception as e:
            st.error(f"Error: {e}")

# --- 3. DATABASE LAB ---
elif page == "3. Database Lab":
    st.header("🗄️ SQLite Database Example")
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS students (roll INTEGER, name TEXT)")
    cursor.execute("INSERT INTO students VALUES (101, 'Aman'), (102, 'Pooja')")
    conn.commit()
    
    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()
    st.table([{"Roll No": r[0], "Name": r[1]} for r in records])