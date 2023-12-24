from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.shortcuts import get_object_or_404
from .permissions import IsAdminUser
from rest_framework import generics
from rest_framework.decorators import api_view
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from .emails import send_otp_via_email,send_otp_via_email_to_instructor
from drf_yasg.utils import swagger_auto_schema


class RefreshTokenView(APIView):
    def post(self, request):
        try:
            # Check if the request contains a valid refresh token
            refresh_token = request.data.get("refresh", None)

            if not refresh_token:
                return Response(
                    {"error": "No valid refresh token provided."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Attempt to validate the refresh token
            try:
                refresh = RefreshToken(refresh_token)

                # If no exception is raised, it's a valid refresh token
            except jwt.ExpiredSignatureError:
                return Response(
                    {"error": "Refresh token has expired."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            except jwt.InvalidTokenError:
                return Response(
                    {"error": "Invalid refresh token."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # Decode the refresh token
            decoded_payload = jwt.decode(
                jwt=refresh_token, key=settings.SECRET_KEY, algorithms=["HS256"]
            )

            # Get the user_id from the decoded payload
            user_id = decoded_payload.get("user_id")

            # Get the user from the Django model using the user_id
            user = get_user_model().objects.get(id=user_id)

            # Create a new refresh token for the user
            new_refresh = RefreshToken.for_user(user)
            new_refresh["role"] = user.role
            new_refresh["email"] = user.email
            new_refresh["first_name"] = user.first_name
            new_refresh["last_name"] = user.last_name

            data = {
                "refresh": str(new_refresh),
                "access": str(new_refresh.access_token),
            }

            return Response(data, status=status.HTTP_200_OK)

        except get_user_model().DoesNotExist:
            return Response(
                {"error": "User associated with the refresh token does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {"error": f"error: {e}"}, status=status.HTTP_400_BAD_REQUEST
            )


# Login View for student
class StudentLoginAPI(APIView):
    """
    API endpoint for student login.
    """
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: "Authentication successful",
            400: "Invalid credentials or invalid data",
            403: "Account blocked or verification pending",
            500: "Internal server error",
        },
    )
    def post(self, request):
        """
        Handle POST requests for student login.

        :param request: The incoming request object.
        :return: JSON response with authentication tokens or error message.
        """

        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                email = "student-" + serializer.data["email"]
                password = serializer.data["password"]

                user = authenticate(email=email, password=password)

                if user is None or user.role != "student":
                    data = {
                        "message": "Invalid credentials",
                    }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
                
                if not user.is_verified:
                    data = {
                        'message':'Please verify your account.'
                    }
                    return Response(data,status=status.HTTP_400_BAD_REQUEST)

                if user.is_blocked:
                    data = {
                        "message": "Your account is blocked. Please contact support for assistance."
                    }
                    return Response(data, status=status.HTTP_403_FORBIDDEN)

                refresh = RefreshToken.for_user(user)
                refresh["role"] = user.role
                refresh["email"] = user.email
                refresh["first_name"] = user.first_name
                refresh["last_name"] = user.last_name
                data = {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
                return Response(data, status=status.HTTP_200_OK)

            return Response(
                {"message": "something went wrong", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            print(e)
            return Response(
                {"message": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class StudentSignupAPI(APIView):
    """
    API endpoint for student signup.
    """
    @swagger_auto_schema(
        request_body=SignupSerializer,
        responses={
            200: "Registration successful",
            400: "Invalid data or email already registered",
            400: "Internal server error",
        },
    )
    def post(self, request):
        """
        Handle POST requests for student signup.

        :param request: The incoming request object.
        :return: JSON response with registration status or error message.
        """
        try:
            data = request.data
            serializer = SignupSerializer(data=data)

            if serializer.is_valid():
                student_email = "student-" + serializer.data["email"]
                print(student_email)
                if CustomUser.objects.filter(email=student_email).exists():
                    response = {
                        "message": "Email Already registered. Login or resend otp to verify account."
                    }
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
                user_data = serializer.validated_data
                user = CustomUser(
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    email="student-" + user_data["email"],
                    role="student",
                )
                user.set_password(user_data["password"])
                user.save()

                # sending email and saving otp to user
                send_otp_via_email(serializer.data["email"])

                # Creating student profile.
                StudentProfile.objects.create(user=user)

                return Response(
                    {
                        "status": 200,
                        "message": "registration successfull. Check email to verify account",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "status": 400,
                    "message": "something went wrong.",
                    "data": serializer.errors,
                }
            )

        except Exception as e:
            print(e)
            return Response(
                {"status": 400, "message": f"{e}"}, status=status.HTTP_400_BAD_REQUEST
            )


class VerifyStudentOTP(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = VerfiyAccountSerializer(data=data)

            if serializer.is_valid():
                email = "student-" + serializer.data["email"]
                otp = serializer.data["otp"]

                user = CustomUser.objects.filter(email=email)
                if not user.exists():
                    return Response(
                        {
                            "status": 400,
                            "message": "something went wrong.",
                            "data": "invalid email",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if not user[0].otp == otp:
                    return Response(
                        {
                            "status": 400,
                            "message": "something went wrong.",
                            "data": "invalid otp",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                user = user.first()
                user.is_verified = True
                user.save()

                return Response(
                    {
                        "status": 200,
                        "message": "Account verified.",
                        "data": {},
                    },
                    status=status.HTTP_200_OK,
                )

        except Exception as e:
            print(e)
            return Response(
                {"status": 400, "message": f"{e}"}, status=status.HTTP_400_BAD_REQUEST
            )



class StudentProfileViewAndEdit(APIView):
    def get(self, request, user_id):
        student_profile = get_object_or_404(StudentProfile, user=user_id)
        print(student_profile.bio)
        serializer = StudentProfileSerializer(student_profile)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        student_profile = get_object_or_404(StudentProfile, user=user_id)
        student_user = student_profile.user

        student_serializer = StudentListingSerializer(
            student_profile, data=request.data.get("student_profile"), partial=True
        )
        user_serializer = CustomUserSerializer(
            student_user, data=request.data.get("user"), partial=True
        )

        if student_serializer.is_valid() and user_serializer.is_valid():
            student = student_serializer.save()
            user = user_serializer.save()

            print("student-data----->", student.user.first_name, student.bio)
            return Response(
                {
                    "message": "Profile updated successfully",
                },
                status=status.HTTP_200_OK,
            )

        # Return errors if either serializer is invalid
        errors = {
            "profile_errors": student_serializer.errors
            if not student_serializer.is_valid()
            else None,
            "user_errors": user_serializer.errors
            if not user_serializer.is_valid()
            else None,
        }

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class InstructorProfileViewAndEdit(APIView):
    def get(self, request, user_id):
        instructor_profile = get_object_or_404(InstructorProfile, user=user_id)
        print(instructor_profile.bio)
        serializer = InstructorProfileSerializer(instructor_profile)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        instructor_profile = get_object_or_404(InstructorProfile, user=user_id)
        instructor_user = instructor_profile.user

        instructor_serializer = InstructorProfileSerializer(
            instructor_profile,
            data=request.data.get("instructor_profile"),
            partial=True,
        )
        user_serializer = CustomUserSerializer(
            instructor_user, data=request.data.get("user"), partial=True
        )

        if instructor_serializer.is_valid() and user_serializer.is_valid():
            instructor = instructor_serializer.save()
            user = user_serializer.save()
            instructor.save()
            user.save()
            user_data = {"first_name": user.first_name, "last_name": user.last_name}
            instructor_data = {"state": instructor.state, "bio": instructor.bio}

            print("student-data----->", instructor.user.first_name, instructor.bio)
            return Response(
                {"message": "Profile updated successfully"}, status=status.HTTP_200_OK
            )

        # Return errors if either serializer is invalid
        errors = {
            "profile_errors": instructor_serializer.errors
            if not instructor_serializer.is_valid()
            else None,
            "user_errors": user_serializer.errors
            if not user_serializer.is_valid()
            else None,
        }

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    


class InstructorSignupAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = SignupSerializer(data=data)

            if serializer.is_valid():
                instructor_email = "instructor-" + serializer.data["email"]
                print(instructor_email)

                if CustomUser.objects.filter(email=instructor_email).exists():
                    response = {
                        "message": "Email Already registered. Login or resend otp to verify account."
                    }
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
                user_data = serializer.validated_data
                user = CustomUser(
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    email="instructor-" + user_data["email"],
                    role="instructor",
                )
                user.set_password(user_data["password"])
                user.save()

                # sending email and saving otp to user
                send_otp_via_email_to_instructor(serializer.data["email"])

                # Creating student profile.
                InstructorProfile.objects.create(user=user)

                return Response(
                    {
                        "status": 200,
                        "message": "registration successfull. Check email to verify account",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "status": 400,
                    "message": "something went wrong.",
                    "data": serializer.errors,
                }
            )

        except Exception as e:
            print(e)
            return Response(
                {"status": 400, "message": f"{e}"}, status=status.HTTP_400_BAD_REQUEST
            )    
        

class VerifyInstructorOTP(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = VerfiyAccountSerializer(data=data)

            if serializer.is_valid():
                email = "instructor-" + serializer.data["email"]
                otp = serializer.data["otp"]

                user = CustomUser.objects.filter(email=email)
                if not user.exists():
                    return Response(
                        {
                            "status": 400,
                            "message": "something went wrong.",
                            "data": "invalid email",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if not user[0].otp == otp:
                    return Response(
                        {
                            "status": 400,
                            "message": "something went wrong.",
                            "data": "invalid otp",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                user = user.first()
                user.is_verified = True
                user.save()

                return Response(
                    {
                        "status": 200,
                        "message": "Account verified.",
                        "data": {},
                    },
                    status=status.HTTP_200_OK,
                )

        except Exception as e:
            print(e)
            return Response(
                {"status": 400, "message": f"{e}"}, status=status.HTTP_400_BAD_REQUEST
            )





class InstructorLoginAPI(APIView):
    """
    API endpoint for instructor login.
    """

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: "Authentication successful",
            400: "Invalid credentials or invalid data",
            500: "Internal server error",
        },
    )
    def post(self, request):
        """
        Handle POST requests for instructor login.

        :param request: The incoming request object.
        :return: JSON response with authentication tokens or error message.
        """
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                email = "instructor-" + serializer.data["email"]
                password = serializer.data["password"]

                user = authenticate(email=email, password=password)

                if user is None or user.role != "instructor":
                    data = {
                        "message": "invalid credentials",
                    }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)

                refresh = RefreshToken.for_user(user)
                refresh["role"] = user.role
                refresh["email"] = user.email
                refresh["first_name"] = user.first_name
                refresh["last_name"] = user.last_name

                instructor = InstructorProfile.objects.get(user=user)
                serializer = InstructorProfileSerializer(instructor)
                instructor_data = serializer.data

                data = {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    # 'instructor_data':instructor_data,
                    # 'email': str(user.email)
                }
                return Response(data, status=status.HTTP_200_OK)

            return Response(
                {
                    "status": 400,
                    "message": "something went wrong",
                    "data": serializer.errors,
                }
            )

        except Exception as e:
            print(e)
            return Response(
                {
                    "status": 500,
                    "message": "Internal server error",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# Login View for Admin
class AdminLoginAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                email = "admin-" + serializer.data["email"]
                password = serializer.data["password"]

                user = authenticate(email=email, password=password)

                if user is None or user.role != "admin":
                    data = {
                        "message": "invalid credentials",
                    }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)

                refresh = RefreshToken.for_user(user)
                refresh["role"] = user.role
                refresh["email"] = user.email
                refresh["first_name"] = user.first_name
                data = {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    # 'email': str(user.email)
                }
                return Response(data, status=status.HTTP_200_OK)

            return Response(
                {
                    "status": 400,
                    "message": "something went wrong",
                    "data": serializer.errors,
                }
            )

        except Exception as e:
            print(e)


class AdminSignupAPI(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            user = serializer.save()
            user.set_password(user_data["password"])
            user.email = "admin-" + user_data["email"]
            user.phone_number = "admin-" + user_data["phone_number"]
            user.role = "admin"
            user.save()

            AdminProfile.objects.create(user=user)
            return Response(
                {"message": "Account created successfully."},
                status=status.HTTP_201_CREATED,
            )
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminStudentListing(generics.ListCreateAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentListingSerializer
    permission_classes = [IsAdminUser]


@api_view(["POST"])
def block_unblock_user(request, user_id):
    try:
        student = CustomUser.objects.get(id=user_id, role="student")
        student.is_blocked = not student.is_blocked
        student.save()
        serializer = CustomUserSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except CustomUser.DoesNotExist:
        return Response(
            {"detail": "Student not found"}, status=status.HTTP_404_NOT_FOUND
        )
