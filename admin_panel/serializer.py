from rest_framework import serializers
from accounts.models import *
from course.models import *
from enrollment.models import Transcation


class InstructorSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    class Meta:
        model = InstructorProfile
        fields = '__all__'
        depth = 1  

    def get_email(self, obj,):
        email = obj.user.email
        if email.startswith("instructor-"):
            return email[len("instructor-"):]
        return email





class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'


class CourseSerializerAdmin(serializers.ModelSerializer):
    instructor_first_name = serializers.CharField(source='instructor.user.first_name',read_only=True)
    instructor_last_name = serializers.CharField(source='instructor.user.last_name',read_only=True)
    class Meta:
        model = Course
        fields = '__all__'
        depth = 1



class TransactionSerializer(serializers.ModelSerializer):
    student_first_name = serializers.CharField(source="student.user.first_name")
    student_last_name = serializers.CharField(source="student.user.last_name")
    instructor_first_name = serializers.CharField(source="instructor.user.first_name")
    instructor_last_name = serializers.CharField(source="instructor.user.last_name")
    course_title = serializers.CharField(source="course.title")

    class Meta:
        model = Transcation
        fields = '__all__'
        

