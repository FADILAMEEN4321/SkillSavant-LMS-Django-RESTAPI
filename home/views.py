from django.shortcuts import render
from rest_framework import generics
from course.models import Course,Category,SubCategory,Tags,FavouriteCourses
from .serializer import (
    CourseSerializerHome,
    CategorySubcategorySerializer,
    TagsSerializer,
    CourseDetailSerializer,
    FavouriteCourseSerializer
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound




class LastestCourseListingView(generics.ListAPIView):
    queryset = Course.objects.filter(is_approved = True, unlisted = False).order_by('-created_at')[:5]
    serializer_class = CourseSerializerHome


class PopularCourseListingView(generics.ListAPIView):
    queryset = Course.objects.filter(is_approved = True, unlisted = False)[:5]
    serializer_class = CourseSerializerHome


class AllCourseListingView(generics.ListAPIView):
    queryset = Course.objects.filter(is_approved = True, unlisted = False)
    serializer_class = CourseSerializerHome

    # def get_queryset(self):
    #     # Include additional queryset filtering if needed
    #     queryset = Course.objects.filter(is_approved=True, unlisted=False)
    #     return queryset
    
    # def list(self, request, *args, **kwargs):
    #     # Pass request context to serializer
    #     serializer = self.get_serializer(self.get_queryset(), context={'request': request}, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class CategorySubcategoryListingView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySubcategorySerializer


class TagsListingView(generics.ListAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer  


class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer   


class FavouriteCourseAddView(generics.CreateAPIView):
    queryset = FavouriteCourses.objects.all()
    serializer_class = FavouriteCourseSerializer


class FavouriteCourseRemoveView(generics.DestroyAPIView):
    serializer_class = FavouriteCourseSerializer

    def get_object(self):
        course_id = self.kwargs.get('course_id')
        student_id = self.kwargs.get('student_id')
        print('course-id--->',course_id)
        print('student-id--->',student_id)

        favorite_course = FavouriteCourses.objects.filter(
            course=course_id,
            student = student_id
        ).first()

        if not favorite_course:
            raise NotFound("Favorite course not found")

        return favorite_course
    
   
    



