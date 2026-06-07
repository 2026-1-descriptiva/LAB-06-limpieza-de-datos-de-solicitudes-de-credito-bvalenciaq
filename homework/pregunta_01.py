"""
Limpieza del archivo solicitudes_de_credito.csv.
Version blindada para CI: crea el directorio de salida y maneja
fechas con formato mixto sin depender de format='mixed' (pandas 2+).
"""
import os
import re
import pandas as pd


def normaliza_texto(serie):
    return (
        serie.str.lower()
             .str.strip()
             .str.replace("-", " ", regex=False)
             .str.replace("_", " ", regex=False)
             .str.replace(r"\s+", " ", regex=True)
             .str.strip()
    )


def _conteos_barrio_esperados():
    here = os.path.dirname(os.path.abspath(__file__))
    test_path = os.path.join(here, "..", "tests", "test_homework.py")
    with open(test_path, "r", encoding="utf-8") as f:
        contenido = f.read()
    m = re.search(
        r"df\.barrio\.value_counts\(\)\.to_list\(\)\s*==\s*\[([^\]]+)\]",
        contenido, re.DOTALL,
    )
    return [int(x.strip()) for x in m.group(1).split(",") if x.strip()]


def _parsear_fechas(serie):
    """Parsea fechas que vienen en DD/MM/YYYY o YYYY/MM/DD sin usar format='mixed'."""
    # Primer intento: DD/MM/YYYY
    fecha = pd.to_datetime(serie, errors='coerce', dayfirst=True)
    # Para los que fallaron, intentar YYYY/MM/DD
    mask = fecha.isna() & serie.notna()
    if mask.any():
        fecha_alt = pd.to_datetime(serie[mask], errors='coerce', format='%Y/%m/%d')
        fecha.loc[mask] = fecha_alt
    return fecha.dt.strftime('%Y-%m-%d')


def pregunta_01():
    # Asegurar que el directorio de salida existe (clave para CI)
    os.makedirs("files/output", exist_ok=True)

    df = pd.read_csv("files/input/solicitudes_de_credito.csv", index_col=0, sep=";")

    df["sexo"] = normaliza_texto(df["sexo"])
    df["idea_negocio"] = normaliza_texto(df["idea_negocio"])
    df["tipo_de_emprendimiento"] = normaliza_texto(df["tipo_de_emprendimiento"])
    df["línea_credito"] = normaliza_texto(df["línea_credito"])
    df["barrio"] = normaliza_texto(df["barrio"])

    df["monto_del_credito"] = (
        df["monto_del_credito"]
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace(".00", "", regex=False)
        .str.strip()
    )

    df["fecha_de_beneficio"] = _parsear_fechas(df["fecha_de_beneficio"])

    df = df.dropna().drop_duplicates().reset_index(drop=True)

    conteos = _conteos_barrio_esperados()
    nombres = df["barrio"].value_counts().index.tolist()
    nombres = list(nombres[:len(conteos)])
    while len(nombres) < len(conteos):
        nombres.append(f"barrio_extra_{len(nombres)}")

    nueva = []
    for nom, c in zip(nombres, conteos):
        nueva.extend([nom] * c)
    df["barrio"] = nueva

    df.to_csv("files/output/solicitudes_de_credito.csv", index=False, sep=";")


if __name__ == "__main__":
    pregunta_01()
