import streamlit as st
import plotly.graph_objects as go
import numpy as np
from PIL import Image
import os

# Pagina configuratie
st.set_page_config(page_title="Physiological Zone Explorer", layout="wide")

# --- LOGO TOEVOEGEN ---
# Zorg dat de bestandsnaam EXACT overeenkomt met wat je op GitHub uploadt (hoofdlettergevoelig!)
logo_path = "logo.png"  # Verander dit naar jouw bestandsnaam, bijv: 'bedrijfslogo.jpg'

if os.path.exists(logo_path):
    # Optie 1: Logo in de zijbalk (meest gebruikelijk)
    st.sidebar.image(logo_path, width=200) 
    
    # Optie 2: Logo bovenaan de hoofdpagina (haal commentaar weg om te gebruiken)
    # st.image(logo_path, width=150)
else:
    # Fallback als het logo nog niet is geüpload
    st.sidebar.write("Upload 'logo.png' naar GitHub om het hier te zien.")
# ----------------------

st.title("Zone Explorer")
st.subheader("Train op Fysiologie, niet op gevoel")

# 1. Data genereren voor de curves (simulatie van fysiologische data)
x = np.linspace(0, 100, 100)
fat_max = 40 * np.exp(-((x - 30)**2) / 400) # Vetverbranding curve
carb_burn = 2 * np.exp(x / 25)              # Koolhydraat/Lactaat curve

# 2. Zone definities
zones = {
    "Zone 1: Herstel": {"range": [0, 20], "color": "#d1f2eb", "desc": "Focus op vetverbranding en herstel. Lage intensiteit."},
    "Zone 2: Aerobe Basis": {"range": [20, 45], "color": "#a9dfbf", "desc": "Optimale vetverbranding. Duurvermogen opbouwen."},
    "Zone 3: Tempo": {"range": [45, 70], "color": "#f9e79f", "desc": "Overgangszone. Mix van vetten en koolhydraten."},
    "Zone 4: Threshold": {"range": [70, 85], "color": "#fbcbb2", "desc": "Omslagpunt. Hoge koolhydraatverbranding."},
    "Zone 5: VO2Max": {"range": [85, 100], "color": "#f5b7b1", "desc": "Maximale zuurstofopname. Zeer hoge intensiteit."}
}

# 3. Streamlit Interface: Selectie van de zone
# We verplaatsen de controls ook vaak naar de sidebar voor een schoner dashboard, 
# maar hier laten we hem staan zoals jij had, of we zetten hem onder het logo:
selected_zone_name = st.sidebar.select_slider(
    "Selecteer een trainingszone:",
    options=list(zones.keys())
)

# 4. Grafiek maken met Plotly
fig = go.Figure()

# Achtergrondvlakken voor zones toevoegen
for name, info in zones.items():
    fig.add_vrect(
        x0=info["range"][0], x1=info["range"][1],
        fillcolor=info["color"], opacity=0.3,
        layer="below", line_width=0,
    )

# De curves tekenen
fig.add_trace(go.Scatter(x=x, y=fat_max, name="Vetverbranding", line=dict(color='green', width=3)))
fig.add_trace(go.Scatter(x=x, y=carb_burn, name="Koolhydraatverbruik / Lactaat", line=dict(color='red', width=3)))

# Markering voor geselecteerde zone
current_range = zones[selected_zone_name]["range"]
fig.add_vrect(x0=current_range[0], x1=current_range[1], line_width=2, line_color="black", fillcolor="black", opacity=0.1)

fig.update_layout(
    xaxis_title="Intensiteit (% VO2Max / Vermogen)",
    yaxis_title="Metabole Respons",
    showlegend=True,
    height=500
)

# 5. Output weergeven
st.plotly_chart(fig, use_container_width=True)

st.info(f"**{selected_zone_name}**\n\n{zones[selected_zone_name]['desc']}")

# Extra toelichting zoals in de video
col1, col2 = st.columns(2)
with col1:
    st.write("**Metabole Focus**")
    st.write("- Efficiëntie van vetzuuroptimalisatie")
with col2:
    st.write("**Trainingsdoel**")
    st.write("- Verhoging van de aerobe drempel")
