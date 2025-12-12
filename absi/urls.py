from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.views.static import serve
from django_cas_ng import views as cas_views
from absi.main import views

admin.autodiscover()


def trigger_error(request):
    division_by_zero = 1 / 0  # noqa: F841


urlpatterns = [
    path('', views.IndexView.as_view()),
    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),
    path('cas/login', cas_views.LoginView.as_view(),
         name='cas_ng_login'),
    path('cas/logout', cas_views.LogoutView.as_view(),
         name='cas_ng_logout'),

    path('_impersonate/', include('impersonate.urls')),
    path('stats/', TemplateView.as_view(template_name="stats.html")),
    path('smoketest/', include('smoketest.urls')),
    path('uploads/<str:path>', serve, {'document_root': settings.MEDIA_ROOT}),

    path('transcribe/', views.TranscribeView.as_view(),
         name='transcribe_view'),

    path('sentry-debug/', trigger_error),
]
