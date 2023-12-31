import io
import uvicorn
import yaml
import functools
from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse
from fastapi.responses import Response
from threading import Event
from PingMonitoning import PingMonThread


from data_model import TelegramChatData

app = FastAPI()

events_hashmap = {}


@app.get('/openapi.yaml', include_in_schema=False)
@functools.lru_cache()
def read_openapi_yaml():
    openapi_json= app.openapi()
    yaml_s = io.StringIO()
    yaml.dump(openapi_json, yaml_s)
    return Response(yaml_s.getvalue(), media_type='text/yaml')


@app.post("/AddTelegram")
async def add_telegram(item: TelegramChatData):
    event = Event()
    if item.tool == "ping":
        thread = PingMonThread(item.token, item.chat_id, item.ip_address, event)
        thread.start()
        events_hashmap[thread.ident] = event
    else:
        raise HTTPException(status_code=404, detail=  "tool == %  is not supported".format(item.tool))

    events_hashmap[thread.ident] = event

    return JSONResponse( {"id":  thread.ident} )

@app.post("/DelTelegram")
async def del_telegram(item: int):

    if item in events_hashmap:
        event = events_hashmap[item]
        event.set()
    else:
        raise HTTPException(status_code=404, detail="Item not found")

    return JSONResponse( {"id": item} )



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8500)
