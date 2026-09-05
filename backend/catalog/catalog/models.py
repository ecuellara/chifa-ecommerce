import time
from django.utils.text import slugify
from django.db import models
from .utils import resize_and_compress_image

class Product(models.Model):
    # ... campos existentes ...

    def save(self, *args, **kwargs):
        # Verificar si se está subiendo una nueva imagen
        if self.image and self.image.file:
            # Procesar la imagen
            processed_image = resize_and_compress_image(
                self.image.file,
                target_size=(400, 400),
                quality=85,
                format='JPEG'
            )
            # Asignar el contenido procesado al campo image
            # Generar un nombre de archivo único
            ext = 'jpg'
            filename = f"products/{self.slug}_{self.id}_{int(time.time())}.{ext}" if self.id else f"products/{self.slug}_temp.{ext}"
            self.image.save(filename, processed_image, save=False)
        
        super().save(*args, **kwargs)