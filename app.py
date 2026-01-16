import streamlit as st
import pandas as pd
import numpy as np
import joblib
import re
import time
from datetime import datetime

# ==========================================
# 1. PREMIUM PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Valkyrie AI | Premium Student Success Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS with professional design
st.markdown("""
<style>
    /* Import premium fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Premium Color Palette - Professional Blues & Golds */
    :root {
        --primary-blue: #2563eb;
        --primary-blue-dark: #1d4ed8;
        --secondary-blue: #3b82f6;
        --accent-gold: #f59e0b;
        --accent-gold-dark: #d97706;
        --success-green: #10b981;
        --warning-orange: #f97316;
        --danger-red: #ef4444;
        --neutral-50: #f9fafb;
        --neutral-100: #f3f4f6;
        --neutral-200: #e5e7eb;
        --neutral-300: #d1d5db;
        --neutral-600: #4b5563;
        --neutral-700: #374151;
        --neutral-800: #1f2937;
        --neutral-900: #111827;
        
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    /* Global Typography */
    .stApp {
        background: linear-gradient(135deg, var(--neutral-50) 0%, var(--neutral-100) 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: var(--neutral-900);
        letter-spacing: -0.025em;
    }
    
    /* Premium Header - Professional Blue */
    .premium-header {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
        padding: 3rem 2rem;
        border-radius: 24px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-xl);
    }
    
    .brand-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .brand-subtitle {
        font-size: 1.1rem;
        font-weight: 400;
        opacity: 0.9;
        margin: 0;
        letter-spacing: 0.01em;
    }
    
    /* Premium Cards - Clean White */
    .premium-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--neutral-200);
        transition: all 0.2s ease;
    }
    
    .premium-card:hover {
        box-shadow: var(--shadow-lg);
        transform: translateY(-2px);
    }
    
    /* Premium Metric Cards - Clean & Professional */
    .metric-card-premium {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--neutral-200);
        transition: all 0.2s ease;
    }
    
    .metric-card-premium:hover {
        box-shadow: var(--shadow-md);
    }
    
    .metric-value {
        font-size: 2.25rem;
        font-weight: 700;
        color: var(--primary-blue);
        margin: 0.5rem 0;
        line-height: 1;
    }
    
    .metric-label {
        font-size: 0.875rem;
        font-weight: 500;
        color: var(--neutral-600);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 0;
    }
    
    .metric-status {
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        display: inline-block;
        margin-top: 0.5rem;
        background: var(--neutral-100);
        color: var(--neutral-700);
    }
    
    /* Risk Indicators - Professional Colors */
    .risk-indicator {
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        border: 1px solid;
        transition: all 0.2s ease;
    }
    
    .risk-critical {
        background: rgba(239, 68, 68, 0.05);
        border-color: rgba(239, 68, 68, 0.2);
        color: var(--danger-red);
    }
    
    .risk-high {
        background: rgba(249, 115, 22, 0.05);
        border-color: rgba(249, 115, 22, 0.2);
        color: var(--warning-orange);
    }
    
    .risk-medium {
        background: rgba(245, 158, 11, 0.05);
        border-color: rgba(245, 158, 11, 0.2);
        color: var(--accent-gold);
    }
    
    .risk-low {
        background: rgba(16, 185, 129, 0.05);
        border-color: rgba(16, 185, 129, 0.2);
        color: var(--success-green);
    }
    
    /* Premium Buttons - Gold Accent */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-gold-dark) 100%);
        color: white;
        font-weight: 600;
        font-size: 1rem;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        box-shadow: var(--shadow-md);
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-lg);
    }
    
    /* Professional Sidebar - Subtle Blue */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--neutral-100) 0%, var(--neutral-50) 100%);
        border-right: 1px solid var(--neutral-200);
    }
    
    /* Premium Form Elements */
    .stSlider > div > div > div > div {
        background: var(--primary-blue);
        border-radius: 8px;
    }
    
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div {
        border-radius: 12px;
        border: 2px solid var(--neutral-200);
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.2s ease;
        background: white;
    }
    
    .stTextInput > div > div > input:focus, 
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > div:focus {
        border-color: var(--primary-blue);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    
    /* Professional Report Styling - Clean White */
    .premium-report {
        background: white;
        border: 1px solid var(--neutral-200);
        border-radius: 16px;
        padding: 2.5rem;
        margin: 2rem 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        line-height: 1.5;
        color: var(--neutral-800);
        box-shadow: var(--shadow-sm);
        position: relative;
    }
    
    .premium-report::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: var(--primary-blue);
        border-radius: 16px 0 0 16px;
    }
    
    /* Progress Bars - Clean Blue */
    .stProgress > div > div > div > div {
        background: var(--primary-blue);
        border-radius: 4px;
    }
    
    /* Clean Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-in {
        animation: fadeInUp 0.5s ease-out;
    }
    
    /* Section Headers - Professional */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--neutral-900);
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--neutral-200);
    }
    
    /* Premium Welcome Screen */
    .welcome-card {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, var(--neutral-50) 0%, white 100%);
    }
    
    .feature-card {
        text-align: center;
        padding: 2rem;
        background: white;
        border-radius: 12px;
        border: 1px solid var(--neutral-200);
        transition: all 0.2s ease;
    }
    
    .feature-card:hover {
        border-color: var(--primary-blue);
        box-shadow: var(--shadow-md);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. MODEL LOADING WITH ERROR HANDLING
# ==========================================
@st.cache_resource
def load_premium_models():
    try:
        with st.spinner("🚀 Initializing Valkyrie AI Premium Engine..."):
            time.sleep(2)
            
        bundle = joblib.load('student_risk_model.pkl')
        
        # Validate required components
        required_keys = ['final_model', 'nlp_model', 'nlp_vectorizer']
        missing_keys = [key for key in required_keys if key not in bundle]
        
        if missing_keys:
            st.error(f"Missing premium model components: {missing_keys}")
            return None
            
        return bundle
    except FileNotFoundError:
        st.error("""
        <div class="premium-card" style="border-color: var(--danger-red); background: rgba(239, 68, 68, 0.05);">
            <h3 style="color: var(--danger-red); margin: 0;">🚨 Premium Model File Not Found</h3>
            <p style="margin: 0.5rem 0;">Please ensure 'student_risk_model.pkl' is available in your app directory.</p>
            <p style="margin: 0; font-size: 0.9rem; color: var(--neutral-600);">Premium Support: premium@valkyrie-ai.com</p>
        </div>
        """, unsafe_allow_html=True)
        return None
    except Exception as e:
        st.error(f"""
        <div class="premium-card">
            <h3 style="color: var(--danger-red); margin: 0;">⚠️ Premium Engine Error</h3>
            <p style="margin: 0.5rem 0;">{str(e)}</p>
            <p style="margin: 0; font-size: 0.9rem; color: var(--neutral-600);">Technical team has been notified automatically.</p>
        </div>
        """, unsafe_allow_html=True)
        return None

# ==========================================
# 3. CORE PROCESSING FUNCTIONS
# ==========================================
def clean_text(text):
    """Clean and process text input"""
    if not isinstance(text, str): 
        return ""
    text = text.lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def calculate_features(input_df, nlp_score):
    """Calculate engineered features for the model"""
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
    
    # Expected column order - CONSISTENT WITH YOUR MODEL
    expected_cols = [
        'attendance_pct', 'sleep_hours_avg', 'avg_daily_study_hours',
        'avg_weekly_library_hours', 'previous_sem_gpa', 'last_test_score',
        'social_media_hours_per_day', 'extracurricular_engagement_score',
        'nlp_stress_score', 'is_backlog', 'sleep_deviation',
        'academic_index', 'focus_ratio', 'risk_alarm'
    ]
    
    return df[expected_cols]

def generate_professional_plan(risk_drivers, name, risk_prob):
    """Generate professional 4-week plan with clean formatting"""
    
    plan = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    VALKYRIE AI - PROFESSIONAL COUNSELING REPORT              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ Student: {name:<50} ║
║ Risk Level: {'HIGH' if risk_prob > 0.6 else 'MEDIUM' if risk_prob > 0.3 else 'LOW':<49} ║
║ Risk Score: {f"{risk_prob:.1%}":<48} ║
║ Generated: {datetime.now().strftime('%B %d, %Y'):<47} ║
╚══════════════════════════════════════════════════════════════════════════════╝

WEEK 1: FOUNDATION & STABILIZATION
====================================
Focus: Establishing core habits and immediate risk mitigation

DAILY PROTOCOLS:
"""
    if 'Sleep' in risk_drivers:
        plan += "• Sleep Optimization: 10-3-2-1 Rule (No caffeine 10h before, food 3h, work 2h, screens 1h)\n"
        plan += "• Target: 8 hours consistent sleep schedule (11 PM - 7 AM)\n"
    else:
        plan += "• Maintain optimal sleep schedule and track sleep quality\n"
    
    if 'Stress' in risk_drivers:
        plan += "• Stress Management: 15-minute morning meditation + evening journaling\n"
        plan += "• Use 4-7-8 breathing technique before study sessions\n"
    
    if 'Backlogs/Attendance' in risk_drivers:
        plan += "• Emergency Protocol: Meet with course coordinator within 48 hours\n"
        plan += "• Attendance Recovery: Set 5 alarms, find accountability partner\n"
    
    plan += f"""
ACADEMIC FOCUS:
• Minimum {6 if 'Grades' in risk_drivers else 4} hours daily focused study
• Active recall sessions every 2 hours
• Weekly review with study group

WELLNESS INTEGRATION:
• 30 minutes physical activity (walking counts)
• 2L water daily minimum
• Digital sunset: No screens after 10 PM

SUCCESS METRICS:
□ Attendance improved by 10%
□ Sleep deviation < 1 hour
□ Stress self-rating reduced by 2 points
□ Study hours increased by 1 hour daily

WEEK 2: ACCELERATION & CONSISTENCY
====================================
Focus: Building momentum and establishing routines

ADVANCED STRATEGIES:
"""
    if 'Focus' in risk_drivers:
        plan += "• Digital Detox: Social media limited to 30 minutes daily\n"
        plan += "• Pomodoro Mastery: 50min study + 10min break cycles\n"
        plan += "• Distraction Elimination: Study phone in separate room\n"
    
    if 'Grades' in risk_drivers:
        plan += "• Academic Intensive: Past paper analysis (2 papers/week)\n"
        plan += "• Professor Office Hours: Minimum 2 visits this week\n"
        plan += "• Concept Mapping: Visual learning for complex topics\n"
    
    plan += f"""
OPTIMIZATION TECHNIQUES:
• Spaced repetition schedule implementation
• Feynman technique: Teach concepts to study buddy
• Mind mapping for subject interconnections
• Weekly performance review and adjustment

LIFESTYLE UPGRADES:
• Meal prep for consistent nutrition
• Morning routine optimization (30-min buffer)
• Evening wind-down ritual establishment
• Weekend recovery planning

MILESTONE TARGETS:
□ Clear 50% of identified backlogs
□ Focus ratio improved by 25%
□ Academic index increased by 10 points
□ Consistency streak: 7-day habit formation

WEEK 3: MASTERY & OPTIMIZATION
===============================
Focus: Peak performance and skill refinement

ADVANCED PROTOCOLS:
"""
    plan += "• Peak Performance: Identify and replicate your optimal study conditions\n"
    plan += "• Speed Learning: 2x video playback with active note-taking\n"
    plan += "• Memory Palace: Implement for complex information retention\n"
    plan += "• Mock Examination: Full practice test under exam conditions\n"
    
    if 'Stress' in risk_drivers:
        plan += "• Stress Inoculation: Gradual exposure to pressure situations\n"
        plan += "• Cognitive Behavioral Techniques: Challenge negative thought patterns\n"
    
    plan += """
PERFORMANCE METRICS:
□ Mock exam score improvement: Target 75%+
□ Study efficiency: 90%+ retention rate
□ Stress management: Maintain <4/10 daily
□ Network expansion: 3 new academic connections

WEEK 4: CONSOLIDATION & FUTURE-PROOFING
========================================
Focus: Maintaining gains and building sustainable systems

SUSTAINABILITY PROTOCOLS:
• System Automation: Create habits that run on autopilot
• Relapse Prevention: Identify triggers and create counter-strategies
• Performance Monitoring: Weekly self-assessment routine
• Continuous Improvement: Monthly optimization reviews

LONG-TERM STRATEGIES:
• Advanced course planning for next semester
• Scholarship and opportunity identification
• Research project initiation
• Leadership role development

FINAL ASSESSMENT TARGETS:
□ Risk probability reduced by 50%
□ Academic index: 80+ (Excellent range)
□ Consistency score: 95%+ daily completion
□ Stress level: <3/10 sustained
□ Network: 10+ academic connections
□ Leadership: 1 initiative started

NEXT STEPS:
• Graduate to Advanced Performance Coaching (APC-90 Program)
• Consider Research Excellence Track (RET-100)
• Explore Leadership Development Intensive (LDI-85)
• Plan Career Acceleration Protocol (CAP-95)

Stay exceptional,
The Valkyrie AI Team
"""
    
    return report

# ==========================================
# 4. PREMIUM SIDEBAR
# ==========================================
def premium_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="background: white; border-radius: 16px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: var(--shadow-sm); border: 1px solid var(--neutral-200);">
            <h3 style="color: var(--primary-blue); margin: 0 0 0.5rem 0; font-weight: 600;">🎓 Student Portal</h3>
            <p style="color: var(--neutral-600); margin: 0; font-size: 0.9rem;">Premium Analytics Access</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("premium_student_form"):
            st.markdown("### 📋 Student Profile")
            
            # Basic Information
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name*", "Student Name", 
                                   help="Enter your complete name",
                                   placeholder="e.g., Sarah Johnson")
            
            with col2:
                student_id = st.text_input("Student ID", "STU-2024-001", 
                                         help="Your unique identifier",
                                         placeholder="e.g., STU-2024-001")
            
            # Academic Metrics
            st.markdown("### 📊 Academic Performance")
            
            col1, col2 = st.columns(2)
            with col1:
                gpa = st.slider("GPA (0-10)", 0.0, 10.0, 7.5, 
                              help="Previous semester GPA",
                              format="%.1f")
                test_score = st.slider("Test Score", 0, 100, 75, 
                                     help="Latest test performance")
            
            with col2:
                backlog = st.selectbox("Backlogs", ["No", "Yes"], 
                                     help="Any pending subjects")
                attendance = st.slider("Attendance %", 0, 100, 85, 
                                     help="Overall attendance")
            
            # Campus Life - ONLY USE FEATURES THAT EXIST IN YOUR MODEL
            st.markdown("### 🏫 Campus Engagement")
            
            col1, col2 = st.columns(2)
            with col1:
                library_hrs = st.slider("Library Hours/Week", 0, 20, 5, 
                                      help="Weekly library time")
                extra_score = st.slider("Extracurricular Score", 0, 10, 6, 
                                      help="Activity participation (0-10)")
            
            with col2:
                study_hrs = st.slider("Daily Study Hours", 0.0, 12.0, 4.0, 
                                    help="Focused study time",
                                    format="%.1f")
            
            # Lifestyle & Wellness
            st.markdown("### 🌱 Lifestyle & Wellness")
            
            col1, col2 = st.columns(2)
            with col1:
                social_hrs = st.slider("Social Media Hours", 0.0, 8.0, 2.5, 
                                     help="Daily social media usage",
                                     format="%.1f")
                sleep_hrs = st.slider("Sleep Hours", 0.0, 12.0, 7.0, 
                                    help="Average nightly sleep",
                                    format="%.1f")
            
            with col2:
                stress_level = st.slider("Stress Level", 1, 10, 5, 
                                       help="1=Very Low, 10=Very High")
            
            # Daily Reflection
            st.markdown("### 📝 Daily Reflection")
            diary_entry = st.text_area("How are you feeling today?", 
                                     "I feel overwhelmed with the upcoming exams and assignments.",
                                     height=120,
                                     help="Our AI will analyze your emotional state",
                                     placeholder="Share your thoughts, feelings, and concerns...")
            
            # Premium submit button
            submitted = st.form_submit_button("🔍 GENERATE PREMIUM ANALYSIS", 
                                            use_container_width=True,
                                            help="Generate your comprehensive premium report")
    
    return submitted, name, student_id, gpa, test_score, backlog, attendance, library_hrs, extra_score, study_hrs, social_hrs, sleep_hrs, stress_level, diary_entry

