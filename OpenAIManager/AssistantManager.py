from .ThreadsManager import ThreadsManager
from .Helpers import AssistantParams, Message
from openai import OpenAI
from openai.types.beta.thread import Thread # the openai Thread type
import time



class AssistantManager():
    """
    TODO: fill in docstring
    """

    def __init__(self, client: OpenAI, assistant_id: str=None, assistant_params: AssistantParams=None) -> None:
        """
        TODO: fill in docstring
        """
        self.client = client
        self.assistant = None
        self.thread = None

        # Specify existing openai assistant
        if not assistant_id is None:
            self.assistant = client.beta.assistants.retrieve(assistant_id)
        
        # Or create new assistant with provided assistant parameters
        elif not assistant_params is None:      
            self.assistant = self.create_assitant(assistant_params)
        
        # Otherwise throw an error
        else:
            raise ValueError("Both \'assistant_id\' and \'assistant_params\' were left undefined. "
                             + "If you would like to create an assistant, please provide its parameters via \'assistant_params\'."
                             + "Otherwise, specify an existing assistant using \'assistant_id\'.")
        
        self.threads = ThreadsManager(self.client)
    

    def send_message(self, message: Message):
        """
        TODO: fill in docstring
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
        TODO: fill in docstring
        """
        return self.client.beta.assistants.create(**params.to_dict())