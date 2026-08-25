from django.urls import include, path, re_path
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.views.static import serve
from django_cas_ng import views as cas_views
from absi.main import views, apiviews
from pagetree.generic.views import EditView, InstructorView

admin.autodiscover()


def trigger_error(request):
    division_by_zero = 1 / 0  # noqa: F841


urlpatterns = [
    path('', views.IndexView.as_view(), name='index_view'),

    path('progress/', views.ProgressView.as_view()),

    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),

    path('login/', views.LoginSplashView.as_view(),
         name='login_splash'),

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

    path('api/azure_assess/', views.AzureAssessJobView.as_view(),
         name='api_azure_assess_job_view'),

    path('api/userprofile/update/',
         apiviews.UpdateUserProfileView.as_view(),
         name='api_update_userprofile'),

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
        views.AuthedPageView.as_view(
            hierarchy_name='main', hierarchy_base='/pages/')),

    path('audio/<int:pk>', views.AudioDispatchView.as_view(),
         name='audio-view'),
    path('polly-audio/<int:pk>', views.PollyAudioView.as_view(),
         name='polly-audio'),
    path('azure-audio/<int:pk>', views.AzureAudioView.as_view(),
         name='azure-audio'),

    path('', include('django.contrib.flatpages.urls')),
]
