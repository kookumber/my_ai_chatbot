from fastapi import WebSocket, status, Query
from typing import Optional

# Function receives WebSocket and token then checks if the token is None or null
# If so, returns a policy violation status and else just returns the token
async def get_token(websocket: WebSocket, token: Optional[str] = Query(None)):
    if token is None or token == "":
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    return token