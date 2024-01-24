from openai import OpenAI
import json
import requests



class OpenAIManager():
    """
    Manages interactions with the OpenAI API, specifically for retrieving available models.

    This class is designed to encapsulate the functionality related to the OpenAI API, 
    primarily focusing on listing the available models. It currently offers limited 
    additional utility beyond what the OpenAI Python client library provides. 
    This redundancy might not justify its use in a context where direct usage of 
    the OpenAI client library would suffice.

    Attributes:
        list_models_api_url (str): The API URL for listing OpenAI models.
    """
    
    list_models_api_url = "https://api.openai.com/v1/models"


    def __init__(self, api_key: str) -> None:
        """
        Initializes the OpenAIManager with the provided API key.

        This constructor initializes the OpenAI client and retrieves a list of available
        models at the time of instantiation. It stores the API key and the list of 
        models for further use.

        :param api_key: The API key for accessing OpenAI services.
        :type api_key: str

        :return: None
        """
        self.client = OpenAI(api_key=api_key)
        self.api_key = api_key
        self.available_models = self.get_available_models()


    def get_available_models(self):
        """
        Retrieves a list of available models from the OpenAI API.

        This method makes an HTTP request to the OpenAI API to fetch the currently available models.
        It returns a list of model identifiers. Note that this method directly interacts with the API
        and does not utilize the OpenAI client library, which might be seen as a redundancy given that
        the client library already provides this functionality.

        :return: A list of available model names.
        :rtype: list[str]

        :raises: HTTPError or other network-related errors if the request to the OpenAI API fails.
        """
        json_data = requests.get("https://api.openai.com/v1/models", headers={'Authorization': f'Bearer {self.api_key}'})
        # Parse the JSON data
        data = json.loads(json_data.text)
        # Extract model names
        model_names = [item['id'] for item in data['data']]
        
        return model_names