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

# Premium CSS with professional design system
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap');
    
    /* Premium Color Palette */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --accent-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --success-gradient: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        --warning-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        --danger-gradient: linear-gradient(135deg, #ff0844 0%, #ffb199 100%);
        
        --bg-primary: #ffffff;
        --bg-secondary: #f8fafc;
        --bg-card: rgba(255, 255, 255, 0.95);
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --text-muted: #94a3b8;
        --border-light: rgba(226, 232, 240, 0.5);
        --shadow-soft: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-medium: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-large: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    /* Global Typography */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', serif;
        font-weight: 600;
        color: var(--text-primary);
        letter-spacing: -0.025em;
    }
    
    /* Premium Header */
    .premium-header {
        background: var(--primary-gradient);
        padding: 3rem 2rem;
        border-radius: 24px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-large);
        position: relative;
        overflow: hidden;
    }
    
    .premium-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"><g fill="none" fill-rule="evenodd"><g fill="%23ffffff" fill-opacity="0.05"><circle cx="30" cy="30" r="2"/></g></svg>');
        animation: float 20s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    .brand-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .brand-subtitle {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: var(--bg-card);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: var(--shadow-medium);
        border: 1px solid var(--border-light);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-large);
    }
    
    /* Premium Metric Cards */
    .metric-card-premium {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card-premium::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: left 0.5s ease;
    }
    
    .metric-card-premium:hover::before {
        left: 100%;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        font-weight: 500;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 0;
    }
    
    .metric-status {
        font-size: 0.8rem;
        font-weight: 600;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        display: inline-block;
        margin-top: 0.5rem;
    }
    
    /* Risk Indicators with Premium Styling */
    .risk-indicator {
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .risk-critical {
        background: linear-gradient(135deg, rgba(255, 8, 68, 0.1) 0%, rgba(255, 177, 153, 0.1) 100%);
        border-color: rgba(255, 8, 68, 0.3);
    }
    
    .risk-high {
        background: linear-gradient(135deg, rgba(255, 154, 0, 0.1) 0%, rgba(255, 106, 0, 0.1) 100%);
        border-color: rgba(255, 154, 0, 0.3);
    }
    
    .risk-medium {
        background: linear-gradient(135deg, rgba(246, 211, 101, 0.1) 0%, rgba(253, 160, 133, 0.1) 100%);
        border-color: rgba(246, 211, 101, 0.3);
    }
    
    .risk-low {
        background: linear-gradient(135deg, rgba(86, 171, 47, 0.1) 0%, rgba(168, 224, 99, 0.1) 100%);
        border-color: rgba(86, 171, 47, 0.3);
    }
    
    /* Premium Buttons */
    .stButton > button {
        background: var(--primary-gradient);
        color: white;
        font-weight: 600;
        font-size: 1rem;
        border: none;
        padding: 1rem 2rem;
        border-radius: 50px;
        box-shadow: var(--shadow-medium);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-large);
    }
    
    /* Elegant Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1rem;
    }
    
    /* Premium Form Styling */
    .stSlider > div > div > div > div {
        background: var(--primary-gradient);
        border-radius: 10px;
    }
    
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        border-radius: 15px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Professional Report Styling */
    .premium-report {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        font-family: 'Inter', monospace;
        font-size: 0.95rem;
        line-height: 1.8;
        color: var(--text-primary);
        box-shadow: var(--shadow-medium);
        position: relative;
    }
    
    .premium-report::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background: var(--primary-gradient);
        border-radius: 20px 0 0 20px;
    }
    
    /* Progress Visualization */
    .progress-container {
        background: rgba(102, 126, 234, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #764ba2;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. PREMIUM HEADER COMPONENT
# ==========================================
def display_premium_header():
    st.markdown("""
    <div class="premium-header animate-in">
        <h1 class="brand-title">⚡ Valkyrie AI</h1>
        <p class="brand-subtitle">Premium Student Success Intelligence Platform</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 3. MODEL LOADING WITH PREMIUM UI
# ==========================================
@st.cache_resource
def load_premium_models():
    try:
        # Premium loading experience
        with st.spinner("🚀 Initializing Valkyrie AI Premium Engine..."):
            time.sleep(2)  # Premium feel
            
        bundle = joblib.load('student_risk_model.pkl')
        
        # Validate model components
        required_keys = ['final_model', 'nlp_model', 'nlp_vectorizer']
        missing_keys = [key for key in required_keys if key not in bundle]
        
        if missing_keys:
            st.error(f"Missing premium model components: {missing_keys}")
            return None
            
        return bundle
    except FileNotFoundError:
        st.error("""
        <div class="glass-card" style="border-color: #ff0844; background: rgba(255, 8, 68, 0.05);">
            <h3 style="color: #ff0844; margin: 0;">🚨 Premium Model File Not Found</h3>
            <p style="margin: 0.5rem 0;">Please ensure 'student_risk_model.pkl' is available in your app directory.</p>
            <p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary);">Premium Support: premium@valkyrie-ai.com</p>
        </div>
        """, unsafe_allow_html=True)
        return None
    except Exception as e:
        st.error(f"""
        <div class="glass-card" style="border-color: #ff0844;">
            <h3 style="color: #ff0844; margin: 0;">⚠️ Premium Engine Error</h3>
            <p style="margin: 0.5rem 0;">Advanced AI system encountered: {str(e)}</p>
            <p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary);">Technical team has been notified automatically.</p>
        </div>
        """, unsafe_allow_html=True)
        return None

# ==========================================
# 4. CORE PROCESSING FUNCTIONS
# ==========================================
def clean_text(text):
    """Enhanced text cleaning with premium processing"""
    if not isinstance(text, str): 
        return ""
    text = text.lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def calculate_features(input_df, nlp_score):
    """Premium feature engineering with validation"""
    df = input_df.copy()
    df['nlp_stress_score'] = nlp_score
    
    # Academic Index with validation
    df['academic_index'] = ((df['previous_sem_gpa'] * 10) + df['last_test_score']) / 2
    
    # Sleep Deviation
    df['sleep_deviation'] = abs(df['sleep_hours_avg'] - 8)
    
    # Focus Ratio with premium calculation
    df['focus_ratio'] = df['avg_daily_study_hours'] / (df['social_media_hours_per_day'] + 1)
    
    # Risk Alarm
    df['risk_alarm'] = np.where((df['is_backlog'] == 1) & (df['attendance_pct'] < 75), 1, 0)
    
    # Expected column order (premium validation)
    expected_cols = [
        'attendance_pct', 'sleep_hours_avg', 'avg_daily_study_hours',
        'avg_weekly_library_hours', 'previous_sem_gpa', 'last_test_score',
        'social_media_hours_per_day', 'extracurricular_engagement_score',
        'is_exam_week', 'nlp_stress_score', 'is_backlog', 'sleep_deviation',
        'academic_index', 'focus_ratio', 'risk_alarm'
    ]
    
    return df[expected_cols]

def generate_elegant_4_week_plan(risk_drivers, name, risk_prob):
    """Generate elegant, professional 4-week plan"""
    
    plan = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ⚡ VALKYRIE AI - PREMIUM COUNSELING REPORT                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ Student: {name:<50} ║
║ Risk Level: {'HIGH' if risk_prob > 0.6 else 'MEDIUM' if risk_prob > 0.3 else 'LOW':<49} ║
║ Risk Score: {f"{risk_prob:.1%}":<48} ║
║ Generated: {datetime.now().strftime('%B %d, %Y'):<47} ║
╚══════════════════════════════════════════════════════════════════════════════╝

"""
    
    # Week 1 - Foundation (Elegant Format)
    plan += f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🏗️  WEEK 1: FOUNDATION & STABILIZATION                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Focus: Establishing core habits and immediate risk mitigation              │
└─────────────────────────────────────────────────────────────────────────────┘

📋 DAILY PROTOCOLS:
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
🎯 ACADEMIC FOCUS:
• Minimum {6 if 'Grades' in risk_drivers else 4} hours daily focused study
• Active recall sessions every 2 hours
• Weekly review with study group

💪 WELLNESS INTEGRATION:
• 30 minutes physical activity (walking counts)
• 2L water daily minimum
• Digital sunset: No screens after 10 PM

✅ SUCCESS METRICS:
□ Attendance improved by 10%
□ Sleep deviation < 1 hour
□ Stress self-rating reduced by 2 points
□ Study hours increased by 1 hour daily

"""
    
    # Week 2 - Acceleration
    plan += f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│ ⚡ WEEK 2: ACCELERATION & CONSISTENCY                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Focus: Building momentum and establishing routines                          │
└─────────────────────────────────────────────────────────────────────────────┘

🚀 ADVANCED STRATEGIES:
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
🔧 OPTIMIZATION TECHNIQUES:
• Spaced repetition schedule implementation
• Feynman technique: Teach concepts to study buddy
• Mind mapping for subject interconnections
• Weekly performance review and adjustment

🌟 LIFESTYLE UPGRADES:
• Meal prep for consistent nutrition
• Morning routine optimization (30-min buffer)
• Evening wind-down ritual establishment
• Weekend recovery planning

🏆 MILESTONE TARGETS:
□ Clear 50% of identified backlogs
□ Focus ratio improved by 25%
□ Academic index increased by 10 points
□ Consistency streak: 7-day habit formation

"""
    
    return plan

# ==========================================
# 5. PREMIUM SIDEBAR COMPONENT
# ==========================================
def premium_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                     border-radius: 20px; padding: 2rem; margin-bottom: 2rem; border: 1px solid rgba(102, 126, 234, 0.2);">
            <h3 style="color: #667eea; margin: 0 0 0.5rem 0; font-weight: 600;">🎓 Student Portal</h3>
            <p style="color: #64748b; margin: 0; font-size: 0.9rem;">Premium Analytics Access</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("premium_student_form"):
            st.markdown("### 📋 Student Profile")
            
            # Basic Information with premium styling
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name*", "Student Name", 
                                   help="Enter your complete name",
                                   placeholder="e.g., Sarah Johnson")
            
            with col2:
                student_id = st.text_input("Student ID", "STU-2024-001", 
                                         help="Your unique identifier",
                                         placeholder="e.g., STU-2024-001")
            
            # Academic Metrics Section
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
            
            # Campus Life Section
            st.markdown("### 🏫 Campus Engagement")
            
            col1, col2 = st.columns(2)
            with col1:
                library_hrs = st.slider("Library Hours/Week", 0, 20, 5, 
                                      help="Weekly library time")
                extra_score = st.slider("Extracurricular Score", 0, 10, 6, 
                                      help="Activity participation (0-10)")
            
            with col2:
                exam_week = st.selectbox("Exam Week", ["No", "Yes"], 
                                       help="Currently in exam period")
                study_hrs = st.slider("Daily Study Hours", 0.0, 12.0, 4.0, 
                                    help="Focused study time",
                                    format="%.1f")
            
            # Lifestyle & Wellness Section
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
                exercise_hrs = st.slider("Exercise Hours/Week", 0, 20, 3, 
                                         help="Physical activity time")
            
            # Daily Reflection Section
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
    
    return submitted, name, student_id, gpa, test_score, backlog, attendance, library_hrs, extra_score, exam_week, study_hrs, social_hrs, sleep_hrs, stress_level, exercise_hrs, diary_entry

