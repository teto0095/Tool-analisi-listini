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

# --- GESTIONE LINGUE (DIZIONARIO) ---
lingua_scelta = st.sidebar.radio("🌐 Language / Lingua", ["Italiano", "English"], horizontal=True)
st.sidebar.divider()

testi = {
    "Italiano": {
        "param_title": "Parametri",
        "direction": "🔄 Direzione:",
        "weight": "⚖️ Peso (Kg):",
        "zone": "📍 Zona:",
        "discount_title": "### 🏷️ Sconti Commerciali",
        "discount_caption": "*(Inserisci un numero intero, es: 10)*",
        "sconto_a": "Sconto Player A (%)",
        "sconto_b": "Sconto Player B (%)",
        "sconto_c": "Sconto Player C (%)",
        "fuel_title": "### ⛽ Fuel Surcharge",
        "fuel_caption": "*(Usa il punto per i decimali, es: 2.25 — step 0.25)*",
        "fuel_a": "Fuel Player A (%)",
        "fuel_b": "Fuel Player B (%)",
        "fuel_c": "Fuel Player C (%)",
        "comparison_msg": "Confronto tariffe **{tipo}** per spedizioni di **{kg} Kg** verso **{zona}**.",
        "winner_msg": "🏆 Il partner più competitivo per questa tratta è **{vincitore}** con un prezzo totale di **€ {prezzo:.2f}**",
        "nolo": "Nolo:",
        "sconto": "Sconto:",
        "chart_title": "📈 Analisi Visiva Costi Totali",
        "chart_yaxis": "Prezzo Totale Inclusivo (€)",
        "matrix_title": "🗃️ Matrici dei Listini Base",
        "matrix_select": "Seleziona il listino da visualizzare:",
        "matrix_all": "Mostra Tutti",
        "matrix_only_a": "Solo Player A",
        "matrix_only_b": "Solo Player B",
        "matrix_only_c": "Solo Player C",
        "err_int": "⚠️ {label}: inserisci un numero intero valido. Uso {default}.",
        "err_float": "⚠️ {label}: inserisci un decimale valido (es. 2.25). Uso {default:.2f}.",
        "err_range_int": "⚠️ {label}: valore fuori range ({min_v}-{max_v}). Uso {default}.",
        "err_range_float": "⚠️ {label}: valore fuori range ({min_v}-{max_v}). Uso {default:.2f}.",
        "rounded": "↳ {label} arrotondato a {val:.2f}"
    },
    "English": {
        "param_title": "Parameters",
        "direction": "🔄 Direction:",
        "weight": "⚖️ Weight (Kg):",
        "zone": "📍 Zone:",
        "discount_title": "### 🏷️ Commercial Discounts",
        "discount_caption": "*(Enter an integer, e.g., 10)*",
        "sconto_a": "Discount Player A (%)",
        "sconto_b": "Discount Player B (%)",
        "sconto_c": "Discount Player C (%)",
        "fuel_title": "### ⛽ Fuel Surcharge",
        "fuel_caption": "*(Use a dot for decimals, e.g., 2.25 — 0.25 steps)*",
        "fuel_a": "Fuel Player A (%)",
        "fuel_b": "Fuel Player B (%)",
        "fuel_c": "Fuel Player C (%)",
        "comparison_msg": "Comparing **{tipo}** rates for **{kg} Kg** shipments to **{zona}**.",
        "winner_msg": "🏆 The most competitive partner for this route is **{vincitore}** with a total price of **€ {prezzo:.2f}**",
        "nolo": "Freight:",
        "sconto": "Discount:",
        "chart_title": "📈 Visual Analysis of Total Costs",
        "chart_yaxis": "Total Inclusive Price (€)",
        "matrix_title": "🗃️ Base Price Matrices",
        "matrix_select": "Select the price list to display:",
        "matrix_all": "Show All",
        "matrix_only_a": "Only Player A",
        "matrix_only_b": "Only Player B",
        "matrix_only_c": "Only Player C",
        "err_int": "⚠️ {label}: enter a valid integer. Using {default}.",
        "err_float": "⚠️ {label}: enter a valid decimal (e.g., 2.25). Using {default:.2f}.",
        "err_range_int": "⚠️ {label}: value out of range ({min_v}-{max_v}). Using {default}.",
        "err_range_float": "⚠️ {label}: value out of range ({min_v}-{max_v}). Using {default:.2f}.",
        "rounded": "↳ {label} rounded to {val:.2f}"
    }
}
t = testi[lingua_scelta]

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
    raw = st.sidebar.text_input(label, value=str(default), key=key)
    raw = raw.strip().replace(",", ".")
    try:
        val = int(float(raw))
        if val < min_v or val > max_v:
            st.sidebar.error(t["err_range_int"].format(label=label, min_v=min_v, max_v=max_v, default=default))
            return default
        return val
    except ValueError:
        st.sidebar.error(t["err_int"].format(label=label, default=default))
        return default

