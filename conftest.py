import pytest


@pytest.fixture
def lazy_user(db):
    """Create a lazy user for testing."""
    from lazysignup.models import LazyUser
    user, username = LazyUser.objects.create_lazy_user()
    return user


@pytest.fixture
def regular_user(db):
    """Create a regular (non-lazy) user for testing."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    return User.objects.create_user('testuser', 'test@example.com', 'password123')
