import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------------------------------------------------------
# 1. CONFIGURATIE & PAGE SETUP
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Zone Explorer", layout="wide")

st.markdown("""
<style>
    /* Algemene styling */
    .main {background-color: #fdfdfd;}
    h1 {font-family: 'Helvetica', sans-serif; font-weight: 900; color: #111827;}
    
    /* Header styling */
    .header-title {font-size: 3rem; font-weight: 900; color: #111827; text-align: center; margin-bottom: 0;}
    @media (max-width: 700px) { .header-title { font-size: 2rem; } }
    .header-accent {color: #ef4444; font-style: italic;}
    .header-sub {text-align: center; color: #6b7280; font-size: 1.1rem; margin-top: 10px; margin-bottom: 40px;}
    
    /* Model Switcher Buttons */
    div.stRadio > div {display: flex; justify-content: center; gap: 20px;}
    div.stRadio > div > label {
        background-color: #f3f4f6; padding: 10px 20px; border-radius: 10px; 
        font-weight: bold; border: 2px solid transparent; cursor: pointer;
    }
    div.stRadio > div > label:hover {background-color: #e5e7eb;}
    
    /* Zone Cards */
    .zone-card {
        padding: 30px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        height: 100%; color: #1f2937;
    }
    .valkuil-box {
        background-color: rgba(0,0,0,0.06); border: 2px solid rgba(0,0,0,0.05);
        padding: 15px; border-radius: 10px; font-style: italic; font-weight: 600; margin-top: 20px;
    }
    .info-box {
        background-color: white; padding: 25px; border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px; border: 1px solid #f3f4f6;
    }
    .pro-tip-box {
        background-color: #111827; color: white; padding: 25px;
        border-radius: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    
    /* Buttons */
    div.stButton > button {
        border-radius: 50px; border: 1px solid #e5e7eb; background-color: white;
        color: #374151; font-weight: 800; width: 100%; transition: all 0.2s;
    }
    div.stButton > button:hover {
        border-color: #111827; color: #111827; transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. FUNCTIE: TEKEN DE GRAFIEK
# -----------------------------------------------------------------------------
def draw_lactate_curve(model_type):
    # Data voor de curve
    x = np.linspace(0, 100, 500)
    y = 0.5 + 0.00005 * np.power(x, 2.8) 
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Styles
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Curve lijn
    ax.plot(x, y, color='#1f2937', linewidth=5, zorder=10)
    
    # Drempels (VT1 en VT2 zijn fysiologische feiten, die verplaatsen niet)
    vt1_x = 45
    vt2_x = 75
    ymax = max(y)

    # Verticale lijnen
    ax.vlines(x=vt1_x, ymin=0, ymax=ymax, colors='#9ca3af', linestyles='dotted', linewidth=2)
    ax.vlines(x=vt2_x, ymin=0, ymax=ymax, colors='#9ca3af', linestyles='dotted', linewidth=2)
    
    # Labels voor de drempels
    ax.text(vt1_x, ymax, " VT1 ", ha='center', va='bottom', fontsize=10, fontweight='bold', backgroundcolor='#1f2937', color='white')
    ax.text(vt2_x, ymax, " VT2 ", ha='center', va='bottom', fontsize=10, fontweight='bold', backgroundcolor='#1f2937', color='white')
    
    # --- HIER IS DE MAGIE: VERSCHILLENDE VLAKKEN PER MODEL ---
    
    if model_type == "3-Zone Model":
        # Zone 1 (Groen)
        ax.fill_between(x, y, where=(x <= vt1_x), color='#dcfce7', alpha=0.8)
        ax.text(20, 0.2, "ZONE 1\n(LOW)", ha='center', fontsize=10, fontweight='bold', color='#166534')
        
        # Zone 2 (Geel) - In 3-zone model is dit alles tussen vt1 en vt2
        ax.fill_between(x, y, where=((x > vt1_x) & (x <= vt2_x)), color='#fef9c3', alpha=0.8)
        ax.text(60, 0.5, "ZONE 2\n(MED)", ha='center', fontsize=10, fontweight='bold', color='#854d0e')
        
        # Zone 3 (Rood)
        ax.fill_between(x, y, where=(x > vt2_x), color='#fee2e2', alpha=0.8)
        ax.text(88, 2.0, "ZONE 3\n(HIGH)", ha='center', fontsize=10, fontweight='bold', color='#991b1b')
        
    elif model_type == "5-Zone Model":
        # We verdelen de ruimte voor VT1 in Z1 en Z2
        z1_limit = 25
        
        # Z1
        ax.fill_between(x, y, where=(x <= z1_limit), color='#dcfce7', alpha=0.9)
        ax.text(12, 0.2, "Z1", ha='center', fontsize=9, fontweight='bold', color='#166534')
        
        # Z2 (Tot VT1)
        ax.fill_between(x, y, where=((x > z1_limit) & (x <= vt1_x)), color='#ecfdf5', alpha=0.9)
        ax.text(35, 0.3, "Z2", ha='center', fontsize=9, fontweight='bold', color='#065f46')
        
        # Z3 (Begin van middenblok)
        z3_limit = 60
        ax.fill_between(x, y, where=((x > vt1_x) & (x <= z3_limit)), color='#fef9c3', alpha=0.9)
        ax.text(52, 0.6, "Z3", ha='center', fontsize=9, fontweight='bold', color='#854d0e')
        
        # Z4 (Tot VT2)
        ax.fill_between(x, y, where=((x > z3_limit) & (x <= vt2_x)), color='#ffedd5', alpha=0.9)
        ax.text(68, 1.0, "Z4", ha='center', fontsize=9, fontweight='bold', color='#9a3412')
        
        # Z5 (Boven VT2)
        ax.fill_between(x, y, where=(x > vt2_x), color='#fee2e2', alpha=0.9)
        ax.text(88, 2.5, "Z5", ha='center', fontsize=9, fontweight='bold', color='#991b1b')

    # As Labels
    ax.text(0, ymax/2, "LACTAAT", rotation=90, va='center', ha='right', color='#9ca3af', fontsize=8)
    ax.text(50, -0.2, "INTENSITEIT (WATTAGE)", ha='center', color='#9ca3af', fontsize=8)

    return fig

# -----------------------------------------------------------------------------
# 3. HEADER & MODEL SELECTIE
# -----------------------------------------------------------------------------

st.markdown("""
    <div class='header-title'>Master je <span class='header-accent'>Intensiteit.</span></div>
    <div class='header-sub'>Ontdek de fysiologische ankers achter je trainingszones.</div>
""", unsafe_allow_html=True)

# Tabs ipv Radio buttons voor een modernere look
col_spacer_l, col_select, col_spacer_r = st.columns([1, 2, 1])
with col_select:
    model_choice = st.radio("", ["3-Zone Model", "5-Zone Model"], horizontal=True, label_visibility="collapsed")

st.write("") 

# -----------------------------------------------------------------------------
# 4. BOVENKANT: GRAFIEK & UITLEG
# -----------------------------------------------------------------------------
col_graph, col_expl = st.columns([1.5, 1])

with col_graph:
    st.pyplot(draw_lactate_curve(model_choice))
    
    # Legenda onder grafiek
    c1, c2 = st.columns(2)
    with c1:
        st.info("**VT1 / Aerobe Drempel**\nJe kunt nog net praten.")
    with c2:
        st.error("**VT2 / Anaerobe Drempel**\nHet punt van verzuring.")

with col_expl:
    st.markdown(f"## *{model_choice.upper()}*")
    
    if model_choice == "3-Zone Model":
        st.write("Het klassieke 'gepolariseerde' model. Simpel en effectief.")
        st.success("**Zone 1 (Low):** Rust & Duur")
        st.warning("**Zone 2 (Med):** Tempo & Sweetspot")
        st.error("**Zone 3 (High):** Boven omslagpunt")
    else:
        st.write("Voor gedetailleerde sturing en specifieke prikkels.")
        st.success("**Z1/Z2:** Basis & Vetverbranding")
        st.warning("**Z3/Z4:** Tempo & Drempel")
        st.error("**Z5:** VO2Max & Sprint")

    st.markdown("""
    <div class="pro-tip-box" style="margin-top: 20px;">
        <p style="font-style: italic; font-size: 0.95rem;">
        "Train je drempels omhoog door er net onder te rijden, niet door er altijd overheen te gaan."
        </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# -----------------------------------------------------------------------------
# 5. ONDERKANT: INTERACTIEVE DETAILS
# -----------------------------------------------------------------------------

st.markdown("<h3 style='text-align: center; color: #9ca3af; letter-spacing: 2px; margin-bottom: 20px;'>ONTDEK ELKE ZONE</h3>", unsafe_allow_html=True)

# Data dictionary
zones_data = {
    "Zone 1": {
        "title": "ZONE 1: HERSTEL", "subtitle": "Herstel / Actief Herstel",
        "desc": "Heel rustig trappen. Praattempo: je kunt moeiteloos blijven praten. De focus ligt hier op doorbloeding.",
        "valkuil": "Te veel Z1 bouwt geen conditie op, maar is essentieel voor je volume.",
        "prikkels": ["Herstelcapaciteit", "Vetverbranding", "Capillarisatie"],
        "color_bg": "#dcfce7", "color_border": "#86efac", "color_accent": "#166534"
    },
    "Zone 2": {
        "title": "ZONE 2: BASIS", "subtitle": "Duur / Kalibreren met VT1",
        "desc": "De motorkamer. Onder VT1 train je de aerobe efficiëntie. Je voelt dat je werkt, maar kunt nog hele zinnen praten.",
        "valkuil": "Gevaar van de 'grijze zone': te hard voor Z2, te zacht voor echte kwaliteit.",
        "prikkels": ["Mitochondriale dichtheid", "Uithoudingsvermogen", "Vetmetabolisme"],
        "color_bg": "#ecfdf5", "color_border": "#a7f3d0", "color_accent": "#065f46"
    },
    "Zone 3": {
        "title": "ZONE 3: TEMPO", "subtitle": "Comfortabel Zwaar",
        "desc": "Stevig doorrijden. Korte zinnen lukken nog nét. Dit is vaak het tempo van een lange klim.",
        "valkuil": "Wordt snel de 'standaard' rit, waardoor je nooit écht uitrust of écht hard traint.",
        "prikkels": ["Mentale hardheid", "Spieruithoudingsvermogen", "Glycogeen opslag"],
        "color_bg": "#fef9c3", "color_border": "#fde047", "color_accent": "#854d0e"
    },
    "Zone 4": {
        "title": "ZONE 4: THRESHOLD", "subtitle": "Drempel / Rond VT2",
        "desc": "Hard. Praten is bijna onmogelijk. Dit zit rond je anaerobe drempel (FTP).",
        "valkuil": "Te vaak in Z4 leidt snel tot overtraining.",
        "prikkels": ["Lactaat tolerantie", "FTP verhoging", "Pacing"],
        "color_bg": "#ffedd5", "color_border": "#fdba74", "color_accent": "#9a3412"
    },
    "Zone 5": {
        "title": "ZONE 5: VO2 MAX", "subtitle": "Zeer Hard / Maximaal",
        "desc": "Alles geven. Je ventilatie is maximaal. Blokken zijn kort (3-8 min).",
        "valkuil": "Vraagt zeer veel hersteltijd. Alleen doen als je fris bent.",
        "prikkels": ["VO2 Max", "Anaerobe capaciteit", "Explosiviteit"],
        "color_bg": "#fee2e2", "color_border": "#fca5a5", "color_accent": "#991b1b"
    }
}

if 'selected_zone' not in st.session_state:
    st.session_state.selected_zone = "Zone 1"

def set_zone(z): st.session_state.selected_zone = z

# Buttons
cols = st.columns(5)
keys = list(zones_data.keys())
for i, col in enumerate(cols):
    with col:
        if st.button(keys[i], key=f"btn_{i}", use_container_width=True):
            set_zone(keys[i])

# Details weergeven
curr = zones_data[st.session_state.selected_zone]
c_left, c_right = st.columns([1.5, 1], gap="large")

with c_left:
    st.markdown(f"""
    <div class="zone-card" style="background-color: {curr['color_bg']}; border: 3px solid {curr['color_border']};">
        <h2 style="color: {curr['color_accent']}; margin:0; font-weight:900; font-style:italic;">{curr['title']}</h2>
        <h4 style="color: #6b7280; margin-top:5px;">{curr['subtitle']}</h4>
        <p style="margin-top: 15px; font-size: 1.1rem; line-height:1.6;">{curr['desc']}</p>
        <div class="valkuil-box">⚠️ {curr['valkuil']}</div>
    </div>
    """, unsafe_allow_html=True)

with c_right:
    items = "".join([f"<li>{p}</li>" for p in curr['prikkels']])
    st.markdown(f"""
    <div class="info-box">
        <strong style="color: #9ca3af; letter-spacing: 1px;">TRAININGSPRIKKELS</strong>
        <ul style="margin-top: 10px; padding-left: 20px;">{items}</ul>
    </div>
    <div class="pro-tip-box">
        <em>"Gebruik hartslag als controle, maar laat wattage leidend zijn."</em>
    </div>
    """, unsafe_allow_html=True)
