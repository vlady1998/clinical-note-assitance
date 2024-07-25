import app.ai.prompts as prompts
from app.ai.models.llms.norsk_llama3_8b import model as norsk_llama3_8b
from app.exceptions.http_exceptions import InternalServerErrorHTTPException
from app.exceptions.langfuse_exceptions import LangFusePromptError
from app.utils.logging import AppLogger
from fastapi import APIRouter
from pydantic import BaseModel

logger = AppLogger().get_logger()

router = APIRouter(prefix="/summarize")

class SummarizeRequestSchema(BaseModel):
    transcription: str

class SummarizeResponseSchema(BaseModel):
    summary: str

@router.post("", response_model=SummarizeResponseSchema)
async def summarize(model: SummarizeRequestSchema):
    # pass
    """
    Request:

        {
            transcription (str): Transcription that needs to be summarized
        }

    Response:

        {
            summary (str): Summary
        }
    """
    try:
        prompt = prompts.get_summarization_prompt(
            content=model.transcription,
            prompt_name="norsk-summarization-prompt"
        )
        result = await norsk_llama3_8b.invoke(prompt=prompt.prompt,
                                              langfuse_args={"name": "summarization", "prompt": prompt.langfuse_client})

    except LangFusePromptError as e:
        raise InternalServerErrorHTTPException(msg=e.message)
    finally:
        pass

    return SummarizeResponseSchema(summary=result)
