import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------------------------------------------------------
# 1. CONFIGURATIE & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Zone Explorer", layout="wide")

st.markdown("""
<style>
    /* Algemene styling */
    .main {background-color: #fdfdfd;}
    h1, h2, h3 {font-family: 'Helvetica', sans-serif; font-weight: 900; color: #111827;}
    
    /* Header */
    .header-title {font-size: 3rem; font-weight: 900; color: #111827; text-align: center; margin-bottom: 5px;}
    .header-accent {color: #ef4444; font-style: italic;}
    .header-sub {text-align: center; color: #6b7280; font-size: 1.1rem; margin-bottom: 40px;}
    
    /* Tabs/Radio Buttons */
    div.stRadio > div {display: flex; justify-content: center; gap: 20px;}
    div.stRadio > div > label {
        background-color: #f3f4f6; padding: 10px 25px; border-radius: 10px; 
        font-weight: bold; border: 2px solid transparent; cursor: pointer; transition: 0.3s;
    }
    div.stRadio > div > label:hover {background-color: #e5e7eb;}
    
    /* Kaarten en Boxen */
    .zone-card {
        padding: 30px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        height: 100%; color: #1f2937;
    }
    .valkuil-box {
        background-color: rgba(0,0,0,0.04); border-left: 4px solid rgba(0,0,0,0.2);
        padding: 15px; margin-top: 25px; font-style: italic; font-size: 0.95rem;
    }
    .info-box {
        background-color: white; padding: 25px; border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06); margin-bottom: 20px; border: 1px solid #f3f4f6;
    }
    
    /* Knoppen */
    div.stButton > button {
        border-radius: 50px; border: 1px solid #e5e7eb; background-color: white;
        color: #374151; font-weight: 800; width: 100%; transition: all 0.2s;
    }
    div.stButton > button:hover {
        border-color: #111827; color: #111827; transform: translateY(-2px);
    }
    
    /* Lijstjes styling */
    ul { margin-bottom: 0; }
    li { margin-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. GRAFIEK LOGICA (Gebaseerd op Slide 1, 2 & 3)
# -----------------------------------------------------------------------------
def draw_lactate_curve(model_type):
    # Simulatie van een lactaatcurve
    x = np.linspace(0, 100, 500)
    y = 0.8 + 0.00005 * np.power(x, 2.9) 
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Minimalistische stijl
    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    
    # De Curve
    ax.plot(x, y, color='#1f2937', linewidth=4, zorder=10)
    
    # ANKERS DEFINIËREN (Uit Slide 3: VT1 en VT2 zijn de vaste ankers)
    # VT1 = Grens tussen Z2 en Z3 (in 5-zone model)
    # VT2 = Grens tussen Z4 en Z5 (in 5-zone model)
    vt1_x = 48 
    vt2_x = 78
    ymax = max(y)

    # Verticale lijnen voor VT1 en VT2
    ax.vlines(x=vt1_x, ymin=0, ymax=ymax, colors='#6b7280', linestyles='dotted', linewidth=1.5)
    ax.vlines(x=vt2_x, ymin=0, ymax=ymax, colors='#6b7280', linestyles='dotted', linewidth=1.5)
    
    # Labels boven de lijnen (Zoals op Slide 1 & 3)
    ax.text(vt1_x, ymax, " VT1 / LT1 ", ha='center', va='bottom', fontsize=9, fontweight='bold', backgroundcolor='#e5e7eb', color='#374151')
    ax.text(vt2_x, ymax, " VT2 / LT2 ", ha='center', va='bottom', fontsize=9, fontweight='bold', backgroundcolor='#e5e7eb', color='#374151')
    
    # --- VLAKVERDELING ---
    if model_type == "3-Zone Model":
        # Slide 1: Zone 1 (Groen) tot VT1, Zone 2 (Oranje) tot VT2, Zone 3 (Rood) na VT2
        ax.fill_between(x, y, where=(x <= vt1_x), color='#dcfce7', alpha=0.8) # Green
        ax.text(24, 0.5, "ZONE 1", ha='center', fontsize=10, fontweight='bold', color='#166534')
        
        ax.fill_between(x, y, where=((x > vt1_x) & (x <= vt2_x)), color='#ffedd5', alpha=0.8) # Orange
        ax.text(63, 1.0, "ZONE 2", ha='center', fontsize=10, fontweight='bold', color='#9a3412')
        
        ax.fill_between(x, y, where=(x > vt2_x), color='#fee2e2', alpha=0.8) # Red
        ax.text(89, 2.5, "ZONE 3", ha='center', fontsize=10, fontweight='bold', color='#991b1b')
        
    elif model_type == "5-Zone Model":
        # Slide 2: Z1/Z2 (Groen), Z3 (Geel), Z4 (Oranje), Z5 (Rood)
        
        # Z1 (Laag in het groene blok)
        z1_limit = 28
        ax.fill_between(x, y, where=(x <= z1_limit), color='#dcfce7', alpha=0.9)
        ax.text(14, 0.4, "Z1", ha='center', fontsize=9, fontweight='bold', color='#166534')
        
        # Z2 (Tot aan VT1 - Slide 5: "Onder of rond VT1")
        ax.fill_between(x, y, where=((x > z1_limit) & (x <= vt1_x)), color='#bbf7d0', alpha=0.9) # Iets donkerder groen
        ax.text(38, 0.6, "Z2", ha='center', fontsize=9, fontweight='bold', color='#15803d')
        
        # Z3 (Direct na VT1 - Slide 6: "Comfortabel zwaar")
        z3_limit = 63
        ax.fill_between(x, y, where=((x > vt1_x) & (x <= z3_limit)), color='#fef9c3', alpha=0.9) # Geel
        ax.text(55, 0.9, "Z3", ha='center', fontsize=9, fontweight='bold', color='#854d0e')
        
        # Z4 (Tot aan VT2 - Slide 7: "Rond VT2")
        ax.fill_between(x, y, where=((x > z3_limit) & (x <= vt2_x)), color='#ffedd5', alpha=0.9) # Oranje
        ax.text(70, 1.5, "Z4", ha='center', fontsize=9, fontweight='bold', color='#9a3412')
        
        # Z5 (Boven VT2 - Slide 8: "Boven VT2")
        ax.fill_between(x, y, where=(x > vt2_x), color='#fee2e2', alpha=0.9) # Rood
        ax.text(90, 3.0, "Z5", ha='center', fontsize=9, fontweight='bold', color='#991b1b')

    # Assen labels (Slide 1)
    ax.text(0, ymax/2, "Lactate (mmol/L)", rotation=90, va='center', ha='right', color='#9ca3af', fontsize=8)
    ax.text(50, -0.2, "Power (W)", ha='center', color='#9ca3af', fontsize=8)

    return fig

# -----------------------------------------------------------------------------
# 3. CONTENT (DATA UIT SLIDE 4-8)
# -----------------------------------------------------------------------------

# De teksten hieronder zijn letterlijk overgenomen uit je screenshots
zones_data = {
    "Zone 1": {
        "title": "ZONE 1", 
        "subtitle": "Herstel / Actief Herstel",
        "desc": "Heel rustig trappen. Praattempo: je kunt moeiteloos blijven praten. Ademhaling blijft laag en stabiel.",
        "herkenning": "Heel rustig trappen. Praattempo: je kunt moeiteloos praten.",
        "prikkels": [
            "Herstelcapaciteit (doorbloeding, 'frisse benen')",
            "Techniek/cadans zonder metabole stress",
            "Basisvolume met minimale belasting"
        ],
        "doelen": [
            "Sneller herstellen tussen zware sessies",
            "Volume toevoegen zonder extra vermoeidheid",
            "Consistent kunnen trainen week na week"
        ],
        "valkuil": "Als je alleen Z1 doet, bouw je weinig prestatieprikkel op—Z1 is ondersteunend, niet 'het hele plan'.",
        "color_bg": "#dcfce7", "color_border": "#86efac", "color_accent": "#166534"
    },
    "Zone 2": {
        "title": "ZONE 2", 
        "subtitle": "Duur / Aerobe Basis",
        "desc": "Rustig tot steady. Je kunt nog praten, maar je voelt dat je 'werkt'. Dit zit onder of rond VT1: vaak de hoogste intensiteit die je lang kunt stapelen.",
        "herkenning": "Rustig tot steady. Je kunt nog praten, maar voelt dat je 'werkt'.",
        "prikkels": [
            "Aerobe capaciteit (meer 'motor')",
            "Aerobe efficiëntie: zelfde watt = minder ademdruk/HR",
            "Vet+koolhydraatmix efficiënt gebruiken (zonder 'vet-only' mythes)"
        ],
        "doelen": [
            "Uithoudingsvermogen (lange ritten, fond, gran fondo)",
            "Basis voor intensiever werk (Z4-Z5 kun je beter verwerken)",
            "Betere pacing: minder snel 'opblazen'"
        ],
        "valkuil": "Z2 label verschilt per model. VT1 is het anker waarmee je jouw Z2 goed kalibreert.",
        "color_bg": "#f0fdf4", "color_border": "#bbf7d0", "color_accent": "#15803d"
    },
    "Zone 3": {
        "title": "ZONE 3", 
        "subtitle": "Tempo / Comfortabel Zwaar",
        "desc": "Stevig. Korte zinnen praten lukt nog nét. Dit is vaak 'comfortabel zwaar': je kunt het best lang volhouden, maar herstelkosten lopen op.",
        "herkenning": "Stevig. Korte zinnen praten lukt nog nét.",
        "prikkels": [
            "Tempo-uithoudingsvermogen (langere stukken stevig rijden)",
            "Race-gevoel / sportspecifiek tempo",
            "Mentale tolerantie voor 'stevig doorrijden'"
        ],
        "doelen": [
            "Gran fondo / lange solo's / langere beklimmingen",
            "Dieselvermogen en langdurig tempo rijden",
            "Specifieke voorbereiding op race pace"
        ],
        "valkuil": "Z3 wordt snel je standaard (groep, wind, heuvels). Te veel Z3 -> minder ruimte voor écht veel Z2 én kwaliteit in Z4-Z5.",
        "color_bg": "#fefce8", "color_border": "#fde047", "color_accent": "#a16207"
    },
    "Zone 4": {
        "title": "ZONE 4", 
        "subtitle": "Threshold",
        "desc": "Hard, je kunt nauwelijks praten. Dit zit rond je VT2-anker: ademdruk is hoog en het voelt alsof je het tempo 'moet managen'.",
        "herkenning": "Hard, je kunt nauwelijks praten. Rond VT2-anker.",
        "prikkels": [
            "Drempelvermogen verhogen (hoog, lang vol te houden)",
            "Tolerantie voor hoge ventilatie/ademdruk",
            "Pacingvaardigheid rond wedstrijdintensiteit (TT/klim)"
        ],
        "doelen": [
            "Sneller worden op 20-60 min inspanningen",
            "Tijdrit / lange klim / breakaway-werk",
            "Hogere 'stabiele' watts voor race-onderdelen"
        ],
        "valkuil": "HR kan achterlopen bij korte stappen (HR-lag); daarom is watt + ademrespons vaak betrouwbaarder om dit domein te plaatsen.",
        "color_bg": "#fff7ed", "color_border": "#fdba74", "color_accent": "#c2410c"
    },
    "Zone 5": {
        "title": "ZONE 5", 
        "subtitle": "VO2 max / Zeer Hard",
        "desc": "Zeer hard. Praten kan niet. Blokken zijn kort, ventilatie gaat maximaal. Dit is duidelijk boven VT2 en bedoeld om tijd op hoog aeroob vermogen te maken.",
        "herkenning": "Zeer hard. Praten kan niet. Duidelijk boven VT2.",
        "prikkels": [
            "VO2max-prikkel (centrale + perifere belasting)",
            "Hoog vermogen herhalen onder vermoeidheid",
            "Verbetering van 'top-end' en klim-aanzetten"
        ],
        "doelen": [
            "Klimvermogen op 3-8 min verbeteren",
            "Sneller herstellen tussen harde inspanningen",
            "Race-situaties: gaten dichten, attacks, harde passages"
        ],
        "valkuil": "Z5 vraagt veel herstel. Werkt het best met veel Z1-Z2 eromheen ('best of both worlds').",
        "color_bg": "#fef2f2", "color_border": "#fca5a5", "color_accent": "#b91c1c"
    }
}

# -----------------------------------------------------------------------------
# 4. PAGINA OPBOUW
# -----------------------------------------------------------------------------

# Header
st.markdown("""
    <div class='header-title'>Master je <span class='header-accent'>Intensiteit.</span></div>
    <div class='header-sub'>Fysiologische ankers & zones (gebaseerd op VT1 & VT2)</div>
""", unsafe_allow_html=True)

# Model Switcher
col_spacer_l, col_select, col_spacer_r = st.columns([1, 2, 1])
with col_select:
    model_choice = st.radio("", ["3-Zone Model", "5-Zone Model"], horizontal=True, label_visibility="collapsed")

st.write("")

# BOVENKANT: GRAFIEK + LEGEND
c_graph, c_info = st.columns([1.6, 1], gap="medium")

with c_graph:
    st.pyplot(draw_lactate_curve(model_choice))

with c_info:
    st.markdown(f"### {model_choice}")
    if model_choice == "3-Zone Model":
        st.write("Het fysiologische basismodel (Slide 1).")
        st.info("**Zone 1 (Groen):** Onder VT1. Rustig & Duur.")
        st.warning("**Zone 2 (Oranje):** Tussen VT1 en VT2. Tempo & Threshold.")
        st.error("**Zone 3 (Rood):** Boven VT2. High Intensity.")
    else:
        st.write("Coachingdetail voor specifiekere prikkels (Slide 2).")
        st.success("**Z1 & Z2:** Onder VT1 (Basis)")
        st.warning("**Z3 & Z4:** Tussen VT1 en VT2 (Tempo/Drempel)")
        st.error("**Z5:** Boven VT2 (VO2 Max)")
    
    st.markdown("""
    <div style="background-color: #111827; color: white; padding: 20px; border-radius: 15px; margin-top: 20px;">
        <p style="font-style: italic; font-size: 0.9rem; margin:0;">
        "VT1 & VT2 zijn je fysiologische drempels voor zones. Zones = doseren op fysiologie, niet op gevoel alleen."
        </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ONDERKANT: INTERACTIEVE ZONE DETAILS
st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>ONTDEK ELKE ZONE</h2>", unsafe_allow_html=True)

if 'selected_zone' not in st.session_state:
    st.session_state.selected_zone = "Zone 1"

def set_zone(z): st.session_state.selected_zone = z

# Knoppenbalk
cols = st.columns(5)
keys = list(zones_data.keys())
for i, col in enumerate(cols):
    with col:
        if st.button(keys[i], key=f"btn_{i}", use_container_width=True):
            set_zone(keys[i])

# Data ophalen
curr = zones_data[st.session_state.selected_zone]

# Weergave Details
col_left, col_right = st.columns([1.2, 1], gap="large")

with col_left:
    st.markdown(f"""
    <div class="zone-card" style="background-color: {curr['color_bg']}; border: 3px solid {curr['color_border']};">
        <h2 style="color: {curr['color_accent']}; margin-top:0;">{curr['title']}</h2>
        <h4 style="color: #6b7280;">{curr['subtitle']}</h4>
        
        <p style="font-size: 1.1rem; line-height: 1.6; margin-top: 20px;">
            <b>Wat is het (herkenning):</b><br>
            {curr['desc']}
        </p>
        
        <div class="valkuil-box">
             <strong>⚠️ LET OP / VALKUIL:</strong><br>
             {curr['valkuil']}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    # Lijstjes genereren
    prikkels_html = "".join([f"<li>{item}</li>" for item in curr['prikkels']])
    doelen_html = "".join([f"<li>{item}</li>" for item in curr['doelen']])
    
    st.markdown(f"""
    <div class="info-box">
        <strong style="color: #9ca3af; letter-spacing: 1px; font-size: 0.85rem;">TRAININGSPRIKKELS (Slide {4 + keys.index(st.session_state.selected_zone)})</strong>
        <ul style="padding-left: 20px; margin-top: 5px; margin-bottom: 20px;">{prikkels_html}</ul>
        
        <strong style="color: #9ca3af; letter-spacing: 1px; font-size: 0.85rem;">DOELEN WAAR DIT BIJ HELPT</strong>
        <ul style="padding-left: 20px; margin-top: 5px;">{doelen_html}</ul>
    </div>
    """, unsafe_allow_html=True)
