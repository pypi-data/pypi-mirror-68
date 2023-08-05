import requests
import os

JUNOPASS_API_BASE = os.environ.get(
    "JUNOPASS_API_BASE", "https://console.junopass.com/api/v1/")


def _authenticate_request(access_token, payload):
    """
    Send auth request to JunoPass
    Step 1 process
    """
    if not access_token:
        raise Exception("Access token is required")
    headers = {"Authorization": f"Token {access_token}"}
    api_url = f"{JUNOPASS_API_BASE}user/authenticate/"
    resp = requests.post(api_url, json=payload, headers=headers, timeout=10)
    return resp


def _verify_request(access_token, payload):
    """
    Send signed challenges and otp for verification
    """
    if not access_token:
        raise Exception("Access token is required")
    headers = {"Authorization": f"Token {access_token}"}
    api_url = f"{JUNOPASS_API_BASE}user/verify/"
    resp = requests.post(api_url, json=payload, headers=headers, timeout=10)
    return resp
