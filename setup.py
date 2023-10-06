from record import Recorder
from asr import ASR
from tandamGPT import TandamGPT
from tts import TTS
        
class Setup:
    def __init__(self) -> None:
        self.bot = TandamGPT()

    # save the settings from Gradio UI input
    def save(self, language: str, silence_duration: int):
        self.sd = silence_duration
        self.language = language
        self.bot.set_language(self.language)

    # Record your voice using the microphone
    def record(self):
        filename = "user.wav"

        # Record audio from microphone then pass on to Whisper to trasnscribe.
        Recorder.record_audio(filename=filename, silence_duration=self.sd)
        user_msg = ASR.transcribe(filename=filename, language=self.language).strip()

        return user_msg

    # The AI response along with the correction and explanation is obtained by prompting GPT 3.5 API. 
    def get_bot_msg(self, message):
        text = self.bot.receive(message).strip()
        return text

    def get_correction(self, message):
        return self.bot.correction(message)
    
    def get_explanation(self, message):
        return self.bot.explanation(message)

    # Generate the audio file of AI speaking.
    def audio_file(self, bot_msg: str):
        tts = TTS(language=self.language)
        filename = tts.generate_audio(text = bot_msg)

        return filename