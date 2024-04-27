#main worker class

import json
import time
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from myGpt_utils import wait_on_run, get_response, add_file_ids
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client using the API key from .env file
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# Define worker roles and associated contexts and tools
worker_selection = {
    "SoftwareEngineer": {
        "role_context": 'You are a powerful coding assistant',
        "tools": [{"type": "code_interpreter"}]
    },
    "Writer": {
        "role_context": 'You are a insight writing assistant',
        "tools": None
    }
}

# Define models
models = {
    'gpt3': "gpt-3.5-turbo-1106",
    'gpt4': "gpt-4-1106-preview"
}

# Worker class definition with methods for interaction and management
class GptAgent:
    def __init__(self, name, role_context=None, model="gpt-3.5-turbo-1106", **kwargs):
        assistant_kwargs = {
            'name': name,
            'instructions': role_context,
            'model': model
        }
        # Add any additional kwargs passed to the constructor
        assistant_kwargs.update(kwargs)
        # Create an assistant with the specified properties
        self.assistant = client.beta.assistants.create(**assistant_kwargs)
        self.thread = None
        self.run = None
        self.name = name
        self.role_context = role_context
        self.tools = kwargs.get('tools')  # Save tools if provided
        self.model = model
        self.thread_id = ''
        self.uploaded_files = {}  # Initialize an empty dict for uploaded files

    def __str__(self):
        # Represent the Worker as a string
        return f"Worker(Name: {self.name}, Role Context: {self.role_context})"

    def create_thread_and_run(self, user_input):
        # Create a new thread and submit a message
        self.thread = client.beta.threads.create()
        self.thread_id = self.thread.id
        self.submit_message(self.thread_id, user_input)

    def continue_thread(self, user_input):
        # Submit a message to continue an existing thread
        self.submit_message(self.thread_id, user_input)

    # Internal method for submitting messages, printing prompts, and waiting for responses
    def submit_message(self, thread_id, user_message):
        print('===============================================================')
        print('                             USER')
        print('===============================================================')
        print(user_message)

        # Create a message and run thread
        client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=user_message
        )
        self.run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant.id,
        )

        # Wait for the run to complete
        self.run = wait_on_run(self, self.run, thread_id)
        # Retrieve the response
        self.response = get_response(thread_id)

    def upload_file_to_assistant(self, file_names):
        # Upload files to the assistant and update the uploaded files dictionary
        file_ids = add_file_ids(file_names)
        self.uploaded_files.update(file_ids)
        client.beta.assistants.update(self.assistant.id, file_ids=list(file_ids.keys()))