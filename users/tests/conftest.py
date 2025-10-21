import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture(scope='function')
def user():
    yield User.objects.create_user(
        username='testuser1',
        password='password123',
        email='test1@gmail.com',)
