from rest_framework.response import Response
from rest_framework.views import APIView
from course.models import Course
from rest_framework import status
from rest_framework.exceptions import NotFound
from accounts.models import StudentProfile
from .models import EnrolledCourse
from rest_framework import generics
from .serializer import EnrolledCourseSerializer
from accounts.permissions import IsStudent



class VerifyCourseEnrollEligibility(APIView):
     def get(self,request, course_id, student_id):
          try:
            course = Course.objects.get(id = course_id)
            student = StudentProfile.objects.get(id = student_id)

            if EnrolledCourse.objects.filter(course=course,student=student).exists():
                response = {
                    "message":"You are already enrolled in this course."
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)


            if course.is_approved == True and course.unlisted == False:
                response = {
                    "message":"course is eligible for enrollment.course is approved and listed."
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    "message":"sorry there is some issue regarding the enrollment of this course."
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

          except Course.DoesNotExist:
               raise NotFound("Course not found")
          except StudentProfile.DoesNotExist:
              raise NotFound("Student not found.")
          
          except Exception as e:

            response = {
                "message": "An error occurred while verifying course eligibility.",
                "error":e
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                


class EnrolledCourseListView(generics.ListAPIView):
    queryset = EnrolledCourse.objects.all()
    serializer_class = EnrolledCourseSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return EnrolledCourse.objects.filter(student = self.request.user.studentprofile)             


