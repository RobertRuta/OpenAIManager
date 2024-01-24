from .threads_manager import ThreadsManager
from .helpers import AssistantParams, Message
from openai import OpenAI
from openai.types.beta.thread import Thread # the openai Thread type
import time



class AssistantManager():
    """
    A class for managing openAI assistants. Handles assistant creation and message sending via this assistant.
    """

    def __init__(self, client: OpenAI, assistant_id: str=None, assistant_params: AssistantParams=None) -> None:
        """
        Creates an AssistantManager object.

        :param: client: OpenAi object that serves as a connection to the api.
        :type client: openai.OpenAI
        :param assistant_id: OpenAI assistant ID of existing assistant.
        :type assistant_id: str
        :param assistant_params: OpenAIManager.Helpers.AssistantParams object constitituting the parameters of an assistant.
        :type assistant_params: AssistantManager
        If provided when assistant_id was not, constructor will create assistant with the provided parameters.

        :raises TypeError: If assistant_params is not of type AssistantParams.
        :raises ValuError: If both assistant_id and assistant_params not provided.

        :return: None
        :rtype: None
        """
        self.client = client
        self.assistant = None
        self.thread = None

        # Specify existing openai assistant
        if not assistant_id is None:
            self.assistant = client.beta.assistants.retrieve(assistant_id)
        
        # Or create new assistant with provided assistant parameters
        elif not assistant_params is None:
            if isinstance(assistant_params, AssistantParams):
                self.assistant = self.create_assitant(assistant_params)
            else:
                raise TypeError("\'assistant_params\' must be of type \'AssistantParams\'.")
        
        # Otherwise throw an error
        else:
            raise ValueError("Both \'assistant_id\' and \'assistant_params\' were left undefined. "
                             + "If you would like to create an assistant, please provide its parameters via \'assistant_params\'."
                             + "Otherwise, specify an existing assistant using \'assistant_id\'.")
        
        self.threads = ThreadsManager(self.client)
    

    def send_message(self, message: Message) -> str:
        """
        Sends a message to the OpenAI Assistant and receives a response.

        This method handles message sending to the OpenAI Assistant within a thread. 
        If the thread associated with the message does not exist, it creates a new thread remotely and locally. 
        It then adds the message to the thread and runs the assistant to generate a response.
        The method waits until the assistant's run status is 'completed' to ensure that a response is generated.
        Finally, it retrieves and returns the new message from the assistant.

        :param message: The message object containing the message to be sent.
        :type message: Message

        :raises: Various exceptions related to network issues, API errors, or unexpected response formats.

        :return: The assistant's text response.
        :rtype: str
        """
        thread_key = message.thread_key        
        thread_id = self.threads.get_thread_id_local(thread_key)
        thread: Thread = None

        if not thread_id is None:
            thread = self.threads.get_thread_remote(thread_id)

        else:
            thread = self.threads.create_thread_remote()
            self.threads.create_thread_local(thread, thread_key)
        
        message._thread_id = thread.id

        # Add message to thread
        message = self.client.beta.threads.messages.create(**message.to_dict())
        
        # Run the assistant
        run = self.client.beta.threads.runs.create(thread_id=thread.id, assistant_id=self.assistant.id)

        while run.status != "completed":
            time.sleep(0.5)
            run = self.client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        # Retrieve the Messages
        messages = self.threads.get_messages_remote(thread)
        new_message = messages[0]
        
        return new_message


    def create_assitant(self, params: AssistantParams):
        """
        Creates a new OpenAI Assistant based on provided AssistantParams object.

        This method creates a new assistant using the OpenAI API. It takes the parameters
        defined by the assistant, converts them into the appropriate format using the `to_dict` 
        method of the `AssistantParams` class, and then calls the OpenAI API to create the 
        assistant. The newly created assistant is returned.

        :param params: Parameters for the assistant to be created.
        :type params: AssistantParams

        :raises TypeError: If params is not of type `AssistantParams`.

        :return: The newly created assistant object.
        :rtype: openai.types.beta.assistant.Assistant
        """
        return self.client.beta.assistants.create(**params.to_dict())