from django.conf import settings
import random
import requests

def send_otp(phone_number):
    try:
        otp = random.randint(100000, 999999)
        url=f'https://2factor.in/API/V1/{settings.API_KEY}/SMS/{phone_number}/{otp}'
        response = requests.get(url)
        print(response.json())
        return otp
    except Exception as e:
        print(e)
        return None