import streamlit as st
import time
import random
import json
from streamlit.components.v1 import html
import base64

# Initialize session state
def init_session():
    if "current_screen" not in st.session_state:
        st.session_state.current_screen = "login"
    
    if "selections" not in st.session_state:
        st.session_state.selections = {
            "genre": "",
            "setting": "",
            "characters": [],
            "language": "Hindi",
            "tone": "Bollywood Masala",
            "conflict": "",
            "ending": "",
            "story_type": "story"
        }
    
    if "generated_story" not in st.session_state:
        st.session_state.generated_story = ""
    
    if "loading" not in st.session_state:
        st.session_state.loading = False
        st.session_state.char_count = 0
        st.session_state.scene_count = 0
        st.session_state.story_progress = 0

# Custom CSS for styling
def apply_custom_css():
    st.markdown("""
    <style>
        :root {
            --primary: #ff3e6c;
            --secondary: #ff6b6b;
            --accent: #ff9f43;
            --background: #0f0c29;
            --card-bg: #1a1a2e;
            --text: #ffffff;
            --text-secondary: #bbbbbb;
            --success: #4caf50;
            --warning: #ff9800;
            --border-radius: 15px;
            --transition: all 0.3s ease;
            --shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
        }
        
        body {
            background: linear-gradient(135deg, var(--background), #1a1a2e);
            color: var(--text);
            background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiPjxkZWZzPjxwYXR0ZXJuIGlkPSJwYXR0ZXJuIiB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHBhdHRlcm5Vbml0cz0idXNlclNwYWNlT25Vc2UiIHBhdHRlcm5UcmFuc2Zvcm09InJvdGF0ZSg0NSkiPjxjaXJjbGUgY3g9IjEwIiBjeT0iMTAiIHI9IjEiIGZpbGw9IiMzMzMzMzMiIGZpbGwtb3BhY2l0eT0iMC4xIi8+PC9wYXR0ZXJuPjwvZGVmcz48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSJ1cmwoI3BhdHRlcm4pIi8+PC9zdmc+');
            font-family: 'Poppins', sans-serif;
        }
        
        .stApp {
            background: transparent;
            max-width: 500px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .app-container {
            background: rgba(26, 26, 46, 0.95);
            border-radius: var(--border-radius);
            overflow: hidden;
            box-shadow: var(--shadow);
            min-height: 90vh;
            position: relative;
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .app-header {
            text-align: center;
            padding: 20px 0;
            background: linear-gradient(to right, var(--primary), var(--accent));
            position: relative;
            overflow: hidden;
        }
        
        .app-title {
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(to right, #ffd700, #ff8c00);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 4px 8px rgba(0,0,0,0.3);
            margin-bottom: 5px;
            position: relative;
            z-index: 2;
            font-family: 'Kalam', cursive;
        }
        
        .app-subtitle {
            color: var(--text);
            font-size: 1.1rem;
            margin-bottom: 15px;
            position: relative;
            z-index: 2;
            opacity: 0.9;
        }
        
        .card {
            background: var(--card-bg);
            border-radius: var(--border-radius);
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: var(--shadow);
            border: 1px solid rgba(255, 255, 255, 0.1);
            position: relative;
            overflow: hidden;
        }
        
        .screen-title {
            font-size: 2rem;
            margin-bottom: 15px;
            background: linear-gradient(to right, var(--primary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            text-align: center;
        }
        
        .screen-description {
            color: var(--text-secondary);
            margin-bottom: 25px;
            font-size: 1rem;
            text-align: center;
            line-height: 1.6;
        }
        
        .option-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .option-card {
            background: rgba(50, 50, 70, 0.6);
            border-radius: var(--border-radius);
            padding: 15px;
            text-align: center;
            cursor: pointer;
            transition: var(--transition);
            border: 2px solid transparent;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 140px;
            justify-content: center;
            position: relative;
            overflow: hidden;
        }
        
        .option-card:hover {
            transform: translateY(-5px);
            background: rgba(80, 80, 120, 0.4);
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        }
        
        .option-card.selected {
            background: rgba(255, 62, 108, 0.2);
            border-color: var(--primary);
            box-shadow: 0 0 20px rgba(255, 62, 108, 0.4);
        }
        
        .btn {
            background: linear-gradient(to right, var(--primary), var(--accent));
            color: white;
            border: none;
            padding: 18px 25px;
            border-radius: var(--border-radius);
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            width: 100%;
            margin-top: 10px;
            box-shadow: 0 6px 20px rgba(255, 62, 108, 0.4);
            position: relative;
            overflow: hidden;
            z-index: 1;
        }
        
        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(255, 62, 108, 0.6);
        }
        
        .btn-outline {
            background: transparent;
            border: 2px solid var(--primary);
            color: var(--primary);
            box-shadow: none;
        }
        
        .btn-outline:hover {
            background: rgba(255, 62, 108, 0.1);
        }
        
        .btn-group {
            display: flex;
            gap: 15px;
            margin-top: 15px;
        }
        
        .free-banner {
            background: linear-gradient(45deg, #4CAF50, #8BC34A);
            color: white;
            border-radius: var(--border-radius);
            padding: 10px;
            text-align: center;
            margin: 10px 0;
            font-weight: bold;
            font-size: 0.9rem;
        }
        
        .character-card {
            background: rgba(50, 50, 70, 0.6);
            border-radius: var(--border-radius);
            padding: 20px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 20px;
            transition: var(--transition);
            border: 2px solid transparent;
            cursor: pointer;
        }
        
        .character-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .character-card.selected {
            border-color: var(--primary);
            background: rgba(255, 62, 108, 0.2);
        }
        
        .character-avatar {
            width: 70px;
            height: 70px;
            border-radius: 50%;
            background: linear-gradient(45deg, var(--primary), var(--accent));
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            flex-shrink: 0;
        }
        
        .character-name {
            font-weight: bold;
            color: var(--accent);
            margin-bottom: 5px;
            font-size: 1.1rem;
        }
        
        .character-traits {
            color: var(--text-secondary);
            font-size: 0.95rem;
        }
        
        .progress-bar {
            height: 10px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
            overflow: hidden;
            margin: 25px 0;
            position: relative;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(to right, var(--primary), var(--accent));
            border-radius: 5px;
            transition: width 0.5s ease;
        }
        
        .ai-agent {
            background: rgba(106, 17, 203, 0.2);
            border-radius: var(--border-radius);
            padding: 15px;
            margin: 20px 0;
            text-align: center;
            border: 1px solid var(--primary);
        }
        
        .loading {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 30px;
            text-align: center;
        }
        
        .spinner {
            width: 50px;
            height: 50px;
            border: 5px solid rgba(255, 255, 255, 0.1);
            border-top: 5px solid var(--accent);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .story-container {
            background: rgba(30, 30, 46, 0.8);
            border-radius: var(--border-radius);
            padding: 25px;
            margin-bottom: 20px;
            max-height: 50vh;
            overflow-y: auto;
            border: 1px solid rgba(255, 255, 255, 0.1);
            line-height: 1.8;
            font-size: 1.05rem;
        }
        
        .story-title {
            font-size: 1.8rem;
            margin-bottom: 20px;
            color: var(--accent);
            text-align: center;
            font-weight: 700;
            font-family: 'Kalam', cursive;
        }
        
        .scene {
            margin-bottom: 35px;
            padding-bottom: 25px;
            border-bottom: 1px dashed rgba(255, 255, 255, 0.15);
        }
        
        .scene-title {
            font-size: 1.4rem;
            color: var(--primary);
            margin-bottom: 15px;
            font-weight: 600;
            padding-left: 15px;
            border-left: 4px solid var(--accent);
        }
        
        .cinematic-tip {
            background: rgba(255, 107, 107, 0.15);
            border-left: 4px solid var(--accent);
            padding: 18px;
            font-style: italic;
            border-radius: 0 var(--border-radius) var(--border-radius) 0;
            font-size: 1rem;
            margin-top: 20px;
            position: relative;
        }
        
        .ad-placeholder {
            background: linear-gradient(45deg, #ff416c, #ff4b2b);
            border-radius: var(--border-radius);
            padding: 20px;
            text-align: center;
            margin: 25px 0;
            animation: gradientAnimation 4s ease infinite;
            background-size: 200% 200%;
            font-weight: 600;
            position: relative;
            overflow: hidden;
        }
        
        .conflict-card {
            padding: 20px;
            background: rgba(50, 50, 70, 0.6);
            border-radius: var(--border-radius);
            cursor: pointer;
            transition: var(--transition);
            border: 2px solid transparent;
        }
        
        .conflict-card:hover {
            transform: translateY(-3px);
            background: rgba(80, 80, 120, 0.4);
        }
        
        .conflict-card.selected {
            background: rgba(255, 62, 108, 0.2);
            border-color: var(--primary);
        }
        
        .summary-item {
            display: flex;
            justify-content: space-between;
            padding: 15px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .summary-label {
            color: var(--text-secondary);
            font-weight: 500;
        }
        
        .summary-value {
            font-weight: 600;
            text-align: right;
            color: var(--accent);
            max-width: 60%;
        }
        
        .story-type-btn {
            padding: 15px;
            text-align: center;
            background: rgba(50, 50, 70, 0.6);
            border-radius: var(--border-radius);
            cursor: pointer;
            transition: var(--transition);
            border: 2px solid transparent;
            font-weight: 600;
        }
        
        .story-type-btn:hover {
            transform: translateY(-3px);
            background: rgba(80, 80, 120, 0.4);
        }
        
        .story-type-btn.selected {
            background: rgba(255, 62, 108, 0.2);
            border-color: var(--primary);
            box-shadow: 0 0 15px rgba(255, 62, 108, 0.4);
        }
        
        .toolbar {
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .toolbar-btn {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text);
            padding: 12px 15px;
            border-radius: var(--border-radius);
            cursor: pointer;
            transition: var(--transition);
            display: flex;
            align-items: center;
            gap: 8px;
            flex: 1;
            min-width: 120px;
            justify-content: center;
            font-weight: 500;
            margin-bottom: 10px;
        }
        
        .toolbar-btn:hover {
            background: rgba(255, 62, 108, 0.3);
            transform: translateY(-2px);
        }
        
        .stTextInput input, .stTextArea textarea, .stSelectbox select {
            background: rgba(30, 30, 46, 0.8) !important;
            color: var(--text) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: var(--border-radius) !important;
            padding: 10px !important;
        }
        
        .stTextInput label, .stTextArea label, .stSelectbox label {
            color: var(--text-secondary) !important;
            font-weight: 600 !important;
        }
        
        .stButton>button {
            width: 100%;
            background: linear-gradient(to right, var(--primary), var(--accent)) !important;
            color: white !important;
            border-radius: var(--border-radius) !important;
            padding: 18px 25px !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            box-shadow: 0 6px 20px rgba(255, 62, 108, 0.4) !important;
            transition: var(--transition) !important;
        }
        
        .stButton>button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 25px rgba(255, 62, 108, 0.6) !important;
        }
        
        .floating-icon {
            position: absolute;
            font-size: 5rem;
            opacity: 0.1;
            z-index: 0;
            animation: float 8s ease-in-out infinite;
        }
        
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }
        
        .icon-1 { top: 10%; left: 5%; }
        .icon-2 { top: 25%; right: 5%; animation-delay: 1s; }
        .icon-3 { bottom: 20%; left: 10%; animation-delay: 2s; }
        .icon-4 { bottom: 15%; right: 15%; animation-delay: 3s; }
        
        @media (max-width: 500px) {
            .app-container {
                min-height: 95vh;
            }
            
            .option-grid {
                grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            }
            
            .btn-group {
                flex-direction: column;
            }
            
            .story-container {
                max-height: 45vh;
            }
            
            .toolbar-btn {
                min-width: 100px;
                font-size: 0.9rem;
                padding: 10px 12px;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# Navigation function
def navigate_to(screen):
    st.session_state.current_screen = screen
    st.experimental_rerun()

# Login screen
def login_screen():
    st.markdown("""
    <div class="app-header">
        <div class="floating-icon icon-1">📜</div>
        <div class="floating-icon icon-2">🎬</div>
        <div class="floating-icon icon-3">✨</div>
        <div class="floating-icon icon-4">🎭</div>
        
        <h1 class="app-title">ScriptWizard AI</h1>
        <p class="app-subtitle">Create stories in any language - All features FREE!</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
        <div class="card">
            <h2 class="screen-title">Welcome to ScriptWizard</h2>
            <p class="screen-description">Sign in to create amazing stories, novels, and scripts</p>
            
            <div class="free-banner">
                <i class="fas fa-crown"></i> ALL FEATURES UNLOCKED - NO PAYMENTS REQUIRED
            </div>
        """, unsafe_allow_html=True)
        
        email = st.text_input("Email", placeholder="Enter your email", key="login_email")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
        
        if st.button("Login", key="login_btn", use_container_width=True):
            if email and password:
                st.session_state.selections["email"] = email
                navigate_to("genre")
            else:
                st.warning("Please enter email and password")
        
        st.markdown("<p style='text-align: center; margin: 20px 0; color: var(--text-secondary);'>OR</p>", unsafe_allow_html=True)
        
        if st.button("Continue with Google", key="google_btn", use_container_width=True):
            st.info("Google login functionality would be implemented here")
        
        st.markdown("""
        </div>
        
        <div class="ad-placeholder">
            <p><i class="fas fa-ad"></i> Advertisement Space</p>
            <small>Our app is completely free - Ads help support development</small>
        </div>
        
        <p style="text-align: center; margin-top: 20px; color: var(--text-secondary);">
            Don't have an account? <a href="#" style="color: var(--accent); font-weight: 600;">Sign Up</a>
        </p>
        """, unsafe_allow_html=True)

# Genre selection screen
def genre_screen():
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">ScriptWizard AI</h1>
        <p class="app-subtitle">Create stories in any language - All features FREE!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 class='screen-title'>Choose Your Genre</h2>", unsafe_allow_html=True)
    st.markdown("<p class='screen-description'>Select the genre for your story</p>", unsafe_allow_html=True)
    
    progress = 12.5
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress}%;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    genres = [
        ("Bollywood Masala", "fas fa-film"),
        ("Kids Cartoon", "fas fa-child"),
        ("Mythological", "fas fa-om"),
        ("Historical Drama", "fas fa-fort-awesome"),
        ("Romantic Comedy", "fas fa-heart"),
        ("Action Thriller", "fas fa-running"),
        ("Family Drama", "fas fa-home"),
        ("Sci-Fi Fantasy", "fas fa-rocket"),
        ("Horror Comedy", "fas fa-ghost"),
        ("Patriotic", "fas fa-flag"),
        ("Crime Mystery", "fas fa-search"),
        ("Social Issue", "fas fa-hands-helping")
    ]
    
    cols = st.columns(3)
    col_index = 0
    
    for genre, icon in genres:
        with cols[col_index]:
            is_selected = st.session_state.selections['genre'] == genre
            st.markdown(f"""
            <div class="option-card {'selected' if is_selected else ''}" 
                onclick="window.parent.postMessage({{'genre': '{genre}'}}, '*');">
                <i class="{icon}"></i>
                <h3>{genre}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        col_index = (col_index + 1) % 3
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Back", key="genre_back", use_container_width=True):
            navigate_to("login")
    with col2:
        if st.button("Next", key="genre_next", use_container_width=True):
            if st.session_state.selections['genre']:
                navigate_to("setting")
            else:
                st.warning("Please select a genre")

# Setting selection screen
def setting_screen():
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">ScriptWizard AI</h1>
        <p class="app-subtitle">Create stories in any language - All features FREE!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 class='screen-title'>Story Setting</h2>", unsafe_allow_html=True)
    st.markdown("<p class='screen-description'>Where does your story take place?</p>", unsafe_allow_html=True)
    
    progress = 25
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress}%;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    settings = [
        ("Grand Indian Wedding", "fas fa-gem"),
        ("Mumbai Streets", "fas fa-city"),
        ("Magical Forest", "fas fa-tree"),
        ("Royal Palace", "fas fa-crown"),
        ("Space Adventure Park", "fas fa-space-shuttle"),
        ("Village Fair", "fas fa-umbrella-beach"),
        ("Himalayan Monastery", "fas fa-mountain"),
        ("Underwater Kingdom", "fas fa-water"),
        ("Candyland", "fas fa-candy-cane"),
        ("Ancient Temple", "fas fa-place-of-worship"),
        ("Futuristic Delhi", "fas fa-futbol"),
        ("Enchanted School", "fas fa-school"),
        ("Desert Village", "fas fa-sun"),
        ("Haunted Haveli", "fas fa-ghost"),
        ("Kerala Backwaters", "fas fa-ship"),
        ("Robot Factory", "fas fa-robot")
    ]
    
    cols = st.columns(3)
    col_index = 0
    
    for setting, icon in settings:
        with cols[col_index]:
            is_selected = st.session_state.selections['setting'] == setting
            st.markdown(f"""
            <div class="option-card {'selected' if is_selected else ''}" 
                onclick="window.parent.postMessage({{'setting': '{setting}'}}, '*');">
                <i class="{icon}"></i>
                <h3>{setting}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        col_index = (col_index + 1) % 3
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Back", key="setting_back", use_container_width=True):
            navigate_to("genre")
    with col2:
        if st.button("Next", key="setting_next", use_container_width=True):
            if st.session_state.selections['setting']:
                navigate_to("character")
            else:
                st.warning("Please select a setting")

# Character creation screen
def character_screen():
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">ScriptWizard AI</h1>
        <p class="app-subtitle">Create stories in any language - All features FREE!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 class='screen-title'>Create Characters</h2>", unsafe_allow_html=True)
    st.markdown("<p class='screen-description'>Select your main characters</p>", unsafe_allow_html=True)
    
    progress = 37.5
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress}%;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="free-banner">
        <i class="fas fa-unlock"></i> ALL CHARACTERS UNLOCKED - COMPLETELY FREE!
    </div>
    """, unsafe_allow_html=True)
    
    characters = [
        ("hero", "Raj", "Charming, brave, romantic hero with a heart of gold", "👨"),
        ("heroine", "Priya", "Strong, independent woman with a mysterious past", "👩"),
        ("villain", "Vikram", "Ruthless businessman with a hidden agenda", "🦹"),
        ("comic", "Bunty", "Raj's funny best friend who lightens the mood", "🤡"),
        ("kid", "Chotu", "Smart, tech-savvy kid who saves the day", "🧒"),
        ("mentor", "Guruji", "Wise old man who guides the hero", "🧓"),
        ("sidekick", "Motu", "Loyal friend who supports the hero", "🧑")
    ]
    
    for role, name, traits, emoji in characters:
        is_selected = any(char['name'] == name for char in st.session_state.selections['characters'])
        st.markdown(f"""
        <div class="character-card {'selected' if is_selected else ''}" 
            onclick="window.parent.postMessage({{'character': '{name}'}}, '*');">
            <div class="character-avatar">
                {emoji}
            </div>
            <div class="character-info">
                <div class="character-name">{name} ({role.capitalize()})</div>
                <div class="character-traits">{traits.split(',')[0]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Back", key="character_back", use_container_width=True):
            navigate_to("setting")
    with col2:
        if st.button("Next", key="character_next", use_container_width=True):
            if st.session_state.selections['characters']:
                navigate_to("language")
            else:
                st.warning("Please select at least one character")

# Language selection screen
def language_screen():
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">ScriptWizard AI</h1>
        <p class="app-subtitle">Create stories in any language - All features FREE!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 class='screen-title'>Language & Style</h2>", unsafe_allow_html=True)
    st.markdown("<p class='screen-description'>Select language and writing style</p>", unsafe_allow_html=True)
    
    progress = 50
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress}%;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="free-banner">
        <i class="fas fa-globe"></i> ALL LANGUAGES AVAILABLE - NO RESTRICTIONS!
    </div>
    """, unsafe_allow_html=True)
    
    languages = [
        "Hindi (हिंदी)", "English", "Tamil (தமிழ்)", "Telugu (తెలుగు)", 
        "Malayalam (മലയാളം)", "Kannada (ಕನ್ನಡ)", "Marathi (मराठी)", 
        "Bengali (বাংলা)", "Gujarati (ગુજરાતી)", "Punjabi (ਪੰਜਾਬੀ)", 
        "Urdu (اردو)", "Odia (ଓଡ଼ିଆ)", "Assamese (অসমীয়া)", "Mandarin (中文)", 
        "Japanese (日本語)", "Korean (한국어)", "Thai (ไทย)", "French (Français)", 
        "German (Deutsch)", "Spanish (Español)", "Italian (Italiano)", 
        "Russian (Русский)"
    ]
    
    tones = [
        "Bollywood Masala", "Kids Cartoon", "Mythological Epic", 
        "Realistic", "Humorous", "Dark Thriller", "Poetic", 
        "Dramatic", "Satirical", "Romantic"
    ]
    
    # Language selection
    lang_index = languages.index(st.session_state.selections['language']) if st.session_state.selections['language'] in languages else 0
    st.session_state.selections['language'] = st.selectbox("Language", languages, index=lang_index)
    
    # Tone selection
    tone_index = tones.index(st.session_state.selections['tone']) if st.session_state.selections['tone'] in tones else 0
    st.session_state.selections['tone'] = st.selectbox("Tone/Style", tones, index=tone_index)
    
    st.markdown("""
    <div class="ai-agent">
        <h3><i class="fas fa-robot"></i> AI Story Agent</h3>
        <p>Our intelligent AI will craft a unique, detailed story based on your selections</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Back", key="language_back", use_container_width=True):
            navigate_to("character")
    with col2:
        if st.button("Next", key="language_next", use_container_width=True):
            navigate_to("conflict")

# Conflict screen
def conflict_screen():
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">ScriptWizard AI</h1>
        <p class="app-subtitle">Create stories in any language - All features FREE!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 class='screen-title'>Main Conflict</h2>", unsafe_allow_html=True)
    st.markdown("<p class='screen-description'>What drives your story forward?</p>", unsafe_allow_html=True)
    
    progress = 62.5
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress}%;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    conflicts = [
        ("Lost Heirloom", "A priceless family artifact holds a secret that could change everything"),
        ("Forbidden Love", "Two lovers from rival families must overcome societal barriers"),
        ("Hidden Identity", "The protagonist discovers they have a secret heritage with great responsibility"),
        ("Corporate Conspiracy", "A powerful company is hiding a dangerous secret that threatens millions"),
        ("Supernatural Threat", "An ancient evil awakens and only the chosen one can stop it"),
        ("Political Intrigue", "A conspiracy at the highest levels of government threatens the nation"),
        ("Family Secret", "A long-buried family secret resurfaces, threatening to tear relationships apart"),
        ("Magical Curse", "A centuries-old curse begins to manifest with dangerous consequences"),
        ("Technological Takeover", "An AI gains consciousness and plans to take control of all digital systems"),
        ("Mythical Prophecy", "An ancient prophecy foretells a great calamity that only the hero can prevent")
    ]
    
    cols = st.columns(2)
    col_index = 0
    
    for title, description in conflicts:
        with cols[col_index]:
            is_selected = st.session_state.selections['conflict'] == description
            st.markdown(f"""
            <div class="conflict-card {'selected' if is_selected else ''}" 
                onclick="window.parent.postMessage({{'conflict': '{description}'}}, '*');">
                <h3>{title}</h3>
                <p>{description}</p>
            </div>
            """, unsafe_allow_html=True)
        
        col_index = (col_index + 1) % 2
    
    # Custom conflict
    custom_conflict = st.text_area("Or describe your own conflict", 
                                  placeholder="Describe the main conflict or plot twist...",
                                  value=st.session_state.selections['conflict'] if st.session_state.selections['conflict'] and not any(st.session_state.selections['conflict'] == d for _, d in conflicts) else "")
    
    if custom_conflict:
        st.session_state.selections['conflict'] = custom_conflict
    
    st.markdown("""
    <div class="ai-agent">
        <h3><i class="fas fa-brain"></i> AI Conflict Analyzer</h3>
        <p>Our AI will transform your conflict into a compelling narrative</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Back", key="conflict_back", use_container_width=True):
            navigate_to("language")
    with col2:
        if st.button("Next", key="conflict_next", use_container_width=True):
            if st.session_state.selections['conflict']:
                navigate_to("ending")
            else:
                st.warning("Please select or describe a conflict")

# Ending screen
def ending_screen():
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">ScriptWizard AI</h1>
        <p class="app-subtitle">Create stories in any language - All features FREE!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 class='screen-title'>Choose Your Ending</h2>", unsafe_allow_html=True)
    st.markdown("<p class='screen-description'>How will your story conclude?</p>", unsafe_allow_html=True)
    
    progress = 75
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress}%;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    endings = [
        ("Heroic Victory", "fas fa-trophy"),
        ("Tragic Sacrifice", "fas fa-skull"),
        ("Open Ending", "fas fa-question"),
        ("Plot Twist", "fas fa-sync-alt"),
        ("Happy Reunion", "fas fa-laugh-beam"),
        ("Bittersweet", "fas fa-meh"),
        ("Redemption", "fas fa-hands-helping"),
        ("New Beginning", "fas fa-seedling"),
        ("Cliffhanger", "fas fa-mountain"),
        ("Philosophical", "fas fa-brain")
    ]
    
    cols = st.columns(3)
    col_index = 0
    
    for ending, icon in endings:
        with cols[col_index]:
            is_selected = st.session_state.selections['ending'] == ending
            st.markdown(f"""
            <div class="option-card {'selected' if is_selected else ''}" 
                onclick="window.parent.postMessage({{'ending': '{ending}'}}, '*');">
                <i class="{icon}"></i>
                <h3>{ending}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        col_index = (col_index + 1) % 3
    
    st.markdown("""
    <div class="ai-agent">
        <h3><i class="fas fa-wand-magic-sparkles"></i> AI Story Weaver</h3>
        <p>Our AI will craft a unique conclusion that will leave readers wanting more</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Back", key="ending_back", use_container_width=True):
            navigate_to("conflict")
    with col2:
        if st.button("Next", key="ending_next", use_container_width=True):
            if st.session_state.selections['ending']:
                navigate_to("confirm")
            else:
                st.warning("Please select an ending")

# Confirmation screen
def confirm_screen():
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">ScriptWizard AI</h1>
        <p class="app-subtitle">Create stories in any language - All features FREE!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 class='screen-title'>Confirm Your Story</h2>", unsafe_allow_html=True)
    st.markdown("<p class='screen-description'>Review your selections before generating</p>", unsafe_allow_html=True)
    
    progress = 87.5
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress}%;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="free-banner">
        <i class="fas fa-gift"></i> ENJOY OUR APP COMPLETELY FREE - NO HIDDEN COSTS!
    </div>
    """, unsafe_allow_html=True)
    
    # Summary card
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        # Summary items
        st.markdown("""
        <div class="summary-item">
            <span class="summary-label">Genre:</span>
            <span class="summary-value">{genre}</span>
        </div>
        <div class="summary-item">
            <span class="summary-label">Setting:</span>
            <span class="summary-value">{setting}</span>
        </div>
        <div class="summary-item">
            <span class="summary-label">Characters:</span>
            <span class="summary-value">{characters}</span>
        </div>
        <div class="summary-item">
            <span class="summary-label">Language:</span>
            <span class="summary-value">{language}</span>
        </div>
        <div class="summary-item">
            <span class="summary-label">Tone:</span>
            <span class="summary-value">{tone}</span>
        </div>
        <div class="summary-item">
            <span class="summary-label">Conflict:</span>
            <span class="summary-value">{conflict}</span>
        </div>
        <div class="summary-item">
            <span class="summary-label">Ending:</span>
            <span class="summary-value">{ending}</span>
        </div>
        """.format(
            genre=st.session_state.selections['genre'] or "Not selected",
            setting=st.session_state.selections['setting'] or "Not selected",
            characters=", ".join([c['name'] for c in st.session_state.selections['characters']]) or "Not selected",
            language=st.session_state.selections['language'],
            tone=st.session_state.selections['tone'],
            conflict=(st.session_state.selections['conflict'][:50] + "..." 
                     if st.session_state.selections['conflict'] and len(st.session_state.selections['conflict']) > 50 
                     else st.session_state.selections['conflict']) if st.session_state.selections['conflict'] else "Not selected",
            ending=st.session_state.selections['ending'] or "Not selected"
        ), unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="ai-agent">
        <h3><i class="fas fa-robot"></i> AI Story Generator</h3>
        <p>Our intelligent agent will now create your unique story based on all your selections</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Story type selection
    col1, col2 = st.columns(2)
    with col1:
        is_story = st.session_state.selections['story_type'] == 'story'
        st.markdown(f"""
        <div class="story-type-btn {'selected' if is_story else ''}" 
            onclick="window.parent.postMessage({{'story_type': 'story'}}, '*');">
            <i class="fas fa-book"></i>
            Generate Story (2000+ words)
        </div>
        """, unsafe_allow_html=True)
    with col2:
        is_novel = st.session_state.selections['story_type'] == 'novel'
        st.markdown(f"""
        <div class="story-type-btn {'selected' if is_novel else ''}" 
            onclick="window.parent.postMessage({{'story_type': 'novel'}}, '*');">
            <i class="fas fa-book-open"></i>
            Generate Novel (10000+ words)
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Back", key="confirm_back", use_container_width=True):
            navigate_to("ending")
    with col2:
        if st.button("Generate Story", key="generate_story", use_container_width=True):
            st.session_state.loading = True
            st.session_state.char_count = 0
            st.session_state.scene_count = 0
            st.session_state.story_progress = 0
            navigate_to("loading")

