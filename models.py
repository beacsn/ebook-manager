from dataclasses import dataclass

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