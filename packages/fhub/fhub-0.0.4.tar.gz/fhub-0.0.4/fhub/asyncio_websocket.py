import aiohttp
import asyncio
import json

async def main(on_tick):
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('wss://ws.finnhub.io?token=bqi6c5frh5rbubolumn0') as ws:
            await ws.send_json({"type": "subscribe", "symbol": "BINANCE:BTCUSDT"})
            async for msg in ws:

                if msg.type == aiohttp.WSMsgType.TEXT:
                    if msg.data == 'close cmd':
                        await ws.close()
                        break
                    else:
                        await on_tick(msg)
                elif msg.type == aiohttp.WSMsgType.PING:
                    ws.pong()
                elif msg.type == aiohttp.WSMsgType.CLOSE:
                    await ws.close()

                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break

async def mostrar(msg):
    global data
    # print(msg.data)
    _json = json.loads(msg.data)
    if 'data' in _json.keys():
        print(_json['data'])
        data  += _json['data']
    else:
        print(f'Otro : {_json}')

    return

def get_ticks(on_tick):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(on_tick))
    return data

if __name__ == '__main__':
    data = []
    get_ticks(on_tick=mostrar)
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main(mostrar))
    print('aya bamos')
