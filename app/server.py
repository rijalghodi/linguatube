from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from packages.chains import translation_chain, word_info_chain
from fastapi.middleware.cors import CORSMiddleware
from app.routers import video, transcript, scrap_youtube, document, item
app = FastAPI()

allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
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
    return RedirectResponse("/docs")

@app.get("/hello")
async def hello_world():
    return {"message": "Hello, World!"}
app.include_router(video.router)
app.include_router(transcript.router)
app.include_router(scrap_youtube.router)
app.include_router(item.router)
app.include_router(document.router)

# Edit this to add the chain you want to add
add_routes(app, word_info_chain, path="/word-info")
add_routes(app, translation_chain, path="/translate")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
