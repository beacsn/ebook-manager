from dataclasses import dataclass
from dataclasses import field

from pathlib import Path


@dataclass
class Libro:

    titulo: str

    autor: str

    ruta: Path

    formato: str

    descripcion: str = ""

    idioma: str = ""

    isbn: str = ""

    # =====================================================
    # GOOGLE BOOKS
    # =====================================================

    generos: list[str] = field(
        default_factory=list
    )

    thumbnail: str = ""

    descripcion_google: str = ""

    enriquecido: bool = False