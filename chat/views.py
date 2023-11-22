from rest_framework import generics
from .serializer import ChatMessageSerializer
from accounts.permissions import IsInstructor, IsStudent
from course.models import Course
from .models import ChatMessage



class PreviousChatsListView(generics.ListAPIView):
    permission_classes = [IsStudent | IsInstructor]
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        course = Course.objects.get(id=course_id)
        return ChatMessage.objects.filter(course=course).order_by('timestamp')
    
    

