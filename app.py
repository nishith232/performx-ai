import streamlit as st
import pandas as pd

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="PerformX AI",
    page_icon="🏆",
    layout="wide"
)

st.title("🏆 PerformX AI — Gamified Performance Feedback Agent")
st.caption("Transforming KPIs into Motivation using AI Gamification")

# ---------------- ADMIN PANEL ----------------
st.sidebar.header("🔐 Admin Controls")
admin_mode = st.sidebar.checkbox("Enable Admin Mode")

# ---------------- SESSION DATA STORAGE ----------------
if "employee_data" not in st.session_state:
    st.session_state.employee_data = pd.read_csv("kpi_data.csv")

df = st.session_state.employee_data

# ---------------- SCORING ENGINE ----------------
df["score"] = (
    df["sales"] * 0.4 +
    df["deliveries"] * 0.3 +
    df["customer_rating"] * 10 * 0.2 +
    df["attendance"] * 0.1
)

# ---------------- LEVEL SYSTEM ----------------
def assign_level(score):
    if score > 85:
        return "🏆 Elite"
    elif score > 70:
        return "🔥 Pro"
    elif score > 55:
        return "⭐ Rising"
    else:
        return "🌱 Beginner"

df["level"] = df["score"].apply(assign_level)

# ---------------- BADGES ----------------
def badge(row):
    if row["customer_rating"] > 4.7:
        return "Customer Hero"
    elif row["sales"] > 85:
        return "Sales Ninja"
    else:
        return "Consistent Performer"

df["badge"] = df.apply(badge, axis=1)

# ---------------- AI FEEDBACK ----------------
def feedback(row):
    if row["score"] > 80:
        return f"Excellent work {row['employee']}! You're leading the team."
    elif row["attendance"] < 90:
        return f"{row['employee']}, improving attendance can boost performance."
    else:
        return f"Good progress {row['employee']}. Focus on customer satisfaction."

df["feedback"] = df.apply(feedback, axis=1)

# ---------------- EXECUTIVE AI SCORECARD ----------------
st.header("🏢 Executive AI Scorecard")

avg_score = df["score"].mean()
top_employee = df.loc[df["score"].idxmax()]["employee"]
avg_rating = df["customer_rating"].mean()
attendance_risk_count = len(df[df["attendance"] < 90])

if avg_score > 75:
    health_status = "🟢 Strong Workforce Performance"
elif avg_score > 60:
    health_status = "🟡 Moderate Performance"
else:
    health_status = "🔴 Improvement Needed"

col1, col2, col3, col4 = st.columns(4)
col1.metric("📊 Avg Performance Score", f"{avg_score:.1f}")
col2.metric("🏆 Top Performer", top_employee)
col3.metric("⭐ Avg Customer Rating", f"{avg_rating:.2f}")
col4.metric("⚠ Attendance Risks", attendance_risk_count)

st.success(f"AI Assessment: {health_status}")

# ---------------- LEADERBOARD ----------------
st.header("🏅 Leaderboard")
leaderboard = df.sort_values("score", ascending=False)
st.dataframe(leaderboard)

# ---------------- FILTERING ----------------
st.header("🔎 Filter Employees")

level_filter = st.selectbox(
    "Filter by Level",
    ["All", "🏆 Elite", "🔥 Pro", "⭐ Rising", "🌱 Beginner"]
)

if level_filter != "All":
    df = df[df["level"] == level_filter]

# ---------------- PERFORMANCE CHART ----------------
st.header("📊 Performance Scores")
st.bar_chart(df.set_index("employee")["score"])

# ---------------- EMPLOYEE VIEW ----------------
st.header("👤 Employee Insights")

emp = st.selectbox("Select Employee", df["employee"])
row = df[df["employee"] == emp].iloc[0]

st.metric("Level", row["level"])
st.write("Badge:", row["badge"])
st.success(row["feedback"])
st.progress(int(row["score"]))

st.info("💡 You're only a few points away from the next level! Keep going!")

# ---------------- AI MANAGER INSIGHTS ----------------
st.header("🧠 AI Manager Insights")

avg_score = df["score"].mean()
best_employee = df.loc[df["score"].idxmax()]["employee"]
low_attendance = df[df["attendance"] < 90]["employee"].tolist()

insight_text = f"""
📈 Average Team Performance Score: {avg_score:.2f}

🏆 Top Performer: {best_employee}
"""

if len(low_attendance) > 0:
    insight_text += f"\n⚠ Attendance Risk detected for {len(low_attendance)} employees."

st.success(insight_text)

if row["level"] == "🔥 Pro":
    st.balloons()
    st.success("🎉 Pro Performer Achieved! Outstanding performance!")

# ---------------- AI MANAGER DECISION DASHBOARD ----------------
st.header("📋 AI Manager Decision Dashboard")

top_performers = df[df["score"] > 80]["employee"].tolist()
low_performers = df[df["score"] < 55]["employee"].tolist()
attendance_risk = df[df["attendance"] < 90]["employee"].tolist()

decisions = ""

if len(top_performers) > 0:
    decisions += f"🏆 Reward Recommendation: Recognize {len(top_performers)} high performers.\n\n"

if len(low_performers) > 0:
    decisions += f"📚 Coaching Needed for {len(low_performers)} employees.\n\n"

if len(attendance_risk) > 0:
    decisions += f"⏰ Monitor attendance for {len(attendance_risk)} employees.\n\n"

st.info(decisions)

# ---------------- ADMIN CONTROLS ----------------
if admin_mode:

    st.sidebar.subheader("➕ Add Employee")

    new_name = st.sidebar.text_input("Employee Name")
    new_sales = st.sidebar.number_input("Sales", 0, 200, 50)
    new_deliveries = st.sidebar.number_input("Deliveries", 0, 200, 40)
    new_rating = st.sidebar.slider("Customer Rating ⭐", 1.0, 5.0, 4.0)
    new_attendance = st.sidebar.number_input("Attendance %", 0, 100, 90)

    if st.sidebar.button("Add Employee"):
        new_row = pd.DataFrame([{
            "employee": new_name,
            "sales": new_sales,
            "deliveries": new_deliveries,
            "customer_rating": new_rating,
            "attendance": new_attendance
        }])

        st.session_state.employee_data = pd.concat(
            [st.session_state.employee_data, new_row],
            ignore_index=True
        )

        st.success("Employee Added Successfully ✅")

    # -------- REMOVE EMPLOYEE --------
    st.sidebar.subheader("❌ Remove Employee")

    remove_emp = st.sidebar.selectbox(
        "Select Employee to Remove",
        st.session_state.employee_data["employee"]
    )

    if st.sidebar.button("Delete Employee"):
        st.session_state.employee_data = (
            st.session_state.employee_data[
                st.session_state.employee_data["employee"] != remove_emp
            ]
        )

        st.warning(f"{remove_emp} removed.")
