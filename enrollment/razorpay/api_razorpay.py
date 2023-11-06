from rest_framework.views import APIView
from rest_framework import status
from .razorpay_serializer import CreateOrderSerializer
from rest_framework.response import Response
from .main import RazorpayClient

#object for razorpay client
rz_client = RazorpayClient()


class CreateOrderAPIView(APIView):
    def post(self, request):
        create_order_serializer = CreateOrderSerializer(data = request.data)

        if create_order_serializer.is_valid():
            order_response = rz_client.create_order(
                amount=create_order_serializer.validated_data['amount'],
                currency=create_order_serializer.validated_data['currency']
            )

            response = {
                "message":"razorpay payment order created",
                "data":order_response,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        
        else:
            response = {
                "error":create_order_serializer.errors,
                "message":"bad request",
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        

class TransactionAPIView(APIView):
    def post(self, request):
        

