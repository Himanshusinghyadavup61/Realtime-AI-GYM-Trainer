import os
import streamlit as st

DEFAULT_ICE_SERVERS = [
    {
        "urls": [
            "stun:stun.l.google.com:19302",
            "stun:stun1.l.google.com:19302",
            "stun:stun2.l.google.com:19302",
            "stun:stun3.l.google.com:19302",
            "stun:stun4.l.google.com:19302",
        ]
    },
    {
        "urls": "turn:openrelay.metered.ca:80",
        "username": "openrelayproject",
        "credential": "openrelayproject",
    },
    {
        "urls": "turn:openrelay.metered.ca:443",
        "username": "openrelayproject",
        "credential": "openrelayproject",
    },
    {
        "urls": "turn:openrelay.metered.ca:443?transport=tcp",
        "username": "openrelayproject",
        "credential": "openrelayproject",
    },
]


def get_rtc_configuration():
    """
    Returns WebRTC configuration with STUN and TURN servers.
    Can be customized via Streamlit secrets or environment variables:
    
    Option A (Streamlit secrets):
        [webrtc]
        turn_server = "turn:relay.metered.ca:443"
        turn_username = "your-user"
        turn_credential = "your-password"
        
    Option B (Environment variables):
        TURN_SERVER=turn:relay.metered.ca:443
        TURN_USERNAME=your-user
        TURN_CREDENTIAL=your-password
    """
    # Check Streamlit secrets
    if hasattr(st, "secrets"):
        if "rtc_configuration" in st.secrets:
            return dict(st.secrets["rtc_configuration"])
        if "ice_servers" in st.secrets:
            return {"iceServers": list(st.secrets["ice_servers"])}
        if "webrtc" in st.secrets:
            sec = st.secrets["webrtc"]
            ts = sec.get("turn_server")
            tu = sec.get("turn_username")
            tc = sec.get("turn_credential")
            if ts and tu and tc:
                return {
                    "iceServers": [
                        {
                            "urls": [
                                "stun:stun.l.google.com:19302",
                                "stun:stun1.l.google.com:19302",
                            ]
                        },
                        {"urls": ts, "username": tu, "credential": tc},
                        {"urls": f"{ts}?transport=tcp", "username": tu, "credential": tc},
                    ]
                }

    # Check environment variables
    ts = os.environ.get("TURN_SERVER")
    tu = os.environ.get("TURN_USERNAME")
    tc = os.environ.get("TURN_CREDENTIAL")
    if ts and tu and tc:
        return {
            "iceServers": [
                {
                    "urls": [
                        "stun:stun.l.google.com:19302",
                        "stun:stun1.l.google.com:19302",
                    ]
                },
                {"urls": ts, "username": tu, "credential": tc},
                {"urls": f"{ts}?transport=tcp", "username": tu, "credential": tc},
            ]
        }

    return {"iceServers": DEFAULT_ICE_SERVERS}
