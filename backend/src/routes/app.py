import json
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from src.utils.utils import get_path_to_usb_drive, test_generator
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/directory")
async def directory():
    return Response(
        content=json.dumps(get_path_to_usb_drive()),
    )


@app.post("/dynamic_analyze")
def dynamic_analyze():
    pass


@app.get("/logs_stream")
async def logs_stream():
    return StreamingResponse(test_generator(), media_type="text/event-stream")
