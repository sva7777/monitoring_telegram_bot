import io
import uvicorn
import yaml
import functools
import sys
import click
from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse
from fastapi.responses import Response
from threading import Event
from PingMonitoning import PingMonThread
from ThreadInfo import ThreadInfo
from Telegram.TgSendMessage import TgSendMessage
import asyncio
import datetime
from data_model import TelegramChatData
from data_model import Message
from Bot.base import TGCoordinator

app = FastAPI()

threads_hashmap = {}

# ToDo: Do I need idempotency support? I think no, because most of requests are gonna be local


@app.get("/openapi.yaml", include_in_schema=False)
@functools.lru_cache()
def read_openapi_yaml():
    openapi_json = app.openapi()
    yaml_s = io.StringIO()
    yaml.dump(openapi_json, yaml_s)
    return Response(yaml_s.getvalue(), media_type="text/yaml")


@app.post("/AddTelegram", responses={ 422: {"model": Message}})
async def add_telegram(item: TelegramChatData):

    for t in threads_hashmap.values():
        if (
            item.ip_address == t.ip_address
            and item.tool == t.tool
            and item.chat_id == t.chat_id
        ):
            return JSONResponse(status_code=422, content={"message": "Duplicate( equal ip_address, chat_id, tool) request" })

    if item.tool == "ping":
        event = Event()

        tg= TgSendMessage(item.token, item.chat_id, item.ip_address, event)
        thread = PingMonThread(item.ip_address, event, tg)
        thread.start()

        thread_info = ThreadInfo(
            event=event,
            chat_id=item.chat_id,
            ip_address=item.ip_address,
            tool=item.tool
        )

        threads_hashmap[thread.ident] = thread_info
    # currently only ping can be specified

    return JSONResponse({"id": thread.ident})


@app.post("/DelTelegram",  responses={404: {"model": Message} } )
async def del_telegram(item: int):
    if item in threads_hashmap:
        thread_info = threads_hashmap.pop(item)
        thread_info.event.set()

    else:
        return JSONResponse(status_code=404, content={"message": "Item not found"})

    return JSONResponse({"id": item})


@app.post("/ListTelegram")
async def list_telegram():
    res = []

    for key, item in threads_hashmap.items():
        d = item.getDictionary(key)
        res.append(d)

    return JSONResponse(res)


@click.command()
@click.argument("port", required=False, default=8500)
def main(port):
    uvicorn.run(app, host="0.0.0.0", port=port)



def run():
    loop = asyncio.get_event_loop()

    tg_coordinator = TGCoordinator("", 2)


    try:
        print('bot has been started')
        loop.create_task(tg_coordinator.start())
        loop.run_forever()
    except KeyboardInterrupt:
        print("\nstopping", datetime.datetime.now())
        loop.run_until_complete(tg_coordinator.stop())
        print('bot has been stopped', datetime.datetime.now())



if __name__ == "__main__":
    # ToDo: I run two event loop. my first event loop will block second call
    main()
    run()

