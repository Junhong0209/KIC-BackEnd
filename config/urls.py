from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_url_patterns = [
    path("v1/", include("v1.urls"))
]

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="KICSV Web Site API",
        default_version="v1",
        description="KICSV 웹 사이트를 위한 API Docs",
        terms_of_service="https://www.google.com/policies/terms/"
    ),
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_url_patterns
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include("v1.urls")),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view_v1.without_ui(cache_timeout=0), name="schema-json"),
    re_path(r'^swagger/$', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
