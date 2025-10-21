import pytest
from rest_framework.test import APIClient

from shop.models import Album, Review


@pytest.fixture(scope='function')
def api_client():
    """Fixture to provide api client
    :return APIClient"""
    yield APIClient()


@pytest.fixture(scope='function')
def authenticated_client(api_client, user):
    """APIClient with authenticated user
    :return APIClient"""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture(scope='function')
def album():
    """Test album"""
    yield Album.objects.create(
        title="Test Album",
        artist_id=1,
        genre="Rock",
        year=2020,
        price=9.99
    )


@pytest.fixture(scope='function')
def review(user, album):
    """Test review."""
    yield Review.objects.create(
        user=user,
        album=album,
        rating=5,
        comment="Excellent!"
    )
