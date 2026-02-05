import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------------------------------------------------------
# 1. SETUP & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Zone Explorer", layout="wide")

# We voegen CSS toe om de moderne 'look & feel' van je React code na te bootsen
st.markdown("""
<style>
    /* Algemeen */
    .main {background-color: #f8fafc;} /* Slate-50 look */
    h1, h2, h3, h4, p, div {font-family: 'Helvetica', sans-serif;}
    
    /* Header Knoppen */
    div.stRadio > div {display: flex; justify-content: center; gap: 10px;}
    div.stRadio > div > label {
        background-color: #e2e8f0; padding: 10px 25px; border-radius: 12px; 
        font-weight: bold; border: 2px solid transparent; cursor: pointer; transition: 0.3s;
        color: #475569;
    }
    div.stRadio > div > label:hover {background-color: #cbd5e1;}
    div.stRadio > div > label[data-baseweb="radio"] > div:first-child {background-color: #0f172a;}
    
    /* Navigatie Knoppen (Zone 1, Zone 2 etc) */
    div.stButton > button {
        border-radius: 16px; border: 2px solid #e2e8f0; background-color: white;
        color: #64748b; font-weight: 800; width: 100%; transition: all 0.2s;
        padding: 15px 0;
    }
    div.stButton > button:hover {
        border-color: #0f172a; color: #0f172a; transform: translateY(-2px);
        background-color: #f8fafc;
    }
    
    /* Kaarten en Boxen */
    .card-shadow {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    /* Specifieke tekst stijlen */
    .tracking-widest { letter-spacing: 0.1em; }
    .uppercase { text-transform: uppercase; }
    .font-black { font-weight: 900; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA (Vertaald uit jouw React objecten 'zones3' en 'zones5')
# -----------------------------------------------------------------------------

# Helper om kleuren te bepalen (vertaald uit jouw getColor functie)
def get_colors(color_class):
    colors = {
        'emerald': {'bg': '#ecfdf5', 'border': '#a7f3d0', 'text': '#047857', 'accent': '#059669', 'fill': '#dcfce7'},
        'teal':    {'bg': '#f0fdf4', 'border': '#99f6e4', 'text': '#0f766e', 'accent': '#0d9488', 'fill': '#ccfbf1'},
        'amber':   {'bg': '#fffbeb', 'border': '#fde68a', 'text': '#b45309', 'accent': '#d97706', 'fill': '#fef9c3'},
        'orange':  {'bg': '#fff7ed', 'border': '#fed7aa', 'text': '#c2410c', 'accent': '#ea580c', 'fill': '#ffedd5'},
        'red':     {'bg': '#fef2f2', 'border': '#fecaca', 'text': '#b91c1c', 'accent': '#dc2626', 'fill': '#fee2e2'}
    }
    return colors.get(color_class, colors['emerald'])

zones3 = {
    "Zone 1": {
        "title": "ZONE 1 (LOW)", "subtitle": "Onder VT1 - Stabiele Ademhaling",
        "theory": "De basis van elke training. Je ademhaling blijft laag en stabiel. Je gebruikt hoofdzakelijk vetten en de interne belasting is minimaal.",
        "bullets": ["Easy écht easy houden", "Basisdomein voor vetverbranding", "Minimale metabole stress"],
        "prikkels": ["Capillarisatie", "Mitochondriale efficiëntie", "Basisvolume"],
        "doelen": ["Vetverbranding optimaliseren", "Herstel bevorderen", "Basisconditie"],
        "voorbeelden": ["60-90 min herstelrit", "Warming-up"],
        "takeaway": "Zones = doseren op fysiologie, niet op gevoel alleen.",
        "colorClass": "emerald"
    },
    "Zone 2": {
        "title": "ZONE 2 (TEMPO)", "subtitle": "Tussen VT1 & VT2 - Verhoogde Ventilatie",
        "theory": "Het overgangsgebied. Ademarbeid stijgt merkbaar. Je kunt nog praten, maar in kortere zinnen. Herstelkosten lopen op.",
        "bullets": ["Comfortabel zwaar tempo", "Dieselvermogen opbouwen", "Mentale tolerantie voor inspanning"],
        "prikkels": ["Tempo-uithoudingsvermogen", "Race-gevoel", "Koolhydraat-mix efficiëntie"],
        "doelen": ["Gran fondo tempo", "Lange solo's", "Specifieke race pace"],
        "voorbeelden": ["2x20 min tempo", "Lange klim steady"],
        "takeaway": "VT1 & VT2 zijn je fysiologische ankers voor zones.",
        "colorClass": "orange"
    },
    "Zone 3": {
        "title": "ZONE 3 (HIGH)", "subtitle": "Boven VT2 - Maximale Ademarbeid",
        "theory": "Boven de tweede ventilatoire drempel. Ademhaling gaat maximaal. 'Steady' rijden wordt onmogelijk; dit is werk met een hoge herstelvraag.",
        "bullets": ["Hard werk hard genoeg maken", "Werken tegen het aerobe plafond", "Maximale ventilatoire druk"],
        "prikkels": ["VO2max prikkel", "Lactaat tolerantie", "Top-end vermogen"],
        "doelen": ["Klimvermogen (3-8 min)", "Gaten dichten / attacks", "FTP verhogen"],
        "voorbeelden": ["4x4 Norway intervallen", "30/30's"],
        "takeaway": "Meting via ademvariabelen (VE, Rf) is de gouden standaard.",
        "colorClass": "red"
    }
}

zones5 = {
    "Zone 1": {
        "title": "ZONE 1", "subtitle": "Herstel (Ver onder VT1)",
        "theory": "Heel rustig trappen. Praattempo: moeiteloos praten. Ademhaling blijft laag en stabiel.",
        "bullets": ["Easy écht easy houden", "Ondersteunend, niet het hele plan"],
        "prikkels": ["Herstelcapaciteit (doorbloeding)", "Techniek/cadans zonder stress", "Basisvolume"],
        "doelen": ["Sneller herstellen", "Volume zonder vermoeidheid", "Consistentie"],
        "voorbeelden": ["30-60 min herstelrit", "Spin na intervaldag"],
        "takeaway": "Z1 is ondersteunend voor de rest van je plan.",
        "colorClass": "emerald"
    },
    "Zone 2": {
        "title": "ZONE 2", "subtitle": "Aerobe Basis (Kalibreren met VT1)",
        "theory": "Rustig tot steady. Je voelt dat je 'werkt'. Zit onder of rond VT1: hoogste intensiteit die je lang kunt stapelen.",
        "bullets": ["Hoogste aerobe efficiëntie", "Zelfde watt = minder ademdruk over tijd"],
        "prikkels": ["Aerobe capaciteit", "Aerobe efficiëntie", "Vet+koolhydraatmix"],
        "doelen": ["Uithoudingsvermogen", "Basis voor intensief werk", "Betere pacing"],
        "voorbeelden": ["90-240 min duurrit", "2-3 uur basis"],
        "takeaway": "VT1 is het anker waarmee je Z2 goed kalibreert.",
        "colorClass": "teal"
    },
    "Zone 3": {
        "title": "ZONE 3", "subtitle": "Tempo (Comfortabel Zwaar)",
        "theory": "Stevig. Korte zinnen lukken nét. Je krijgt sneller 'drift' (zelfde watt = hogere ademdruk/HR).",
        "bullets": ["Valkuil: te vaak 'grijs' rijden", "Dieselvermogen trainen"],
        "prikkels": ["Tempo-uithoudingsvermogen", "Race-gevoel", "Mentale tolerantie"],
        "doelen": ["Gran fondo / lange solo's", "Specifieke race pace"],
        "voorbeelden": ["3x15 min tempo", "Lange klim steady"],
        "takeaway": "Voorkom dat Z3 je standaardrit wordt.",
        "colorClass": "amber"
    },
    "Zone 4": {
        "title": "ZONE 4", "subtitle": "Threshold (Rond VT2)",
        "theory": "Hard, nauwelijks praten. Ademdruk is hoog, tempo 'managen'. Duidelijke herstelvraag.",
        "bullets": ["Drempelvermogen verhogen", "Tolerantie voor hoge ventilatie"],
        "prikkels": ["Drempelvermogen", "Pacingvaardigheid", "Ademrespons training"],
        "doelen": ["Sneller op 20-60 min inspanningen", "Tijdrit / breakaway"],
        "voorbeelden": ["3x10 min threshold", "Over/unders"],
        "takeaway": "Wattage + ademrespons is hier betrouwbaarder dan HR.",
        "colorClass": "orange"
    },
    "Zone 5": {
        "title": "ZONE 5", "subtitle": "VO2 Max (Boven VT2)",
        "theory": "Zeer hard. Praten onmogelijk. Ventilatie gaat maximaal. Tijd doorbrengen tegen aerobe plafond.",
        "bullets": ["Kort & scherp", "Vraagt veel herstel"],
        "prikkels": ["VO2max-prikkel", "Top-end verbetering", "Herstel tussen pieken"],
        "doelen": ["Klimvermogen verbeteren", "Attacks / gaten dichten"],
        "voorbeelden": ["4x4 Norway", "5x3 min intervallen"],
        "takeaway": "Werkt best met veel Z1-Z2 eromheen.",
        "colorClass": "red"
    }
}

# -----------------------------------------------------------------------------
# 3. GRAFIEK (Matplotlib versie van jouw Recharts AreaChart)
# -----------------------------------------------------------------------------
def draw_ventilation_chart(vt1, vt2):
    x = np.linspace(0, 100, 101)
    # Formule uit jouw react code: 15 + 0.001 * x^2.5
    y = 15 + 0.001 * np.power(x, 2.5)
    
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # Styling
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')

    # Curve
    ax.plot(x, y, color='#1e293b', linewidth=4, zorder=10)
    
    # Fill (Gradient simulatie met blokken)
    ax.fill_between(x, y, where=(x <= vt1), color='#dcfce7', alpha=0.9) # Groen tot VT1
    ax.fill_between(x, y, where=((x > vt1) & (x <= vt2)), color='#ffedd5', alpha=0.9) # Oranje tot VT2
    ax.fill_between(x, y, where=(x > vt2), color='#fee2e2', alpha=0.9) # Rood na VT2
    
    # Ankers
    ymax = max(y)
    ax.vlines(x=vt1, ymin=15, ymax=ymax, colors='#94a3b8', linestyles='dashed', linewidth=2)
    ax.vlines(x=vt2, ymin=15, ymax=ymax, colors='#94a3b8', linestyles='dashed', linewidth=2)
    
    ax.text(vt1, ymax+2, "VT1 ANKER", ha='center', fontsize=9, fontweight='bold', color='#64748b')
    ax.text(vt2, ymax+2, "VT2 ANKER", ha='center', fontsize=9, fontweight='bold', color='#64748b')
    
    return fig

# -----------------------------------------------------------------------------
# 4. APP LOGICA
# -----------------------------------------------------------------------------

# Header
st.markdown("""
<div style="text-align: center; margin-bottom: 30px;">
    <h1 style="font-size: 3rem; margin-bottom: 0; color: #0f172a;">Master je <span style="color: #dc2626; font-style: italic;">Intensiteit.</span></h1>
    <p style="color: #64748b; font-size: 1.1rem; font-weight: 500;">Focus op ventilatoire ankers VT1 & VT2 als leidraad.</p>
</div>
""", unsafe_allow_html=True)

# Model Switcher
c1, c2, c3 = st.columns([1,2,1])
with c2:
    model_choice = st.radio("", ["3-Zone Model", "5-Zone Model"], horizontal=True, label_visibility="collapsed")

# Bepaal actieve data
active_zones = zones3 if model_choice == "3-Zone Model" else zones5
zone_keys = list(active_zones.keys())

# Grafiek Sectie
col_chart, col_sidebar = st.columns([2, 1], gap="medium")

with col_chart:
    st.markdown("""
    <div style="background: white; padding: 20px; border-radius: 20px; border: 1px solid #f1f5f9; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
        <h3 style="margin-top:0; color:#0f172a; display:flex; align-items:center; gap:10px;">
            🌬️ Ventilatoire Respons
        </h3>
    </div>
    """, unsafe_allow_html=True)
    st.pyplot(draw_ventilation_chart(48, 78))

with col_sidebar:
    st.markdown("""
    <div style="background-color: #0f172a; color: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
        <h2 style="font-size: 1.2rem; font-weight: 900; font-style: italic; margin-bottom: 5px; color: white;">WAAROM ZONES?</h2>
        <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 15px;">Doseren op fysiologie, niet op gevoel.</p>
        <div style="font-size: 0.9rem; color: #e2e8f0; display: flex; flex-direction: column; gap: 10px;">
            <div>✅ Easy écht easy houden.</div>
            <div>✅ Koppel zones aan Watt + context.</div>
            <div style="color: #f87171; font-weight: bold; border-top: 1px solid #334155; padding-top: 10px;">❤️ VT1 & VT2 zijn exactere ankers.</div>
        </div>
    </div>
    <div style="background: white; padding: 15px; border-radius: 20px; border: 1px solid #f1f5f9; color: #64748b; font-style: italic; font-size: 0.9rem;">
        ℹ️ "Zones werken pas echt als ze gemeten, gekalibreerd en toegepast worden."
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border: 0; border-top: 1px solid #e2e8f0; margin: 40px 0;'>", unsafe_allow_html=True)

# Zone Navigatie
if 'selected_zone' not in st.session_state:
    st.session_state.selected_zone = "Zone 1"

# Reset als model wisselt en zone niet bestaat
if st.session_state.selected_zone not in active_zones:
    st.session_state.selected_zone = "Zone 1"

cols = st.columns(len(zone_keys))
for i, key in enumerate(zone_keys):
    with cols[i]:
        if st.button(key, key=f"btn_{i}", use_container_width=True):
            st.session_state.selected_zone = key

# DETAIL WEERGAVE
curr = active_zones[st.session_state.selected_zone]
colors = get_colors(curr['colorClass'])

# Layout voor details
c_card, c_info = st.columns([1.5, 1], gap="large")

with c_card:
    # Hier genereren we de grote gekleurde kaart (HTML)
    bullets_html = "".join([f"<li style='margin-bottom: 5px; color: #475569; font-weight: 600;'>{b}</li>" for b in curr['bullets']])
    
    st.markdown(f"""
    <div style="background-color: {colors['bg']}; border: 3px solid {colors['border']}; border-radius: 30px; padding: 40px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
        <h2 style="color: {colors['text']}; font-size: 3rem; font-weight: 900; font-style: italic; margin: 0; line-height: 1;">{curr['title']}</h2>
        <p style="color: #64748b; font-weight: 900; letter-spacing: 2px; font-size: 0.8rem; text-transform: uppercase; margin-top: 10px; margin-bottom: 30px;">{curr['subtitle']}</p>
        
        <div style="margin-bottom: 30px;">
            <h4 style="font-weight: 900; font-size: 0.75rem; color: #94a3b8; letter-spacing: 2px; text-transform: uppercase;">📖 THEORIE</h4>
            <p style="font-size: 1.25rem; font-weight: 700; color: #1e293b; margin-bottom: 20px; line-height: 1.4;">{curr['theory']}</p>
            <ul style="padding-left: 20px; font-style: italic;">
                {bullets_html}
            </ul>
        </div>
        
        <div style="background: rgba(255,255,255,0.7); backdrop-filter: blur(10px); padding: 20px; border-radius: 20px; border: 1px solid white; display: flex; align-items: center; gap: 15px;">
            <div style="background: {colors['bg']}; padding: 10px; border-radius: 12px;">⚠️</div>
            <div>
                <span style="display: block; font-size: 0.65rem; font-weight: 900; color: #94a3b8; text-transform: uppercase; letter-spacing: 2px;">GOUDEN TAKEAWAY</span>
                <span style="color: #334155; font-weight: 700; font-style: italic;">{curr['takeaway']}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c_info:
    # Prikkels & Doelen Box
    prikkels_html = "".join([f"<li style='margin-bottom: 5px;'>{p}</li>" for p in curr['prikkels']])
    doelen_html = "".join([f"<li style='margin-bottom: 5px;'>{d}</li>" for d in curr['doelen']])
    voorbeelden_html = "".join([f"<li style='margin-bottom: 8px; color: #cbd5e1; font-weight: 700; font-style: italic;'>🚴 {v}</li>" for v in curr['voorbeelden']])

    st.markdown(f"""
    <div style="background: white; padding: 30px; border-radius: 30px; border: 1px solid #f1f5f9; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
            <div style="background: #eff6ff; padding: 8px; border-radius: 10px;">⚡</div>
            <h4 style="margin: 0; font-size: 0.75rem; font-weight: 900; letter-spacing: 2px; color: #94a3b8; text-transform: uppercase;">PRIKKELS & DOELEN</h4>
        </div>
        
        <div style="margin-bottom: 20px;">
            <p style="font-size: 0.7rem; font-weight: 900; color: #cbd5e1; text-transform: uppercase; margin-bottom: 5px;">PRIKKELS</p>
            <ul style="padding-left: 20px; font-weight: 700; color: #334155; font-size: 0.95rem;">{prikkels_html}</ul>
        </div>
        
        <div>
            <p style="font-size: 0.7rem; font-weight: 900; color: #cbd5e1; text-transform: uppercase; margin-bottom: 5px;">HELPT BIJ</p>
            <ul style="padding-left: 20px; font-weight: 700; color: #334155; font-size: 0.95rem;">{doelen_html}</ul>
        </div>
    </div>
    
    <div style="background: #0f172a; padding: 30px; border-radius: 30px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
            <div style="background: #1e293b; padding: 8px; border-radius: 10px;">🔥</div>
            <h4 style="margin: 0; font-size: 0.75rem; font-weight: 900; letter-spacing: 2px; color: #64748b; text-transform: uppercase;">PRAKTIJK VOORBEELDEN</h4>
        </div>
        <ul style="padding-left: 0; list-style: none; margin: 0;">
            {voorbeelden_html}
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid #e2e8f0;">
    <p style="color: #cbd5e1; font-size: 0.75rem; font-weight: 900; letter-spacing: 4px; text-transform: uppercase;">VT1 & VT2 — De Ankers van jouw Succes</p>
</div>
""", unsafe_allow_html=True)
