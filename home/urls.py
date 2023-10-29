from django.urls import path
from .views import *

urlpatterns = [
    path('latest-courses/',LastestCourseListingView.as_view(), name="latest-courses/"),
    path('popular-courses/',PopularCourseListingView.as_view(), name="popular-courses/"),
]
