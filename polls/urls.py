from django.urls import path

from .models import Poll
from .views import PollView

urlpatterns = [
    path('', PollView.as_view())
]