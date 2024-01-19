from ..Helpers import AssistantParams, Message
from openai import OpenAI
import shelve
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
        
        self.thread_manager = ThreadsManager(self)
    

    def get_thread(self, message: Message):
        """
        TODO: fill in docstring
        """

        self.thread = message.author
        return self.thread
    

    def send_message(self, message: Message):
        """
        TODO: fill in docstring
        """
        username = message.author
        
        thread = self.thread_manager.get_thread(username)

        # Add message to thread
        message = self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message.text,
        )
        
        # Run the assistant
        run = self.client.beta.threads.runs.create(thread_id=thread.id, assistant_id=self.assistant.id)

        while run.status != "completed":
            # Be nice to the API
            time.sleep(0.5)
            run = self.client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        # Retrieve the Messages
        messages = self.client.beta.threads.messages.list(thread_id=thread.id)
        new_message = messages.data[0].content[0].text.value
        
        return new_message


    def create_assitant(self, params: AssistantParams):
        """
        TODO: fill in docstring
        """
        return self.client.beta.assistants.create(**params.to_dict())
    


class ThreadsManager:
    """
    TODO: fill in docstring
    """

    def __init__(self, assistant_manager: AssistantManager) -> None:
        """
        TODO: fill in docstring
        """
        self.assistant_manager = assistant_manager
        self.local_thread_dict = self.read_shelf_to_dict()
        self.local_thread_id_list = self.get_thread_id_list_from_shelf()


    def get_thread(self, username):
        """
        TODO: fill in docstring
        """
        thread = self.get_thread_from_shelf(username)

        if thread is None:
            thread = self.create_thread(username)
        
        return thread

    
    def create_thread(self, username):
        """
        TODO: fill in docstring
        """
        thread = self.assistant_manager.client.beta.threads.create()
        
        if not thread.id is None:
            print(f"Thread created with id: {thread.id}.")
            print(f"Storing thread on shelf for username: {username}.")
            self.store_thread_on_shelf(username, thread.id)
        
        else:
            print("Thread was not created. Returning None.")

        return thread


    def get_thread_from_shelf(self, username):
        """
        TODO: fill in docstring
        """
        thread = None
        thread_id = self.find_thread_on_shelf(username)

        if thread_id is None:
            print(f"Could not find thread on shelf for username: {username}. Returning None.")
            thread = None
        
        else:
            print(f"Found thread for {username} with thread ID {thread_id} on shelf.")
            thread = self.get_thread_from_openai(thread_id)

        return thread
    

    def get_thread_from_openai(self, thread_id):
        return self.assistant_manager.client.beta.threads.retrieve(thread_id)
    

    def find_thread_on_shelf(self, username):
        """
        TODO: fill in docstring
        """
        thread_id = None
        with shelve.open("threads_db") as threads_shelf:
            thread_id = threads_shelf.get(username, None)
        
        return thread_id
        

    def store_thread_on_shelf(self, username, thread_id):
        """
        TODO: fill in docstring
        """
        with shelve.open("threads_db", writeback=True) as threads_shelf:
            threads_shelf[username] = thread_id


    def read_shelf_to_dict(self) -> dict:
        """
        Reads the entire shelve database and returns its contents as a dictionary.

        :return: A dictionary with usernames as keys and thread IDs as values.
        """
        shelf_dict = {}
        with shelve.open("threads_db") as threads_shelf:
            for key in threads_shelf:
                shelf_dict[key] = threads_shelf[key]
        
        self.local_thread_dict = shelf_dict
        return shelf_dict
    

    def get_message_history(self, thread):
        """
        Gets the message history associated with a thread.

        :return: History of messages as a list. Message at index 0 is the latest message.
        """
        raw_msg_list = self.assistant_manager.client.beta.threads.messages.list(thread.id)
        return [msg.content[0].text.value for msg in raw_msg_list]
    

    def get_thread_id_list_from_shelf(self):
        thread_dict = self.read_shelf_to_dict()
        return [thread_id for username, thread_id in thread_dict.items()]


    def __repr__(self) -> str:
        shelf_dict = self.read_shelf_to_dict()
        return str(shelf_dict)