from rest_framework import serializers
from enrollment.models import EnrolledCourse, Payment, Transcation
from course.models import Course, Module


class CreateOrderSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    currency = serializers.CharField()


class EnrolledCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrolledCourse
        fields = '__all__'

    def create(self, validated_data):
        # Get the enrolled course instance
        enrolled_course = super().create(validated_data)

        # Get all modules related to the enrolled course
        modules = Module.objects.filter(course=enrolled_course.course)

        # Set the completion status of all modules to False
        module_completion_status = {str(module.module_order): False for module in modules}

        # Update the enrolled course instance with module completion status
        enrolled_course.module_completion_status = module_completion_status
        enrolled_course.save()

        return enrolled_course    


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment  
        fields = '__all__'     



class TranscationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcation
        fields = '__all__'