import app.ai.prompts as prompts
from app.ai.models.llms.norsk_llama3_8b import model as norsk_llama3_8b
from app.exceptions.http_exceptions import InternalServerErrorHTTPException
from app.exceptions.langfuse_exceptions import LangFusePromptError
from app.utils.logging import AppLogger
from fastapi import APIRouter
from pydantic import BaseModel

logger = AppLogger().get_logger()

router = APIRouter(prefix="/soap")

class SoapRequestSchema(BaseModel):
    transcription: str

class SoapResponseSchema(BaseModel):
    note: str

@router.post("/subjective", response_model=SoapResponseSchema)
async def subjective(model: SoapRequestSchema):
    # pass
    """
    TODO
    """
    try:
        prompt = prompts.get_summarization_prompt(
            content=model.transcription,
            prompt_name=model.langfuse_prompt_name,
            prompt_version=model.langfuse_prompt_version
        )
        result = await norsk_llama3_8b.invoke(prompt=prompt.prompt, langfuse_args={"name": "summarization", "prompt": prompt.langfuse_client})

    except LangFusePromptError as e:
        raise InternalServerErrorHTTPException(msg=e.message)
    finally:
        pass

    return SoapResponseSchema(note=result)
