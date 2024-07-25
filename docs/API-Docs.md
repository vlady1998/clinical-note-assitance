# Websocket Endpoints (/ws)

## 1. /transcription

Websocket endpoint for real-time transciption using Faster-Whisper model.
    
### Receive: JSON format

1. type
    
    Type of message: "config" or "audio".

    When you're sending configuration details like language, it is "config".
    When you're sending reocrding data, it is "audio".
    
2. data

    Body of message:
    
    If type is "config", it is configuration settings.
    If type is "audio", it is audio base64 encoded chunk data.
    
### Send: JSON format

1. When type is "config", it is not sending any message.

2. When type is "audio", send transcribed words arrays with their timestamp(timestamp in milliseconds)

    ```
    [
        {
            "word": "Hello",
            "timestamp": [0, 786]
        },
        {
            "word": "How",
            "timestamp": [1001, 1897]
        }
    ]
    ```

