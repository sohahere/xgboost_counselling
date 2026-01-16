import streamlit as st
import pandas as pd
import numpy as np
import joblib
import re

# ==========================================
# 1. PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="Valkyrie | Student 360° AI Counselor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
    .report-box {
        background-color: #1e1e1e;
        color: #dcdcdc;
        padding: 25px;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        border-left: 5px solid #ff4b4b;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. LOAD MODELS (WITH DEBUGGING)
# ==========================================
@st.cache_resource
def load_models():
    try:
        # Try loading the model bundle
        bundle = joblib.load('student_risk_model.pkl')
        return bundle
    except FileNotFoundError:
        st.error("⚠️ FATAL ERROR: 'student_risk_model.pkl' not found.")
        st.info("Please make sure you uploaded the .pkl file to the GitHub repository.")
        return None
    except Exception as e:
        st.error(f"⚠️ MODEL LOADING ERROR: {e}")
        st.info("This usually happens due to version mismatch between Colab and Streamlit.")
        return None

models = load_models()

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================
def clean_text(text):
    if not isinstance(text, str): return ""
    text = text.lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def calculate_features(input_df, nlp_score):
    # Copy to avoid settingwithcopy warnings
    df = input_df.copy()
    
    # NLP Score
    df['nlp_stress_score'] = nlp_score
    
    # 1. Academic Index
    df['academic_index'] = ((df['previous_sem_gpa'] * 10) + df['last_test_score']) / 2
    
    # 2. Sleep Deviation
    df['sleep_deviation'] = abs(df['sleep_hours_avg'] - 8)
    
    # 3. Focus Ratio (Study / Social+1)
    df['focus_ratio'] = df['avg_daily_study_hours'] / (df['social_media_hours_per_day'] + 1)
    
    # 4. Risk Alarm
    df['risk_alarm'] = np.where((df['is_backlog'] == 1) & (df['attendance_pct'] < 75), 1, 0)
    
    # Ensure column order matches training exactly
    # THIS ORDER MUST MATCH YOUR X_train.columns list from Colab
    expected_cols = [
        'previous_sem_gpa', 'attendance_pct', 'avg_daily_study_hours',
        'social_media_hours_per_day', 'sleep_hours_avg', 'last_test_score',
        'is_backlog', 'nlp_stress_score', 'academic_index', 'sleep_deviation',
        'focus_ratio', 'risk_alarm'
    ]
    
    # Reorder columns to match model expectation
    return df[expected_cols]

def generate_4_week_plan(risk_drivers, name):
    plan = f"### 🗓️ 4-Week Intervention Protocol for {name}\n\n"
    
    # WEEK 1: STABILIZATION
    plan += "**WEEK 1: BIOLOGICAL STABILIZATION**\n"
    if 'Sleep' in risk_drivers:
        plan += "- 🌑 **Protocol:** 'The 10-3-2-1 Rule'. No caffeine 10hrs before bed, no food 3hrs before, no work 2hrs before, no screens 1hr before.\n"
    else:
        plan += "- ✅ **Protocol:** Maintain current sleep. Focus on hydration.\n"
    if 'Stress' in risk_drivers:
        plan += "- 🧠 **Mental:** 10 mins daily journaling (Brain Dump) to lower NLP Stress Score.\n\n"
    else:
        plan += "- 🧠 **Mental:** Light review of daily notes (15 mins).\n\n"

    # WEEK 2: ACADEMIC TRIAGE
    plan += "**WEEK 2: ACADEMIC TRIAGE**\n"
    if 'Backlogs/Attendance' in risk_drivers:
        plan += "- 🚨 **CRITICAL:** Meet with faculty regarding attendance. You are in the 'Danger Zone'.\n"
        plan += "- 📚 **Action:** Dedicate Sat/Sun purely to backlog clearance (4 hour blocks).\n\n"
    elif 'Grades' in risk_drivers:
        plan += "- 📉 **Action:** Identify the 2 hardest subjects. Review past papers for these ONLY.\n\n"
    else:
        plan += "- 🚀 **Action:** Start advanced revision for upcoming tests.\n\n"

    # WEEK 3: OPTIMIZATION
    plan += "**WEEK 3: DOPAMINE DETOX**\n"
    if 'Focus' in risk_drivers:
        plan += "- 📱 **Restriction:** Social Media limit hard-capped at 30 mins/day. Delete apps if necessary.\n"
        plan += "- ⏱️ **Technique:** Use Pomodoro (50min study / 10min break).\n\n"
    else:
        plan += "- ✨ **Technique:** Teach a concept to a friend (Feynman Technique).\n\n"

    # WEEK 4: MAINTENANCE
    plan += "**WEEK 4: PERFORMANCE PEAK**\n"
    plan += "- 🏁 **Goal:** Take one full mock test in exam conditions.\n"
    plan += "- 🔄 **Review:** Analyze errors from the mock test. Do not start new topics.\n"
    
    return plan

# ==========================================
# 4. SIDEBAR - USER INPUTS
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.title("Student Profile")
    st.write("Input current semester data:")
    
    with st.form("student_data"):
        name = st.text_input("Student Name", "Alex")
        
        st.subheader("📊 Academic Metrics")
        gpa = st.slider("Previous Sem GPA", 0.0, 10.0, 7.5)
        test_score = st.slider("Last Test Score (0-100)", 0, 100, 65)
        backlog = st.selectbox("Do you have Backlogs?", ["No", "Yes"])
        attendance = st.slider("Attendance %", 0, 100, 80)
        
        st.subheader("🕰️ Habits & Health")
        study_hrs = st.slider("Daily Study (Hours)", 0.0, 12.0, 2.0)
        social_hrs = st.slider("Social Media (Hours)", 0.0, 12.0, 3.0)
        sleep_hrs = st.slider("Avg Sleep (Hours)", 0.0, 12.0, 6.5)
        
        st.subheader("📖 Daily Journal")
        diary_entry = st.text_area("How are you feeling today?", 
                                   "I am feeling a bit overwhelmed with the syllabus and exams coming up.")
        
        submit = st.form_submit_button("GENERATE 360° REPORT")

# ==========================================
# 5. MAIN APPLICATION LOGIC
# ==========================================
if submit:
    if models is None:
        st.error("🚫 Cannot generate report because the model failed to load. See error above.")
    else:
        try:
            # --- A. PREPROCESSING ---
            # 1. Handle NLP
            cleaned_diary = clean_text(diary_entry)
            vec_text = models['nlp_vectorizer'].transform([cleaned_diary])
            nlp_prob = models['nlp_model'].predict_proba(vec_text)[0][1]
            
            # 2. Prepare Raw DataFrame
            raw_data = pd.DataFrame({
                'previous_sem_gpa': [gpa],
                'attendance_pct': [attendance],
                'avg_daily_study_hours': [study_hrs],
                'social_media_hours_per_day': [social_hrs],
                'sleep_hours_avg': [sleep_hrs],
                'last_test_score': [test_score],
                'is_backlog': [1 if backlog == "Yes" else 0]
            })
            
            # 3. Feature Engineering
            final_input = calculate_features(raw_data, nlp_prob)
            
            # 4. Prediction
            risk_prob = models['final_model'].predict_proba(final_input)[0][1]
            
            # --- B. DISPLAY HEADER ---
            st.title(f"🎓 Analysis Report for {name}")
            st.markdown("---")
            
            # --- C. TOP LEVEL METRICS ---
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Risk Probability", f"{risk_prob:.1%}", 
                        delta="-High Risk" if risk_prob > 0.5 else "Safe",
                        delta_color="inverse")
            
            with col2:
                st.metric("Academic Index", f"{final_input['academic_index'][0]:.1f}/100",
                        help="Combined score of GPA and Tests")
                
            with col3:
                stress_level = "High" if nlp_prob > 0.6 else "Moderate" if nlp_prob > 0.3 else "Low"
                st.metric("Detected Stress (NLP)", stress_level, f"Score: {nlp_prob:.2f}")

            # --- D. DIAGNOSIS & COUNTERFACTUALS ---
            st.subheader("🩺 AI Diagnosis & Simulations")
            
            c1, c2 = st.columns([1, 1.5])
            
            risk_drivers = []
            
            with c1:
                st.markdown("#### ⚠️ Key Risk Factors Identified")
                # Logic to identify drivers
                if final_input['risk_alarm'][0] == 1:
                    st.error("🔴 **DEATH SPIRAL:** Backlogs + Low Attendance.")
                    risk_drivers.append("Backlogs/Attendance")
                if final_input['sleep_deviation'][0] > 1.5:
                    st.warning(f"🟡 **Sleep Debt:** You are deviating {final_input['sleep_deviation'][0]:.1f} hrs from ideal.")
                    risk_drivers.append("Sleep")
                if final_input['focus_ratio'][0] < 0.5:
                    st.warning("🟠 **Distracted:** Social media use is double your study time.")
                    risk_drivers.append("Focus")
                if final_input['academic_index'][0] < 50:
                    st.error("🔴 **Academic Critical:** Grades are significantly low.")
                    risk_drivers.append("Grades")
                if nlp_prob > 0.5:
                    st.info("🔵 **Mental Strain:** Diary text indicates hidden anxiety.")
                    risk_drivers.append("Stress")
                    
                if not risk_drivers:
                    st.success("✅ No critical risk factors detected. Keep it up!")

            with c2:
                st.markdown("#### 🧪 'What-If' Simulation Lab")
                st.markdown("Running real-time counterfactuals to find the easiest fix...")
                
                # 1. Simulate Sleep Fix
                sim_sleep = final_input.copy()
                sim_sleep['sleep_deviation'] = 0 # Fix sleep
                sleep_new_prob = models['final_model'].predict_proba(sim_sleep)[0][1]
                
                # 2. Simulate Study Boost (+2 hours)
                sim_study = final_input.copy()
                sim_study['avg_daily_study_hours'] += 2
                # Recalc focus ratio
                sim_study['focus_ratio'] = sim_study['avg_daily_study_hours'] / (sim_study['social_media_hours_per_day'] + 1)
                study_new_prob = models['final_model'].predict_proba(sim_study)[0][1]
                
                # Display Improvements
                st.write(f"• If you fix **Sleep Schedule** (8hrs): Risk drops to **{sleep_new_prob:.1%}**")
                st.progress(1 - sleep_new_prob)
                
                st.write(f"• If you add **+2 Hours Study**: Risk drops to **{study_new_prob:.1%}**")
                st.progress(1 - study_new_prob)
                
                best_fix = "Sleep" if sleep_new_prob < study_new_prob else "Study"
                st.success(f"💡 **AI Recommendation:** The most efficient way to improve is focusing on **{best_fix}**.")

            st.markdown("---")

            # --- E. THE PREMIUM PLAN ---
            st.subheader(f"🛡️ The Valkyrie Protocol: 4-Week Action Plan")
            
            plan_content = generate_4_week_plan(risk_drivers, name)
            
            st.markdown(f"""
            <div class="report-box">
            {plan_content}
            </div>
            """, unsafe_allow_html=True)
            
            st.download_button(
                label="📥 Download Counseling Report (TXT)",
                data=plan_content,
                file_name=f"{name}_counseling_plan.txt",
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"❌ PREDICTION ERROR: {e}")
            st.info("There was an issue processing the data. Check if your inputs match the training data range.")

else:
    if models is not None:
        st.info("👈 Please enter student details in the sidebar to generate the report.")
        st.markdown("""
        ### 👋 Welcome to Valkyrie
        This tool uses **XGBoost** and **Natural Language Processing** to analyze student performance risks.
        
        **Features:**
        - 🧠 **Multi-Modal Analysis:** Combines grades with text diaries.
        - 🔮 **Counterfactual AI:** Tells you exactly what to change to lower risk.
        - 🗓️ **Auto-Counseling:** Generates a 4-week tailored intervention plan.
        """)
    else:
        st.warning("⚠️ Waiting for model file...")
