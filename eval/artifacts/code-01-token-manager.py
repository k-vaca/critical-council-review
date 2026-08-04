# auth/token_manager.py
#
# Holds the service access token for the outbound API clients and refreshes
# it shortly before expiry. The worker pool runs 16 threads and they all
# share a single TokenManager instance created at process start.
#
# The identity provider issues one active token per client_id: when a new
# token is issued, any previously issued token for that client_id stops
# working immediately.

import time
import requests

TOKEN_URL = "https://api.example.com/oauth/token"
REFRESH_SKEW = 30


class TokenManager:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self._token = None
        self._expires_at = 0

    def get_token(self):
        if self._token is None or time.time() > self._expires_at - REFRESH_SKEW:
            self._refresh()
        return self._token

    def _refresh(self):
        for attempt in range(5):
            try:
                resp = requests.post(
                    TOKEN_URL,
                    data={
                        "grant_type": "client_credentials",
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                    },
                    timeout=10,
                )
                if resp.status_code == 200:
                    body = resp.json()
                    self._token = body["access_token"]
                    self._expires_at = time.time() + body["expires_in"]
                    return
                time.sleep(2 ** attempt)
            except:
                time.sleep(2 ** attempt)
        raise RuntimeError("could not refresh token")
