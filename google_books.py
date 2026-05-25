import requests

import time


def buscar_google_books(
    titulo,
    autor
):

    try:
        print("Buscando en Google Books:", titulo, autor);
        query = (
            f"intitle:{titulo}"
            f"+inauthor:{autor}"
        )

        url = (
            "https://www.googleapis.com/books/v1/volumes"
            f"?q={query}"
            "&maxResults=1"
        )

        response = requests.get(
            url,
            timeout=10
        )

        data = response.json()
        print("Respuesta de Google Books:", data)
        items = data.get(
            "items",
            []
        )

        if not items:

            return None

        libro = items[0]

        info = libro.get(
            "volumeInfo",
            {}
        )

        resultado = {

            "generos": info.get(
                "categories",
                []
            ),

            "descripcion_google": info.get(
                "description",
                ""
            ),

            "thumbnail": info.get(
                "imageLinks",
                {}
            ).get(
                "thumbnail",
                ""
            )
        }

        # ---------------------------------------------
        # Evitar rate limit
        # ---------------------------------------------

        time.sleep(10000)

        return resultado

    except Exception:

        return None