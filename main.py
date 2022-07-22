# uvicorn main:app --reload --host=0.0.0.0 --port=8003

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseSettings
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

import os

class Settings(BaseSettings):
    APP_ENV: str = 'dev'

    class Config:
        env_file = '.env'

settings = Settings(_env_file=f'{os.getenv("ENV_STATE")}.env')
app = FastAPI(middleware=[
    Middleware(CORSMiddleware, allow_origins=["*"])
], debug=True)
templates = Jinja2Templates(directory="templates/")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse('upload.html', {'request': request})

@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}

@app.post("/upload-file/")
async def create_upload_file(file: UploadFile):
    # return {"filename": file.filename}
    file_location = f"./save/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}
