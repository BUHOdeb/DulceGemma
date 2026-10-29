from django.db.models import Prefetch
from django.shortcuts import render

from .models import Categoria, Producto


def home(request):
    productos = Producto.objects.filter(activo=True).prefetch_related("precios")
    categorias = Categoria.objects.filter(activo=True).prefetch_related(
        Prefetch("productos", queryset=productos, to_attr="items"))
    return render(request, "catalogo/home.html", {"categorias": [c for c in categorias if c.items]})
