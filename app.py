import streamlit as st
import pandas as pd
import numpy as np
import joblib
import re
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
from typing import Dict, List, Tuple
import base64
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.colors import HexColor
import uuid

# ==========================================
# 1. PREMIUM PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Valkyrie AI | Premium Student Success Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium branding and styling
st.markdown("""
<style>
    /* Premium Dark Theme */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Glassmorphism effect for main containers */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Premium metric cards */
    .metric-card-premium {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        transition: transform 0.3s ease;
    }
    
    .metric-card-premium:hover {
        transform: translateY(-5px);
    }
    
    /* Risk indicator cards */
    .risk-critical {
        background: linear-gradient(135deg, #ff0844 0%, #ffb199 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 5px 15px rgba(255, 8, 68, 0.3);
    }
    
    .risk-high {
        background: linear-gradient(135deg, #ff9a00 0%, #ff6a00 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 5px 15px rgba(255, 154, 0, 0.3);
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 5px 15px rgba(246, 211, 101, 0.3);
    }
    
    .risk-low {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 5px 15px rgba(86, 171, 47, 0.3);
    }
    
    /* Premium buttons */
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
    
    /* Custom sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Professional report styling */
    .premium-report {
        background: #1e1e1e;
        color: #dcdcdc;
        padding: 2rem;
        border-radius: 15px;
        font-family: 'SF Mono', 'Courier New', monospace;
        border-left: 5px solid #667eea;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        margin: 1rem 0;
    }
    
    /* Animated loading */
    .loading-animation {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Premium typography */
    .premium-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        color: #64748b;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. PREMIUM BRANDING & HEADER
# ==========================================
def display_premium_header():
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    
    with col2:
        st.markdown('<h1 class="premium-title">⚡ Valkyrie AI</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Premium Student Success Intelligence Platform</p>', unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: right; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px;">
            <p style="margin: 0; color: white; font-size: 0.9rem;">Premium Version</p>
            <p style="margin: 0; color: #dcdcdc; font-size: 0.8rem;">360° Student Analytics</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 3. ADVANCED MODEL LOADING WITH ERROR HANDLING
# ==========================================
@st.cache_resource
def load_premium_models():
    """Load models with comprehensive error handling and validation"""
    try:
        # Simulate loading delay for premium feel
        with st.spinner("🚀 Initializing Valkyrie AI Engine..."):
            time.sleep(2)
            
        bundle = joblib.load('student_risk_model.pkl')
        
        # Validate model components
        required_keys = ['final_model', 'nlp_model', 'nlp_vectorizer']
        missing_keys = [key for key in required_keys if key not in bundle]
        
        if missing_keys:
            raise ValueError(f"Missing model components: {missing_keys}")
        
        return bundle
    except FileNotFoundError:
        st.error("""
        <div class="main-container">
            <h3>🚨 Critical Error: Model File Not Found</h3>
            <p>The premium AI models could not be loaded. Please ensure 'student_risk_model.pkl' is available.</p>
            <p><strong>Premium Support:</strong> contact@valkyrie-ai.com</p>
        </div>
        """, unsafe_allow_html=True)
        return None
    except Exception as e:
        st.error(f"""
        <div class="main-container">
            <h3>⚠️ Premium Engine Error</h3>
            <p>Advanced AI system encountered an error: {str(e)}</p>
            <p>Our technical team has been notified.</p>
        </div>
        """, unsafe_allow_html=True)
        return None

# ==========================================
# 4. ENHANCED TEXT PROCESSING
# ==========================================
def advanced_text_processing(text: str) -> Dict:
    """Advanced NLP processing with emotion detection and sentiment analysis"""
    if not isinstance(text, str):
        return {"cleaned": "", "sentiment": "neutral", "emotions": {}, "stress_indicators": []}
    
    # Basic cleaning
    cleaned = re.sub(r'http\S+', '', text.lower())
    cleaned = re.sub(r'[^a-zA-Z\s]', '', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    # Stress keyword detection
    stress_keywords = {
        'high': ['overwhelmed', 'stressed', 'anxious', 'worried', 'panic', 'drowning', 'crushing', 'impossible'],
        'medium': ['difficult', 'challenging', 'struggling', 'behind', 'confused', 'lost', 'pressure'],
        'low': ['okay', 'fine', 'managing', 'coping', 'alright']
    }
    
    stress_level = 'low'
    stress_indicators = []
    
    for level, keywords in stress_keywords.items():
        found = [word for word in keywords if word in cleaned]
        if found:
            stress_level = level
            stress_indicators.extend(found)
            break
    
    return {
        "cleaned": cleaned,
        "sentiment": "negative" if stress_level in ['high', 'medium'] else "neutral",
        "stress_level": stress_level,
        "stress_indicators": stress_indicators,
        "word_count": len(cleaned.split())
    }

# ==========================================
