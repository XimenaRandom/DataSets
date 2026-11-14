from pathlib import Path

import pandas as pd


def main() -> None:
    folder = Path(__file__).resolve().parent
    input_path = folder / "netflix_titles.csv"
    output_path = folder / "netflix_clean.csv"

    df = pd.read_csv(input_path)
    original_records = len(df)
    original_columns = len(df.columns)

    text_columns = [
        column
        for column in df.columns
        if not pd.api.types.is_numeric_dtype(df[column])
    ]
    for column in text_columns:
        df[column] = (
            df[column]
            .astype("string")
            .str.replace(r"[\r\n\t]+", " ", regex=True)
            .str.strip()
            .str.normalize("NFC")
            .replace("", pd.NA)
        )

    df["date_added"] = (
        pd.to_datetime(df["date_added"], format="%B %d, %Y", errors="coerce")
        .dt.strftime("%d/%m/%Y")
        .astype("string")
    )

    duration_values = df["duration"].str.extract(r"^(\d+)\s+min$", expand=False)
    duration_min = pd.to_numeric(duration_values, errors="coerce").astype("Int64")
    movie_rows = df["type"].str.casefold().eq("movie").fillna(False)
    df["duration_min"] = duration_min.where(movie_rows, pd.NA)

    exact_duplicates_removed = int(df.duplicated().sum())
    df = df.drop_duplicates()

    missing_ids_removed = int(df["show_id"].isna().sum())
    df = df.loc[df["show_id"].notna()].copy()

    duplicate_ids_removed = int(df["show_id"].duplicated().sum())
    df = df.drop_duplicates(subset="show_id", keep="first")

    movie_rows = df["type"].str.casefold().eq("movie").fillna(False)
    positive_duration = df["duration_min"].gt(0).fillna(False)
    movies_with_duration = int((movie_rows & positive_duration).sum())
    movies_without_positive_duration = int((movie_rows & ~positive_duration).sum())

    df.to_csv(
        output_path,
        sep=",",
        header=True,
        index=False,
        encoding="utf-8-sig",
    )

    report = pd.DataFrame(
        [
            ("Registros del archivo original, sin cabecera", original_records),
            ("Columnas del archivo original", original_columns),
            ("Filas completamente duplicadas eliminadas", exact_duplicates_removed),
            (
                "Registros sin show_id eliminados después de retirar duplicados",
                missing_ids_removed,
            ),
            (
                "Registros con show_id repetido eliminados posteriormente",
                duplicate_ids_removed,
            ),
            ("Registros del archivo limpio", len(df)),
            (
                "Películas con duration_min numérica mayor que cero",
                movies_with_duration,
            ),
            (
                "Películas sin una duración numérica mayor que cero",
                movies_without_positive_duration,
            ),
        ],
        columns=["Indicador", "Cantidad"],
    )

    print(f"Archivo limpio guardado en: {output_path}")
    print("\nTabla 1. Resultado de la limpieza")
    print(report.to_string(index=False))


if __name__ == "__main__":
    main()