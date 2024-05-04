from django.shortcuts import render
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .helpers import create_assistant
from time import sleep
from openai import OpenAI
import base64
import tempfile
import whisper

class ChatView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client=OpenAI(api_key='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')
        self.model=None
        # self.assistant_id=create_assistant(self.client)
    def load_model(self):
        # Check if the model is already loaded in the cache
        if not self.model:
            # Load the model here
            self.model = whisper.load_model("tiny")

    def get_medical_advice(self,user_input):
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a medical chatbot that diagnoses diseases. User will input in the form: Symptoms: \"....\", Pulse Rate: \"...\", Blood Pressure: \"....\", Oxygen level: \"....\", Temperature: \".....\" , you have to provide output in the form: Predicted disease: \"....\" , Treatment Plan: \"....\", Prescribed Drugs: \"....\", Specialization: \"....\". Prescribe safe drugs based on treatment plan. For specialization, if treatment plan involves visiting a doctor, it specifies which specialization of doctor to visit. Also some inputs from user may be unknown, diagnose and provide output with rest known inputs."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return response.choices[0].message.content

    def post(self,request):
        if not request.data['pulse_rate']:
            return Response({"message":"Please provide pulse_rate"},400)
        
        if not request.data['blood_pressure']:
            return Response({"message":"Please provide blood pressure"},400)
        
        if not request.data['oxygen_level']:
            return Response({"message":"Please provide oxygen level"},400)
        
        if not request.data['temperature']:
            return Response({"message":"Please provide temperature"},400)

        pulse_rate=request.data['pulse_rate']
        blood_pressure=request.data['blood_pressure']
        oxygen_level=request.data['oxygen_level']
        temperature=request.data['temperature']
        symptoms=""
        if request.data['text']!="":
            symptoms=request.data['text']
        else:
            audio_data = request.data['audio']

            # Load the model
            self.load_model()

            result = self.model.transcribe(audio_data,language="english")
            print(f' The text in video: \n {result["text"]}')
            symptoms=result["text"]
        user_input = f"Symptoms: \"{symptoms}\", Pulse Rate: \"{pulse_rate}\", Blood Pressure: \"{blood_pressure}\", Oxygen level: \"{oxygen_level}\", Temperature: \"{temperature}\""


        advice = self.get_medical_advice(user_input)
        print(advice)   
        return Response({"message":advice},200)
