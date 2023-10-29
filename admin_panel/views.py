from django.shortcuts import render
from rest_framework import generics
from accounts.models import *
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view



class AdminInstructorListing(generics.ListCreateAPIView):
    queryset = InstructorProfile.objects.all()
    serializer_class = InstructorSerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryListCreateView(generics.ListCreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class SubCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class TagsListCreateView(generics.ListCreateAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class TagsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer    


@api_view(['PUT'])
def course_approval_toggle(request,course_id):
    try:
        course = Course.objects.get(id=course_id)
        course.is_approved = not course.is_approved
        course.save()
        serializer = CourseSerializerAdmin(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Course.DoesNotExist:
        return Response({'details':'course not found'}, status=status.HTTP_404_NOT_FOUND)


class PendingCourseListView(generics.ListAPIView):
    queryset = Course.objects.filter(is_approved=False)
    serializer_class = CourseSerializerAdmin


class ApprovedCoursesListView(generics.ListAPIView):
    queryset = Course.objects.filter(is_approved=True)
    serializer_class = CourseSerializerAdmin
