import os
import time
from pathlib import Path
from PIL import Image, ImageOps


def process_product_image(abs_image_path: str, slug: str) -> str:
    """
    Convierte imagen a JPG 400x400 cover y la renombra.
    Retorna la ruta RELATIVA para guardar en ImageField.
    Ej: "products/producto_arroz-chaufa_1725456789.jpg"
    """
    # 1. Abrir imagen original desde disco
    img = Image.open(abs_image_path)

    # 2. Quitar transparencia: pegar sobre fondo blanco y pasar a RGB
    if img.mode in ("RGBA", "LA", "P"):
        fondo = Image.new("RGB", img.size, (255, 255, 255))
        # Si tiene canal alfa, úsalo como máscara, si no, pega directo
        try:
            fondo.paste(img, mask=img.split()[-1])
        except Exception:
            fondo.paste(img)
        img = fondo
    elif img.mode != "RGB":
        img = img.convert("RGB")

    # 3. Resize + recorte centrado a 400x400
    img = ImageOps.fit(img, (400, 400), Image.LANCZOS, centering=(0.5, 0.5))

    # 4. Construir nuevo nombre
    safe_slug = slug or "sin-slug"
    timestamp = int(time.time())
    relative_path = f"products/producto_{safe_slug}_{timestamp}.jpg"

    # 5. Resolver ruta absoluta: MEDIA_ROOT/products/...
    # abs_image_path = .../media/products/DSC001.png
    # media_root = .../media
    media_root = Path(abs_image_path).parent.parent
    new_abs_path = media_root / relative_path
    new_abs_path.parent.mkdir(parents=True, exist_ok=True)

    # 6. Guardar comprimida
    img.save(new_abs_path, format="JPEG", quality=85, optimize=True)

    # 7. Borrar original si cambió el nombre
    if Path(abs_image_path).resolve() != new_abs_path.resolve():
        try:
            os.remove(abs_image_path)
        except FileNotFoundError:
            pass

    return relative_path