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
from pydub import AudioSegment
from django.http import JsonResponse
import io
import json
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationChain 
import base64
from tensorflow.keras.models import load_model
import tensorflow as tf
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory


review_template = """\
For the following text, extract the following information:

Symtoms: what are the symptoms of the patient?
Answer output them as a comma separated Python list.

Format the output as JSON with the following keys:
Symptoms

text: {text}
"""

os.environ['OPENAI_API_KEY'] = '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'

class ChatView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client=OpenAI(api_key='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')
        self.model=None
        self.model2=None
        # self.assistant_id=create_assistant(self.client)
    def load_model(self):
        # Check if the model is already loaded in the cache
        if not self.model:
            # Load the model here
            self.model = whisper.load_model("/home/nomnom/Documents/models/medium.pt")

    def get_medical_advice(self,user_input):
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a medical chatbot that diagnoses diseases. User will input in the form: Symptoms: \"....\", Pulse Rate: \"...\", Oxygen level: \"....\", Temperature: \".....\" , you have to provide output in the form: Predicted disease: \"....\" , Treatment Plan: \"....\", Prescribed Drugs: \"....\", Specialization: \"....\". Prescribe safe drugs based on treatment plan. For specialization, if treatment plan involves visiting a doctor, it specifies which specialization of doctor to visit. Also some inputs from user may be unknown, diagnose and provide output with rest known inputs."
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
    
    def put(self,request):
        audio_file = request.FILES.get('audio_data')
        if audio_file:
            audio_data = audio_file.read()
            audio_format = request.POST.get('type', 'wav')

            # Convert audio data to AudioSegment
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_data))

            # Save AudioSegment as MP3 file
            audio_segment.export('audio.mp3', format='mp3')

            return JsonResponse({'message': 'Audio file saved as MP3'})
        else:
            return JsonResponse({'error': 'No audio file provided'}, status=400)


    def post(self,request):
        print(request.data)
        if request.data['image']:
            image_path = 'output_image.jpg'
            base64_image_data = request.data['image'].replace('data:image/jpeg;base64,', '')
            decoded_image_data = base64.b64decode(base64_image_data)
            with open('output_image.jpg', 'wb') as f:
                f.write(decoded_image_data)
            
            self.load_image_model()
            image = tf.io.read_file(image_path)
            image = tf.io.decode_jpeg(image, channels=3)
            image = tf.image.convert_image_dtype(image, tf.float32)
            image = tf.image.resize(image, (224, 224))  # Resize the image as needed
            image = tf.expand_dims(image, axis=0)
            prediction = self.model2.predict(image)
            prediction = prediction[0]
            sum=0
            for i in range(len(prediction)):
                sum+=prediction[i]
            
            print(len(prediction))
            return Response({"message":prediction},200)

        if not request.data['pulse_rate']:
            return Response({"message":"Please provide pulse_rate"},400)
        
        if not request.data['oxygen_level']:
            return Response({"message":"Please provide oxygen level"},400)
        
        if not request.data['temperature']:
            return Response({"message":"Please provide temperature"},400)

        pulse_rate=request.data['pulse_rate']
        oxygen_level=request.data['oxygen_level']
        temperature=request.data['temperature']
        symptoms=""
        if request.data['text']!="":
            symptoms=request.data['text']
        else:
            # Load the model
            self.load_model()
            print("Model loaded")
            result = self.model.transcribe("audio.mp3",language="english")
            print(f' The text in video: \n {result["text"]}')
            txt=result["text"]
            prompt = ChatPromptTemplate.from_template(review_template)
            turbo_llm_memory = ChatOpenAI(
                temperature=0,
                model_name='gpt-4-turbo'
            )
            prompt_txt = prompt.format_messages(text=txt)
            memory = ConversationBufferWindowMemory(k=1)
            memory.save_context({"input": "Hi"},
                                {"output": "What's up"})
            memory.save_context({"input": "Not much, just hanging"},
                                {"output": "Cool"})
            memory.load_memory_variables({})
            memory_llm_conversation = ConversationChain(
                llm=turbo_llm_memory, 
                verbose=True
            )
            res = memory_llm_conversation(prompt_txt)
            symptoms=res['response']
            print(symptoms,"symptoms")
            a=symptoms.split(":")
            a=a[1]
            a.replace('"','')
            a.replace('}','')
            symptoms=a
            print(symptoms,"symptoms")
        user_input = f"Symptoms: \"{symptoms}\", Pulse Rate: \"{pulse_rate}\", Oxygen level: \"{oxygen_level}\", Temperature: \"{temperature}\""


        advice = self.get_medical_advice(user_input)
        print("Advice:", advice)

    # Split the advice string to extract each attribute
        
        advice_attributes = advice.split("\n")
        if(len(advice_attributes)<4):
            res={"predicted_disease": None,"treatment_plan": None,"prescribed_drugs": None,"specialization": None}

            return Response({"message":res},200)
        
        print("Advice Attributes:", advice_attributes)
        predicted_disease = advice_attributes[0].split(": ")[1].strip('"').replace('",', '')
        treatment_plan = advice_attributes[1].split(": ")[1].strip('"').replace('",', '')
        prescribed_drugs = advice_attributes[2].split(": ")[1].strip('"').replace('",', '')
        specialization = advice_attributes[3].split(": ")[1].strip('"').replace('",', '')

        res={"predicted_disease": predicted_disease,"treatment_plan": treatment_plan,"prescribed_drugs": prescribed_drugs,"specialization": specialization}

        return Response({"message":res},200)
