import app.constants as constants
from app.ai.models.llms.llm import LLM
from app.utils.logging import AppLogger
from langfuse.decorators import langfuse_context
from langfuse.decorators import observe

logger = AppLogger().get_logger()

class NorskLlama38b(LLM):

    def __init__(self):
        self.model_id = constants.NORSK_LLAMA3_MODEL
        pass

    @observe(as_type="generation", capture_input=False, capture_output=False)
    async def invoke(self, prompt: str, cfg=None, langfuse_args: dict | None = None):
        """
        Parameters:
            prompt (str): prompt
            cfg (optional[dict]): A dictionary containing configuration settings for text generation. The default configuration includes temperature, max_new_tokens, and top_p parameters. If None, default configuration is used.
            langfuse_args(optional[dict]): A dictionary containing configuration settings for langfuse. For available properties, check langfuse_context.update_current_observation(). "model", "model_parameters", "input", "output" will be ignored.
        """
        if not self.pipeline:
            logger.error("Piepeline is not loaded yet")

        if not cfg:
            cfg = {}
        default_cfg = {
            "temperature": 0.6,
            "max_new_tokens": 1000,
            "top_p": 0.9
        }
        final_cfg = {**default_cfg, **cfg}

        input_ids = self.pipeline.tokenizer(prompt, return_tensors="pt").input_ids.to(self.pipeline.model.device)

        outputs = self.pipeline.model.generate(
            input_ids,
            eos_token_id=self.pipeline.tokenizer.eos_token_id,
            do_sample=True,
            **final_cfg
        )
        response = self.pipeline.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # langfuse integration

        if not langfuse_args:
            langfuse_args = {}

        langfuse_args["model"] = constants.NORSK_LLAMA3_MODEL
        langfuse_args["model_parameters"] = final_cfg
        langfuse_args["input"] = prompt
        langfuse_args["output"] = response[len(prompt):]

        langfuse_context.update_current_observation(**langfuse_args)
        return response[len(prompt):]

logger.info("Norsk model loading...")

model = NorskLlama38b()
model.load_pipeline()

logger.info("Norsk model loaded...")
