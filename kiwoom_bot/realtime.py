from __future__ import annotations

import asyncio
import json

from .client import KiwoomClient
from .config import load_settings


async def connect_realtime() -> None:
    try:
        import websockets
    except ImportError as error:
        raise RuntimeError("Install dependencies first: pip install -r requirements.txt") from error

    settings = load_settings()
    client = KiwoomClient(settings)
    token = client.load_token()

    async with websockets.connect(settings.websocket_url) as websocket:
        await websocket.send(json.dumps({"trnm": "LOGIN", "token": token}))
        async for message in websocket:
            print(message)


if __name__ == "__main__":
    asyncio.run(connect_realtime())

