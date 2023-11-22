from rest_framework import serializers
from .models import Course,Module


class CourseSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()
    fromatted_created_at = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = '__all__'

    def get_duration(self,obj):
        return obj.total_duration()

    def get_fromatted_created_at(self, obj):
        return obj.formatted_created_at()    
        


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'


class CourseAndModuleSerializer(serializers.ModelSerializer):
    # modules = ModuleSerializer(many=True, read_only=True)
    formatted_created_at = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = '__all__' 
        depth = 1  

    def get_formatted_created_at(self, obj):
        return obj.formatted_created_at()      



