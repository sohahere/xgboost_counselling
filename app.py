"""
Premium Student Risk Assessment & Counseling App
A comprehensive 360° counseling system with personalized action plans
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import re
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import shap
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Student 360° Risk Assessment & Counseling",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #34495e;
        text-align: center;
        margin-bottom: 3rem;
    }
    .risk-card {
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .high-risk {
        background: linear-gradient(135deg, #ff6b6b, #ee5a52);
        color: white;
    }
    .medium-risk {
        background: linear-gradient(135deg, #feca57, #ff9ff3);
        color: white;
    }
    .low-risk {
        background: linear-gradient(135deg, #48cae4, #00b4d8);
        color: white;
    }
    .counseling-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #0077b6;
    }
    .action-item {
        background: white;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 4px solid #0077b6;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .metric-box {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    .progress-bar {
        width: 100%;
        height: 20px;
        background-color: #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        transition: width 0.3s ease;
    }
    </style>
""", unsafe_allow_html=True)

# Load models (these will be uploaded to GitHub)
@st.cache_resource
def load_models():
    try:
        with open('nlp_model.pkl', 'rb') as f:
            nlp_model = pickle.load(f)
        with open('tfidf_vectorizer.pkl', 'rb') as f:
            tfidf = pickle.load(f)
        with open('xgboost_model.pkl', 'rb') as f:
            xgb_model = pickle.load(f)
        with open('model_metadata.pkl', 'rb') as f:
            metadata = pickle.load(f)
        return nlp_model, tfidf, xgb_model, metadata
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None, None, None

# Text preprocessing
def clean_text(text):
    if not isinstance(text, str): return ""
    text = text.lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Risk assessment function
def assess_risk(student_data, nlp_model, tfidf, xgb_model, metadata):
    # Clean and vectorize text
    clean_text_data = clean_text(student_data.get('daily_text_log', ''))
    text_vector = tfidf.transform([clean_text_data])
    
    # Get NLP stress score
    nlp_stress_score = nlp_model.predict_proba(text_vector)[0, 1]
    
    # Prepare features for XGBoost
    features = {
        'previous_sem_gpa': student_data['previous_sem_gpa'],
        'last_test_score': student_data['last_test_score'],
        'attendance_pct': student_data['attendance_pct'],
        'avg_daily_study_hours': student_data['avg_daily_study_hours'],
        'social_media_hours_per_day': student_data['social_media_hours_per_day'],
        'sleep_hours_avg': student_data['sleep_hours_avg'],
        'is_backlog': 1 if student_data['backlog_count'] > 0 else 0,
        'nlp_stress_score': nlp_stress_score
    }
    
    # Calculate engineered features
    features['academic_index'] = (features['previous_sem_gpa'] * 10 + features['last_test_score']) / 2
    features['sleep_deviation'] = abs(features['sleep_hours_avg'] - 8)
    features['focus_ratio'] = features['avg_daily_study_hours'] / (features['social_media_hours_per_day'] + 1)
    features['risk_alarm'] = 1 if (features['is_backlog'] == 1 and features['attendance_pct'] < 75) else 0
    
    # Create feature vector in correct order
    feature_names = metadata['feature_names']
    feature_vector = np.array([[features[name] for name in feature_names]])
    
    # Get risk prediction
    risk_prob = xgb_model.predict_proba(feature_vector)[0, 1]
    risk_prediction = 1 if risk_prob >= metadata['threshold'] else 0
    
    return risk_prob, risk_prediction, features, nlp_stress_score

