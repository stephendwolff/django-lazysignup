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

    def test_views_uses_gettext_lazy(self):
        """views.py should use gettext_lazy, not ugettext_lazy."""
        import inspect
        import lazysignup.views as views_module
        source = inspect.getsource(views_module)
        assert 'ugettext_lazy' not in source, "ugettext_lazy is deprecated"

    def test_views_does_not_use_is_ajax(self):
        """views.py should not use request.is_ajax() (removed in Django 4.0)."""
        import inspect
        import lazysignup.views as views_module
        source = inspect.getsource(views_module)
        assert 'is_ajax()' not in source, "is_ajax() was removed in Django 4.0"

    def test_urls_use_path_or_re_path(self):
        """URL configs should use path/re_path, not deprecated url()."""
        import inspect
        import lazysignup.urls as urls_module
        source = inspect.getsource(urls_module)
        assert 'from django.conf.urls import url' not in source
        assert 'from django.urls import' in source

    def test_no_identity_comparison_for_strings(self):
        """Test files should use == for string comparison, not 'is'."""
        from pathlib import Path
        # Check tests/urls.py
        urls_path = Path(__file__).parent / 'urls.py'
        urls_content = urls_path.read_text()
        assert "is 'auth.User'" not in urls_content, "Use == for string comparison, not is"
        assert "is not 'auth.User'" not in urls_content, "Use != for string comparison, not is not"

        # Check tests/tests.py
        tests_path = Path(__file__).parent / 'tests.py'
        tests_content = tests_path.read_text()
        assert "is 'auth.User'" not in tests_content, "Use == for string comparison, not is"
        assert "is not 'auth.User'" not in tests_content, "Use != for string comparison, not is not"

    def test_setup_has_no_six_dependency(self):
        """setup.py should not list six as a dependency."""
        from pathlib import Path
        setup_path = Path(__file__).parent.parent.parent / 'setup.py'
        content = setup_path.read_text()
        assert "'six" not in content.lower(), "six should be removed from dependencies"