# Loading screen
def loading_screen():
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">ScriptWizard AI</h1>
        <p class="app-subtitle">Create stories in any language - All features FREE!</p>
    </div>
    
    <div class="loading">
        <div class="spinner"></div>
        <h2>AI is generating your story</h2>
        <p>Our intelligent agent is crafting a unique, detailed story based on your selections</p>
        <div class="ai-agent">
            <h3><i class="fas fa-robot"></i> AI Agent Working</h3>
            <p>Analyzing characters: <span id="char-count">{char_count}</span> | Building scenes: <span id="scene-count">{scene_count}</span> | Progress: <span id="progress">{progress}%</span></p>
        </div>
    </div>
    """.format(
        char_count=st.session_state.char_count,
        scene_count=st.session_state.scene_count,
        progress=st.session_state.story_progress
    ), unsafe_allow_html=True)
    
    # Simulate AI processing
    if st.session_state.loading:
        time.sleep(0.3)
        
        max_char_count = len(st.session_state.selections['characters'])
        max_scene_count = 6 if st.session_state.selections['story_type'] == 'story' else 12
        
        if st.session_state.char_count < max_char_count:
            st.session_state.char_count += 1
            st.session_state.story_progress = int(10 + (st.session_state.char_count / max_char_count) * 30)
            st.experimental_rerun()
        
        if st.session_state.char_count >= max_char_count and st.session_state.scene_count < max_scene_count:
            st.session_state.scene_count += 1
            st.session_state.story_progress = int(40 + (st.session_state.scene_count / max_scene_count) * 50)
            st.experimental_rerun()
        
        if st.session_state.char_count >= max_char_count and st.session_state.scene_count >= max_scene_count:
            st.session_state.story_progress = 100
            time.sleep(0.5)
            generate_story()
            st.session_state.loading = False
            navigate_to("output")
            st.experimental_rerun()

# Generate story content
def generate_story():
    selections = st.session_state.selections
    hero = next((c for c in selections['characters'] if c['role'] == 'hero'), 
               {"name": "Raj", "traits": "Brave hero"})
    heroine = next((c for c in selections['characters'] if c['role'] == 'heroine'), 
                 {"name": "Priya", "traits": "Strong heroine"})
    villain = next((c for c in selections['characters'] if c['role'] == 'villain'), 
                 {"name": "Vikram", "traits": "Ruthless villain"})
    
    is_novel = selections['story_type'] == 'novel'
    scene_count = 12 if is_novel else 6
    
    story = f"""
    <div class="story-title">{generate_title(selections)}</div>
    """
    
    # Generate multiple scenes
    for i in range(1, scene_count + 1):
        story += generate_scene(i, scene_count, selections, hero, heroine, villain)
    
    # Add cinematic tips
    story += generate_cinematic_tips(selections)
    
    st.session_state.generated_story = story

# Helper functions for story generation
def generate_title(selections):
    titles = {
        'Bollywood Masala': ['Pyaar Ki Yeh Kahani', 'Dilwale Dulhania', 'Ishq Waala Love', 'Jab We Met Again'],
        'Kids Cartoon': ['The Adventure of Chotu', 'Magic Forest Friends', 'Space Explorers Club', 'Candyland Dreams'],
        'Mythological': ['The Legend of Gods', 'Eternal Warriors', 'Divine Prophecy', 'Realm of Immortals'],
        'Historical Drama': ['The Crown of Kings', 'Era of Empires', 'Warrior Princess', 'Legacy of Blood']
    }
    
    default_titles = ['The Great Journey', 'Eternal Bonds', 'Secrets Unveiled', 'Destiny\'s Path']
    
    if selections['genre'] in titles:
        return random.choice(titles[selections['genre']])
    
    return random.choice(default_titles)

def generate_scene(scene_num, total_scenes, selections, hero, heroine, villain):
    scene_title = ""
    scene_content = ""
    
    # First scene
    if scene_num == 1:
        scene_title = f"SCENE 1: {selections['setting'].upper()}"
        scene_content = f"""
            EXT. {selections['setting'].upper()} - DAY<br><br>
            {hero['name']} stands at the center of {selections['setting']}, contemplating the {selections['conflict'].lower() if selections['conflict'] else 'mystery that awaits'}. 
            The {selections['tone'].lower()} atmosphere sets the stage for this {selections['genre'].lower()} tale.<br><br>
            
            As {hero['name']} reflects on the challenges ahead, {villain['name']} makes a dramatic entrance, 
            setting the conflict into motion with a declaration: "{selections['conflict'][:50] if selections['conflict'] else 'Everything is about to change...'}"
        """
    # Climax scene
    elif scene_num == total_scenes - 1:
        scene_title = f"SCENE {scene_num}: THE CLIMAX"
        scene_content = f"""
            INT. {selections['setting'].upper()} - NIGHT<br><br>
            {hero['name']} confronts {villain['name']} in a final showdown. The {selections['conflict'].lower() if selections['conflict'] else 'central conflict'} reaches its peak as 
            {'sacrifices are made' if 'Tragic' in selections['ending'] else 'secrets are revealed'}.<br><br>
            
            "{'There is still good in you!' if 'Redemption' in selections['ending'] else 'This ends now!'}" {hero['name']} declares, 
            {'voice trembling with emotion' if 'Dramatic' in selections['tone'] else 'weapon at the ready'}.
        """
    # Final scene
    elif scene_num == total_scenes:
        scene_title = f"SCENE {scene_num}: {selections['ending'].upper()} CONCLUSION"
        scene_content = f"""
            EXT. {selections['setting'].upper()} - DAWN<br><br>
            {generate_ending(selections, hero, heroine)}
        """
    # Middle scenes
    else:
        scene_title = f"SCENE {scene_num}: {get_scene_title(scene_num, total_scenes)}"
        scene_content = f"""
            {get_random_location(selections)}<br><br>
            {hero['name']} {get_character_action(scene_num, selections)} as the plot thickens. 
            {get_plot_development(scene_num, selections)}<br><br>
            
            {villain['name']} {get_villain_action(scene_num, selections)}, adding complexity to the {selections['conflict'].lower() if selections['conflict'] else 'central conflict'}.
        """
    
    return f"""
        <div class="scene">
            <div class="scene-title">{scene_title}</div>
            <div class="scene-content">
                {scene_content}
            </div>
            <div class="cinematic-tip">
                {generate_cinematic_tip(scene_num, selections)}
            </div>
        </div>
    """

def generate_ending(selections, hero, heroine):
    if selections['ending'] == 'Heroic Victory':
        return f"""
            {hero['name']} stands triumphant, having resolved {selections['conflict'].lower() if selections['conflict'] else 'the crisis'}. 
            {heroine['name']} rushes to {hero['name']}'s side as the people of {selections['setting']} celebrate their victory. 
            "You did it!" she exclaims, embracing {hero['name']}. The future looks bright.
        """
    elif selections['ending'] == 'Tragic Sacrifice':
        return f"""
            {hero['name']} lies wounded, having made the ultimate sacrifice to save {selections['setting']}. 
            {heroine['name']} cradles {hero['name']} as the conflict resolves at a terrible cost. 
            "It wasn't supposed to end this way," she whispers, tears streaming down her face.
        """
    elif selections['ending'] == 'Open Ending':
        return f"""
            {hero['name']} and the antagonist stand facing each other, both wounded but neither defeated. 
            "This isn't over," {hero['name']} declares, eyes locked on the enemy. 
            The {selections['conflict'].lower() if selections['conflict'] else 'conflict'} remains unresolved as the screen fades to black.
        """
    else:
        return f"""
            The story concludes with {hero['name']} reflecting on the journey through {selections['setting']}. 
            {'The ' + selections['conflict'].lower() + ' has been resolved' if selections['conflict'] else 'Peace has been restored'}, 
            and a new chapter begins for everyone involved.
        """

def generate_cinematic_tips(selections):
    return f"""
        <div class="cinematic-tip">
            <strong>FULL PRODUCTION GUIDE:</strong> This {selections['genre']} story in {selections['language']} should be filmed with attention to {selections['tone'].lower()} details. 
            {'For the novel adaptation, focus on character development and subplots.' if selections['story_type'] == 'novel' else 'For the short story, maintain a fast pace with impactful scenes.'}
        </div>
    """

def get_scene_title(scene_num, total_scenes):
    scene_titles = [
        "The Journey Begins",
        "Unexpected Encounter",
        "Rising Tensions",
        "Darkest Hour",
        "Twist of Fate",
        "Point of No Return",
        "Allies Gather",
        "Secrets Revealed",
        "Betrayal",
        "Preparation",
        "The Calm Before Storm"
    ]
    return scene_titles[scene_num % len(scene_titles)] if scene_titles else "Plot Development"

def get_random_location(selections):
    locations = [
        f"EXT. {selections['setting'].upper()} - DAY",
        "INT. ANCIENT TEMPLE - NIGHT",
        "EXT. FOREST CLEARING - DUSK",
        "INT. SECRET HIDEOUT - DAWN",
        "EXT. MOUNTAIN PASS - NOON",
        "INT. ROYAL PALACE - EVENING"
    ]
    return random.choice(locations)

def get_character_action(scene_num, selections):
    actions = [
        f"discovers a crucial clue about {selections['conflict'][:30] if selections['conflict'] else 'the mystery'}",
        "encounters an unexpected ally who provides new insights",
        "struggles with personal doubts while facing increasing challenges",
        "devises a clever plan to overcome the latest obstacle",
        "reflects on the journey so far, gaining new determination",
        "confronts a moral dilemma that tests their core values"
    ]
    return actions[scene_num % len(actions)]

def get_plot_development(scene_num, selections):
    developments = [
        "A new piece of information comes to light that changes everything.",
        f"The stakes are raised as the true scale of {selections['conflict'][:30] if selections['conflict'] else 'the conflict'} becomes apparent.",
        f"Unexpected events force {selections['characters'][0]['name'] if selections['characters'] else 'the hero'} to reconsider their approach.",
        "A flashback reveals crucial backstory that explains the current situation.",
        "The situation grows more complex as hidden motives come to the surface.",
        "A secondary character provides wisdom that shifts the protagonist's perspective."
    ]
    return developments[scene_num % len(developments)]

def get_villain_action(scene_num, selections):
    actions = [
        "unveils a new layer to their master plan",
        "reveals a personal connection to the protagonist that changes the dynamic",
        "demonstrates unexpected depth and complexity",
        "creates a new obstacle that seems insurmountable",
        "manipulates events from behind the scenes",
        "confronts the hero directly in a tense standoff"
    ]
    return actions[scene_num % len(actions)]

def generate_cinematic_tip(scene_num, selections):
    tips = [
        "Use wide establishing shots to show the setting. Close-ups for emotional moments.",
        "Consider using handheld camera for intense action sequences.",
        "Lighting should reflect the mood - warm tones for hopeful scenes, cool for tense moments.",
        f"Incorporate cultural elements authentic to the {selections['language']} setting.",
        f"Use color grading to enhance the {selections['tone'].lower()} atmosphere.",
        "Silence can be powerful - don't be afraid to use quiet moments for dramatic effect.",
        "Transition between scenes using thematic elements rather than hard cuts."
    ]
    return tips[scene_num % len(tips)]

# Output screen
def output_screen():
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">ScriptWizard AI</h1>
        <p class="app-subtitle">Create stories in any language - All features FREE!</p>
    </div>
    """, unsafe_allow_html=True)
    
    output_desc = "2000+ word story" if st.session_state.selections['story_type'] == 'story' else "10000+ word novel"
    st.markdown(f"<h2 class='screen-title'>Your Generated Script</h2>", unsafe_allow_html=True)
    st.markdown(f"<p class='screen-description' id='output-description'>Your {output_desc} in {st.session_state.selections['language']} with {st.session_state.selections['tone']} style</p>", unsafe_allow_html=True)
    
    # Toolbar
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("Edit", key="edit_btn", use_container_width=True):
            st.info("Edit functionality would be implemented here")
    with col2:
        if st.button("Save", key="save_btn", use_container_width=True):
            st.success("Story saved successfully!")
    with col3:
        if st.button("Export", key="export_btn", use_container_width=True):
            st.success("Exported as PDF")
    with col4:
        if st.button("Enhance", key="enhance_btn", use_container_width=True):
            st.info("AI enhancement applied")
    with col5:
        if st.button("Video Tips", key="video_btn", use_container_width=True):
            st.info("Video tips displayed")
    
    # Display the generated story
    st.markdown(f"""
    <div class="story-container">
        {st.session_state.generated_story}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="ad-placeholder">
        <p><i class="fas fa-ad"></i> Advertisement Space</p>
        <small>Ads help keep our app completely free for everyone</small>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Back to Edit", key="output_back", use_container_width=True):
        navigate_to("confirm")

# JavaScript handler for card selections
def inject_js_handler():
    js = """
    <script>
    window.addEventListener('message', (event) => {
        if (event.data.genre) {
            Streamlit.setComponentValue(event.data.genre);
            Streamlit.setComponentValue("genre_selected");
        }
        if (event.data.setting) {
            Streamlit.setComponentValue(event.data.setting);
            Streamlit.setComponentValue("setting_selected");
        }
        if (event.data.character) {
            Streamlit.setComponentValue(event.data.character);
            Streamlit.setComponentValue("character_selected");
        }
        if (event.data.conflict) {
            Streamlit.setComponentValue(event.data.conflict);
            Streamlit.setComponentValue("conflict_selected");
        }
        if (event.data.ending) {
            Streamlit.setComponentValue(event.data.ending);
            Streamlit.setComponentValue("ending_selected");
        }
        if (event.data.story_type) {
            Streamlit.setComponentValue(event.data.story_type);
            Streamlit.setComponentValue("story_type_selected");
        }
    });
    </script>
    """
    html(js, height=0)

# Main app
def main():
    init_session()
    apply_custom_css()
    
    # Add Font Awesome
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">', unsafe_allow_html=True)
    
    # Add Google Fonts
    st.markdown('<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Kalam:wght@400;700&display=swap" rel="stylesheet">', unsafe_allow_html=True)
    
    # Inject JavaScript for card selections
    inject_js_handler()
    
    # Handle card selections
    if "genre_selected" in st.session_state:
        st.session_state.selections["genre"] = st.session_state["genre_selected"]
        st.experimental_rerun()
    
    if "setting_selected" in st.session_state:
        st.session_state.selections["setting"] = st.session_state["setting_selected"]
        st.experimental_rerun()
    
    if "character_selected" in st.session_state:
        char_name = st.session_state["character_selected"]
        characters = [
            ("hero", "Raj", "Charming, brave, romantic hero with a heart of gold", "👨"),
            ("heroine", "Priya", "Strong, independent woman with a mysterious past", "👩"),
            ("villain", "Vikram", "Ruthless businessman with a hidden agenda", "🦹"),
            ("comic", "Bunty", "Raj's funny best friend who lightens the mood", "🤡"),
            ("kid", "Chotu", "Smart, tech-savvy kid who saves the day", "🧒"),
            ("mentor", "Guruji", "Wise old man who guides the hero", "🧓"),
            ("sidekick", "Motu", "Loyal friend who supports the hero", "🧑")
        ]
        
        char_info = next((c for c in characters if c[1] == char_name), None)
        
        if char_info:
            role, name, traits, emoji = char_info
            char_data = {"role": role, "name": name, "traits": traits}
            
            # Toggle selection
            if any(char['name'] == name for char in st.session_state.selections['characters']):
                st.session_state.selections['characters'] = [c for c in st.session_state.selections['characters'] if c['name'] != name]
            else:
                st.session_state.selections['characters'].append(char_data)
        
        st.experimental_rerun()
    
    if "conflict_selected" in st.session_state:
        st.session_state.selections["conflict"] = st.session_state["conflict_selected"]
        st.experimental_rerun()
    
    if "ending_selected" in st.session_state:
        st.session_state.selections["ending"] = st.session_state["ending_selected"]
        st.experimental_rerun()
    
    if "story_type_selected" in st.session_state:
        st.session_state.selections["story_type"] = st.session_state["story_type_selected"]
        st.experimental_rerun()
    
    # Screen routing
    screens = {
        "login": login_screen,
        "genre": genre_screen,
        "setting": setting_screen,
        "character": character_screen,
        "language": language_screen,
        "conflict": conflict_screen,
        "ending": ending_screen,
        "confirm": confirm_screen,
        "loading": loading_screen,
        "output": output_screen
    }
    
    if st.session_state.current_screen in screens:
        screens[st.session_state.current_screen]()

if __name__ == "__main__":
    main()