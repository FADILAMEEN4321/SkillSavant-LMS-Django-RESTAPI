from django.urls import path
from .views import *

urlpatterns = [
    path('latest-courses/',LastestCourseListingView.as_view(), name="latest-courses/"),
    path('popular-courses/',PopularCourseListingView.as_view(), name="popular-courses/"),
    path('all-courses/',AllCourseListingView.as_view(), name="all-courses"),
    path('categories-subcategories/',CategorySubcategoryListingView.as_view(), name="categories-subcategories"),
    path('tags/',TagsListingView.as_view(), name="tags"),
    path('single-course-details/<int:pk>/',CourseDetailView.as_view(), name="single-course-details"),
    path('add_favourite_course/',FavouriteCourseAddView.as_view(), name="add_favourite_course"),
    path('remove_favourite_course/<int:student_id>/<int:course_id>/',FavouriteCourseRemoveView.as_view(), name="remove_favourite_course"),
    path('list-all-favourite-courses/<int:student_id>/',FavouriteCourseListingView.as_view(), name="list-all-favourite-courses"),

]
