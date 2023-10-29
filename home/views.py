from django.shortcuts import render
from rest_framework import generics
from course.models import Course
from .serializer import CourseSerializerHome


class LastestCourseListingView(generics.ListAPIView):
    queryset = Course.objects.filter(is_approved = True).order_by('-created_at')[:5]
    serializer_class = CourseSerializerHome


class PopularCourseListingView(generics.ListAPIView):
    queryset = Course.objects.filter(is_approved = True)[:5]
    serializer_class = CourseSerializerHome