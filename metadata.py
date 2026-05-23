from ebooklib import epub

from PIL import Image

from io import BytesIO

from pathlib import Path
import hashlib
import re

COVERS_DIR = Path("cache/covers")

COVERS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# =========================================================
# VALIDAR IMAGEN
# =========================================================

def imagen_valida(contenido):

    try:

        imagen = Image.open(
            BytesIO(contenido)
        )

        imagen.verify()

        return True

    except Exception:

        return False


# =========================================================
# EXTRAER PORTADA
# =========================================================

def extraer_portada_epub(ruta_epub):

    ruta_cache = generar_nombre_cache(
        ruta_epub
    )

    if ruta_cache.exists():

        return str(ruta_cache)

    try:

        book = epub.read_epub(
            str(ruta_epub)
        )

        # =================================================
        # 1. BUSCAR COVER REAL
        # =================================================

        for item in book.get_items():

            nombre = item.get_name().lower()

            if (
                "cover" in nombre
                or "portada" in nombre
            ):

                contenido = item.get_content()

                if imagen_valida(contenido):

                    with open(ruta_cache, "wb") as f:

                        f.write(contenido)

                    return str(ruta_cache)

        # =================================================
        # 2. FALLBACK
        # =================================================

        for item in book.get_items():

            if item.media_type.startswith(
                "image"
            ):

                contenido = item.get_content()

                if imagen_valida(contenido):

                    # return contenido
                    with open(ruta_cache, "wb") as f:

                        f.write(contenido)

                    return str(ruta_cache)

    except Exception:

        return None

    return None


# =========================================================
# EXTRAER METADATA
# =========================================================

def extraer_metadata_epub(ruta_epub):

    try:

        book = epub.read_epub(
            str(ruta_epub)
        )

        metadata = {}

        # -------------------------------------------------
        # TITULO
        # -------------------------------------------------

        titulo = book.get_metadata(
            "DC",
            "title"
        )

        if titulo:

            metadata["titulo"] = titulo[0][0]

        # -------------------------------------------------
        # AUTOR
        # -------------------------------------------------

        autor = book.get_metadata(
            "DC",
            "creator"
        )

        if autor:

            metadata["autor"] = autor[0][0]

        # -------------------------------------------------
        # IDIOMA
        # -------------------------------------------------

        idioma = book.get_metadata(
            "DC",
            "language"
        )

        if idioma:

            metadata["idioma"] = idioma[0][0]

        # -------------------------------------------------
        # DESCRIPCION
        # -------------------------------------------------

        descripcion = book.get_metadata(
            "DC",
            "description"
        )

        if descripcion:

            metadata["descripcion"] = limpiar_html(
                descripcion[0][0]
            )

        return metadata

    except Exception:

        return {}
    



def generar_nombre_cache(ruta_epub):

    hash_nombre = hashlib.md5(
        str(ruta_epub).encode()
    ).hexdigest()

    return COVERS_DIR / f"{hash_nombre}.jpg"


def limpiar_html(texto):

    if not texto:

        return ""

    texto = re.sub(
        r"<.*?>",
        "",
        texto
    )

    texto = texto.replace(
        "\n",
        " "
    )

    return texto.strip()