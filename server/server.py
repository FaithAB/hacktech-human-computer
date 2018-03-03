import asyncio
import websockets

# Actually handles incoming connections
connected = set()
async def handler(websocket, path):
    global connected
    # Register.
    connected.add(websocket)
    print("Connected: {}".format(len(connected)))
    try:
        # Implement logic here.
        await asyncio.wait([ws.send("Hello!") for ws in connected])
        await asyncio.sleep(10)
    finally:
        # Unregister.
        connected.remove(websocket)
        print("Connected: {}".format(len(connected)))

bit = False # Single bit we're trying to flip
def update():
    while True:
        print("Update")
        yield from asyncio.sleep(1)

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

start_server = websockets.serve(handler, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.async(update())
asyncio.get_event_loop().run_forever()
