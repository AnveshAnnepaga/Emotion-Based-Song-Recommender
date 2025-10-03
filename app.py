import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import getpass 

from auth_service import create_user, sign_in_user 
from emotion_analyzer import analyze_emotion
from song_recommender import get_song_recommender
from user_logger import log_user_interaction, get_user_history 

st.set_page_config(page_title="Mood AI Recommender", layout="wide", initial_sidebar_state="collapsed")

# Load environment variables and Supabase client
load_dotenv()
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# --- CUSTOM CSS INJECTION FOR MINIMALIST DARK MODE ---
st.markdown("""
<style>
/* 1. GLOBAL BACKGROUND AND THEME */
.stApp {
    background-color: #0d1117; 
    color: #E6EDF3; 
}
/* Title Styling */
h1 {
    text-align: center;
    font-size: 3em !important;
    font-weight: 700 !important;
    color: #FFFFFF;
    margin-top: 40px;
    margin-bottom: 5px;
}
/* Subtitle/Slogan Styling */
h3 {
    text-align: center;
    color: #8B949E; 
    margin-bottom: 40px;
}
/* 2. CUSTOM BUTTONS (Vibrant Teal Accent) */
.stButton button {
    background-color: #00FF7F; /* Bright Mint Green/Teal */
    color: #0d1117 !important; /* Dark text for contrast */
    border: none;
    border-radius: 8px;
    padding: 10px 30px;
    font-weight: bold;
    font-size: 1.1em;
    transition: background-color 0.3s;
}
.stButton button:hover {
    background-color: #00e673;
}

/* 3. INPUT FIELDS AND FORM CONTAINER (Removed box styling for clean look) */
.main-form-card {
    background-color: transparent; 
    border: none; 
    box-shadow: none; 
    padding: 30px 0; 
    margin-top: 20px;
}
/* Labels (Subtle Green) */
div[data-testid="stWidgetLabel"] label {
    color: #38b2ac !important; /* Teal for labels */
    font-weight: 600;
}
/* Info and Success Messages for Dark Theme */
div[data-testid="stInfo"], div[data-testid="stSuccess"] {
    background-color: #1a2d2a;
    color: #38b2ac;
    border-left: 5px solid #38b2ac;
}
</style>
""", unsafe_allow_html=True)


# --- STATE MANAGEMENT ---
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'user_id' not in st.session_state: st.session_state['user_id'] = None
if 'user_name' not in st.session_state: st.session_state['user_name'] = None 
if 'page' not in st.session_state: st.session_state['page'] = 'home' 
if 'last_input' not in st.session_state: st.session_state['last_input'] = ""
if 'is_analyzing' not in st.session_state: st.session_state['is_analyzing'] = False


# --- AUTHENTICATION FORMS ---

def show_login_page():
    # Dedicated login page content
    st.markdown("<h1 style='text-align: center;'>User Login</h1>", unsafe_allow_html=True)
    st.markdown("### Please enter your credentials to access your history.", unsafe_allow_html=True)
    st.markdown("---")

    form_cols = st.columns([0.3, 0.4, 0.3])
    with form_cols[1]:
        with st.form(key="login_form"):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            submit_button = st.form_submit_button("Log In", type="primary", use_container_width=True)

            if submit_button:
                with st.spinner("Verifying credentials..."):
                    user_id, user_name = sign_in_user(email, password)
                    if user_id:
                        st.session_state['logged_in'] = True
                        st.session_state['user_id'] = user_id
                        st.session_state['user_name'] = user_name 
                        st.toast("Login Successful! Welcome Back!", icon="🎉")
                        st.session_state['page'] = 'home' # Redirect to home
                        st.rerun()
                    else:
                        st.error("Login failed. Check credentials.")
        
        if st.button("← Back to Home", key="back_login"):
            st.session_state['page'] = 'home'
            st.rerun()


