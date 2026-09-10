import logging
import re
from pathlib import Path
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from .models import Product
from .utils import process_product_image

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Product)
def process_product_image_signal(sender, instance, created, **kwargs):
    # 1. Si no hay imagen, no hay nada que hacer
    if not instance.image:
        return

    # 2. Evitar recursión por si acaso
    if getattr(instance, "_processing_image", False):
        return

    current_name = instance.image.name  # ej: products/prueba.jpg

    # 3. Si ya tiene formato final y ya es 400x400, salir
    if re.match(r"products/producto_.*_\d+\.jpg", current_name):
        try:
            with Image.open(instance.image.path) as im:
                if im.size == (400, 400) and im.format == "JPEG":
                    return
        except FileNotFoundError:
            return

    # 4. Procesar: redimensionar + renombrar + borrar original
    try:
        abs_path = instance.image.path
    except Exception:
        return

    try:
        new_relative = process_product_image(abs_path, instance.slug or "sin-slug")
    except ValidationError as e:
        # Archivo rechazado (no-imagen o >5MB): deja producto sin foto, no tumba el save
        logger.warning('Imagen rechazada en producto %s: %s', instance.pk, e)
        Product.objects.filter(pk=instance.pk).update(image=None)
        return

    # 5. Actualizar solo el campo image SIN disparar de nuevo la señal
    Product.objects.filter(pk=instance.pk).update(image=new_relative)