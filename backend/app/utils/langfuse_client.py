from app.config import settings
from app.utils.logging import AppLogger
from langfuse import Langfuse

logger = AppLogger().get_logger()

class LangFuseClient:
    """
    A client to interact with the LangFuse service.

    Attributes:
        client (Langfuse): An instance of the Langfuse

    Example:
        >>> client = LangFuseClient()
        >>> # Using custom configuration
        >>> custom_cfg = {
        >>>     "secret_key": "my_secret_key",
        >>>     "public_key": "my_public_key",
        >>>     "host": "https://lanfuse.getara.ai"
        >>> }
        >>> client = LangFuseClient(cfg=custom_cfg)
    """

    client = None

    def __init__(self, cfg = None):
        """
        Initializes the langfuse client instance with the given credentials.

        Parameters:

             cfg (dict, optional): A dictionary containing optional configuration settings.
                                  Expected keys in the dictionary include 'secret_key',
                                  'public_key', and 'host'. These settings will override the
                                  default values obtained from the settings module if provided.
                                  If 'cfg' is not specified or is None, the client will use
                                  the default configuration from the environment variables.
        """
        if cfg is None:
            cfg = {}
        default_cfg = {
            "secret_key": settings.langfuse_secret_key,
            "public_key": settings.langfuse_public_key,
            "host": settings.langfuse_host
        }
        final_cfg = {**default_cfg, **cfg}
        self.client  = Langfuse(**final_cfg)
