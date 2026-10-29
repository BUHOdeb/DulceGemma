from django.db import models
from django.utils.text import slugify


class Categoria(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True, blank=True, help_text="Se genera solo desde el nombre.")
    descripcion = models.CharField("Descripción corta", max_length=200, blank=True)
    imagen = models.ImageField("Foto de portada (opcional)", upload_to="categorias/", blank=True)
    orden = models.PositiveSmallIntegerField(default=0, help_text="Menor número aparece primero.")
    activo = models.BooleanField(default=True, help_text="Desmarca para ocultar toda la categoría.")

    class Meta:
        ordering = ["orden", "nombre"]
        verbose_name = "categoría"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, related_name="productos", on_delete=models.PROTECT)
    nombre = models.CharField(max_length=120)
    subtitulo = models.CharField("Descripción corta", max_length=200, blank=True)
    imagen = models.ImageField(upload_to="productos/", blank=True)
    orden = models.PositiveSmallIntegerField(default=0, help_text="Menor número aparece primero.")
    activo = models.BooleanField(default=True, help_text="Desmarca para ocultarlo de la web.")

    class Meta:
        ordering = ["categoria__orden", "orden", "nombre"]

    def __str__(self):
        return self.nombre


class Precio(models.Model):
    producto = models.ForeignKey(Producto, related_name="precios", on_delete=models.CASCADE)
    grupo = models.CharField(
        max_length=80, blank=True,
        help_text="Subtítulo opcional (Bañados, Por mayor…). Los precios del mismo grupo deben ir seguidos.",
    )
    etiqueta = models.CharField(max_length=120, help_text="Ej: 25 unidades")
    valor = models.CharField(max_length=40, help_text="Ej: $12.500 o $700 c/u")
    orden = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["orden", "id"]

    def __str__(self):
        return f"{self.etiqueta}: {self.valor}"