def show_signup_page():
    # Dedicated signup page content
    st.markdown("<h1 style='text-align: center;'>New User Sign Up</h1>", unsafe_allow_html=True)
    st.markdown("### Create your account to save your personalized music history.", unsafe_allow_html=True)
    st.markdown("---")

    form_cols = st.columns([0.3, 0.4, 0.3])
    with form_cols[1]:
        with st.form(key="signup_form"):
            # User Details
            col1, col2 = st.columns(2)
            name = col1.text_input("Full Name", key="signup_name")
            age = col2.number_input("Age", min_value=10, max_value=120, key="signup_age", value=25)
            
            email = st.text_input("Email", key="signup_email")
            
            # Password Fields with Validation
            password = st.text_input("Password (Min 8 Chars)", type="password", key="signup_password")
            retype_password = st.text_input("Retype Password", type="password", key="signup_retype_password")
            
            submit_button = st.form_submit_button("Sign Up & Create Account", type="primary", use_container_width=True)

            if submit_button:
                if not name or not email or not password:
                    st.error("Please fill all required fields.")
                elif password != retype_password:
                    st.error("Passwords do not match. Please retype.")
                elif len(password) < 8:
                    st.error("Password must be at least 8 characters long.")
                else:
                    with st.spinner("Creating secure account..."):
                        user_id, user_name = create_user(name, age, email, password)
                        if user_id:
                            st.success("Account created successfully! Please log in on the next page.")
                            st.session_state['page'] = 'login' # Redirect to login
                            st.rerun()
                        else:
                             st.error("Account creation failed. User with this email might already exist.")

        if st.button("← Back to Home", key="back_signup"):
            st.session_state['page'] = 'home'
            st.rerun()


# --- HEADER AND NAVIGATION ---

def setup_header(logged_in):
    # This renders the header and navigation controls at the top of every page.
    header_cols = st.columns([0.2, 0.6, 0.2]) 

    with header_cols[0]:
        # LEFT SIDE: Logo
        st.markdown('<div class="app-header-container"><span class="header-logo-text">🎧 MoodWave AI</span></div>', unsafe_allow_html=True)
    
    with header_cols[1]:
        # CENTER: Spacer
        st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
    
    with header_cols[2]:
        # RIGHT SIDE: AUTH BUTTONS 
        if not logged_in:
            button_cols_r = st.columns(2)
            with button_cols_r[0]:
                if st.button("Log In", key="nav_login", type="primary", use_container_width=True): 
                    st.session_state['page'] = 'login'
                    st.rerun()
            with button_cols_r[1]:
                if st.button("Sign Up", key="nav_signup", type="secondary", use_container_width=True):
                    st.session_state['page'] = 'signup'
                    st.rerun()
        else:
            # Display Logout Button
            if st.button("Log Out", key="top_logout", use_container_width=True, type="secondary"):
                st.session_state['logged_in'] = False
                st.session_state['user_id'] = None
                st.session_state['user_name'] = None
                st.session_state['page'] = 'home'
                st.rerun()


