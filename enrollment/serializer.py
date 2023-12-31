from rest_framework import serializers
from .models import EnrolledCourse
from course.models import Course


class CourseSerializer(serializers.ModelSerializer):
    instructor_first_name = serializers.CharField(source="instructor.user.first_name")
    instructor_last_name = serializers.CharField(source="instructor.user.last_name")

    class Meta:
        model = Course
        fields = "__all__"


class EnrolledCourseSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    completion_percentage = serializers.SerializerMethodField()

    class Meta:
        model = EnrolledCourse
        fields = "__all__"

    def get_completion_percentage(self, enrolled_course):
        return enrolled_course.completion_percentage()
