from datetime import datetime
from turtle import st
from pydantic import BaseModel
from typing import List, Optional
import uuid

# Pydantic's BaseModel class is used to model the chat data

# Messages sent and received within the Chat class are stored within the Message class
class Message(BaseModel):
    id = uuid.uuid4()
    msg: str
    timestamp = str(datetime.now())


# Chat class holds data about a single Chat session
class Chat(BaseModel):
    token: str
    messages: List[Message]
    name: str
    session_start = str(datetime.now())