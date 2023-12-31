from django.urls import path
from .views import *

urlpatterns = [
    path('verify-course/<int:course_id>/<int:student_id>/',VerifyCourseEnrollEligibility.as_view(), name="verify-course"),
    path('enrolled-courses/',EnrolledCourseListView.as_view(), name='enrolled-courses'),
    path('mark_module_completed/', ModuleCompletionMarkingView.as_view(), name='mark_module_completed'),
]
