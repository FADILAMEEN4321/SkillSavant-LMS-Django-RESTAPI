from django.urls import path
from .api_razorpay import CreateOrderAPIView

urlpatterns = [
    path('razorpay_order/create/', CreateOrderAPIView.as_view(), name="create-order-api")
]
