from transformers import pipeline

# Transcribe audio from a file using an Automatic Speech Recognition (ASR) model.
class ASR:
    @staticmethod
    def transcribe(filename: str, language: str) -> str:
        pipe = pipeline("automatic-speech-recognition", model="openai/whisper-medium", generate_kwargs = {"language":language})
        result = pipe(filename)

        return result["text"]