# Generate comprehensive counseling report
def generate_counseling_report(risk_score, features, nlp_stress_score, student_data):
    report = {
        'risk_level': 'HIGH' if risk_score >= 0.5 else 'MEDIUM' if risk_score >= 0.3 else 'LOW',
        'risk_percentage': risk_score * 100,
        'nlp_stress_score': nlp_stress_score * 100,
        'key_issues': [],
        'recommendations': [],
        'action_plan': [],
        'timeline': {}
    }
    
    # Analyze key issues
    if features['academic_index'] < 60:
        report['key_issues'].append({
            'issue': 'Low Academic Performance',
            'severity': 'HIGH' if features['academic_index'] < 40 else 'MEDIUM',
            'details': f'Academic Index: {features["academic_index"]:.1f}/100'
        })
    
    if features['sleep_deviation'] > 2:
        report['key_issues'].append({
            'issue': 'Poor Sleep Pattern',
            'severity': 'HIGH' if features['sleep_deviation'] > 3 else 'MEDIUM',
            'details': f'Deviation from ideal 8 hours: {features["sleep_deviation"]:.1f} hours'
        })
    
    if features['focus_ratio'] < 0.5:
        report['key_issues'].append({
            'issue': 'Low Focus Ratio',
            'severity': 'HIGH' if features['focus_ratio'] < 0.3 else 'MEDIUM',
            'details': f'Study to distraction ratio: {features["focus_ratio"]:.2f}'
        })
    
    if features['is_backlog'] == 1:
        report['key_issues'].append({
            'issue': 'Academic Backlogs',
            'severity': 'HIGH',
            'details': 'Outstanding backlogs detected'
        })
    
    if features['attendance_pct'] < 75:
        report['key_issues'].append({
            'issue': 'Low Attendance',
            'severity': 'HIGH' if features['attendance_pct'] < 60 else 'MEDIUM',
            'details': f'Current attendance: {features["attendance_pct"]:.1f}%'
        })
    
    if nlp_stress_score > 0.7:
        report['key_issues'].append({
            'issue': 'High Psychological Stress',
            'severity': 'HIGH' if nlp_stress_score > 0.85 else 'MEDIUM',
            'details': f'Stress detected from text analysis: {nlp_stress_score*100:.1f}%'
        })
    
    # Generate recommendations
    for issue in report['key_issues']:
        if issue['issue'] == 'Low Academic Performance':
            report['recommendations'].extend([
                "Schedule daily 2-hour focused study sessions",
                "Join study groups with high-performing peers",
                "Meet with professors during office hours",
                "Use active learning techniques (flashcards, practice tests)"
            ])
        
        elif issue['issue'] == 'Poor Sleep Pattern':
            report['recommendations'].extend([
                "Establish fixed sleep schedule (10 PM - 6 AM)",
                "Avoid screens 1 hour before bedtime",
                "Create relaxing bedtime routine",
                "Limit caffeine intake after 2 PM"
            ])
        
        elif issue['issue'] == 'Low Focus Ratio':
            report['recommendations'].extend([
                "Use Pomodoro technique (25 min study, 5 min break)",
                "Study in distraction-free environment",
                "Use website blockers during study hours",
                "Keep phone in another room while studying"
            ])
        
        elif issue['issue'] == 'Academic Backlogs':
            report['recommendations'].extend([
                "Create backlog clearance timeline",
                "Prioritize clearing 1-2 backlogs per month",
                "Seek help from academic advisor",
                "Consider summer/winter courses"
            ])
        
        elif issue['issue'] == 'Low Attendance':
            report['recommendations'].extend([
                "Set multiple alarms for classes",
                "Find an attendance buddy",
                "Prepare clothes/materials night before",
                "Reward yourself for perfect attendance weekly"
            ])
    
    # Generate 4-week action plan
    report['action_plan'] = generate_4_week_plan(report['key_issues'], features)
    
    return report

