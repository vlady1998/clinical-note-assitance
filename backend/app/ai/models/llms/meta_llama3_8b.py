import app.constants as constants
from app.config import settings
from app.utils.logging import AppLogger
from backend.backend.app.ai.models.llms.llm import LLM

logger = AppLogger().get_logger()

model = LLM(access_token=settings.hugging_face_access_token, model_id=constants.META_LLAMA3_MODEL)

logger.info("Meta llama3 model loading...")
model.load_pipeline()
logger.info("Meta llama3 model loaded...")
