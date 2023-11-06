import razorpay
from django.conf import settings
client = razorpay.Client(auth=(
    settings.RAZOR_PAY_KEY_ID, 
    settings.RAZOR_PAY_KEY_SECRET
    ))