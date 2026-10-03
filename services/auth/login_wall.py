import streamlit as st
from services.persistence.exercise_repository import get_or_create_user


THEME_PRESETS = {
    "🌌 Cyber Neon": {
        "primary": "#6366f1",
        "secondary": "#a855f7",
        "accent": "#ec4899",
        "badge_bg": "rgba(99, 102, 241, 0.14)",
        "badge_border": "rgba(99, 102, 241, 0.4)",
        "badge_text": "#818cf8",
        "title_grad": "linear-gradient(135deg, #ffffff 35%, #a5b4fc 75%, #c084fc 100%)",
        "glow_1": "radial-gradient(circle, rgba(99, 102, 241, 0.22) 0%, rgba(99, 102, 241, 0) 70%)",
        "glow_2": "radial-gradient(circle, rgba(168, 85, 247, 0.20) 0%, rgba(168, 85, 247, 0) 70%)",
        "glow_3": "radial-gradient(circle, rgba(236, 72, 153, 0.12) 0%, rgba(236, 72, 153, 0) 70%)",
        "card_hover_border": "rgba(129, 140, 248, 0.55)",
        "shadow_glow": "rgba(99, 102, 241, 0.28)",
    },
    "⚡ Emerald Matrix": {
        "primary": "#10b981",
        "secondary": "#06b6d4",
        "accent": "#14b8a6",
        "badge_bg": "rgba(16, 185, 129, 0.14)",
        "badge_border": "rgba(16, 185, 129, 0.4)",
        "badge_text": "#34d399",
        "title_grad": "linear-gradient(135deg, #ffffff 35%, #6ee7b7 75%, #38bdf8 100%)",
        "glow_1": "radial-gradient(circle, rgba(16, 185, 129, 0.22) 0%, rgba(16, 185, 129, 0) 70%)",
        "glow_2": "radial-gradient(circle, rgba(6, 182, 212, 0.20) 0%, rgba(6, 182, 212, 0) 70%)",
        "glow_3": "radial-gradient(circle, rgba(20, 184, 166, 0.12) 0%, rgba(20, 184, 166, 0) 70%)",
        "card_hover_border": "rgba(52, 211, 153, 0.55)",
        "shadow_glow": "rgba(16, 185, 129, 0.28)",
    },
    "🔥 Solar Flare": {
        "primary": "#f59e0b",
        "secondary": "#f43f5e",
        "accent": "#fb923c",
        "badge_bg": "rgba(245, 158, 11, 0.14)",
        "badge_border": "rgba(245, 158, 11, 0.4)",
        "badge_text": "#fbbf24",
        "title_grad": "linear-gradient(135deg, #ffffff 35%, #fde68a 75%, #f87171 100%)",
        "glow_1": "radial-gradient(circle, rgba(245, 158, 11, 0.22) 0%, rgba(245, 158, 11, 0) 70%)",
        "glow_2": "radial-gradient(circle, rgba(244, 63, 94, 0.20) 0%, rgba(244, 63, 94, 0) 70%)",
        "glow_3": "radial-gradient(circle, rgba(251, 146, 60, 0.12) 0%, rgba(251, 146, 60, 0) 70%)",
        "card_hover_border": "rgba(251, 191, 36, 0.55)",
        "shadow_glow": "rgba(245, 158, 11, 0.28)",
    },
}


