from openai import OpenAI
from openai.types.beta.thread import Thread
import shelve



class ThreadsManager:
    """
    TODO: fill in docstring
    """

    def __init__(self, client: OpenAI) -> None:
        """
        TODO: fill in docstring
        """
        self.client = client
        self.local_threads = self.get_threads_local()


    def get_thread_remote(self, thread_id: str) -> Thread:
        """
        TODO: fill in docstring
        """
        thread: Thread = None
        try:
            thread = self.client.beta.threads.retrieve(thread_id)
        except Exception as e:
            print("Unable to locate thread. The following exception was raised: " + str(e))
        
        return thread


    def get_thread_id_local(self, thread_key: str) -> str:
        """
        TODO: fill in docstring
        """
        thread_id = None
        if not thread_key is None:
            thread_dict = self.get_threads_local()
            thread_id = thread_dict.get(thread_key, None)
            # thread_dict_by_username = {username: id for id, username in thread_dict.items()}
            # thread_id = thread_dict_by_username[username]
        
        return thread_id


    def create_thread_remote(self):
        """
        TODO: fill in docstring
        """
        thread = None
        try:
            thread = self.client.beta.threads.create()
        except Exception as e:
            print("Unable to create thread. The following exception was raised: " + str(e))
        
        return thread            


    def create_thread_local(self, thread: Thread=None, thread_key: str=None):
        """
        TODO: fill in docstring
        """
        if thread is None:
            print(f"No thread provided. Creating a new thread \'{thread.id}\' at remote.")
            thread = self.create_thread_remote()
        
        if not thread is None:
            found_thread_id = None

            with shelve.open("threads_db", writeback=True) as threads_shelf:
                print("Looking for thread in local shelve db.")
                found_thread_id = threads_shelf.get(thread_key, None)

                if found_thread_id is None:
                    print("Did not find existing thread. Creating a new one...")
                    threads_shelf[thread_key] = thread.id            
        
        else:
            print("Returning None.")

        return thread


    def get_threads_local(self) -> dict:
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
    

    def get_messages_remote(self, thread):
        """
        Gets the message history associated with a thread directly from openai.

        :return: History of messages as a list. Message at index 0 is the latest message.
        """
        raw_msg_list = self.client.beta.threads.messages.list(thread.id)
        return [msg.content[0].text.value for msg in raw_msg_list]


    def __repr__(self) -> str:
        shelf_dict = self.get_threads_local()
        return str(shelf_dict)