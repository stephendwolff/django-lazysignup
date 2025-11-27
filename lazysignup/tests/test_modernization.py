import pytest
from lazysignup.models import LazyUser


class TestLazyUserModernization:
    """Tests verifying Python 3 modernization."""

    def test_no_default_app_config(self):
        """__init__.py should not use deprecated default_app_config (Django 3.2+)."""
        from pathlib import Path
        init_path = Path(__file__).parent.parent / '__init__.py'
        content = init_path.read_text()
        assert 'default_app_config' not in content, "default_app_config is deprecated since Django 3.2"

    def test_lazy_user_str_returns_string(self, lazy_user):
        """LazyUser.__str__ should return a string without six decorator."""
        lazy_user_obj = LazyUser.objects.get(user=lazy_user)
        result = str(lazy_user_obj)
        assert isinstance(result, str)
        assert lazy_user.username in result

    def test_lazy_user_has_no_six_dependency(self):
        """Verify six is not imported in models module."""
        import lazysignup.models as models_module
        import sys
        # After modernization, six should not be in the module's imports
        assert 'six' not in dir(models_module), "six should be removed from models.py"

    def test_get_user_class_uses_remote_field(self):
        """get_user_class should use only remote_field.model (not rel.to)."""
        import inspect
        source = inspect.getsource(LazyUser.get_user_class)
        assert 'rel.to' not in source, "rel.to is deprecated, use remote_field.model"
        assert 'remote_field' in source

    def test_get_user_class_returns_user_model(self, db):
        """get_user_class should return the configured user model."""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        assert LazyUser.get_user_class() == User
