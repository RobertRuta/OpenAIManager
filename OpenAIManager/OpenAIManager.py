from openai import OpenAI
import json
import requests



class OpenAIManager():
    """
    TODO: fill in docstring
    """
    
    list_models_api_url = "https://api.openai.com/v1/models"

    def __init__(self, api_key: str) -> None:
        """
        TODO: fill in docstring
        """
        self.client = OpenAI(api_key=api_key)
        self.api_key = api_key
        self.available_models = self.get_available_models()

    def get_available_models(self):
        """
        TODO: fill in docstring
        """
        json_data = requests.get("https://api.openai.com/v1/models", headers={'Authorization': f'Bearer {self.api_key}'})
        # Parse the JSON data
        data = json.loads(json_data.text)
        # Extract model names
        model_names = [item['id'] for item in data['data']]
        
        return model_names