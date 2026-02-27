import streamlit as st
import pandas as pd

# ---------------- LOGIN USERS ----------------
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "manager": {"password": "manager123", "role": "user"}
}

# ---------------- LOGIN SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

# ---------------- LOGIN PAGE ----------------
if not st.session_state.logged_in:

    st.title("🔐 PerformX AI Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.role = USERS[username]["role"]
            st.success("Login Successful ✅")
            st.rerun()
        else:
            st.error("Invalid username or password")

    st.stop()

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="PerformX AI",
    page_icon="🏆",
    layout="wide"
)

st.title("🏆 PerformX AI — Gamified Performance Feedback Agent")
st.caption("Transforming KPIs into Motivation using AI Gamification")

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔐 Admin Controls")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.role = None
    st.rerun()

admin_mode = False
if st.session_state.role == "admin":
    admin_mode = st.sidebar.checkbox("Enable Admin Mode")

# ---------------- SESSION DATA STORAGE ----------------
if "employee_data" not in st.session_state:
    st.session_state.employee_data = pd.read_csv("kpi_data.csv")

latest_data = pd.read_csv("kpi_data.csv")
st.session_state.employee_data = latest_data.copy()

df = st.session_state.employee_data
# ---------------- ENSURE ROLE COLUMN EXISTS ----------------
if "role_type" not in df.columns:
    df["role_type"] = "Sales"   # default role

# ---------------- SAVE DATA FUNCTION ----------------
def save_data():
    st.session_state.employee_data.to_csv("kpi_data.csv", index=False)

# ---------------- SCORING ENGINE ----------------
# ---------------- ROLE-BASED SCORING ENGINE ----------------

def calculate_score(row):

    if row["role_type"] == "Sales":
        return (
            row["sales"] * 0.5 +
            row["deliveries"] * 0.2 +
            row["customer_rating"] * 10 * 0.2 +
            row["attendance"] * 0.1
        )

    elif row["role_type"] == "Support":
        return (
            row["sales"] * 0.2 +
            row["deliveries"] * 0.2 +
            row["customer_rating"] * 10 * 0.5 +
            row["attendance"] * 0.1
        )

    elif row["role_type"] == "Operations":
        return (
            row["sales"] * 0.2 +
            row["deliveries"] * 0.5 +
            row["customer_rating"] * 10 * 0.2 +
            row["attendance"] * 0.1
        )

    else:
        return (
            row["sales"] * 0.4 +
            row["deliveries"] * 0.3 +
            row["customer_rating"] * 10 * 0.2 +
            row["attendance"] * 0.1
        )

df["score"] = df.apply(calculate_score, axis=1)

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

# ---------------- FILTERING + SEARCH (STEP 3 ADDED) ----------------
st.header("🔎 Filter Employees")

search_name = st.text_input("Search Employee by Name")

level_filter = st.selectbox(
    "Filter by Level",
    ["All", "🏆 Elite", "🔥 Pro", "⭐ Rising", "🌱 Beginner"]
)

if level_filter != "All":
    df = df[df["level"] == level_filter]

# ✅ STEP 3 SEARCH FILTER
if search_name:
    df = df[df["employee"].str.contains(search_name, case=False, na=False)]

# ---------------- PERFORMANCE CHART ----------------
st.header("📊 Performance Scores")
st.bar_chart(df.set_index("employee")["score"])

# ---------------- EMPLOYEE VIEW ----------------
st.header("👤 Employee Insights")

emp = st.selectbox("Select Employee", df["employee"])
row = df[df["employee"] == emp].iloc[0]

st.metric("Level", row["level"])
st.write("Role:", row["role_type"])
st.write("Badge:", row["badge"])
st.success(row["feedback"])
st.progress(int(row["score"]))

st.info("💡 You're only a few points away from the next level! Keep going!")

if row["level"] == "🔥 Pro":
    st.balloons()
    st.success("🎉 Pro Performer Achieved!")

# ---------------- ADMIN CONTROLS ----------------
if admin_mode:

    st.sidebar.subheader("➕ Add Employee")

    new_name = st.sidebar.text_input("Employee Name")
    new_sales = st.sidebar.number_input("Sales", 0, 200, 50)
    new_deliveries = st.sidebar.number_input("Deliveries", 0, 200, 40)
    new_rating = st.sidebar.slider("Customer Rating ⭐", 1.0, 5.0, 4.0)
    new_attendance = st.sidebar.number_input("Attendance %", 0, 100, 90)
    
    new_role = st.sidebar.selectbox(
    "Employee Role",
    ["Sales", "Support", "Operations"]
    )

    if st.sidebar.button("Add Employee"):
        new_row = pd.DataFrame([{
            "employee": new_name,
            "sales": new_sales,
            "deliveries": new_deliveries,
            "customer_rating": new_rating,
            "attendance": new_attendance,
            "role_type": new_role
        }])

        st.session_state.employee_data = pd.concat(
            [st.session_state.employee_data, new_row],
            ignore_index=True
        )
        save_data()
        st.success("Employee Added Successfully ✅")

    # -------- EDIT EMPLOYEE --------
    st.sidebar.subheader("✏️ Edit Employee")

    edit_emp = st.sidebar.selectbox(
        "Select Employee to Edit",
        st.session_state.employee_data["employee"],
        key="edit_select"
    )
    edit_role = st.sidebar.selectbox(
    "Edit Role",
    ["Sales", "Support", "Operations"],
    index=["Sales","Support","Operations"].index(edit_row["role_type"])
    )
    edit_row = st.session_state.employee_data[
        st.session_state.employee_data["employee"] == edit_emp
    ].iloc[0]

    edit_sales = st.sidebar.number_input("Edit Sales", 0, 200, int(edit_row["sales"]))
    edit_deliveries = st.sidebar.number_input("Edit Deliveries", 0, 200, int(edit_row["deliveries"]))
    edit_rating = st.sidebar.slider("Edit Customer Rating ⭐", 1.0, 5.0, float(edit_row["customer_rating"]))
    edit_attendance = st.sidebar.number_input("Edit Attendance %", 0, 100, int(edit_row["attendance"]))

    if st.sidebar.button("Update Employee"):
        idx = st.session_state.employee_data[
            st.session_state.employee_data["employee"] == edit_emp
        ].index[0]

        st.session_state.employee_data.loc[idx, "sales"] = edit_sales
        st.session_state.employee_data.loc[idx, "deliveries"] = edit_deliveries
        st.session_state.employee_data.loc[idx, "customer_rating"] = edit_rating
        st.session_state.employee_data.loc[idx, "attendance"] = edit_attendance
        st.session_state.employee_data.loc[idx, "role_type"] = edit_role
        
        save_data()
        st.success(f"{edit_emp} updated successfully ✅")

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
        save_data()
        st.warning(f"{remove_emp} removed.")

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

avg_rating = df["customer_rating"].mean()

if avg_rating > 4.5:
    decisions += "⭐ Customer satisfaction is strong across workforce."
else:
    decisions += "📊 Recommend customer-experience training."

st.info(decisions)
