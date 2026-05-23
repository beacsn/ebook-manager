import json

from pathlib import Path

from models import Libro


CACHE_DIR = Path("cache")

CACHE_PATH = CACHE_DIR / "libros.json"


# =========================================================
# GUARDAR CACHE
# =========================================================

def guardar_cache(libros):

    print("Entrando en guardar_cache")

    CACHE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    datos = []

    contador = 0

    for libro in libros:

        contador += 1

        if contador % 100 == 0:

            print(f"{contador} libros...")

        datos.append({

            "titulo": libro.titulo,

            "autor": libro.autor,

            "ruta": str(libro.ruta),

            "formato": libro.formato,

            "descripcion": libro.descripcion,

            "idioma": libro.idioma
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


# =========================================================
# CARGAR CACHE
# =========================================================

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

        return None

    libros = []

    for item in datos:

        libro = Libro(

            titulo=item.get(
                "titulo",
                ""
            ),

            autor=item.get(
                "autor",
                ""
            ),

            ruta=Path(
                item.get(
                    "ruta",
                    ""
                )
            ),

            formato=item.get(
                "formato",
                ""
            ),

            descripcion=item.get(
                "descripcion",
                ""
            ),

            idioma=item.get(
                "idioma",
                ""
            )
        )

        libros.append(libro)

    return libros