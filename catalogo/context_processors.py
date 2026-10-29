from urllib.parse import quote

from django.conf import settings


def negocio(request):
    n = settings.NEGOCIO
    base = f"https://wa.me/{n['whatsapp']}"
    return {
        "negocio": n,
        "wa_pedido": f"{base}?text={quote('Hola Dulce Gemma, quiero hacer un pedido')}",
        "wa_cotizar": f"{base}?text={quote('Hola Dulce Gemma, quiero cotizar un queque o torta')}",
        "wa_base": base,
    }