# ==========================================
# 5. MAIN APPLICATION
# ==========================================
def main():
    # Display premium header
    display_premium_header()
    
    # Load models with premium UI
    models = load_premium_models()
    if models is None:
        st.stop()
    
    # Premium sidebar
    submitted, name, student_id, gpa, test_score, backlog, attendance, library_hrs, extra_score, study_hrs, social_hrs, sleep_hrs, stress_level, diary_entry = premium_sidebar()
    
    # Main analysis area
    if submitted:
        try:
            # Premium loading experience
            with st.spinner("🧠 Valkyrie AI Analyzing Your Profile..."):
                time.sleep(2)  # Premium feel
                
            # Process inputs with premium validation
            cleaned_diary = clean_text(diary_entry)
            vec_text = models['nlp_vectorizer'].transform([cleaned_diary])
            nlp_prob = models['nlp_model'].predict_proba(vec_text)[0][1]
            
            # Prepare premium data - ONLY FEATURES THAT EXIST IN YOUR MODEL
            raw_data = pd.DataFrame({
                'previous_sem_gpa': [gpa],
                'attendance_pct': [attendance],
                'avg_daily_study_hours': [study_hrs],
                'social_media_hours_per_day': [social_hrs],
                'sleep_hours_avg': [sleep_hrs],
                'last_test_score': [test_score],
                'is_backlog': [1 if backlog == "Yes" else 0],
                'avg_weekly_library_hours': [library_hrs],
                'extracurricular_engagement_score': [extra_score]
            })
            
            final_input = calculate_features(raw_data, nlp_prob)
            risk_prob = models['final_model'].predict_proba(final_input)[0][1]
            
            # Prepare results package
            results_package = {
                'name': name,
                'risk_prob': risk_prob,
                'academic_index': final_input['academic_index'][0],
                'nlp_prob': nlp_prob,
                'focus_ratio': final_input['focus_ratio'][0],
                'final_input': final_input,
                'models': models
            }
            
            # Display premium analysis
            risk_drivers = display_premium_analysis(results_package)
            
            # Professional report section
            st.markdown("---")
            st.markdown("### 📋 Professional 4-Week Transformation Plan")
            
            professional_plan = generate_professional_plan(risk_drivers, name, risk_prob)
            
            # Display in professional container
            st.markdown(f"""
            <div class="premium-report animate-in">
                <pre style="margin: 0; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; line-height: 1.5;">{professional_plan}</pre>
            </div>
            """, unsafe_allow_html=True)
            
            # Professional download options
            st.markdown("---")
            st.markdown("### 💾 Download Your Professional Report")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.download_button(
                    label="📄 Download Full Report",
                    data=professional_plan,
                    file_name=f"{name.replace(' ', '_')}_Valkyrie_Professional_Report_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col2:
                # Executive summary
                summary = f"""
Valkyrie AI Professional - Executive Summary
Student: {name}
Date: {datetime.now().strftime('%B %d, %Y')}
Risk Level: {'HIGH' if risk_prob > 0.6 else 'MEDIUM' if risk_prob > 0.3 else 'LOW'}
Risk Score: {risk_prob:.1%}

Priority Actions:
1. {'Fix sleep schedule immediately' if 'Sleep' in risk_drivers else 'Maintain good sleep habits'}
2. {'Increase study hours' if 'Grades' in risk_drivers else 'Continue current study pattern'}
3. {'Reduce social media usage' if 'Focus' in risk_drivers else 'Maintain digital wellness'}
4. {'Implement stress management' if 'Stress' in risk_drivers else 'Continue wellness practices'}

Next Steps: Follow the 4-week transformation plan for optimal results.
"""
                st.download_button(
                    label="📊 Download Executive Summary",
                    data=summary,
                    file_name=f"{name.replace(' ', '_')}_Executive_Summary.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col3:
                # Action items
                action_items = "\n".join([f"{i+1}. {driver}" for i, driver in enumerate(risk_drivers)]) if risk_drivers else "1. Maintain current excellence"
                st.download_button(
                    label="✅ Download Action Items",
                    data=f"Priority Actions for {name}:\n\n{action_items}",
                    file_name=f"{name.replace(' ', '_')}_Action_Items.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            # Professional footer
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: white; border-radius: 16px; margin-top: 2rem; box-shadow: var(--shadow-sm); border: 1px solid var(--neutral-200);">
                <h3 style="color: var(--primary-blue); margin: 0 0 1rem 0; font-weight: 600;">🎓 Valkyrie AI Professional Platform</h3>
                <p style="color: var(--neutral-600); margin: 0; font-size: 1rem; line-height: 1.6;">
                    Advanced machine learning meets educational psychology for unprecedented student success outcomes.
                </p>
                <p style="color: var(--neutral-500); margin: 1rem 0 0 0; font-size: 0.9rem;">
                    For professional support: support@valkyrie-ai.com | Available 24/7 for student success
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            # Simple error display without HTML formatting issues
            st.error(f"Analysis Error: {str(e)}")
            st.info("Please check your inputs and try again.")
    
    else:
        # Professional welcome screen
        st.markdown("""
        <div class="premium-card animate-in welcome-card">
            <h2 style="text-align: center; color: var(--neutral-900); margin: 0;">🎓 Welcome to Valkyrie AI Professional</h2>
            <p style="text-align: center; color: var(--neutral-600); margin: 0.5rem 0;">Unlock your academic potential with professional AI-powered counseling</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="premium-card animate-in feature-card" style="animation-delay: 0.1s;">
                <h3 style="color: var(--primary-blue); margin: 0 0 1rem 0; text-align: center;">🧠 AI Analysis</h3>
                <p style="color: var(--neutral-600); margin: 0; text-align: center; line-height: 1.6;">Advanced machine learning models analyze your academic and emotional patterns with professional-grade accuracy.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="premium-card animate-in feature-card" style="animation-delay: 0.2s;">
                <h3 style="color: var(--primary-blue); margin: 0 0 1rem 0; text-align: center;">📊 360° Insights</h3>
                <p style="color: var(--neutral-600); margin: 0; text-align: center; line-height: 1.6;">Comprehensive analysis covering academics, lifestyle, and mental wellness for holistic student success.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="premium-card animate-in feature-card" style="animation-delay: 0.3s;">
                <h3 style="color: var(--primary-blue); margin: 0 0 1rem 0; text-align: center;">🎯 Action Plans</h3>
                <p style="color: var(--neutral-600); margin: 0; text-align: center; line-height: 1.6;">Professional 4-week transformation plans with measurable outcomes and expert-grade guidance.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Professional quote section
        st.markdown("""
        <div class="premium-card animate-in" style="animation-delay: 0.4s; margin-top: 2rem; text-align: center;">
            <p style="color: var(--neutral-600); font-style: italic; font-size: 1.1rem; margin: 0;">"The future belongs to those who prepare for it today"</p>
            <p style="color: var(--neutral-500); margin: 0.5rem 0 0 0; font-size: 0.9rem;">— Malcolm X</p>
            <p style="color: var(--neutral-500); margin: 1rem 0 0 0; font-size: 0.9rem;">Complete the professional form in the sidebar to begin your transformation journey</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
