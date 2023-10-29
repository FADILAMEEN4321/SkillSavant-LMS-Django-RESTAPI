from django.urls import path
from .views import *

urlpatterns = [
    path('courses/create/', CourseView.as_view(), name='create-course'),

    path('modules/create/', ModuleView.as_view(), name='create-module'),
    path('instructor-courses/<int:instructor_id>/', CourseView.as_view(), name='instructor-courses'),

    path('courses-details/<int:pk>/', CourseDetailView.as_view(), name='courses-details'),


]
