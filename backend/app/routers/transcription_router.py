from typing import List
from app.ai.models.faster_whisper import faster_whisper_model
from app.schemas.transcription_schemas import TranscriptionRequestSchema, TranscriptionWordSchema
from app.utils.logging import AppLogger
from fastapi import APIRouter

logger = AppLogger().get_logger()

router = APIRouter(prefix="/transcription")

@router.post("", response_model=List[TranscriptionWordSchema])
async def transcription(model: TranscriptionRequestSchema):
    # pass
    """
    Generate Transcription using Faster-Whisper Large-V3 model
    """
    segments, info = faster_whisper_model.transcribe_from_blob(blob=model.blob, cfg=model.config)
    result = []
    for segment in segments:
        for word in segment.words:
            result.append(TranscriptionWordSchema(
                word=word.word,
                timestamp=[ int(word.start * 1000), int(word.end * 1000) ]
            ))
    return result