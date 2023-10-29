from rest_framework import serializers
from course.models import Course


class CourseSerializerHome(serializers.ModelSerializer):
    instructor_first_name = serializers.CharField(source='instructor.user.first_name', read_only=True)
    instructor_last_name = serializers.CharField(source='instructor.user.last_name', read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        depth = 1
