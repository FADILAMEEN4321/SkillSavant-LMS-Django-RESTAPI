from django.shortcuts import render
from rest_framework import generics
from accounts.models import *
from .serializer import *

# Create your views here.

class AdminInstructorListing(generics.ListCreateAPIView):
    queryset = InstructorProfile.objects.all()
    serializer_class = InstructorSerializer