import pytest
from rest_framework import status
from rest_framework.test import APIClient
from apps.users.models import User
from apps.projects.models import Project  # Импортируем модель Project


@pytest.fixture
def create_user():
    # Создаем проект
    project = Project.objects.create(name="Project A")

    # Создаем пользователя с привязкой к проекту
    user = User.objects.create_user(
        username="user1", password="password123", email="user1@example.com",
        first_name="First", last_name="Last", phone="1234567890",
        position="Developer", project=project  # Передаем объект Project
    )
    return user


@pytest.mark.django_db
def test_user_detail_page_is_displayed(create_user):
    client = APIClient()

    # Эндпоинт для получения пользователя по ID (проверьте, что URL правильный)
    response = client.get(f'/users/{create_user.id}/')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['username'] == "user1"
    assert response.data['email'] == "user1@example.com"
    assert response.data['project'] == "Project A"  # Проверка, что проект отображается


@pytest.mark.django_db
def test_user_detail_page_not_found():
    client = APIClient()

    # Эндпоинт для несуществующего пользователя
    response = client.get('/users/999/')  # Запрос на несуществующего пользователя

    assert response.status_code == status.HTTP_404_NOT_FOUND
    # Преобразуем тело ответа в JSON
    response_data = response.json()
    assert response_data.get('detail') == "Not found."
