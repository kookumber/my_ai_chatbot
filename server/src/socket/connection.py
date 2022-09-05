from fastapi import WebSocket

#ConnectionManager class is initialized with an active_connections attribute that is a list of active connections
class ConnectionManager: 
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    # The asyn connect method will accept a WebSocket and add it to the list of active connections
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    # The disconnect method will remove the Websocket from the list of active connections
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    # Send_personal_message method will take in a message and the websocket we want to send the message to and asynchrously send the message
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

