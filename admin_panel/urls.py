from django.urls import path
from .views import *


urlpatterns = [
     path('admin/instructors/', AdminInstructorListing.as_view(), name='admin-instructors'),
    
]
