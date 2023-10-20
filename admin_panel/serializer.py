from rest_framework import serializers
from accounts.models import *


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorProfile
        fields = '__all__'
        depth = 1  