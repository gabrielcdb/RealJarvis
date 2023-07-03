# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import queue
import threading
from TTS import TTSManager
from GPT import GPTHandler
from ASR import ASR

class System:
    def __init__(self, ASRmodelList, TTSmodelList, LLMmodelList, ASRmodelSelected , TTSmodelSelected , LLMmodelSelected, gpt_key, elevenlab_key):
        self.talking = False
        self.speaking = False
        self.ASRmodelList = ASRmodelList
        self.TTSmodelList = TTSmodelList
        self.LLMmodelList = LLMmodelList
        self.tts_manager = TTSManager(system = self, model = self.TTSmodelList[TTSmodelSelected], api_key = elevenlab_key)
        self.gpt_handler = GPTHandler(system = self, model=self.LLMmodelList[LLMmodelSelected], api_key = gpt_key)
        self.asr = ASR(self, model = self.ASRmodelList[ASRmodelSelected])

        
    def run(self):
        # Create a queue for each type of request
        self.tts_queue = queue.Queue()
        self.gpt_queue = queue.Queue()
        self.asr_queue = queue.Queue()
        self.system_queue = queue.Queue()

        # Create a thread for each queue to handle its requests
        self.tts_thread = threading.Thread(target=self.handle_tts_requests)
        self.gpt_thread = threading.Thread(target=self.handle_gpt_requests)
        self.asr_thread = threading.Thread(target=self.handle_asr_requests)
        self.system_thread = threading.Thread(target=self.handle_system_requests)

        # Start each thread
        self.tts_thread.start()
        self.gpt_thread.start()
        self.asr_thread.start()
        self.system_thread.start()

        self.gpt_handler.start()
        self.asr.run()
    # Enqueue a request
    def enqueue_tts_request(self, request):
        self.tts_queue.put(request)

    def enqueue_gpt_request(self, request):
        self.gpt_queue.put(request)

    def enqueue_asr_request(self, request):
        self.asr_queue.put(request)

    def enqueue_system_request(self, request):
        self.system_queue.put(request)

    def handle_system_requests(self):
        while True:
            # Get the next request from the queue
            request = self.system_queue.get()
            if request == "MUTE":
                self.enqueue_tts_request("PAUSE")
            if request == "UNMUTE":
                self.enqueue_tts_request("PLAY")
            # Mark the task as done
            self.system_queue.task_done()
    # Handle requests
    def handle_tts_requests(self):
        while True:
            # Get the next request from the queue
            request = self.tts_queue.get()

            self.tts_manager.add_message(request)

            # Mark the task as done
            self.tts_queue.task_done()

    def handle_gpt_requests(self):
        while True:
            # Get the next request from the queue
            request = self.gpt_queue.get()

            self.gpt_handler.add_message(request)

            # Mark the task as done
            self.gpt_queue.task_done()

    def handle_asr_requests(self):
        while True:
            # Get the next request from the queue
            request = self.asr_queue.get()
            
            # Mark the task as done
            self.asr_queue.task_done()

if __name__ == "__main__":
    system = System()
    system.run()
