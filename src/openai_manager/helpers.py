from .openai_manager import OpenAIManager



class Message():
    """
    Represents a message in a conversation with an OpenAI assistant.

    This class encapsulates the data related to a single message, including its text,
    associated thread key, and unique identifiers. It provides functionality to convert
    the message data into a dictionary format suitable for API calls.
    """

    def __init__(self, message_text: str, thread_key: str=None, id: str=None, thread_id: str=None) -> None:
        """
        Initializes a new instance of the Message class.

        :param message_text: The text content of the message.
        :type message_text: str
        :param thread_key: An optional key identifying the thread this message is associated with.
        :type thread_key: str, optional
        :param id: An optional unique identifier for the message.
        :type id: str, optional
        :param thread_id: An optional identifier for the thread this message belongs to.
        :type thread_id: str, optional

        :raises ValueError: If message_text is None or empty.

        :return: None
        :rtype: None
        """
        if message_text is None or len(message_text) == 0:
            raise ValueError("No message body provided.")

        if thread_key is None:
            thread_key = "None"

        # self.files = files
        self.thread_key = thread_key
        self.message_text = message_text

        self._id = id
        self._thread_id = thread_id


    def to_dict(self) -> str:
        """
        Converts the message data into a dictionary format.

        This method is particularly useful for preparing the message data to be sent
        through the OpenAI API. It structures the message content, role, and any file
        attachments in a dictionary.

        :return: A dictionary representation of the message.
        :rtype: dict
        """
        return {
            "thread_id": self._thread_id,
            "role": "user",
            "content": self.message_text,
            "file_ids": []
        }



class AssistantParams():
    """
    Encapsulates the parameters for creating or configuring an OpenAI assistant.

    This class holds various configuration options for an OpenAI assistant, including
    the model to be used, a name for the assistant, a description, instructions, and
    any associated tools or file IDs. It supports converting these parameters into a
    dictionary format suitable for API calls.
    """

    def __init__(self, openai_manager: OpenAIManager, model: str, name: str="DefaultAssistant", description: str="", instructions: str="", tools: list=None, file_ids: list=None) -> None:
        """
        Initializes a new instance of the AssistantParams class.

        :param openai_manager: The OpenAIManager instance to validate the model availability.
        :type openai_manager: OpenAIManager
        :param model: The model name to be used by the assistant.
        :type model: str
        :param name: An optional name for the assistant.
        :type name: str, optional
        :param description: An optional description for the assistant.
        :type description: str, optional
        :param instructions: Optional instructions for the assistant.
        :type instructions: str, optional
        :param tools: Optional list of tools the assistant can use.
        :type tools: list, optional
        :param file_ids: Optional list of file IDs associated with the assistant.
        :type file_ids: list, optional

        :raises ValueError: If the provided model is not available in openai_manager.

        :return: None
        :rtype: None
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
        Converts the assistant parameters into a dictionary format.

        This method structures the assistant's configuration options into a dictionary,
        making it suitable for use in API calls or other configurations where a dictionary
        representation is required.

        :return: A dictionary representation of the assistant parameters.
        :rtype: dict
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
        Returns a string representation of the AssistantParams instance.

        This method provides a convenient way to obtain a readable representation of
        the assistant parameters, including its model, name, description, instructions,
        tools, and file IDs.

        :return: A string representation of the instance.
        :rtype: str
        """
        return (f"{self.__class__.__name__}("
                f"model={self.model!r}, name={self.name!r}, "
                f"description={self.description!r}, instructions={self.instructions!r}, "
                f"tools={self.tools!r}, file_ids={self.file_ids!r})")