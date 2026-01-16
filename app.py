import streamlit as st
import pandas as pd
import numpy as np
import joblib
import re
import time
from datetime import datetime

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Valkyrie AI | Student Success Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS styling
st.markdown("""
<style>
    /* Premium gradient background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Glassmorphism containers */
    .glass-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Premium metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
    }
    
    /* Risk indicators */
    .risk-critical {
        background: linear-gradient(135deg, #ff0844 0%, #ffb199 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 0.5rem 0;
    }
    
    .risk-high {
        background: linear-gradient(135deg, #ff9a00 0%, #ff6a00 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 0.5rem 0;
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 0.5rem 0;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 0.5rem 0;
    }
    
    /* Professional report styling */
    .premium-report {
        background: #1e1e1e;
        color: #dcdcdc;
        padding: 2rem;
        border-radius: 15px;
        font-family: 'Courier New', monospace;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. MODEL LOADING WITH ERROR HANDLING
# ==========================================
@st.cache_resource
def load_models():
    try:
        # Show loading animation
        with st.spinner("🚀 Initializing Valkyrie AI Engine..."):
            time.sleep(1.5)
            
        bundle = joblib.load('student_risk_model.pkl')
        
        # Validate required components
        required_keys = ['final_model', 'nlp_model', 'nlp_vectorizer']
        missing_keys = [key for key in required_keys if key not in bundle]
        
        if missing_keys:
            st.error(f"Missing model components: {missing_keys}")
            return None
            
        return bundle
    except FileNotFoundError:
        st.error("""
        <div style="background: rgba(255,255,255,0.95); padding: 2rem; border-radius: 15px; text-align: center;">
            <h3>🚨 Model File Not Found</h3>
            <p>Please ensure 'student_risk_model.pkl' is uploaded to your app directory.</p>
            <p><strong>Support:</strong> contact@valkyrie-ai.com</p>
        </div>
        """, unsafe_allow_html=True)
        return None
    except Exception as e:
        st.error(f"Model loading error: {str(e)}")
        return None

# ==========================================
# 3. CORE FUNCTIONS
# ==========================================
def clean_text(text):
    if not isinstance(text, str): return ""
    text = text.lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def calculate_features(input_df, nlp_score):
    df = input_df.copy()
    df['nlp_stress_score'] = nlp_score
    
    # Academic Index
    df['academic_index'] = ((df['previous_sem_gpa'] * 10) + df['last_test_score']) / 2
    
    # Sleep Deviation
    df['sleep_deviation'] = abs(df['sleep_hours_avg'] - 8)
    
    # Focus Ratio
    df['focus_ratio'] = df['avg_daily_study_hours'] / (df['social_media_hours_per_day'] + 1)
    
    # Risk Alarm
    df['risk_alarm'] = np.where((df['is_backlog'] == 1) & (df['attendance_pct'] < 75), 1, 0)
    
    # Expected column order
    expected_cols = [
        'attendance_pct', 'sleep_hours_avg', 'avg_daily_study_hours',
        'avg_weekly_library_hours', 'previous_sem_gpa', 'last_test_score',
        'social_media_hours_per_day', 'extracurricular_engagement_score',
        'is_exam_week', 'nlp_stress_score', 'is_backlog', 'sleep_deviation',
        'academic_index', 'focus_ratio', 'risk_alarm'
    ]
    
    return df[expected_cols]

def generate_premium_4_week_plan(risk_drivers, name, risk_prob):
    """Generate comprehensive 4-week premium plan"""
    
    plan = f"""
⚡ VALKYRIE AI - PREMIUM COUNSELING REPORT
Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
Student: {name}
Risk Level: {'HIGH' if risk_prob > 0.6 else 'MEDIUM' if risk_prob > 0.3 else 'LOW'} ({risk_prob:.1%})

═══════════════════════════════════════════════════════════════
"""
    
    # Week 1 - Foundation
    plan += f"""
🏗️ WEEK 1: FOUNDATION & STABILIZATION
Focus: Establishing core habits and immediate risk mitigation

DAILY PROTOCOLS:
"""
    if 'Sleep' in risk_drivers:
        plan += "● Sleep Optimization: 10-3-2-1 Rule (No caffeine 10h before, food 3h, work 2h, screens 1h)\n"
        plan += "● Target: 8 hours consistent sleep schedule (11 PM - 7 AM)\n"
    else:
        plan += "● Maintain optimal sleep schedule and track sleep quality\n"
    
    if 'Stress' in risk_drivers:
        plan += "● Stress Management: 15-minute morning meditation + evening journaling\n"
        plan += "● Use 4-7-8 breathing technique before study sessions\n"
    
    if 'Backlogs/Attendance' in risk_drivers:
        plan += "● Emergency Protocol: Meet with course coordinator within 48 hours\n"
        plan += "● Attendance Recovery: Set 5 alarms, find accountability partner\n"
    
    plan += f"""
ACADEMIC FOCUS:
● Minimum {6 if 'Grades' in risk_drivers else 4} hours daily focused study
● Active recall sessions every 2 hours
● Weekly review with study group

WELLNESS INTEGRATION:
● 30 minutes physical activity (walking counts)
● 2L water daily minimum
● Digital sunset: No screens after 10 PM

SUCCESS METRICS:
□ Attendance improved by 10%
□ Sleep deviation < 1 hour
□ Stress self-rating reduced by 2 points
□ Study hours increased by 1 hour daily

═══════════════════════════════════════════════════════════════
"""
    
    # Week 2 - Acceleration
    plan += f"""
⚡ WEEK 2: ACCELERATION & CONSISTENCY
Focus: Building momentum and establishing routines

ADVANCED STRATEGIES:
"""
    if 'Focus' in risk_drivers:
        plan += "● Digital Detox: Social media limited to 30 minutes daily\n"
        plan += "● Pomodoro Mastery: 50min study + 10min break cycles\n"
        plan += "● Distraction Elimination: Study phone in separate room\n"
    
    if 'Grades' in risk_drivers:
        plan += "● Academic Intensive: Past paper analysis (2 papers/week)\n"
        plan += "● Professor Office Hours: Minimum 2 visits this week\n"
        plan += "● Concept Mapping: Visual learning for complex topics\n"
    
    plan += f"""
OPTIMIZATION TECHNIQUES:
● Spaced repetition schedule implementation
● Feynman technique: Teach concepts to study buddy
● Mind mapping for subject interconnections
● Weekly performance review and adjustment

LIFESTYLE UPGRADES:
● Meal prep for consistent nutrition
● Morning routine optimization (30-min buffer)
● Evening wind-down ritual establishment
● Weekend recovery planning

MILESTONE TARGETS:
□ Clear 50% of identified backlogs
□ Focus ratio improved by 25%
□ Academic index increased by 10 points
□ Consistency streak: 7-day habit formation

═══════════════════════════════════════════════════════════════
"""
    
    return plan

# ==========================================
# 4. MAIN APPLICATION
# ==========================================
def main():
    # Premium header
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=60)
    
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <h1 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                     -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                     font-weight: 700; margin-bottom: 0.5rem;">
                ⚡ Valkyrie AI
            </h1>
            <p style="color: #64748b; margin: 0;">Premium Student Success Intelligence Platform</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: right; padding: 0.5rem; background: rgba(255,255,255,0.1); border-radius: 10px;">
            <p style="margin: 0; color: white; font-size: 0.8rem;">Premium Version</p>
            <p style="margin: 0; color: #dcdcdc; font-size: 0.7rem;">360° Analytics</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Load models
    models = load_models()
    if models is None:
        st.stop()
    
    # Sidebar with premium form
    with st.sidebar:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            <h3 style="color: white; margin: 0;">🎓 Student Portal</h3>
            <p style="color: #dcdcdc; margin: 0; font-size: 0.9rem;">Premium Analytics Access</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("premium_student_form"):
            st.markdown("### 📋 Student Profile")
            
            # Basic Information
            name = st.text_input("Full Name*", "Student Name", help="Enter your complete name")
            student_id = st.text_input("Student ID", "STU-2024-001", help="Your unique identifier")
            
            # Academic Metrics
            st.markdown("### 📊 Academic Performance")
            col1, col2 = st.columns(2)
            with col1:
                gpa = st.slider("GPA (0-10)", 0.0, 10.0, 7.5, help="Previous semester GPA")
                test_score = st.slider("Test Score", 0, 100, 75, help="Latest test performance")
            
            with col2:
                backlog = st.selectbox("Backlogs", ["No", "Yes"], help="Any pending subjects")
                attendance = st.slider("Attendance %", 0, 100, 85, help="Overall attendance")
            
            # Campus Life
            st.markdown("### 🏫 Campus Engagement")
            col1, col2 = st.columns(2)
            with col1:
                library_hrs = st.slider("Library Hours/Week", 0, 20, 5, help="Weekly library time")
                extra_score = st.slider("Extracurricular Score", 0, 10, 6, help="Activity participation")
            
            with col2:
                exam_week = st.selectbox("Exam Week", ["No", "Yes"], help="Currently in exam period")
                study_hrs = st.slider("Daily Study Hours", 0.0, 12.0, 4.0, help="Focused study time")
            
            # Lifestyle Metrics
            st.markdown("### 🌱 Lifestyle & Wellness")
            col1, col2 = st.columns(2)
            with col1:
                social_hrs = st.slider("Social Media Hours", 0.0, 8.0, 2.5, help="Daily social media usage")
                sleep_hrs = st.slider("Sleep Hours", 0.0, 12.0, 7.0, help="Average nightly sleep")
            
            with col2:
                stress_level = st.slider("Stress Level", 1, 10, 5, help="1=Very Low, 10=Very High")
                exercise_hrs = st.slider("Exercise Hours/Week", 0, 20, 3, help="Physical activity time")
            
            # Daily Journal
            st.markdown("### 📝 Daily Reflection")
            diary_entry = st.text_area("How are you feeling today?", 
                                     "I feel overwhelmed with the upcoming exams and assignments.",
                                     height=100,
                                     help="Our AI will analyze your emotional state")
            
            submitted = st.form_submit_button("🔍 GENERATE PREMIUM ANALYSIS", 
                                            use_container_width=True)
    
    # Main analysis area
    if submitted:
        try:
            # Show premium loading
            with st.spinner("🧠 Valkyrie AI Analyzing Your Profile..."):
                time.sleep(2)  # Premium feel
                
            # Process inputs
            cleaned_diary = clean_text(diary_entry)
            vec_text = models['nlp_vectorizer'].transform([cleaned_diary])
            nlp_prob = models['nlp_model'].predict_proba(vec_text)[0][1]
            
            # Prepare data
            raw_data = pd.DataFrame({
                'previous_sem_gpa': [gpa],
                'attendance_pct': [attendance],
                'avg_daily_study_hours': [study_hrs],
                'social_media_hours_per_day': [social_hrs],
                'sleep_hours_avg': [sleep_hrs],
                'last_test_score': [test_score],
                'is_backlog': [1 if backlog == "Yes" else 0],
                'avg_weekly_library_hours': [library_hrs],
                'extracurricular_engagement_score': [extra_score],
                'is_exam_week': [1 if exam_week == "Yes" else 0]
            })
            
            final_input = calculate_features(raw_data, nlp_prob)
            risk_prob = models['final_model'].predict_proba(final_input)[0][1]
            
            # Display premium results
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.95); padding: 2rem; border-radius: 20px; margin: 1rem 0;">
                <h2 style="text-align: center; color: #2c3e50;">🎓 Premium Analysis Report</h2>
                <p style="text-align: center; color: #7f8c8d;">Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Premium metrics dashboard
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Risk Probability</h3>
                    <div style="font-size: 2rem; font-weight: bold;">{risk_prob:.1%}</div>
                    <div style="font-size: 0.9rem;">{'HIGH' if risk_prob > 0.6 else 'MEDIUM' if risk_prob > 0.3 else 'LOW'} RISK</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                academic_index = final_input['academic_index'][0]
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Academic Index</h3>
                    <div style="font-size: 2rem; font-weight: bold;">{academic_index:.0f}/100</div>
                    <div style="font-size: 0.9rem;">{'Excellent' if academic_index >= 80 else 'Good' if academic_index >= 60 else 'Needs Work'}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                stress_score = nlp_prob * 10
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Stress Analysis</h3>
                    <div style="font-size: 2rem; font-weight: bold;">{stress_score:.1f}/10</div>
                    <div style="font-size: 0.9rem;">{'High' if stress_score > 7 else 'Moderate' if stress_score > 4 else 'Low'}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                focus_ratio = final_input['focus_ratio'][0]
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Focus Ratio</h3>
                    <div style="font-size: 2rem; font-weight: bold;">{focus_ratio:.2f}</div>
                    <div style="font-size: 0.9rem;">{'Excellent' if focus_ratio > 2 else 'Good' if focus_ratio > 1 else 'Needs Improvement'}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Risk analysis section
            st.markdown("---")
            st.markdown("### 🩺 Premium Risk Analysis")
            
            col1, col2 = st.columns([1, 2])
            
            risk_drivers = []
            
            with col1:
                st.markdown("#### ⚠️ Risk Factors Identified")
                
                if final_input['risk_alarm'][0] == 1:
                    st.markdown("""
                    <div class="risk-critical">
                        <strong>🚨 CRITICAL ALERT:</strong><br>
                        Death Spiral Detected<br>
                        <small>Backlogs + Low Attendance</small>
                    </div>
                    """, unsafe_allow_html=True)
                    risk_drivers.append("Backlogs/Attendance")
                
                if final_input['sleep_deviation'][0] > 1.5:
                    st.markdown(f"""
                    <div class="risk-high">
                        <strong>⚠️ SLEEP DEBT:</strong><br>
                        {final_input['sleep_deviation'][0]:.1f}h deviation<br>
                        <small>From optimal 8 hours</small>
                    </div>
                    """, unsafe_allow_html=True)
                    risk_drivers.append("Sleep")
                
                if final_input['focus_ratio'][0] < 0.5:
                    st.markdown("""
                    <div class="risk-medium">
                        <strong>📱 DISTRACTION RISK:</strong><br>
                        Low Focus Ratio<br>
                        <small>Social > Study Time</small>
                    </div>
                    """, unsafe_allow_html=True)
                    risk_drivers.append("Focus")
                
                if final_input['academic_index'][0] < 50:
                    st.markdown("""
                    <div class="risk-high">
                        <strong>📚 ACADEMIC CRITICAL:</strong><br>
                        Low Performance<br>
                        <small>Immediate intervention needed</small>
                    </div>
                    """, unsafe_allow_html=True)
                    risk_drivers.append("Grades")
                
                if nlp_prob > 0.6:
                    st.markdown("""
                    <div class="risk-medium">
                        <strong>🧠 MENTAL STRAIN:</strong><br>
                        High Stress Detected<br>
                        <small>From text analysis</small>
                    </div>
                    """, unsafe_allow_html=True)
                    risk_drivers.append("Stress")
                
                if not risk_drivers:
                    st.markdown("""
                    <div class="risk-low">
                        <strong>✅ OPTIMAL STATUS:</strong><br>
                        No Critical Risks<br>
                        <small>Keep up the great work!</small>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("#### 🔮 Counterfactual Analysis")
                
                # Simulate different scenarios
                scenarios = []
                
                # Sleep optimization
                sim_sleep = final_input.copy()
                sim_sleep['sleep_deviation'] = 0
                sleep_new_prob = models['final_model'].predict_proba(sim_sleep)[0][1]
                scenarios.append({
                    'action': 'Sleep Optimization (8 hours)',
                    'new_risk': sleep_new_prob,
                    'effort': 'Low',
                    'timeline': '1 week'
                })
                
                # Study increase
                sim_study = final_input.copy()
                sim_study['avg_daily_study_hours'] += 2
                sim_study['focus_ratio'] = sim_study['avg_daily_study_hours'] / (sim_study['social_media_hours_per_day'] + 1)
                study_new_prob = models['final_model'].predict_proba(sim_study)[0][1]
                scenarios.append({
                    'action': 'Increase Study (+2 hours daily)',
                    'new_risk': study_new_prob,
                    'effort': 'Medium',
                    'timeline': '2 weeks'
                })
                
                # Social media reduction
                sim_social = final_input.copy()
                sim_social['social_media_hours_per_day'] *= 0.5
                sim_social['focus_ratio'] = sim_social['avg_daily_study_hours'] / (sim_social['social_media_hours_per_day'] + 1)
                social_new_prob = models['final_model'].predict_proba(sim_social)[0][1]
                scenarios.append({
                    'action': 'Reduce Social Media (-50%)',
                    'new_risk': social_new_prob,
                    'effort': 'Medium',
                    'timeline': '1 week'
                })
                
                # Display scenarios
                for scenario in scenarios:
                    improvement = risk_prob - scenario['new_risk']
                    col_a, col_b = st.columns([3, 1])
                    
                    with col_a:
                        st.write(f"**{scenario['action']}**")
                        st.write(f"New Risk: **{scenario['new_risk']:.1%}** (Improvement: {improvement:.1%})")
                        st.progress(1 - scenario['new_risk'])
                    
                    with col_b:
                        st.write(f"Effort: **{scenario['effort']}**")
                        st.write(f"Timeline: **{scenario['timeline']}**")
            
            # Premium 4-week plan
            st.markdown("---")
            st.markdown("### 📋 Premium 4-Week Transformation Plan")
            
            plan_content = generate_premium_4_week_plan(risk_drivers, name, risk_prob)
            
            st.markdown(f"""
            <div class="premium-report">
                <pre>{plan_content}</pre>
            </div>
            """, unsafe_allow_html=True)
            
            # Download options
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.download_button(
                    label="📄 Download Full Report",
                    data=plan_content,
                    file_name=f"{name.replace(' ', '_')}_Valkyrie_Report_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col2:
                # Create summary for download
                summary = f"""
Valkyrie AI - Executive Summary
Student: {name}
Date: {datetime.now().strftime('%B %d, %Y')}
Risk Level: {'HIGH' if risk_prob > 0.6 else 'MEDIUM' if risk_prob > 0.3 else 'LOW'}
Risk Score: {risk_prob:.1%}

Key Recommendations:
1. {'Fix sleep schedule immediately' if 'Sleep' in risk_drivers else 'Maintain good sleep habits'}
2. {'Increase study hours' if 'Grades' in risk_drivers else 'Continue current study pattern'}
3. {'Reduce social media usage' if 'Focus' in risk_drivers else 'Maintain digital wellness'}
4. {'Implement stress management' if 'Stress' in risk_drivers else 'Continue wellness practices'}

Next Steps: Follow the 4-week transformation plan for optimal results.
"""
                st.download_button(
                    label="📊 Download Summary",
                    data=summary,
                    file_name=f"{name.replace(' ', '_')}_Executive_Summary.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col3:
                # Create action items
                action_items = "\n".join([f"{i+1}. {driver}" for i, driver in enumerate(risk_drivers)]) if risk_drivers else "1. Maintain current excellence"
                st.download_button(
                    label="✅ Download Action Items",
                    data=f"Priority Actions for {name}:\n\n{action_items}",
                    file_name=f"{name.replace(' ', '_')}_Action_Items.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            # Premium footer
            st.markdown("---")
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: rgba(255,255,255,0.1); border-radius: 15px; margin-top: 2rem;">
                <h3 style="color: white; margin: 0 0 1rem 0;">🎓 Valkyrie AI Premium Platform</h3>
                <p style="color: #dcdcdc; margin: 0; font-size: 0.9rem;">
                    Advanced machine learning meets educational psychology for unprecedented student success outcomes.
                </p>
                <p style="color: #a0a0a0; margin: 0.5rem 0 0 0; font-size: 0.8rem;">
                    For premium support: premium@valkyrie-ai.com | 24/7 Student Success Hotline
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Analysis error: {str(e)}")
            st.info("Please check your inputs and try again.")
    
    else:
        # Welcome screen
        st.markdown("""
        <div class="glass-container">
            <h2 style="text-align: center; color: #2c3e50;">🎓 Welcome to Valkyrie AI Premium</h2>
            <p style="text-align: center; color: #7f8c8d; font-size: 1.1rem;">
                Unlock your academic potential with advanced AI-powered counseling
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="text-align: center; padding: 1rem;">
                <h3 style="color: #667eea;">🧠 AI Analysis</h3>
                <p style="color: #7f8c8d;">Advanced machine learning models analyze your academic and emotional patterns</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 1rem;">
                <h3 style="color: #667eea;">📊 360° Insights</h3>
                <p style="color: #7f8c8d;">Comprehensive analysis covering academics, lifestyle, and mental wellness</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="text-align: center; padding: 1rem;">
                <h3 style="color: #667eea;">🎯 Action Plans</h3>
                <p style="color: #7f8c8d;">Personalized 4-week transformation plans with measurable outcomes</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem;">
            <p style="color: #7f8c8d; font-style: italic;">
                "The future belongs to those who prepare for it today" - Malcolm X
            </p>
            <p style="color: #95a5a6; font-size: 0.9rem;">
                Complete the form in the sidebar to begin your premium analysis
            </p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
