import time
import json
import streamlit as st


def init_analytics_state():
    """Initializes session state tracking for workout analytics."""
    if "analytics_active" not in st.session_state:
        st.session_state.analytics_active = False
    if "workout_start_ts" not in st.session_state:
        st.session_state.workout_start_ts = None
    if "workout_end_ts" not in st.session_state:
        st.session_state.workout_end_ts = None
    if "rep_flaws_log" not in st.session_state:
        st.session_state.rep_flaws_log = []  # List of {"rep": n, "issue": str, "timestamp": float}
    if "current_rep_pending_issues" not in st.session_state:
        st.session_state.current_rep_pending_issues = set()
    if "last_tracked_reps" not in st.session_state:
        st.session_state.last_tracked_reps = 0
    if "show_scorecard" not in st.session_state:
        st.session_state.show_scorecard = False
    if "last_summary" not in st.session_state:
        st.session_state.last_summary = None


def start_analytics(exercise: str, target_sets: int, reps_per_set: int):
    """Starts tracking a new workout session."""
    st.session_state.analytics_active = True
    st.session_state.workout_start_ts = time.time()
    st.session_state.workout_end_ts = None
    st.session_state.rep_flaws_log = []
    st.session_state.current_rep_pending_issues = set()
    st.session_state.last_tracked_reps = 0
    st.session_state.show_scorecard = False
    st.session_state.last_summary = None


def track_live_frame(exercise: str, metrics: dict, current_reps: int):
    """Tracks potential form flaws occurring during the current rep."""
    if not st.session_state.get("analytics_active", False):
        return

    # Check for new completed reps
    last_reps = st.session_state.get("last_tracked_reps", 0)
    if current_reps > last_reps:
        # A rep was just finished
        pending = list(st.session_state.get("current_rep_pending_issues", set()))
        if pending:
            for issue in pending:
                st.session_state.rep_flaws_log.append({
                    "rep": current_reps,
                    "issue": issue,
                    "timestamp": time.time(),
                })
        # Reset pending issues for the next upcoming rep
        st.session_state.current_rep_pending_issues = set()
        st.session_state.last_tracked_reps = current_reps

    # Detect form flaw in the current active frame
    issue = _extract_issue(exercise, metrics)
    if issue:
        st.session_state.current_rep_pending_issues.add(issue)


def _extract_issue(exercise: str, metrics: dict) -> str:
    """Helper to detect form flaw string from detector metrics."""
    if not metrics:
        return None

    if exercise == "Squats":
        depth = metrics.get("depth_status", "")
        back = metrics.get("back_angle", 180)
        if depth == "TOO HIGH":
            return "Squat depth too high (knees didn't reach 90° parallel)"
        if isinstance(back, (int, float)) and back < 125:
            return "Excessive forward torso lean during squat"

    elif exercise == "Push-ups":
        alignment = metrics.get("body_alignment", "")
        hip = metrics.get("hip_status", "")
        if hip == "SAGGING":
            return "Hip sag detected (keep core tight and spine neutral)"
        if hip == "PIKED UP":
            return "Hips raised too high (plank should form a straight diagonal)"
        if alignment == "Poor Form":
            return "Body alignment broken (sagging core or bent knees)"

    elif exercise == "Biceps Curls (Dumbbell)":
        swing = metrics.get("swing_status", "")
        shoulder = metrics.get("shoulder_status", "")
        if swing == "SWINGING":
            return "Torso momentum swing (isolate elbows against your ribs)"
        if shoulder == "ELBOW DRIFTING":
            return "Elbow flaring outward away from torso"

    elif exercise == "Shoulder Press":
        arch = metrics.get("back_arch_status", "")
        if arch == "Excessive Arch":
            return "Excessive lumbar back arch (brace glutes and abs)"

    elif exercise == "Lunges":
        balance = metrics.get("balance_status", "")
        if balance == "OFF BALANCE":
            return "Loss of balance (widen stance to hip-width)"

    return None


