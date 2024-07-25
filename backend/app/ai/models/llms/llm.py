from typing import List, Optional

import torch
import transformers
from app.utils.logging import AppLogger
from pydantic import BaseModel

logger = AppLogger().get_logger()

class LLMMessage(BaseModel):
    """
    LLM model message schema
    """
    role: str
    content: str

class LLM:
    """
    A class representing a Language Model (LLM) for text generation tasks,
    utilizing transformer pipelines for advanced natural language processing.

    Attributes:
        model_id (str): Identifier for the pre-trained model to be used. Default is "meta-llama/Meta-Llama-3-8B-Instruct".
        access_token (str): Access token required for authenticating with the model hosting service.
        pipeline (transformers.Pipeline): The loaded transformer pipeline for text generation.

    Methods:
        load_pipeline(): Configures and loads the transformer pipeline with the specified model.
        invoke(messages, cfg): Generates text based on the input messages using the pre-loaded pipeline with an optional configuration.

    Example:
        >>> llm = LLM(access_token="your_access_token_here")
        >>> llm.load_pipeline()
        >>> response = await llm.invoke([LLMMessage(prompt="Tell me a story about a wizard")])
        >>> print(response)
    """

    model_id: str = ""
    access_token: str = ""
    pipeline = None

    def __init__(self, model_id: Optional[str] = None, access_token: str = ""):
        """
        Initializes the LLM instance with the given model ID and access token.

        Parameters:
            model_id (str): Identifier for the pre-trained model to be used for text generation. Default is "meta-llama/Meta-Llama-3-8B-Instruct".
            access_token (str): Access token for using the model hosting service. Must be provided by the user.
        """
        self.access_token = access_token
        if not model_id:
            self.model_id = model_id

    def load_pipeline(self):
        """
        Configures and initiates loading of the text generation pipeline, which includes the model and tokenizer, with specified device allocation.
        """
        self.pipeline = transformers.pipeline(
            "text-generation",
            model=self.model_id,
            token=self.access_token,
            model_kwargs={"torch_dtype": torch.bfloat16, "low_cpu_mem_usage": True},
            device_map="auto"
        )

    async def invoke(self, messages: List[LLMMessage], cfg=None):
        """
        Generates responses from the language model based on the input messages using the configured pipeline, with an optional configuration.

        Parameters:
            messages (List[LLMMessage]): A list of LLMMessage objects containing the prompts for the model.
            cfg (dict, optional): A dictionary containing configuration settings for text generation. The default configuration includes temperature, max_new_tokens, and top_p parameters. If None, default configuration is used.

        Returns:
            str: The generated text that follows the input prompt(s).
        """

        if not self.pipeline:
            logger.error("Piepeline is not loaded yet")

        if cfg is None:
            cfg = {}

        default_cfg = {
            "temperature": 0.6,
            "max_new_tokens": 1000,
            "top_p": 0.9
        }
        final_cfg = {**default_cfg, **cfg}

        prompt = self.pipeline.tokenizer.apply_chat_template(
                [{ "role": message.role, "content": message.content } for message in messages],
                tokenize=False,
                add_generation_prompt=True
        )

        terminators = [
            self.pipeline.tokenizer.eos_token_id,
            self.pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]

        outputs = self.pipeline(
            prompt,
            eos_token_id=terminators,
            do_sample=True,
            pad_token_id=self.pipeline.tokenizer.eos_token_id,
            **final_cfg
        )

        return outputs[0]["generated_text"][len(prompt):]
