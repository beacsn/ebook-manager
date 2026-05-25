import requests

import time


# =========================================================
# BUSCAR LIBRO
# =========================================================

def buscar_openlibrary(
    titulo,
    autor
):

    try:

        print(
            f"Buscando: {titulo}"
        )

        # -------------------------------------------------
        # SEARCH
        # -------------------------------------------------

        url = (
            "https://openlibrary.org/search.json"
            f"?title={titulo}"
        )

        response = requests.get(
            url,
            timeout=10
        )

        data = response.json()

        docs = data.get(
            "docs",
            []
        )

        if not docs:

            print("No encontrado")

            return None

        # -------------------------------------------------
        # PRIMER RESULTADO
        # -------------------------------------------------

        libro = docs[0]

        print(
            "Encontrado:",
            libro.get("title")
        )

        # -------------------------------------------------
        # WORK KEY
        # -------------------------------------------------

        work_key = libro.get(
            "key"
        )

        generos = []

        descripcion = ""

        # -------------------------------------------------
        # WORK DETAILS
        # -------------------------------------------------

        if work_key:

            work_url = (
                f"https://openlibrary.org"
                f"{work_key}.json"
            )

            work_response = requests.get(
                work_url,
                timeout=10
            )

            work_data = work_response.json()

            generos = work_data.get(
                "subjects",
                []
            )[:10]

            desc = work_data.get(
                "description",
                ""
            )

            if isinstance(desc, dict):

                descripcion = desc.get(
                    "value",
                    ""
                )

            else:

                descripcion = desc

        # -------------------------------------------------
        # COVER
        # -------------------------------------------------

        thumbnail = ""

        cover_id = libro.get(
            "cover_i"
        )

        if cover_id:

            thumbnail = (
                "https://covers.openlibrary.org/b/id/"
                f"{cover_id}-L.jpg"
            )

        resultado = {

            "generos": generos,

            "descripcion_google": descripcion,

            "thumbnail": thumbnail
        }

        time.sleep(0.2)

        return resultado

    except Exception as e:

        print(
            "Error OpenLibrary:",
            e
        )

        return None