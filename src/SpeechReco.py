import whisper
import pyaudio
import numpy as np


class speechReco:
    def __init__(self, model_size = "base"):
        self.model = whisper.load_model(model_size) # load whisper model model_size
        
        self.audio = pyaudio.PyAudio()
    
    def wakeUpCall(self, wake_word="hey b2", duration=4):
        stream = self.audio.open(format=pyaudio.paInt16, channels=1,
                                 rate=16000, input=True, frames_per_buffer=1024)
        
        print(f"Lytter efter wake word: '{wake_word}'")

        chunk_count = int(16000 / 1024 * duration)  # antal chunks for duration sekunder
        
        while True:
            frames = [stream.read(1024, exception_on_overflow=False) for _ in range(chunk_count)]
            audio = np.frombuffer(b"".join(frames), np.int16).astype(np.float32) / 32768.0
            text = self.model.transcribe(audio, fp16=False, language="en")["text"].lower()
            print("Du sagde:", text)
            if wake_word in text:
                print("Wake word registreret!")
                break

        stream.stop_stream()
        stream.close()   

    def recordSpeech(self, seconds = 3):
        # Standardparametre for optagelse
        format = pyaudio.paInt16
        channels = 1
        rate = 16000
        chunk = 1024

        # Start stream
        stream = self.audio.open(format=format,
                                 channels=channels,
                                 rate=rate,
                                 input=True,
                                 frames_per_buffer=chunk,
                                 input_device_index=1)

        print("Optager tale...")
        frames = []

        for _ in range(0, int(rate / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)

        print("Optagelse færdig.")

        # Stop og luk stream
        stream.stop_stream()
        stream.close()

        # Konverter byte-data til numpy array
        audio_data = np.frombuffer(b"".join(frames), np.int16).astype(np.float32) / 32768.0
        
        return audio_data

    def convertAudioToText(self, audio_data):

        # Kald whisper modellen
        result = self.model.transcribe(audio_data, fp16=False)
        return result["text"]

    def wakeAndRecord(self):
        self.wakeUpCall("hey b2")
        
        return self.convertAudioToText(self.recordSpeech(5))


if __name__ == "__main__":
    speech = speechReco()

    print(speech.wakeAndRecord()) 
    


