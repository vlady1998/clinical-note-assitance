from typing import Tuple

from pydantic import BaseModel, model_validator

class TranscriptionConfigSchema(BaseModel):
    language: str = "en"

class TranscriptionRequestSchema(BaseModel):
    blob: str
    config: TranscriptionConfigSchema

class TranscriptionWordSchema(BaseModel):
    word: str
    timestamp: Tuple[int, int]