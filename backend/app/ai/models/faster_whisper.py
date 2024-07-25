import base64
import tempfile
import io
from pydub import AudioSegment
from typing import List
from faster_whisper import WhisperModel

class FasterWhisperModel:
    """
    A class for transcribing audio files using a pretrained Whisper model,
    with support for various model sizes and configurations.

    Attributes:
        model_size (str): Size of the Whisper model to be loaded. Default is "large-v3".
        device (str): The device type ('cuda' or 'cpu') on which the model will operate.
        compute_type (str): The precision ('float16' or 'float32') for computation.
        model (WhisperModel): The loaded Whisper model object, ready for transcriptions.

    Methods:
        load_model(): Loads the Whisper model based on the initialization parameters.
        transcribe(path, cfg): Transcribes the audio file at the given path using the specified or default configuration.
    """

    def __init__(self, model_size: str = "large-v3", device="cuda", compute_type="float16"):
        """
        Initializes the FasterWhisperModel instance by setting up the model configuration
        and loading the Whisper model.

        Parameters:
            model_size (str): The size of the Whisper model to load. Default is "large-v3".
            device (str): The computation device ('cuda' or 'cpu'). Default is 'cuda'.
            compute_type (str): The precision of computation ('float16' or 'float32'). Default is 'float16'.
        """
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.load_model()

    def load_model(self):
        """ Loads the Whisper model based on the initialized parameters. """
        self.model = WhisperModel(self.model_size, device=self.device, compute_type=self.compute_type)

    def transcribe_from_blobs(self, blobs: List[str] | None, cfg=None):
        """
        Transcribes an audio file from list of blobs by concatenating blobs into one.

        Parameters:
            blob (List[str]): List of base64 encoded blob bytes
            cfg (Optional[dict]):  A dictionary containing configuration settings that overwrite default settings. For more information, check `transcribe_from_file` documentation.

        Returns:
            tuple: Returns a tuple containing the segmentation data and metadata about the transcription. For more information, check `transcribe_from_file` documentation.
        """

        # Start with an empty audio segment
        combined_audio = AudioSegment.silent(duration=0)
        
        # Decode and load each blob into pydub's AudioSegment and concatenate
        for base64_blob in blobs:
            # Decode base64 string to bytes
            audio_bytes = base64.b64decode(base64_blob)
            
            # Create an AudioSegment from these bytes
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format="wav")
            
            # Concatenate audio segments
            combined_audio += audio_segment

        # Create a temporary file to save the concatenated audio so it can be read by another process or function
        with tempfile.NamedTemporaryFile(suffix='.wav') as fp:
            combined_audio.export(fp.name, format='wav')
            # Ensure the file is written and ready for other processes to read
            fp.flush()
            
            # Now you can pass the filename to the transcription function
            return self.transcribe_from_file(fp.name, cfg=cfg)

    def transcribe_from_blob(self, blob: str | None = None, cfg=None):
        """
        Transcribes an audio file from blob.

        Parameters:
            blob (str): Base64 encoded blob bytes
            cfg (Optional[dict]):  A dictionary containing configuration settings that overwrite default settings. For more information, check `transcribe_from_file` documentation.

        Returns:
            tuple: Returns a tuple containing the segmentation data and metadata about the transcription. For more information, check `transcribe_from_file` documentation.
        """
        audio_data = base64.b64decode(blob)
        with tempfile.NamedTemporaryFile(suffix='.wav') as fp:
            fp.write(audio_data)
            fp.flush()

            return self.transcribe_from_file(fp.name, cfg=cfg)

    def transcribe_from_file(self, path: str = "", cfg=None):
        """
        Transcribes an audio file using the Whisper model, according to the specified configuration.

        Parameters:
            path (str): The file path of the audio to be transcribed. Default is an empty string.
            cfg (dict, optional): A dictionary containing configuration settings that overwrite default settings.
                If None is passed, default settings are used. Default configuration includes:
                    {
                        "beam_size": 5,
                        "language": "en",
                        "word_timestamps": True,
                        "vad_filter": True
                        "no_speech_prob": 0.5
                    }

        Returns:
            tuple: Returns a tuple containing the segmentation data and metadata about the transcription.
        """
        if cfg is None:
            cfg = {}
        default_cfg = {
            "beam_size": 5,
            "language": "en",
            "word_timestamps": True,
            "vad_filter": True,
            "no_speech_prob": 0.5
        }
        final_cfg = {**default_cfg, **cfg}

        transcribe_params = {
            "audio": path,
            "beam_size": final_cfg["beam_size"],
            "word_timestamps": final_cfg["word_timestamps"],
            "vad_filter": final_cfg["vad_filter"]
        }
        
        if final_cfg["language"] != "auto":
            transcribe_params["language"] = final_cfg["language"]

        segments, info = self.model.transcribe(**transcribe_params)

        return [segment for segment in segments if segment.no_speech_prob <= final_cfg["no_speech_prob"]], info

faster_whisper_model = FasterWhisperModel()