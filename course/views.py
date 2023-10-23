from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Course
from .serializer import CourseSerializer,ModuleSerializer



class CourseView(APIView):
    def post(self, request):
        try:
            serializer = CourseSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            # Handle unexpected exceptions
            return Response({'message': 'An error occurred while creating the course.', 'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self,request,instructor_id):
        try:
            courses = Course.objects.filter(instructor=instructor_id)
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        except Course.DoesNotExist:
            return Response({'message':'No courses found for this instructor.'},status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'message': 'An error occurred while fetching courses.', 'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        


class ModuleView(APIView):
    def post(self, request,):
        try:
            serializer = ModuleSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'message': 'An error occurred while creating the module.', 'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)  





