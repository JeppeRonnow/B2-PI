import subprocess
import tempfile
import os
import platform


class PiperTTS:
    def __init__(self, voices_dir = "../voices"):
        self.voices_dir = os.path.abspath(voices_dir)
        self.model_path = None

    def load_model(self, model_name: str):
        # Load a Piper TTS model.

        path = os.path.join(self.voices_dir, model_name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model file not found: {path}")
        self.model_path = path

    def speak(self, text: str):
        # speak
        if self.model_path is None:
            raise RuntimeError("No model loaded. Call load_model() first.")

        # temp wav file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            wav_path = f.name

        try:
            # run Piper command
            subprocess.run(
                ["piper", "--model", self.model_path, "--output_file", wav_path],
                input=text.encode("utf-8"),
                check=True
            )
            
            # play file
            if platform.system() == "Linux":
                subprocess.run(["aplay", wav_path])
            elif platform.system() == "Windows":
                subprocess.run([
                    "powershell",
                    "-c",
                    f"(New-Object Media.SoundPlayer '{wav_path}').PlaySync();"
                ])
            else:
                print(f"TTS saved to {wav_path} (no playback command for {platform.system()})")

            # remove file
        finally:
            if os.path.exists(wav_path):
                os.remove(wav_path)


if __name__ == "__main__":
    tts = PiperTTS()
    tts.load_model("en_US-amy-medium.onnx")
    tts.speak("Little fucking test. Yay hell-l-lo")
