import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Energiesystemen en brandstof - SportMetrics",
    layout="wide",
)

HTML_PAGE = r"""
<!doctype html>
<html lang="nl">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Energiesystemen en brandstof - SportMetrics</title>
  <style>
    @import url("https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Spectral:wght@400;600&display=swap");

    :root {
      --sand: #f6f1ea;
      --clay: #e9ddd2;
      --ink: #1e2a2f;
      --muted: #5c6b73;
      --sea: #2f7c85;
      --deep: #0f4c5c;
      --sun: #f4b66a;
      --peach: #f1c9a9;
      --card: rgba(255, 255, 255, 0.82);
      --border: rgba(30, 42, 47, 0.12);
      --shadow: 0 18px 50px rgba(15, 76, 92, 0.18);
    }

    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      font-family: "Spectral", "Times New Roman", serif;
      color: var(--ink);
      background: radial-gradient(1200px 800px at 10% -10%, #ffffff 0%, var(--sand) 60%, var(--clay) 100%);
    }

    .bg-shape {
      position: fixed;
      inset: auto;
      width: 480px;
      height: 480px;
      border-radius: 50%;
      background: radial-gradient(circle at 30% 30%, rgba(47, 124, 133, 0.28), rgba(47, 124, 133, 0.02));
      z-index: 0;
    }
    .bg-shape.one { top: -120px; right: -120px; }
    .bg-shape.two { bottom: -200px; left: -140px; background: radial-gradient(circle, rgba(244, 182, 106, 0.35), rgba(244, 182, 106, 0.02)); }

    nav {
      position: fixed;
      top: 28px;
      right: 26px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      background: rgba(255, 255, 255, 0.7);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 14px 14px;
      box-shadow: var(--shadow);
      z-index: 3;
      max-width: 190px;
    }
    nav h4 {
      margin: 0 0 6px;
      font-family: "Space Grotesk", sans-serif;
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--muted);
    }
    .nav-link {
      font-family: "Space Grotesk", sans-serif;
      font-size: 13px;
      text-decoration: none;
      color: var(--muted);
      display: flex;
      gap: 6px;
      align-items: center;
      transition: color 0.2s ease;
    }
    .nav-link span {
      display: inline-block;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--clay);
      border: 1px solid var(--border);
    }
    .nav-link.active { color: var(--deep); font-weight: 600; }
    .nav-link.active span { background: var(--sea); border-color: var(--sea); }

    .progress {
      height: 6px;
      background: rgba(47, 124, 133, 0.12);
      border-radius: 999px;
      overflow: hidden;
      margin-top: 6px;
    }
    .progress span { display: block; height: 100%; width: 0%; background: var(--sea); transition: width 0.2s ease; }

    main {
      position: relative;
      z-index: 1;
      max-width: 1100px;
      margin: 0 auto;
      padding: 64px 24px 120px;
    }

    section {
      margin: 0 0 72px;
      padding: 36px;
      border-radius: 26px;
      background: var(--card);
      box-shadow: var(--shadow);
      border: 1px solid var(--border);
      transition: all 0.7s ease;
    }
    body.enable-animations section { opacity: 0; transform: translateY(20px); }
    body.enable-animations section.in-view { opacity: 1; transform: translateY(0); }

    .hero {
      padding: 54px 44px;
      background: linear-gradient(140deg, rgba(255, 255, 255, 0.92), rgba(241, 201, 169, 0.55));
    }
    .hero h1 {
      font-family: "Space Grotesk", sans-serif;
      font-size: clamp(2.2rem, 3.4vw, 3.4rem);
      margin: 0 0 12px;
      color: var(--deep);
    }
    .hero p {
      font-size: 1.05rem;
      color: var(--muted);
      margin: 0;
      max-width: 720px;
    }
    .hero .hero-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 18px;
      margin-top: 28px;
    }
    .hero .stat {
      padding: 16px 18px;
      background: rgba(255, 255, 255, 0.7);
      border-radius: 16px;
      border: 1px solid var(--border);
      font-family: "Space Grotesk", sans-serif;
      font-size: 0.95rem;
      color: var(--muted);
    }
    .hero .stat strong { display: block; color: var(--deep); font-size: 1.1rem; }

    h2 {
      font-family: "Space Grotesk", sans-serif;
      margin: 0 0 12px;
      color: var(--deep);
      font-size: 1.8rem;
    }
    h3 {
      font-family: "Space Grotesk", sans-serif;
      margin: 0 0 8px;
      color: var(--deep);
    }
    p { margin: 0 0 14px; color: var(--ink); line-height: 1.55; }
    .muted { color: var(--muted); }

    .grid-3 {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 18px;
    }
    .card {
      background: rgba(255, 255, 255, 0.86);
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 16px 18px;
    }
    .pill {
      display: inline-block;
      font-family: "Space Grotesk", sans-serif;
      font-size: 0.72rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--muted);
      border: 1px solid var(--border);
      padding: 4px 10px;
      border-radius: 999px;
      margin-bottom: 10px;
    }

    .timeline {
      display: grid;
      grid-template-columns: repeat(3, minmax(120px, 1fr));
      gap: 12px;
      margin-top: 12px;
    }
    .timeline .slot {
      padding: 10px;
      border-radius: 14px;
      background: rgba(47, 124, 133, 0.08);
      border: 1px solid rgba(47, 124, 133, 0.16);
      font-family: "Space Grotesk", sans-serif;
      font-size: 0.85rem;
    }

    .mixer {
      margin-top: 18px;
      padding: 18px;
      border-radius: 18px;
      border: 1px dashed rgba(47, 124, 133, 0.4);
      background: rgba(47, 124, 133, 0.06);
    }
    .mixer label {
      font-family: "Space Grotesk", sans-serif;
      font-size: 0.9rem;
    }
    .mixer input[type="range"] { width: 100%; margin: 10px 0 6px; }
    .mix-row {
      display: grid;
      grid-template-columns: 130px 1fr 54px;
      gap: 12px;
      align-items: center;
      margin: 10px 0;
      font-family: "Space Grotesk", sans-serif;
      font-size: 0.85rem;
    }
    .mix-bar {
      background: rgba(15, 76, 92, 0.08);
      border-radius: 999px;
      overflow: hidden;
      height: 10px;
      border: 1px solid rgba(15, 76, 92, 0.2);
    }
    .mix-bar span {
      display: block;
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, var(--sea), var(--deep));
      border-radius: 999px;
      transition: width 0.3s ease;
    }
    .mix-value { text-align: right; color: var(--muted); }

    .fuel-row .mix-bar span { background: linear-gradient(90deg, var(--sun), var(--deep)); }

    .callout {
      background: rgba(244, 182, 106, 0.18);
      border: 1px solid rgba(244, 182, 106, 0.45);
      padding: 16px 18px;
      border-radius: 18px;
      font-family: "Space Grotesk", sans-serif;
    }

    .zone-picker {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin: 12px 0 18px;
    }
    .zone-btn {
      border: 1px solid var(--border);
      background: rgba(255, 255, 255, 0.9);
      font-family: "Space Grotesk", sans-serif;
      padding: 8px 14px;
      border-radius: 999px;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .zone-btn.active { background: var(--deep); color: #fff; border-color: var(--deep); }
    .zone-panel { display: none; }
    .zone-panel.active { display: block; }

    .summary {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;
      margin-top: 18px;
    }

    .footer {
      text-align: center;
      font-family: "Space Grotesk", sans-serif;
      font-size: 0.9rem;
      color: var(--muted);
    }

    @media (max-width: 980px) {
      nav { display: none; }
      section { padding: 28px; }
      .mix-row { grid-template-columns: 110px 1fr 48px; }
    }

    @media (max-width: 720px) {
      main { padding: 40px 16px 90px; }
      section { padding: 22px; margin: 0 0 48px; }
      .hero { padding: 30px 22px; }
      .hero h1 { font-size: clamp(1.8rem, 6vw, 2.4rem); }
      .hero .hero-grid { grid-template-columns: 1fr; }
      .timeline { grid-template-columns: 1fr; }
      .grid-3 { grid-template-columns: 1fr; }
      .summary { grid-template-columns: 1fr; }
      .mix-row { grid-template-columns: 1fr; gap: 6px; }
      .mix-value { text-align: left; }
      .zone-picker { gap: 8px; }
      .zone-btn { width: 100%; text-align: center; }
    }

    @media (prefers-reduced-motion: reduce) {
      * { scroll-behavior: auto; }
      section { transition: none; }
      body.enable-animations section { opacity: 1; transform: none; }
    }
  </style>
</head>
<body>
  <div class="bg-shape one"></div>
  <div class="bg-shape two"></div>

  <nav aria-label="Navigatie">
    <h4>Route</h4>
    <a class="nav-link" href="#intro" data-section="intro"><span></span>Intro</a>
    <a class="nav-link" href="#atp" data-section="atp"><span></span>ATP</a>
    <a class="nav-link" href="#routes" data-section="routes"><span></span>Routes</a>
    <a class="nav-link" href="#pcr" data-section="pcr"><span></span>ATP-PCr</a>
    <a class="nav-link" href="#anaerobe" data-section="anaerobe"><span></span>Anaerobe</a>
    <a class="nav-link" href="#aerobe" data-section="aerobe"><span></span>Aerobe</a>
    <a class="nav-link" href="#zones" data-section="zones"><span></span>Zones</a>
    <a class="nav-link" href="#samenvatting" data-section="samenvatting"><span></span>Samenvatting</a>
    <div class="progress"><span id="progress-bar"></span></div>
  </nav>

  <main>
    <section id="intro" class="hero" data-title="Intro">
      <span class="pill">Energiesystemen en brandstof</span>
      <h1>Energiesystemen en brandstof: hoe je lichaam vermogen maakt</h1>
      <p>Inspanning is geen "een systeem aan". Je lichaam levert ATP via meerdere routes tegelijk. Wat verandert is de verdeling tussen die routes, afhankelijk van intensiteit, duur, trainingstoestand en brandstofvoorraad.</p>
      <div class="hero-grid">
        <div class="stat"><strong>ATP is de valuta</strong>Elke spiercontractie betaal je met ATP. Je voorraad is klein, dus je maakt het continu opnieuw.</div>
        <div class="stat"><strong>Power vs capaciteit</strong>Hoe hoger de intensiteit, hoe sneller je ATP nodig hebt. Dat duwt je naar routes met hoge power.</div>
        <div class="stat"><strong>Continuum</strong>Er zijn geen harde knips. Alle routes draaien altijd mee, maar de dominantie schuift.</div>
      </div>
    </section>

    <section id="atp" data-title="ATP">
      <h2>ATP als energievaluta</h2>
      <p>Omdat je soms direct maximale power nodig hebt (sprint) en soms lang en laag (duur), bestaan er meerdere routes met verschillende power en capaciteit. De power-capacity trade-off verklaart vrijwel alles in training.</p>
      <div class="timeline">
        <div class="slot">Hoge intensiteit = hoge ATP vraag per seconde</div>
        <div class="slot">Dominantie schuift naar snellere ATP levering</div>
        <div class="slot">Langere duur vraagt om duurzame routes</div>
      </div>
      <div class="mixer" aria-live="polite">
        <label for="intensity">Sleep: intensiteit</label>
        <input id="intensity" type="range" min="0" max="100" value="35" />
        <div class="mix-row">
          <div>ATP-PCr</div>
          <div class="mix-bar"><span id="mix-pcr"></span></div>
          <div class="mix-value" id="mix-pcr-value">0%</div>
        </div>
        <div class="mix-row">
          <div>Anaerobe</div>
          <div class="mix-bar"><span id="mix-anaer"></span></div>
          <div class="mix-value" id="mix-anaer-value">0%</div>
        </div>
        <div class="mix-row">
          <div>Aerobe</div>
          <div class="mix-bar"><span id="mix-aero"></span></div>
          <div class="mix-value" id="mix-aero-value">0%</div>
        </div>
      </div>
    </section>

    <section id="routes" data-title="Routes">
      <h2>De drie hoofd routes (parallel + continu)</h2>
      <div class="grid-3">
        <div class="card">
          <span class="pill">ATP-PCr (alactisch)</span>
          <p><strong>Bron:</strong> fosfocreatine (PCr)</p>
          <p><strong>Dominant venster:</strong> 0-10(15) sec bij maximale inspanning</p>
          <p><strong>Begrenzing:</strong> PCr voorraad is klein en snel leeg</p>
        </div>
        <div class="card">
          <span class="pill">Anaerobe glycolyse</span>
          <p><strong>Substraat:</strong> koolhydraat</p>
          <p><strong>Dominant venster:</strong> 15 sec tot 2-3 min</p>
          <p><strong>Begrenzing:</strong> systeemstress (ionen/H+) en tolerantie</p>
        </div>
        <div class="card">
          <span class="pill">Aerobe oxidatie</span>
          <p><strong>Substraat:</strong> koolhydraat + vet</p>
          <p><strong>Dominant venster:</strong> minuten tot uren</p>
          <p><strong>Begrenzing:</strong> VO2 plafond bij hoge intensiteit en glycogeen bij lange duur</p>
        </div>
      </div>
      <p class="muted">Continuum: alle routes dragen altijd iets bij. Met stijgende intensiteit schuift de dominantie richting routes met hogere ATP productie.</p>
    </section>

    <section id="pcr" data-title="ATP-PCr">
      <h2>ATP-PCr: instant power en waarom herhalingen pijn doen</h2>
      <p>ATP-PCr levert acceleratie en sprintvermogen. PCr buffert de eerste seconden tot tientallen seconden. Maar PCr raakt snel beperkt en herstel kost tijd. Daarom zakt het vermogen bij herhaalde sprints, zelfs als motivatie hoog is.</p>
      <div class="callout">
        Praktisch: bij maximale inspanning wordt PCr vaak binnen 10-15 sec limiterend. Bijna volledig herstel duurt meestal enkele minuten, afhankelijk van herstelintensiteit.
      </div>
    </section>

    <section id="anaerobe" data-title="Anaerobe">
      <h2>Anaerobe koolhydraatafbraak en lactaat</h2>
      <p>Deze route levert snel ATP uit koolhydraten en wordt belangrijk zodra de ATP vraag per seconde hoog wordt. De keerzijde is dat systeemstress snel oploopt (o.a. H+ en ionen), waardoor prestatie en duurzaamheid dalen.</p>
      <div class="grid-3">
        <div class="card">
          <h3>Lactaat is geen afval</h3>
          <p>Lactaat is een transportvorm van energie en kan later weer worden geoxideerd. Denk aan lactate shuttle in andere spiervezels en de hartspier.</p>
        </div>
        <div class="card">
          <h3>Waar het mis gaat</h3>
          <p>Probleem ontstaat wanneer productie en stress sneller stijgen dan oxidatieve verwerking. Dan nemen drift en onhoudbaarheid toe.</p>
        </div>
        <div class="card">
          <h3>Praktisch venster</h3>
          <p>Typisch tientallen seconden tot enkele minuten hard werken. Daarna zie je vaak vermogensval en sterke adem- of HR-drift.</p>
        </div>
      </div>
    </section>

    <section id="aerobe" data-title="Aerobe">
      <h2>Aerobe oxidatie en substraten</h2>
      <p>De aerobe motor is je duurzame ATP fabriek. Je verbrandt altijd een mix van koolhydraat en vet. Naarmate intensiteit stijgt wordt koolhydraat relatief dominanter, omdat vetoxidatie de gevraagde ATP snelheid minder goed kan bijbenen.</p>
      <div class="mixer" aria-live="polite">
        <label for="fuel">Sleep: intensiteit en brandstofmix</label>
        <input id="fuel" type="range" min="0" max="100" value="35" />
        <div class="mix-row fuel-row">
          <div>Koolhydraat</div>
          <div class="mix-bar"><span id="mix-carb"></span></div>
          <div class="mix-value" id="mix-carb-value">0%</div>
        </div>
        <div class="mix-row fuel-row">
          <div>Vet</div>
          <div class="mix-bar"><span id="mix-fat"></span></div>
          <div class="mix-value" id="mix-fat-value">0%</div>
        </div>
      </div>
      <div class="summary">
        <div class="card">
          <h3>Glycogeen als limiter</h3>
          <p>Aerobe koolhydraatverbranding kan stevige intensiteit lang ondersteunen, maar bij lange duur wordt vaak glycogeen limiterend. Richtlijn: 60-120 min bij stevige belasting, afhankelijk van voeding, pacing en training.</p>
        </div>
        <div class="card">
          <h3>Vet als voorraad</h3>
          <p>Vetvoorraad raakt zelden op. Het is vooral bruikbaar bij lage tot matige intensiteit waar de ATP vraag lager is.</p>
        </div>
        <div class="card">
          <h3>FatMax context</h3>
          <p>FatMax is een piek in vetoxidatie, geen vet-only zone. De mix verschuift, niet de aanwezigheid van vet.</p>
        </div>
      </div>
    </section>

    <section id="zones" data-title="Zones">
      <h2>Koppeling naar zones en SportMetrics</h2>
      <p>Zone modellen zijn de praktische vertaalslag van het energiesysteem. SportMetrics koppelt vermogen, hartslag, ademrespons en VO2 om jouw drempelgebieden en aerobe plafond te positioneren. We gebruiken de test om intensiteitsdomeinen en zone-ankers te bepalen die direct naar training vertaalbaar zijn.</p>
      <div class="callout">SportMetrics doet geen lactaatmetingen (prikken), alleen ademgasanalyse.</div>
      <div class="zone-picker" role="tablist" aria-label="Zones">
        <button class="zone-btn active" data-zone="vt1" role="tab">Rond VT1</button>
        <button class="zone-btn" data-zone="vt2" role="tab">Richting VT2/CP</button>
        <button class="zone-btn" data-zone="above" role="tab">Boven VT2/CP</button>
      </div>
      <div class="zone-panel active" id="zone-vt1" role="tabpanel">
        <p>Overwegend aerobe dominantie. Stabieler, zuinig en geschikt voor veel volume.</p>
      </div>
      <div class="zone-panel" id="zone-vt2" role="tabpanel">
        <p>Hogere ATP vraag, meer koolhydraat en glycolytische druk. Meer drift en hogere herstelkosten.</p>
      </div>
      <div class="zone-panel" id="zone-above" role="tabpanel">
        <p>Geen echte steady state. Tijd op beperkte capaciteit, hoge systeemstress.</p>
      </div>
    </section>

    <section id="samenvatting" data-title="Samenvatting">
      <h2> Samenvatting</h2>
      <p>Elke beweging betaal je met ATP. Omdat je ATP voorraad klein is, moet je lichaam het continu bijmaken via meerdere routes die parallel draaien. Het is een continuum: er zijn geen harde afkappunten, maar wel een verschuiving in dominantie wanneer de ATP vraag per seconde stijgt. PCr levert instant power (kort), anaerobe koolhydraatafbraak levert snel ATP (beperkt houdbaar, hogere systeemstress) en aerobe oxidatie levert duurzame energie uit koolhydraat en vet (vet: enorme voorraad, maar lagere maximale ATP snelheid). Lactaat is geen afval, maar een transportvorm van energie die later weer kan worden geoxideerd (o.a. spier en hart).</p>
      <p>Zone modellen zijn de praktische kaart: rond VT1 stabiel en zuinig, richting VT2/CP nemen drift en herstelkosten toe, en daarboven kom je in een domein zonder echte steady state.</p>
      <p class="footer">Tot snel bij sportmetrics!.</p>
    </section>
  </main>

  <script>
    document.body.classList.add("enable-animations");

    const sections = Array.from(document.querySelectorAll("section[data-title]"));
    const navLinks = Array.from(document.querySelectorAll(".nav-link"));
    const progressBar = document.getElementById("progress-bar");

    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("in-view");
        }
      });
    }, { threshold: 0.2 });

    sections.forEach((section) => revealObserver.observe(section));

    const spyObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          navLinks.forEach((link) => link.classList.toggle("active", link.dataset.section === entry.target.id));
        }
      });
    }, { threshold: 0.55 });

    sections.forEach((section) => spyObserver.observe(section));

    window.addEventListener("scroll", () => {
      const doc = document.documentElement;
      const scrollTop = doc.scrollTop || document.body.scrollTop;
      const scrollHeight = doc.scrollHeight - doc.clientHeight;
      const progress = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
      progressBar.style.width = `${progress}%`;
    });

    const intensity = document.getElementById("intensity");
    const fuel = document.getElementById("fuel");

    function normalize(values) {
      const sum = values.reduce((acc, val) => acc + val, 0) || 1;
      return values.map((val) => val / sum);
    }

    function systemMix(value) {
      const pcr = Math.max(0, (value - 70) / 30);
      const anaer = Math.max(0, 1 - Math.abs(value - 60) / 30);
      const aero = Math.max(0, (70 - value) / 70);
      const [p, a, e] = normalize([pcr, anaer, aero]);
      return { p, a, e };
    }

    function updateMix() {
      const value = parseInt(intensity.value, 10);
      const { p, a, e } = systemMix(value);
      document.getElementById("mix-pcr").style.width = `${Math.round(p * 100)}%`;
      document.getElementById("mix-anaer").style.width = `${Math.round(a * 100)}%`;
      document.getElementById("mix-aero").style.width = `${Math.round(e * 100)}%`;
      document.getElementById("mix-pcr-value").textContent = `${Math.round(p * 100)}%`;
      document.getElementById("mix-anaer-value").textContent = `${Math.round(a * 100)}%`;
      document.getElementById("mix-aero-value").textContent = `${Math.round(e * 100)}%`;
    }

    function updateFuel() {
      const value = parseInt(fuel.value, 10);
      const carb = Math.min(1, Math.max(0, value / 100));
      const fat = 1 - carb;
      document.getElementById("mix-carb").style.width = `${Math.round(carb * 100)}%`;
      document.getElementById("mix-fat").style.width = `${Math.round(fat * 100)}%`;
      document.getElementById("mix-carb-value").textContent = `${Math.round(carb * 100)}%`;
      document.getElementById("mix-fat-value").textContent = `${Math.round(fat * 100)}%`;
    }

    intensity.addEventListener("input", updateMix);
    fuel.addEventListener("input", updateFuel);
    updateMix();
    updateFuel();

    const zoneButtons = Array.from(document.querySelectorAll(".zone-btn"));
    const zonePanels = {
      vt1: document.getElementById("zone-vt1"),
      vt2: document.getElementById("zone-vt2"),
      above: document.getElementById("zone-above")
    };

    zoneButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const target = button.dataset.zone;
        zoneButtons.forEach((btn) => btn.classList.toggle("active", btn === button));
        Object.entries(zonePanels).forEach(([key, panel]) => {
          panel.classList.toggle("active", key === target);
        });
      });
    });
  </script>
</body>
</html>
"""

components.html(HTML_PAGE, height=4200, scrolling=True)
