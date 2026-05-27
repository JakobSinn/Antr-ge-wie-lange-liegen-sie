import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

urlbase = "https://schabernack.stura.uni-heidelberg.de/sitzungsverwaltung/Sitzungsunterlagen-digital/Protokoll/{}-Studierendenrat"
anfang = 197
ende = 225
sondersitzungscheck = []
df = pd.DataFrame(columns=["sitzung", "titel"])


def topsnehmen(urlbase, sitzung):
    url = urlbase.format(sitzung)
    try:
        html = requests.get(url).text
    except requests.RequestException as e:
        print(f"Fehler beim Abrufen der Seite {sitzung}: {e}")
        return []

    soup = BeautifulSoup(html, "html.parser")

    rows = []

    # Tagesordnungspunkte stehen in Heading-Tags
    for tag in soup.find_all(["span"]):
        text = tag.get_text(" ", strip=True)
        if not text:
            continue

        if re.match(r"^\d+\.\d+(?:\.\d+)*\.\s+", text):
            # Nummer vorne entfernen
            title = re.sub(r"^\d+\.\d+(?:\.\d+)*\.\s*", " ", text)
            rows.append(title)
    return rows


for sitzung in range(anfang, ende + 1):
    rows = topsnehmen(urlbase, sitzung)

    print(f"Sitzung {sitzung}: {len(rows)} Tagesordnungspunkte gefunden.")
    if len(rows) < 5:
        sondersitzungscheck.append(sitzung)

    df_current = pd.DataFrame({"sitzung": [sitzung] * len(rows), "titel": rows})
    if not df_current.empty:
        df = pd.concat([df, df_current], ignore_index=True)

urlbasesonder = urlbase + "-Sondersitzung"
for sitzung in sondersitzungscheck:
    rows = topsnehmen(urlbasesonder, sitzung)

    print(f"Sondersitzung {sitzung}: {len(rows)} Tagesordnungspunkte gefunden.")
    df_sondersitzung = pd.DataFrame({"sitzung": [sitzung] * len(rows), "titel": rows})
    df = pd.concat([df, df_sondersitzung], ignore_index=True)
df.to_csv("antraege.csv", index=False, encoding="utf-8")

print(df.head(10))

# hier könnte man noch händisch filtern und eine nette grafik erstellen oder so
