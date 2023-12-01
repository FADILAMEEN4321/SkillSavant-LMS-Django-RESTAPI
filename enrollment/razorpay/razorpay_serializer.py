from rest_framework import serializers
from enrollment.models import EnrolledCourse, Payment, Transcation
from course.models import Course, Module


class CreateOrderSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    currency = serializers.CharField()


class EnrolledCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrolledCourse
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class TranscationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcation
        fields = "__all__"
