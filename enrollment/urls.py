from django.urls import path
from .views import *

urlpatterns = [
    path('verify-course/<int:course_id>/<int:student_id>/',VerifyCourseEnrollEligibility.as_view(), name="verify-course"),
]
