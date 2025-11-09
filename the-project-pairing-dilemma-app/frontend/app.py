import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import base64
import os

# Page config
st.set_page_config(
    page_title="Project Pairing Dilemma",
    page_icon="🎯",
    layout="wide"
)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'form'
if 'prediction_made' not in st.session_state:
    st.session_state.prediction_made = False

# Load and encode background image
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Get the background image
bg_image_path = os.path.join(os.path.dirname(__file__), "gradient.png")
bg_image_base64 = get_base64_image(bg_image_path)

# Custom CSS with background image
st.markdown(f"""
    <style>
    /* Main app background with image */
    .stApp {{
        background-image: url('data:image/png;base64,{bg_image_base64}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    .main {{
        padding: 2rem;
    }}
    
    /* Glass effect for main content */
    .block-container {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }}
    
    /* Title styling */
    h1 {{
        color: #ffffff !important;
        text-align: center;
        margin-bottom: 0.5rem;
        font-size: 3rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }}
    
    h2, h3 {{
        color: #ffffff !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    }}
    
    /* Labels and text */
    label {{
        color: #ffffff !important;
        font-weight: 600;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
    }}
    
    p, li, span {{
        color: #ffffff !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    }}
    
    .subtitle {{
        text-align: center;
        color: #ffffff !important;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
    }}
    
    /* Button styling */
    .stButton>button {{
        width: 100%;
        background: rgba(0, 115, 230, 0.8);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        color: white;
        padding: 0.75rem;
        font-size: 1.1rem;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin-top: 1rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(0, 115, 230, 0.3);
        transition: all 0.3s ease;
    }}
    
    .stButton>button:hover {{
        background: rgba(0, 91, 181, 0.9);
        color: #ffeb3b;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 115, 230, 0.5);
    }}
    
    /* Input fields with glass effect */
    .stTextInput input, .stNumberInput input {{
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px;
        color: #000000 !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }}
    
    .stTextInput input:hover, .stNumberInput input:hover {{
        border-color: rgba(0, 115, 230, 0.6) !important;
        box-shadow: 0 6px 20px rgba(0, 115, 230, 0.2);
        transform: translateY(-2px);
    }}
    
    /* Selectbox styling */
    .stSelectbox > div > div {{
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px;
        color: #000000 !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }}
    
    .stSelectbox:hover > div > div {{
        border-color: rgba(0, 115, 230, 0.6) !important;
        box-shadow: 0 6px 20px rgba(0, 115, 230, 0.2);
        transform: translateY(-2px);
    }}
    
    /* Selectbox dropdown */
    .stSelectbox svg {{
        fill: #000000 !important;
    }}
    
    [data-baseweb="popover"] {{
        background: rgba(255, 255, 255, 0.98) !important;
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 10px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }}
    
    [data-baseweb="menu"] {{
        background: rgba(255, 255, 255, 0.98) !important;
    }}
    
    [role="option"] {{
        color: #000000 !important;
        background: rgba(255, 255, 255, 0.95) !important;
        padding: 10px 15px !important;
    }}
    
    [role="option"]:hover {{
        background: rgba(0, 115, 230, 0.3) !important;
    }}
    
    /* Slider styling */
    .stSlider > div > div > div > div {{
        background-color: rgba(0, 115, 230, 0.8) !important;
    }}
    
    /* Form styling */
    .stForm {{
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        padding: 2rem;
        border-radius: 20px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }}
    
    /* Prediction card */
    .prediction-card {{
        padding: 2.5rem;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 2px solid rgba(255, 255, 255, 0.3);
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }}
    
    /* Metric card */
    .metric-card {{
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        border: 2px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }}
    
    /* Expander styling */
    .streamlit-expanderHeader {{
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px;
    }}
    
    .streamlit-expanderContent {{
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }}
    
    /* Metrics */
    [data-testid="stMetricValue"] {{
        color: #ffffff !important;
        font-size: 2rem !important;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }}
    
    [data-testid="stMetricLabel"] {{
        color: #ffffff !important;
        font-weight: 600;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    }}
    
    /* Dataframe */
    .stDataFrame {{
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

def show_form():
    # Header
    st.title("🎯 Project Pairing Dilemma")
    st.markdown('<p class="subtitle">Predict whether a student prefers Solo or Team projects</p>', unsafe_allow_html=True)

    # Info box
    with st.expander("ℹ️ About This Tool"):
        st.markdown("""
        **Faculty often struggle to form balanced project teams.** This tool helps predict student preferences based on:
        
        - 📊 **Introversion/Extraversion**: Social energy preference (1=Introvert, 5=Extravert)
        - 🎲 **Risk-Taking**: Willingness to take risks (1=Low, 5=High)
        - 🎯 **Primary Club/Activity**: Main extracurricular involvement
        - ⏰ **Weekly Hobby Hours**: Time spent on hobbies per week
        
        **Impact**: Helps faculty assign balanced teams and respect individual preferences.
        """)

    st.markdown("---")

    # Main form
    st.markdown("### 📝 Student Information")

    with st.form(key='prediction_form'):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Personality Traits**")
            introversion_extraversion = st.slider(
                "Introversion/Extraversion",
                min_value=1,
                max_value=5,
                value=3,
                help="1 = Introvert, 5 = Extravert"
            )
            
            risk_taking = st.slider(
                "Risk-Taking Level",
                min_value=1,
                max_value=5,
                value=3,
                help="1 = Low risk-taker, 5 = High risk-taker"
            )
        
        with col2:
            st.markdown("**Activities & Interests**")
            club_options = [
                "Coding Club",
                "Sports Club",
                "Music Club",
                "Cultural Club",
                "Drama Club",
                "Entrepreneurship Cell",
                "Literary Club",
                "Robotics Club"
            ]
            club_top1 = st.selectbox(
                "Primary Club/Activity",
                options=club_options,
                index=0,
                help="Select your primary club or activity"
            )
            
            weekly_hobby_hours = st.number_input(
                "Weekly Hobby Hours",
                min_value=0,
                max_value=100,
                value=10,
                help="Hours spent on hobbies per week"
            )
        
        submit_button = st.form_submit_button(label='🔮 Predict Preference')

    # Handle prediction
    if submit_button:
        with st.spinner('Analyzing student profile...'):
            payload = {
                "introversion_extraversion": introversion_extraversion,
                "risk_taking": risk_taking,
                "club_top1": club_top1,
                "weekly_hobby_hours": weekly_hobby_hours
            }
            
            try:
                response = requests.post("http://127.0.0.1:8000/predict", json=payload)
                response.raise_for_status()
                result = response.json()
                
                # Display result
                st.markdown("---")
                st.markdown("### 🎉 Prediction Result")
                
                prediction = result['prediction']
                prob_solo = result['prediction_probability']['Solo']
                prob_team = result['prediction_probability']['Team']
                
                # Result card
                if prediction == "Team":
                    st.markdown(f"""
                    <div class="prediction-card">
                        <h2>👥 Team Player</h2>
                        <p style="font-size: 1.2rem; margin-top: 1rem;">
                            This student is predicted to prefer <strong>Team Projects</strong>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="prediction-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                        <h2>🎯 Solo Worker</h2>
                        <p style="font-size: 1.2rem; margin-top: 1rem;">
                            This student is predicted to prefer <strong>Solo Projects</strong>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Probability gauge
                st.markdown("### 📊 Confidence Level")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Solo Preference", f"{prob_solo*100:.1f}%")
                with col2:
                    st.metric("Team Preference", f"{prob_team*100:.1f}%")
                
                # Gauge chart
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=prob_team * 100,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Team Preference Probability", 'font': {'size': 20}},
                    delta={'reference': 50, 'increasing': {'color': "#667eea"}},
                    gauge={
                        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                        'bar': {'color': "#667eea"},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'steps': [
                            {'range': [0, 50], 'color': '#ffeaa7'},
                            {'range': [50, 100], 'color': '#74b9ff'}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 50
                        }
                    }
                ))
                
                fig.update_layout(
                    height=300,
                    margin=dict(l=20, r=20, t=50, b=20),
                    paper_bgcolor="white",
                    font={'color': "#2c3e50", 'family': "Arial"}
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.success("✅ Prediction completed successfully!")
                
                # Mark that prediction has been made
                st.session_state.prediction_made = True
                
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Error connecting to the backend: {e}")
                st.info("Make sure the backend server is running on http://127.0.0.1:8000")

    # Navigation buttons - only show if prediction has been made
    if st.session_state.prediction_made:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📊 View Dashboard", use_container_width=True):
                st.session_state.page = 'dashboard'
                st.rerun()

    # Footer
    st.markdown("""
    <div style="text-align: center; color: #7f8c8d; padding: 1rem;">
        <p>Built with ❤️ for better team formation | Powered by Debanshu </p>
    </div>
    """, unsafe_allow_html=True)

def show_dashboard():
    st.title("📊 Project Preference Dashboard")
    
    # Back button
    if st.button("← Back to Prediction Form"):
        st.session_state.page = 'form'
        st.rerun()
    
    st.markdown("---")
    
    try:
        # Fetch data from the backend
        response = requests.get("http://127.0.0.1:8000/data-summary")
        response.raise_for_status()
        data = response.json()
        
        # Key Metrics
        st.markdown("### 📈 Key Metrics")
        col1, col2, col3 = st.columns(3)
        
        pref_dist = data['preference_distribution']
        total = sum(pref_dist.values())
        team_count = pref_dist.get('Team', 0)
        solo_count = pref_dist.get('Solo', 0)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #667eea;">👥 Team Preference</h3>
                <h1 style="color: #2c3e50;">{team_count}</h1>
                <p style="color: #7f8c8d;">{(team_count/total*100):.1f}% of students</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #f5576c;">🎯 Solo Preference</h3>
                <h1 style="color: #2c3e50;">{solo_count}</h1>
                <p style="color: #7f8c8d;">{(solo_count/total*100):.1f}% of students</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #4CAF50;">📊 Total Students</h3>
                <h1 style="color: #2c3e50;">{total}</h1>
                <p style="color: #7f8c8d;">Model Accuracy: {data['accuracy']*100:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Preference Distribution")
            pref_df = pd.DataFrame(list(pref_dist.items()), columns=['Preference', 'Count'])
            fig = px.pie(pref_df, values='Count', names='Preference', 
                        color='Preference',
                        color_discrete_map={'Team': '#667eea', 'Solo': '#f5576c'},
                        hole=0.4)
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Introversion/Extraversion Distribution")
            intro_data = data['introversion_distribution']
            intro_df = pd.DataFrame(list(intro_data.items()), columns=['Score', 'Count'])
            intro_df['Score'] = intro_df['Score'].astype(str)
            fig = px.bar(intro_df, x='Score', y='Count', 
                        color='Count',
                        color_continuous_scale='Blues')
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎲 Risk-Taking Distribution")
            risk_data = data['risk_taking_distribution']
            risk_df = pd.DataFrame(list(risk_data.items()), columns=['Score', 'Count'])
            risk_df['Score'] = risk_df['Score'].astype(str)
            fig = px.bar(risk_df, x='Score', y='Count',
                        color='Count',
                        color_continuous_scale='Reds')
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 Confusion Matrix")
            cm = data['confusion_matrix']
            cm_df = pd.DataFrame(cm, 
                               columns=['Predicted Solo', 'Predicted Team'],
                               index=['Actual Solo', 'Actual Team'])
            fig = px.imshow(cm_df, 
                          text_auto=True,
                          color_continuous_scale='Purples',
                          aspect='auto')
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 📋 Recent Submissions")
        recent_df = pd.DataFrame(data['recent_submissions'])
        if not recent_df.empty:
            # Show only relevant columns
            display_cols = ['introversion_extraversion', 'risk_taking', 'club_top1', 'weekly_hobby_hours', 'teamwork_preference']
            display_cols = [col for col in display_cols if col in recent_df.columns]
            st.dataframe(recent_df[display_cols].tail(10), use_container_width=True)
        else:
            st.info("No submissions yet")
            
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error connecting to the backend: {e}")
        st.info("Make sure the backend server is running on http://127.0.0.1:8000")
    except Exception as e:
        st.error(f"❌ Error loading dashboard: {e}")

# Page router
if st.session_state.page == 'form':
    show_form()
elif st.session_state.page == 'dashboard':
    show_dashboard()