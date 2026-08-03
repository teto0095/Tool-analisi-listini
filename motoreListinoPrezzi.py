import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- IMPOSTAZIONI PAGINA ---
st.set_page_config(page_title="Pricing Dashboard", page_icon="📊", layout="wide")

# --- CSS PERSONALIZZATO ---
st.markdown("""
<style>
    .card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        text-align: center;
    }
    .player-name { font-size: 1.2rem; font-weight: 600; color: #333; margin-bottom: 5px; }
    .price-big { font-size: 2.5rem; font-weight: 800; margin-bottom: 5px; }
    .price-detail { font-size: 0.9rem; color: #666; line-height: 1.4; }
</style>
""", unsafe_allow_html=True)

# --- 1. DATI FITTIZI (MATRICI) ---
zone = ["Zona 1 (Nord)", "Zona 2 (Centro)", "Zona 3 (Sud e Isole)"]
fasce_peso = ["0-5 kg", "5.1-15 kg", "15.1-30 kg", "Oltre 30 kg"]

# EXPORT
listino_a_export = pd.DataFrame({"Zona 1 (Nord)": [8.0, 14.0, 22.0, 35.0], "Zona 2 (Centro)": [10.0, 16.0, 25.0, 40.0], "Zona 3 (Sud e Isole)": [13.0, 20.0, 30.0, 48.0]}, index=fasce_peso)
listino_b_export = pd.DataFrame({"Zona 1 (Nord)": [9.0, 13.0, 20.0, 38.0], "Zona 2 (Centro)": [11.0, 15.0, 23.0, 42.0], "Zona 3 (Sud e Isole)": [14.0, 18.0, 28.0, 50.0]}, index=fasce_peso)
listino_c_export = pd.DataFrame({"Zona 1 (Nord)": [7.5, 15.0, 24.0, 33.0], "Zona 2 (Centro)": [9.5, 17.0, 26.0, 38.0], "Zona 3 (Sud e Isole)": [12.5, 21.0, 32.0, 45.0]}, index=fasce_peso)

# IMPORT
listino_a_import = pd.DataFrame({"Zona 1 (Nord)": [10.0, 16.0, 25.0, 40.0], "Zona 2 (Centro)": [12.0, 18.0, 28.0, 45.0], "Zona 3 (Sud e Isole)": [15.0, 23.0, 35.0, 55.0]}, index=fasce_peso)
listino_b_import = pd.DataFrame({"Zona 1 (Nord)": [11.0, 15.0, 23.0, 42.0], "Zona 2 (Centro)": [13.0, 17.0, 26.0, 48.0], "Zona 3 (Sud e Isole)": [16.0, 21.0, 32.0, 58.0]}, index=fasce_peso)
listino_c_import = pd.DataFrame({"Zona 1 (Nord)": [9.5, 17.0, 26.0, 38.0], "Zona 2 (Centro)": [11.5, 19.0, 29.0, 43.0], "Zona 3 (Sud e Isole)": [14.5, 24.0, 37.0, 52.0]}, index=fasce_peso)

def get_fascia_peso(kg):
    if kg <= 5.0: return "0-5 kg"
    elif kg <= 15.0: return "5.1-15 kg"
    elif kg <= 30.0: return "15.1-30 kg"
    else: return "Oltre 30 kg"

# --- HELPER: CASELLE DI TESTO VALIDATE ---
def text_input_intero(label, key, default, min_v=0, max_v=100):
    """Casella di testo che accetta solo numeri interi (es. sconti %)."""
    raw = st.sidebar.text_input(label, value=str(default), key=key)
    raw = raw.strip().replace(",", ".")
    try:
        val = int(float(raw))  # tollera anche "10.0" digitato per errore
        if val < min_v or val > max_v:
            st.sidebar.error(f"⚠️ {label}: valore fuori range ({min_v}-{max_v}). Uso {default}.")
            return default
        return val
    except ValueError:
        st.sidebar.error(f"⚠️ {label}: inserisci un numero intero valido. Uso {default}.")
        return default

