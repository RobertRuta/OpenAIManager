from openai import OpenAI
from openai.types.beta.thread import Thread
import shelve



class ThreadsManager:
    """
    Manages the storage and retrieval of threads and messages for an OpenAI application.

    This class handles the interactions between local storage and the remote OpenAI API, 
    specifically focusing on thread management. It provides methods to create, retrieve, 
    and manage threads both locally and remotely. Due to API limitations and the current 
    scope of the class design, it lacks functionality to fetch all threads directly from 
    the remote server, and its capabilities are primarily centered around individual 
    management of known threads.
    """

    def __init__(self, client: OpenAI) -> None:
        """
        Initializes the ThreadsManager with a client for OpenAI API interactions.

        This constructor sets up the manager with an OpenAI client and initializes 
        local storage for thread tracking. It loads existing thread data from local 
        storage upon instantiation.

        :param client: The OpenAI client used for API interactions.
        :type client: openai.OpenAI

        :return: None
        """
        self.client = client
        self.local_threads = self.get_threads_local()


    def get_thread_remote(self, thread_id: str) -> Thread:
        """
        Retrieves a specific thread from the remote OpenAI server using its ID.

        This method attempts to fetch a thread from the OpenAI API. If the thread does 
        not exist or an error occurs during retrieval, an exception is caught and handled.

        :param thread_id: The unique identifier of the thread to retrieve.
        :type thread_id: str

        :return: The retrieved thread or None if not found or an error occurs.
        :rtype: openai.types.beta.thread.Thread or None
        """
        thread: Thread = None
        try:
            thread = self.client.beta.threads.retrieve(thread_id)
        except Exception as e:
            print("Unable to locate thread. The following exception was raised: " + str(e))
        
        return thread


    def get_thread_id_local(self, thread_key: str) -> str:
        """
        Retrieves the ID of a local thread based on a provided \"thread key\".

        This method looks up a thread's ID in the local shelve database using the provided 
        thread key. If the thread key does not exist in the local storage, None is returned.

        :param thread_key: The key used to identify the thread in local storage.
        :type thread_key: str

        :return: The ID of the thread associated with the given key, or None if not found.
        :rtype: str or None
        """
        thread_id = None
        if not thread_key is None:
            thread_dict = self.get_threads_local()
            thread_id = thread_dict.get(thread_key, None)
        
        return thread_id


    def create_thread_remote(self):
        """
        Creates a new thread on the remote OpenAI server.

        This method attempts to create a new thread using the OpenAI API. If an error 
        occurs during creation, it is printed and the thread is left as None.

        :return: The created thread or None if an error occurs.
        :rtype: Thread or None
        """
        thread = None
        try:
            thread = self.client.beta.threads.create()
        except Exception as e:
            print("Unable to create thread. The following exception was raised: " + str(e))
        
        return thread            


    def create_thread_local(self, thread: Thread=None, thread_key: str=None):
        """
        Creates a new thread in local storage or updates an existing one.

        This method adds a new thread to local storage using the provided thread object 
        and key. If the thread is not provided, a new one is created remotely. If the 
        thread already exists in local storage, it is updated.

        :param thread: The thread object to store or update locally.
        :type thread: Thread, optional
        :param thread_key: The key to associate with the thread in local storage.
        :type thread_key: str, optional

        :return: The thread object after creation or update.
        :rtype: Thread
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
        Retrieves all threads stored in local storage.

        This method reads the entire local shelve database and returns its contents 
        as a dictionary. The dictionary maps thread keys to thread IDs.

        :return: A dictionary of thread keys and their corresponding IDs.
        :rtype: dict
        """
        shelf_dict = {}
        with shelve.open("threads_db") as threads_shelf:
            for key in threads_shelf:
                shelf_dict[key] = threads_shelf[key]
        
        self.local_thread_dict = shelf_dict
        return shelf_dict
    

    def get_messages_remote(self, thread):
        """
        Retrieves the message history for a given thread from the OpenAI API.

        This method fetches the message history associated with the specified thread 
        directly from the OpenAI server. The messages are returned in a list, with the 
        latest message at index 0.

        :param thread: The thread object for which to retrieve messages.
        :type thread: Thread

        :return: A list of messages from the thread, latest first.
        :rtype: list
        """
        raw_msg_list = self.client.beta.threads.messages.list(thread.id)
        return [msg.content[0].text.value for msg in raw_msg_list]


    def __repr__(self) -> str:
        """
        Returns a string representation of the current state of local thread storage.

        This method generates a string representation of the threads currently stored 
        in local storage, providing a quick overview of the thread keys and their 
        corresponding IDs.

        :return: A string representation of the local thread storage.
        :rtype: str
        """
        shelf_dict = self.get_threads_local()
        return str(shelf_dict)