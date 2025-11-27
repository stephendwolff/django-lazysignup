from django.urls import path, include, re_path
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings

if settings.AUTH_USER_MODEL == 'auth.User':
    from lazysignup.tests.forms import GoodUserCreationForm
else:
    from custom_user_tests.forms import GoodUserCreationForm

from django.contrib import admin

from lazysignup import views
from lazysignup.tests import views as test_views

admin.autodiscover()

urlpatterns = [
    re_path(r'^admin/?', admin.site.urls),
    path('convert/', include('lazysignup.urls')),
    path('custom_convert/', views.convert, {'template_name': 'lazysignup/done.html'}),
    path('custom_convert_ajax/', views.convert, {'ajax_template_name': 'lazysignup/done.html'}),
    path('nolazy/', test_views.view, name='test_view'),
    path('lazy/', test_views.lazy_view, name='test_lazy_view'),
    path('bad-custom-convert/', views.convert, {'form_class': UserCreationForm}, name='test_bad_convert'),
    path('good-custom-convert/', views.convert, {'form_class': GoodUserCreationForm}, name='test_good_convert'),
]
