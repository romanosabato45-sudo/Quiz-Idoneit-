
# Quiz Idoneità — Economia, Diritto, Informatica

Web app Streamlit con:
- Generazione casuale di domande dai tuoi PDF
- Scelta del numero di domande (minimo 20)
- Correzione automatica, tabella errori, spiegazioni e fonti
- Download del report CSV

## Come eseguire in locale
1) Installa Python 3.10+
2) Apri un terminale nella cartella e installa le dipendenze:
   pip install -r requirements.txt
3) Avvia:
   streamlit run app.py

## Pubblicazione (per ottenere un link da condividere)
Opzione A — Streamlit Community Cloud (gratis):
1) Crea un repository su GitHub e carica i file (app.py, questions.json, requirements.txt).
2) Vai su https://streamlit.io/cloud , collega il tuo GitHub e seleziona il repo.
3) Come file principale indica `app.py`. La piattaforma genererà un URL pubblico.

Opzione B — Render/Heroku:
- Creare un servizio web Python e impostare `streamlit run app.py` come comando di avvio.

