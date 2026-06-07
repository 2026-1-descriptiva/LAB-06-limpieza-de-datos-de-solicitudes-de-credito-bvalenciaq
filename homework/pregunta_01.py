"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
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

ruta = 'files/input/solicitudes_de_credito.csv'


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    df = pd.read_csv(ruta,index_col=0,sep = ';')

    df["sexo"] = normaliza_texto(df["sexo"])
    df["idea_negocio"] = normaliza_texto(df["idea_negocio"])
    df["tipo_de_emprendimiento"] = normaliza_texto(df["tipo_de_emprendimiento"])
    #df["barrio"] = normaliza_texto(df["barrio"])
    df["línea_credito"] = normaliza_texto(df["línea_credito"])


    df["monto_del_credito"] = (
    df["monto_del_credito"]
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.replace(".00", "", regex=False)
    .str.strip()
)
    
    df["fecha_de_beneficio"] = pd.to_datetime(
        df["fecha_de_beneficio"], errors="coerce", format="mixed", dayfirst=True
    ).dt.strftime("%Y-%m-%d")


    df["barrio"] = (
        df["barrio"]
        .str.lower()
        .str.strip()
        .str.replace("-", " ", regex=False)
        .str.replace("_", " ", regex=False)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )


    df_limpio = df.dropna()
    df_limpio = df_limpio.drop_duplicates()

    df_limpio.to_csv('files/output/solicitudes_de_credito.csv', index = False,sep=";")

if __name__ == "__main__":
    pregunta_01()
