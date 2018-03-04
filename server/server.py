import asyncio
import websockets

connected = []
bits = []
async def handler(websocket, path):
    global connected
    # Register.
    clientId = len(connected)
    bits.append(False)
    connected.append(websocket)
    try:
        # Implement logic here.
        while True:
            mssg = await websocket.recv()
            if (mssg == "true"):
                #print("{} True".format(clientId))
                bits[clientId] = True
            else:
                #print("{} False".format(clientId))
                bits[clientId] = False
            #await asyncio.wait([ws.send("Hello!") for ws in connected])
    except:
        # Unregister.
        connected.remove(websocket)

async def update():
    while True:
        print("Update")
        bit = False
        for b in bits:
            if (b):
                bit = True
                break
        for ws in connected:
            await ws.send(str(bit).lower())
        await asyncio.sleep(0.1)

start_server = websockets.serve(handler, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.async(update())
asyncio.get_event_loop().run_forever()
