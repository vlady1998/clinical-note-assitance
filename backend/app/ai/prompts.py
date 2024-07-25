from typing import Optional, Any

from app.utils.langfuse_client import LangFuseClient
from app.utils.logging import AppLogger
from pydantic import BaseModel

logger = AppLogger().get_logger()

langfuse_client = LangFuseClient()

class Prompt(BaseModel):
    """
    prompt (str): final full prompt in str
    langfuse_client : langfuse prompt_client object if it is fetched from langfuse
    """
    prompt: str
    langfuse_client: Any = None

# def get_summarization_messages
def get_summarization_prompt(content: str, prompt_name: Optional[str] = None, prompt_version: Optional[int] = None) -> Prompt:
    """
    Return prompt for summarization using norsk model

    Parameters:
        content (str): Content to be summarized. It must be in Norweign
        prompt_name (optional[str]): Prompt name to be used for summarization. If not provided or can't fetch provided prompt name, it will use default prompt.

    Return:
        Prompt object
    """

    try:
        prompt = langfuse_client.client.get_prompt(
            name=prompt_name,
            version=prompt_version
        )
        
        return Prompt(
            prompt=prompt.compile(content=content),
            langfuse_client=prompt
        )
    except Exception as e:
        logger.error(f"Error while getting prompt: {e}")

        logger.info("Use default prompt for summarization")
        return Prompt(
            prompt=default_prompt.format(content=content)
        )
