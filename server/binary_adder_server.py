import asyncio
import websockets
import json
import random

class Room:
    def __init__(self):
        self.size = 0
        self.generateNums()
        self.connected = []

    def generateNums(self):
        carry = 0
        self.a = []
        self.b = []
        self.c = []
        self.s = []
        self.s0 = []
        for i in range(0, self.size):
            self.a.append(random.randint(0,1))
            self.b.append(random.randint(0,1))
            self.s.append(0)
            self.c.append(0)
            n = self.a[i] + self.b[i] + carry
            self.s0.append((0, 1)[n == 1 or n == 3])
            carry = (0, 1)[n > 2]

    def add(self, ws):
        self.connected.append(ws)
        self.size += 1
        self.generateNums()

    def rm(self, ws):
        self.connected.remove(ws)
        self.size -= 1
        self.generateNums()

rooms = {}

connected = []
async def handler(websocket, path):
    global connected
    # Register.
    clientId = len(connected)
    room = ""
    connected.append(websocket)
    try:
        # Implement logic here.
        while True:
            mssg = await websocket.recv()
            obj = json.loads(mssg)
            if ("room" in obj):
                room = obj["room"]
                if (not(room in rooms)):
                    rooms[room] = Room()
                clientId = len(rooms[room].connected)
                rooms[room].add(websocket)
                continue

            if (room == ""):
                continue

            rooms[room].s[clientId] = obj["s"]
            rooms[room].c[clientId] = obj["c"]
            #await asyncio.wait([ws.send("Hello!") for ws in connected])
    except Exception as e:
        # Unregister.
        print(e)
        connected.remove(websocket)

async def update():
    while True:
        for r in rooms:
            rm = rooms[r]
            print("{} {} {}".format(r, rm.c, rm.s))
            for i in range(0, len(rm.connected)):
                carry = (rm.c[i-1], 0)[i==0]
                mssg = json.dumps({ "a":rm.a[i], "b":rm.b[i], "c":carry })
                await rm.connected[i].send(mssg)
        await asyncio.sleep(0.5)

start_server = websockets.serve(handler, 'localhost', 8767)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.async(update())
asyncio.get_event_loop().run_forever()
