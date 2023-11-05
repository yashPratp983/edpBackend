from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime
from .helpers import send_otp

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        phone_number = serializer.data['phone_number']
        otp = send_otp(phone_number)
        if otp is None:
            raise AuthenticationFailed('OTP not sent! Please try again')
        user = User.objects.filter(phone_number=phone_number).first()
        user.otp = otp
        user.save()
        return Response({"message": "User created successfully", "data": serializer.data}, status=201)
    
class LoginView(APIView):
    def post(self, request):
        phone = request.data['phone_number']
        password = request.data['password']
        
        user = User.objects.filter(phone_number=phone).first()
        
        if user is None:
            raise AuthenticationFailed('User not found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Wrong Password!')
        
        if not user.is_verified:
            raise AuthenticationFailed('Account is not verified!')
        
        
        payload = {
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response
    
class VerifyPhoneNumber(APIView):
    def post(self, request):
        phone_number = request.data['phone_number']
        otp_sent = request.data['otp']
        otp_sent = int(otp_sent)
        
        user = User.objects.filter(phone_number=phone_number).first()
        print(user.otp)
        
        if user is None:
            raise AuthenticationFailed('User not found!')
        
        if otp_sent != user.otp:
            raise AuthenticationFailed('Invalid OTP!')
        
        user.is_verified = True
        user.save()
        
        return Response({"message": "Phone number verified successfully"}, status=200)
    
class ResendOTP(APIView):
    def get(self, request):
        phone_number = request.data['phone_number']
        
        user = User.objects.filter(phone_number=phone_number).first()
        
        if user is None:
            raise AuthenticationFailed('User not found!')
        
        otp = send_otp(phone_number)
        if otp is None:
            raise AuthenticationFailed('OTP not sent! Please try again')
        user.otp = otp
        user.save()
        return Response({"message": "OTP sent successfully"}, status=200)
    
    

class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response