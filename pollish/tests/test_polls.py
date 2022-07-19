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
	def test_if_user_anonymous_returns_403(self, create_poll):

		response = create_poll({})

		assert response.status_code == status.HTTP_403_FORBIDDEN

	def test_if_invalid_data_returns_400(self, authenticate, create_poll):
		
		authenticate()

		response = create_poll({'question_text': ''})

		assert response.status_code == status.HTTP_400_BAD_REQUEST
		# check for error message on return body
		assert response.data['choices'] is not None


	@pytest.mark.skip
	def test_if_valid_poll_data_returns_201(self, api_client, create_poll):

		username = "user1"
		password = "bar"
		user = django_user_model.objects.create_user(username=username, password=password)
		# Use this:
		api_client.force_login(user)
		# Or this:
		api_client.login(username=username, password=password)

		response = create_poll({'question_text': 'A', 'choices': [{
			'choice_text': 'Option 1'
		}, {
			'choice_text': 'Option 2'
		}]})

		assert response.status_code == status.HTTP_201_CREATED


