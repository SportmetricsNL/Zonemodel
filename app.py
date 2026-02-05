import streamlit as st
import numpy as np
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Zone Explorer", layout="wide", page_icon="🚴")

# Custom CSS om de 'premium' look van de React app te benaderen
st.markdown("""
<style>
    /* Algemene achtergrond en fonts */
    .stApp {
        background-color: #f8fafc;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Titels */
    h1 { color: #0f172a; font-weight: 900 !important; letter-spacing: -1px; }
    h2 { color: #334155; font-weight: 800 !important; }
    h3 { color: #475569; font-weight: 700 !important; }
    
    /* Cards styling */
    .custom-card {
        background-color: white;
        padding: 2rem;
        border-radius: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    
    /* Sidebar card style */
    .theory-card {
        background-color: #0f172a;
        color: white;
        padding: 2rem;
        border-radius: 1.5rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    /* Zone buttons simulatie (Streamlit buttons zijn lastig te stylen, we doen het via columns) */
    div.stButton > button {
        border-radius: 12px;
        font-weight: bold;
        border: 2px solid #e2e8f0;
        width: 100%;
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        border-color: #94a3b8;
        transform: translateY(-2px);
    }

    /* Highlight box voor Takeaway */
    .takeaway-box {
        background-color: #fff7ed;
        border-left: 4px solid #f97316;
        padding: 1rem;
        border-radius: 0.5rem;
        color: #9a3412;
        font-style: italic;
        font-weight: 600;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA & INHOUD (Ventilatoire Focus)
# -----------------------------------------------------------------------------

# Fysiologische ankers (x-as waarden 0-100)
VT1_X = 48
VT2_X = 78

# 3-Zone Model Data
ZONES_3 = {
    "Zone 1": {
        "title": "ZONE 1 (LOW)",
        "subtitle": "Onder VT1 - Stabiele Ademhaling",
        "theory": "De basis van elke training. Je ademhaling blijft laag en stabiel. Je gebruikt hoofdzakelijk vetten en de interne belasting is minimaal.",
        "bullets": [
            "Easy écht easy houden",
            "Basisdomein voor vetverbranding",
            "Minimale metabole stress"
        ],
        "prikkels": ["Capillarisatie", "Mitochondriale efficiëntie", "Basisvolume"],
        "doelen": ["Vetverbranding optimaliseren", "Herstel bevorderen", "Basisconditie"],
        "voorbeelden": ["60-90 min herstelrit", "Warming-up"],
        "takeaway": "Zones = doseren op fysiologie, niet op gevoel alleen.",
        "color": "rgba(16, 185, 129, 0.2)", # Emerald
        "stroke": "#059669"
    },
    "Zone 2": {
        "title": "ZONE 2 (TEMPO)",
        "subtitle": "Tussen VT1 & VT2 - Verhoogde Ventilatie",
        "theory": "Het overgangsgebied. Ademarbeid stijgt merkbaar. Je kunt nog praten, maar in kortere zinnen. Herstelkosten lopen op.",
        "bullets": [
            "Comfortabel zwaar tempo",
            "Dieselvermogen opbouwen",
            "Mentale tolerantie voor inspanning"
        ],
        "prikkels": ["Tempo-uithoudingsvermogen", "Race-gevoel", "Koolhydraat-mix efficiëntie"],
        "doelen": ["Gran fondo tempo", "Lange solo's", "Specifieke race pace"],
        "voorbeelden": ["2x20 min tempo", "Lange klim steady"],
        "takeaway": "VT1 & VT2 zijn je fysiologische ankers voor zones.",
        "color": "rgba(249, 115, 22, 0.2)", # Orange
        "stroke": "#ea580c"
    },
    "Zone 3": {
        "title": "ZONE 3 (HIGH)",
        "subtitle": "Boven VT2 - Maximale Ademarbeid",
        "theory": "Boven de tweede ventilatoire drempel. Ademhaling gaat maximaal. 'Steady' rijden wordt onmogelijk; dit is werk met een hoge herstelvraag.",
        "bullets": [
            "Hard werk hard genoeg maken",
            "Werken tegen het aerobe plafond",
            "Maximale ventilatoire druk"
        ],
        "prikkels": ["VO2max prikkel", "Lactaat tolerantie", "Top-end vermogen"],
        "doelen": ["Klimvermogen (3-8 min)", "Gaten dichten / attacks", "FTP verhogen"],
        "voorbeelden": ["4x4 Norway intervallen", "30/30's"],
        "takeaway": "Meting via ademvariabelen (VE, Rf) is de gouden standaard.",
        "color": "rgba(239, 68, 68, 0.2)", # Red
        "stroke": "#dc2626"
    }
}

# 5-Zone Model Data
ZONES_5 = {
    "Zone 1": {
        "title": "ZONE 1",
        "subtitle": "Herstel (Ver onder VT1)",
        "theory": "Heel rustig trappen. Praattempo: moeiteloos praten. Ademhaling blijft laag en stabiel.",
        "bullets": ["Easy écht easy houden", "Ondersteunend, niet het hele plan"],
        "prikkels": ["Herstelcapaciteit (doorbloeding)", "Techniek/cadans zonder stress", "Basisvolume"],
        "doelen": ["Sneller herstellen", "Volume zonder vermoeidheid", "Consistentie"],
        "voorbeelden": ["30-60 min herstelrit", "Spin na intervaldag"],
        "takeaway": "Z1 is ondersteunend voor de rest van je plan.",
        "color": "rgba(16, 185, 129, 0.2)", # Emerald
        "stroke": "#059669"
    },
    "Zone 2": {
        "title": "ZONE 2",
        "subtitle": "Aerobe Basis (Kalibreren met VT1)",
        "theory": "Rustig tot steady. Je voelt dat je 'werkt'. Zit onder of rond VT1: hoogste intensiteit die je lang kunt stapelen.",
        "bullets": ["Hoogste aerobe efficiëntie", "Zelfde watt = minder ademdruk over tijd"],
        "prikkels": ["Aerobe capaciteit", "Aerobe efficiëntie", "Vet+koolhydraatmix"],
        "doelen": ["Uithoudingsvermogen", "Basis voor intensief werk", "Betere pacing"],
        "voorbeelden": ["90-240 min duurrit", "2-3 uur basis"],
        "takeaway": "VT1 is het anker waarmee je Z2 goed kalibreert.",
        "color": "rgba(20, 184, 166, 0.2)", # Teal
        "stroke": "#0d9488"
    },
    "Zone 3": {
        "title": "ZONE 3",
        "subtitle": "Tempo (Comfortabel Zwaar)",
        "theory": "Stevig. Korte zinnen lukken nét. Je krijgt sneller 'drift' (zelfde watt = hogere ademdruk/HR).",
        "bullets": ["Valkuil: te vaak 'grijs' rijden", "Dieselvermogen trainen"],
        "prikkels": ["Tempo-uithoudingsvermogen", "Race-gevoel", "Mentale tolerantie"],
        "doelen": ["Gran fondo / lange solo's", "Specifieke race pace"],
        "voorbeelden": ["3x15 min tempo", "Lange klim steady"],
        "takeaway": "Voorkom dat Z3 je standaardrit wordt.",
        "color": "rgba(245, 158, 11, 0.2)", # Amber
        "stroke": "#d97706"
    },
    "Zone 4": {
        "title": "ZONE 4",
        "subtitle": "Threshold (Rond VT2)",
        "theory": "Hard, nauwelijks praten. Ademdruk is hoog, tempo 'managen'. Duidelijke herstelvraag.",
        "bullets": ["Drempelvermogen verhogen", "Tolerantie voor hoge ventilatie"],
        "prikkels": ["Drempelvermogen", "Pacingvaardigheid", "Ademrespons training"],
        "doelen": ["Sneller op 20-60 min inspanningen", "Tijdrit / breakaway"],
        "voorbeelden": ["3x10 min threshold", "Over/unders"],
        "takeaway": "Wattage + ademrespons is hier betrouwbaarder dan HR.",
        "color": "rgba(249, 115, 22, 0.2)", # Orange
        "stroke": "#ea580c"
    },
    "Zone 5": {
        "title": "ZONE 5",
        "subtitle": "VO2 Max (Boven VT2)",
        "theory": "Zeer hard. Praten onmogelijk. Ventilatie gaat maximaal. Tijd doorbrengen tegen aerobe plafond.",
        "bullets": ["Kort & scherp", "Vraagt veel herstel"],
        "prikkels": ["VO2max-prikkel", "Top-end verbetering", "Herstel tussen pieken"],
        "doelen": ["Klimvermogen verbeteren", "Attacks / gaten dichten"],
        "voorbeelden": ["4x4 Norway", "5x3 min intervallen"],
        "takeaway": "Werkt best met veel Z1-Z2 eromheen.",
        "color": "rgba(239, 68, 68, 0.2)", # Red
        "stroke": "#dc2626"
    }
}

# -----------------------------------------------------------------------------
# 3. INTERFACE LOGICA
# -----------------------------------------------------------------------------

# Header
st.markdown("<h1 style='text-align: center;'>Master je <span style='color: #dc2626; font-style: italic;'>Intensiteit.</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 1.1rem;'>Focus op ventilatoire ankers VT1 & VT2.</p>", unsafe_allow_html=True)

# Model Selectie
col_m1, col_m2, col_m3 = st.columns([1,2,1])
with col_m2:
    model_choice = st.radio("Kies je model:", ["5-Zone Model", "3-Zone Model"], horizontal=True, label_visibility="collapsed")

# Bepaal actieve dataset
active_zones = ZONES_3 if model_choice == "3-Zone Model" else ZONES_5

# Layout: Links Grafiek, Rechts Info
col_graph, col_sidebar = st.columns([2, 1])

# --- GRAFIEK (Plotly) ---
with col_graph:
    with st.container():
        st.markdown(f"### 🌬️ Ventilatoire Respons ({model_choice})")
        
        # Genereer curve data (Exponentiële stijging voor ventilatie)
        x = np.linspace(0, 100, 200)
        y = 15 + 0.001 * np.power(x, 2.5) # Simuleert VE curve

        fig = go.Figure()

        # Zones inkleuren
        if model_choice == "3-Zone Model":
            # Zone 1 (0 tot VT1)
            fig.add_trace(go.Scatter(x=x[x<=VT1_X], y=y[x<=VT1_X], fill='tozeroy', mode='none', fillcolor='rgba(16, 185, 129, 0.2)', name='ZONE 1'))
            # Zone 2 (VT1 tot VT2)
            mask_z2 = (x >= VT1_X) & (x <= VT2_X)
            fig.add_trace(go.Scatter(x=x[mask_z2], y=y[mask_z2], fill='tozeroy', mode='none', fillcolor='rgba(249, 115, 22, 0.2)', name='ZONE 2'))
            # Zone 3 (VT2 tot 100)
            fig.add_trace(go.Scatter(x=x[x>=VT2_X], y=y[x>=VT2_X], fill='tozeroy', mode='none', fillcolor='rgba(239, 68, 68, 0.2)', name='ZONE 3'))
        else:
            # 5 Zones (geschatte verdeling rondom VT1/VT2)
            # Z1 + Z2 eindigen bij VT1. Z3 + Z4 eindigen bij VT2.
            # Z1
            fig.add_trace(go.Scatter(x=x[x<=30], y=y[x<=30], fill='tozeroy', mode='none', fillcolor='rgba(16, 185, 129, 0.2)', name='Z1'))
            # Z2
            mask_z2 = (x >= 30) & (x <= VT1_X)
            fig.add_trace(go.Scatter(x=x[mask_z2], y=y[mask_z2], fill='tozeroy', mode='none', fillcolor='rgba(20, 184, 166, 0.2)', name='Z2'))
            # Z3
            mask_z3 = (x >= VT1_X) & (x <= 65)
            fig.add_trace(go.Scatter(x=x[mask_z3], y=y[mask_z3], fill='tozeroy', mode='none', fillcolor='rgba(245, 158, 11, 0.2)', name='Z3'))
            # Z4
            mask_z4 = (x >= 65) & (x <= VT2_X)
            fig.add_trace(go.Scatter(x=x[mask_z4], y=y[mask_z4], fill='tozeroy', mode='none', fillcolor='rgba(249, 115, 22, 0.2)', name='Z4'))
            # Z5
            fig.add_trace(go.Scatter(x=x[x>=VT2_X], y=y[x>=VT2_X], fill='tozeroy', mode='none', fillcolor='rgba(239, 68, 68, 0.2)', name='Z5'))

        # De hoofdlijn
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='#1e293b', width=4), name='Ademvolume (VE)'))

        # Verticale lijnen voor VT1 en VT2
        fig.add_vline(x=VT1_X, line_width=2, line_dash="dash", line_color="#94a3b8", annotation_text="VT1 (Ademarbeid stijgt)", annotation_position="top left")
        fig.add_vline(x=VT2_X, line_width=2, line_dash="dash", line_color="#94a3b8", annotation_text="VT2 (Steady wordt lastig)", annotation_position="top left")

        # Layout cleanup
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, showticklabels=False, title="Intensiteit (%)"),
            yaxis=dict(showgrid=False, showticklabels=False, title="Ventilatie"),
            margin=dict(l=0, r=0, t=30, b=0),
            showlegend=False,
            height=350,
            hovermode="x unified"
        )

        st.plotly_chart(fig, use_container_width=True)

# --- SIDEBAR INFO ---
with col_sidebar:
    st.markdown("""
    <div class="theory-card">
        <h3 style="color:white; margin-top:0;">WAAROM ZONES?</h3>
        <p style="color:#94a3b8; font-size: 0.9rem;">Doseren op fysiologie, niet op gevoel.</p>
        <hr style="border-color: #334155;">
        <div style="font-size: 0.85rem; line-height: 1.6;">
            <p>✅ Easy écht easy houden, hard écht hard.</p>
            <p>✅ Koppel zones aan Watt + context (Adem/RPE).</p>
            <p style="color: #f87171; font-weight: bold;">❤️ VT1 & VT2 zijn exactere ankers dan % HRmax.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# -----------------------------------------------------------------------------
# 4. ZONE DETAILS (Interactief)
# -----------------------------------------------------------------------------

# Knoppen voor zones
zone_keys = list(active_zones.keys())
cols = st.columns(len(zone_keys))

# We gebruiken session state om de selectie te onthouden
if 'selected_zone' not in st.session_state:
    st.session_state.selected_zone = zone_keys[0]

# Reset selectie als model verandert
if st.session_state.selected_zone not in active_zones:
    st.session_state.selected_zone = zone_keys[0]

def set_zone(z):
    st.session_state.selected_zone = z

for i, col in enumerate(cols):
    z_key = zone_keys[i]
    if col.button(z_key, use_container_width=True, key=f"btn_{z_key}"):
        set_zone(z_key)

# Huidige data ophalen
curr = active_zones[st.session_state.selected_zone]

# Details tonen
st.markdown(f"<div style='height: 20px;'></div>", unsafe_allow_html=True) # Spacer

c_detail_L, c_detail_R = st.columns([1.5, 1])

with c_detail_L:
    st.markdown(f"""
    <div class="custom-card" style="border-top: 5px solid {curr['stroke']};">
        <h1 style="color: {curr['stroke']}; margin-bottom: 0;">{curr['title']}</h1>
        <p style="font-weight: bold; color: #64748b; letter-spacing: 1px; text-transform: uppercase;">{curr['subtitle']}</p>
        
        <h4 style="margin-top: 1.5rem; display:flex; align-items:center; gap:8px;">📖 Theorie</h4>
        <p style="font-size: 1.1rem; line-height: 1.6; color: #334155;">{curr['theory']}</p>
        
        <ul>
            {"".join([f"<li style='color: #475569; margin-bottom: 4px;'>{b}</li>" for b in curr['bullets']])}
        </ul>

        <div class="takeaway-box">
            💡 GOUDEN TAKEAWAY: {curr['takeaway']}
        </div>
    </div>
    """, unsafe_allow_html=True)

with c_detail_R:
    st.markdown(f"""
    <div class="custom-card">
        <h4 style="margin-top:0; color: #64748b;">⚡ Prikkels</h4>
        <ul style="margin-bottom: 1.5rem;">
            {"".join([f"<li>{p}</li>" for p in curr['prikkels']])}
        </ul>

        <h4 style="margin-top:0; color: #64748b;">🎯 Doelen</h4>
        <ul style="margin-bottom: 1.5rem;">
            {"".join([f"<li>{d}</li>" for d in curr['doelen']])}
        </ul>

        <h4 style="margin-top:0; color: #64748b;">🚴 Voorbeelden</h4>
        <ul>
            {"".join([f"<li style='font-style: italic;'>{v}</li>" for v in curr['voorbeelden']])}
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<div style='text-align: center; color: #cbd5e1; margin-top: 3rem; font-size: 0.8rem;'>VT1 & VT2 — De Ankers van jouw Succes</div>", unsafe_allow_html=True)
