import io
import uvicorn
import yaml
import functools
from fastapi import FastAPI
from starlette.responses import JSONResponse
from fastapi.responses import Response


from data_model import TelegramChatData

app = FastAPI()


@app.get('/openapi.yaml', include_in_schema=False)
@functools.lru_cache()
def read_openapi_yaml():
    openapi_json= app.openapi()
    yaml_s = io.StringIO()
    yaml.dump(openapi_json, yaml_s)
    return Response(yaml_s.getvalue(), media_type='text/yaml')


@app.post("/AddTelegram")
async def add_telegram(item: TelegramChatData):
    return JSONResponse( {"res": 0} )



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8500)
