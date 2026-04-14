# core/urls.py
"""URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""
from rest_framework.routers import DefaultRouter

from django.conf import settings
from django.conf.urls.static import static

#from django.contrib import admin
from django.urls import include, path

from core.api.views import UserViewSet
from core.sites import core_admin_site

router = DefaultRouter()
router.register(r"users", UserViewSet)

handler404 = "core.views.custom_404"
handler500 = "core.views.custom_500"

urlpatterns = [
    #path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("accounts/", include("allauth.urls")),
    path("admin/", core_admin_site.urls),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")), # For browsable API login
]

# Debug toolbar (development only)
if settings.DEBUG:  # type: ignore[misc]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # type: ignore[misc]
   # urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]