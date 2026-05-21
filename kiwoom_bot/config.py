from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"


def load_env_file(path: Path = ENV_FILE) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


@dataclass(frozen=True)
class Settings:
    env: str
    app_key: str
    secret_key: str
    allow_orders: bool

    @property
    def base_url(self) -> str:
        if self.env == "real":
            return "https://api.kiwoom.com"
        return "https://mockapi.kiwoom.com"

    @property
    def websocket_url(self) -> str:
        if self.env == "real":
            return "wss://api.kiwoom.com:10000/api/dostk/websocket"
        return "wss://mockapi.kiwoom.com:10000/api/dostk/websocket"


def load_settings() -> Settings:
    load_env_file()

    env = os.getenv("KIWOOM_ENV", "mock").strip().lower()
    if env not in {"mock", "real"}:
        raise ValueError("KIWOOM_ENV must be either 'mock' or 'real'.")

    app_key = os.getenv("KIWOOM_APP_KEY", "").strip()
    secret_key = os.getenv("KIWOOM_SECRET_KEY", "").strip()
    allow_orders = os.getenv("KIWOOM_ALLOW_ORDERS", "false").strip().lower() == "true"

    return Settings(
        env=env,
        app_key=app_key,
        secret_key=secret_key,
        allow_orders=allow_orders,
    )