def render_login_wall():
    if st.session_state.get("user_id") is not None:
        return True

    # State for theme preset
    if "landing_theme" not in st.session_state:
        st.session_state.landing_theme = "🌌 Cyber Neon"

    # Top Control Bar (Branding + Theme Switcher)
    top_col1, top_col2 = st.columns([1.5, 1], gap="medium")
    with top_col1:
        st.markdown(
            """
            <div style="display:flex; align-items:center; gap:10px; padding: 4px 0 10px 0;">
                <span style="font-size: 1.8rem;">🏋️</span>
                <span style="font-weight: 800; font-size: 1.35rem; letter-spacing: -0.02em; color: #f8fafc;">
                    APNA <span style="color:#818cf8;">AI COACH</span>
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top_col2:
        selected_theme = st.pills(
            "Theme Aesthetic",
            options=list(THEME_PRESETS.keys()),
            default=st.session_state.landing_theme,
            label_visibility="collapsed",
            key="theme_pill_selector",
        )
        if selected_theme and selected_theme != st.session_state.landing_theme:
            st.session_state.landing_theme = selected_theme
            st.rerun()

    theme = THEME_PRESETS.get(st.session_state.landing_theme, THEME_PRESETS["🌌 Cyber Neon"])

    # Custom Landing Page CSS with Ambient Orbs and Micro-Animations
    st.markdown(
        f"""
        <style>
        /* Hide Streamlit sidebar on landing page */
        [data-testid="stSidebar"] {{
            display: none !important;
        }}
        .block-container {{
            max-width: 1180px !important;
            padding-top: 1.5rem !important;
            padding-bottom: 4rem !important;
            position: relative;
            z-index: 1;
        }}

        /* Ambient Background Blur Orbs */
        .ambient-glow {{
            position: fixed;
            border-radius: 50%;
            pointer-events: none;
            z-index: 0;
            filter: blur(100px);
            opacity: 0.85;
            animation: floatGlow 12s ease-in-out infinite alternate;
        }}

        @keyframes floatGlow {{
            0% {{ transform: translate(0px, 0px) scale(1); }}
            50% {{ transform: translate(30px, -25px) scale(1.06); }}
            100% {{ transform: translate(-20px, 20px) scale(0.96); }}
        }}

        .glow-top-left {{
            top: -120px;
            left: -120px;
            width: 580px;
            height: 580px;
            background: {theme["glow_1"]};
        }}

        .glow-top-right {{
            top: 20px;
            right: -150px;
            width: 620px;
            height: 620px;
            background: {theme["glow_2"]};
        }}

        .glow-center-bottom {{
            bottom: -180px;
            left: 20%;
            width: 720px;
            height: 720px;
            background: {theme["glow_3"]};
        }}

        /* Hero styling */
        .hero-badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 16px;
            border-radius: 9999px;
            background: {theme["badge_bg"]};
            border: 1px solid {theme["badge_border"]};
            color: {theme["badge_text"]};
            font-size: 0.84rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 1.2rem;
            box-shadow: 0 0 20px -4px {theme["badge_border"]};
        }}

        .hero-title {{
            font-size: 3.3rem !important;
            font-weight: 800 !important;
            line-height: 1.15 !important;
            background: {theme["title_grad"]};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1.2rem !important;
            letter-spacing: -0.03em;
        }}

        .hero-subtitle {{
            font-size: 1.22rem !important;
            color: #94a3b8 !important;
            line-height: 1.6 !important;
            max-width: 780px;
            margin-bottom: 2.2rem;
        }}

        /* Glassmorphism Auth Card */
        .auth-card {{
            background: linear-gradient(135deg, rgba(26, 32, 48, 0.75), rgba(15, 20, 32, 0.92));
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 18px;
            padding: 2rem 2.2rem;
            box-shadow: 0 20px 45px -15px rgba(0, 0, 0, 0.7), 0 0 35px -10px {theme["shadow_glow"]};
            margin-bottom: 3rem;
            backdrop-filter: blur(16px);
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .auth-card:hover {{
            border-color: {theme["card_hover_border"]};
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8), 0 0 45px -5px {theme["shadow_glow"]};
        }}

        .auth-card-title {{
            font-size: 1.45rem;
            font-weight: 800;
            color: #f8fafc;
            margin-bottom: 0.4rem;
        }}

        .auth-card-desc {{
            font-size: 0.95rem;
            color: #94a3b8;
            margin-bottom: 1.2rem;
        }}

        /* Interactive Feature Cards with Smooth Hover */
        .feature-card {{
            background: linear-gradient(145deg, rgba(20, 26, 40, 0.85), rgba(12, 16, 26, 0.95));
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 1.8rem;
            height: 100%;
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            overflow: hidden;
        }}

        .feature-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, transparent, {theme["card_hover_border"]}, transparent);
            opacity: 0;
            transition: opacity 0.35s ease;
        }}

        .feature-card:hover {{
            transform: translateY(-8px) scale(1.015);
            border-color: {theme["card_hover_border"]};
            box-shadow: 0 20px 38px -12px {theme["shadow_glow"]}, 0 0 20px -4px {theme["shadow_glow"]};
        }}

        .feature-card:hover::before {{
            opacity: 1;
        }}

        .feature-icon {{
            font-size: 2.3rem;
            margin-bottom: 0.8rem;
            display: inline-block;
            transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .feature-card:hover .feature-icon {{
            transform: scale(1.18) rotate(4deg);
        }}

        .feature-title {{
            font-size: 1.18rem;
            font-weight: 700;
            color: #f1f5f9;
            margin-bottom: 0.5rem;
        }}

        .feature-desc {{
            font-size: 0.92rem;
            color: #94a3b8;
            line-height: 1.6;
        }}

        /* Exercise cards with slide hover */
        .exercise-card {{
            background: linear-gradient(135deg, rgba(23, 29, 44, 0.7), rgba(15, 20, 32, 0.85));
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 14px;
            padding: 1.25rem 1.45rem;
            margin-bottom: 0.85rem;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .exercise-card:hover {{
            transform: translateX(8px);
            border-color: {theme["card_hover_border"]};
            background: linear-gradient(135deg, rgba(30, 40, 60, 0.85), rgba(18, 24, 38, 0.95));
            box-shadow: 0 10px 25px -8px {theme["shadow_glow"]};
        }}

        .exercise-name {{
            font-weight: 700;
            font-size: 1.05rem;
            color: #f1f5f9;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .exercise-desc {{
            font-size: 0.88rem;
            color: #94a3b8;
            margin-top: 5px;
            line-height: 1.5;
        }}

        /* Step cards */
        .step-number {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 42px;
            height: 42px;
            border-radius: 12px;
            background: {theme["badge_bg"]};
            border: 1px solid {theme["badge_border"]};
            color: {theme["badge_text"]};
            font-weight: 800;
            font-size: 1.05rem;
            margin-bottom: 0.9rem;
            box-shadow: 0 0 15px -3px {theme["badge_border"]};
        }}

        /* Section Headings */
        .section-header {{
            text-align: center;
            margin-top: 4.5rem;
            margin-bottom: 2.5rem;
        }}

        .section-title {{
            font-size: 2.1rem;
            font-weight: 800;
            color: #f8fafc;
            margin-bottom: 0.4rem;
            letter-spacing: -0.02em;
        }}

        .section-subtitle {{
            font-size: 1.05rem;
            color: #64748b;
        }}
        </style>

        <!-- Ambient Background Glow Orbs -->
        <div class="ambient-glow glow-top-left"></div>
        <div class="ambient-glow glow-top-right"></div>
        <div class="ambient-glow glow-center-bottom"></div>
        """,
        unsafe_allow_html=True,
    )

    # 1. Hero Section
    st.markdown(
        """
        <div class="hero-badge">⚡ Real-time Neural Fitness Intelligence</div>
        <h1 class="hero-title">Your AI Gym Coach.<br>Live Posture & Voice Feedback.</h1>
        <p class="hero-subtitle">
            Experience Olympic-level coaching at home. Computer-vision posture detection, 
            instant audio corrections, and automated rep counters — running entirely in your browser.
        </p>
        """,
        unsafe_allow_html=True,
    )

    # 2. Main Login / Session Initiation Form
    col_auth, col_banner = st.columns([1.1, 0.9], gap="large")

    with col_auth:
        st.markdown(
            """
            <div class="auth-card">
                <div class="auth-card-title">🚀 Ready to Train?</div>
                <div class="auth-card-desc">No password needed. Enter your athlete name to track your session history.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("landing_login_form", clear_on_submit=False):
            username = st.text_input(
                "Athlete Username",
                placeholder="e.g. himanshu, alex_fit",
                help="Your workout progress and rep counts will be saved under this profile.",
            )
            submit_button = st.form_submit_button(
                "Enter Gym & Launch Camera ➔",
                use_container_width=True,
            )

        if submit_button:
            if not username or not username.strip():
                st.error("Please enter a username to proceed.")
                return False

            user = get_or_create_user(username.strip())
            st.session_state["user_id"] = user["id"]
            st.session_state["username"] = user["username"]
            st.rerun()

    with col_banner:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, rgba(28, 36, 54, 0.75), rgba(15, 20, 32, 0.95));
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 18px;
                padding: 1.9rem;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                height: 100%;
                box-shadow: 0 15px 35px -10px rgba(0,0,0,0.6);
            ">
                <div>
                    <h3 style="color:#f1f5f9; font-size:1.25rem; font-weight:700; margin-bottom:14px; display:flex; align-items:center; gap:8px;">
                        <span>✨</span> What You Get
                    </h3>
                    <ul style="color:#94a3b8; font-size:0.95rem; line-height:2.0; list-style:none; padding-left:0;">
                        <li>🎯 <strong>33-Point 3D Skeletal Tracking</strong> with MediaPipe Pose</li>
                        <li>🎙️ <strong>Instant Voice Coaching</strong> powered by Groq High-Speed LLM</li>
                        <li>📈 <strong>Auto Rep & Depth Counters</strong> with zero wearables</li>
                        <li>🏆 <strong>Post-Workout Form Scorecard</strong> with Rep-by-Rep Flaw Breakdown</li>
                        <li>🔒 <strong>100% Client-Side Privacy</strong> — your camera feed is never stored</li>
                        <li>💾 <strong>Progress History Log</strong> automatically saved to your profile</li>
                    </ul>
                </div>
                <div style="font-size:0.83rem; color:#64748b; margin-top:14px; border-top:1px solid rgba(255,255,255,0.08); padding-top:12px;">
                    Works on Chrome, Edge, Safari, & Firefox with web camera access.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 3. Core Features Section
    st.markdown(
        """
        <div class="section-header">
            <div class="section-title">Built for Peak Human Performance</div>
            <div class="section-subtitle">Cutting-edge edge AI computer vision meets sports biomechanics</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Sub-Degree Vision Tracking</div>
                <div class="feature-desc">
                    High-frame-rate skeletal triangulation continuously computes joint angles, spine posture, and knee displacement at 30+ FPS.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🎙️</div>
                <div class="feature-title">Real-Time Voice Coaching</div>
                <div class="feature-desc">
                    Get spoken cues through your speakers before bad habits take over. Your AI coach tells you to push deeper, straighten your back, or finish strong.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <div class="feature-title">Cadence & Form Analytics</div>
                <div class="feature-desc">
                    Automated concentric & eccentric phase analysis ensures only complete, valid reps are counted with detailed post-workout scorecards.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 4. Supported Exercises Section
    st.markdown(
        """
        <div class="section-header">
            <div class="section-title">Supported Movement Library</div>
            <div class="section-subtitle">Real-time biomechanics feedback tailored for key compound and isolation lifts</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    e_col1, e_col2 = st.columns(2, gap="large")

    with e_col1:
        st.markdown(
            """
            <div class="exercise-card">
                <div class="exercise-name">🏋️ Squats</div>
                <div class="exercise-desc">Monitors knee flexion angle to confirm parallel depth (&lt;90°) while checking thoracic and lumbar spine curvature.</div>
            </div>
            <div class="exercise-card">
                <div class="exercise-name">💪 Push-ups</div>
                <div class="exercise-desc">Detects elbow deflection depth, checks full extension lockout, and flags lower-back sagging or hip piking.</div>
            </div>
            <div class="exercise-card">
                <div class="exercise-name">⚡ Bicep Curls (Dumbbell)</div>
                <div class="exercise-desc">Checks strict elbow isolation against the ribs and prevents momentum cheat-swinging during contraction.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with e_col2:
        st.markdown(
            """
            <div class="exercise-card">
                <div class="exercise-name">🚀 Shoulder Overhead Press</div>
                <div class="exercise-desc">Verifies bilateral lockouts overhead, tracks symmetrical pressing velocity, and warns against dangerous lower-back hyperextension.</div>
            </div>
            <div class="exercise-card">
                <div class="exercise-name">🏃 Lunges</div>
                <div class="exercise-desc">Tracks front knee 90° load angle, ensures vertical torso stability, and alerts on knee-over-toe overextension.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 5. How It Works (3 Steps)
    st.markdown(
        """
        <div class="section-header">
            <div class="section-title">How It Works in 3 Steps</div>
            <div class="section-subtitle">Start your personal AI workout session in under 15 seconds</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    s1, s2, s3 = st.columns(3, gap="medium")

    with s1:
        st.markdown(
            """
            <div class="feature-card" style="text-align:center;">
                <div class="step-number">01</div>
                <div class="feature-title">Set Up Your Camera</div>
                <div class="feature-desc">Place your laptop or phone camera 6-8 feet away with your full body visible in the frame.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with s2:
        st.markdown(
            """
            <div class="feature-card" style="text-align:center;">
                <div class="step-number">02</div>
                <div class="feature-title">Choose Your Target</div>
                <div class="feature-desc">Pick your exercise, set your target sets and reps in the workout dashboard.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with s3:
        st.markdown(
            """
            <div class="feature-card" style="text-align:center;">
                <div class="step-number">03</div>
                <div class="feature-title">Listen & Train</div>
                <div class="feature-desc">Focus on the lift. Your AI Coach speaks cues aloud to guide your form through every single rep.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    st.divider()
    st.markdown(
        """
        <div style="text-align:center; color:#64748b; font-size:0.88rem; padding:15px 0;">
            Apna AI Gym Coach • Engineered with Streamlit, MediaPipe, OpenCV & Groq Neural LLM
        </div>
        """,
        unsafe_allow_html=True,
    )

    return False