import json
import time
from queue import Queue
from threading import Thread
import openai
import os

# Create a class for the GPT Handler
class GPTHandler:
    def __init__(self,key,system, model):
        self.system = system
        self.message_queue = Queue()
        self.running = False
        openai.api_key = key
        self.model = model

    # Define the function
    def get_current_weather(self, location, unit="fahrenheit"):
        weather_info = {
            "location": location,
            "temperature": "72",
            "unit": unit,
            "forecast": ["sunny", "windy"],
        }
        return json.dumps(weather_info)
    def goodbye(self, bye):
        goodbye = {
            "bye": bye,
        }
        os._exit(0)
        return json.dumps(goodbye)
    def standby(self):
        return

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

    # Define the conversation
    def run_conversation(self):
        messages = [{"role": "system", "content": "You are Jarvis from iron man, a gentle and polite british AI assistant that always call the user 'Sir' or 'Monsieur'. You are currently connected to an ASR system and a TTS system so you now have voice and ears, behave accordingly"}]
        #messages.append({"role": "user", "content": "Please greet your master, introduce yourself, then ask him his name to better serve him. After that you will always call him by 'master + the name provided."})
        
        while self.running:
            while not self.message_queue.empty():
                new_message = self.message_queue.get()
                if new_message == "System Greetings":
                    second_response = openai.ChatCompletion.create(
                        model=self.model,
                        messages=messages,
                        stream=True,
                    )
                    sentence = ""
                    print("Jarvis said: ", end='', flush=True)
                    for event in second_response: 
                        event_text = event['choices'][0]['delta']
                        content  = event_text.get('content', '') 
                        if content != None:
                            print(content , end='', flush=True)
                            sentence += content
                            if "." in content or "!" in content or "?" in content or ":" in content or "," in content:
                                self.system.enqueue_tts_request(sentence)
                                sentence = content[-1]
                            time.sleep(0.2)
                else:
                    print()
                    print("You said: "+new_message)
                    messages.append({"role": "user", "content": new_message})

                    functions = [
                        {
                            "name": "get_current_weather",
                            "description": "Get the current weather in a given location",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "location": {
                                        "type": "string",
                                        "description": "The city and state, e.g. San Francisco, CA",
                                    },
                                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                                },
                                "required": ["location"],
                            },
                        },
                        {
                            "name": "goodbye",
                            "description": "Close the discussion",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "bye": {
                                        "type": "string",
                                        "description": "The goodbye formula",
                                    },
                                },
                            },
                        }
                    ]

                    response = openai.ChatCompletion.create(
                        model=self.model,
                        messages=messages,
                        functions=functions,
                        function_call="auto",
                        stream=True,
                    )
                    print("Jarvis said: ", end='', flush=True)
                    sentence = ""
                    function_name = ""
                    function_call_buffer = ""
                    full_content = ""
                    for event in response: 
                        event_text = event['choices'][0]['delta']
                        content  = event_text.get('content', '') 
                        if content != None:
                            full_content += content
                            print(content , end='', flush=True)
                            sentence += content
                            if "." in content or "!" in content or "?" in content or ":" in content or "," in content:
                                self.system.enqueue_tts_request(sentence)
                                sentence = content[-1]
                            time.sleep(0.2)
                        if event_text.get("function_call"):
                            available_functions = {
                                "get_current_weather": self.get_current_weather,
                                "goodbye": self.goodbye,
                            }
                            if("name" in event_text["function_call"].keys()):
                                function_name = event_text["function_call"]["name"]
                                if function_name != "python":
                                    function_to_call = available_functions[function_name]
                            if 'arguments' in event_text['function_call']:
                                function_call_buffer+=event_text['function_call']['arguments']

                            if '}' in function_call_buffer and function_name != "python":
                                function_args = json.loads(function_call_buffer)
                                if function_to_call == self.get_current_weather:
                                    function_response = function_to_call(
                                        location=function_args.get("location"),
                                        unit=function_args.get("unit"),
                                    )
                                else:
                                    function_response = function_to_call(bye = function_args.get("bye"))
                                messages.append({"role": "user", "content": full_content})
                                messages.append(
                                    {
                                        "role": "function",
                                        "name": function_name,
                                        "content": function_response,
                                    }
                                )
                                second_response = openai.ChatCompletion.create(
                                    model=self.model,
                                    messages=messages,
                                    stream=True,
                                )
                                sentence = ""
                                for event in second_response: 
                                    event_text = event['choices'][0]['delta']
                                    content  = event_text.get('content', '') 
                                    if content != None:
                                        print(content , end='', flush=True)
                                        sentence += content
                                        if "." in content or "!" in content or "?" in content or "," in content:
                                            self.system.enqueue_tts_request(sentence)
                                            sentence = content[-1]
                                        time.sleep(0.2)

                    if sentence != "":
                        self.system.enqueue_tts_request(sentence)
                        sentence = ""           
            time.sleep(0.2)
        
