from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
import urllib.error
import urllib.request

from .config import PROJECT_ROOT, Settings


TOKEN_FILE = PROJECT_ROOT / ".kiwoom_token.json"


class KiwoomApiError(RuntimeError):
    pass


class KiwoomClient:
    def __init__(self, settings: Settings):
        self.settings = settings

    def issue_token(self) -> dict:
        if not self.settings.app_key or not self.settings.secret_key:
            raise KiwoomApiError("Set KIWOOM_APP_KEY and KIWOOM_SECRET_KEY in .env first.")

        payload = {
            "grant_type": "client_credentials",
            "appkey": self.settings.app_key,
            "secretkey": self.settings.secret_key,
        }
        response = self._post_json("/oauth2/token", payload, api_id="au10001", with_token=False)
        token = response.get("token")
        if not token:
            raise KiwoomApiError(f"Token was not returned: {response}")

        self._save_token(response)
        return response

    def load_token(self) -> str:
        if not TOKEN_FILE.exists():
            token_data = self.issue_token()
        else:
            token_data = json.loads(TOKEN_FILE.read_text(encoding="utf-8"))

        token = token_data.get("token", "")
        if not token:
            raise KiwoomApiError("Token cache is invalid. Run `python -m kiwoom_bot token` again.")
        return token

    def request(self, endpoint: str, api_id: str, body: dict | None = None) -> dict:
        return self._post_json(endpoint, body or {}, api_id=api_id, with_token=True)

    def guarded_order(self, endpoint: str, api_id: str, body: dict) -> dict:
        if not self.settings.allow_orders:
            raise KiwoomApiError(
                "Order blocked. Set KIWOOM_ALLOW_ORDERS=true only after mock testing."
            )
        return self.request(endpoint, api_id, body)

    def _post_json(self, endpoint: str, payload: dict, api_id: str, with_token: bool) -> dict:
        url = self.settings.base_url + endpoint
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "api-id": api_id,
        }
        if with_token:
            headers["authorization"] = f"Bearer {self.load_token()}"

        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                body = response.read().decode("utf-8")
                return json.loads(body) if body else {}
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8", errors="replace")
            raise KiwoomApiError(f"HTTP {error.code}: {body}") from error
        except urllib.error.URLError as error:
            raise KiwoomApiError(f"Network error: {error.reason}") from error

    @staticmethod
    def _save_token(token_data: dict, path: Path = TOKEN_FILE) -> None:
        data = dict(token_data)
        data["saved_at"] = datetime.now().isoformat(timespec="seconds")
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

