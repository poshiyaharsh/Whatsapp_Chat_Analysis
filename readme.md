# WhatsApp Chat Analyzer

A Streamlit web app to analyze exported WhatsApp chats.  
It shows detailed statistics, timelines, activity patterns, word usage, emojis and more.

## Features

- **Upload & Preprocessing**
  - Upload a WhatsApp `.txt` export (12‑hour timestamp format with AM/PM).
  - Cleans data, handles group notifications, media markers, links, and emojis.
  - Caching via `st.cache_data` for faster reruns.

- **Filters**
  - Optional **date range filter**.
  - Optional **keyword filter** (“show only messages containing …”).
  - Per‑user or **Overall** selection.

- **Overview**
  - Total messages
  - Total words
  - Media shared
  - Links shared

- **Timelines**
  - Monthly timeline of message counts.
  - Daily timeline of message counts.

- **Activity**
  - Most busy day of week.
  - Most busy month.
  - Weekly activity heatmap (day vs period).
  - Hourly activity (what time of day people chat most).
  - Most busy users (when viewing Overall).

- **Words & Emojis**
  - Wordcloud with English + Hinglish stopword removal (`stop_hinglish.txt`).
  - Most common words.
  - Emoji table + emoji pie chart.

- **Advanced Analytics**
  - Sentiment overview (positive / neutral / negative, using TextBlob).
  - Message length distribution + average words per message.
  - User comparison (messages, words, media, links for two users).
  - Export filtered data as CSV.

## Tech Stack

- **Python**
- **Streamlit**
- **pandas**
- **matplotlib**, **seaborn**
- **wordcloud**
- **urlextract**
- **emoji**
- **textblob**

## Installation

```bash
# create and activate virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # on Windows

# install dependencies
pip install -r requirements.txt
```

Tested with **Python 3.11–3.13**.  
Other recent 3.x versions will probably work, but 3.11+ is recommended.

If you don’t have a `requirements.txt`, you can install manually:

```bash
pip install streamlit pandas matplotlib seaborn wordcloud urlextract emoji textblob
python -m textblob.download_corpora
```

## Running the App

From the project root:

```bash
streamlit run app.py
```

Then open the URL shown in the terminal (usually `http://localhost:8501`), upload a WhatsApp chat export, choose filters and a user, and click **“Show Analysis”**.

## Notes

- **Timestamp format**: the app expects 12‑hour timestamps with AM/PM like: `19/08/25, 12:19 pm -`.
- `stop_hinglish.txt` should stay in the project root so wordcloud / common‑words keep working.
