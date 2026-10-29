from django.contrib import admin

from .models import Categoria, Precio, Producto


class PrecioInline(admin.TabularInline):
    model = Precio
    extra = 1


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "orden", "activo")
    list_editable = ("orden", "activo")
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "orden", "activo")
    list_editable = ("orden", "activo")
    list_filter = ("categoria", "activo")
    inlines = [PrecioInline]
