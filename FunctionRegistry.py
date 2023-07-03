import json
import os
class FunctionRegistry:
    def __init__(self):
        #add new methods names there
        self.available_functions = {
            "get_current_weather": self.get_current_weather,
            "goodbye": self.goodbye,
            "change_language": self.change_language
                            }
        self.functions = [
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
        inprogress = {
                            "name": "change_language",
                            "description": "Change the speaking language",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "language": {
                                        "type": "string",
                                        "description": "The language to turn the converstation in, in a lowkey 2 character format, for gTTS",
                                    },
                                },
                                "required": ["language"],
                            },
                        }

    def register_function(self, function_name, function):
        self.available_functions[function_name] = function

    def call(self, function_name, function_call_args):
        if function_name not in self.available_functions:
            raise ValueError(f"No such function: {function_name}")

        function_to_call = self.available_functions[function_name]
        result = function_to_call(**function_call_args)

        return result
    #add new methods there
    def get_current_weather(self, location, unit="fahrenheit"):
        weather_info = {
            "location": location,
            "temperature": "72",
            "unit": unit,
            "forecast": ["sunny", "windy"],
        }
        result = {
            "action": "answer",
            "argsForGPT": json.dumps(weather_info),
        }
        return result
    def change_language(self, language):

        sys_args = {
            "action": "change_language",
            "language": language,
        }

        result = {
                "action": "system",
                "argsForGPT": "",
                "argsForSystem": json.dumps(sys_args),
        }
        return result
    def goodbye(self, bye):
        goodbye = {
            "bye": bye,
        }
        print("Goodbye")
        os._exit(0)
        return json.dumps(goodbye)