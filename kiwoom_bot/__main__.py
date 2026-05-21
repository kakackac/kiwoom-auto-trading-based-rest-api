from __future__ import annotations

import argparse
import json

from .client import KiwoomApiError, KiwoomClient
from .config import load_settings


def main() -> int:
    parser = argparse.ArgumentParser(description="Kiwoom REST API starter CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("doctor", help="Check local configuration")
    subparsers.add_parser("token", help="Issue and cache an access token")

    request_parser = subparsers.add_parser("request", help="Send a generic POST request")
    request_parser.add_argument("--endpoint", required=True, help="Example: /api/dostk/acnt")
    request_parser.add_argument("--api-id", required=True, help="Example: ka00001")
    request_parser.add_argument("--body", default="{}", help="JSON body")

    args = parser.parse_args()
    settings = load_settings()
    client = KiwoomClient(settings)

    try:
        if args.command == "doctor":
            print(json.dumps(
                {
                    "env": settings.env,
                    "base_url": settings.base_url,
                    "websocket_url": settings.websocket_url,
                    "has_app_key": bool(settings.app_key),
                    "has_secret_key": bool(settings.secret_key),
                    "allow_orders": settings.allow_orders,
                },
                ensure_ascii=False,
                indent=2,
            ))
            return 0

        if args.command == "token":
            token_data = client.issue_token()
            safe_data = dict(token_data)
            if "token" in safe_data:
                safe_data["token"] = safe_data["token"][:8] + "...redacted"
            print(json.dumps(safe_data, ensure_ascii=False, indent=2))
            return 0

        if args.command == "request":
            body = json.loads(args.body)
            response = client.request(args.endpoint, args.api_id, body)
            print(json.dumps(response, ensure_ascii=False, indent=2))
            return 0

    except (KiwoomApiError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