def show_welcome_page():
    # This is the landing page content for unauthenticated users.
    
    # --- CENTRAL LAYOUT ---
    st.markdown("<h1 style='text-align: center;'>Emotion-Based Song Recommender</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #8B949E;'>Analyze Your Mood and Get the Perfect Soundtrack for Your Day.</h3>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True) 
    
    # --- FEATURE BLOCK TO FILL SPACE ---
    st.markdown("""
        <div style='text-align: center; background-color: #161B22; padding: 25px; border-radius: 12px; margin-bottom: 25px; border: 1px solid #30363D;'>
            <h4 style='color: #00FF7F; margin-top: 0;'>— Your Emotional AI Companion —</h4>
            <p style='color: white; font-size: 1.2em;'>
                Describe a moment, and our deep learning model instantly analyzes your mood to curates the perfect sonic experience.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("Analyze Your Mood")
    st.success("Try the tool instantly below, or log in to save your history!")
    
    # Dynamic Content Rendering (Input/Results)
    show_input_and_results(False)


def show_main_app():
    # This is the dedicated view for LOGGED-IN users only.
    st.header(f"Welcome back, {st.session_state['user_name']}!")
    st.markdown("---")
    
    # 1. USER HISTORY DISPLAY
    with st.expander("⏮️ View Your Last Recommendations", expanded=False):
        user_history = get_user_history(st.session_state['user_id'])
        
        if user_history:
            st.dataframe(user_history, use_container_width=True, 
                         column_config={
                             "Link": st.column_config.LinkColumn("Link", display_text="Listen"),
                             "Input Snippet": "Your Input",
                             "Mood": st.column_config.Column("Mood", width="small")
                         })
        else:
            st.info("You haven't requested any songs yet! Start the conversation below.")
            
    st.markdown("---")
    st.subheader("Analyze Your Mood")
    st.success("Tell me about your mood, situation, or what's on your mind.")
    
    # RENDER THE CORE APPLICATION INPUT/OUTPUT
    show_input_and_results(True)


def show_input_and_results(is_logged_in):
    # Renders the core functionality (Input Box and Recommendation Logic)
    
    # Use columns to place the text area and the button on the same line
    input_col, button_col = st.columns([0.8, 0.2]) # 80% width for text, 20% for button
    
    with input_col:
        user_input = st.text_area("Describe Your Current Situation:", height=100, key="mood_input", 
                                  placeholder="e.g., 'I feel completely overwhelmed by work and need to relax.'",
                                  value=st.session_state['last_input'])
    
    with button_col:
        # Spacer is needed to vertically align the button to the bottom of the tall text area
        st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True) 
        
        # The button is now placed directly beside the text area
        if st.button("Analyze & Get Song", type="primary", use_container_width=True, key="analyze_button_main"):
            if user_input:
                st.session_state['last_input'] = user_input
                st.session_state['is_analyzing'] = True
                st.rerun()
            else:
                st.warning("Please enter some text for mood analysis.")
                
    # Display Results after a Rerun (This section remains unchanged)
    if st.session_state.get('is_analyzing'):
        st.session_state['is_analyzing'] = False 
        
        with st.spinner("Analyzing emotional tone..."):
            detected_mood = analyze_emotion(st.session_state['last_input'])
            st.session_state['last_mood'] = detected_mood
            
            st.markdown("---")
            st.subheader("✅ Analysis Result")
            st.success(f"The detected emotional tone is: **{detected_mood.upper()}**.")

            song = get_song_recommender(detected_mood)

            if song:
                st.info("✨ Your Song Recommendation:")
                container_song = st.container(border=True)
                container_song.markdown(
                    f"<h3 style='color: #00FF7F; margin-top: 0;'>{song['song_title']}</h3>" 
                    f"<p style='color: #BB86FC;'>**Artist:** {song['artists']}</p>"       
                    , unsafe_allow_html=True
                )
                container_song.link_button("▶️ Listen Now", url=song['link'], use_container_width=True) 
                
                # Log the interaction only if logged in
                if is_logged_in:
                    try:
                        log_user_interaction(st.session_state['user_id'], st.session_state['last_input'], detected_mood, song['id'])
                        st.caption("Interaction logged successfully and saved to history.")
                    except Exception as e:
                        st.caption(f"Error logging interaction: {e}")
                else:
                    st.caption("Log in to save this recommendation to your history!")
            else:
                st.warning(f"No songs found for mood: {detected_mood.upper()}. Please add more songs to your database.")
# --- MAIN ENTRY POINT ---

def main_page():
    # Call the header first, as it contains the crucial navigation logic
    setup_header(st.session_state['logged_in']) 
    
    # Router based on state
    if st.session_state['page'] == 'login':
        show_login_page()
    elif st.session_state['page'] == 'signup':
        show_signup_page()
    elif st.session_state['page'] == 'home' and st.session_state['logged_in']:
        show_main_app()
    elif st.session_state['page'] == 'home' and not st.session_state['logged_in']:
        show_welcome_page() # Initial, unauthenticated view

if __name__ == '__main__':
    main_page()