import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from shop.models import Album, Review, Artist, Label


@pytest.fixture(scope='function')
def api_client():
    """Fixture to provide api client
    :return APIClient"""
    yield APIClient()


@pytest.fixture
def admin_user():
    yield User.objects.create_superuser(
        username='adminuser',
        password='adminpass123',
        email='admin@example.com'
    )


@pytest.fixture(scope='function')
def user():
    yield User.objects.create_user(
        username='testuser1',
        password='password123',
        email='test1@gmail.com',)


@pytest.fixture
def authenticated_admin_client(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture(scope='function')
def authenticated_client(api_client, user):
    """APIClient with authenticated user
    :return APIClient"""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture(scope='function')
def artist():
    yield Artist.objects.create(name="Test Artist")


@pytest.fixture(scope='function')
def label():
    yield Label.objects.create(name="Test Label")


@pytest.fixture(scope='function')
def album(artist, label):
    yield Album.objects.create(
        title="Test Album",
        artist=artist,
        label=label,
        genre="Rock",
        year=2020,
        price=9.99,
        available=True
    )


@pytest.fixture(scope='function')
def review(user, album):
    yield Review.objects.create(
        user=user,
        album=album,
        rating=5,
        comment="Excellent!"
    )
