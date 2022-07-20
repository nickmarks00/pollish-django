from django.core.mail import BadHeaderError
from templated_mail.mail import BaseEmailMessage
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .models import User

@api_view(['POST'])
def send_email(request):

    email = request.data.get('email', None)

    if email is None:
        return Response('Email missing from request body', status=status.HTTP_400_BAD_REQUEST)


    queryset = User.objects.filter(email=email)
    if queryset.exists():
        user = queryset[0]

        try:
            message = BaseEmailMessage(
                template_name = 'emails/forgotten_password.html',
                context = {
                    'username': user.username,
                    'recovery_key': '1234'
                }
            )
            message.send([email])
        except BadHeaderError:
            return Response('Error sending message', status=status.HTTP_400_BAD_REQUEST)

    return Response('Sent recovery email successfully...', status=status.HTTP_200_OK)