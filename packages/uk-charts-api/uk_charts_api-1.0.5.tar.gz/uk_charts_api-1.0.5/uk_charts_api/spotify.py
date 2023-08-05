import base64
from typing import Dict

import requests


class Spotify:
    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.headers = self.spotify_headers(self.client_id, self.client_id)

    def spotify_headers(self, client_id: str, client_secret: str) -> Dict:
        data = {"grant_type": "client_credentials"}
        auth_code = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        headers = {"Authorization": f"Basic {auth_code}"}
        resp = requests.post("https://accounts.spotify.com/api/token", data=data, headers=headers)

        auth_token = resp.json()["access_token"]

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth_token}",
        }

        return headers

    def refresh_headers(self) -> None:
        self.headers = self.spotify_headers(self.client_id, self.client_secret)
