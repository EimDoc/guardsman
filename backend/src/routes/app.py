import json
from fastapi import FastAPI, Response

from src.utils.utils import get_path_to_usb_drive
app = FastAPI()


@app.get("/directory")
async def directory():
    return Response(
        content=json.dumps(get_path_to_usb_drive()),
        headers={"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
    )


@app.post("/dynamic_analyze")
def dynamic_analyze():
    pass
