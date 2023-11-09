import asyncio
import json

import websockets as websockets

PORT = 8345

SS = dict(cnt=0)

async def handler(websocket):
    async for message in websocket:
        print(message)
        msg = json.loads(message)
        mtype = msg['mtype']
        period = msg['round_num']
        print(f"cnt: {SS['cnt']}")
        SS['cnt'] += 1


async def get_messages():
    async with websockets.serve(handler, "", PORT):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    try:
        asyncio.run(get_messages())
    except KeyboardInterrupt:
        print("Goodbye.")