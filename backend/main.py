from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import uvicorn
import os

app = FastAPI()

class MusicRequest(BaseModel):
    link: str
    platform: str
    separateAudio: bool
    outputPath: str

class CueRequest(BaseModel):
    outputPath: str

@app.post("/api/process")
async def process_music(request: MusicRequest):
    try:
        subprocess.run([
            "python", "process_music.py",
            request.link,
            request.platform,
            "true" if request.separateAudio else "false",
            request.outputPath
        ], check=True)
        return {"message": "Music processed successfully"}
    except subprocess.CalledProcessError:
        raise HTTPException(status_code=500, detail="Failed to process music")

# @app.get("/api/check-cuegen")
# async def check_cuegen():
#     try:
#         subprocess.run(["CueGen.Console", "--version"], check=True, capture_output=True)
#         return {"isAvailable": True}
#     except subprocess.CalledProcessError:
#         return {"isAvailable": False}

# @app.get("/api/download-cuegen")
# async def download_cuegen():
#     try:
#         subprocess.run(["python", "download_cuegen.py"], check=True)
#         return {"success": True}
#     except subprocess.CalledProcessError:
#         raise HTTPException(status_code=500, detail="Failed to download CueGen")

@app.post("/api/generate-cues")
async def generate_cues(request: CueRequest):
    try:
        subprocess.run(["python", "generate_cues.py", request.outputPath], check=True)
        return {"message": "Cues generated successfully"}
    except subprocess.CalledProcessError:
        raise HTTPException(status_code=500, detail="Failed to generate cues")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))

