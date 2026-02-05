import streamlit as st

# -----------------------------------------------------------------------------
# 1. CONFIGURATIE & DATA
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Zone Explorer", layout="wide")

# Hier definiëren we alle tekst en kleuren uit jouw screenshots in een dictionary
zones_data = {
    "Zone 1": {
        "title": "ZONE 1: HERSTEL",
        "subtitle": "Herstel / Actief Herstel",
        "desc": "Heel rustig trappen. Praattempo: je kunt moeiteloos blijven praten. De focus ligt hier op doorbloeding en het 'spoelen' van de benen zonder metabole stress.",
        "valkuil": "Te veel Z1 bouwt geen conditie op, maar is essentieel voor je volume.",
        "prikkels": ["Ideaal na zware intervaldagen", "Verbeter herstelcapaciteit", "Houd ademhaling laag"],
        "color_bg": "#dcfce7",  # Mint groen
        "color_border": "#86efac",
        "color_accent": "#166534"
    },
    "Zone 2": {
        "title": "ZONE 2: AEROBE BASIS",
        "subtitle": "Duur / Kalibreren met VT1",
        "desc": "Dit is de motorkamer. Onder VT1 train je de aerobe efficiëntie en vetverbranding. Je voelt dat je werkt, maar kunt nog hele zinnen praten.",
        "valkuil": "Gevaar van de 'grijze zone': te hard voor Z2, te zacht voor echte kwaliteit.",
        "prikkels": ["Bulk van je training", "Verhoogt mitochondriale dichtheid", "Lage herstelkosten"],
        "color_bg": "#ecfdf5",  # Licht groen
        "color_border": "#a7f3d0",
        "color_accent": "#065f46"
    },
    "Zone 3": {
        "title": "ZONE 3: TEMPO",
        "subtitle": "Comfortabel Zwaar",
        "desc": "Stevig doorrijden. Korte zinnen lukken nog nét. Dit is vaak het tempo van een Gran Fondo of lange klim. De herstelkosten beginnen hier op te lopen.",
        "valkuil": "Wordt snel de 'standaard' rit, waardoor je nooit écht uitrust of écht hard traint.",
        "prikkels": ["Mentale tolerantie", "Specifiek tempo-duur", "Dieselvermogen"],
        "color_bg": "#fef9c3",  # Geel
        "color_border": "#fde047",
        "color_accent": "#854d0e"
    },
    "Zone 4": {
        "title": "ZONE 4: THRESHOLD",
        "subtitle": "Drempel / Rond VT2",
        "desc": "Hard. Praten is bijna onmogelijk. Dit zit rond je anaerobe drempel. Essentieel voor het verhogen van je FTP/Drempelvermogen.",
        "valkuil": "Te vaak in Z4 leidt snel tot overtraining en chronische vermoeidheid.",
        "prikkels": ["Verhoogt anaerobe drempel", "Lactaat tolerantie", "Pacing vaardigheden"],
        "color_bg": "#ffedd5",  # Oranje/Zand
        "color_border": "#fdba74",
        "color_accent": "#9a3412"
    },
    "Zone 5": {
        "title": "ZONE 5: VO2 MAX",
        "subtitle": "Zeer Hard / Maximaal",
        "desc": "Alles geven. Je ventilatie is maximaal. Blokken zijn kort (3-8 min). Bedoeld om je aerobe plafond (VO2 Max) te verhogen.",
        "valkuil": "Vraagt zeer veel hersteltijd. Alleen doen als je fris bent.",
        "prikkels": ["Verhoogt aerobe plafond", "Klim-attacks oefenen", "Top-end vermogen"],
        "color_bg": "#fee2e2",  # Rood/Roze
        "color_border": "#fca5a5",
        "color_accent": "#991b1b"
    }
}

# -----------------------------------------------------------------------------
# 2. STATE MANAGEMENT (Welke knop is ingedrukt?)
# -----------------------------------------------------------------------------
if 'selected_zone' not in st.session_state:
    st.session_state.selected_zone = "Zone 1"

def set_zone(zone_name):
    st.session_state.selected_zone = zone_name

