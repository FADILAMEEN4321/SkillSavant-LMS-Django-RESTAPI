from rest_framework.response import Response
from rest_framework.views import APIView
from course.models import Course
from rest_framework import status
from rest_framework.exceptions import NotFound
from accounts.models import StudentProfile
from .models import EnrolledCourse, ModuleProgress
from rest_framework import generics
from .serializer import EnrolledCourseSerializer
from accounts.permissions import IsStudent
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class VerifyCourseEnrollEligibility(APIView):
    permission_classes = [IsStudent]

    def get(self, request, course_id, student_id):
        try:
            course = Course.objects.get(id=course_id)
            student = StudentProfile.objects.get(id=student_id)

            if EnrolledCourse.objects.filter(course=course, student=student).exists():
                response = {"message": "You are already enrolled in this course."}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            if course.is_approved == True and course.unlisted == False:
                response = {
                    "message": "course is eligible for enrollment.course is approved and listed."
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    "message": "sorry there is some issue regarding the enrollment of this course."
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        except Course.DoesNotExist:
            raise NotFound("Course not found")
        except StudentProfile.DoesNotExist:
            raise NotFound("Student not found.")

        except Exception as e:
            response = {
                "message": "An error occurred while verifying course eligibility.",
                "error": e,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EnrolledCourseListView(generics.ListAPIView):
    queryset = EnrolledCourse.objects.all()
    serializer_class = EnrolledCourseSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return EnrolledCourse.objects.filter(student=self.request.user.studentprofile)


class ModuleCompletionMarkingView(APIView):
    """
    API endpoint for marking a module as completed.
    """

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "module_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "student_id": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=["module_id", "student_id"],
        ),
        responses={
            200: "Module marked as completed",
            400: "Bad request. Invalid data provided.",
            404: "Module progress not found",
        },
    )
    def post(self, request):
        """
        Handle POST requests for marking a module as completed.

        """
        module_id = request.data.get("module_id")
        student_id = request.data.get("student_id")
        if module_id is not None and student_id is not None:
            try:
                module_progress = ModuleProgress.objects.get(
                    module=module_id, student=student_id
                )
                module_progress.mark_as_completed()
                return Response(
                    {"message": "Module marked as completed"}, status=status.HTTP_200_OK
                )

            except ModuleProgress.DoesNotExist:
                return Response(
                    {"error": "Module progress not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
