# Dulce’Gemma – Landing en Django

## Puesta en marcha
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py cargar_catalogo      # categorías, productos, precios y fotos iniciales
python manage.py createsuperuser      # usuario para /admin/
python manage.py runserver
```
- Web: http://127.0.0.1:8000/ — Admin: http://127.0.0.1:8000/admin/
- **Categorías** (Alfajores, Cuchuflis, Tortas…): cada una es una sección con su menú de acceso rápido. Puedes cambiar orden, ocultarlas y ponerles foto de portada.
- **Productos**: cada tarjeta lleva su foto, descripción y precios (se editan en la misma pantalla).
- Teléfono/WhatsApp: `NEGOCIO` en `dulcegemma/settings.py`.
- `cargar_catalogo --reset` restaura precios y fotos originales (pisa tus cambios).
- Si ya tenías la versión anterior: borra `db.sqlite3` y repite los comandos (cambió la estructura de la base de datos).

## Producción
Variables de entorno: `DJANGO_DEBUG=0`, `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS=tudominio.cl`, `DJANGO_CSRF_ORIGINS=https://tudominio.cl`.
Luego `python manage.py collectstatic --noinput` y `gunicorn dulcegemma.wsgi`.
Las fotos subidas desde el admin se guardan en `media/`: usa un disco persistente (en hostings con disco efímero se pierden).
