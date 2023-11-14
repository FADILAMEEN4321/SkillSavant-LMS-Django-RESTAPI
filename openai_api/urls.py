from django.urls import path
from .views import *

urlpatterns = [
    path('learning-path-creation/',LearningPathCreationApi.as_view())
]
