import os
import json
import logging
import urllib.request
import streamlit as st

logger = logging.getLogger(__name__)

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


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_metered_ice_servers(app_name: str, api_key: str):
    """
    Fetches real-time ICE servers directly from Metered API.
    """
    try:
        url = f"https://{app_name}.metered.live/api/v1/turn/credentials?apiKey={api_key}"
        req = urllib.request.Request(url, headers={"User-Agent": "Streamlit-WebRTC"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode())
                if isinstance(data, list) and len(data) > 0:
                    return data
    except Exception as e:
        logger.warning(f"Could not fetch Metered credentials via API: {e}")
    return None


def get_rtc_configuration():
    """
    Returns WebRTC configuration with STUN and TURN servers.
    Supports Metered API Key or manual credentials from Streamlit Secrets or Environment Variables.
    """
    # 1. Check for Metered API Key (simplest setup)
    metered_api_key = None
    metered_app_name = "ai-gym-coach-app"

    if hasattr(st, "secrets"):
        if "METERED_API_KEY" in st.secrets:
            metered_api_key = st.secrets["METERED_API_KEY"]
        elif "metered" in st.secrets and "api_key" in st.secrets["metered"]:
            metered_api_key = st.secrets["metered"]["api_key"]
            metered_app_name = st.secrets["metered"].get("app_name", metered_app_name)
        elif "webrtc" in st.secrets and "metered_api_key" in st.secrets["webrtc"]:
            metered_api_key = st.secrets["webrtc"]["metered_api_key"]
            metered_app_name = st.secrets["webrtc"].get("app_name", metered_app_name)

        if "METERED_APP_NAME" in st.secrets:
            metered_app_name = st.secrets["METERED_APP_NAME"]

    if not metered_api_key:
        metered_api_key = os.environ.get("METERED_API_KEY")
        metered_app_name = os.environ.get("METERED_APP_NAME", metered_app_name)

    if metered_api_key:
        servers = fetch_metered_ice_servers(metered_app_name, metered_api_key)
        if servers:
            return {"iceServers": servers}

    # 2. Check for manual TURN credentials in Streamlit secrets
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

    # 3. Check for manual TURN credentials in environment variables
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
