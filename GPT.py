import json
import time
from queue import Queue
from threading import Thread
import openai
import os
from FunctionRegistry import FunctionRegistry
class GPTHandler:
    def __init__(self, api_key, system, model):
        self.system = system
        self.message_queue = Queue()
        self.running = False
        openai.api_key = api_key
        self.model = model
        self.function_registry = FunctionRegistry()
        self.messages = []
        with open("localdir/config.json", "r") as f:
            config = json.load(f)
        if "init_message" in config:
            self.init_message = config["init_message"]
        else:
            self.init_message = "You are Jarvis, a powerful AI assistant that can perform many tasks. You are currently connected to an ASR system and a TTS system, so you now have voice and ears."
            config["init_message"] = self.init_message
            with open("localdir/config.json", "w") as f:
                json.dump(config, f)

    # Define the method to start the conversation
    def start(self):
        self.running = True
        self.thread = Thread(target=self.run_conversation)
        self.thread.start()

    # Define the method to stop the conversation
    def stop(self):
        self.running = False
        self.thread.join()

    # Define the method to add a message to the queue
    def add_message(self, message):
        self.message_queue.put(message)

    def get_chat_response(self, functions = False):
        if functions:
            return openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            functions=self.function_registry.functions,
            function_call="auto",
            stream=True,
            )
        return openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            stream=True,
        )

    def handle_chat_response(self, response):
        sentence = ""
        function_name = ""
        function_call_buffer = ""
        full_content = ""
        for event in response:
            event_text = event['choices'][0]['delta']
            content = event_text.get('content', '')
            if content is not None:
                full_content += content
                print(content, end='', flush=True)
                sentence += content
                self.maybe_enqueue_tts_request(sentence)
                sentence = self.trim_sentence(sentence)
                time.sleep(0.2)
            if event_text.get("function_call"):
                function_call_buffer , function_name = self.handle_function_call(event_text, function_call_buffer, function_name)

        if sentence.strip():
            self.system.enqueue_tts_request(sentence)
    def handle_function_call(self, event_text, function_call_buffer, function_name):
        if "name" in event_text["function_call"].keys():
            function_name = event_text["function_call"]["name"]
        if 'arguments' in event_text['function_call']:
            function_call_buffer += event_text['function_call']['arguments']

        if '}' in function_call_buffer:
            function_call_args = json.loads(function_call_buffer)
            function_call_response = self.function_registry.call(function_name, function_call_args)
            if function_call_response["action"] == "answer":
                self.messages.append(
                    {
                        "role": "function",
                        "name": function_name,
                        "content": function_call_response["argsForGPT"],
                    }
                )
                response = self.get_chat_response(functions=False)
                self.handle_chat_response(response)
            elif function_call_response["action"] == "system":
                argsForSystem =json.loads(function_call_response["argsForSystem"])
                if argsForSystem["action"] == "change_language":
                    self.system.changeLanguage(argsForSystem["language"])
        return function_call_buffer , function_name

    def maybe_enqueue_tts_request(self, sentence):
        if "." in sentence or "!" in sentence or "?" in sentence or ":" in sentence or ("," in sentence and len(sentence) > 40):
            self.system.enqueue_tts_request(sentence)

    def trim_sentence(self, sentence):
        if "." in sentence or "!" in sentence or "?" in sentence or ":" in sentence or ("," in sentence and len(sentence) > 40):
            return ""
        return sentence

    def run_conversation(self):
        print(f"Starting LLM {self.model} model")
        self.messages.append({"role": "system", "content": self.init_message})

        while self.running:
            self.system.thinking = False
            while not self.message_queue.empty():
                self.system.thinking = False
                new_message = self.message_queue.get()
                self.system.thinking = True

                if new_message == "System Greetings":
                    response = self.get_chat_response(functions=False)
                    self.handle_chat_response(response)
                else:
                    print()
                    print("You said: " + new_message)
                    self.messages.append({"role": "user", "content": new_message})

                    response = self.get_chat_response(functions=True)
                    self.handle_chat_response(response)

            time.sleep(0.2)