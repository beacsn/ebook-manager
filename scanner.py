from pathlib import Path

from models import Libro

from metadata import extraer_metadata_epub


EXTENSIONES = [
    ".epub",
    ".pdf",
    ".mobi"
]


def escanear_biblioteca(root_path):

    libros = []

    root = Path(root_path)

    print("Iniciando escaneo...")

    for letra in root.iterdir():

        if not letra.is_dir():
            continue

        for autor in letra.iterdir():

            if not autor.is_dir():
                continue

            for archivo in autor.iterdir():

                if not archivo.is_file():
                    continue

                if archivo.suffix.lower() not in EXTENSIONES:
                    continue

                titulo = archivo.stem

                autor_nombre = autor.name

                descripcion = ""

                idioma = ""

                isbn = ""


                # ---------------------------------------------------------
                # EPUB METADATA
                # ---------------------------------------------------------

                if archivo.suffix.lower() == ".epub":

                    metadata = extraer_metadata_epub(
                        archivo
                    )

                    titulo = metadata.get(
                        "titulo",
                        titulo
                    )

                    autor_nombre = metadata.get(
                        "autor",
                        autor_nombre
                    )

                    descripcion = metadata.get(
                        "descripcion",
                        ""
                    )

                    idioma = metadata.get(
                        "idioma",
                        ""
                    )


                libro = Libro(
                    titulo=titulo,
                    autor=autor_nombre,
                    ruta=archivo,
                    formato=archivo.suffix.lower(),
                    descripcion=descripcion,
                    idioma=idioma,
                    isbn=isbn
                )

                libros.append(libro)

    return libros