def text_input_decimale_step(label, key, default, step=0.25, min_v=0.0, max_v=100.0):
    """Casella di testo che accetta solo numeri decimali arrotondati a multipli di 'step'."""
    raw = st.sidebar.text_input(label, value=f"{default:.2f}", key=key)
    raw = raw.strip().replace(",", ".")
    try:
        val = float(raw)
        if val < min_v or val > max_v:
            st.sidebar.error(f"⚠️ {label}: valore fuori range ({min_v}-{max_v}). Uso {default:.2f}.")
            return default
        # Arrotonda al multiplo di 'step' più vicino (es. 0.25)
        val_arrotondato = round(val / step) * step
        if abs(val_arrotondato - val) > 1e-9:
            st.sidebar.caption(f"↳ {label} arrotondato a {val_arrotondato:.2f}")
        return val_arrotondato
    except ValueError:
        st.sidebar.error(f"⚠️ {label}: inserisci un numero decimale valido (es. 2.25). Uso {default:.2f}.")
        return default

# --- 2. SIDEBAR E CASELLE DI TESTO ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2972/2972185.png", width=60)
st.sidebar.title("Parametri")
input_tipo = st.sidebar.radio("🔄 Direzione:", ["EXPORT", "IMPORT"])
st.sidebar.divider()

input_kg = st.sidebar.number_input("⚖️ Peso (Kg):", min_value=0.1, value=5.0, step=0.5)
input_zona = st.sidebar.selectbox("📍 Zona:", zone)
st.sidebar.divider()

# SCONTI INTERI
st.sidebar.markdown("### 🏷️ Sconti Commerciali")
st.sidebar.caption("*(Inserisci un numero intero, es: 10)*")
sconto_a = text_input_intero("Sconto Player A (%)", "sconto_a", default=10)
sconto_b = text_input_intero("Sconto Player B (%)", "sconto_b", default=15)
sconto_c = text_input_intero("Sconto Player C (%)", "sconto_c", default=5)

st.sidebar.divider()

# FUEL DECIMALI
st.sidebar.markdown("### ⛽ Fuel Surcharge")
st.sidebar.caption("*(Usa il punto per i decimali, es: 2.25 — valori arrotondati a step di 0.25)*")
fuel_a = text_input_decimale_step("Fuel Player A (%)", "fuel_a", default=12.00, step=0.25)
fuel_b = text_input_decimale_step("Fuel Player B (%)", "fuel_b", default=10.50, step=0.25)
fuel_c = text_input_decimale_step("Fuel Player C (%)", "fuel_c", default=15.75, step=0.25)

# --- 3. MOTORE DI CALCOLO ---
if input_tipo == "EXPORT":
    listino_a, listino_b, listino_c = listino_a_export, listino_b_export, listino_c_export
else:
    listino_a, listino_b, listino_c = listino_a_import, listino_b_import, listino_c_import

fascia_selezionata = get_fascia_peso(input_kg)

prezzo_base_a = listino_a.loc[fascia_selezionata, input_zona]
prezzo_base_b = listino_b.loc[fascia_selezionata, input_zona]
prezzo_base_c = listino_c.loc[fascia_selezionata, input_zona]

# Calcolo Nolo
prezzo_nolo_a = prezzo_base_a * (1 - (sconto_a / 100))
prezzo_nolo_b = prezzo_base_b * (1 - (sconto_b / 100))
prezzo_nolo_c = prezzo_base_c * (1 - (sconto_c / 100))

# Calcolo Finale (Nolo + Fuel)
prezzo_finale_a = prezzo_nolo_a * (1 + (fuel_a / 100))
prezzo_finale_b = prezzo_nolo_b * (1 + (fuel_b / 100))
prezzo_finale_c = prezzo_nolo_c * (1 + (fuel_c / 100))

# --- DETERMINAZIONE VINCITORE ---
dizionario_prezzi = {"Player A": prezzo_finale_a, "Player B": prezzo_finale_b, "Player C": prezzo_finale_c}
vincitore = min(dizionario_prezzi, key=dizionario_prezzi.get)
prezzo_minimo = dizionario_prezzi[vincitore]
prezzo_massimo = max(dizionario_prezzi.values())

def get_text_color(prezzo):
    if prezzo == prezzo_minimo: return "#198754"
    elif prezzo == prezzo_massimo: return "#dc3545"
    else: return "#6c757d"

