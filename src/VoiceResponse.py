import numpy as np
import google.generativeai as genai
from src.ConfigManager import ConfigManager

class VoiceResponse:
    def __init__(self, pre_prompt=None):
        self.config = ConfigManager()

        # loads prompt from yaml
        if pre_prompt == None:
            pre_prompt = self.config.get_pre_prompt()
        else:
            print("den er ikke None")
            
        llm_api_key = self.config.get_api_key('google') 

        genai.configure(api_key=llm_api_key)

        # get model
        model_config = self.config.get_model_config('google')
        model_name = model_config.get('default', 'gemini-1.5-flash')
        
        # generation settings
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "max_output_tokens": 1000,
        }
        
        # safety settings
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
        
        # model with system instruction
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
            safety_settings=safety_settings,
            system_instruction=pre_prompt
        )
        
        # chat session
        self.chat_session = self.model.start_chat(history=[])
        print(f"initialized with model: {model_name}")
    
    def chat(self, user_message):
        try:
            response = self.chat_session.send_message(user_message)
            return response.text
        except Exception as e:
            return f"Error: {e}"
    
    def reset_conversation(self):
        self.chat_session = self.model.start_chat(history=[])
        print("Conversation reset!")
    
    def get_history(self):
        return self.chat_session.history
    
    def start_conversation(self):
        print(f"Chat started! (type 'quit' to exit, 'reset' to start over)")
                
        while True:
            user_input = input("\nYou: ")
            
            if user_input.lower() == 'quit':
                print("Goodbye!")
                break
            elif user_input.lower() == 'reset':
                self.reset_conversation()
                continue
                
            response = self.chat(user_input)
            print(f"Assistant: {response}")



# tester
if __name__ == "__main__":
    try:
        voice = VoiceResponse()
        
        print("ready for chat")

        print(f"response: {voice.chat("hey whats your name")}")
        
    except Exception as e:
        print(f"Error: {e}")
