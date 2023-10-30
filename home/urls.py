from django.urls import path
from .views import *

urlpatterns = [
    path('latest-courses/',LastestCourseListingView.as_view(), name="latest-courses/"),
    path('popular-courses/',PopularCourseListingView.as_view(), name="popular-courses/"),
    path('all-courses/',AllCourseListingView.as_view(), name="all-courses"),
    path('categories-subcategories/',CategorySubcategoryListingView.as_view(), name="categories-subcategories"),
    path('tags/',TagsListingView.as_view(), name="tags"),
    path('single-course-details/<int:pk>/',CourseDetailView.as_view(), name="single-course-details"),

]