def finish_analytics() -> dict:
    """Finalizes analytics and returns a comprehensive workout summary."""
    st.session_state.analytics_active = False
    now = time.time()
    st.session_state.workout_end_ts = now

    start_ts = st.session_state.get("workout_start_ts", now)
    duration_sec = max(1.0, now - start_ts)

    total_reps = st.session_state.get("reps", 0)
    flaws = st.session_state.get("rep_flaws_log", [])
    
    # Identify unique flawed reps
    flawed_reps_set = {f["rep"] for f in flaws}
    flawed_reps_count = len(flawed_reps_set)
    clean_reps_count = max(0, total_reps - flawed_reps_count)

    # Cadence (seconds per rep)
    cadence = round(duration_sec / total_reps, 1) if total_reps > 0 else 0.0

    # Letter grade & Accuracy
    if total_reps == 0:
        accuracy_pct = 0.0
        grade = "N/A"
        grade_color = "#94a3b8"
        verdict = "No completed repetitions recorded in this session."
    else:
        accuracy_pct = round((clean_reps_count / total_reps) * 100, 1)
        if accuracy_pct >= 90:
            grade = "A+"
            grade_color = "#10b981"
            verdict = "Elite Form! Outstanding biomechanical consistency."
        elif accuracy_pct >= 80:
            grade = "A"
            grade_color = "#6366f1"
            verdict = "Great Execution! Minor form adjustments needed."
        elif accuracy_pct >= 68:
            grade = "B"
            grade_color = "#f59e0b"
            verdict = "Solid Effort. Watch the highlighted form cues."
        else:
            grade = "Needs Work"
            grade_color = "#f43f5e"
            verdict = "Focus on form over speed. Reduce weight or pace."

    summary = {
        "username": st.session_state.get("username", "Athlete"),
        "exercise": st.session_state.get("exercise_type", "Workout"),
        "total_reps": total_reps,
        "clean_reps": clean_reps_count,
        "flawed_reps": flawed_reps_count,
        "accuracy_pct": accuracy_pct,
        "duration_sec": int(duration_sec),
        "duration_formatted": f"{int(duration_sec // 60):02d}:{int(duration_sec % 60):02d}",
        "cadence_sec_per_rep": cadence,
        "sets_completed": st.session_state.get("sets_completed", 0),
        "target_sets": st.session_state.get("target_sets", 0),
        "grade": grade,
        "grade_color": grade_color,
        "verdict": verdict,
        "flaws": flaws,
        "completed_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now)),
    }

    st.session_state.last_summary = summary
    st.session_state.show_scorecard = True
    return summary


