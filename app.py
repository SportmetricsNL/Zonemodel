import React, { useState, useMemo, useEffect } from 'react';
import { 
  AreaChart, Area, XAxis, YAxis, 
  CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine, Label 
} from 'recharts';
import { 
  Zap, 
  Activity, 
  Target, 
  AlertTriangle, 
  Info, 
  ChevronRight,
  TrendingUp,
  Wind,
  Layers,
  BookOpen,
  Bike, // Gecorrigeerd: 'Bike' in plaats van 'Bicycle'
  CheckCircle2
} from 'lucide-react';

const App = () => {
  const [modelType, setModelType] = useState('5-Zone Model');
  const [selectedZone, setSelectedZone] = useState('Zone 1');

  // Fysiologische ankers (gekalibreerd op % intensiteit/wattage)
  const vt1 = 48; // Eerste ventilatoire omslag
  const vt2 = 78; // Tweede ventilatoire omslag

  // Data voor het 3-Zone Model (Fysiologische basis)
  const zones3 = {
    "Zone 1": {
      title: "ZONE 1 (LOW)",
      subtitle: "Onder VT1 - Stabiele Ademhaling",
      theory: "De basis van elke training. Je ademhaling blijft laag en stabiel. Je gebruikt hoofdzakelijk vetten en de interne belasting is minimaal.",
      bullets: [
        "Easy écht easy houden",
        "Basisdomein voor vetverbranding",
        "Minimale metabole stress"
      ],
      prikkels: ["Capillarisatie", "Mitochondriale efficiëntie", "Basisvolume"],
      doelen: ["Vetverbranding optimaliseren", "Herstel bevorderen", "Basisconditie"],
      voorbeelden: ["60-90 min herstelrit", "Warming-up"],
      takeaway: "Zones = doseren op fysiologie, niet op gevoel alleen.",
      colorClass: "emerald",
      sidebarLabel: "LOW"
    },
    "Zone 2": {
      title: "ZONE 2 (TEMPO)",
      subtitle: "Tussen VT1 & VT2 - Verhoogde Ventilatie",
      theory: "Het overgangsgebied. Ademarbeid stijgt merkbaar. Je kunt nog praten, maar in kortere zinnen. Herstelkosten lopen op.",
      bullets: [
        "Comfortabel zwaar tempo",
        "Dieselvermogen opbouwen",
        "Mentale tolerantie voor inspanning"
      ],
      prikkels: ["Tempo-uithoudingsvermogen", "Race-gevoel", "Koolhydraat-mix efficiëntie"],
      doelen: ["Gran fondo tempo", "Lange solo's", "Specifieke race pace"],
      voorbeelden: ["2x20 min tempo", "Lange klim steady"],
      takeaway: "VT1 & VT2 zijn je fysiologische ankers voor zones.",
      colorClass: "orange",
      sidebarLabel: "THRESH"
    },
    "Zone 3": {
      title: "ZONE 3 (HIGH)",
      subtitle: "Boven VT2 - Maximale Ademarbeid",
      theory: "Boven de tweede ventilatoire drempel. Ademhaling gaat maximaal. 'Steady' rijden wordt onmogelijk; dit is werk met een hoge herstelvraag.",
      bullets: [
        "Hard werk hard genoeg maken",
        "Werken tegen het aerobe plafond",
        "Maximale ventilatoire druk"
      ],
      prikkels: ["VO2max prikkel", "Lactaat tolerantie", "Top-end vermogen"],
      doelen: ["Klimvermogen (3-8 min)", "Gaten dichten / attacks", "FTP verhogen"],
      voorbeelden: ["4x4 Norway intervallen", "30/30's"],
      takeaway: "Meting via ademvariabelen (VE, Rf) is de gouden standaard.",
      colorClass: "red",
      sidebarLabel: "HIGH"
    }
  };

  // Data voor het 5-Zone Model (Coaching Detail)
  const zones5 = {
    "Zone 1": {
      title: "ZONE 1",
      subtitle: "Herstel (Ver onder VT1)",
      theory: "Heel rustig trappen. Praattempo: moeiteloos praten. Ademhaling blijft laag en stabiel.",
      bullets: ["Easy écht easy houden", "Ondersteunend, niet het hele plan"],
      prikkels: ["Herstelcapaciteit (doorbloeding)", "Techniek/cadans zonder stress", "Basisvolume"],
      doelen: ["Sneller herstellen", "Volume zonder vermoeidheid", "Consistentie"],
      voorbeelden: ["30-60 min herstelrit", "Spin na intervaldag"],
      takeaway: "Z1 is ondersteunend voor de rest van je plan.",
      colorClass: "emerald",
      sidebarLabel: "Z1"
    },
    "Zone 2": {
      title: "ZONE 2",
      subtitle: "Aerobe Basis (Kalibreren met VT1)",
      theory: "Rustig tot steady. Je voelt dat je 'werkt'. Zit onder of rond VT1: hoogste intensiteit die je lang kunt stapelen.",
      bullets: ["Hoogste aerobe efficiëntie", "Zelfde watt = minder ademdruk over tijd"],
      prikkels: ["Aerobe capaciteit", "Aerobe efficiëntie", "Vet+koolhydraatmix"],
      doelen: ["Uithoudingsvermogen", "Basis voor intensief werk", "Betere pacing"],
      voorbeelden: ["90-240 min duurrit", "2-3 uur basis"],
      takeaway: "VT1 is het anker waarmee je Z2 goed kalibreert.",
      colorClass: "teal",
      sidebarLabel: "Z2"
    },
    "Zone 3": {
      title: "ZONE 3",
      subtitle: "Tempo (Comfortabel Zwaar)",
      theory: "Stevig. Korte zinnen lukken nét. Je krijgt sneller 'drift' (zelfde watt = hogere ademdruk/HR).",
      bullets: ["Valkuil: te vaak 'grijs' rijden", "Dieselvermogen trainen"],
      prikkels: ["Tempo-uithoudingsvermogen", "Race-gevoel", "Mentale tolerantie"],
      doelen: ["Gran fondo / lange solo's", "Specifieke race pace"],
      voorbeelden: ["3x15 min tempo", "Lange klim steady"],
      takeaway: "Voorkom dat Z3 je standaardrit wordt.",
      colorClass: "amber",
      sidebarLabel: "Z3"
    },
    "Zone 4": {
      title: "ZONE 4",
      subtitle: "Threshold (Rond VT2)",
      theory: "Hard, nauwelijks praten. Ademdruk is hoog, tempo 'managen'. Duidelijke herstelvraag.",
      bullets: ["Drempelvermogen verhogen", "Tolerantie voor hoge ventilatie"],
      prikkels: ["Drempelvermogen", "Pacingvaardigheid", "Ademrespons training"],
      doelen: ["Sneller op 20-60 min inspanningen", "Tijdrit / breakaway"],
      voorbeelden: ["3x10 min threshold", "Over/unders"],
      takeaway: "Wattage + ademrespons is hier betrouwbaarder dan HR.",
      colorClass: "orange",
      sidebarLabel: "Z4"
    },
    "Zone 5": {
      title: "ZONE 5",
      subtitle: "VO2 Max (Boven VT2)",
      theory: "Zeer hard. Praten onmogelijk. Ventilatie gaat maximaal. Tijd doorbrengen tegen aerobe plafond.",
      bullets: ["Kort & scherp", "Vraagt veel herstel"],
      prikkels: ["VO2max-prikkel", "Top-end verbetering", "Herstel tussen pieken"],
      doelen: ["Klimvermogen verbeteren", "Attacks / gaten dichten"],
      voorbeelden: ["4x4 Norway", "5x3 min intervallen"],
      takeaway: "Werkt best met veel Z1-Z2 eromheen.",
      colorClass: "red",
      sidebarLabel: "Z5"
    }
  };

  useEffect(() => { setSelectedZone("Zone 1"); }, [modelType]);

  const activeZones = modelType === '3-Zone Model' ? zones3 : zones5;
  const curr = activeZones[selectedZone] || activeZones["Zone 1"];

  // Curve die Ventilatie (VE) simuleert (stijgt exponentieel bij drempels)
  const chartData = useMemo(() => {
    return Array.from({ length: 101 }, (_, i) => ({
      x: i,
      ve: 15 + 0.001 * Math.pow(i, 2.5) // Basisventilatie + exponentiële stijging
    }));
  }, []);

  const getColor = (cls) => {
    const colors = {
      emerald: { bg: 'bg-emerald-50', border: 'border-emerald-200', text: 'text-emerald-700', accent: 'bg-emerald-600', fill: '#dcfce7' },
      teal: { bg: 'bg-teal-50', border: 'border-teal-200', text: 'text-teal-700', accent: 'bg-teal-600', fill: '#ccfbf1' },
      amber: { bg: 'bg-amber-50', border: 'border-amber-200', text: 'text-amber-700', accent: 'bg-amber-600', fill: '#fef9c3' },
      orange: { bg: 'bg-orange-50', border: 'border-orange-200', text: 'text-orange-700', accent: 'bg-orange-600', fill: '#ffedd5' },
      red: { bg: 'bg-red-50', border: 'border-red-200', text: 'text-red-700', accent: 'bg-red-600', fill: '#fee2e2' }
    };
    return colors[cls] || colors.emerald;
  };

  const currentColors = getColor(curr.colorClass);

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans p-4 md:p-8">
      <header className="max-w-6xl mx-auto mb-10 text-center">
        <h1 className="text-4xl md:text-6xl font-black tracking-tight mb-2">
          Master je <span className="text-red-600 italic">Intensiteit.</span>
        </h1>
        <p className="text-slate-500 text-lg font-medium">Focus op ventilatoire ankers VT1 & VT2 als leidraad.</p>

        <div className="flex justify-center mt-8">
          <div className="bg-slate-200 p-1 rounded-2xl flex gap-1 shadow-inner">
            {["3-Zone Model", "5-Zone Model"].map((m) => (
              <button
                key={m}
                onClick={() => setModelType(m)}
                className={`px-8 py-3 rounded-xl font-black transition-all flex items-center gap-2 ${
                  modelType === m ? "bg-white text-slate-900 shadow-md scale-105" : "text-slate-500 hover:text-slate-700"
                }`}
              >
                <Layers size={18} />
                {m}
              </button>
            ))}
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Grafiek - Ademrespons */}
        <div className="lg:col-span-8 bg-white p-6 md:p-8 rounded-[2rem] shadow-sm border border-slate-100">
          <div className="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4">
            <h3 className="font-black text-2xl flex items-center gap-2 tracking-tight">
              <Wind className="text-blue-500" size={24} />
              Ventilatoire Respons
            </h3>
            <div className="flex gap-4 text-[10px] font-black uppercase tracking-widest text-slate-400">
              <span className="flex items-center gap-2 border border-slate-200 px-3 py-1 rounded-full">VT1: Ademarbeid stijgt</span>
              <span className="flex items-center gap-2 border border-slate-200 px-3 py-1 rounded-full">VT2: Steady wordt lastig</span>
            </div>
          </div>
          
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -30, bottom: 0 }}>
                <defs>
                  <linearGradient id="veGradient" x1="0" y1="0" x2="1" y2="0">
                    <stop offset="0%" stopColor="#dcfce7" />
                    <stop offset={`${vt1}%`} stopColor="#dcfce7" />
                    <stop offset={`${vt1}%`} stopColor="#ffedd5" />
                    <stop offset={`${vt2}%`} stopColor="#ffedd5" />
                    <stop offset={`${vt2}%`} stopColor="#fee2e2" />
                    <stop offset="100%" stopColor="#fee2e2" />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="x" hide />
                <YAxis hide domain={[15, 'auto']} />
                <Tooltip 
                  content={({ active, payload }) => active && payload ? (
                    <div className="bg-slate-900 text-white p-3 shadow-2xl rounded-xl border border-slate-700 text-xs">
                      <p className="font-black tracking-widest uppercase mb-1">Intensiteit</p>
                      <p className="text-xl font-black text-blue-400">{payload[0].payload.x}%</p>
                      <p className="text-slate-400 mt-2 italic">Ademvolume (VE): Hoog</p>
                    </div>
                  ) : null}
                />
                <Area type="monotone" dataKey="ve" stroke="#1e293b" strokeWidth={5} fill="url(#veGradient)" fillOpacity={0.9} />
                <ReferenceLine x={vt1} stroke="#94a3b8" strokeDasharray="4 4" strokeWidth={2}>
                  <Label value="VT1 ANKER" position="top" fill="#64748b" fontWeight="900" fontSize={10} dy={-10} />
                </ReferenceLine>
                <ReferenceLine x={vt2} stroke="#94a3b8" strokeDasharray="4 4" strokeWidth={2}>
                  <Label value="VT2 ANKER" position="top" fill="#64748b" fontWeight="900" fontSize={10} dy={-10} />
                </ReferenceLine>
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Sidebar - Fysiologische Toelichting */}
        <div className="lg:col-span-4 space-y-6">
          <div className="bg-slate-900 text-white p-8 rounded-[2rem] shadow-2xl relative overflow-hidden group">
            <h2 className="text-2xl font-black italic mb-2 uppercase tracking-tight">Waarom zones?</h2>
            <p className="text-slate-400 text-sm mb-6 font-medium">Doseren op fysiologie, niet op gevoel.</p>
            
            <div className="space-y-4 text-sm relative z-10">
              <div className="flex gap-3">
                <CheckCircle2 size={18} className="text-emerald-400 shrink-0" />
                <p>Easy écht easy houden, hard écht hard.</p>
              </div>
              <div className="flex gap-3">
                <CheckCircle2 size={18} className="text-emerald-400 shrink-0" />
                <p>Koppel zones aan Watt + context (Adem/RPE).</p>
              </div>
              <div className="flex gap-3 font-bold text-red-400 border-t border-slate-800 pt-4">
                <Activity size={18} className="shrink-0" />
                <p>VT1 & VT2 zijn exactere ankers dan % HRmax.</p>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-[2rem] border border-slate-100 italic text-slate-500 text-sm flex gap-3 shadow-sm">
            <Info size={24} className="text-slate-300 flex-shrink-0" />
            "Zones werken pas echt als ze gemeten, gekalibreerd en toegepast worden."
          </div>
        </div>

        {/* Zone Navigatie */}
        <div className="lg:col-span-12">
          <div className={`grid gap-3 ${modelType === '3-Zone Model' ? 'grid-cols-3' : 'grid-cols-2 md:grid-cols-5'}`}>
            {Object.keys(activeZones).map((zoneKey) => (
              <button
                key={zoneKey}
                onClick={() => setSelectedZone(zoneKey)}
                className={`p-5 rounded-2xl font-black text-sm transition-all border-2 flex flex-col items-center gap-2 ${
                  selectedZone === zoneKey 
                  ? `bg-white ${getColor(activeZones[zoneKey].colorClass).border} shadow-lg scale-105 ring-4 ring-slate-100 z-10` 
                  : "bg-white border-transparent text-slate-400 hover:bg-slate-50"
                }`}
              >
                <span className={selectedZone === zoneKey ? getColor(activeZones[zoneKey].colorClass).text : ""}>{zoneKey}</span>
                <div className={`w-8 h-1 rounded-full ${selectedZone === zoneKey ? getColor(activeZones[zoneKey].colorClass).accent : "bg-slate-100"}`}></div>
              </button>
            ))}
          </div>
        </div>

        {/* Gedetailleerde Zone Kaart */}
        <div className="lg:col-span-12 grid grid-cols-1 lg:grid-cols-3 gap-8 mb-16">
          <div className={`lg:col-span-2 ${currentColors.bg} border-2 ${currentColors.border} rounded-[3rem] p-8 md:p-12 transition-all shadow-sm`}>
            <div className="flex flex-col md:flex-row md:items-end gap-3 mb-6">
              <h2 className={`text-6xl font-black italic tracking-tighter ${currentColors.text}`}>
                {curr.title}
              </h2>
            </div>
            <p className="text-slate-500 font-black uppercase tracking-[0.2em] text-xs mb-8">{curr.subtitle}</p>
            
            <div className="mb-10">
              <h4 className="flex items-center gap-2 font-black text-sm uppercase tracking-widest text-slate-400 mb-3">
                <BookOpen size={16} /> Theorie
              </h4>
              <p className="text-2xl leading-snug text-slate-800 font-bold tracking-tight mb-6">
                {curr.theory}
              </p>
              <ul className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {curr.bullets.map((b, i) => (
                  <li key={i} className="flex items-center gap-2 text-slate-600 font-semibold italic border-l-2 border-slate-300 pl-3">
                    {b}
                  </li>
                ))}
              </ul>
            </div>

            <div className="bg-white/80 backdrop-blur-md p-6 rounded-3xl border border-white shadow-xl flex gap-5 items-center">
              <div className={`p-3 rounded-2xl ${currentColors.bg}`}>
                <AlertTriangle className="text-orange-600" size={24} />
              </div>
              <div>
                <span className="block font-black text-[10px] uppercase tracking-[0.2em] text-slate-400 mb-1">Gouden Takeaway</span>
                <p className="text-slate-700 italic font-bold text-lg">{curr.takeaway}</p>
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <div className="bg-white p-8 rounded-[2.5rem] border border-slate-100 shadow-sm">
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-blue-100 rounded-xl"><Zap size={20} className="text-blue-600" /></div>
                <h4 className="font-black uppercase tracking-widest text-xs text-slate-400">Prikkels & Doelen</h4>
              </div>
              <div className="space-y-6">
                <div>
                  <p className="text-[10px] font-black uppercase text-slate-400 mb-2">Prikkels</p>
                  <ul className="space-y-2">
                    {curr.prikkels.map((p, i) => (
                      <li key={i} className="flex items-center gap-3 font-bold text-slate-700">
                        <div className={`w-1.5 h-1.5 rounded-full ${currentColors.accent}`}></div> {p}
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <p className="text-[10px] font-black uppercase text-slate-400 mb-2">Helpt bij</p>
                  <ul className="space-y-2">
                    {curr.doelen.map((d, i) => (
                      <li key={i} className="flex items-center gap-3 font-bold text-slate-700">
                        <div className={`w-1.5 h-1.5 rounded-full ${currentColors.accent}`}></div> {d}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>

            <div className="bg-slate-900 text-white p-8 rounded-[2.5rem] shadow-lg relative overflow-hidden">
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-slate-800 rounded-xl"><Bike size={20} className="text-red-500" /></div>
                <h4 className="font-black uppercase tracking-widest text-xs text-slate-500">Praktijk Voorbeelden</h4>
              </div>
              <ul className="space-y-4">
                {curr.voorbeelden.map((v, i) => (
                  <li key={i} className="flex items-center gap-4 font-black text-slate-300 italic">
                    <ChevronRight size={18} className="text-red-500" /> {v}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </main>

      <footer className="max-w-6xl mx-auto text-center py-16 border-t border-slate-200">
        <p className="text-slate-300 text-xs font-black uppercase tracking-[0.5em]">VT1 & VT2 — De Ankers van jouw Succes</p>
      </footer>
    </div>
  );
};

export default App;
