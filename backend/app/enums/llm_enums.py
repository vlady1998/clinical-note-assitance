from enum import Enum as PyEnum

import app.constants as constants


class LLMMessageRoleEnum(PyEnum):
    SYSTEM = constants.LLM_MESSAGE_ROLE_SYSTEM
    USER = constants.LLM_MESSAGE_ROLE_USER
    ASSISTANT = constants.LLM_MESSAGE_ROLE_ASSISTANT
