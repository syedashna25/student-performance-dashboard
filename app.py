import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Student Performance Dashboard", layout="wide")
st.title("Student Performance and Attendance Dashboard")
st.write("A mini project for analyzing attendance, marks, pass rate, and students needing support.")

DATA_FILE = Path(__file__).parent / "student_data.csv"
if not DATA_FILE.exists():
    st.error("student_data.csv was not found. Keep it in the same folder as app.py.")
    st.stop()

df = pd.read_csv(DATA_FILE)
subjects = ["Maths", "Science", "English", "Computer"]
required = ["Student_ID", "Name", "Attendance_Percentage"] + subjects
missing = [column for column in required if column not in df.columns]
if missing:
    st.error("Missing required columns: " + ", ".join(missing))
    st.stop()

df["Average_Marks"] = df[subjects].mean(axis=1).round(2)
df["Result"] = df[subjects].ge(35).all(axis=1).map({True: "Pass", False: "Fail"})
df["Status"] = (
    (df["Attendance_Percentage"] < 75) |
    df[subjects].lt(35).any(axis=1)
).map({True: "At Risk", False: "Good"})

st.sidebar.header("Filters")
selected_status = st.sidebar.multiselect(
    "Student status", options=["Good", "At Risk"], default=["Good", "At Risk"]
)
filtered = df[df["Status"].isin(selected_status)]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Students", len(df))
c2.metric("Average Marks", f"{df['Average_Marks'].mean():.1f}/100")
c3.metric("Pass Rate", f"{df['Result'].eq('Pass').mean() * 100:.1f}%")
c4.metric("At-Risk Students", int(df["Status"].eq("At Risk").sum()))

st.subheader("Student Records")
st.dataframe(filtered, use_container_width=True, hide_index=True)

left, right = st.columns(2)
with left:
    st.subheader("Subject-wise Average Marks")
    fig, ax = plt.subplots()
    df[subjects].mean().plot(kind="bar", ax=ax)
    ax.set_ylabel("Average marks (out of 100)")
    ax.set_ylim(0, 100)
    ax.tick_params(axis="x", rotation=0)
    st.pyplot(fig)
    plt.close(fig)

with right:
    st.subheader("Pass and Fail")
    result_counts = df["Result"].value_counts()
    fig2, ax2 = plt.subplots()
    result_counts.plot(kind="pie", autopct="%1.1f%%", ax=ax2)
    ax2.set_ylabel("")
    st.pyplot(fig2)
    plt.close(fig2)

st.subheader("Attendance vs Average Marks")
fig3, ax3 = plt.subplots()
ax3.scatter(df["Attendance_Percentage"], df["Average_Marks"])
ax3.set_xlabel("Attendance (%)")
ax3.set_ylabel("Average marks")
ax3.set_xlim(0, 100)
ax3.set_ylim(0, 100)
ax3.grid(True)
st.pyplot(fig3)
plt.close(fig3)

st.subheader("Student Details")
student_name = st.selectbox("Choose a student", df["Name"].tolist(),key="student_details_selector")
st.dataframe(df[df["Name"] == student_name], use_container_width=True, hide_index=True)