# -----------------------------------------------------------------------------
# 3. STYLING (CSS)
# -----------------------------------------------------------------------------
# Dit stukje CSS zorgt ervoor dat het eruit ziet als de screenshots (kaarten, schaduwen, kleuren)
st.markdown("""
<style>
    /* Algemene styling */
    .block-container {padding-top: 2rem;}
    
    /* De zone kaart links */
    .zone-card {
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        height: 100%;
        color: #1f2937;
    }
    .zone-title {
        font-family: 'Helvetica', sans-serif;
        font-weight: 800;
        font-size: 40px;
        font-style: italic;
        margin-bottom: 5px;
    }
    .zone-subtitle {
        font-weight: 700;
        font-size: 20px;
        color: #6b7280;
        margin-bottom: 20px;
    }
    .valkuil-box {
        background-color: rgba(0,0,0,0.05);
        border: 1px solid rgba(0,0,0,0.1);
        padding: 15px;
        border-radius: 10px;
        margin-top: 30px;
        font-size: 0.9rem;
        font-style: italic;
        font-weight: 600;
    }
    
    /* De rechterkant (Prikkels & Pro Tip) */
    .info-box {
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .pro-tip-box {
        background-color: #111827; /* Donkerblauw/Zwart */
        color: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    .stButton button {
        border-radius: 20px;
        border: 1px solid #e5e7eb;
        background-color: white;
        font-weight: bold;
        width: 100%;
    }
    .stButton button:hover {
        border-color: #3b82f6;
        color: #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. DE LAYOUT
# -----------------------------------------------------------------------------

st.markdown("<h1 style='text-align: center; color: #374151;'>ONTDEK ELKE ZONE</h1>", unsafe_allow_html=True)
st.write("") # Spacer

# --- De Interactieve Knoppen ---
cols = st.columns(5)
zones_list = list(zones_data.keys())

for i, zone_name in enumerate(zones_list):
    with cols[i]:
        # Als de knop wordt ingedrukt, update de session state
        if st.button(zone_name.upper(), use_container_width=True):
            set_zone(zone_name)
            st.rerun()

st.write("---") # Scheidingslijn

# Haal de data op voor de geselecteerde zone
current_data = zones_data[st.session_state.selected_zone]

# --- De Content Sectie ---
col_left, col_right = st.columns([1, 1])

with col_left:
    # We gebruiken f-strings om de CSS kleuren dynamisch in te vullen
    st.markdown(f"""
    <div class="zone-card" style="background-color: {current_data['color_bg']}; border: 2px solid {current_data['color_border']};">
        <div class="zone-title" style="color: {current_data['color_accent']}">{current_data['title']}</div>
        <div class="zone-subtitle">{current_data['subtitle']}</div>
        <p style="font-size: 1.1rem; line-height: 1.6;">{current_data['desc']}</p>
        
        <div class="valkuil-box">
            BELANGRIJKE VALKUIL:<br>
            "{current_data['valkuil']}"
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    # Trainingsprikkels Box
    prikkels_html = "".join([f"<li style='margin-bottom: 10px;'><b>{p}</b></li>" for p in current_data['prikkels']])
    
    st.markdown(f"""
    <div class="info-box">
        <h5 style="color: #9ca3af; letter-spacing: 1px; font-size: 0.8rem; font-weight: 800; margin-bottom: 20px;">TRAININGSPRIKKELS</h5>
        <ul style="list-style-type: disc; padding-left: 20px; color: #1f2937;">
            {prikkels_html}
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Context Pro Tip Box (Donker)
    st.markdown("""
    <div class="pro-tip-box">
        <h5 style="color: #6b7280; letter-spacing: 1px; font-size: 0.8rem; font-weight: 800; margin-bottom: 15px;">CONTEXT PRO TIP</h5>
        <p style="font-style: italic; font-size: 1rem; line-height: 1.5;">
        "Gebruik hartslag als controle, maar laat wattage leidend zijn voor de meest constante prikkel in deze zone."
        </p>
    </div>
    """, unsafe_allow_html=True)
