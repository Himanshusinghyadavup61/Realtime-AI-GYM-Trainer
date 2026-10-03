import streamlit as st
from services.persistence.exercise_repository import get_or_create_user


def render_login_wall():
    if st.session_state.get("user_id") is not None:
        return True

    # Custom landing page styling
    st.markdown(
        """
        <style>
        /* Full width for landing page & hide sidebar */
        [data-testid="stSidebar"] {
            display: none !important;
        }
        .block-container {
            max-width: 1180px !important;
            padding-top: 2.5rem !important;
            padding-bottom: 4rem !important;
        }

        /* Hero section styling */
        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 16px;
            border-radius: 9999px;
            background: rgba(99, 102, 241, 0.12);
            border: 1px solid rgba(99, 102, 241, 0.35);
            color: #818cf8;
            font-size: 0.85rem;
            font-weight: 600;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 1.2rem;
        }

        .hero-title {
            font-size: 3.2rem !important;
            font-weight: 800 !important;
            line-height: 1.15 !important;
            background: linear-gradient(135deg, #ffffff 40%, #a5b4fc 80%, #c084fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1.2rem !important;
        }

        .hero-subtitle {
            font-size: 1.25rem !important;
            color: #94a3b8 !important;
            line-height: 1.6 !important;
            max-width: 780px;
            margin-bottom: 2.2rem;
        }

        /* Glassmorphism Auth Card */
        .auth-card {
            background: linear-gradient(135deg, rgba(30, 35, 48, 0.75), rgba(17, 21, 32, 0.9));
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 16px;
            padding: 2rem 2.2rem;
            box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.6), 0 0 30px -10px rgba(99, 102, 241, 0.18);
            margin-bottom: 3.5rem;
        }

        .auth-card-title {
            font-size: 1.4rem;
            font-weight: 700;
            color: #f8fafc;
            margin-bottom: 0.4rem;
        }

        .auth-card-desc {
            font-size: 0.95rem;
            color: #94a3b8;
            margin-bottom: 1.2rem;
        }

        /* Feature Cards */
        .feature-card {
            background: #121622;
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 14px;
            padding: 1.7rem;
            height: 100%;
            transition: all 0.25s ease;
        }
        .feature-card:hover {
            border-color: rgba(99, 102, 241, 0.4);
            transform: translateY(-4px);
            box-shadow: 0 12px 28px -10px rgba(99, 102, 241, 0.2);
        }

        .feature-icon {
            font-size: 2.2rem;
            margin-bottom: 0.8rem;
            display: inline-block;
        }

        .feature-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: #f1f5f9;
            margin-bottom: 0.5rem;
        }

        .feature-desc {
            font-size: 0.92rem;
            color: #94a3b8;
            line-height: 1.55;
        }

        /* Exercise pill list */
        .exercise-card {
            background: #151a28;
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 12px;
            padding: 1.2rem 1.4rem;
            margin-bottom: 0.8rem;
        }
        .exercise-name {
            font-weight: 700;
            font-size: 1.05rem;
            color: #e2e8f0;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .exercise-desc {
            font-size: 0.88rem;
            color: #94a3b8;
            margin-top: 4px;
        }

        /* Step Card */
        .step-number {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 38px;
            height: 38px;
            border-radius: 10px;
            background: rgba(99, 102, 241, 0.15);
            color: #818cf8;
            font-weight: 800;
            font-size: 1rem;
            margin-bottom: 0.8rem;
        }

        /* Section Headings */
        .section-header {
            text-align: center;
            margin-top: 4rem;
            margin-bottom: 2.5rem;
        }
        .section-title {
            font-size: 2rem;
            font-weight: 800;
            color: #f8fafc;
            margin-bottom: 0.4rem;
        }
        .section-subtitle {
            font-size: 1.05rem;
            color: #64748b;
        }
        </style>
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
            """
            <div style="
                background: linear-gradient(135deg, rgba(30, 41, 59, 0.6), rgba(15, 23, 42, 0.9));
                border: 1px solid rgba(99, 102, 241, 0.25);
                border-radius: 16px;
                padding: 1.8rem;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                height: 100%;
            ">
                <div>
                    <h3 style="color:#e2e8f0; font-size:1.25rem; font-weight:700; margin-bottom:12px;">
                        ✨ What You Get
                    </h3>
                    <ul style="color:#94a3b8; font-size:0.95rem; line-height:1.9; list-style:none; padding-left:0;">
                        <li>🎯 <strong>33-Point 3D Skeletal Tracking</strong> with MediaPipe Pose</li>
                        <li>🎙️ <strong>Instant Voice Coaching</strong> powered by Groq High-Speed LLM</li>
                        <li>📈 <strong>Auto Rep & Depth Counters</strong> with zero wearables</li>
                        <li>🔒 <strong>100% Client-Side Privacy</strong> — your camera feed is never stored</li>
                        <li>💾 <strong>Progress History Log</strong> automatically saved to your profile</li>
                    </ul>
                </div>
                <div style="font-size:0.82rem; color:#64748b; margin-top:12px; border-top:1px solid rgba(255,255,255,0.06); padding-top:10px;">
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
                    Automated concentric & eccentric phase analysis ensures only complete, valid reps are counted toward your workout targets.
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