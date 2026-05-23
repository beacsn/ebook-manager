from ebooklib import epub

from PIL import Image

from io import BytesIO


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

                    return contenido

        # =================================================
        # 2. FALLBACK
        # =================================================

        for item in book.get_items():

            if item.media_type.startswith(
                "image"
            ):

                contenido = item.get_content()

                if imagen_valida(contenido):

                    return contenido

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

            metadata["descripcion"] = descripcion[0][0]

        return metadata

    except Exception:

        return {}