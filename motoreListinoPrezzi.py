import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- IMPOSTAZIONI PAGINA ---
st.set_page_config(page_title="Pricing Dashboard", page_icon="📊", layout="wide")

# --- CSS PERSONALIZZATO (Per abbellire l'interfaccia) ---
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
    .price-detail { font-size: 0.9rem; color: #666; }
</style>
""", unsafe_allow_html=True)

# --- 1. DATI FITTIZI (MATRICI EXPORT/IMPORT) ---
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

# --- 2. SIDEBAR (Input Utente) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2972/2972185.png", width=60) # Piccola icona logistica
st.sidebar.title("Parametri")
input_tipo = st.sidebar.radio("🔄 Direzione:", ["EXPORT", "IMPORT"])
st.sidebar.divider()

input_kg = st.sidebar.number_input("⚖️ Peso (Kg):", min_value=0.1, value=5.0, step=0.5)
input_zona = st.sidebar.selectbox("📍 Zona:", zone)
st.sidebar.divider()

st.sidebar.markdown("### 🏷️ Sconti Commerciali")
sconto_a = st.sidebar.slider("Sconto Player A (%)", 0, 100, 10)
sconto_b = st.sidebar.slider("Sconto Player B (%)", 0, 100, 15)
sconto_c = st.sidebar.slider("Sconto Player C (%)", 0, 100, 5)

# --- 3. MOTORE DI CALCOLO ---
if input_tipo == "EXPORT":
    listino_a, listino_b, listino_c = listino_a_export, listino_b_export, listino_c_export
else:
    listino_a, listino_b, listino_c = listino_a_import, listino_b_import, listino_c_import

fascia_selezionata = get_fascia_peso(input_kg)

prezzo_base_a = listino_a.loc[fascia_selezionata, input_zona]
prezzo_base_b = listino_b.loc[fascia_selezionata, input_zona]
prezzo_base_c = listino_c.loc[fascia_selezionata, input_zona]

prezzo_finale_a = prezzo_base_a * (1 - (sconto_a / 100))
prezzo_finale_b = prezzo_base_b * (1 - (sconto_b / 100))
prezzo_finale_c = prezzo_base_c * (1 - (sconto_c / 100))

# --- DETERMINAZIONE COLORI E VINCITORE ---
dizionario_prezzi = {"Player A": prezzo_finale_a, "Player B": prezzo_finale_b, "Player C": prezzo_finale_c}
vincitore = min(dizionario_prezzi, key=dizionario_prezzi.get)
prezzo_minimo = dizionario_prezzi[vincitore]
prezzo_massimo = max(dizionario_prezzi.values())

def get_text_color(prezzo):
    if prezzo == prezzo_minimo: return "#198754"  # Verde Successo
    elif prezzo == prezzo_massimo: return "#dc3545"  # Rosso Pericolo
    else: return "#6c757d"  # Grigio Neutro

# --- 4. DASHBOARD (Area Principale) ---
st.title("📊 Pricing Intelligence Dashboard")
st.markdown(f"Confronto tariffe **{input_tipo}** per spedizioni di **{input_kg} Kg** verso **{input_zona}**.")

# Alert Vincitore
st.success(f"🏆 Il partner più competitivo per questa tratta è **{vincitore}** con un prezzo netto di **€ {prezzo_minimo:.2f}**")
st.write("") # Spazio

# --- CARDS HTML PERSONALIZZATE ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="card" style="border-top: 5px solid #FF0000;">
        <div class="player-name">Player A</div>
        <div class="price-big" style="color: {get_text_color(prezzo_finale_a)};">€ {prezzo_finale_a:.2f}</div>
        <div class="price-detail">Sconto: <b>{sconto_a}%</b> | Base: € {prezzo_base_a:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card" style="border-top: 5px solid #800080;">
        <div class="player-name">Player B</div>
        <div class="price-big" style="color: {get_text_color(prezzo_finale_b)};">€ {prezzo_finale_b:.2f}</div>
        <div class="price-detail">Sconto: <b>{sconto_b}%</b> | Base: € {prezzo_base_b:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card" style="border-top: 5px solid #FFC107;">
        <div class="player-name">Player C</div>
        <div class="price-big" style="color: {get_text_color(prezzo_finale_c)};">€ {prezzo_finale_c:.2f}</div>
        <div class="price-detail">Sconto: <b>{sconto_c}%</b> | Base: € {prezzo_base_c:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- GRAFICO PLOTLY PREMIUM ---
st.subheader("📈 Analisi Visiva Costi")

df_grafico = pd.DataFrame({
    "Player": ["Player A", "Player B", "Player C"],
    "Prezzo": [prezzo_finale_a, prezzo_finale_b, prezzo_finale_c]
}).sort_values(by="Prezzo", ascending=True).set_index("Player")

mappa_colori = {"Player A": "#FF0000", "Player B": "#800080", "Player C": "#FFC107"}
colori_ordinati = [mappa_colori[p] for p in df_grafico.index]

fig = go.Figure(data=[go.Bar(
    x=df_grafico.index,
    y=df_grafico["Prezzo"],
    text=[f"€ {val:.2f}" for val in df_grafico["Prezzo"]],
    textposition='outside', # Mette il testo sopra la barra
    textfont=dict(size=14, color="black"),
    marker=dict(color=colori_ordinati, line=dict(color='white', width=1))
)])

fig.update_layout(
    template="plotly_white", # Tema pulito e professionale
    yaxis_title="Prezzo Netto (€)",
    xaxis_title="",
    margin=dict(l=0, r=0, t=20, b=0),
    height=450,
    plot_bgcolor="rgba(0,0,0,0)" # Sfondo trasparente
)
fig.update_yaxes(showgrid=True, gridcolor="#e0e0e0") # Griglia leggera

st.plotly_chart(fig, use_container_width=True)

# --- SEZIONE DEBUG/DATI ---
st.write("")
with st.expander("🗃️ Visualizza le Matrici dei Listini Base"):
    ca, cb, cc = st.columns(3)
    with ca: st.markdown("**Player A**"); st.dataframe(listino_a, use_container_width=True)
    with cb: st.markdown("**Player B**"); st.dataframe(listino_b, use_container_width=True)
    with cc: st.markdown("**Player C**"); st.dataframe(listino_c, use_container_width=True)