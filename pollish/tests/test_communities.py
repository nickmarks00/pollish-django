import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker
from rest_framework import status

from pollish.models import Community


@pytest.fixture
def create_community(api_client):
    def do_create_community(community):
        return api_client.post('/pollish/communities/', community)
    return do_create_community


@pytest.mark.django_db
class TestCreateCommunity:

    def test_if_anonymous_returns_401(self, create_community):
        img = ('media/communities/community_Animals/gary-bendig-6GMq7AGxNbE-unsplash.jpg')

        with open(img, 'rb') as in_image:
            community = {
                'image': SimpleUploadedFile('community.jpg', in_image.read()),
                'name': 'Community',
            }

            response = create_community(community)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
