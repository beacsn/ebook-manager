import json

from pathlib import Path

from models import Libro


CACHE_DIR = Path("cache")

CACHE_PATH = CACHE_DIR / "libros.json"


def guardar_cache(libros):
    print("Entrando en guardar_cache")
    # -----------------------------------------------------
    # Crear carpeta cache si no existe
    # -----------------------------------------------------

    CACHE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    datos = []

    for libro in libros:
        contador += 1

        if contador % 100 == 0:
            print(f"{contador} libros...")
        datos.append({
            "titulo": libro.titulo,
            "autor": libro.autor,
            "ruta": str(libro.ruta),
            "formato": libro.formato
        })
    print(CACHE_PATH)
    with open(
        CACHE_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            datos,
            f,
            ensure_ascii=False,
            indent=4
        )
        print("Cache guardada correctamente")


def cargar_cache():

    if not CACHE_PATH.exists():
        return None

    try:

        with open(
            CACHE_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            datos = json.load(f)

    except Exception:

        # ---------------------------------------------
        # Cache corrupta
        # ---------------------------------------------

        return None

    libros = []

    for item in datos:

        libro = Libro(
            titulo=item["titulo"],
            autor=item["autor"],
            ruta=Path(item["ruta"]),
            formato=item["formato"]
        )

        libros.append(libro)

    return libros