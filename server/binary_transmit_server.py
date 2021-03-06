import asyncio
import signal
import websockets
import sys

from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer, SimpleSSLWebSocketServer

clients = set()
class Server(WebSocket):
    def handleMessage(self):
        for client in clients:
            if client != self:
                client.sendMessage(self.data)

    def handleConnected(self):
        clients.add(self)

    def handleClose(self):
        clients.remove(self)


server = SimpleWebSocketServer("localhost", 8766, Server) # TODO: change to domain name

def close_sig_handler(signal, frame):
    server.close()
    sys.exit()

signal.signal(signal.SIGINT, close_sig_handler)
server.serveforever()
