# Semesterprojekt VisionAI: Jonathan Holzinger, Mathis Laken, Kayra Ciftci
# Import der benötigten Bibliotheken
import streamlit as st  # Streamlit für die Benutzeroberfläche
import base64  # Base64 zum Kodieren von Bilddaten
import requests  # Für HTTP-Anfragen an die API
import pandas as pd  # Pandas für Datenmanipulation
import json  # Zum Arbeiten mit JSON-Daten
import os  # Betriebssystemfunktionen wie Dateiverwaltung

# OpenAI API Key
api_key = st.secrets["api_key_streamlit_secret"]

def encode_image(image_path):
    # Bild in Base64 kodieren
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_image
    except Exception as e:
        st.error(f" :X: Fehler beim Kodieren des Bildes: {e}")
        return None

def json_to_dataframe(content):
    try:
        # Entferne die Markdown-Codeblock-Kennzeichnung (```json und ``` am Ende)
        if content.startswith("```json"):
            content = content[7:-3].strip()

        # JSON-Inhalt in ein Python-Dictionary umwandeln
        data = json.loads(content)

        # Verwende ausschließlich den Schlüssel "table"
        if "table" in data:

            # Konvertiere das Dictionary in einen DataFrame
            df = pd.DataFrame(data["table"])

        else:
            st.error("Kein 'table'-Schlüssel in den JSON-Daten gefunden.")
            return None

        # Spaltennamen anpassen, falls notwendig
        if "Description" in df.columns:
            df["Description"] = df["Description"].apply(lambda x: "\n- ".join(x) if isinstance(x, list) else x)

        return df

    except Exception as e:
        st.error(f" :X: Fehler beim Umwandeln des JSON-Inhalts in einen DataFrame: {e}")
        return None



def analyze_image(image_path):
    # Bild kodieren
    base64_image = encode_image(image_path)
    if not base64_image:
        return None

    # API-Anfrage vorbereiten
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Analyze the image and create a table with the following columns: Category and Description. "
                    "The categories are based on the date, participants, and the symbols in the image: Crown = Erfolge, "
                    "Lightbulb = Erkenntnisse, Heart = Positives :black_heart:, Checklist = ToDos. List the corresponding points under the "
                    "appropriate category, including any text on the right side of the image as additional bullet points in the same row. "
                    "Omit the symbol labels. The table should be well-structured and formatted as pure JSON, using the key 'table'. "
                    "Ignore the use of colors. If bullet points are written side by side, write them on separate lines in the table. "
                    "Include all the text from the image. Return the content directly as valid JSON with the key 'table' without any additional characters or formatting."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }
    # API-Anfrage senden
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()  # Überprüft auf HTTP-Fehler
    except requests.exceptions.RequestException as e:
        st.error(f" :X: Fehler bei der API-Anfrage: {e}")
        return None

    # API-Antwort verarbeiten
    with st.expander("Hier klicken für die API-Rohantwort :point_up_2:"):
        st.write('''

        ''')
        try:
            data = response.json()
            st.write("API-Rohantwort:", data)  # Debugging: Rohdaten anzeigen
            if 'choices' not in data or not data['choices']:
                st.error("Keine gültigen Daten in der API-Antwort.")
                return None
            content = data['choices'][0]['message']['content']
            st.write("Content der API-Antwort:", content)  # Debugging: Inhalt anzeigen

            # JSON in DataFrame umwandeln
            df = json_to_dataframe(content)
            return df
        except json.JSONDecodeError as e:
            st.error(f" :X: Fehler beim Dekodieren des JSON-Inhalts: {e}")
            return None
        except Exception as e:
            st.error(f" :X: Allgemeiner Fehler bei der Verarbeitung der API-Antwort: {e}")
            return None


# Erstelle den temporären Ordner, falls er nicht existiert
if not os.path.exists("temp"):
    os.makedirs("temp")

# Streamlit App Titel
st.title(":orange[Retrospektive - OCR] :camera:")

# Widget für die Kameraaufnahme
camera_image = st.camera_input("**Mache ein Bild deiner Retrospektive:** :camera_with_flash:")

if camera_image:
    # Zeige das aufgenommene Bild an
    st.image(camera_image, caption="Aufgenommenes Bild", use_column_width=True)


    # Speichere das aufgenommene Bild temporär
    temp_path = os.path.join("temp", "camera_image.jpg")
    with open(temp_path, "wb") as f:
        f.write(camera_image.getbuffer())

    # Rufe die Analyse-Funktion auf
    df = analyze_image(temp_path)
    if df is not None:
        # Zeige die Tabelle auf der Streamlit-Seite an
        st.write("Analyseergebnisse:")
        st.table(df)

        # CSV-Datei zur Verfügung stellen
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Ergebnisse als CSV herunterladen",
            data=csv,
            file_name="analyse_ergebnisse_camera_image.csv",
            mime="text/csv",
        )
    else:
        st.error(f"Fehler bei der Analyse des aufgenommenen Bildes :exclamation:")

# Drag-and-Drop Feld für den Bildupload
uploaded_files = st.file_uploader("**Ziehe einfach ein Bild hierhin oder klicke auf Hochladen:** :file_folder:", type=["jpg", "jpeg", "png"],
                                  accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        # Zeige das hochgeladene Bild an
        st.image(uploaded_file, caption=f":frame_with_picture: Hochgeladenes Bild: {uploaded_file.name}", use_column_width=True)

        # Speichere das Bild temporär
        temp_path = os.path.join("temp", uploaded_file.name)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Rufe die Analyse-Funktion auf
        df = analyze_image(temp_path)
        if df is not None:
            # Zeige die Tabelle auf der Streamlit-Seite an
            st.write(":chart_with_upwards_trend: Analyseergebnisse:")
            st.table(df)

            # CSV-Datei zur Verfügung stellen
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Ergebnisse als CSV herunterladen :page_facing_up:",
                data=csv,
                file_name=f"analyse_ergebnisse_{uploaded_file.name}.csv",
                mime="text/csv",
            )
        else:
            st.error(f"Fehler bei der Analyse von {uploaded_file.name} :exclamation:")

# Cleanup temporäre Dateien nach der Verarbeitung
if os.path.exists("temp"):
    for file in os.listdir("temp"):
        os.remove(os.path.join("temp", file))
