from http.client import HTTPException
import os
from fastapi import APIRouter, FastAPI, WebSocket, Request, Depends, HTTPException, WebSocketDisconnect
import uuid
from src.socket.connection import ConnectionManager
from src.socket.utils import get_token

chat = APIRouter()

manager = ConnectionManager()

# @route   Websocket /chat
# @desc    Socket for chatbot
# @access  Public
@chat.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket, token: str = Depends(get_token)):
    await manager.connect(websocket) #Add the WebSocket to the connection manager

    #Then run a while True loop to ensure that the socket stays open
    try:
        while True:
            data = await websocket.receive_text() # While connection is open, we receive messages sent by client with receive_text and print to terminal for now
            print(data)
            await manager.send_personal_message(f"Response: Simulating response from the GPT service", websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
# @route   POST /token
# @desc    Route to generate chat token
# @access  Public
@chat.post("/token")
async def token_generator(name: str, request: Request):
    # We check here that client provides a name and it's not empty then generate a token using uuid4
    if name == "":
        raise HTTPException(status_code=400, detail={
            "loc": "name", 
            "msg": "Enter a valid name"
        })
    token = str(uuid.uuid4())
    # Session data is simple dictionary for the name and token
    data = {
        "name": name, 
        "token": token
        }

    return data

# @route   POST /refresh_token
# @desc    Route to refresh token
# @access  Public
@chat.post("/refresh_token")
async def refresh_token(request: Request):
    return None


