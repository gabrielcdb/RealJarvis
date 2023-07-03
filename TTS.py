import threading
import queue
import time
import pygame

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/TxGEqnHWrfWFTfGW9XjX"

TTS_MODELS = {
    "ELEVENLABS": "elevenlabs",
    "GTTS": "gtts",
    "PYTTS": "pytts"
}

class TTSManagerFactory:
    @staticmethod
    def create(model, **kwargs):
        if model == TTS_MODELS["ELEVENLABS"]:
            from elevenlabs import set_api_key
            set_api_key(kwargs['api_key'])
            return ElevenlabsTTSManager(kwargs['api_key'], kwargs.get('system', None))
        elif model == TTS_MODELS["GTTS"]:
            return GTTSTTSManager(kwargs.get('system', None))
        elif model == TTS_MODELS["PYTTS"]:
            return PyttsTTSManager(kwargs.get('system', None))
        else:
            raise ValueError(f"Unsupported model: {model}")

class AbstractTTSManager:
    def __init__(self, system=None):
        self.system = system
        self.paused = False
        self.audio_list = []
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
        self.load_thread = threading.Thread(target=self.load_next)
        self.load_thread.start()

    def add_message(self, text):
        self.queue.put(text)

    def run(self):
        print(f"Starting TTS {self.__class__.__name__} model")
        pygame.mixer.init()
        while True:
            if not pygame.mixer.get_busy() and not self.paused and self.audio_list:
                sound = self.audio_list.pop(0)
                sound.play()
            if pygame.mixer.get_busy() and self.system is not None:
                self.system.speaking = True
            else:
                if self.system is not None:
                    self.system.speaking = False
            time.sleep(0.2)

    def stop(self):
        self.queue.put('STOP')

    def pause(self):
        self.queue.put('PAUSE')

    def play(self):
        self.queue.put('PLAY')
    
    def load_next(self):
        while True:
            text = self.queue.get()
            if text == 'STOP':
                pygame.mixer.stop()
            elif text == 'PAUSE':
                pygame.mixer.pause()
                self.paused = True
            elif text == 'PLAY':
                self.audio_list=[]
                pygame.mixer.unpause()
                self.paused = False
            else:
                sound = self.play_text(text)
                if sound != None:
                    self.audio_list.append(sound)

class ElevenlabsTTSManager(AbstractTTSManager):
    def __init__(self, api_key, system=None):
        super().__init__(system)
        self.headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }

    def play_text(self, text):
        if not self.paused and text != "":
            data = {
                "text": str(text),
                "model_id": "eleven_multilingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
            response = requests.post(url, json=data, headers=self.headers, stream=True)
            byte_stream = io.BytesIO()
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    byte_stream.write(chunk)
            byte_stream.seek(0)
            return pygame.mixer.Sound(byte_stream)

class GTTSTTSManager(AbstractTTSManager):
    def __init__(self, system=None):
        super().__init__(system)
        from gtts import gTTS
        self.gTTS = gTTS
        self.language = 'en'

    def play_text(self, text):
        if not self.paused and text != "":
            myobj = self.gTTS(text=text, lang=self.language, slow=False)
            myobj.save("output.wav")
            return pygame.mixer.Sound("output.wav")
    def changeLanguage (self, language):
        from gtts.lang import tts_langs
        if language in tts_langs():
            self.language = language
class PyttsTTSManager(AbstractTTSManager):
    def __init__(self, system=None):
        super().__init__(system)
        import pyttsx3
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 130)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
    def play_text(self, text):
        if not self.paused and text != "":
            self.engine.save_to_file(text, 'output.wav')
            self.engine.runAndWait()
            return pygame.mixer.Sound("output.wav")

