import google.generativeai as genai
import yaml
import os
from pathlib import Path

class ConfigManager:
    def __init__(self, config_path="config.yaml"):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = os.path.join(base_dir, config_path)
        self.config = self.load_config()
    
    def load_config(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(
                f"Configuration file '{self.config_path}' not found. "
                f"Please copy config.example.yaml to config.yaml and add your API keys."
            )
        
        try:
            with open(self.config_path, 'r', encoding='utf-8-sig') as file:  # utf-8-sig handles BOM
                return yaml.safe_load(file)
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file: {e}")
    
    def get_api_key(self, provider):
        return self.config['api_keys'].get(f'{provider}_api_key')
    
    def get_model_config(self, provider):
        return self.config['models'].get(provider, {})

    def get_pre_prompt(self):
        return self.config.get('pre_prompt', '')

if __name__ == "__main__":
    try:
        conf = ConfigManager()
        print(f"API Key: {conf.get_api_key('google')}")
        print(f"Model: {conf.get_model_config('google')['default']}")
        print(f"promt lenght: {len(conf.get_pre_prompt())}")
    except Exception as e:
        print(f"Error: {e}")
