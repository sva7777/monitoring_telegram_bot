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


from data_model import TelegramChatData

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


@app.post("/AddTelegram")
async def add_telegram(item: TelegramChatData):
    event = Event()

    for t in threads_hashmap.values():
        if (
            item.ip_address == t.ip_address
            and item.tool == t.tool
            and item.chat_id == t.chat_id
        ):
            raise HTTPException(
                status_code=422,
                detail="Duplicate( equal ip_address, chat_id, tool) request",
            )

    if item.tool == "ping":
        thread = PingMonThread(item.token, item.chat_id, item.ip_address, event)
        thread.start()

        thread_info = ThreadInfo(
            event=event,
            chat_id=item.chat_id,
            ip_address=item.ip_address,
            tool=item.tool,
        )

        threads_hashmap[thread.ident] = thread_info
    else:
        raise HTTPException(
            status_code=404, detail="tool == %  is not supported".format(item.tool)
        )

    return JSONResponse({"id": thread.ident})


@app.post("/DelTelegram")
async def del_telegram(item: int):
    if item in threads_hashmap:
        thread_info = threads_hashmap[item]
        thread_info.event.set()
    else:
        raise HTTPException(status_code=404, detail="Item not found")

    return JSONResponse({"id": item})


@app.post("/ListTelegram")
async def list_telegram():
    res = []

    for key, item in threads_hashmap.items():
        d = item.getDictionary(key)
        res.append(d)

    return JSONResponse(res)


@click.command()
@click.argument("port",required=False, default=8500)
def main(port):
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()