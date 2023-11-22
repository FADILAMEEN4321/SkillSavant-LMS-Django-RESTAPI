from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password


# Serializer for student,instructor and admin login.
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


#for student signup
class SignupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ('email','first_name','last_name','phone_number','password')
        extra_kwargs = {
            'password':{'write_only':True}
        }

        # def create(self, validated_data):
        #     email = validated_data['email']
        #     first_name = validated_data['first_name']
        #     last_name = validated_data['last_name']
        #     phone_number = validated_data['phone_number']
        #     password = validated_data['password']

        #     if CustomUser.objects.filter(email=email).exists():
        #         raise serializers.ValidationError({'email': 'This email is already in use.'})
            
        #     if CustomUser.objects.filter(phone_number=phone_number).exists():
        #         raise serializers.ValidationError({'phone_number': 'This phone_number is already in use.'})
            
            
        #     user = CustomUser(email=email,first_name=first_name,last_name=last_name,phone_number=phone_number,role='student')
        #     user.set_password(password)
            
        #     user.save()
        #     print(user.password,'----------.password')

        #     return user
            




#for retriving logged in user details
class StudentProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    first_name = serializers.CharField(source="user.first_name")

    class Meta:
        model = StudentProfile
        fields = '__all__' 

    def get_email(self,obj):
        email = obj.user.email
        if email.startswith("student-"):
            return email[len("student-"):]
        return email 


class InstructorProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    first_name = serializers.CharField(source="user.first_name")

    class Meta:
        model = InstructorProfile
        fields = '__all__' 

    def get_email(self,obj):
        email = obj.user.email
        if email.startswith("instructor-"):
            return email[len("instructor-"):]
        return email    


class StudentListingSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    student_name = serializers.CharField(source='user.get_full_name')

    class Meta:
        model = StudentProfile
        fields = '__all__'
        depth = 1 

    def get_email(self,obj):
        email = obj.user.email
        if email.startswith("student-"):
            return email[len("student-"):]
        return email     


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'  

             