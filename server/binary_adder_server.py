import asyncio
import websockets
import json

a = [0, 0, 1]
b = [1, 0, 1]
c = [0, 0, 0]
s0 = [1, 1, 0]
s = [0, 0, 0]
connected = []
bits = []
async def handler(websocket, path):
    global connected
    # Register.
    clientId = len(connected)
    connected.append(websocket)
    try:
        # Implement logic here.
        while True:
            mssg = await websocket.recv()
            obj = json.loads(mssg)
            s[clientId] = obj["s"]
            c[clientId] = obj["c"]
            #await asyncio.wait([ws.send("Hello!") for ws in connected])
    except Exception as e:
        # Unregister.
        print(e)
        connected.remove(websocket)

async def update():
    while True:
        print("Update {}".format(len(connected)))
        print(s)
        for i in range(0, len(connected)):
            carry = (c[i-1], 0)[i==0]
            mssg = json.dumps({ "a":a[i], "b":b[i], "c":carry })
            await connected[i].send(mssg)
        await asyncio.sleep(0.5)

start_server = websockets.serve(handler, 'localhost', 8767)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.async(update())
asyncio.get_event_loop().run_forever()