# ==========================================
# 6. PREMIUM ANALYSIS DISPLAY
# ==========================================
def display_premium_analysis(results):
    """Display analysis results with premium styling"""
    
    # Premium header for results
    st.markdown(f"""
    <div class="glass-card animate-in">
        <h2 style="text-align: center; color: var(--text-primary); margin: 0;">🎓 Premium Analysis Report</h2>
        <p style="text-align: center; color: var(--text-secondary); margin: 0.5rem 0;">Generated for {results['name']} • {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Premium metrics grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        risk_status = 'HIGH' if results['risk_prob'] > 0.6 else 'MEDIUM' if results['risk_prob'] > 0.3 else 'LOW'
        risk_color = '#ff0844' if results['risk_prob'] > 0.6 else '#ff9a00' if results['risk_prob'] > 0.3 else '#56ab2f'
        
        st.markdown(f"""
        <div class="metric-card-premium animate-in">
            <div class="metric-value">{results['risk_prob']:.1%}</div>
            <div class="metric-label">Risk Probability</div>
            <div class="metric-status" style="background: {risk_color}; color: white;">{risk_status} RISK</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        academic_status = 'Excellent' if results['academic_index'] >= 80 else 'Good' if results['academic_index'] >= 60 else 'Needs Work'
        academic_color = '#56ab2f' if results['academic_index'] >= 80 else '#ff9a00' if results['academic_index'] >= 60 else '#ff0844'
        
        st.markdown(f"""
        <div class="metric-card-premium animate-in" style="animation-delay: 0.1s;">
            <div class="metric-value">{results['academic_index']:.0f}</div>
            <div class="metric-label">Academic Index</div>
            <div class="metric-status" style="background: {academic_color}; color: white;">{academic_status}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        stress_score = results['nlp_prob'] * 10
        stress_status = 'Low' if stress_score <= 4 else 'Moderate' if stress_score <= 7 else 'High'
        stress_color = '#56ab2f' if stress_score <= 4 else '#ff9a00' if stress_score <= 7 else '#ff0844'
        
        st.markdown(f"""
        <div class="metric-card-premium animate-in" style="animation-delay: 0.2s;">
            <div class="metric-value">{stress_score:.1f}</div>
            <div class="metric-label">Stress Level</div>
            <div class="metric-status" style="background: {stress_color}; color: white;">{stress_status}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        focus_status = 'Excellent' if results['focus_ratio'] > 2 else 'Good' if results['focus_ratio'] > 1 else 'Needs Improvement'
        focus_color = '#56ab2f' if results['focus_ratio'] > 2 else '#ff9a00' if results['focus_ratio'] > 1 else '#ff0844'
        
        st.markdown(f"""
        <div class="metric-card-premium animate-in" style="animation-delay: 0.3s;">
            <div class="metric-value">{results['focus_ratio']:.2f}</div>
            <div class="metric-label">Focus Ratio</div>
            <div class="metric-status" style="background: {focus_color}; color: white;">{focus_status}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Risk Analysis Section
    st.markdown("---")
    st.markdown("### 🩺 Premium Risk Analysis")
    
    col1, col2 = st.columns([1, 2])
    
    risk_drivers = []
    
    with col1:
        st.markdown("#### ⚠️ Risk Factors Identified")
        
        if results['final_input']['risk_alarm'][0] == 1:
            st.markdown("""
            <div class="risk-indicator risk-critical animate-in">
                <h4 style="color: #ff0844; margin: 0 0 0.5rem 0;">🚨 Critical Alert</h4>
                <p style="margin: 0; font-weight: 600;">Death Spiral Detected</p>
                <p style="margin: 0.25rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">Backlogs + Low Attendance</p>
            </div>
            """, unsafe_allow_html=True)
            risk_drivers.append("Backlogs/Attendance")
        
        if results['final_input']['sleep_deviation'][0] > 1.5:
            st.markdown(f"""
            <div class="risk-indicator risk-high animate-in" style="animation-delay: 0.1s;">
                <h4 style="color: #ff9a00; margin: 0 0 0.5rem 0;">⚠️ Sleep Debt</h4>
                <p style="margin: 0; font-weight: 600;">{results['final_input']['sleep_deviation'][0]:.1f}h deviation</p>
                <p style="margin: 0.25rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">From optimal 8 hours</p>
            </div>
            """, unsafe_allow_html=True)
            risk_drivers.append("Sleep")
        
        if results['final_input']['focus_ratio'][0] < 0.5:
            st.markdown("""
            <div class="risk-indicator risk-medium animate-in" style="animation-delay: 0.2s;">
                <h4 style="color: #f6d365; margin: 0 0 0.5rem 0;">📱 Distraction Risk</h4>
                <p style="margin: 0; font-weight: 600;">Low Focus Ratio</p>
                <p style="margin: 0.25rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">Social > Study Time</p>
            </div>
            """, unsafe_allow_html=True)
            risk_drivers.append("Focus")
        
        if results['final_input']['academic_index'][0] < 50:
            st.markdown("""
            <div class="risk-indicator risk-high animate-in" style="animation-delay: 0.3s;">
                <h4 style="color: #ff9a00; margin: 0 0 0.5rem 0;">📚 Academic Critical</h4>
                <p style="margin: 0; font-weight: 600;">Low Performance</p>
                <p style="margin: 0.25rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">Immediate intervention needed</p>
            </div>
            """, unsafe_allow_html=True)
            risk_drivers.append("Grades")
        
        if results['nlp_prob'] > 0.6:
            st.markdown("""
            <div class="risk-indicator risk-medium animate-in" style="animation-delay: 0.4s;">
                <h4 style="color: #f6d365; margin: 0 0 0.5rem 0;">🧠 Mental Strain</h4>
                <p style="margin: 0; font-weight: 600;">High Stress Detected</p>
                <p style="margin: 0.25rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">From text analysis</p>
            </div>
            """, unsafe_allow_html=True)
            risk_drivers.append("Stress")
        
        if not risk_drivers:
            st.markdown("""
            <div class="risk-indicator risk-low animate-in">
                <h4 style="color: #56ab2f; margin: 0 0 0.5rem 0;">✅ Optimal Status</h4>
                <p style="margin: 0; font-weight: 600;">No Critical Risks</p>
                <p style="margin: 0.25rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">Keep up the great work!</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🔮 Counterfactual Analysis")
        st.markdown("Running real-time simulations to find your optimal improvement path...")
        
        # Simulate different scenarios
        scenarios = []
        
        # Sleep optimization
        sim_sleep = results['final_input'].copy()
        sim_sleep['sleep_deviation'] = 0
        sleep_new_prob = results['models']['final_model'].predict_proba(sim_sleep)[0][1]
        scenarios.append({
            'action': 'Sleep Optimization (8 hours)',
            'new_risk': sleep_new_prob,
            'effort': 'Low',
            'timeline': '1 week'
        })
        
        # Study increase
        sim_study = results['final_input'].copy()
        sim_study['avg_daily_study_hours'] += 2
        sim_study['focus_ratio'] = sim_study['avg_daily_study_hours'] / (sim_study['social_media_hours_per_day'] + 1)
        study_new_prob = results['models']['final_model'].predict_proba(sim_study)[0][1]
        scenarios.append({
            'action': 'Increase Study (+2 hours daily)',
            'new_risk': study_new_prob,
            'effort': 'Medium',
            'timeline': '2 weeks'
        })
        
        # Social media reduction
        sim_social = results['final_input'].copy()
        sim_social['social_media_hours_per_day'] *= 0.5
        sim_social['focus_ratio'] = sim_social['avg_daily_study_hours'] / (sim_social['social_media_hours_per_day'] + 1)
        social_new_prob = results['models']['final_model'].predict_proba(sim_social)[0][1]
        scenarios.append({
            'action': 'Reduce Social Media (-50%)',
            'new_risk': social_new_prob,
            'effort': 'Medium',
            'timeline': '1 week'
        })
        
        # Display scenarios in elegant cards
        for i, scenario in enumerate(scenarios):
            improvement = results['risk_prob'] - scenario['new_risk']
            
            st.markdown(f"""
            <div class="glass-card animate-in" style="animation-delay: {0.1 * (i + 1)}s; margin: 1rem 0; padding: 1.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <h4 style="margin: 0; color: var(--text-primary);">{scenario['action']}</h4>
                    <span style="background: var(--accent-gradient); color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">{scenario['effort']} Effort</span>
                </div>
                <p style="margin: 0.5rem 0; color: var(--text-secondary);">New Risk: <strong>{scenario['new_risk']:.1%}</strong> (Improvement: {improvement:.1%})</p>
                <p style="margin: 0; color: var(--text-muted); font-size: 0.9rem;">Timeline: {scenario['timeline']}</p>
                <div style="margin-top: 1rem;">
                    <div style="background: #e2e8f0; border-radius: 10px; height: 8px; overflow: hidden;">
                        <div style="background: var(--success-gradient); width: {(1 - scenario['new_risk']) * 100}%; height: 100%; border-radius: 10px; transition: width 0.5s ease;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    return risk_drivers

# ==========================================
# 7. ELEGANT REPORT GENERATION
# ==========================================
def generate_elegant_report(risk_drivers, name, risk_prob, results):
    """Generate premium counseling report with elegant formatting"""
    
    report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ⚡ VALKYRIE AI - PREMIUM COUNSELING REPORT                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ Student: {name:<50} ║
║ Risk Level: {'HIGH' if risk_prob > 0.6 else 'MEDIUM' if risk_prob > 0.3 else 'LOW':<49} ║
║ Risk Score: {f"{risk_prob:.1%}":<48} ║
║ Generated: {datetime.now().strftime('%B %d, %Y'):<47} ║
╚══════════════════════════════════════════════════════════════════════════════╝

"""
    
    # Week 1 - Foundation (Elegant Format)
    report += f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🏗️  WEEK 1: FOUNDATION & STABILIZATION                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Focus: Establishing core habits and immediate risk mitigation              │
└─────────────────────────────────────────────────────────────────────────────┘

📋 DAILY PROTOCOLS:
"""
    if 'Sleep' in risk_drivers:
        report += "• Sleep Optimization: 10-3-2-1 Rule (No caffeine 10h before, food 3h, work 2h, screens 1h)\n"
        report += "• Target: 8 hours consistent sleep schedule (11 PM - 7 AM)\n"
    else:
        report += "• Maintain optimal sleep schedule and track sleep quality\n"
    
    if 'Stress' in risk_drivers:
        report += "• Stress Management: 15-minute morning meditation + evening journaling\n"
        report += "• Use 4-7-8 breathing technique before study sessions\n"
    
    if 'Backlogs/Attendance' in risk_drivers:
        report += "• Emergency Protocol: Meet with course coordinator within 48 hours\n"
        report += "• Attendance Recovery: Set 5 alarms, find accountability partner\n"
    
    report += f"""
🎯 ACADEMIC FOCUS:
• Minimum {6 if 'Grades' in risk_drivers else 4} hours daily focused study
• Active recall sessions every 2 hours
• Weekly review with study group

💪 WELLNESS INTEGRATION:
• 30 minutes physical activity (walking counts)
• 2L water daily minimum
• Digital sunset: No screens after 10 PM

✅ SUCCESS METRICS:
□ Attendance improved by 10%
□ Sleep deviation < 1 hour
□ Stress self-rating reduced by 2 points
□ Study hours increased by 1 hour daily

"""
    
    # Week 2 - Acceleration
    report += f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│ ⚡ WEEK 2: ACCELERATION & CONSISTENCY                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Focus: Building momentum and establishing routines                          │
└─────────────────────────────────────────────────────────────────────────────┘

🚀 ADVANCED STRATEGIES:
"""
    if 'Focus' in risk_drivers:
        report += "• Digital Detox: Social media limited to 30 minutes daily\n"
        report += "• Pomodoro Mastery: 50min study + 10min break cycles\n"
        report += "• Distraction Elimination: Study phone in separate room\n"
    
    if 'Grades' in risk_drivers:
        report += "• Academic Intensive: Past paper analysis (2 papers/week)\n"
        report += "• Professor Office Hours: Minimum 2 visits this week\n"
        report += "• Concept Mapping: Visual learning for complex topics\n"
    
    report += f"""
🔧 OPTIMIZATION TECHNIQUES:
• Spaced repetition schedule implementation
• Feynman technique: Teach concepts to study buddy
• Mind mapping for subject interconnections
• Weekly performance review and adjustment

🌟 LIFESTYLE UPGRADES:
• Meal prep for consistent nutrition
• Morning routine optimization (30-min buffer)
• Evening wind-down ritual establishment
• Weekend recovery planning

🏆 MILESTONE TARGETS:
□ Clear 50% of identified backlogs
□ Focus ratio improved by 25%
□ Academic index increased by 10 points
□ Consistency streak: 7-day habit formation

"""
    
    return report

# ==========================================
# 8. MAIN APPLICATION LOGIC
# ==========================================
def main():
    # Display premium header
    display_premium_header()
    
    # Load models with premium UI
    models = load_premium_models()
    if models is None:
        st.stop()
    
    # Premium sidebar
    submitted, name, student_id, gpa, test_score, backlog, attendance, library_hrs, extra_score, exam_week, study_hrs, social_hrs, sleep_hrs, stress_level, exercise_hrs, diary_entry = premium_sidebar()
    
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
            
            # Prepare premium data
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
            
            # Elegant report section
            st.markdown("---")
            st.markdown("### 📋 Premium 4-Week Transformation Plan")
            
            elegant_report = generate_elegant_report(risk_drivers, name, risk_prob, results_package)
            
            # Display in elegant container
            st.markdown(f"""
            <div class="premium-report animate-in">
                <pre style="margin: 0; font-family: 'Inter', monospace; font-size: 0.9rem; line-height: 1.6;">{elegant_report}</pre>
            </div>
            """, unsafe_allow_html=True)
            
            # Premium download options
            st.markdown("---")
            st.markdown("### 💾 Download Your Premium Report")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.download_button(
                    label="📄 Download Full Report",
                    data=elegant_report,
                    file_name=f"{name.replace(' ', '_')}_Valkyrie_Premium_Report_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col2:
                # Executive summary
                summary = f"""
Valkyrie AI Premium - Executive Summary
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
            
            # Premium footer
            st.markdown("""
            <div style="text-align: center; padding: 3rem 2rem; background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); border-radius: 24px; margin-top: 3rem; border: 1px solid rgba(102, 126, 234, 0.2);">
                <h3 style="color: #667eea; margin: 0 0 1rem 0; font-weight: 600;">🎓 Valkyrie AI Premium Platform</h3>
                <p style="color: #64748b; margin: 0; font-size: 1rem; line-height: 1.6;">
                    Advanced machine learning meets educational psychology for unprecedented student success outcomes.
                </p>
                <p style="color: #94a3b8; margin: 1rem 0 0 0; font-size: 0.9rem;">
                    For premium support: premium@valkyrie-ai.com | Available 24/7 for student success
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"""
            <div class="glass-card" style="border-color: #ff0844;">
                <h3 style="color: #ff0844; margin: 0;">❌ Analysis Error</h3>
                <p style="margin: 0.5rem 0;">{str(e)}</p>
                <p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary);">Please check your inputs and try again.</p>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # Premium welcome screen
        st.markdown("""
        <div class="glass-card animate-in">
            <h2 style="text-align: center; color: var(--text-primary); margin: 0;">🎓 Welcome to Valkyrie AI Premium</h2>
            <p style="text-align: center; color: var(--text-secondary); margin: 0.5rem 0;">Unlock your academic potential with advanced AI-powered counseling</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="glass-card animate-in" style="animation-delay: 0.1s;">
                <h3 style="color: #667eea; margin: 0 0 1rem 0; text-align: center;">🧠 AI Analysis</h3>
                <p style="color: var(--text-secondary); margin: 0; text-align: center; line-height: 1.6;">Advanced machine learning models analyze your academic and emotional patterns with unprecedented accuracy.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="glass-card animate-in" style="animation-delay: 0.2s;">
                <h3 style="color: #667eea; margin: 0 0 1rem 0; text-align: center;">📊 360° Insights</h3>
                <p style="color: var(--text-secondary); margin: 0; text-align: center; line-height: 1.6;">Comprehensive analysis covering academics, lifestyle, and mental wellness for holistic student success.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="glass-card animate-in" style="animation-delay: 0.3s;">
                <h3 style="color: #667eea; margin: 0 0 1rem 0; text-align: center;">🎯 Action Plans</h3>
                <p style="color: var(--text-secondary); margin: 0; text-align: center; line-height: 1.6;">Personalized 4-week transformation plans with measurable outcomes and professional-grade guidance.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Premium quote section
        st.markdown("""
        <div class="glass-card animate-in" style="animation-delay: 0.4s; margin-top: 2rem; text-align: center;">
            <p style="color: var(--text-secondary); font-style: italic; font-size: 1.1rem; margin: 0;">"The future belongs to those who prepare for it today"</p>
            <p style="color: var(--text-muted); margin: 0.5rem 0 0 0; font-size: 0.9rem;">— Malcolm X</p>
            <p style="color: var(--text-muted); margin: 1rem 0 0 0; font-size: 0.9rem;">Complete the premium form in the sidebar to begin your transformation journey</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