# Generate detailed 4-week action plan
def generate_4_week_plan(issues, features):
    plan = {
        'Week 1': {'theme': 'Assessment & Immediate Actions', 'tasks': []},
        'Week 2': {'theme': 'Building Foundations', 'tasks': []},
        'Week 3': {'theme': 'Consistency & Improvement', 'tasks': []},
        'Week 4': {'theme': 'Evaluation & Future Planning', 'tasks': []}
    }
    
    # Week 1 tasks
    plan['Week 1']['tasks'].extend([
        "Complete detailed self-assessment of current habits",
        "Meet with academic advisor to discuss backlogs",
        "Set up study schedule and stick to it for 5 days",
        "Start sleep hygiene routine (fixed bedtime)",
        "Install focus apps (Forest, Cold Turkey, etc.)"
    ])
    
    # Week 2 tasks
    plan['Week 2']['tasks'].extend([
        "Join at least one study group",
        "Complete backlog assignment #1",
        "Maintain 90% attendance this week",
        "Practice Pomodoro technique daily",
        "Reduce social media by 25%"
    ])
    
    # Week 3 tasks
    plan['Week 3']['tasks'].extend([
        "Meet with professor for difficult subjects",
        "Complete backlog assignment #2",
        "Achieve 95% attendance this week",
        "Take practice test for upcoming exams",
        "Maintain consistent sleep schedule"
    ])
    
    # Week 4 tasks
    plan['Week 4']['tasks'].extend([
        "Evaluate progress with advisor",
        "Complete final backlog assignment",
        "Take mock exam to assess improvement",
        "Plan next month's goals",
        "Celebrate improvements (healthy reward)"
    ])
    
    return plan

