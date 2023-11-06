from django.urls import path
from .views import *


urlpatterns = [
     path('admin/instructors-listing/', AdminInstructorListing.as_view(), name='admin-instructors'),

     path('admin/categories-list-create/', CategoryListCreateView.as_view(), name='category-list-create'),
     path('admin/categories-retrieve-update-destroy/<int:pk>/', CategoryDetailView.as_view(), name='categories-retrieve-update-destroy'),

     path('admin/subcategories-list-create/', SubCategoryListCreateView.as_view(), name='subcategory-list-create'),
     path('admin/subcategories-retrieve-update-destroy/<int:pk>/', SubCategoryDetailView.as_view(), name='subcategories-retrieve-update-destroy'),

     path('admin/tags-list-create/', TagsListCreateView.as_view(), name='tags-list-create'),
     path('admin/tags-retrieve-update-destroy/<int:pk>/', TagsDetailView.as_view(), name='tags-retrieve-update-destroy'),

     path('admin/course-approval-toggle/<int:course_id>/',course_approval_toggle, name="course-approval-toggle"),

     path('admin/pending-courses/',PendingCourseListView.as_view(), name="pending-courses"),
     path('admin/approved-courses/',ApprovedCoursesListView.as_view(), name="approved-courses"),





    
]
