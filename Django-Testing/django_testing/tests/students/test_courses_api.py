import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory

@pytest.mark.django_db
def test_create_retrieve(client, course_factory):
    # Arrange
    course = course_factory(_quantity=1)
    # Act
    url = f'/api/v1/courses/{course[0].id}/'
    response = client.get(url)
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == course[0].name


@pytest.mark.django_db
def test_create_list(client, course_factory):
    # Arrange
    course = course_factory(_quantity=5)
    # Act
    url = '/api/v1/courses/'
    response = client.get(url)
    # Assert
    assert response.status_code == 200
    data = response.json()
    for index , item in enumerate(data):
        assert item['name'] == course[index].name

@pytest.mark.django_db
def test_filter_id(client, course_factory):
    # Arrange
    course = course_factory(_quantity=10)
    # Act
    url = '/api/v1/courses/'
    id_course = course[5].id
    response = client.get(url, {'id': id_course})
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == course[5].name


@pytest.mark.django_db
def test_filter_name(client, course_factory):
    # Arrange
    course = course_factory(_quantity=10)
    # Act
    url = '/api/v1/courses/'
    name = course[5].name
    response = client.get(url, {'name': name})
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == name

@pytest.mark.django_db
def test_success_create(client):
    # Arrange
    course = {'name': 'python'}
    # Act
    url = '/api/v1/courses/'
    response = client.post(url, course)
    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == 'python'


@pytest.mark.django_db
def test_success_update(client, course_factory):
    # Arrange
    course = course_factory(_quantity=1)
    new_course = {'name': 'java_script'}
    # Act
    url = f'/api/v1/courses/{course[0].id}/'
    response = client.patch(url, new_course)
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'java_script'

@pytest.mark.django_db
def test_success_delete(client, course_factory):
    # Arrange
    course = course_factory(_quantity=1)
    # Act
    url = f'/api/v1/courses/{course[0].id}/'
    response = client.delete(url)
    # Assert
    assert response.status_code == 204