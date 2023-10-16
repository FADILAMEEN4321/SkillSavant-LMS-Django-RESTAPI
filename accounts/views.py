from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.decorators import api_view




#Login View for student
class StudentLoginAPI(APIView):
    def post(self,request):
        try:
            data = request.data
            serializer = LoginSerializer(data = data)
            if serializer.is_valid():
                email = 'student-' + serializer.data['email']
                password = serializer.data['password']

                user = authenticate(email=email,password=password)

                if user is None or user.role != 'student':
                    data = {
                        'message': 'invalid credentials',
                    }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
                
                refresh = RefreshToken.for_user(user)  
                refresh['role'] = user.role
                refresh['email'] = user.email
                refresh['first_name'] = user.first_name
                refresh['last_name'] = user.last_name
                data = {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        # 'email': str(user.email)

                    }   
                return Response(data, status=status.HTTP_200_OK)
            
            return Response({
                'status':400,
                'message':"something went wrong",
                'data':serializer.errors
            })  

        except Exception as e:
            print(e)  



class StudentSignupAPI(APIView):
    def post(self,request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            # user = serializer.save()
            user = CustomUser(
                first_name = user_data['first_name'],
                last_name = user_data['last_name'],
                email = 'student-' + user_data['email'],
                phone_number = 'student-' + user_data['phone_number'],
                role = 'student'
            )

            user.set_password(user_data['password'] )
            user.save()

            StudentProfile.objects.create(user=user)
            return Response({'message':'Account created successfully.'},status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class StudentProfileViewAndEdit(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self,request,user_id):
        student_profile = get_object_or_404(StudentProfile,user=user_id)
        print(student_profile.bio)
        serializer = StudentProfileSerializer(student_profile)
        print(serializer.data)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,user_id):
        student_profile = get_object_or_404(StudentProfile, user=user_id)
        serializer = CustomUserSerializer(student_profile, data=request.data, partial=True)
        if serializer.is_valid():
            student = serializer.save()
            print('hello',student.user.first_name,student.bio)
            return Response({'message': 'Profile updated successfully',}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
class InstructorSignupAPI(APIView):
    def post(self,request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            # user = serializer.save()
            user = CustomUser(
                first_name = user_data['first_name'],
                last_name = user_data['last_name'],
                email = 'instructor-' + user_data['email'],
                phone_number = 'instructor-' + user_data['phone_number'],
                role = 'instructor'
            )
            user.set_password(user_data['password'] )
            # user.email = 'instructor-' + user_data['email']
            # user.phone_number = 'instructor-' + user_data['phone_number']
            # user.role = 'instructor'
            user.save()

            InstructorProfile.objects.create(user=user)
            return Response({'message':'Account created successfully.'},status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  



#Login View for student
class InstructorLoginAPI(APIView):
    def post(self,request):
        try:
            data = request.data
            serializer = LoginSerializer(data = data)
            if serializer.is_valid():
                email = 'instructor-' + serializer.data['email']
                password = serializer.data['password']

                user = authenticate(email=email,password=password)

                if user is None or user.role != 'instructor':
                    data = {
                        'message': 'invalid credentials',
                    }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
                
                refresh = RefreshToken.for_user(user)  
                refresh['role'] = user.role
                refresh['email'] = user.email
                refresh['first_name'] = user.first_name
                refresh['last_name'] = user.last_name
                data = {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        # 'email': str(user.email)
                    }   
                return Response(data, status=status.HTTP_200_OK)
            
            return Response({
                'status':400,
                'message':"something went wrong",
                'data':serializer.errors
            })  

        except Exception as e:
            print(e)        




#Login View for Admin
class AdminLoginAPI(APIView):
    def post(self,request):
        try:
            data = request.data
            serializer = LoginSerializer(data = data)
            if serializer.is_valid():
                email = 'admin-' + serializer.data['email']
                password = serializer.data['password']

                user = authenticate(email=email,password=password)

                if user is None or user.role != 'admin':
                    data = {
                        'message': 'invalid credentials',
                    }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
                
                refresh = RefreshToken.for_user(user)  
                refresh['role'] = user.role
                refresh['email'] = user.email
                refresh['first_name'] = user.first_name
                data = {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        # 'email': str(user.email)
                    }   
                return Response(data, status=status.HTTP_200_OK)
            
            return Response({
                'status':400,
                'message':"something went wrong",
                'data':serializer.errors
            })  

        except Exception as e:
            print(e)       




class AdminSignupAPI(APIView):
    def post(self,request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            user = serializer.save()
            user.set_password(user_data['password'] )
            user.email = 'admin-' + user_data['email']
            user.phone_number = 'admin-' + user_data['phone_number']
            user.role = 'admin'
            user.save()

            AdminProfile.objects.create(user=user)
            return Response({'message':'Account created successfully.'},status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  




class AdminStudentListing(generics.ListCreateAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentListingSerializer


@api_view(['POST'])
def block_unblock_user(request,user_id):
    try:
        student = CustomUser.objects.get(id=user_id, role='student')
        student.is_blocked = not student.is_blocked
        student.save()
        serializer = CustomUserSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except CustomUser.DoesNotExist:
        return Response({'detail': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

 


