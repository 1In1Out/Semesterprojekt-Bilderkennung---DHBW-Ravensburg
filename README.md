# Bildanalyse mit Streamlit und OpenAI API

## Semesterprojekt VisionAI

Dieses Projekt wurde im Rahmen des Semesterprojekts VisionAI erstellt. Die Autoren sind Jonathan Holzinger, Mathis Laken und Kayra Ciftci.

## Übersicht

Dieses Projekt implementiert eine Anwendung zur Analyse von Bildern mithilfe der OpenAI API. Es nutzt die Streamlit-Bibliothek, um eine benutzerfreundliche Oberfläche zu bieten, über die Nutzer Bilder hochladen und deren Inhalte analysieren können. Die Ergebnisse werden in Form einer Tabelle dargestellt und können als CSV-Datei heruntergeladen werden.

## Funktionen

- **Bild-Upload:** Nutzer können Bilder im JPG-, JPEG- oder PNG-Format hochladen.
- **Foto-Funktion:** Nutzer können ein Foto aufnehmen, welches dann direkt ausgewertet wird. 
- **Bildanzeige:** Die hochgeladenen Bilder werden auf der Streamlit-Seite angezeigt.
- **Bildanalyse:** Die Anwendung kodiert das Bild in Base64 und sendet es an die OpenAI API zur Analyse. Das Ergebnis ist eine Tabelle mit Kategorien und Beschreibungen, die aus dem Bild extrahiert werden.
- **Tabellendarstellung:** Die Analyseergebnisse werden als Tabelle dargestellt.
- **CSV-Download:** Nutzer können die Tabelle als CSV-Datei herunterladen.
- **Temporäre Speicherung:** Die hochgeladenen Bilder werden temporär gespeichert und nach der Analyse wieder gelöscht.

## Voraussetzungen

- Python 3.7 oder höher
- Folgende Python-Bibliotheken:
  - `streamlit`
  - `base64`
  - `requests`
  - `pandas`
  - `json`
  - `os`

Diese können mit folgendem Befehl installiert werden:

```bash
pip install streamlit pandas requests
