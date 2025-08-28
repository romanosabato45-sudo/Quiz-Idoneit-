
import streamlit as st
import json, random, datetime
from io import StringIO
import pandas as pd

st.set_page_config(page_title="Quiz Idoneità — Economia, Diritto, Informatica",
                   layout="wide")

@st.cache_data
def load_questions():
    with open("questions.json","r",encoding="utf-8") as f:
        data = json.load(f)
    return data

QUESTIONS = load_questions()
ALL_TOPICS = sorted({q["topic"] for q in QUESTIONS})

def sample_questions(topics, n, seed=None):
    pool = [q.copy() for q in QUESTIONS if q["topic"] in topics]
    if n < 20:
        n = 20
    n = min(n, len(pool))
    rng = random.Random(seed)
    sampled = rng.sample(pool, n)
    for q in sampled:
        if q["type"] == "mcq":
            choices = q["choices"][:]
            rng.shuffle(choices)
            q["shuffled"] = choices
    return sampled

st.title("📘 Quiz Idoneità — Economia, Diritto, Informatica")
st.caption("Domande generate dai tuoi documenti, verificate su fonti ufficiali. Ogni test è casuale.")

with st.sidebar:
    st.header("Impostazioni test")
    topics = st.multiselect("Scegli gli argomenti", ALL_TOPICS, default=ALL_TOPICS)
    n_q = st.number_input("Numero di domande (min 20)", min_value=20, max_value=len(QUESTIONS), value=max(20, min(25, len(QUESTIONS))))
    seed = st.number_input("Semina casuale (opzionale)", min_value=0, value=0, step=1)
    new_test = st.button("🔄 Genera nuovo test")

if "questions" not in st.session_state or new_test:
    st.session_state.questions = sample_questions(topics, int(n_q), int(seed) if seed else None)
    st.session_state.answers = {}
    st.session_state.submitted = False
    st.session_state.started_at = datetime.datetime.now().isoformat(timespec="seconds")

qs = st.session_state.questions
answers = st.session_state.answers

st.subheader("Domande")
for q in qs:
    st.markdown(f"**{q['topic']}** — {q['question']}")
    if q["type"] == "mcq":
        sel = st.radio("",
                       options=q["shuffled"],
                       key=f"ans_{q['id']}",
                       label_visibility="collapsed",
                       index=None)
        if sel is not None:
            answers[q["id"]] = sel
    else:
        sel = st.radio("",
                       options=["Vero","Falso"],
                       key=f"ans_{q['id']}",
                       label_visibility="collapsed",
                       index=None)
        if sel is not None:
            answers[q["id"]] = True if sel=="Vero" else False
    st.divider()

if st.button("✅ Invia risposte"):
    st.session_state.submitted = True

if st.session_state.submitted:
    # Evaluate
    rows = []
    correct = 0
    for q in qs:
        ua = answers.get(q["id"], None)
        if q["type"] == "mcq":
            ok = (ua == q["answer"])
            corr = q["answer"]
            ua_show = ua
        else:
            ok = (ua == q["answer"])
            corr = "Vero" if q["answer"] else "Falso"
            ua_show = "Vero" if ua is True else "Falso" if ua is not None else None
        rows.append({
            "ID": q["id"],
            "Argomento": q["topic"],
            "Domanda": q["question"],
            "Tua risposta": ua_show,
            "Risposta corretta": corr,
            "Esatto?": "✅" if ok else "❌",
            "Spiegazione": q.get("explanation",""),
            "Fonte": q.get("source",""),
            "Fonte URL": q.get("source_url",""),
        })
        if ok: correct += 1

    df = pd.DataFrame(rows)
    score = round(100*correct/len(qs)) if qs else 0

    st.success(f"Punteggio: **{correct}/{len(qs)}**  —  **{score}%**")
    st.progress(score/100)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ Risposte corrette")
        st.dataframe(df[df["Esatto?"]=="✅"][["ID","Argomento","Domanda","Tua risposta"]], use_container_width=True)
    with col2:
        st.subheader("❌ Errori da rivedere")
        st.dataframe(df[df["Esatto?"]=="❌"][["ID","Argomento","Domanda","Tua risposta","Risposta corretta"]], use_container_width=True)

    st.subheader("📚 Spiegazioni e Fonti")
    st.dataframe(df[["ID","Domanda","Spiegazione","Fonte","Fonte URL"]], use_container_width=True)

    # Downloads
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Scarica report CSV", data=csv, file_name=f"report_quiz_{st.session_state.started_at}.csv", mime="text/csv")

    # Restart
    st.info("Vuoi riprovare con nuove domande? Usa la barra laterale e premi **Genera nuovo test**.")

st.caption("© Quiz Idoneità — basato sui tuoi materiali.")

