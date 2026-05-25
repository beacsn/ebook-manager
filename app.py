import streamlit as st
import os
import json
import html
import math


from scanner import escanear_biblioteca
from metadata import extraer_portada_epub
from cache import (
    cargar_cache,
    guardar_cache
)
from openlibrary import buscar_openlibrary


# =========================================================
# CONFIGURACIÓN
# =========================================================

RUTA_BIBLIOTECA = r"aaa"

MAX_RESULTADOS = 200

LIBROS_POR_PAGINA = 40


# =========================================================
# CONFIGURACIÓN STREAMLIT
# =========================================================

st.set_page_config(
    page_title="Mi Biblioteca",
    layout="wide"
)


st.title("📚 Mi Biblioteca")


# =========================================================
# CARGA DE LIBROS
# =========================================================

def refrescar_biblioteca():

    with st.spinner(
        "Escaneando biblioteca..."
    ):

        libros = escanear_biblioteca(
            RUTA_BIBLIOTECA
        )

        guardar_cache(libros)

        st.cache_data.clear()


def cargar_libros():

    print("Cargando libros...")

    libros = cargar_cache()

    if libros is not None:

        return libros

    libros = escanear_biblioteca(
        RUTA_BIBLIOTECA
    )

    print("Voy a guardar cache")
    guardar_cache(libros)

    return libros


libros = cargar_libros()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("Filtros")

if st.sidebar.button(
    "🔄 Recargar biblioteca"
):

    refrescar_biblioteca()

    st.success(
        "Biblioteca actualizada"
    )

    st.rerun()

if st.sidebar.button(
    "📡 Enriquecer libros"
):

    MAX_ENRIQUECER = 500
    contador = 0
    procesados = 0

    progreso = st.progress(0)

    total = len(libros)

    for libro in libros:

        # -------------------------------------------------
        # YA ENRIQUECIDO
        # -------------------------------------------------

        if libro.enriquecido:
            continue

        print(
            f"Enriqueciendo: {libro.titulo}"
        )

        resultado = buscar_openlibrary(
            libro.titulo,
            libro.autor
        )

        if resultado:

            libro.generos = resultado[
                "generos"
            ]

            libro.descripcion_google = resultado[
                "descripcion_google"
            ]

            libro.thumbnail = resultado[
                "thumbnail"
            ]

        libro.enriquecido = True

        procesados += 1

        # -------------------------------------------------
        # GUARDADO INCREMENTAL
        # -------------------------------------------------

        guardar_cache(libros)

        # -------------------------------------------------
        # LÍMITE
        # -------------------------------------------------

        if procesados >= MAX_ENRIQUECER:

            break


    st.success(
        "Enriquecimiento completado"
    )

    st.rerun()


# ---------------------------------------------------------
# FILTRO LETRA
# ---------------------------------------------------------

letras = sorted(
    list(set(libro.autor[0].upper() for libro in libros))
)

letra_seleccionada = st.sidebar.selectbox(
    "Letra",
    ["Todas"] + letras
)


# ---------------------------------------------------------
# FILTRO AUTOR
# ---------------------------------------------------------

autores_filtrados = []

for libro in libros:

    if letra_seleccionada != "Todas":

        if not libro.autor.upper().startswith(
            letra_seleccionada
        ):
            continue

    autores_filtrados.append(libro.autor)


autores_filtrados = sorted(
    list(set(autores_filtrados))
)


autor_seleccionado = st.sidebar.selectbox(
    "Autor",
    ["Todos"] + autores_filtrados
)


# ---------------------------------------------------------
# BÚSQUEDA
# ---------------------------------------------------------

texto_busqueda = st.sidebar.text_input(
    "Buscar título"
)


# =========================================================
# FILTRADO FINAL
# =========================================================

libros_filtrados = []

for libro in libros:

    # -----------------------------------------------------
    # FILTRO LETRA
    # -----------------------------------------------------

    if letra_seleccionada != "Todas":

        if not libro.autor.upper().startswith(
            letra_seleccionada
        ):
            continue

    # -----------------------------------------------------
    # FILTRO AUTOR
    # -----------------------------------------------------

    if autor_seleccionado != "Todos":

        if libro.autor != autor_seleccionado:
            continue

    # -----------------------------------------------------
    # BÚSQUEDA TEXTO
    # -----------------------------------------------------

    if texto_busqueda:

        if texto_busqueda.lower() not in libro.titulo.lower():
            continue

    libros_filtrados.append(libro)