@st.dialog("🏆 Workout Performance Scorecard", width="large")
def render_scorecard_modal(summary: dict):
    """Renders a rich, interactive scorecard dialog."""
    if not summary:
        st.info("No workout summary found.")
        return

    total_reps = summary.get("total_reps", 0)
    acc = summary["accuracy_pct"]
    grade = summary["grade"]
    color = summary["grade_color"]
    exercise = summary["exercise"]
    verdict = summary["verdict"]

    score_display = f"{acc}%" if total_reps > 0 else "0 Reps"

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.95));
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 16px;
            padding: 1.8rem;
            text-align: center;
            margin-bottom: 1.5rem;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        ">
            <div style="font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.08em; color: #94a3b8; margin-bottom: 6px;">
                {exercise} • Session Complete
            </div>
            <div style="display: flex; align-items: center; justify-content: center; gap: 20px; margin: 10px 0;">
                <div style="
                    font-size: 3.5rem;
                    font-weight: 900;
                    color: {color};
                    line-height: 1;
                ">{score_display}</div>
                <div style="
                    background: rgba(255, 255, 255, 0.08);
                    border: 1px solid {color};
                    padding: 8px 18px;
                    border-radius: 12px;
                    font-size: 1.5rem;
                    font-weight: 800;
                    color: {color};
                ">{grade}</div>
            </div>
            <div style="font-size: 1.05rem; color: #e2e8f0; font-weight: 600; margin-top: 6px;">
                {verdict}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 4 Key Metrics Cards
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            label="🎯 Form Accuracy",
            value=f"{summary['clean_reps']} / {summary['total_reps']}",
            delta=f"{summary['accuracy_pct']}% Clean" if total_reps > 0 else "No reps logged",
        )
    with c2:
        st.metric(
            label="⏱️ Duration",
            value=summary["duration_formatted"],
            help="Total active workout duration",
        )
    with c3:
        st.metric(
            label="⚡ Cadence",
            value=f"{summary['cadence_sec_per_rep']}s" if total_reps > 0 else "N/A",
            help="Average time spent per repetition",
        )
    with c4:
        st.metric(
            label="🏋️ Sets Completed",
            value=f"{summary['sets_completed']} / {summary['target_sets']}",
        )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.divider()

    # Common Mistakes & Biomechanical Breakdown
    st.markdown("#### 🔍 Form Analysis & Common Mistakes")

    flaws = summary.get("flaws", [])
    if total_reps == 0:
        st.markdown(
            """
            <div style="
                background: rgba(148, 163, 184, 0.08);
                border-left: 4px solid #64748b;
                border-radius: 6px;
                padding: 12px 16px;
                color: #94a3b8;
                font-size: 0.95rem;
            ">
                ℹ️ <strong>No completed repetitions were detected.</strong><br>
                To analyze your biomechanics and form score, ensure your camera has a full-body view and complete at least 1 full rep.
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif flaws:
        # Group by issue type
        issue_counts = {}
        rep_map = {}
        for f in flaws:
            issue_text = f["issue"]
            rep_num = f["rep"]
            issue_counts[issue_text] = issue_counts.get(issue_text, 0) + 1
            if issue_text not in rep_map:
                rep_map[issue_text] = []
            if rep_num not in rep_map[issue_text]:
                rep_map[issue_text].append(rep_num)

        for issue_text, count in issue_counts.items():
            reps_str = ", ".join(f"#{r}" for r in sorted(rep_map[issue_text]))
            st.markdown(
                f"""
                <div style="
                    background: rgba(244, 63, 94, 0.08);
                    border-left: 4px solid #f43f5e;
                    border-radius: 6px;
                    padding: 10px 14px;
                    margin-bottom: 8px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                ">
                    <div>
                        <strong style="color:#fecdd3;">⚠️ {issue_text}</strong>
                        <div style="font-size:0.85rem; color:#94a3b8; margin-top:3px;">
                            Flagged on Rep(s): <span style="color:#f43f5e; font-weight:600;">{reps_str}</span>
                        </div>
                    </div>
                    <span style="
                        background: rgba(244, 63, 94, 0.2);
                        color: #f43f5e;
                        padding: 3px 9px;
                        border-radius: 999px;
                        font-size: 0.8rem;
                        font-weight: 700;
                    ">{count}x</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            """
            <div style="
                background: rgba(16, 185, 129, 0.1);
                border-left: 4px solid #10b981;
                border-radius: 6px;
                padding: 12px 16px;
                color: #a7f3d0;
                font-weight: 500;
            ">
                🌟 <strong>Flawless Execution!</strong> Every single rep maintained proper joint angles, range of motion, and posture stability.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    st.divider()

    # Action / Download Buttons
    col_dl, col_close = st.columns([1, 1], gap="medium")

    with col_dl:
        json_report = json.dumps(summary, indent=2)
        filename = f"gym_coach_{summary['exercise'].lower().replace(' ', '_')}_{int(time.time())}.json"
        st.download_button(
            label="📥 Download JSON Report",
            data=json_report,
            file_name=filename,
            mime="application/json",
            use_container_width=True,
        )

    with col_close:
        if st.button("Start Next Workout ➔", use_container_width=True, type="primary"):
            st.session_state.show_scorecard = False
            st.rerun()
