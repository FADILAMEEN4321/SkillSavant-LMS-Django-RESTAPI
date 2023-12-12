from rest_framework.views import APIView
from rest_framework import status
from .razorpay_serializer import (
    CreateOrderSerializer,
    TranscationSerializer,
    EnrolledCourseSerializer,
    PaymentSerializer,
)
from rest_framework.response import Response
from .main import RazorpayClient
from course.models import Course, Module
from accounts.models import StudentProfile, InstructorProfile
from enrollment.models import Transcation, Payment, EnrolledCourse, ModuleProgress
from rest_framework.serializers import ValidationError
from decimal import Decimal
from enrollment.tasks import send_enrollment_email


# Object for razorpay client
rz_client = RazorpayClient()


class CreateOrderAPIView(APIView):
    def post(self, request):
        create_order_serializer = CreateOrderSerializer(data=request.data)

        if create_order_serializer.is_valid():
            order_response = rz_client.create_order(
                amount=create_order_serializer.validated_data["amount"],
                currency=create_order_serializer.validated_data["currency"],
            )

            response = {
                "message": "razorpay payment order created",
                "data": order_response,
            }
            return Response(response, status=status.HTTP_201_CREATED)

        else:
            response = {
                "error": create_order_serializer.errors,
                "message": "bad request",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class EnrollmentCompletionAPIView(APIView):
    def post(self, request):
        try:
            # All data required
            course = Course.objects.get(id=request.data["course"])
            student = StudentProfile.objects.get(id=request.data["student"])
            instructor = InstructorProfile.objects.get(id=course.instructor.id)
            razor_pay_payment_id = request.data["payment_id"]
            razor_pay_order_id = request.data["order_id"]
            razor_pay_signature = request.data["signature"]
            total_amount = Decimal(request.data["total_amount"])
            instructor_share = round(total_amount * Decimal("0.70"), 2)
            company_share = round(total_amount * Decimal("0.30"), 2)

            # adding instructor share to wallet
            instructor.wallet = instructor_share
            instructor.save()

            enroll_course_data = {"course": course.id, "student": student.id}

            payment_data = {
                "student": student.id,
                "course": course.id,
                "total_amount": total_amount,
            }

            transcation_data = {
                "course": course.id,
                "student": student.id,
                "instructor": instructor.id,
                "instructor_share": instructor_share,
                "company_share": company_share,
                "total_amount": total_amount,
                "payment_id": razor_pay_payment_id,
                "order_id": razor_pay_order_id,
                "signature": razor_pay_signature,
            }

            enroll_course_serializer = EnrolledCourseSerializer(data=enroll_course_data)
            payment_serializer = PaymentSerializer(data=payment_data)
            transcation_serializer = TranscationSerializer(data=transcation_data)

            if (
                enroll_course_serializer.is_valid()
                and payment_serializer.is_valid()
                and transcation_serializer.is_valid()
            ):
                print(transcation_serializer.validated_data["order_id"])
                print(transcation_serializer.validated_data[
                        "payment_id"
                    ],)
                print(transcation_serializer.validated_data["order_id"])
                test = rz_client.verify_payment(
                    razorpay_order_id=transcation_serializer.validated_data["order_id"],
                    razorpay_payment_id=transcation_serializer.validated_data[
                        "payment_id"
                    ],
                    razorpay_signature=transcation_serializer.validated_data[
                        "signature"
                    ],
                )
                print(test,'----->test')

                enroll_course_serializer.save()
                payment_serializer.save()
                transcation_serializer.save()

                # Creating ModuleProgress records for each module in the course.
                modules = Module.objects.filter(course=course)
                for module in modules:
                    ModuleProgress.objects.create(module=module, student=student)

                # Sending email asynchronously using Celery
                # student_email = student.user.formatted_student_email()
                # send_enrollment_email.delay(
                #     student_email=student_email, course_title=course.title
                # )

                response = {"message": "Course Enrollment Successfull"}

                return Response(response, status=status.HTTP_201_CREATED)

            else:
                errors = {
                    "enroll_course_errors": enroll_course_serializer.errors,
                    "payment_errors": payment_serializer.errors,
                    "transcation_errors": transcation_serializer.errors,
                }

                response = {
                    "message": "Bad request",
                    "errors": errors,
                }

                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            raise ValidationError(
                {"status_code": status.HTTP_400_BAD_REQUEST, "message": e}
            )
