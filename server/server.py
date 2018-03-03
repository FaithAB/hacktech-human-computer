import asyncio
import websockets
import time

# Demo code. Keeps track of all connected websockets in connected
connected = set()
async def handler(websocket, path):
    global connected
    # Register.
    connected.add(websocket)
    try:
        # Implement logic here.
        await asyncio.wait([ws.send("Hello!") for ws in connected])
        await asyncio.sleep(10)
    finally:
        # Unregister.
        connected.remove(websocket)

bit = False # Single bit we're trying to flip
async def sender(mssg):
    global bit
    bit = not(bit)

# Handles incoming connections
async def connect(websocket, path):
    isSender = await websocket.recv()
    print("< {}".format(isSender))

    if (isSender == "true"):
        while True:
            mssg = websocket.recv()
            await sender(mssg)
    else:
        while True:
            if (bit):
                print("> {}".format("true"))
                await websocket.send("true")
            else:
                print("> {}".format("false"))
                await websocket.send("false")
            time.sleep(0.5)

start_server = websockets.serve(connect, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