# Main app
def main():
    # Title
    st.markdown('<h1 class="main-header">🎓 Student 360° Risk Assessment</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Comprehensive AI-Powered Counseling & Action Planning System</p>', unsafe_allow_html=True)
    
    # Load models
    nlp_model, tfidf, xgb_model, metadata = load_models()
    
    if nlp_model is None:
        st.error("Models not loaded. Please ensure model files are in the correct location.")
        return
    
    # Sidebar for student input
    st.sidebar.header("📊 Student Information")
    
    with st.sidebar.form("student_form"):
        st.subheader("Academic Performance")
        previous_sem_gpa = st.slider("Previous Semester GPA", 0.0, 10.0, 7.0, 0.1)
        last_test_score = st.slider("Last Test Score", 0, 100, 75, 1)
        attendance_pct = st.slider("Attendance Percentage", 0, 100, 85, 1)
        backlog_count = st.number_input("Number of Backlogs", 0, 10, 0, 1)
        
        st.subheader("Study Habits")
        avg_daily_study_hours = st.slider("Average Daily Study Hours", 0.0, 12.0, 4.0, 0.5)
        social_media_hours_per_day = st.slider("Social Media Hours Per Day", 0.0, 12.0, 3.0, 0.5)
        
        st.subheader("Health & Lifestyle")
        sleep_hours_avg = st.slider("Average Sleep Hours", 0.0, 12.0, 7.0, 0.5)
        
        st.subheader("Daily Journal Entry")
        daily_text_log = st.text_area(
            "Write about your day, feelings, or any concerns...",
            height=150,
            placeholder="Today I felt... My main concerns are... I need help with..."
        )
        
        submitted = st.form_submit_button("🔍 Analyze Risk", use_container_width=True)
    
    if submitted:
        # Prepare student data
        student_data = {
            'previous_sem_gpa': previous_sem_gpa,
            'last_test_score': last_test_score,
            'attendance_pct': attendance_pct,
            'avg_daily_study_hours': avg_daily_study_hours,
            'social_media_hours_per_day': social_media_hours_per_day,
            'sleep_hours_avg': sleep_hours_avg,
            'backlog_count': backlog_count,
            'daily_text_log': daily_text_log
        }
        
        # Assess risk
        risk_prob, risk_prediction, features, nlp_stress_score = assess_risk(
            student_data, nlp_model, tfidf, xgb_model, metadata
        )
        
        # Generate counseling report
        report = generate_counseling_report(risk_prob, features, nlp_stress_score, student_data)
        
        # Display results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f'<div class="metric-box"><h3>Risk Level</h3><h2>{report["risk_level"]}</h2></div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<div class="metric-box"><h3>Risk Score</h3><h2>{report["risk_percentage"]:.1f}%</h2></div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'<div class="metric-box"><h3>Stress Level</h3><h2>{report["nlp_stress_score"]:.1f}%</h2></div>', unsafe_allow_html=True)
        
        # Risk visualization
        st.subheader("📈 Risk Assessment Visualization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=report["risk_percentage"],
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Risk Score"},
                delta={'reference': 50},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#ff6b6b" if report["risk_percentage"] >= 50 else "#feca57" if report["risk_percentage"] >= 30 else "#48cae4"},
                    'steps': [
                        {'range': [0, 30], 'color': "#e0f7fa"},
                        {'range': [30, 50], 'color': "#fff3e0"},
                        {'range': [50, 100], 'color': "#ffebee"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 50
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Feature importance radar chart
            feature_values = [
                features['academic_index'],
                (10 - features['sleep_deviation']) * 10,  # Invert so higher is better
                features['focus_ratio'] * 100,
                features['attendance_pct'],
                (10 - features['social_media_hours_per_day']) * 10,  # Invert
                (1 - nlp_stress_score) * 100  # Invert stress
            ]
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=feature_values,
                theta=['Academic Index', 'Sleep Quality', 'Focus Ratio', 'Attendance', 
                       'Social Media Control', 'Mental Health'],
                fill='toself',
                name='Your Profile'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                showlegend=False,
                height=300,
                title="Performance Profile"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Key Issues Section
        if report['key_issues']:
            st.subheader("🚨 Key Issues Identified")
            
            for issue in report['key_issues']:
                severity_color = "#ff6b6b" if issue['severity'] == 'HIGH' else "#feca57"
                st.markdown(f"""
                    <div style="background: {severity_color}22; padding: 1rem; margin: 0.5rem 0; 
                    border-radius: 8px; border-left: 4px solid {severity_color};">
                    <h4 style="color: {severity_color}; margin: 0;">{issue['issue']} - {issue['severity']} PRIORITY</h4>
                    <p style="margin: 0.5rem 0 0 0;">{issue['details']}</p>
                    </div>
                """, unsafe_allow_html=True)
        
        # Recommendations Section
        st.subheader("💡 Personalized Recommendations")
        
        for i, rec in enumerate(report['recommendations'], 1):
            st.markdown(f"""
                <div class="action-item">
                <strong>{i}. {rec}</strong>
                </div>
            """, unsafe_allow_html=True)
        
        # 4-Week Action Plan
        st.subheader("📅 Your 4-Week Action Plan")
        
        for week, details in report['action_plan'].items():
            with st.expander(f"**{week}: {details['theme']}**"):
                for task in details['tasks']:
                    st.checkbox(task, key=f"{week}_{task}")
        
        # Counterfactual Analysis
        st.subheader("🔮 What-If Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**If you improve sleep to 8 hours:**")
            improved_features = features.copy()
            improved_features['sleep_deviation'] = 0
            # Recalculate risk (simplified)
            improved_risk = risk_prob * 0.8  # Approximate improvement
            st.info(f"Risk would drop to: {improved_risk*100:.1f}%")
        
        with col2:
            st.write("**If you study +2 hours daily:**")
            improved_features = features.copy()
            improved_features['avg_daily_study_hours'] += 2
            improved_features['focus_ratio'] = improved_features['avg_daily_study_hours'] / (improved_features['social_media_hours_per_day'] + 1)
            improved_risk = risk_prob * 0.75  # Approximate improvement
            st.info(f"Risk would drop to: {improved_risk*100:.1f}%")
        
        # Download report
        st.subheader("📄 Download Your Report")
        
        report_text = f"""
STUDENT RISK ASSESSMENT REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

RISK LEVEL: {report['risk_level']}
RISK SCORE: {report['risk_percentage']:.1f}%
STRESS LEVEL: {report['nlp_stress_score']:.1f}%

KEY ISSUES:
"""
        for issue in report['key_issues']:
            report_text += f"- {issue['issue']} ({issue['severity']}): {issue['details']}\n"
        
        report_text += "\nRECOMMENDATIONS:\n"
        for i, rec in enumerate(report['recommendations'], 1):
            report_text += f"{i}. {rec}\n"
        
        st.download_button(
            label="Download Report as Text",
            data=report_text,
            file_name=f"student_risk_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()