# =========================================================
# INFORMACIÓN GENERAL
# =========================================================

st.write(f"Libros totales: {len(libros)}")

st.write(
    f"Resultados filtrados: {len(libros_filtrados)}"
)


# =========================================================
# PAGINACIÓN
# =========================================================

total_paginas = math.ceil(
    len(libros_filtrados) / LIBROS_POR_PAGINA
)

pagina_actual = st.number_input(
    "Página",
    min_value=1,
    max_value=max(total_paginas, 1),
    value=1
)

inicio = (
    (pagina_actual - 1)
    * LIBROS_POR_PAGINA
)

fin = inicio + LIBROS_POR_PAGINA

libros_pagina = libros_filtrados[
    inicio:fin
]


# =========================================================
# MOSTRAR LIBROS
# =========================================================

NUM_COLUMNAS = 4

columnas = st.columns(NUM_COLUMNAS)

for indice, libro in enumerate(
    libros_pagina
):

    columna = columnas[indice % NUM_COLUMNAS]

    with columna:

        if libro.formato == ".epub":

            portada = extraer_portada_epub(
                libro.ruta
            )

            if portada:

                st.image(
                    portada,
                    width="stretch"
                )            

        #st.subheader(libro.titulo)
        titulo_html = html.escape(
            libro.titulo
        )

        autor_html = html.escape(
            libro.autor
        )
        st.markdown(
            f"""
            <p style="
                font-size:18px;
                font-weight:bold;
                text-align:center;
                margin-bottom:0px;
            ">
                {titulo_html}
            </p>

            <p style="
                font-size:14px;
                color:#BBBBBB;
                text-align:center;
                margin-top:0px;
            ">
                {autor_html}
            </p>
            """,
            unsafe_allow_html=True
        )

        #st.caption(libro.formato)

        col1, col2 = st.columns(2)

        with col1:

            st.caption(libro.formato)

        with col2:

            if libro.enriquecido:

                st.caption("✅")

            else:

                st.caption("🟡")


        col_btn1, col_btn2 = st.columns(2)

        # -------------------------------------------------
        # ABRIR
        # -------------------------------------------------

        with col_btn1:

            if st.button(
                "Abrir",
                key=f"abrir_{libro.ruta}"
            ):

                os.startfile(libro.ruta)

        # -------------------------------------------------
        # ENRIQUECER
        # -------------------------------------------------

        with col_btn2:

            if st.button(
                "📡",
                key=f"enriquecer_{libro.ruta}"
            ):

                resultado = buscar_openlibrary(
                    libro.titulo,
                    libro.autor
                )

                if resultado:

                    libro.generos = resultado[
                        "generos"
                    ]

                    libro.descripcion_google = resultado[
                        "descripcion_google"
                    ]

                    libro.thumbnail = resultado[
                        "thumbnail"
                    ]

                    libro.enriquecido = True

                    guardar_cache(libros)

                    st.success(
                        "Libro enriquecido"
                    )

                    st.rerun()

                else:

                    st.warning(
                        "No encontrado"
                    )

        with st.expander("Detalles"):

            # -------------------------------------------------
            # DESCRIPCIÓN EPUB
            # -------------------------------------------------

            if libro.descripcion:

                st.write(libro.descripcion)

            # -------------------------------------------------
            # DESCRIPCIÓN OPENLIBRARY
            # -------------------------------------------------

            elif libro.descripcion_google:

                st.write(libro.descripcion_google)

            # -------------------------------------------------
            # IDIOMA
            # -------------------------------------------------

            if libro.idioma:

                st.write(
                    f"🌍 Idioma: {libro.idioma}"
                )

            # -------------------------------------------------
            # GÉNEROS
            # -------------------------------------------------

            if libro.generos:

                st.write("🎭 Géneros:")

                st.write(
                    ", ".join(libro.generos)
                )

            # -------------------------------------------------
            # ESTADO
            # -------------------------------------------------

            if libro.enriquecido:

                st.success(
                    "Libro enriquecido"
                )

            else:

                st.warning(
                    "Pendiente de enriquecer"
                )


# =========================================================
# AVISO LÍMITE
# =========================================================

if len(libros_filtrados) > MAX_RESULTADOS:

    st.warning(
        f"Mostrando solo los primeros "
        f"{MAX_RESULTADOS} resultados"
    )