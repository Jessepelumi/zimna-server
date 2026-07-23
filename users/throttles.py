from rest_framework.throttling import SimpleRateThrottle

class EmailKeyedThrottle(SimpleRateThrottle):
    """
    Base throttle that rate-limits by the email in the request body, not by client IP. 
    Falls back to IP if no email is present so the endpoint is never fully unthrottled.
    """

    scope = None

    def get_cache_key(self, request, view):
        email = (request.data.get("email") or "").lower().strip()
        if not email:
            # No email supplied - throttle by IP instead
            ident = self.get_ident(request)
        else:
            ident = email

        return self.cache_format % {
            "scope": self.scope,
            "ident": ident,
        }

class OTPSendThrottle(EmailKeyedThrottle):
    """Limits how often an OTP code can be requested for one email."""
    scope = "otp_send"

class OTPVerifyThrottle(EmailKeyedThrottle):
    """Limits how much an OTP code can be checked for one email."""
    scope = "otp_verify"

class LoginThrottle(EmailKeyedThrottle):
    """Limits password login attempts per email"""
    scope = "login"
