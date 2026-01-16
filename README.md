# 🎓 Student 360° Risk Assessment & Counseling App

A premium, AI-powered Streamlit application for comprehensive student risk assessment and personalized counseling with detailed 4-week action plans.

## Features

### 🧠 Advanced AI Analysis
- **Multi-modal Risk Assessment**: Combines academic, behavioral, and psychological data
- **NLP Stress Detection**: Analyzes student journal entries for stress indicators
- **XGBoost Machine Learning**: State-of-the-art risk prediction model
- **SHAP Explainability**: Transparent AI decision-making

### 📊 Comprehensive Counseling
- **360° Student Profile**: Academic performance, study habits, health metrics
- **Personalized Recommendations**: Tailored advice based on individual risk factors
- **4-Week Action Plan**: Detailed weekly milestones and tasks
- **What-If Analysis**: Counterfactual scenarios showing improvement potential

### 🎨 Premium UI/UX
- **Interactive Dashboard**: Real-time risk visualization with Plotly
- **Professional Design**: Custom CSS with modern color schemes
- **Responsive Layout**: Optimized for all screen sizes
- **Downloadable Reports**: Generate and save detailed counseling reports

## File Structure

```
├── streamlit_app.py          # Main Streamlit application
├── model_training.py         # Model training script for Colab
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── nlp_model.pkl            # Trained NLP model (generated)
├── tfidf_vectorizer.pkl     # Text vectorizer (generated)
├── xgboost_model.pkl        # Risk prediction model (generated)
├── model_metadata.pkl       # Model configuration (generated)
└── X_test.csv              # Test data for SHAP (generated)
```

## Quick Start Guide

### Step 1: Train Models in Google Colab

1. **Upload your data** to Google Colab:
   - Upload your CSV file (e.g., `student_features_with_labels_v2 (1).csv`)

2. **Run the training script**:
   ```python
   # Upload model_training.py to Colab and run:
   exec(open('model_training.py').read())
   ```

3. **Download generated files**:
   - `nlp_model.pkl`
   - `tfidf_vectorizer.pkl`
   - `xgboost_model.pkl`
   - `model_metadata.pkl`
   - `X_test.csv`

### Step 2: Setup GitHub Repository

1. **Create a new GitHub repository**
2. **Upload all files** to the repository:
   - `streamlit_app.py`
   - `requirements.txt`
   - All `.pkl` model files
   - `X_test.csv`

3. **Repository structure should look like**:
   ```
   your-repo-name/
   ├── streamlit_app.py
   ├── requirements.txt
   ├── nlp_model.pkl
   ├── tfidf_vectorizer.pkl
   ├── xgboost_model.pkl
   ├── model_metadata.pkl
   └── X_test.csv
   ```

### Step 3: Deploy on Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Connect your GitHub account**
3. **Click "New app"**
4. **Configure deployment**:
   - Repository: Select your GitHub repo
   - Branch: main (or master)
   - Main file path: `streamlit_app.py`
   - URL: Choose a custom subdomain (optional)

5. **Click "Deploy"** and wait for the build to complete

### Step 4: Use the Application

1. **Access your deployed app** via the Streamlit URL
2. **Input student data** using the sidebar sliders and forms
3. **Click "Analyze Risk"** to generate comprehensive assessment
4. **Review the 360° analysis** including:
   - Risk level and score
   - Key issues identified
   - Personalized recommendations
   - 4-week action plan
   - What-if scenarios

## Detailed Features

### Input Parameters

**Academic Performance:**
- Previous Semester GPA (0-10)
- Last Test Score (0-100)
- Attendance Percentage (0-100%)
- Number of Backlogs (0-10)

**Study Habits:**
- Average Daily Study Hours (0-12)
- Social Media Hours Per Day (0-12)

**Health & Lifestyle:**
- Average Sleep Hours (0-12)

**Psychological Assessment:**
- Daily journal entry (text analysis for stress)

### Risk Assessment Output

**Risk Metrics:**
- Risk Level: LOW/MEDIUM/HIGH
- Risk Score: 0-100%
- Stress Level: 0-100% (NLP analysis)

**Visualizations:**
- Risk gauge meter
- Performance radar chart
- Feature importance plots

**Counseling Components:**
- Key issues with severity levels
- Personalized recommendations
- 4-week structured action plan
- Counterfactual analysis
- Downloadable reports

### 4-Week Action Plan Structure

**Week 1: Assessment & Immediate Actions**
- Self-assessment completion
- Academic advisor meeting
- Study schedule setup
- Sleep hygiene routine
- Focus app installation

**Week 2: Building Foundations**
- Study group joining
- Backlog clearance start
- Attendance improvement
- Pomodoro technique practice
- Social media reduction

**Week 3: Consistency & Improvement**
- Professor consultations
- Continued backlog clearance
- High attendance maintenance
- Practice testing
- Sleep consistency

**Week 4: Evaluation & Future Planning**
- Progress evaluation
- Final backlog completion
- Mock examination
- Next month planning
- Achievement celebration

## Technical Implementation

### Machine Learning Pipeline

1. **NLP Stress Detection**:
   - TF-IDF vectorization (5000 features)
   - Logistic Regression with balanced class weights
   - Stress score: 0-1 probability

2. **Feature Engineering**:
   - Academic Index: (GPA×10 + Test Score)/2
   - Sleep Deviation: |Actual Sleep - 8 hours|
   - Focus Ratio: Study Hours/(Social Media + 1)
   - Risk Alarm: Backlog + Low Attendance flag

3. **Risk Prediction**:
   - XGBoost Classifier (200 estimators, max_depth=4)
   - Calibrated probabilities (isotonic regression)
   - Optimized threshold: 0.2778 (85% recall)

### Model Performance

- **Target Recall**: 85% (catch at-risk students)
- **Precision**: Optimized for safety
- **Stability**: 5-fold cross-validation
- **Explainability**: SHAP feature importance

## Customization Options

### Styling Modifications

Edit the CSS in `streamlit_app.py` to customize:
- Color schemes
- Layout spacing
- Typography
- Component styling

### Model Updates

To retrain with new data:
1. Update the CSV file path in `model_training.py`
2. Run training in Colab
3. Download and replace `.pkl` files in GitHub
4. Streamlit will auto-deploy changes

### Feature Additions

Add new input fields by:
1. Modifying the sidebar form in `streamlit_app.py`
2. Updating feature engineering in both training and app scripts
3. Retraining models with new features

## Troubleshooting

### Common Issues

**1. Model Loading Errors**
- Ensure all `.pkl` files are in the GitHub repository
- Check file names match exactly
- Verify model compatibility with current scikit-learn version

**2. Streamlit Deployment Issues**
- Check `requirements.txt` for correct package versions
- Ensure `streamlit_app.py` is in repository root
- Verify GitHub connection permissions

**3. Performance Issues**
- Reduce number of features if app is slow
- Cache expensive computations with `@st.cache_resource`
- Optimize Plotly chart rendering

### Support Resources

- Streamlit Documentation: [docs.streamlit.io](https://docs.streamlit.io)
- GitHub Help: [help.github.com](https://help.github.com)
- Google Colab: [colab.research.google.com](https://colab.research.google.com)

## License

This project is created for educational and counseling purposes. Please ensure compliance with your institution's data privacy policies when deploying.

## Acknowledgments

- Built with Streamlit, scikit-learn, XGBoost, and Plotly
- UI design inspired by modern educational platforms
- Counseling framework based on academic success research

---

**Deploy your premium counseling app today and help students succeed! 🚀**
