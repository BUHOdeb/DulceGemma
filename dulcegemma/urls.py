from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

admin.site.site_header = "Dulce’Gemma · Administración"
admin.site.site_title = "Dulce’Gemma"

urlpatterns = [
    path("admin/", admin.site.urls),
    # Fotos subidas desde el admin (suficiente para un sitio pequeño)
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    path("", include("catalogo.urls")),
]
