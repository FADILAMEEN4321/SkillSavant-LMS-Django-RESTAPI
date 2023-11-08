from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework import generics
from .models import Course,Module
from .serializer import CourseSerializer,ModuleSerializer,CourseAndModuleSerializer
from accounts.permissions import IsInstructor
from rest_framework.permissions import IsAuthenticated



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
            return Response({'message': 'Validation error', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({'message': 'An error occurred while creating the course.', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 

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



class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseAndModuleSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Retrieve the related modules for the course
        modules = Module.objects.filter(course=instance)
        course_serializer = self.get_serializer(instance)
        module_serializer = ModuleSerializer(modules,many=True, read_only=True)
        course_and_modules_data = {
            'course': course_serializer.data,
            'modules': module_serializer.data,
        }
        return Response(course_and_modules_data)






