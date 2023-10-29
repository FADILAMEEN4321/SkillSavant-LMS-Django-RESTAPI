from rest_framework import serializers
from .models import Course,Module


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'


class CourseAndModuleSerializer(serializers.ModelSerializer):
    # modules = ModuleSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = '__all__' 
        depth = 1     



