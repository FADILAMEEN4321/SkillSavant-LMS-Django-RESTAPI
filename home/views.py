from django.shortcuts import render
from rest_framework import generics
from course.models import Course,Category,SubCategory,Tags
from .serializer import CourseSerializerHome,CategorySubcategorySerializer,TagsSerializer,CourseDetailSerializer


class LastestCourseListingView(generics.ListAPIView):
    queryset = Course.objects.filter(is_approved = True, unlisted = False).order_by('-created_at')[:5]
    serializer_class = CourseSerializerHome


class PopularCourseListingView(generics.ListAPIView):
    queryset = Course.objects.filter(is_approved = True, unlisted = False)[:5]
    serializer_class = CourseSerializerHome


class AllCourseListingView(generics.ListAPIView):
    queryset = Course.objects.filter(is_approved = True, unlisted = False)
    serializer_class = CourseSerializerHome


class CategorySubcategoryListingView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySubcategorySerializer


class TagsListingView(generics.ListAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer  


class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer      