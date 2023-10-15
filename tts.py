from transformers import AutoProcessor, BarkModel
from optimum.bettertransformer import BetterTransformer
from scipy.io.wavfile import write as write_wav
import torch
from constants import LANGUAGE_TO_VOICE_PRESET

class TTS:
    '''
        Use cuda (GPU) if is available on device.
        Set the processor and model, here using suno/bark-small.
        BetterTransformer will provide better inference speed on the model.
    '''
    def __init__(self, language: str):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.processor = AutoProcessor.from_pretrained("suno/bark-small")
        self.model = BarkModel.from_pretrained("suno/bark-small").to(self.device)
        self.model = BetterTransformer.transform(self.model, keep_original_model=False)
        self.voice_preset = LANGUAGE_TO_VOICE_PRESET.get(language)
        self.sample_rate = self.model.generation_config.sample_rate

    def generate_audio(self, text: str):
        # output file name of gemerated audio
        filename = "AI_speech.wav"
        print("Start audio generation....", end="")
        # Process the input text and generate speech.
        inputs = self.processor(text, voice_preset=self.voice_preset).to(self.device)
        speech_values = self.model.generate(**inputs, do_sample=True)
        
        # Convert speech values to a numpy array and write to a WAV file.
        audio_array = speech_values.cpu().numpy().squeeze()
        write_wav(filename, rate=self.sample_rate, data=audio_array)
        print("Finished audio generation")

        return filename
    

tts = TTS("chinese")
tts.generate_audio("有一天，一隻蜗牛走进一家赌场。他走到柜台前，想跟柜台上的兔子下注。")
