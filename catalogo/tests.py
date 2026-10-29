from django.core.management import call_command
from django.test import TestCase

from .models import Categoria, Producto


class HomeTests(TestCase):
    def setUp(self):
        call_command("cargar_catalogo", verbosity=0)

    def test_home_segmenta_por_categorias(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        for texto in ("Alfajores clásicos", "$800", "$400 c/u", "Mini donas rellenas", "Rellenas de Nutella",
                      'id="tortas-de-cuchuflis"', 'href="#cuchuflis"', "wa.me/56937033038"):
            self.assertContains(r, texto)

    def test_carga_es_idempotente(self):
        call_command("cargar_catalogo", verbosity=0)
        self.assertEqual(Categoria.objects.count(), 7)
        self.assertEqual(Producto.objects.count(), 16)

    def test_categoria_oculta_no_aparece(self):
        Categoria.objects.filter(nombre="Cuchuflis").update(activo=False)
        self.assertNotContains(self.client.get("/"), 'id="cuchuflis"')
