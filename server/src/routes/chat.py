from http.client import HTTPException
import os
from fastapi import APIRouter, FastAPI, WebSocket, Request, Depends, HTTPException, WebSocketDisconnect
import uuid
from src.socket.connection import ConnectionManager
from src.socket.utils import get_token
from src.redis.producer import Producer
from src.redis.config import Redis
from src.schema.chat import Chat
from rejson import Path
import time

chat = APIRouter()
manager = ConnectionManager()
redis = Redis()

# @route   Websocket /chat
# @desc    Socket for chatbot
# @access  Public
@chat.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket, token: str = Depends(get_token)):
    await manager.connect(websocket) #Add the WebSocket to the connection manager
    redis_client = await redis.create_connection()
    producer = Producer(redis_client)

    #Then run a while True loop to ensure that the socket stays open
    try:
        while True:
            data = await websocket.receive_text() # While connection is open, we receive messages sent by client with receive_text and print to terminal for now
            print(data)
            stream_data = {}
            stream_data[token] = data
            await producer.add_to_stream(stream_data, "message_channel")
            await manager.send_personal_message(f"Response: Simulating response from the GPT service", websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
# @route   POST /token
# @desc    Route to generate chat token
# @access  Public
@chat.post("/token")
async def token_generator(name: str, request: Request):
    token = str(uuid.uuid4())

    # We check here that client provides a name and it's not empty then generate a token using uuid4
    if name == "":
        raise HTTPException(status_code=400, detail={
            "loc": "name", 
            "msg": "Enter a valid name"
        })

    # Create a new chat session
    json_client = redis.create_rejson_connection()

    chat_session = Chat(
        token=token,
        messages=[],
        name=name
    )

    print(chat_session.dict())

    # Store chat session in redis JSON with the token as key
    json_client.jsonset(str(token), Path.rootPath(), chat_session.dict())

    # Set a timeout for redis data
    redis_client = await redis.create_connection()
    # We can change 3600 (60 mins) to longer timeframe. Setting at 60 mins for not since this is demo app and we don't want to store chat data in Redic for too long
    # After 60 mins, the chat session data will be lost
    await redis_client.expire(str(token), 3600)

    return chat_session.dict()

# @route   POST /refresh_token
# @desc    Route to refresh token
# @access  Public
@chat.post("/refresh_token")
async def refresh_token(request: Request):
    return None


