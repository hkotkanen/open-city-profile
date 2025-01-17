from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from profiles.api import GeoDivisionViewSet, InterestConceptViewSet, ProfileViewSet

router = routers.DefaultRouter()
router.register("profile", ProfileViewSet)
router.register(
    "interest-concept", InterestConceptViewSet, base_name="interest-concept"
)
router.register("geo-division", GeoDivisionViewSet, base_name="geo-division")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("v1/", include(router.urls)),
    path("docs/", include_docs_urls(title="Open City profile")),
    path("accounts/", include("allauth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
