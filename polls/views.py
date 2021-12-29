from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import generics, serializers
from .serializers import PollSerializer
from .models import Poll

# Create your views here.

class PollView(generics.ListAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer