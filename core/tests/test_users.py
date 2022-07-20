import pytest
from model_bakery import baker
from rest_framework import status

from core.models import User


@pytest.fixture
def create_user(api_client):
    def do_create_user(user):
        return api_client.post('/auth/users/', user)
    return do_create_user

@pytest.fixture
def retrieve_user(api_client):
    def do_retrieve_user(id):
        return api_client.get(f'/core/users/{id}/')
    return do_retrieve_user

@pytest.fixture
def update_user(api_client):
    def do_update_user(id, data):
        return api_client.post(f'/core/users/{id}/', data)
    return do_update_user



@pytest.mark.django_db
class TestCreateUser:
    def test_if_valid_data_returns_201(self, create_user):
        user_data = {'username': 'un', 'email': 'abcd@gmail.com', 'first_name': 'A', 'last_name': 'B', 'password': 'Ilovepollish@123'}

        response = create_user(user_data)

        assert response.status_code == status.HTTP_201_CREATED

    
    def test_if_invalid_data_returns_400(self, create_user):
        bad_user_data = {'username': '', 'email': 'abcd@gmail.com', 'first_name': 'A', 'last_name': 'B', 'password': 'Ilovepollish@123'}

        response = create_user(bad_user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['username'] is not None

    
    def test_if_missing_field_returns_400(self, create_user):
        bad_user_data = {'email': 'abcd@gmail.com', 'first_name': 'A', 'last_name': 'B', 'password': 'Ilovepollish@123'}

        response = create_user(bad_user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST



@pytest.mark.django_db
class TestRetrieveUser:
    def test_if_getting_valid_user_returns_200(self, retrieve_user):
        user = baker.make(User)

        response = retrieve_user(user.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == user.id


    def test_if_valid_data_creates_profile(self, retrieve_user):
        user = baker.make(User)

        response = retrieve_user(user.id)

        assert response.data['profile'] is not None

    
    def test_if_unauthorized_access_to_current_user_returns_401(self, retrieve_user):
        pass


@pytest.mark.django_db
class TestUpdateUser:
    def test_if_anonymous_returns_401(self, update_user):
        pass

    
    def test_if_admin_returns_202(self, update_user):
        pass


    def test_if_authenticated_returns_202(self, update_user):
        pass

