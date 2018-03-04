import asyncio
import websockets

# Actually handles incoming connections
connected = set()
async def handler(websocket, path):
    global connected
    # Register.
    connected.add(websocket)
    print("Connected: {}".format(len(connected)))
    #try:
    #    # Implement logic here.
    #    await asyncio.wait([ws.send("Hello!") for ws in connected])
    #    await asyncio.sleep(1)
    #finally:
    #    # Unregister.
    #    connected.remove(websocket)
    #    print("Connected: {}".format(len(connected)))

bit = False # Single bit we're trying to flip
async def update():
    global connected
    disconnected = set()
    while True:
        print("Update: {}".format(len(connected)))
        for ws in connected:
            try:
                mssg = await ws.recv()
                await ws.send(str(bit))
            except Exception as e:
                print(e)
                disconnected.add(ws)
        for ws in disconnected:
            connected.remove(ws)
            print("Connected: {}".format(len(connected)))
        await asyncio.sleep(1)

start_server = websockets.serve(handler, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.async(update())
asyncio.get_event_loop().run_forever()
