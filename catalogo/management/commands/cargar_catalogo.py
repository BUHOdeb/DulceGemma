from django.core.management.base import BaseCommand

from catalogo.models import Categoria, Precio, Producto

MAYOR = "Por mayor, 20+ de cada sabor"
# (categoría, descripción, foto de portada, [(producto, descripción, foto, [(grupo, etiqueta, valor)])])
CATALOGO = [
    ("Alfajores", "Artesanales y caseros, bañados en chocolate.", "categorias/alfajores-detalle.jpg", [
        ("Alfajores clásicos", "Oreo · Super 8 · Orly trufa · Orly frutilla · Clásico 2 pisos", "alfajores-clasicos",
         [("", "Unidad", "$800"), ("", "2 unidades", "$1.500"), ("", MAYOR, "$700 c/u")]),
        ("Alfajores especiales", "Bon o Bon · Manjar nuez · M&M · Pie de limón", "alfajores-especiales",
         [("", "Unidad", "$1.000"), ("", MAYOR, "$900 c/u")]),
    ]),
    ("Barquillos rellenos", "Crujientes, rellenos y con base de chocolate.", "", [
        ("Barquillos rellenos", "Para regalar o compartir.", "barquillos-rellenos",
         [("", "2 unidades", "$1.000"), ("", "11 unidades", "$5.000"), ("", "22 unidades", "$10.000")]),
        ("Barquillos por mayor", "Presentación empaquetada, ideal para eventos.", "barquillos-presentacion",
         [("", "Desde 60 unidades", "$450 c/u"), ("", "Desde 100 unidades", "$400 c/u")]),
    ]),
    ("Cuchuflis", "Delicados y crujientes, para compartir.", "", [
        ("Cuchuflis bañados", "Cubiertos de chocolate.", "cuchuflis-banados",
         [("", "4 unidades", "$1.000"), ("", "25 unidades", "$6.500"), ("", "50 unidades", "$12.500")]),
        ("Cuchuflis sin bañar", "Crujientes y simples.", "cuchuflis-sin-banar",
         [("", "5 unidades", "$1.000"), ("", "25 unidades", "$4.500"), ("", "50 unidades", "$8.000")]),
        ("Cuchuflis mixtos", "Mezcla de bañados y sin bañar.", "cuchuflis-mixtos",
         [("", "5 unidades (3 sin baño, 2 con baño)", "$1.000"), ("", "25 unidades", "$5.500"),
          ("", "50 unidades", "$10.000"), ("", "100 unidades", "$20.000")]),
    ]),
    ("Tortas de cuchuflis", "El centro de tu mesa dulce.", "", [
        ("Torta de cuchuflis básica", "Lista para regalar o compartir.", "torta-basica",
         [("", "30/35 unidades", "$15.000"), ("", "50 unidades", "$20.000")]),
        ("Torta con toppers personalizada", "Con toppers del tema de tu fiesta.", "torta-toppers",
         [("", "30/35 unidades", "$18.500"), ("", "50 unidades", "$25.000")]),
    ]),
    ("Mini donas", "Bañadas en chocolate o personalizadas.", "", [
        ("Mini donas bañadas", "Individuales, listas para regalar.", "donas-banadas",
         [("", "3 unidades", "$1.000"), ("", "25 unidades", "$8.000"), ("", "50 unidades", "$15.000"),
          ("", "100 unidades", "$30.000")]),
        ("Mini donas personalizadas", "Diseño simple a tu gusto.", "donas-personalizadas",
         [("", "25 unidades", "$9.500"), ("", "50 unidades", "$18.000"), ("", "100 unidades", "$35.000")]),
    ]),
    ("Mini donas rellenas", "Todas incluyen frutilla picada.", "", [
        ("Rellenas de crema pastelera", "", "donas-crema-pastelera",
         [("", "25 unidades", "$10.500"), ("", "50 unidades", "$20.000")]),
        ("Rellenas de manjar", "", "donas-manjar",
         [("", "25 unidades", "$12.000"), ("", "50 unidades", "$22.500")]),
        ("Rellenas de Nutella", "", "",
         [("", "25 unidades", "$15.000"), ("", "50 unidades", "$29.000")]),
    ]),
    ("Cupcakes y galletas", "Para cumpleaños, regalos y eventos.", "", [
        ("Mini cupcakes", "Ideales para cumpleaños y eventos.", "cupcakes",
         [("", "25 unidades", "$12.500"), ("", "50 unidades", "$25.000"), ("", "100 unidades", "$45.000")]),
        ("Galletas tipo kuky", "Empaquetadas, listas para regalar.", "galletas",
         [("", "3 unidades", "$1.200"), ("", "5 unidades", "$2.000")]),
    ]),
]


class Command(BaseCommand):
    help = "Carga el catálogo inicial. Sin --reset no toca lo que ya existe."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Restaura precios y fotos originales.")

    def handle(self, *args, **opts):
        reset = opts["reset"]
        for i, (cat_nombre, cat_desc, cat_img, productos) in enumerate(CATALOGO):
            cat, _ = Categoria.objects.get_or_create(
                nombre=cat_nombre, defaults={"descripcion": cat_desc, "imagen": cat_img, "orden": i * 10})
            for j, (nombre, sub, img, filas) in enumerate(productos):
                prod, creado = Producto.objects.get_or_create(
                    categoria=cat, nombre=nombre,
                    defaults={"subtitulo": sub, "imagen": f"productos/{img}.jpg" if img else "", "orden": j * 10})
                if not creado and not reset:
                    continue
                prod.precios.all().delete()
                Precio.objects.bulk_create(
                    Precio(producto=prod, grupo=g, etiqueta=e, valor=v, orden=k) for k, (g, e, v) in enumerate(filas))
        self.stdout.write(self.style.SUCCESS(
            f"Catálogo listo: {Categoria.objects.count()} categorías, {Producto.objects.count()} productos."))
