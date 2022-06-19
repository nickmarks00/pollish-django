import pytest
from model_bakery import baker
from rest_framework import status

from pollish.models import Poll


@pytest.fixture
def create_poll(api_client):
	def do_create_poll(poll):
		print(poll)
		return api_client.post('/pollish/polls/me/', poll)
	return do_create_poll

@pytest.mark.django_db
class TestCreatePoll:
	def test_if_user_anonymous_returns_401(self, create_poll):

		response = create_poll({})

		assert response.status_code == status.HTTP_401_UNAUTHORIZED

	@pytest.mark.skip
	def test_if_invalid_data_returns_400(self, authenticate, create_poll):
		
		authenticate()

		response = create_poll({'question_text': ''})

		print(response.data.__dict__)

		assert response.status_code == status.HTTP_400_BAD_REQUEST
		# check for error message on return body
		assert response.data['question_text'] is not None

	@pytest.mark.skip
	def test_if_valid_data_returns_201(self, authenticate, create_poll):

		authenticate()

		response = create_poll({'question_text': 'A'})

		assert response.status_code == status.HTTP_201_CREATED


