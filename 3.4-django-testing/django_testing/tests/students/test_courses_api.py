from model_bakery import baker
import pytest
from rest_framework.test import APIClient

from students.models import Course, Student


@pytest.fixture()
def client():
    return APIClient()

@pytest.fixture
def courses_factory():
    def course(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return course


@pytest.fixture
def students_factory():
    def student(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return student

@pytest.mark.django_db
def test_retrieve_course(client, courses_factory):
    course = courses_factory(name='Python')  # Создаем экземпляр курса с помощью фабрики

    response = client.get(f"/api/v1/courses/{course.id}/")

    assert response.status_code == 200
    data = response.json()
    assert data['id'] == course.id


@pytest.mark.django_db
def test_list_courses(client, courses_factory):
    courses_factory(_quantity= 10)
    response = client.get("/api/v1/courses/")

    assert response.status_code == 200
    courses_ex = Course.objects.all()
    assert len(response.data) == len(courses_ex)

@pytest.mark.django_db
def test_filter_id(client, courses_factory):
    course = courses_factory(id=3)

    response = client.get(f"/api/v1/courses/?id={course.id}")

    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == course.id




@pytest.mark.django_db
def test_filter_name(client, courses_factory):
    course = courses_factory(name= 'Python')


    response = client.get(f"/api/v1/courses/?name={course.name}")

    assert response.status_code == 200
    data = response.json()

    assert data[0]['name'] == course.name


@pytest.mark.django_db
def test_create_course(client):
    Course.objects.create(name='Python')
    response = client.post('/api/v1/courses/', data={'id': 1, 'name': 'Python'}, format= 'json')

    assert response.status_code == 201


@pytest.mark.django_db
def test_update_course(client, courses_factory):
    course = courses_factory(name='Python')
    url = f'/api/v1/courses/{course.id}/'
    response = client.patch(url, data={'id': course.id, 'name': 'java'})

    assert response.status_code == 200
    data = response.json()



@pytest.mark.django_db
def test_delete_course(client, courses_factory):
    course = courses_factory(name='Python')
    url = f'/api/v1/courses/{course.id}/'
    response = client.delete(url)

    assert response.status_code == 204