def text_input_decimale_step(label, key, default, step=0.25, min_v=0.0, max_v=100.0):
    raw = st.sidebar.text_input(label, value=f"{default:.2f}", key=key)
    raw = raw.strip().replace(",", ".")
    try:
        val = float(raw)
        if val < min_v or val > max_v:
            st.sidebar.error(t["err_range_float"].format(label=label, min_v=min_v, max_v=max_v, default=default))
            return default
        val_arrotondato = round(val / step) * step
        if abs(val_arrotondato - val) > 1e-9:
            st.sidebar.caption(t["rounded"].format(label=label, val=val_arrotondato))
        return val_arrotondato
    except ValueError:
        st.sidebar.error(t["err_float"].format(label=label, default=default))
        return default

# --- 2. SIDEBAR E CASELLE DI TESTO ---
st.sidebar.title(t["param_title"])
input_tipo = st.sidebar.radio(t["direction"], ["EXPORT", "IMPORT"])
st.sidebar.divider()

input_kg = st.sidebar.number_input(t["weight"], min_value=0.1, value=5.0, step=0.5)
input_zona = st.sidebar.selectbox(t["zone"], zone)
st.sidebar.divider()

# SCONTI INTERI
st.sidebar.markdown(t["discount_title"])
st.sidebar.caption(t["discount_caption"])
sconto_a = text_input_intero(t["sconto_a"], "sconto_a", default=10)
sconto_b = text_input_intero(t["sconto_b"], "sconto_b", default=15)
sconto_c = text_input_intero(t["sconto_c"], "sconto_c", default=5)

st.sidebar.divider()

# FUEL DECIMALI
st.sidebar.markdown(t["fuel_title"])
st.sidebar.caption(t["fuel_caption"])
fuel_a = text_input_decimale_step(t["fuel_a"], "fuel_a", default=12.00, step=0.25)
fuel_b = text_input_decimale_step(t["fuel_b"], "fuel_b", default=10.50, step=0.25)
fuel_c = text_input_decimale_step(t["fuel_c"], "fuel_c", default=15.75, step=0.25)

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
st.markdown(t["comparison_msg"].format(tipo=input_tipo, kg=input_kg, zona=input_zona))

st.success(t["winner_msg"].format(vincitore=vincitore, prezzo=prezzo_minimo))
st.write("")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="card" style="border-top: 5px solid #FF0000;">
        <div class="player-name">Player A</div>
        <div class="price-big" style="color: {get_text_color(prezzo_finale_a)};">€ {prezzo_finale_a:.2f}</div>
        <div class="price-detail">{t["nolo"]} <b>€ {prezzo_nolo_a:.2f}</b><br>{t["sconto"]} {sconto_a}% | Fuel: {fuel_a:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card" style="border-top: 5px solid #800080;">
        <div class="player-name">Player B</div>
        <div class="price-big" style="color: {get_text_color(prezzo_finale_b)};">€ {prezzo_finale_b:.2f}</div>
        <div class="price-detail">{t["nolo"]} <b>€ {prezzo_nolo_b:.2f}</b><br>{t["sconto"]} {sconto_b}% | Fuel: {fuel_b:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card" style="border-top: 5px solid #FFC107;">
        <div class="player-name">Player C</div>
        <div class="price-big" style="color: {get_text_color(prezzo_finale_c)};">€ {prezzo_finale_c:.2f}</div>
        <div class="price-detail">{t["nolo"]} <b>€ {prezzo_nolo_c:.2f}</b><br>{t["sconto"]} {sconto_c}% | Fuel: {fuel_c:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- GRAFICO PLOTLY ---
st.subheader(t["chart_title"])

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
    yaxis_title=t["chart_yaxis"],
    xaxis_title="",
    margin=dict(l=0, r=0, t=20, b=0),
    height=450,
    plot_bgcolor="rgba(0,0,0,0)"
)
fig.update_yaxes(showgrid=True, gridcolor="#e0e0e0")

st.plotly_chart(fig, use_container_width=True)

# --- 5. MENU' A TENDINA MATRICI LISTINI ---
st.divider()
st.subheader(t["matrix_title"])

scelta_listino = st.selectbox(
    t["matrix_select"],
    [t["matrix_all"], t["matrix_only_a"], t["matrix_only_b"], t["matrix_only_c"]]
)

st.write("")

if scelta_listino == t["matrix_all"]:
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
elif scelta_listino == t["matrix_only_a"]:
    st.markdown(f"**Player A ({input_tipo})**")
    st.dataframe(listino_a, use_container_width=True)
elif scelta_listino == t["matrix_only_b"]:
    st.markdown(f"**Player B ({input_tipo})**")
    st.dataframe(listino_b, use_container_width=True)
elif scelta_listino == t["matrix_only_c"]:
    st.markdown(f"**Player C ({input_tipo})**")
    st.dataframe(listino_c, use_container_width=True)
