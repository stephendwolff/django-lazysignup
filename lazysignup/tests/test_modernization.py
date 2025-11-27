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
