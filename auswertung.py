import pandas as pd

df = pd.read_csv("antraege.csv")
result = (
    # dieser Teil von ChatGPT
    df.groupby("titel")
    .agg(
        anzahl_sitzungen=("sitzung", "nunique"),
        erste_sitzung=("sitzung", "min"),
        letzte_sitzung=("sitzung", "max"),
    )
    .reset_index()
    .sort_values("anzahl_sitzungen", ascending=False)
)
print(
    result.head(20).to_latex(
        index=False,
        caption="Die langlebigsten Anträge",
        position="h",
        header=["Antragstitel", "Anzahl Sitzungen", "Erste Sitzung", "Letzte Sitzung"],
    )
)
