from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet


from .models import Poll, Choice, Comment, Profile
from .serializers import ChoiceSerializer, CommentSerializer, PollSerializer, SimplePollSerializer, ProfileSerializer


class SimplePollViewSet(ModelViewSet):
    serializer_class = SimplePollSerializer

    def get_queryset(self):
        return Poll.objects.prefetch_related('choices').all()

class DetailedPollViewSet(ModelViewSet):

    serializer_class = PollSerializer

    def get_queryset(self):
        return Poll.objects.select_related('user').prefetch_related('choices__users', 'comments').filter(user_id=self.kwargs['user_pk'])
    
    def get_serializer_context(self):
        return {'user_id': self.kwargs['user_pk']}


class CommentViewSet(ModelViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.select_related('user').filter(poll_id=self.kwargs['poll_pk'])
    
    def get_serializer_context(self):
        return {'poll_id': self.kwargs['poll_pk']}
    

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
            

class ProfileViewSet(ModelViewSet):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.select_related('user').all()