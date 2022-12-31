import asyncio
import websockets,datetime
# 接收客户端消息并处理，这里只是简单把客户端发来的返回回去
async def recv_msg(websocket):
    counter = 0
    while True:
        recv_text = await websocket.recv()
        with open('/sdcard/Venter/EasyWeb/Projects/'+str(datetime.datetime.now())+'.html','w') as code:
            code.write(recv_text)
            
        await websocket.send('已接收！')

# websocket和path是该函数被回调时自动传过来的，不需要自己传
async def main_logic(websocket, path):
    await recv_msg(websocket)

async def main():
    async with websockets.serve(main_logic, '10.2.120.128', 32333):
        await asyncio.Future()

asyncio.run(main())