from django.urls import path

from .models import Poll
from .views import PollView, RegisterVote

urlpatterns = [
    path('', PollView.as_view()),
    path('test', RegisterVote.as_view())
]