# --- 4. DASHBOARD ---
st.title("📊 Pricing Intelligence Dashboard")
st.markdown(f"Confronto tariffe **{input_tipo}** per spedizioni di **{input_kg} Kg** verso **{input_zona}**.")

st.success(f"🏆 Il partner più competitivo per questa tratta è **{vincitore}** con un prezzo totale di **€ {prezzo_minimo:.2f}**")
st.write("")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="card" style="border-top: 5px solid #FF0000;">
        <div class="player-name">Player A</div>
        <div class="price-big" style="color: {get_text_color(prezzo_finale_a)};">€ {prezzo_finale_a:.2f}</div>
        <div class="price-detail">Nolo: <b>€ {prezzo_nolo_a:.2f}</b><br>Sconto: {sconto_a}% | Fuel: {fuel_a:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card" style="border-top: 5px solid #800080;">
        <div class="player-name">Player B</div>
        <div class="price-big" style="color: {get_text_color(prezzo_finale_b)};">€ {prezzo_finale_b:.2f}</div>
        <div class="price-detail">Nolo: <b>€ {prezzo_nolo_b:.2f}</b><br>Sconto: {sconto_b}% | Fuel: {fuel_b:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card" style="border-top: 5px solid #FFC107;">
        <div class="player-name">Player C</div>
        <div class="price-big" style="color: {get_text_color(prezzo_finale_c)};">€ {prezzo_finale_c:.2f}</div>
        <div class="price-detail">Nolo: <b>€ {prezzo_nolo_c:.2f}</b><br>Sconto: {sconto_c}% | Fuel: {fuel_c:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- GRAFICO PLOTLY ---
st.subheader("📈 Analisi Visiva Costi Totali")

df_grafico = pd.DataFrame({
    "Player": ["Player A", "Player B", "Player C"],
    "Prezzo Totale": [prezzo_finale_a, prezzo_finale_b, prezzo_finale_c]
}).sort_values(by="Prezzo Totale", ascending=True).set_index("Player")

mappa_colori = {"Player A": "#FF0000", "Player B": "#800080", "Player C": "#FFC107"}
colori_ordinati = [mappa_colori[p] for p in df_grafico.index]

fig = go.Figure(data=[go.Bar(
    x=df_grafico.index,
    y=df_grafico["Prezzo Totale"],
    text=[f"€ {val:.2f}" for val in df_grafico["Prezzo Totale"]],
    textposition='outside',
    textfont=dict(size=14, color="black"),
    marker=dict(color=colori_ordinati, line=dict(color='white', width=1))
)])

fig.update_layout(
    template="plotly_white",
    yaxis_title="Prezzo Totale Inclusivo (€)",
    xaxis_title="",
    margin=dict(l=0, r=0, t=20, b=0),
    height=450,
    plot_bgcolor="rgba(0,0,0,0)"
)
fig.update_yaxes(showgrid=True, gridcolor="#e0e0e0")

st.plotly_chart(fig, use_container_width=True)

# --- 5. MENU A TENDINA MATRICI LISTINI ---
st.divider()
st.subheader("🗃️ Matrici dei Listini Base")

# Seleziona quale listino mostrare dal menu a tendina
scelta_listino = st.selectbox(
    "Seleziona il listino da visualizzare:",
    ["Mostra Tutti", "Solo Player A", "Solo Player B", "Solo Player C"]
)

st.write("") # Spazio

if scelta_listino == "Mostra Tutti":
    ca, cb, cc = st.columns(3)
    with ca:
        st.markdown(f"**Player A ({input_tipo})**")
        st.dataframe(listino_a, use_container_width=True)
    with cb:
        st.markdown(f"**Player B ({input_tipo})**")
        st.dataframe(listino_b, use_container_width=True)
    with cc:
        st.markdown(f"**Player C ({input_tipo})**")
        st.dataframe(listino_c, use_container_width=True)

elif scelta_listino == "Solo Player A":
    st.markdown(f"**Player A ({input_tipo})**")
    st.dataframe(listino_a, use_container_width=True)

elif scelta_listino == "Solo Player B":
    st.markdown(f"**Player B ({input_tipo})**")
    st.dataframe(listino_b, use_container_width=True)

elif scelta_listino == "Solo Player C":
    st.markdown(f"**Player C ({input_tipo})**")
    st.dataframe(listino_c, use_container_width=True)
