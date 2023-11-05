from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'password', 'email', 'phone_number', 'gender', 'age']
        extra_kwargs = {
            'password':{'write_only':True}
        }
        
    def save(self):
        password = self.validated_data['password']
        if User.objects.filter(phone_number=self.validated_data['phone_number']).exists():
            raise serializers.ValidationError({'error':'User with same phone_number has already been registered'})
        if password is None:
            raise serializers.ValidationError({'error':'Password is required'})
        account=User(phone_number=self.validated_data['phone_number'],name=self.validated_data['name'],email=self.validated_data['email'],gender=self.validated_data['gender'],age=self.validated_data['age'])
        account.set_password(password)
        account.save()
        return account