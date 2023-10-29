from rest_framework import serializers
from accounts.models import *
from course.models import *


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorProfile
        fields = '__all__'
        depth = 1  


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
    class Meta:
        model = Course
        fields = '__all__'
        depth = 1

        

