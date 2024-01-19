from discord import Message as DiscordMessage
from .Managers.OpenAIManager import OpenAIManager



class Message():
    """
    TODO: fill in docstring
    """

    def __init__(self, message: any) -> None:
        """
        TODO: fill in docstring
        """
        self.text = ""
        self.author = ""

        if isinstance(message, DiscordMessage):
            self.text = str(message.content)
            self.author = str(message.author)

        elif isinstance(message, str):
            self.text = message
            self.author = "default"
            # self._str_message_parser(message)
    
    
    def _str_message_parser(self, message_str: str):
        raise NotImplementedError("Missing code.")



class AssistantParams():
    """
    TODO: fill in docstring
    """

    def __init__(self, openai_manager: OpenAIManager, model: str, name: str="DefaultAssistant", description: str="", instructions: str="", tools: list=None, file_ids: list=None) -> None:
        """
        TODO: fill in docstring
        """
        if tools is None:
            tools = []
        if file_ids is None:
            file_ids = []

        if not model in openai_manager.get_available_models():
            raise ValueError(f"Provided model '{model}' is not one of the available models.")
        
        self.model = model
        self.name = name
        self.description = description
        self.instructions = instructions
        self.tools = tools
        self.file_ids = file_ids


    def to_dict(self) -> dict:
        """
        TODO: fill in docstring
        """
        return {
            'model': self.model,
            'name': self.name,
            'description': self.description,
            'instructions': self.instructions,
            'tools': self.tools,
            'file_ids': self.file_ids
        }


    def __repr__(self) -> str:
        """
        TODO: fill in docstring
        """
        return (f"{self.__class__.__name__}("
                f"model={self.model!r}, name={self.name!r}, "
                f"description={self.description!r}, instructions={self.instructions!r}, "
                f"tools={self.tools!r}, file_ids={self.file_ids!r})")