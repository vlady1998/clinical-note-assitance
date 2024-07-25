import sentry_sdk
from app.routers import soap_router, summarize_router, transcription_router
from app.utils.logging import AppLogger
from app.websockets.transcription import transcription_websocket
from fastapi import FastAPI, WebSocket

sentry_sdk.init(
    dsn="https://9ad379461856a0bcbb781338621c4251@o4507148297371648.ingest.de.sentry.io/4507169618002000",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app = FastAPI()

logger = AppLogger().get_logger()
app = FastAPI(title="Ara AI", description="This is backend for Ara AI", version="0.1.0")

v1_prefix = "/api/v1"

app.include_router(soap_router.router, tags=['Journal notes'], prefix=v1_prefix)
app.include_router(summarize_router.router, tags=['Summarization'], prefix=v1_prefix)
app.include_router(transcription_router.router, tags=['Transcription'], prefix=v1_prefix)

@app.websocket("/ws/transcription")
async def transcription_websocket_endpoint(websocket: WebSocket):
    await transcription_websocket(websocket)
