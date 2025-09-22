from src.VoiceResponse import VoiceResponse
from src.SpeechReco import SpeechReco
from src.PiperTTS import PiperTTS

import os

def main():
    speech = SpeechReco()
    voice = VoiceResponse()
    
    tts = PiperTTS(f"{os.getcwd()}/voices")
    tts.load_model("en_US-amy-medium.onnx")

    user_q = speech.wakeAndRecord()
    print(user_q)

    while True:
        b2_response = voice.chat(user_q)
        print(b2_response)

        tts.speak(b2_response)
        
        user_q = speech.record()
        print(user_q)


if __name__ == "__main__":
    main()

