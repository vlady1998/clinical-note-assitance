class LangFusePromptError(Exception):
    """Prompt not exist in langfuse"""
    def __init__(self, prompt_name: str):
        self.message = f"""
        Can't find prompt.
        Check if your LangFuse credentials are correct, {prompt_name} prompt exists and you passed all the variables in {prompt_name} prompt template.
        """