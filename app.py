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

# ---------------- LOAD DATA ----------------
df = pd.read_csv("kpi_data.csv")

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

# ---------------- LEADERBOARD ----------------
st.header("🏅 Leaderboard")
leaderboard = df.sort_values("score", ascending=False)
st.dataframe(leaderboard)

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

# ---------------- MOTIVATION NUDGE ----------------
st.info("💡 You're only a few points away from the next level! Keep going!")