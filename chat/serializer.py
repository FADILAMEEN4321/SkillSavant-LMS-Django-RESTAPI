from rest_framework import serializers
from .models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source='sender.first_name')
    user_id = serializers.ReadOnlyField(source='sender.id')
    class Meta:
        model = ChatMessage
        fields = ['message', 'first_name', 'user_id']
