import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from langserve import add_routes

from app.routers import (document, message, scrap_youtube, thread, transcript,
                         video, word)

app = FastAPI()

logger = logging.getLogger(__name__)

allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://linguatube.vercel.app",
    "https://linguatube.net"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def redirect_root_to_docs():
    logger.info("Root endpoint accessed")
    return RedirectResponse("/docs")

@app.get("/hello")
async def hello_world():
    return {"message": "Hello, World!"}
app.include_router(word.router)
app.include_router(video.router)
app.include_router(transcript.router)
app.include_router(scrap_youtube.router)
app.include_router(document.router)
app.include_router(thread.router)
app.include_router(message.router)

# Edit this to add the chain you want to add
# add_routes(app, word_info_chain, path="/word-info")
# add_routes(app, translation_chain, path="/translate")

if __name__ == "__main__":
    import os

    import uvicorn
    from dotenv import load_dotenv
    
    load_dotenv()

    PORT = int(os.getenv("PORT") or 8000)
    
    uvicorn.run(app, host="0.0.0.0", port=PORT)
