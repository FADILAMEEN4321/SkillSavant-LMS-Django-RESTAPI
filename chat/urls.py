from django.urls import path
from .views import PreviousChatsListView

urlpatterns = [
    path('previous-chats-listing/<int:course_id>/', PreviousChatsListView.as_view(), name="previous-chats-listing")
]
