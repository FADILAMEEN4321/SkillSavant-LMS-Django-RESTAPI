from django.urls import path
from .api_razorpay import CreateOrderAPIView, EnrollmentCompletionAPIView

urlpatterns = [
    path(
        "razorpay_order/create/", CreateOrderAPIView.as_view(), name="create-order-api"
    ),
    path(
        "enrollment-completion/",
        EnrollmentCompletionAPIView.as_view(),
        name="enrollment-completion",
    ),
]
