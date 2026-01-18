import streamlit as st
import pandas as pd
from utils.llm import generate_text
from utils.planner import build_prompt

# Page config
st.set_page_config(page_title="AI Wellness Planner", layout="centered")

st.title("🤖 AI Lifestyle-Based Diet & Fitness Planner")
st.caption("For Students and Working Professionals")

st.info("⚠️ Disclaimer: General lifestyle suggestions only.")

# ---------------- AGE INPUT ----------------
age = st.number_input("Enter your age", min_value=1, max_value=100)

if age < 15:
    st.error("This system is not applicable for users below 15 years.")
    st.stop()

category = "Student" if age <= 23 else "Working Professional"
st.success(f"User Category: {category}")

# ---------------- LIFESTYLE DETAILS ----------------
st.subheader("📋 Lifestyle Details")
schedule = st.text_area("Describe your daily schedule")
sleep = st.selectbox("Average sleep duration", ["<5 hours", "5–7 hours", "7–9 hours"])
activity = st.selectbox("Physical activity level", ["Low", "Moderate", "High"])
workout_time = st.selectbox("Available workout time", ["10–20 mins", "20–40 mins", "40+ mins"])

# ---------------- FOOD PREFERENCES ----------------
st.subheader("🍱 Food Preferences")
food_type = st.selectbox("Food preference", ["Vegetarian", "Non-Vegetarian"])
budget = st.selectbox("Food budget", ["Low", "Medium", "High"])
restrictions = st.text_area("Food restrictions (if any)")

# ---------------- GOAL ----------------
goal = st.selectbox(
    "Primary goal",
    ["General Wellness", "Weight Management", "Fitness", "Energy Improvement"]
)

# ---------------- GENERATE PLAN ----------------
if st.button("🚀 Generate Personalized Plan"):
    data = {
        "category": category,
        "age": age,
        "schedule": schedule,
        "sleep": sleep,
        "activity": activity,
        "workout_time": workout_time,
        "food_type": food_type,
        "budget": budget,
        "restrictions": restrictions,
        "goal": goal
    }

    prompt = build_prompt(data)

    with st.spinner("Generating your plan..."):
        result = generate_text(prompt)

    st.subheader("✅ Your Personalized Wellness Plan")

    # --- ADDED VISUALS SECTION ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Diet Composition**")
        # Logic to suggest macros based on food_type
        if food_type == "Vegetarian":
            macro_data = pd.DataFrame({'Macros': ['Carbs', 'Protein', 'Fats'], 'Values': [50, 20, 30]})
        else:
            macro_data = pd.DataFrame({'Macros': ['Carbs', 'Protein', 'Fats'], 'Values': [40, 35, 25]})
        st.bar_chart(macro_data.set_index('Macros'))

    with col2:
        st.write("**Workout Intensity**")
        # Map workout time to a percentage for the progress bar
        intensity_map = {"10–20 mins": 30, "20–40 mins": 60, "40+ mins": 90}
        intensity = intensity_map.get(workout_time, 50)
        st.progress(intensity / 100, text=f"Intensity Level: {intensity}%")
        st.caption("Based on your available time and activity level.")

    # ---------------- DISPLAY TEXT PLAN ----------------
    try:
        if "WORKOUT PLAN:" in result and "DAILY ROUTINE ADVICE:" in result:
            diet, rest = result.split("WORKOUT PLAN:")
            workout, routine = rest.split("DAILY ROUTINE ADVICE:")

            st.markdown("---")
            st.markdown("### 🍽️ Diet Plan")
            st.write(diet.replace("DIET PLAN:", "").strip())

            st.markdown("### 🏋️ Workout Plan")
            st.write(workout.strip())

            st.markdown("### 🕒 Daily Routine Advice")
            st.write(routine.strip())
            
            st.balloons() # Added a celebratory effect
        else:
            st.error("AI output was not in the expected format. Here is the raw plan:")
            st.write(result)

    except Exception as e:
        st.error(f"AI generation failed: {e}")
        st.code(result)