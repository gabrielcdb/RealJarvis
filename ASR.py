import os
import subprocess
import threading
import time
import wave
import struct
from datetime import datetime
from queue import Queue
import whisper
import socket
import openai

ASR_MODELS = {
    "LEE_UENO": "lee-ueno",
    "WHISPER": "whisper",
    "WHISPER_ONLINE": "whisper-online"
}

BASE_DIR = os.getcwd()
SUBFOLDER = "subfolder"
TEMP_WAV = "temp.wav"

EOF_MARKER = 0
BUFFER_FORMAT = '=i'
SAMPLE_FORMAT = 'h'
VOLUME_FACTOR = 2
WAVE_PARAMS = (1, 2, 16000, 0, 'NONE', 'NONE')

class ASR(threading.Thread):
    def __init__(self, system, model=ASR_MODELS["LEE_UENO"]):
        threading.Thread.__init__(self)
        self.model = model
        self.results = Queue()
        self.system = system

    def run(self):
        print(f"Starting ASR {self.model} model")
        if self.model == ASR_MODELS["LEE_UENO"]:
            self.run_lee()
        elif self.model == ASR_MODELS["WHISPER"]:
            self.run_whisper()
        elif self.model == ASR_MODELS["WHISPER_ONLINE"]:
            self.run_whisper_online()


    def run_lee(self):
        command = "py B:/OneDrive/BureauPortable/Recognition-model/recognition_wo_mmd2.py"
        subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(2)
        command = "adintool.exe -in mic -out adinnet -server 127.0.0.1  -port 5533 -cutsilence -nostrip"
        subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(2)
        host = 'localhost'  # Server IP
        port = 5534        # Server Port
        client_socket  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print("ASR model lee-ueno loaded")
        # Run the server loop
        while True:
            # Receive data from the client
            message = client_socket.recv(1024).decode()
            print(f"Received data: {message}")
            self.checkForCommands(message)
            self.system.enqueue_gpt_request(message)
        
    def checkForCommands(self, text):
        text = text.lower()
        if "quiet" in text or "silence" in text or "tais-toi" in text or "shut-up" in text or "shut up" in text:
            self.system.enqueue_system_request("MUTE")
        elif "jarvis" in text or "parle" in text or "speak" in text or "unmute" in text:
            self.system.enqueue_system_request("UNMUTE")

    def run_whisper(self):
        now = datetime.now()
        datetime_string = now.strftime("%Y-%m-%d_%H-%M-%S")
        subfolder = "subfolder"
        base_dir = os.getcwd()

        os.makedirs(os.path.join(base_dir, subfolder), exist_ok=True)

        command = f"adintool.exe -in mic -out adinnet -server 127.0.0.1  -port 5533 -cutsilence -nostrip -lv 1000"
        subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        adinserversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        adinserversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        adinserversock.bind(("127.0.0.1", 5533))
        adinserversock.listen(1)
        adinclientsock, adinclient_address = adinserversock.accept()
        print("ASR model whisper loaded")
        self.system.enqueue_gpt_request("System Greetings")
        buffer = b''
        while True:
            rcvmsg = adinclientsock.recv(4)
            nbytes = struct.unpack('=i', rcvmsg)[0]
            tmpdata = adinclientsock.recv(nbytes)
            buffer += tmpdata
            self.system.talking = True
            print(".", end='', flush=True)
            if nbytes == 0:
                print(".")
                # We received an EOF marker, write the accumulated buffer to the file
                with wave.open("temp.wav", "wb") as wav_file:
                    wav_file.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
                    wav_file.writeframes(buffer)
                    
                result = self.whisper_model.transcribe("temp.wav")
                self.checkForCommands(str(result['text']))
                self.system.enqueue_gpt_request(str(result['text']))

                # Clear the buffer
                buffer = b''
                self.system.talking = False

    def run_whisper_online(self):
        command = f"adintool.exe -in mic -out adinnet -server 127.0.0.1  -port 5533 -cutsilence -nostrip -lv 1000"
        subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        adinserversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        adinserversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        adinserversock.bind(("127.0.0.1", 5533))
        adinserversock.listen(1)
        adinclientsock, adinclient_address = adinserversock.accept()
        whisper_model = whisper.load_model("base")
        print("ASR model whisper online loaded")
        self.system.enqueue_gpt_request("System Greetings")
        buffer = b''
        while True:
            rcvmsg = adinclientsock.recv(4)
            nbytes = struct.unpack('=i', rcvmsg)[0]
            tmpdata = adinclientsock.recv(nbytes)
            buffer += tmpdata
            self.system.talking = True
            print(".", end='', flush=True)
            if nbytes == 0:
                print(".")
                # We received an EOF marker, write the accumulated buffer to the file
                with wave.open("temp.wav", "wb") as wav_file:
                    wav_file.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
                    wav_file.writeframes(buffer)
                with open("temp.wav", "rb") as audio_file:
                    result = openai.Audio.transcribe("whisper-1", audio_file)
                    self.checkForCommands(str(result['text']))
                    self.system.enqueue_gpt_request(str(result['text']))

                # Clear the buffer
                buffer = b''
                self.system.talking = False
    def increase_volume(self, buffer, factor):
        # The buffer contains raw audio data in the form of bytes. 
        # To increase the volume, you need to unpack those bytes into integers, increase their value, and then pack them back into bytes.
        # The 'h' argument in the unpack function means the data is short integers (2 bytes).
        audio_as_int = struct.unpack(str(len(buffer)//2)+'h', buffer)
        
        # Multiply each integer value by the volume factor to increase the volume
        audio_as_int = [int(sample * factor) for sample in audio_as_int]
        
        # Convert the integer values back into bytes
        buffer = struct.pack(str(len(audio_as_int))+'h', *audio_as_int)
        
        return buffer
    def get_result(self):
        if not self.results.empty():
            return self.results.get()
        else:
            return None
