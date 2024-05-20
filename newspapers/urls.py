from django.urls import path, include

from .views import (
    NewspaperListView,
    NewspaperDetailView,
    NewspaperCreateView,
    NewspaperUpdateView,
    NewspaperDeleteView,
    RedactorListView,
    RedactorDetailView,
    RedactorCreateView,
    RedactorLicenseUpdateView,
    RedactorDeleteView,
    TopicListView,
    TopicCreateView,
    TopicUpdateView,
    TopicDeleteView, RegisterView, CreateProfileView, ActivateAccountView, toggle_theme,
    toggle_assign_to_newspaper,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", NewspaperListView.as_view(), name="newspapers-list"),
    path(
        "topics/",
        TopicListView.as_view(),
        name="topic-list",
    ),
    path(
        "topics/create/",
        TopicCreateView.as_view(),
        name="topic-create",
    ),
    path(
        "topics/<int:pk>/update/",
        TopicUpdateView.as_view(),
        name="topic-update",
    ),
    path(
        "topics/<int:pk>/delete/",
        TopicDeleteView.as_view(),
        name="topic-delete",
    ),
    path("newspapers/", NewspaperListView.as_view(), name="newspapers-list"),
    path("newspapers/<int:pk>/", NewspaperDetailView.as_view(), name="newspaper-detail"),
    path("newspapers/create/", NewspaperCreateView.as_view(), name="newspapers-create"),
    path("newspapers/<int:pk>/update/", NewspaperUpdateView.as_view(), name="newspapers-update"),
    path("newspapers/<int:pk>/delete/", NewspaperDeleteView.as_view(), name="newspapers-delete"),
    path(
        "newspapers/<int:pk>/toggle-assign/",
        toggle_assign_to_newspaper,
        name="toggle-newspaper-assign",
    ),
    path("redactors/", RedactorListView.as_view(), name="redactor-list"),
    path(
        "redactors/<int:pk>/", RedactorDetailView.as_view(), name="redactor-detail"
    ),
    path("redactors/", RedactorListView.as_view(), name="redactor-list"),
    path(
        "redactors/<int:pk>/", RedactorDetailView.as_view(), name="redactor-detail"
    ),
    path("redactors/create/", RedactorCreateView.as_view(), name="redactor-create"),
    path(
        "redactors/<int:pk>/update/",
        RedactorLicenseUpdateView.as_view(),
        name="redactor-update",
    ),
    path(
        "redactors/<int:pk>/delete/",
        RedactorDeleteView.as_view(),
        name="redactor-delete",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register/", RegisterView.as_view(), name="register"),
    path("accounts/create-profile/", CreateProfileView.as_view(), name="profile_create"),
    path("activate/<str:username>/<str:token>/", ActivateAccountView.as_view(), name="activate"),
    path('toggle_theme/', toggle_theme, name='toggle_theme'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
app_name = "newspapers"
