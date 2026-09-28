import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

st.set_page_config(
    page_title="Aplicación Estadística",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Aplicación Interactiva de Estadística")
st.subheader("Medidas de posición y análisis del Box-Plot")
st.write("Aplicación desarrollada para Ingeniería de Sistemas")

# --------------------------------------------------
# FUNCIONES
# --------------------------------------------------

def calcular_cuartiles(datos):
    datos = sorted(datos)
    n = len(datos)

    mediana = np.median(datos)

    if n % 2 == 0:
        mitad_inferior = datos[:n // 2]
        mitad_superior = datos[n // 2:]
    else:
        mitad_inferior = datos[:n // 2]
        mitad_superior = datos[n // 2 + 1:]

    q1 = np.median(mitad_inferior)
    q3 = np.median(mitad_superior)

    return q1, mediana, q3


def calcular_estadisticas(datos):

    datos = np.array(datos, dtype=float)
    datos_ordenados = np.sort(datos)

    n = len(datos)

    media = np.mean(datos)
    mediana = np.median(datos)

    # Moda
    valores, frecuencias = np.unique(datos, return_counts=True)
    frecuencia_maxima = frecuencias.max()

    if frecuencia_maxima == 1:
        moda = "Sin moda"
    else:
        modas = valores[frecuencias == frecuencia_maxima]
        moda = ", ".join(str(x) for x in modas)

    # Dispersión
    rango = np.max(datos) - np.min(datos)

    varianza = np.var(datos, ddof=1)

    desviacion = np.std(datos, ddof=1)

    # Cuartiles
    q1, q2, q3 = calcular_cuartiles(datos)

    # RIC
    ric = q3 - q1

    # Límites para valores atípicos
    limite_inferior = q1 - 1.5 * ric
    limite_superior = q3 + 1.5 * ric

    # Valores atípicos
    atipicos = datos[
        (datos < limite_inferior) |
        (datos > limite_superior)
    ]

    # Bigotes
    datos_sin_atipicos = datos[
        (datos >= limite_inferior) &
        (datos <= limite_superior)
    ]

    bigote_inferior = np.min(datos_sin_atipicos)
    bigote_superior = np.max(datos_sin_atipicos)

    return {
        "n": n,
        "datos": datos,
        "ordenados": datos_ordenados,
        "media": media,
        "mediana": mediana,
        "moda": moda,
        "rango": rango,
        "varianza": varianza,
        "desviacion": desviacion,
        "q1": q1,
        "q2": q2,
        "q3": q3,
        "ric": ric,
        "limite_inferior": limite_inferior,
        "limite_superior": limite_superior,
        "atipicos": atipicos,
        "bigote_inferior": bigote_inferior,
        "bigote_superior": bigote_superior
    }


# --------------------------------------------------
# DATOS DE EJEMPLO
# --------------------------------------------------

caso1 = [
    120, 135, 128, 142, 150,
    138, 125, 132, 145, 155,
    130, 140, 127, 148, 135,
    160, 129, 133, 137, 142
]

caso2 = [
    42, 45, 44, 47, 43,
    46, 45, 48, 44, 46,
    43, 45, 47, 44, 46,
    45, 43, 120, 47, 46
]

# --------------------------------------------------
# SELECCIÓN DE DATOS
# --------------------------------------------------

st.sidebar.header("📂 Fuente de datos")

opcion = st.sidebar.radio(
    "Seleccione una opción:",
    [
        "Caso 1 - Servidor",
        "Caso 2 - Algoritmo",
        "Cargar archivo"
    ]
)

datos = None

if opcion == "Caso 1 - Servidor":

    datos = caso1

    st.info(
        "Caso 1: tiempos de respuesta de un servidor (ms)."
    )

elif opcion == "Caso 2 - Algoritmo":

    datos = caso2

    st.info(
        "Caso 2: tiempos de ejecución de un algoritmo (ms)."
    )

else:

    archivo = st.sidebar.file_uploader(
        "Cargue un archivo CSV o Excel",
        type=["csv", "xlsx"]
    )

    if archivo is not None:

        try:

            if archivo.name.endswith(".csv"):
                df = pd.read_csv(archivo)

            else:
                df = pd.read_excel(archivo)

            st.write("### Vista previa de los datos")
            st.dataframe(df)

            columnas_numericas = df.select_dtypes(
                include=np.number
            ).columns.tolist()

            if len(columnas_numericas) == 0:

                st.error(
                    "El archivo no contiene columnas numéricas."
                )

            else:

                columna = st.sidebar.selectbox(
                    "Seleccione la columna:",
                    columnas_numericas
                )

                datos = df[columna].dropna().tolist()

        except Exception as e:

            st.error(
                f"No se pudo leer el archivo: {e}"
            )


# --------------------------------------------------
# ANÁLISIS
# --------------------------------------------------

if datos is not None and len(datos) >= 4:

    resultados = calcular_estadisticas(datos)

    st.success(
        f"Se analizaron {resultados['n']} datos correctamente."
    )

    # --------------------------------------------------
    # TENDENCIA CENTRAL
    # --------------------------------------------------

    st.header("📌 Medidas de tendencia central")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Media",
        f"{resultados['media']:.2f}"
    )

    col2.metric(
        "Mediana",
        f"{resultados['mediana']:.2f}"
    )

    col3.metric(
        "Moda",
        resultados["moda"]
    )

    # --------------------------------------------------
    # DISPERSIÓN
    # --------------------------------------------------

    st.header("📏 Medidas de dispersión")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Rango",
        f"{resultados['rango']:.2f}"
    )

    col2.metric(
        "Varianza muestral",
        f"{resultados['varianza']:.2f}"
    )

    col3.metric(
        "Desviación estándar",
        f"{resultados['desviacion']:.2f}"
    )

    # --------------------------------------------------
    # CUARTILES
    # --------------------------------------------------

    st.header("📍 Medidas de posición")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Q1 (P25)",
        f"{resultados['q1']:.2f}"
    )

    col2.metric(
        "Q2 (P50)",
        f"{resultados['q2']:.2f}"
    )

    col3.metric(
        "Q3 (P75)",
        f"{resultados['q3']:.2f}"
    )

    col4.metric(
        "RIC",
        f"{resultados['ric']:.2f}"
    )

    # --------------------------------------------------
    # PERCENTIL DINÁMICO
    # --------------------------------------------------

    st.subheader("🔢 Percentil dinámico")

    percentil = st.slider(
        "Seleccione el percentil:",
        min_value=1,
        max_value=99,
        value=90
    )

    valor_percentil = np.percentile(
        resultados["datos"],
        percentil
    )

    st.metric(
        f"P{percentil}",
        f"{valor_percentil:.2f}"
    )

    # --------------------------------------------------
    # LÍMITES
    # --------------------------------------------------

    st.header("⚠️ Detección de valores atípicos")

    col1, col2 = st.columns(2)

    col1.metric(
        "Límite inferior",
        f"{resultados['limite_inferior']:.2f}"
    )

    col2.metric(
        "Límite superior",
        f"{resultados['limite_superior']:.2f}"
    )

    st.latex(
        r"LI = Q_1 - 1.5(RIC)"
    )

    st.latex(
        r"LS = Q_3 + 1.5(RIC)"
    )

    if len(resultados["atipicos"]) > 0:

        st.warning(
            "Se encontraron valores atípicos:"
        )

        st.write(
            resultados["atipicos"].tolist()
        )

    else:

        st.success(
            "No se encontraron valores atípicos."
        )

    # --------------------------------------------------
    # BOX-PLOT
    # --------------------------------------------------

    st.header("📦 Diagrama de Cajas y Alambres")

    q1 = resultados["q1"]
    mediana = resultados["mediana"]
    q3 = resultados["q3"]

    bigote_inferior = resultados["bigote_inferior"]
    bigote_superior = resultados["bigote_superior"]

    media = resultados["media"]

    fig = go.Figure()

    # Caja
    fig.add_shape(
        type="rect",
        x0=q1,
        x1=q3,
        y0=-0.3,
        y1=0.3
    )

    # Línea de la mediana
    fig.add_shape(
        type="line",
        x0=mediana,
        x1=mediana,
        y0=-0.3,
        y1=0.3,
        line=dict(width=4)
    )

    # Bigote inferior
    fig.add_shape(
        type="line",
        x0=bigote_inferior,
        x1=q1,
        y0=0,
        y1=0,
        line=dict(width=3)
    )

    # Bigote superior
    fig.add_shape(
        type="line",
        x0=q3,
        x1=bigote_superior,
        y0=0,
        y1=0,
        line=dict(width=3)
    )

    # Límites
    fig.add_vline(
        x=resultados["limite_inferior"],
        line_dash="dot",
        annotation_text="LI"
    )

    fig.add_vline(
        x=resultados["limite_superior"],
        line_dash="dot",
        annotation_text="LS"
    )

    # Promedio
    fig.add_trace(
        go.Scatter(
            x=[media],
            y=[0],
            mode="markers",
            marker=dict(
                symbol="diamond",
                size=14
            ),
            name="Promedio",
            hovertemplate=f"Promedio: {media:.2f}<extra></extra>"
        )
    )

    # Valores atípicos
    if len(resultados["atipicos"]) > 0:

        fig.add_trace(
            go.Scatter(
                x=resultados["atipicos"],
                y=[0] * len(resultados["atipicos"]),
                mode="markers",
                marker=dict(size=12),
                name="Valores atípicos",
                hovertemplate="Atípico: %{x}<extra></extra>"
            )
        )

    fig.update_layout(
        title="Box-Plot estadístico",
        xaxis_title="Valor",
        yaxis=dict(
            visible=False,
            range=[-1, 1]
        ),
        height=450,
        showlegend=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------
    # TABLA RESUMEN
    # --------------------------------------------------

    st.header("📋 Resumen estadístico")

    resumen = pd.DataFrame({
        "Medida": [
            "Cantidad de datos",
            "Media",
            "Mediana",
            "Moda",
            "Mínimo",
            "Q1",
            "Q2",
            "Q3",
            "Máximo",
            "RIC",
            "Límite inferior",
            "Límite superior",
            "Desviación estándar",
            "Varianza"
        ],
        "Resultado": [
            resultados["n"],
            round(resultados["media"], 2),
            round(resultados["mediana"], 2),
            resultados["moda"],
            np.min(resultados["datos"]),
            resultados["q1"],
            resultados["q2"],
            resultados["q3"],
            np.max(resultados["datos"]),
            resultados["ric"],
            resultados["limite_inferior"],
            resultados["limite_superior"],
            resultados["desviacion"],
            resultados["varianza"]
        ]
    })

    st.dataframe(
        resumen,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------
    # DATOS ORDENADOS
    # --------------------------------------------------

    with st.expander("🔎 Ver datos ordenados"):

        st.write(
            resultados["ordenados"].tolist()
        )

else:

    st.info(
        "Seleccione un caso de ejemplo o cargue un archivo "
        "con al menos 4 datos numéricos."
    )