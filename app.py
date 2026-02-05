import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------------------------------------------------------
# 1. CONFIGURATIE & PAGE SETUP
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Zone Explorer", layout="wide")

# CSS Styling voor de hele pagina (Fonts, Knoppen, Kaarten)
st.markdown("""
<style>
    /* Algemeen */
    .main {background-color: #fdfdfd;}
    h1 {font-family: 'Helvetica', sans-serif; font-weight: 900; color: #111827;}
    
    /* Header styling */
    .header-title {font-size: 3.5rem; font-weight: 900; color: #111827; text-align: center; margin-bottom: 0;}
    .header-accent {color: #ef4444; font-style: italic;}
    .header-sub {text-align: center; color: #6b7280; font-size: 1.1rem; margin-top: 10px; margin-bottom: 40px;}
    
    /* Model Switcher Buttons (bovenaan) */
    div.stRadio > div {display: flex; justify-content: center; gap: 20px;}
    div.stRadio > div > label {
        background-color: #f3f4f6; padding: 10px 20px; border-radius: 10px; 
        font-weight: bold; border: 2px solid transparent; cursor: pointer;
    }
    div.stRadio > div > label:hover {background-color: #e5e7eb;}
    
    /* Zone Detail Sectie (Onderkant) */
    .zone-card {
        padding: 40px; border-radius: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        height: 100%; color: #1f2937;
    }
    .zone-title {font-weight: 900; font-size: 42px; font-style: italic; margin-bottom: 5px; line-height: 1.1;}
    .zone-subtitle {font-weight: 700; font-size: 20px; color: #6b7280; margin-bottom: 25px;}
    .valkuil-box {
        background-color: rgba(0,0,0,0.06); border: 2px solid rgba(0,0,0,0.08);
        padding: 20px; border-radius: 15px; font-style: italic; font-weight: 600; margin-top: 20px;
    }
    .info-box {
        background-color: white; padding: 30px; border-radius: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06); margin-bottom: 25px; border: 1px solid #f3f4f6;
    }
    .pro-tip-box {
        background-color: #111827; color: white; padding: 30px;
        border-radius: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.25);
    }
    
    /* Knoppen onderin */
    div.stButton > button {
        border-radius: 50px; border: 1px solid #e5e7eb; background-color: white;
        color: #374151; font-weight: 800; width: 100%;
    }
    div.stButton > button:focus {border-color: #111827; color: #111827; box-shadow: none;}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. FUNCTIE: TEKEN DE GRAFIEK (Lactaatcurve)
# -----------------------------------------------------------------------------
def draw_lactate_curve(model_type):
    x = np.linspace(0, 100, 500)
    # Simuleer een exponentiële lactaatcurve
    y = 0.5 + 0.00005 * np.power(x, 2.8) 
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Verwijder randen voor een clean look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False) # Verberg Y-as lijn
    ax.spines['bottom'].set_visible(False) # Verberg X-as lijn
    ax.set_xticks([]) # Geen cijfers op X-as
    ax.set_yticks([]) # Geen cijfers op Y-as
    
    # Teken de curve (dikke zwarte lijn)
    ax.plot(x, y, color='black', linewidth=5, zorder=10)
    
    # Definieer drempels
    vt1_x = 45
    vt2_x = 75
    ymax = max(y)

    # Verticale stippellijnen voor VT1 en VT2
    ax.vlines(x=vt1_x, ymin=0, ymax=ymax, colors='grey', linestyles='dotted', linewidth=2)
    ax.vlines(x=vt2_x, ymin=0, ymax=ymax, colors='grey', linestyles='dotted', linewidth=2)
    
    # Labels voor VT1 en VT2
    ax.text(vt1_x, ymax, " VT1 / LT1 ", ha='left', va='bottom', fontsize=9, fontweight='bold', backgroundcolor='black', color='white')
    ax.text(vt2_x, ymax, " VT2 / LT2 ", ha='left', va='bottom', fontsize=9, fontweight='bold', backgroundcolor='black', color='white')
    
    # Kleurvlakken invullen op basis van model
    if model_type == "3-Zone Model":
        # Zone 1 (Groen)
        ax.fill_between(x, y, where=(x <= vt1_x), color='#dcfce7', alpha=0.6)
        # Zone 2 (Geel/Oranje - hier Tempo genoemd in 3-zone model)
        ax.fill_between(x, y, where=((x > vt1_x) & (x <= vt2_x)), color='#fef9c3', alpha=0.6)
        # Zone 3 (Rood)
        ax.fill_between(x, y, where=(x > vt2_x), color='#fee2e2', alpha=0.6)
        
    elif model_type == "5-Zone Model":
        # 5 zones verdeling (geschat)
        z1_limit = 35
        z2_limit = vt1_x # 45
        z3_limit = 60
        z4_limit = vt2_x # 75
        
        ax.fill_between(x, y, where=(x <= z1_limit), color='#dcfce7', alpha=0.6) # Z1
        ax.fill_between(x, y, where=((x > z1_limit) & (x <= z2_limit)), color='#ecfdf5', alpha=0.6) # Z2
        ax.fill_between(x, y, where=((x > z2_limit) & (x <= z3_limit)), color='#fef9c3', alpha=0.6) # Z3
        ax.fill_between(x, y, where=((x > z3_limit) & (x <= z4_limit)), color='#ffedd5', alpha=0.6) # Z4
        ax.fill_between(x, y, where=(x > z4_limit), color='#fee2e2', alpha=0.6) # Z5

    # Label Y-as
    ax.text(0, ymax/2, "LACTAAT (MMOL/L)", rotation=90, va='center', ha='right', color='#9ca3af', fontsize=8)
    # Label X-as
    ax.text(50, -0.1, "INTENSITEIT (WATTS/POWER)", ha='center', color='#9ca3af', fontsize=8)

    return fig

# -----------------------------------------------------------------------------
# 3. HEADER & MODEL SELECTIE
# -----------------------------------------------------------------------------

# Titel
st.markdown("""
    <div class='header-title'>Master je <span class='header-accent'>Intensiteit.</span></div>
    <div class='header-sub'>Ontdek de fysiologische ankers achter je trainingszones. Wissel tussen modellen en leer hoe je jouw drempels (VT1 & VT2) optimaal gebruikt.</div>
""", unsafe_allow_html=True)

# Selectie knoppen (Radio buttons die lijken op tabs)
col_spacer_l, col_select, col_spacer_r = st.columns([1, 2, 1])
with col_select:
    model_choice = st.radio("Kies je model:", ["3-Zone Model", "5-Zone Model"], horizontal=True, label_visibility="collapsed")

# -----------------------------------------------------------------------------
# 4. GRAFIEK & UITLEG BOVENAAN
# -----------------------------------------------------------------------------
col_graph, col_expl = st.columns([1.5, 1])

with col_graph:
    st.pyplot(draw_lactate_curve(model_choice))
    
    # Extra uitleg onder grafiek (kleine blokjes)
    c1, c2 = st.columns(2)
    with c1:
        st.info("**VT1 - DE AEROBE DREMPEL**\n\nOmslagpunt waar je ademarbeid merkbaar stijgt, maar je nog stabiel blijft.")
    with c2:
        st.error("**VT2 - DE ANAEROBE DREMPEL**\n\nHet punt van verzuring. 'Steady' rijden wordt hierboven onmogelijk.")

with col_expl:
    st.markdown(f"## *{model_choice.upper()}*")
    
    if model_choice == "3-Zone Model":
        st.write("""
        Het model van de fysiologie. Simpel en krachtig: Domein 1 (Easy), Domein 2 (Tempo) en Domein 3 (Hard). VT1 en VT2 zijn de harde grenzen.
        """)
        st.success("**Domein 1: Aerobic**")
        st.warning("**Domein 2: Threshold**")
        st.error("**Domein 3: Severe**")
    else:
        st.write("""
        Hét instrument voor gedetailleerde coaching. Het splitst de brede domeinen op in specifiekere blokken om je trainingen nog nauwkeuriger te plannen.
        """)
        st.success("**Z1/Z2: Basis**")
        st.warning("**Z3/Z4: Tempo**")
        st.error("**Z5+: High End**")

    # De donkere quote box rechts
    st.markdown("""
    <div class="pro-tip-box" style="margin-top: 20px;">
        <p style="font-style: italic; font-size: 0.9rem;">
        "Het doel van zones is niet om cijfers na te jagen, maar om je lichaam de juiste prikkel op het juiste moment te geven."
        </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# -----------------------------------------------------------------------------
# 5. ZONE DETAIL SECTIE (ONDERKANT)
# -----------------------------------------------------------------------------

st.markdown("<h2 style='text-align: center; color: #9ca3af; letter-spacing: 2px; font-size: 1.5rem; margin-bottom: 30px;'>ONTDEK ELKE ZONE</h2>", unsafe_allow_html=True)

# Data voor de 5 zones
zones_data = {
    "Zone 1": {
        "title": "ZONE 1: HERSTEL", "subtitle": "Herstel / Actief Herstel",
        "desc": "Heel rustig trappen. Praattempo: je kunt moeiteloos blijven praten. De focus ligt hier op doorbloeding en het 'spoelen' van de benen zonder metabole stress.",
        "valkuil": "Te veel Z1 bouwt geen conditie op, maar is essentieel voor je volume.",
        "prikkels": ["Ideaal na zware intervaldagen", "Verbeter herstelcapaciteit", "Houd ademhaling laag"],
        "color_bg": "#dcfce7", "color_border": "#86efac", "color_accent": "#166534"
    },
    "Zone 2": {
        "title": "ZONE 2: AEROBE BASIS", "subtitle": "Duur / Kalibreren met VT1",
        "desc": "Dit is de motorkamer. Onder VT1 train je de aerobe efficiëntie en vetverbranding. Je voelt dat je werkt, maar kunt nog hele zinnen praten.",
        "valkuil": "Gevaar van de 'grijze zone': te hard voor Z2, te zacht voor echte kwaliteit.",
        "prikkels": ["Bulk van je training", "Verhoogt mitochondriale dichtheid", "Lage herstelkosten"],
        "color_bg": "#ecfdf5", "color_border": "#a7f3d0", "color_accent": "#065f46"
    },
    "Zone 3": {
        "title": "ZONE 3: TEMPO", "subtitle": "Comfortabel Zwaar",
        "desc": "Stevig doorrijden. Korte zinnen lukken nog nét. Dit is vaak het tempo van een Gran Fondo of lange klim. De herstelkosten beginnen hier op te lopen.",
        "valkuil": "Wordt snel de 'standaard' rit, waardoor je nooit écht uitrust of écht hard traint.",
        "prikkels": ["Mentale tolerantie", "Specifiek tempo-duur", "Dieselvermogen"],
        "color_bg": "#fef9c3", "color_border": "#fde047", "color_accent": "#854d0e"
    },
    "Zone 4": {
        "title": "ZONE 4: THRESHOLD", "subtitle": "Drempel / Rond VT2",
        "desc": "Hard. Praten is bijna onmogelijk. Dit zit rond je anaerobe drempel. Essentieel voor het verhogen van je FTP/Drempelvermogen.",
        "valkuil": "Te vaak in Z4 leidt snel tot overtraining en chronische vermoeidheid.",
        "prikkels": ["Verhoogt anaerobe drempel", "Lactaat tolerantie", "Pacing vaardigheden"],
        "color_bg": "#ffedd5", "color_border": "#fdba74", "color_accent": "#9a3412"
    },
    "Zone 5": {
        "title": "ZONE 5: VO2 MAX", "subtitle": "Zeer Hard / Maximaal",
        "desc": "Alles geven. Je ventilatie is maximaal. Blokken zijn kort (3-8 min). Bedoeld om je aerobe plafond (VO2 Max) te verhogen.",
        "valkuil": "Vraagt zeer veel hersteltijd. Alleen doen als je fris bent.",
        "prikkels": ["Verhoogt aerobe plafond", "Klim-attacks oefenen", "Top-end vermogen"],
        "color_bg": "#fee2e2", "color_border": "#fca5a5", "color_accent": "#991b1b"
    }
}

# State Management voor knoppen
if 'selected_zone' not in st.session_state:
    st.session_state.selected_zone = "Zone 1"

def set_zone(z): st.session_state.selected_zone = z

# Knoppenbalk
c_spacer, c1, c2, c3, c4, c5, c_spacer2 = st.columns([1, 2, 2, 2, 2, 2, 1])
btn_cols = [c1, c2, c3, c4, c5]
zones_list = list(zones_data.keys())

for i, zone_name in enumerate(zones_list):
    with btn_cols[i]:
        if st.button(zone_name.upper(), key=f"zbtn_{i}", use_container_width=True):
            set_zone(zone_name)

st.write("")

# Content weergave (Links Kaart, Rechts Info)
curr = zones_data[st.session_state.selected_zone]
col_l, col_r = st.columns([1.3, 1], gap="large")

with col_l:
    # Let op: f-string formatting correct toegepast om HTML-fouten te voorkomen
    st.markdown(f"""
    <div class="zone-card" style="background-color: {curr['color_bg']}; border: 3px solid {curr['color_border']};">
        <div class="zone-title" style="color: {curr['color_accent']}">{curr['title']}</div>
        <div class="zone-subtitle">{curr['subtitle']}</div>
        <p style="font-size: 1.1rem; line-height: 1.6;">{curr['desc']}</p>
        <div class="valkuil-box">
            <span style="font-weight: 800; font-size: 0.8rem; color: #4b5563; display: block; margin-bottom: 5px;">BELANGRIJKE VALKUIL:</span>
            "{curr['valkuil']}"
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_r:
    prikkels_list = "".join([f"<li style='margin-bottom: 8px;'><b>{p}</b></li>" for p in curr['prikkels']])
    st.markdown(f"""
    <div class="info-box">
        <h5 style="color: #9ca3af; font-size: 0.8rem; font-weight: 800; letter-spacing: 1px; margin-bottom: 20px;">TRAININGSPRIKKELS</h5>
        <ul style="padding-left: 20px;">{prikkels_list}</ul>
    </div>
    <div class="pro-tip-box">
        <h5 style="color: #6b7280; font-size: 0.8rem; font-weight: 800; letter-spacing: 1px; margin-bottom: 15px;">CONTEXT PRO TIP</h5>
        <p style="font-style: italic;">"Gebruik hartslag als controle, maar laat wattage leidend zijn voor de meest constante prikkel in deze zone."</p>
    </div>
    """, unsafe_allow_html=True)
