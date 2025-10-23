# core/utils/turnstile.py
import requests
from django.conf import settings

def verify_turnstile(request):
    """
    Verify Cloudflare Turnstile response.
    Returns True if the verification succeeded, otherwise False.
    Automatically skips verification in DEBUG mode or if using test keys.
    """
    token = request.POST.get("cf-turnstile-response")

    # If there is no token, fail fast
    if not token:
        return False

    # If using test keys or running locally, skip verification
    if settings.DEBUG or settings.TURNSTILE_SITE_KEY.startswith("1x"):
        return True

    data = {
        "secret": settings.TURNSTILE_SECRET_KEY,
        "response": token,
        "remoteip": request.META.get("REMOTE_ADDR"),
    }

    try:
        resp = requests.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify", 
            data=data, 
            timeout=5
        )
        result = resp.json()
        return result.get("success", False)
    except requests.RequestException:
        return False
