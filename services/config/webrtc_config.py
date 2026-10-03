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


def _get_secrets_obj():
    """Safely retrieves st.secrets without throwing StreamlitSecretNotFoundError."""
    try:
        if hasattr(st, "secrets") and len(st.secrets) > 0:
            return st.secrets
    except Exception:
        pass
    return None


def _get_val(dict_obj, *keys):
    """Safely retrieves first matching case-insensitive key from a dict-like object."""
    if dict_obj is None:
        return None
    try:
        for k in keys:
            if hasattr(dict_obj, "get") and dict_obj.get(k) is not None:
                return dict_obj.get(k)
        if hasattr(dict_obj, "items"):
            for existing_k, existing_v in dict_obj.items():
                for target_k in keys:
                    if existing_k.lower() == target_k.lower() and existing_v:
                        return existing_v
    except Exception:
        pass
    return None


def get_rtc_configuration():
    """
    Returns WebRTC configuration with STUN and TURN servers.
    Handles Metered API Key, direct TURN credentials (case-insensitive, with or without [webrtc] section),
    and environment variables.
    """
    secrets = _get_secrets_obj()

    # 1. Check for Metered API Key
    metered_api_key = None
    metered_app_name = "ai-gym-coach-app"

    if secrets:
        metered_api_key = _get_val(secrets, "METERED_API_KEY", "metered_api_key")
        if not metered_api_key and "webrtc" in secrets:
            metered_api_key = _get_val(secrets["webrtc"], "METERED_API_KEY", "metered_api_key")
        if not metered_api_key and "metered" in secrets:
            metered_api_key = _get_val(secrets["metered"], "api_key", "METERED_API_KEY")

        app_name_val = _get_val(secrets, "METERED_APP_NAME", "metered_app_name")
        if app_name_val:
            metered_app_name = app_name_val

    if not metered_api_key:
        metered_api_key = os.environ.get("METERED_API_KEY") or os.environ.get("metered_api_key")

    if metered_api_key:
        servers = fetch_metered_ice_servers(metered_app_name, metered_api_key)
        if servers:
            return {"iceServers": servers}

    # 2. Check for explicit turn_server / turn_username / turn_credential in secrets or environment
    ts = None
    tu = None
    tc = None

    if secrets:
        # Check top-level secrets
        ts = _get_val(secrets, "turn_server", "TURN_SERVER")
        tu = _get_val(secrets, "turn_username", "TURN_USERNAME")
        tc = _get_val(secrets, "turn_credential", "TURN_CREDENTIAL", "turn_password", "TURN_PASSWORD")

        # Check [webrtc] section
        if (not ts or not tu or not tc) and "webrtc" in secrets:
            sec = secrets["webrtc"]
            ts = ts or _get_val(sec, "turn_server", "TURN_SERVER")
            tu = tu or _get_val(sec, "turn_username", "TURN_USERNAME")
            tc = tc or _get_val(sec, "turn_credential", "TURN_CREDENTIAL", "turn_password", "TURN_PASSWORD")

    # Fallback to environment variables
    if not ts or not tu or not tc:
        ts = ts or os.environ.get("turn_server") or os.environ.get("TURN_SERVER")
        tu = tu or os.environ.get("turn_username") or os.environ.get("TURN_USERNAME")
        tc = tc or os.environ.get("turn_credential") or os.environ.get("TURN_CREDENTIAL") or os.environ.get("turn_password") or os.environ.get("TURN_PASSWORD")

    # If TURN credentials are provided, construct proper WebRTC ICE servers
    if ts and tu and tc:
        # Clean up hostname
        clean_host = ts.replace("turns:", "").replace("turn:", "").strip()
        clean_host = clean_host.split(":")[0].split("?")[0]

        return {
            "iceServers": [
                {
                    "urls": [
                        "stun:stun.l.google.com:19302",
                        "stun:stun1.l.google.com:19302",
                        f"stun:{clean_host}:80",
                    ]
                },
                {
                    "urls": f"turn:{clean_host}:80",
                    "username": tu,
                    "credential": tc,
                },
                {
                    "urls": f"turn:{clean_host}:443",
                    "username": tu,
                    "credential": tc,
                },
                {
                    "urls": f"turn:{clean_host}:443?transport=tcp",
                    "username": tu,
                    "credential": tc,
                },
            ]
        }

    return {"iceServers": DEFAULT_ICE_SERVERS}
