import asyncio
import json
import os
import shutil

import aiofiles
import docker
import vt
import paramiko
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
async def dynamic_analyze(file_for_analyze: FileModel) -> list:
    path = file_for_analyze.path_to_file

    if not os.path.exists(PATH_TO_VOLUME):
        os.mkdir(PATH_TO_VOLUME)

    shutil.copy(path, PATH_TO_VOLUME)
    filename = path.split("/")[-1]

    docker_client = docker.from_env()
    container = docker_client.containers.run(
        "ubuntu-dynamic",
        detach=True,
        ports={"22/tcp": 2222},
        volumes={PATH_TO_VOLUME: {'bind': '/home/dockeruser/to_test', 'mode': 'rw'}}
    )

    await asyncio.sleep(10)

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.WarningPolicy)
    ssh_client.connect("localhost", 2222, username="dockeruser", password="dockeruser")

    ssh_client.exec_command(f"sudo python3 ./Code/analyze.py start ./to_test/{filename}")

    await asyncio.sleep(60)

    results = []
    async with aiofiles.open(f"{PATH_TO_VOLUME}/results.txt", mode='r') as f:
        async for i in f:
            results.append(i)

    shutil.rmtree(PATH_TO_VOLUME)
    container.stop()
    container.remove()

    return results


@app.post("/static_analyze")
async def static_analyze(file_for_analyze: FileModel) -> list:
    client = vt.Client(VT_KEY)
    with open(file_for_analyze.path_to_file, "rb") as file:
        analysis = await client.scan_file_async(file, wait_for_completion=True)
    await client.close_async()

    if (analysis.stats.get('malicious') + analysis.stats.get('suspicious') >
            analysis.stats.get('harmless') + analysis.stats.get('undetected')):
        result = "\nПо итогам статического анализа файл считается вредоносным"
    else:
        result = "\nСтатический анализ файла не выявил угроз"

    analysis.stats.pop("timeout")
    analysis.stats.pop("confirmed-timeout")
    analysis.stats.pop("failure")
    analysis.stats.pop("type-unsupported")
    analysis.stats = [f'{key}: {value}' for key, value in analysis.stats.items()]
    analysis.stats.append(result)
    return analysis.stats


@app.get("/logs_stream")
async def logs_stream():
    return StreamingResponse(test_generator(), media_type="text/event-stream")
