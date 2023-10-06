import pyaudio
import wave
import webrtcvad

class Recorder:
    # Function to record audio
    @staticmethod
    def record_audio(filename: str, silence_duration: int) -> None:
        # Constants for audio recording
        RATE = 16000  # Sample rate
        CHUNK_SIZE = 160  # Audio chunk size in frames
        FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
        VAD = 3
        audio = pyaudio.PyAudio()

        # Open a new stream for audio input
        stream = audio.open(format=FORMAT,
                            channels=1,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK_SIZE)

        vad = webrtcvad.Vad()
        vad.set_mode(VAD)
        frames = [] # store microphone input 
        timer = 0 # time the silence duration
        speech_started = False
        
        # Stay in this while loop if user has not started to speak.
        while True:
            data = stream.read(CHUNK_SIZE)
            if speech_started:
                break
            elif not speech_started and vad.is_speech(data, RATE):
                speech_started = True

        # recording stops when the user stops speaking for a duration of time
        print("Speech started.")
        while True:
            data = stream.read(CHUNK_SIZE)
            frames.append(data)
                
            if vad.is_speech(data, RATE):
                timer = 0
            else:
                print(".", end='')
                timer += (CHUNK_SIZE * 1000) / RATE
            
            if timer >= silence_duration * 1000:
                break

        print(" Finished recording.")
        # cut out the silent frames
        silence_frames = silence_duration * 100
        frames = frames[:-silence_frames]

        # Stop and close the audio stream
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Save the audio data to a WAV file
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()


