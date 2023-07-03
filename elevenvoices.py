import pygame
import requests
import io
import threading
import queue
import time
import elevenlabs
from gtts import gTTS
import os
import pyttsx3

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/TxGEqnHWrfWFTfGW9XjX"
headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": "747e35b6483da5dc04404854646d2bcd"
}
class TTSManager:
    def __init__(self, model, api_key = "",system = None):
        self.system = system
        self.paused = False
        self.audio_list = []
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
        self.load_thread = threading.Thread(target=self.load_next)
        self.load_thread.start()
        elevenlabs.set_api_key(api_key)
        self.language = 'en'
        self.model = model
        self.pitch=1.5 
        self.volume=1.25
        self.engine = pyttsx3.init() # object creation
        self.engine.setProperty('rate', 130)  
        voices = self.engine.getProperty('voices')    
        self.engine.setProperty('voice', voices[1].id)
        
    def play_text(self, text):
        if not self.paused:
            if self.model == "elevenlabs":
                    data = {
                        "text": str(text),
                        "model_id": "eleven_multilingual_v1",
                        "voice_settings": {
                            "stability": 0.5,
                            "similarity_boost": 0.5
                        }
                    }
                    response = requests.post(url, json=data, headers=headers, stream=True)
                    byte_stream = io.BytesIO()
                    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                        if chunk:
                            byte_stream.write(chunk)
                    byte_stream.seek(0)
                    return pygame.mixer.Sound(byte_stream)                
            elif self.model == "gtts":
                myobj = gTTS(text=text, lang=self.language, slow=False)
                myobj.save("output.wav")
                return pygame.mixer.Sound("output.wav")
            elif self.model == "pytts":
                self.engine.save_to_file(text, 'output.wav')
                self.engine.runAndWait()
                #engine.setProperty('voice', voices[0].id)
                return pygame.mixer.Sound("output.wav")

    def play_single_text(self, text):
        if self.model == "elevenlabs":
            data = {
                "text": str(text),
                "model_id": "eleven_multilingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
            response = requests.post(url, json=data, headers=headers, stream=True)
            byte_stream = io.BytesIO()
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    byte_stream.write(chunk)
            byte_stream.seek(0)
            sound = pygame.mixer.Sound(byte_stream)
            sound.play()
        elif self.model == "gtts":
                myobj = gTTS(text=text, lang=self.language, slow=False)
                myobj.save("output.wav")
                return pygame.mixer.Sound("output.wav")
        elif self.model == "pytts":
            self.engine.save_to_file(text, 'output.wav')
            #engine.setProperty('voice', voices[0].id)
            self.engine.runAndWait()
            return pygame.mixer.Sound("output.wav")

    def add_message(self, text):
        self.queue.put(text)

    def load_next(self):
        while True:
            text = self.queue.get()
            if text == 'STOP':
                pygame.mixer.stop()
            elif text == 'PAUSE':
                self.play_single_text("Ok")
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

    def run(self):
        pygame.mixer.init()
        while True:
            if not pygame.mixer.get_busy() and not self.paused and self.audio_list:  # Only process new text if there's no active sound playing and not paused
                sound = self.audio_list.pop(0)
                sound.play()
            if pygame.mixer.get_busy() and self.system != None:
                self.system.speaking = True
            else:
                if self.system != None:
                    self.system.speaking = False
            time.sleep(0.2)

    def stop(self):
        self.queue.put('STOP')
    def pause(self):
        self.queue.put('PAUSE')
    def play(self):
        self.queue.put('PLAY')

if(__name__ == "__main__"):
    tts_manager = TTSManager("pytts")

    # Example usage:

    tts_manager.add_message("Hello, world! My name is Gabriel, let me tell you a great story, this is about fun shit")
    tts_manager.add_message("Hello, world! My name is Gabriel, let me tell you a great story, this is about fun shit")
    time.sleep(3)
    tts_manager.pause()  # This will pause playback
    time.sleep(5)
    tts_manager.play()  # This will unpause playback
