

from app.ai.models.faster_whisper import faster_whisper_model
from app.utils.connection_manager import ConnectionManager
from app.utils.logging import AppLogger
from fastapi import WebSocket


class TranscriptionConnectionManager(ConnectionManager):
    """
    Transcription Connection Manager
    """

manager = TranscriptionConnectionManager()

logger = AppLogger().get_logger()

configuration = {
    "language": "en",
    "chunk_length_ms": 500,
    "language_probability_threshold": 0.65,
}

async def transcription_websocket(websocket: WebSocket):
    logger.info("Hello")
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            if data["type"] == "config":
                configuration.update(data["data"])
            if data['type'] == 'audio':
                segments, info = faster_whisper_model.transcribe_from_blobs(blobs=data['data'], cfg=configuration)
                if configuration['language'] == "auto" and info.language_probability >= configuration['language_probability_threshold'] and len(segments) > 0:
                    configuration['language'] = info.language
                    await websocket.send_json({
                        "type": "language",
                        "data": info.language
                    })
                else:
                    words = []
                    for segment in segments:
                        for word in segment.words:
                            chunk_number = (word.end * 1000) // configuration["chunk_length_ms"]
                            is_edge = False
                            if chunk_number *  configuration["chunk_length_ms"] >= (word.start * 1000) and chunk_number *  configuration["chunk_length_ms"] <= (word.end * 1000):
                                is_edge = True
                            words.append({
                                "word": word.word,
                                "timestamp": [ int(word.start * 1000 + data['timestamp']), int(word.end * 1000 + data['timestamp']) ],
                                "is_good": True,
                                "chunk_num": data['chunk_start_no'] + chunk_number,
                            })
                    
                    await websocket.send_json({
                        "type": "word",
                        "data": words
                    })    
               
    except Exception as e:
        logger.error(f"Error: {e}")
        manager.disconnect(websocket)
