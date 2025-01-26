import asyncio
import json
import shutil

import aiofiles
import docker
import vt
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from src.utils.utils import get_path_to_usb_drive, test_generator
from src.models.models import FileModel
from src.config import PATH_TO_VOLUME, VT_KEY


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
async def dynamic_analyze(file_for_analyze: FileModel):
    path = file_for_analyze.path_to_file

    shutil.copy(path, PATH_TO_VOLUME)

    docker_client = docker.from_env()
    container = docker_client.containers.run(
        "ubuntu-dynamic",
        detach=True,
        ports={"22/tcp": 2222},
        volumes={PATH_TO_VOLUME: {'bind': '/home/dockeruser/to_test', 'mode': 'rw'}}
    )

    await asyncio.sleep(30)
    shutil.rmtree(PATH_TO_VOLUME)
    container.stop()
    container.remove()


@app.post("/static_analyze")
async def static_analyze(file_for_analyze: FileModel) -> str:
    client = vt.Client(VT_KEY)
    with open(file_for_analyze.path_to_file, "rb") as file:
        analysis = await client.scan_file_async(file, wait_for_completion=True)
    await client.close_async()

    if analysis.stats.get('malicious') + analysis.stats.get('suspicious') > analysis.stats.get('harmless') + analysis.stats.get('undetected'):
        return "По итогам статического анализа файл считается вредоносным"
    return "Статический анализ файла не выявил угроз"


@app.get("/logs_stream")
async def logs_stream():
    return StreamingResponse(test_generator(), media_type="text/event-stream")
