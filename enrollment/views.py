from rest_framework.response import Response
from rest_framework.views import APIView
from course.models import Course
from rest_framework import status
from rest_framework.exceptions import NotFound



class VerifyCourseEnrollEligibility(APIView):
     def post(self,request, course_id):
          try:
            course = Course.objects.get(id = course_id)
            if course.is_approved == True and course.unlisted == False:
                response = {
                    "message":"course is eligible for enrollment."
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    "message":"sorry there is some issue regarding the enrollment of this course."
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

          except Course.DoesNotExist:
               raise NotFound("Course not found")
          
          except Exception as e:

            response = {
                "message": "An error occurred while verifying course eligibility.",
                "error":e
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
               


