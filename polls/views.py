from django.shortcuts import render
from rest_framework import generics, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ChoiceSerializer, PollSerializer
from .models import Poll, Choice

# Create your views here.

class PollView(generics.ListAPIView):
    queryset = Poll.objects.select_related('profile').all()[:10]
    serializer_class = PollSerializer


class RegisterVote(APIView):

    serializer_class = ChoiceSerializer

    def patch(self, request, format=None):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            choice_id = serializer.data.get('id')

            queryset = Choice.objects.filter(id=choice_id)
            if not queryset.exists():
                return Response({'msg': 'choice not found'}, status.HTTP_404_NOT_FOUND)
            
            choice = queryset[0]

            # check here that the session_key on the post creation != session_key on vote register i.e. the user can't vote on their own post

            choice.votes += 1
            choice.save(update_fields=['votes'])

            return Response(ChoiceSerializer(choice).data, status=status.HTTP_202_ACCEPTED)
        

        return Response({'msg': 'bad serializer'}, status.HTTP_400_BAD_REQUEST)
            

