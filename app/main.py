from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api import chat, upload

app = FastAPI(title="Smart AI Document Assistant API")

# Allow frontend access
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Manual OPTIONS handler (important for Next.js)
@app.options("/{rest_of_path:path}")
async def preflight_handler(request: Request, rest_of_path: str):
    return JSONResponse(
        content={"message": "CORS preflight OK"},
        headers={
            "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        },
    )

# Routers
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(upload.router, prefix="/upload", tags=["Upload"])

@app.get("/")
def root():
    return {
        "message": "📄 Smart AI Document Assistant backend is running successfully!",
    }