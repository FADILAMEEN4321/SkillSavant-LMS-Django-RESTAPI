from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework import generics
from .models import Course, Module
from .serializer import CourseSerializer, ModuleSerializer, CourseAndModuleSerializer
from accounts.permissions import IsInstructor
from rest_framework.permissions import IsAuthenticated
from moviepy.editor import VideoFileClip
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
import io
import os
import tempfile
from datetime import timedelta


class CourseView(APIView):
    permission_classes = [IsInstructor]

    def post(self, request):
        try:
            serializer = CourseSerializer(data=request.data)
            print(request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            print(f"Validation error: {e}")
            return Response(
                {"message": "Validation error", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response(
                {
                    "message": "An error occurred while creating the course.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get(self, request, instructor_id):
        try:
            courses = Course.objects.filter(instructor=instructor_id, unlisted=False)
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Course.DoesNotExist:
            return Response(
                {"message": "No courses found for this instructor."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {
                    "message": "An error occurred while fetching courses.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UnlistCourseView(APIView):
    permission_classes = [IsInstructor]

    def get(self, request, course_id):
        try:
            course = Course.objects.filter(id=course_id).first()

            if not course:
                raise ValueError("Course not found with the given course_id.")

            course.unlisted = True
            course.save()

            response = {"message": "Course unlisted successfully."}
            return Response(response, status=status.HTTP_200_OK)

        except ValueError as ve:
            response = {"error": str(ve)}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            response = {"error": f"An error occurred while processing the request:{e}"}
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ModuleView(APIView):
    def post(
        self,
        request,
    ):
        try:
            serializer = ModuleSerializer(data=request.data)

            if serializer.is_valid():
                module_order = serializer.validated_data.get("module_order")
                course_id = serializer.validated_data.get("course")

                if Module.objects.filter(
                    course=course_id, module_order=module_order
                ).exists():
                    response = {"message": "module order already exists."}
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)

                # Extracting video duration
                video_url = serializer.validated_data.get("video_url")
                duration = self.get_video_duration(video_url)
                serializer.validated_data["duration"] = duration

                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"{e}:error")
            return Response(
                {
                    "message": "An error occurred while creating the module.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_video_duration(self, video_url):
        try:
            if isinstance(video_url, (InMemoryUploadedFile, TemporaryUploadedFile)):
                # Handle both in-memory and on-disk files
                video_content = video_url.read()

                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=".mp4"
                ) as temp_video_file:
                    temp_video_path = temp_video_file.name
                    temp_video_file.write(video_content)

                video_clip = VideoFileClip(temp_video_path)

                video_duration_seconds = int(video_clip.duration)

                # Converting duration to timedelta
                video_duration_timedelta = timedelta(seconds=video_duration_seconds)

                video_clip.close()  # Explicitly closing the video clip
                os.remove(temp_video_path)  # Cleaning up the temporary file

                return video_duration_timedelta
            else:
                raise ValueError("Unsupported file type")

        except Exception as e:
            print(f"Error getting video duration: {e}")
            return timedelta()


class ModuleDeleteView(generics.DestroyAPIView):
    permission_classes = [IsInstructor]
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer


class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseAndModuleSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Retrieve the related modules for the course
        modules = Module.objects.filter(course=instance)
        course_serializer = self.get_serializer(instance)
        module_serializer = ModuleSerializer(modules, many=True, read_only=True)
        course_and_modules_data = {
            "course": course_serializer.data,
            "modules": module_serializer.data,
        }
        return Response(course_and_modules_data)
