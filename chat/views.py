from django.shortcuts import render
import openai
from openai import OpenAI
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .helpers import create_assistant
from time import sleep

class ChatView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = openai.OpenAI(api_key='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')
        self.assistant_id=create_assistant(self.client)

    def get(self,request):
        print("Starting a new conversation...")  # Debugging line
        thread = self.client.beta.threads.create()
        print(f"New thread created with ID: {thread.id}")  # Debugging line
        return Response({"thread_id":thread.id},status=400)

    def post(self,request):
        # if not request.body.thread:
        #     return Response({"error":"Thread id is not been provided"})
        
        thread_id=request.data['thread']
        user_input=request.data['message']
         # Add the user's message to the thread
        self.client.beta.threads.messages.create(thread_id=thread_id,
                                            role="user",
                                            content=user_input)
        print(self.assistant_id)

        # Run the Assistant
        run = self.client.beta.threads.runs.create(thread_id=thread_id,
                                                assistant_id=self.assistant_id)

        # Check if the Run requires action (function call)
        while True:
            try:
                run_status = self.client.beta.threads.runs.retrieve(thread_id=thread_id,
                                                            run_id=run.id)
                print(run_status)
                if run_status.status == 'completed':
                    break
                sleep(1)  # Wait for a second before checking again
            except Exception as e:
                print(f"Error: {e}")
                break

        # Retrieve and return the latest message from the assistant
        messages = self.client.beta.threads.messages.list(thread_id=thread_id)
        response = messages.data[0].content[0].text.value

        print(f"Assistant response: {response}")  # Debugging line
        return Response({"message":response},200)
