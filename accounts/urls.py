from django.urls import path,include
from .views import *


urlpatterns = [
     path('student-login/',StudentLoginAPI.as_view()),
     path('student-profile-view-update/<int:user_id>/', StudentProfileViewAndEdit.as_view(), name='student-profile'),
     path('student-signup/', StudentSignupAPI.as_view(), name='student-signup'),


     path('instructor-signup/', InstructorSignupAPI.as_view(), name='instructor-signup'),
     path('instructor-login/',InstructorLoginAPI.as_view(), name="instructor-login"),



     path('admin-login/',AdminLoginAPI.as_view(), name="admin-login"),
     path('admin-signup/', AdminSignupAPI.as_view(), name='admin-signup'),
     path('admin/students/', AdminStudentListing.as_view(), name='admin-students'),
     path('admin/students-block-unblock/<int:user_id>/', block_unblock_user, name='admin-block-unblock'),


]