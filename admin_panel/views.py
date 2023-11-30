from rest_framework import generics
from accounts.models import *
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from enrollment.models import Transcation
from accounts.permissions import IsAdminUser,IsInstructor


class AdminInstructorListing(generics.ListCreateAPIView):
    queryset = InstructorProfile.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = [IsAdminUser]


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser | IsInstructor]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser | IsInstructor]


class SubCategoryListCreateView(generics.ListCreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [IsAdminUser | IsInstructor]


class SubCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [IsAdminUser | IsInstructor]


class TagsListCreateView(generics.ListCreateAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [IsAdminUser | IsInstructor]


class TagsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [IsAdminUser | IsInstructor]


@api_view(["PUT"])
def course_approval_toggle(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        course.is_approved = not course.is_approved
        course.save()
        serializer = CourseSerializerAdmin(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Course.DoesNotExist:
        return Response(
            {"details": "course not found"}, status=status.HTTP_404_NOT_FOUND
        )


class PendingCourseListView(generics.ListAPIView):
    queryset = Course.objects.filter(is_approved=False)
    serializer_class = CourseSerializerAdmin
    permission_classes = [IsAdminUser]


class ApprovedCoursesListView(generics.ListAPIView):
    queryset = Course.objects.filter(is_approved=True)
    serializer_class = CourseSerializerAdmin
    permission_classes = [IsAdminUser]


class SalesListView(generics.ListAPIView):
    queryset = Transcation.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAdminUser]
