import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.users.models import User  # Используем кастомную модель пользователя
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'agile_app.settings'
django.setup()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs)  # Создание пользователя через create_user для хэширования пароля

    return make_user


@pytest.mark.django_db
def test_get_user_list(api_client, create_user):
    create_user(username="testuser1", password="TestPassword123")
    create_user(username="testuser2", password="TestPassword123")

    url = reverse("user-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 2


@pytest.mark.django_db
def test_register_user(api_client):
    url = reverse("users-register")
    user_data = {
        "username": "newuser",
        "password": "TestPassword123",  # Используем надежный пароль
        "email": "newuser@example.com"
    }

    response = api_client.post(url, data=user_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username="newuser").exists()


@pytest.mark.django_db
def test_register_user_invalid_data(api_client):
    url = reverse("user-register")

    # Попытка регистрации без пароля
    invalid_data = {"username": "newuser"}
    response = api_client.post(url, data=invalid_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Попытка регистрации с коротким паролем
    invalid_data = {"username": "newuser", "password": "123"}
    response = api_client.post(url, data=invalid_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Попытка регистрации с некорректным форматом email
    invalid_data = {"username": "newuser", "password": "TestPassword123", "email": "invalid-email"}
    response = api_client.post(url, data=invalid_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
