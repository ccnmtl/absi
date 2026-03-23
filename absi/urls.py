from django.urls import include, path, re_path
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.views.static import serve
from django_cas_ng import views as cas_views
from absi.main import views
from pagetree.generic.views import PageView, EditView, InstructorView

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

    path('stats/', TemplateView.as_view(template_name="stats.html")),
    path('smoketest/', include('smoketest.urls')),
    path('uploads/<str:path>', serve, {'document_root': settings.MEDIA_ROOT}),

    path('transcribe/', views.TranscribeView.as_view(),
         name='transcribe_view'),

    path('api/transcribe/', views.QueueAWSTranscribeJobView.as_view(),
         name='api_transcribe_job_view'),

    path('api/azure_transcribe/', views.AzureTranscribeJobView.as_view(),
         name='api_azure_transcribe_job_view'),

    path('s3sign/', views.SignS3ECSView.as_view()),

    path('sentry-debug/', trigger_error),

    # pagetree
    path('pagetree/', include('pagetree.urls')),
    re_path(
        r'^pages/edit/(?P<path>.*)$',
        EditView.as_view(hierarchy_name='main', hierarchy_base='/pages/'),
        name='edit-page'),
    re_path(
        r'^pages/instructor/(?P<path>.*)$',
        InstructorView.as_view(
            hierarchy_name='main', hierarchy_base='/pages/')),
    re_path(
        r'^pages/(?P<path>.*)$',
        PageView.as_view(
            hierarchy_name='main', hierarchy_base='/pages/')),
]
