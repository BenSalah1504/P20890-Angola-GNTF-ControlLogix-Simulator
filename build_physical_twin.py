# -*- coding: utf-8 -*-
"""
GNTF QUINGUILA TANK FARM — COMPLETE PHYSICAL TWIN & CONTROLLOGIX 5580 SOFT-PLC WEB SIMULATOR
Generates a self-contained, zero-dependency industrial HTML5/JS/SVG/Canvas simulator
coupling a continuous-time physical process twin with the 25 Allen-Bradley ST routines.
"""
import os
import json
import glob

BASE_DIR = r"c:\Users\Wajdi TAKTAK\Desktop\DOC\ws_g\pme_ladder_export"
ST_DIR = os.path.join(BASE_DIR, "ab_st_routines")
OUT_PATHS = [
    os.path.join(BASE_DIR, "GNTF_Physical_Twin_Simulator.html"),
    r"C:\Users\Wajdi TAKTAK\Desktop\P20890_Angola\GNTF_Physical_Twin_Simulator.html",
]

ROUTINE_ORDER = [
    "MainRoutine", "Init", "Input", "DI_1", "DI_2",
    "AI_1", "CalcVa1", "AI_2", "CalcVa2", "AI_3", "CalcVa3",
    "AI_4_New", "Ai_AL_1", "Ai_AL_2", "Ai_AL_3", "Vote_1",
    "Logic", "CE_LOG", "Indicat", "Shutdow", "Protect",
    "Loc_Al", "FLT_1", "Sound", "Output"
]

def load_st_routines():
    routines = {}
    for name in ROUTINE_ORDER:
        p = os.path.join(ST_DIR, f"{name}.st")
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                routines[name] = f.read()
    return routines

ST_ROUTINES = load_st_routines()
print(f"Loaded {len(ST_ROUTINES)} ST routines.")

HTML_TEMPLATE_PART1 = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GNTF Quinguila Tank Farm — Physical Twin & ControlLogix 5580 Soft-PLC Simulator</title>
<style>
:root {
  --bg-0: #070b12;
  --bg-1: #0d1420;
  --bg-2: #131d2e;
  --bg-3: #1b283f;
  --border: #263859;
  --border-hi: #3b5586;
  --text-0: #f0f6fc;
  --text-1: #b8c7e0;
  --text-2: #7b90b2;
  --cyan: #00d4ff;
  --blue: #2f81f7;
  --green: #10b981;
  --green-hi: #22c55e;
  --amber: #f59e0b;
  --orange: #f97316;
  --red: #ef4444;
  --red-hi: #ff2a2a;
  --purple: #a855f7;
  --font-sans: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
  --font-mono: 'Consolas', 'JetBrains Mono', 'Courier New', monospace;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--bg-0);
  color: var(--text-0);
  font-family: var(--font-sans);
  font-size: 13px;
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  user-select: none;
}

/* TOP SCADA HEADER */
.top-header {
  background: linear-gradient(90deg, #09101d 0%, #111d33 50%, #09101d 100%);
  border-bottom: 1px solid var(--border);
  padding: 6px 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-shrink: 0;
}
.brand-block {
  display: flex;
  align-items: center;
  gap: 10px;
}
.brand-badge {
  background: linear-gradient(135deg, #0284c7, #1d4ed8);
  color: #fff;
  font-weight: 800;
  font-size: 12px;
  padding: 5px 9px;
  border-radius: 5px;
  letter-spacing: 0.6px;
  border: 1px solid #38bdf8;
  box-shadow: 0 0 12px rgba(2,132,199,0.4);
}
.brand-title {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-0);
  letter-spacing: 0.3px;
}
.brand-sub {
  font-size: 11px;
  color: var(--text-2);
  font-family: var(--font-mono);
}

/* KPI PILLS IN HEADER */
.header-kpis {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
.kpi-pill {
  background: var(--bg-2);
  border: 1px solid var(--border);
  border-radius: 5px;
  padding: 4px 9px;
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: var(--font-mono);
  font-size: 11.5px;
}
.kpi-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--green);
  box-shadow: 0 0 6px var(--green);
}
.kpi-dot.alarm {
  background: var(--red-hi);
  box-shadow: 0 0 10px var(--red-hi);
  animation: pulse-fast 0.6s infinite alternate;
}
.kpi-dot.warn {
  background: var(--amber);
  box-shadow: 0 0 8px var(--amber);
}
@keyframes pulse-fast {
  from { opacity: 1; transform: scale(1); }
  to { opacity: 0.3; transform: scale(0.85); }
}

/* SIMULATOR CONTROLS */
.sim-controls {
  display: flex;
  align-items: center;
  gap: 6px;
}
.btn {
  background: var(--bg-3);
  color: var(--text-0);
  border: 1px solid var(--border-hi);
  border-radius: 4px;
  padding: 5px 10px;
  font-size: 11.5px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  transition: all 0.15s;
}
.btn:hover { background: #263959; border-color: var(--cyan); }
.btn.active { background: #1d4ed8; border-color: #60a5fa; color: #fff; }
.btn.success { background: #065f46; border-color: #10b981; color: #ecfdf5; }
.btn.success:hover { background: #047857; }
.btn.warn { background: #78350f; border-color: #f59e0b; color: #fef3c7; }
.btn.warn:hover { background: #92400e; }
.btn.danger { background: #7f1d1d; border-color: #ef4444; color: #fee2e2; }
.btn.danger:hover { background: #991b1b; }
.speed-select {
  background: var(--bg-2);
  color: var(--cyan);
  border: 1px solid var(--border-hi);
  border-radius: 4px;
  padding: 4px 6px;
  font-family: var(--font-mono);
  font-size: 11.5px;
  font-weight: 700;
}

/* NAVIGATION TABS */
.nav-bar {
  background: var(--bg-1);
  border-bottom: 1px solid var(--border);
  padding: 0 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
}
.nav-tabs {
  display: flex;
  gap: 2px;
}
.nav-tab {
  padding: 8px 14px;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-1);
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.15s;
}
.nav-tab:hover { color: var(--text-0); background: rgba(255,255,255,0.03); }
.nav-tab.active {
  color: var(--cyan);
  border-bottom-color: var(--cyan);
  background: rgba(0,212,255,0.07);
}
.tab-badge {
  background: var(--bg-3);
  color: var(--text-1);
  padding: 1px 6px;
  border-radius: 9px;
  font-size: 10px;
  font-family: var(--font-mono);
}
.tab-badge.alert { background: var(--red); color: #fff; }

/* QUICK FGCP STRIP IN NAV BAR */
.quick-fgcp {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 0;
}
.led-chip {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 3px 8px;
  border-radius: 4px;
  font-family: var(--font-mono);
  font-size: 10.5px;
  font-weight: 700;
  background: #0d1522;
  border: 1px solid #22324d;
  color: #64748b;
}
.led-chip .bulb {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #334155;
}
.led-chip.on-green { color: #d1fae5; border-color: #059669; background: rgba(16,185,129,0.14); }
.led-chip.on-green .bulb { background: #22c55e; box-shadow: 0 0 8px #22c55e; }
.led-chip.on-red { color: #fee2e2; border-color: #dc2626; background: rgba(239,68,68,0.18); }
.led-chip.on-red .bulb { background: #ff2a2a; box-shadow: 0 0 9px #ff2a2a; }
.led-chip.on-amber { color: #fef3c7; border-color: #d97706; background: rgba(245,158,11,0.18); }
.led-chip.on-amber .bulb { background: #f59e0b; box-shadow: 0 0 8px #f59e0b; }

/* MAIN WORKSPACE AREA */
.workspace {
  flex: 1;
  overflow: hidden;
  display: flex;
  position: relative;
}
.view-panel {
  display: none;
  width: 100%;
  height: 100%;
  overflow: auto;
  padding: 10px 14px;
}
.view-panel.active {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* GRID LAYOUTS */
.pid-layout {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 10px;
  height: 100%;
  min-height: 0;
}
.card {
  background: var(--bg-1);
  border: 1px solid var(--border);
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.card-header {
  background: var(--bg-2);
  border-bottom: 1px solid var(--border);
  padding: 7px 12px;
  font-size: 12px;
  font-weight: 700;
  color: var(--text-0);
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
}
.card-body {
  padding: 10px;
  overflow: auto;
  flex: 1;
}

/* SVG P&ID CANVAS STYLING */
.pid-svg-wrap {
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 50% 50%, #0e1829 0%, #070c15 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}
.pid-svg {
  width: 100%;
  height: 100%;
  max-height: 100%;
}
.pipe {
  fill: none;
  stroke: #283a57;
  stroke-width: 4;
  stroke-linecap: round;
  stroke-linejoin: round;
}
.pipe-flow {
  fill: none;
  stroke: var(--cyan);
  stroke-width: 3;
  stroke-dasharray: 10 8;
  animation: flow-anim 0.8s linear infinite;
  opacity: 0;
  transition: opacity 0.25s;
}
.pipe-flow.oil { stroke: #f59e0b; }
.pipe-flow.gas { stroke: #a855f7; }
.pipe-flow.water { stroke: #00d4ff; }
.pipe-flow.foam { stroke: #22c55e; stroke-width: 4; }
.pipe-flow.active { opacity: 0.95; }
@keyframes flow-anim {
  from { stroke-dashoffset: 18; }
  to { stroke-dashoffset: 0; }
}
.equip-node {
  cursor: pointer;
  transition: filter 0.15s;
}
.equip-node:hover {
  filter: drop-shadow(0 0 6px rgba(0,212,255,0.65));
}

/* TABLES & SLIDERS */
.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 11.5px;
}
.data-table th {
  background: var(--bg-2);
  color: var(--text-1);
  text-align: left;
  padding: 6px 8px;
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 2;
}
.data-table td {
  padding: 5px 8px;
  border-bottom: 1px solid rgba(38,56,89,0.5);
  font-family: var(--font-mono);
}
.data-table tr:hover { background: rgba(255,255,255,0.03); }

input[type=range] {
  -webkit-appearance: none;
  appearance: none;
  height: 5px;
  background: #22324d;
  border-radius: 3px;
  outline: none;
}
input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 13px;
  height: 13px;
  border-radius: 50%;
  background: var(--cyan);
  cursor: pointer;
  border: 2px solid #fff;
}

/* FGCP HARDWARE PANEL MIMIC */
.fgcp-cabinet {
  background: linear-gradient(180deg, #1b2432 0%, #111722 100%);
  border: 3px solid #3c4d69;
  border-radius: 8px;
  padding: 14px;
  box-shadow: inset 0 0 25px rgba(0,0,0,0.75);
}
.led-matrix-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(175px, 1fr));
  gap: 8px;
}
.panel-lamp {
  background: #0c121d;
  border: 1px solid #2b3b54;
  border-radius: 5px;
  padding: 8px 10px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.lamp-lens {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #1f2937;
  border: 2px solid #4b5563;
  flex-shrink: 0;
  transition: all 0.12s;
}
.lamp-lens.red.lit {
  background: radial-gradient(circle, #ff8080 0%, #ef4444 60%, #991b1b 100%);
  border-color: #fca5a5;
  box-shadow: 0 0 14px #ef4444;
}
.lamp-lens.green.lit {
  background: radial-gradient(circle, #86efac 0%, #22c55e 60%, #166534 100%);
  border-color: #bbf7d0;
  box-shadow: 0 0 14px #22c55e;
}
.lamp-lens.amber.lit {
  background: radial-gradient(circle, #fde68a 0%, #f59e0b 60%, #92400e 100%);
  border-color: #fef08a;
  box-shadow: 0 0 14px #f59e0b;
}

/* C&E MATRIX TABLE */
.ce-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 10.5px;
  font-family: var(--font-mono);
}
.ce-table th, .ce-table td {
  border: 1px solid #24344f;
  padding: 4px 5px;
  text-align: center;
}
.ce-table th.cause-col, .ce-table td.cause-col {
  text-align: left;
  min-width: 220px;
  position: sticky;
  left: 0;
  background: #101929;
  z-index: 1;
}
.ce-table tr.cause-active td.cause-col {
  background: #45121b;
  color: #fecaca;
  font-weight: 700;
}
.ce-cell-hit {
  background: #dc2626 !important;
  color: #fff !important;
  font-weight: 800;
  box-shadow: inset 0 0 6px rgba(255,255,255,0.5);
}
.ce-cell-spec {
  color: var(--cyan);
  font-weight: 700;
}

/* BOTTOM ISA-18.2 ALARM BANNER */
.alarm-footer {
  background: #080d16;
  border-top: 2px solid var(--border);
  height: 112px;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}
.alarm-footer-bar {
  background: var(--bg-2);
  padding: 4px 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border);
  font-size: 11px;
}
.alarm-list {
  flex: 1;
  overflow-y: auto;
  padding: 4px 12px;
  font-family: var(--font-mono);
  font-size: 11px;
}
.alm-row {
  display: grid;
  grid-template-columns: 85px 95px 110px 1fr 120px 80px;
  gap: 8px;
  padding: 3px 6px;
  border-bottom: 1px solid rgba(255,255,255,0.04);
  align-items: center;
}
.alm-row.unack {
  background: rgba(239,68,68,0.22);
  color: #fecaca;
  animation: alm-flash 0.7s infinite alternate;
}
.alm-row.ack {
  background: rgba(245,158,11,0.12);
  color: #fde68a;
}
@keyframes alm-flash {
  from { background: rgba(239,68,68,0.28); }
  to { background: rgba(239,68,68,0.06); }
}

/* ST CODE VIEWER */
.st-code-box {
  background: #070b12;
  border: 1px solid var(--border);
  border-radius: 5px;
  padding: 10px 12px;
  font-family: var(--font-mono);
  font-size: 12px;
  line-height: 1.5;
  overflow: auto;
  white-space: pre;
  color: #d1d5db;
  height: 100%;
}
.st-kw { color: #60a5fa; font-weight: 700; }
.st-cmt { color: #6b7280; font-style: italic; }
.st-num { color: #f59e0b; }
.st-val-true { background: rgba(34,197,94,0.22); color: #4ade80; padding: 0 4px; border-radius: 3px; font-weight: 700; }
.st-val-false { background: rgba(148,163,184,0.12); color: #94a3b8; padding: 0 4px; border-radius: 3px; }
.st-val-num { background: rgba(0,212,255,0.15); color: #38bdf8; padding: 0 4px; border-radius: 3px; font-weight: 700; }
</style>
</head>
<body>
"""

HTML_TEMPLATE_PART2 = r"""
<!-- ==================== TOP SCADA HEADER ==================== -->
<header class="top-header">
  <div class="brand-block">
    <div class="brand-badge">EPPM ANGOLA</div>
    <div>
      <div class="brand-title">GNTF QUINGUILA TANK FARM — PHYSICAL TWIN &amp; ICSS SIMULATOR</div>
      <div class="brand-sub">PLC: Allen-Bradley 1756-L82E (192.168.20.10) | Rack: 1756-A13 | Program: P20890_Angola (25 ST Routines)</div>
    </div>
  </div>

  <div class="header-kpis">
    <div class="kpi-pill" title="ControlLogix 5580 CPU State">
      <span class="kpi-dot" id="kpi-plc-dot"></span>
      <span>CPU: <strong id="kpi-plc-mode" style="color:var(--green-hi)">REM RUN</strong> (<span id="kpi-scan-ms">50</span>ms)</span>
    </div>
    <div class="kpi-pill" title="Master Emergency Shutdown Status (Local:8:O.Data.0)">
      <span class="kpi-dot" id="kpi-esd-dot"></span>
      <span>ESD: <strong id="kpi-esd-txt">HEALTHY</strong></span>
    </div>
    <div class="kpi-pill" title="6401-ESDV-001 Fuel Gas Shutdown Valve">
      <span class="kpi-dot" id="kpi-esdv-dot"></span>
      <span>ESDV-001: <strong id="kpi-esdv-txt">OPEN (100%)</strong></span>
    </div>
    <div class="kpi-pill" title="Deluge / Foam Suppression System">
      <span class="kpi-dot" id="kpi-deluge-dot"></span>
      <span>DELUGE: <strong id="kpi-deluge-txt">STANDBY</strong></span>
    </div>
    <div class="kpi-pill" title="Simulation Clock & Speed">
      <span>SIM TIME: <strong id="kpi-sim-time" style="color:var(--cyan)">00:00:00.0</strong></span>
    </div>
  </div>

  <div class="sim-controls">
    <button class="btn active" id="btn-play-pause" onclick="toggleSimRun()">&#9654; RUNNING</button>
    <select class="speed-select" id="sel-sim-speed" onchange="setSimSpeed(this.value)" title="Time Warp Multiplier">
      <option value="0.25">0.25x</option>
      <option value="1" selected>1.0x (Real-Time)</option>
      <option value="2">2.0x</option>
      <option value="5">5.0x</option>
      <option value="10">10.0x</option>
      <option value="30">30.0x (Fast Timers)</option>
    </select>
    <button class="btn warn" onclick="pressSystemMute()" title="FGCP E12 Mute / HMI Accept (M00001)">&#128263; MUTE (E12)</button>
    <button class="btn success" onclick="pressSystemReset()" title="FGCP E11 Reset / HMI Reset (M00002)">&#8635; RESET (E11)</button>
    <button class="btn danger" onclick="triggerManualESD()" title="Press Field ESD Fuel Gas Pushbutton E9 (6401-ESDV-001)">&#9888; ESD TRIP (E9)</button>
    <button class="btn" id="btn-audio-toggle" onclick="toggleAudio()" title="Enable/Disable Web Audio Horn Synthesizer">&#128266; AUDIO: OFF</button>
  </div>
</header>

<!-- ==================== NAVIGATION & FGCP STATUS BAR ==================== -->
<nav class="nav-bar">
  <div class="nav-tabs">
    <button class="nav-tab active" onclick="switchTab('tab-pid', this)">1. P&amp;ID PROCESS TWIN</button>
    <button class="nav-tab" onclick="switchTab('tab-fgmap', this)">2. 2D F&amp;G PLUME MAP <span class="tab-badge" id="badge-fg">41</span></button>
    <button class="nav-tab" onclick="switchTab('tab-fgcp', this)">3. FGCP-7404-001 PANEL</button>
    <button class="nav-tab" onclick="switchTab('tab-ce', this)">4. LIVE C&amp;E MATRIX</button>
    <button class="nav-tab" onclick="switchTab('tab-plc', this)">5. 1756 RACK &amp; ST DEBUGGER</button>
    <button class="nav-tab" onclick="switchTab('tab-scenarios', this)">6. FAT / SAT SCENARIOS</button>
    <button class="nav-tab" onclick="switchTab('tab-trends', this)">7. TRENDS &amp; HISTORIAN <span class="tab-badge" id="badge-alm">0</span></button>
  </div>

  <div class="quick-fgcp">
    <div class="led-chip on-green" id="qled-l15"><span class="bulb"></span>L15 ESDV OPEN</div>
    <div class="led-chip" id="qled-l14"><span class="bulb"></span>L14 ESDV CLOSED</div>
    <div class="led-chip" id="qled-l16"><span class="bulb"></span>L16 LOW AIR</div>
    <div class="led-chip" id="qled-l17"><span class="bulb"></span>L17 LOW GAS</div>
    <div class="led-chip" id="qled-z1"><span class="bulb"></span>Z1 PCR HORN</div>
    <div class="led-chip" id="qled-sa"><span class="bulb"></span>SA-001 BELL</div>
    <div class="led-chip" id="qled-h2s"><span class="bulb"></span>H2SA HORN</div>
    <div class="led-chip" id="qled-sda"><span class="bulb"></span>SDA SMOKE</div>
    <div class="led-chip" id="qled-sdge"><span class="bulb"></span>SD-GE TRIP</div>
  </div>
</nav>

<!-- ==================== MAIN WORKSPACE ==================== -->
<main class="workspace">

  <!-- ==================== TAB 1: INTERACTIVE P&ID PROCESS TWIN ==================== -->
  <section class="view-panel active" id="tab-pid">
    <div class="pid-layout">
      <!-- Left: Full Interactive SVG P&ID of Quinguila Tank Farm -->
      <div class="card">
        <div class="card-header">
          <span>QUINGUILA TANK FARM (GNTF) — LIVE DYNAMIC P&amp;ID &amp; HYDRAULIC TWIN (Click any tank, pump, valve, or transmitter to inspect/control)</span>
          <div style="display:flex;gap:8px;align-items:center;">
            <span style="font-size:11px;color:var(--text-2)">Physics Mode:</span>
            <button class="btn active" id="btn-phys-auto" onclick="setPhysicsCoupling(true)" style="padding:2px 8px;font-size:11px;">COUPLED ODE PHYSICS</button>
            <button class="btn" id="btn-phys-man" onclick="setPhysicsCoupling(false)" style="padding:2px 8px;font-size:11px;">MANUAL OVERRIDE</button>
            <button class="btn" onclick="resetPlantToNormal()" style="padding:2px 8px;font-size:11px;">RESTORE STEADY-STATE</button>
          </div>
        </div>
        <div class="pid-svg-wrap" id="pid-canvas-container">
          <!-- Populated dynamically by renderPIDSVG() -->
        </div>
      </div>

      <!-- Right: Selected Equipment Faceplate & Quick Process Sliders -->
      <div class="card">
        <div class="card-header">
          <span id="fp-title">EQUIPMENT FACEPLATE &amp; PROCESS CONTROLS</span>
          <span style="font-size:11px;color:var(--cyan);font-family:var(--font-mono)" id="fp-tag">OVERVIEW</span>
        </div>
        <div class="card-body" id="fp-body">
          <!-- Populated by renderFaceplate() -->
        </div>
      </div>
    </div>
  </section>

  <!-- ==================== TAB 2: 2D SPATIAL FIRE & GAS PLUME DISPERSION MAP ==================== -->
  <section class="view-panel" id="tab-fgmap">
    <div class="pid-layout" style="grid-template-columns: 1fr 430px;">
      <div class="card">
        <div class="card-header">
          <span>GNTF GENERAL ARRANGEMENT (01-MAN-03-08) — 2D GAUSSIAN GAS/FIRE PLUME DISPERSION TWIN</span>
          <div style="display:flex;gap:6px;align-items:center;">
            <span style="font-size:11px;color:var(--text-1)">Click Map to Inject Hazard:</span>
            <button class="btn active" id="hz-btn-ch4" onclick="setHazardTool('CH4')" style="padding:3px 8px;font-size:11px;">CH4 Gas Cloud</button>
            <button class="btn" id="hz-btn-h2s" onclick="setHazardTool('H2S')" style="padding:3px 8px;font-size:11px;">H2S Sour Gas</button>
            <button class="btn" id="hz-btn-fire" onclick="setHazardTool('FIRE')" style="padding:3px 8px;font-size:11px;">Pool Fire</button>
            <button class="btn" id="hz-btn-smoke" onclick="setHazardTool('SMOKE')" style="padding:3px 8px;font-size:11px;">Elec. Room Smoke</button>
            <button class="btn danger" onclick="clearAllPlumes()" style="padding:3px 8px;font-size:11px;">Clear All Hazards</button>
          </div>
        </div>
        <div class="card-body" style="padding:0;position:relative;display:flex;flex-direction:column;">
          <!-- Wind & Source Bar -->
          <div style="background:rgba(13,20,32,0.92);border-bottom:1px solid var(--border);padding:6px 12px;display:flex;gap:18px;align-items:center;flex-wrap:wrap;z-index:2;">
            <div style="display:flex;align-items:center;gap:6px;">
              <span style="font-size:11px;color:var(--text-1)">Wind Dir:</span>
              <input type="range" min="0" max="359" value="45" id="sl-wind-dir" oninput="updateWind()">
              <strong id="lbl-wind-dir" style="font-family:var(--font-mono);color:var(--cyan);width:42px;">45&deg; NE</strong>
            </div>
            <div style="display:flex;align-items:center;gap:6px;">
              <span style="font-size:11px;color:var(--text-1)">Wind Speed:</span>
              <input type="range" min="0.5" max="15" step="0.5" value="3.5" id="sl-wind-spd" oninput="updateWind()">
              <strong id="lbl-wind-spd" style="font-family:var(--font-mono);color:var(--cyan);width:48px;">3.5 m/s</strong>
            </div>
            <div style="display:flex;align-items:center;gap:6px;">
              <span style="font-size:11px;color:var(--text-1)">Release Intensity:</span>
              <input type="range" min="10" max="150" value="65" id="sl-plume-str" oninput="updateWind()">
              <strong id="lbl-plume-str" style="font-family:var(--font-mono);color:var(--amber);width:42px;">65%</strong>
            </div>
            <div style="font-size:11px;color:var(--text-2)">Active Plumes: <strong id="lbl-plume-cnt" style="color:var(--text-0)">0</strong></div>
          </div>
          <div style="flex:1;position:relative;background:#070d17;overflow:hidden;" id="fg-map-wrap">
            <canvas id="fg-plume-canvas" width="1100" height="620" style="width:100%;height:100%;cursor:crosshair;display:block;"></canvas>
          </div>
        </div>
      </div>

      <!-- Right: All 41 F&G Detectors Individual Sliders, Fault & Inhibit Controls -->
      <div class="card">
        <div class="card-header">
          <span>F&amp;G DETECTOR CHANNELS (SLOTS 2, 3, 4)</span>
          <input type="text" id="fg-filter-inp" placeholder="Filter tag (e.g. DG-001, H2S, DF)..." oninput="renderFGDetectorTable()" style="background:var(--bg-0);border:1px solid var(--border);color:var(--text-0);padding:3px 8px;border-radius:4px;font-size:11px;width:170px;">
        </div>
        <div class="card-body" style="padding:0;" id="fg-detector-table-wrap">
          <!-- Populated by renderFGDetectorTable() -->
        </div>
      </div>
    </div>
  </section>

  <!-- ==================== TAB 3: PHYSICAL FGCP-7404-001 & PCR MATRIX PANEL ==================== -->
  <section class="view-panel" id="tab-fgcp">
    <div id="fgcp-panel-container" style="display:flex;flex-direction:column;gap:12px;">
      <!-- Populated by renderFGCPPanel() -->
    </div>
  </section>

  <!-- ==================== TAB 4: LIVE CAUSE & EFFECT MATRIX (01-MAN-03-07) ==================== -->
  <section class="view-panel" id="tab-ce">
    <div class="card" style="height:100%;">
      <div class="card-header">
        <span>LIVE CAUSE &amp; EFFECT MATRIX (EPPM 01-MAN-03-07-PDF-C2C FINAL) — REAL-TIME INTERSECTION VERIFIER</span>
        <div style="display:flex;gap:8px;">
          <span style="font-size:11px;color:var(--text-2)">Legend: <strong style="color:var(--cyan)">X</strong>=Trip/Action | <strong style="color:var(--cyan)">C</strong>=Continuous Alarm | <strong style="color:var(--cyan)">D</strong>=Discontinuous (1Hz) | <strong style="color:var(--cyan)">10s</strong>=Delayed Standby Start</span>
          <button class="btn" onclick="resetPlantToNormal()" style="padding:2px 8px;font-size:11px;">CLEAR ALL CAUSES</button>
        </div>
      </div>
      <div class="card-body" style="padding:0;" id="ce-matrix-wrap">
        <!-- Populated by renderCEMatrix() -->
      </div>
    </div>
  </section>

  <!-- ==================== TAB 5: CONTROLLOGIX 1756 RACK & LIVE ST DEBUGGER ==================== -->
  <section class="view-panel" id="tab-plc">
    <div class="pid-layout" style="grid-template-columns: 440px 1fr;">
      <!-- Left: 1756-A13 Chassis Slot Inspector & Hardware I/O Table -->
      <div class="card">
        <div class="card-header">
          <span>1756-A13 CHASSIS (SLOTS 0–9) HARDWARE I/O</span>
          <select class="speed-select" id="sel-rack-slot" onchange="renderRackInspector()">
            <option value="2">Slot 2: 1756-IF16 (TB-02 Gas AI)</option>
            <option value="3">Slot 3: 1756-IF16 (TB-03 Press/MAC AI)</option>
            <option value="4">Slot 4: 1756-IF16 (TB-04 H2S/Flame/Smoke)</option>
            <option value="6">Slot 6: 1756-IF8H (TB-06 Radar Tank LTs)</option>
            <option value="7">Slot 7: 1756-IB32 (TB-07 Digital Inputs)</option>
            <option value="8">Slot 8: 1756-OB32 (TB-08 Digital Outputs)</option>
            <option value="9">Slot 9: MVI56E-MCM (Modbus Master/Slave)</option>
          </select>
        </div>
        <div class="card-body" id="rack-inspector-body" style="padding:6px;">
          <!-- Populated by renderRackInspector() -->
        </div>
      </div>

      <!-- Right: Studio 5000 Live Structured Text Routine Debugger -->
      <div class="card">
        <div class="card-header">
          <div style="display:flex;align-items:center;gap:8px;">
            <span>STUDIO 5000 LOGIX DESIGNER — LIVE ST ROUTINE MONITOR:</span>
            <select class="speed-select" id="sel-st-routine" onchange="renderSTDebugger()"></select>
          </div>
          <span style="font-size:11px;color:var(--text-2);font-family:var(--font-mono)">Inline values update in real time</span>
        </div>
        <div class="card-body" style="padding:0;">
          <div class="st-code-box" id="st-debugger-box"></div>
        </div>
      </div>
    </div>
  </section>

  <!-- ==================== TAB 6: AUTOMATED FAT / SAT SCENARIO RUNNER ==================== -->
  <section class="view-panel" id="tab-scenarios">
    <div class="card" style="height:100%;">
      <div class="card-header">
        <span>AUTOMATED FACTORY &amp; SITE ACCEPTANCE TEST (FAT / SAT) SCENARIO SUITE (SCOPE OF WORK SECTION VII &amp; IX)</span>
        <span style="font-size:11px;color:var(--cyan)" id="scen-active-status">Select a test scenario below to execute automated step-by-step verification</span>
      </div>
      <div class="card-body" id="scenarios-body">
        <!-- Populated by renderScenariosView() -->
      </div>
    </div>
  </section>

  <!-- ==================== TAB 7: REAL-TIME MULTI-PEN TRENDS & HISTORIAN ==================== -->
  <section class="view-panel" id="tab-trends">
    <div class="pid-layout" style="grid-template-columns: 1fr 480px;">
      <div class="card">
        <div class="card-header">
          <span>HIGH-SPEED MULTI-PEN PROCESS &amp; F&amp;G STRIP CHART RECORDER</span>
          <div style="display:flex;gap:8px;">
            <button class="btn" onclick="SimState.trendHistory=[];">Clear Chart</button>
          </div>
        </div>
        <div class="card-body" style="display:flex;flex-direction:column;gap:8px;">
          <canvas id="trend-canvas" width="900" height="460" style="width:100%;flex:1;background:#060a11;border:1px solid var(--border);border-radius:4px;"></canvas>
          <div style="display:flex;gap:14px;flex-wrap:wrap;font-family:var(--font-mono);font-size:11px;">
            <span style="color:#f59e0b">&#9632; PIT-003 Oil Manifold (0-3000 Psi)</span>
            <span style="color:#00d4ff">&#9632; PIT-002 Water Manifold (0-1500 Psi)</span>
            <span style="color:#a855f7">&#9632; 6401-PST-001 Fuel Gas (0-150 Psi)</span>
            <span style="color:#22c55e">&#9632; 6401-FT-001 Export Flow (0-500 bbl/h)</span>
            <span style="color:#ef4444">&#9632; Max CH4 (%LEL)</span>
            <span style="color:#ec4899">&#9632; Max H2S (PPM)</span>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <span>HISTORICAL EVENT &amp; ALARM JOURNAL (SOE LOG)</span>
          <button class="btn" onclick="exportSOECSV()" style="padding:2px 8px;font-size:11px;">&#128190; Export CSV</button>
        </div>
        <div class="card-body" style="padding:0;" id="soe-log-wrap">
          <!-- Populated by renderSOELog() -->
        </div>
      </div>
    </div>
  </section>

</main>

<!-- ==================== BOTTOM ISA-18.2 LIVE ALARM BANNER ==================== -->
<footer class="alarm-footer">
  <div class="alarm-footer-bar">
    <div style="display:flex;align-items:center;gap:12px;">
      <strong style="color:var(--red-hi)">&#9888; ISA-18.2 LIVE ALARM SUMMARY</strong>
      <span id="alm-summary-counts" style="font-family:var(--font-mono);color:var(--text-1)">0 Active | 0 Unacknowledged</span>
    </div>
    <div style="display:flex;gap:6px;">
      <button class="btn warn" style="padding:2px 8px;font-size:11px;" onclick="pressSystemMute()">ACK ALL / MUTE HORN (E12)</button>
      <button class="btn success" style="padding:2px 8px;font-size:11px;" onclick="pressSystemReset()">SYSTEM RESET (E11)</button>
    </div>
  </div>
  <div class="alarm-list" id="live-alarm-banner">
    <!-- Populated by renderAlarmBanner() -->
  </div>
</footer>
"""

JS_ENGINE_PART1 = r"""
<script>
// ============================================================================
// 1. EMBEDDED STUDIO 5000 STRUCTURED TEXT (ST) ROUTINES
// ============================================================================
const ST_ROUTINES = __ST_ROUTINES_JSON__;
const ROUTINE_ORDER = __ROUTINE_ORDER_JSON__;

// ============================================================================
// 2. COMPLETE PLANT & PLC STATE (PHYSICAL TWIN + CONTROLLOGIX 1756-L82E)
// ============================================================================
const SimState = {
  running: true,
  speed: 1.0,
  simTimeSec: 0.0,
  scanCount: 0,
  coupledPhysics: true,
  selectedEquip: 'OVERVIEW',
  hazardTool: 'CH4',
  audioEnabled: false,
  windDirDeg: 45,
  windSpeedMs: 3.5,
  plumeReleaseStrength: 65,
  plumes: [], // {x, y, type:'CH4'|'H2S'|'FIRE'|'SMOKE', strength, radius, created}
  trendHistory: [],
  soeLog: [],
  activeAlarms: {}, // id -> {id, time, tag, group, msg, prio, ack, active}
  activeScenario: null,

  // --- PHYSICAL TWIN CONTINUOUS STATE ---
  phys: {
    // 4 Crude Oil Storage Tanks (T-100..300: 0-10m, T-400: 0-12m)
    tanks: {
      T100: { level: 5.20, maxH: 10.0, areaM2: 452, inValve: 100, outValve: 60, fillBblH: 95, drainBblH: 45 },
      T200: { level: 6.40, maxH: 10.0, areaM2: 452, inValve: 80,  outValve: 70, fillBblH: 85, drainBblH: 50 },
      T300: { level: 4.10, maxH: 10.0, areaM2: 452, inValve: 75,  outValve: 50, fillBblH: 70, drainBblH: 35 },
      T400: { level: 7.80, maxH: 12.0, areaM2: 615, inValve: 90,  outValve: 65, fillBblH: 110, drainBblH: 55 }
    },
    // Heater Treaters V-710 & V-810
    treaters: {
      V710: { online: true, tempC: 66.5, pressPsi: 44.0, flowBblH: 180.0, waterCutPct: 14.2 },
      V810: { online: true, tempC: 68.0, pressPsi: 45.5, flowBblH: 180.0, waterCutPct: 12.8 }
    },
    // Fuel Gas & ESDV-001 Pneumatic System
    airAccPsi: 82.0,          // 7002-PST-001 (0-100 Psi, PAL=50)
    airCompressorOn: true,
    airLeakFault: false,
    fuelGasSupplyPsi: 72.0,   // Upstream supply
    fuelGasLinePsi: 68.0,     // 6401-PST-001 (0-150 Psi, PAL=40, PAH=100)
    esdvPositionPct: 100.0,   // 6401-ESDV-001 physical stem 0..100%
    esdvStuckFault: false,    // Mechanical jam fault for testing discrepancy timer

    // Oil Expedition Manifold
    oilExpPressPsi: 58.0,     // PIT-001 (0-200 Psi, PAL=10, PAH=100)
    oilExpFlowBblH: 185.0,    // 6401-FT-001 (0-500 bbl/h, FAL=30, FAH=300)
    oilExpChokePct: 75.0,

    // Power Oil Multiplex System (PIT-003: 0-3000 Psi, PAL=1700, PAH=2700, PAHH=2800)
    oilBoosterRun: true,      // P-2100 / P-2200
    powerOilPumps: {
      P2300: { cmdRun: true, running: true, rpm: 1650, lubePsi: 62, tempC: 74, ctrl: 'TTD-H Modbus' },
      P2400: { cmdRun: true, running: true, rpm: 1650, lubePsi: 61, tempC: 75, ctrl: 'TTD-H Modbus' },
      P2500: { cmdRun: true, running: true, rpm: 1620, lubePsi: 60, tempC: 73, ctrl: 'TTD-H Modbus' },
      P2600: { cmdRun: false, running: false, rpm: 0,  lubePsi: 0,  tempC: 32, ctrl: 'S1501 Modbus' }
    },
    oilManifoldPsi: 2150.0,   // PIT-003
    oilWellChokePct: 68.0,

    // Water Injection System (PIT-002: 0-1500 Psi, PAL=200, PAH=800, PAHH=900)
    waterBoosterRun: true,    // P-3600 / P-3700
    waterInjPumps: {
      P3800: { cmdRun: true, running: true, rpm: 1580, lubePsi: 58, tempC: 68, ctrl: 'TTD-H Modbus' },
      P3900: { cmdRun: true, running: true, rpm: 1580, lubePsi: 59, tempC: 69, ctrl: 'TTD-H Modbus' }
    },
    waterManifoldPsi: 540.0,  // PIT-002
    waterWellChokePct: 70.0,

    // Firewater & AFFF Foam Deluge System
    pumpARunning: false,      // 7503-PUMP-A (Electric Duty)
    pumpAFailFault: false,    // Simulate Pump A fails to build pressure -> triggers Pump B after 10s!
    pumpAWireBreak: false,    // Open circuit on Pump A coil check
    pumpBRunning: false,      // 7503-PUMP-B (Diesel Standby)
    pumpBWireBreak: false,    // Open circuit on Pump B coil check
    delugeValveOpenPct: 0.0,  // Deluge header valve opening
    delugeLinePsi: 0.0,       // 7503-PST-001 (0-100 Psi, PAH=50)
    foamTankPct: 92.0,        // AFFF Tank Level (Low switch < 20% -> 7503-LS-001)
    dieselTankPct: 88.0,      // Diesel Fuel Tank Level (Low switch < 20% -> 7503-LS-002)

    // Gas Generators (GE-01 & GE-02)
    gasGenRunning: true
  },

  // --- FIELD F&G DETECTORS & CALL POINTS (41 DEVICES WITH 2D COORDINATES) ---
  detectors: [],

  // --- DIGITAL INPUT SWITCHES / PUSHBUTTONS ---
  di: {
    FS_FGCP_E8: false,        // Panel Foam Stop button E8
    FS_7503_001_Pressed: false, // Field Foam Stop button (NC in field: false=not pressed)
    Pump_B_Inhibited: false,  // 75-SB-01B
    Reset_PB_E11: false,      // FGCP E11 Reset
    Mute_PB_E12: false,       // FGCP E12 Mute
    ESDV_6401_E9_Pressed: false, // Field/Panel ESD Fuel Gas Button E9 (NC in field)
    INHIBIT_FOAM_REL: false,  // Keyswitch S2
    INHIBIT_ALL_OUTPUTS: false, // Keyswitch S3
    ESTOP_P2300_E1: false,    // 7404-SB-004 (E1)
    ESTOP_P2400_E2: false,    // 7404-SB-005 (E2)
    ESTOP_P2500_E3: false,    // 7404-SB-006 (E3)
    ESTOP_P2600_E4: false,    // 7404-SB-007 (E4)
    ESTOP_P3800_E5: false,    // 7404-SB-008 (E5)
    ESTOP_P3900_E6: false     // 7404-SB-009 (E6)
  },

  // --- CONTROLLOGIX 1756-L82E TAG DATABASE & TIMERS ---
  plc: {
    First_Scan: true,
    M00001: false,
    M00002: false,
    timers: {},
    counters: {},
    tags: {},
    slotI: { 2: new Array(16).fill(0), 3: new Array(16).fill(0), 4: new Array(16).fill(0), 6: new Array(8).fill(0), 7: new Array(32).fill(false), 9: new Array(16).fill(0) },
    slotO: { 8: new Array(32).fill(false) }
  }
};

// Initialize all 33 Analog F&G Detectors on the 2D Quinguila Site Map
function initDetectors() {
  const list = [
    // 12 CH4 Point Detectors 7404-DG-001..012 (Slot 2 Ch 0..11)
    { id:'7404-DG-001', slot:2, ch:0,  type:'CH4', unit:'%LEL', min:0, max:100, lo:20, hi:30, x:180, y:140, zone:'Tank Bund North (T-100)' },
    { id:'7404-DG-002', slot:2, ch:1,  type:'CH4', unit:'%LEL', min:0, max:100, lo:20, hi:30, x:310, y:140, zone:'Tank Bund North (T-200)' },
    { id:'7404-DG-003', slot:2, ch:2,  type:'CH4', unit:'%LEL', min:0, max:100, lo:20, hi:30, x:180, y:290, zone:'Tank Bund South (T-300)' },
    { id:'7404-DG-004', slot:2, ch:3,  type:'CH4', unit:'%LEL', min:0, max:100, lo:20, hi:30, x:310, y:290, zone:'Tank Bund South (T-400)' },
    { id:'7404-DG-005', slot:2, ch:4,  type:'CH4', unit:'%LEL', min:0, max:100, lo:20, hi:30, x:470, y:155, zone:'Heater Treater V-710' },
    { id:'7404-DG-006', slot:2, ch:5,  type:'CH4', unit:'%LEL', min:0, max:100, lo:20, hi:30, x:470, y:275, zone:'Heater Treater V-810' },
    { id:'7404-DG-007', slot:2, ch:6,  type:'CH4', unit:'%LEL', min:0, max:100, lo:20, hi:30, x:640, y:150, zone:'Power Oil Pump House W' },
    { id:'7404-DG-008', slot:2, ch:7,  type:'CH4', unit:'%LEL', min:0, max:100, lo:20, hi:30, x:745, y:150, zone:'Power Oil Pump House E' },
    { id:'7404-DG-009', slot:2, ch:8,  type:'CH4', unit:'%LEL', min:0, max:100, lo:20, hi:30, x:640, y:270, zone:'Water Inj Pump Skid W' },
    { id:'7404-DG-010', slot:2, ch:9,  type:'CH4', unit:'%LEL', min:0, max:100, lo:20, hi:30, x:745, y:270, zone:'Water Inj Pump Skid E' },
    { id:'7404-DG-011', slot:2, ch:10, type:'CH4', unit:'%LEL', min:0, max:100, lo:20, hi:30, x:555, y:390, zone:'Fuel Gas ESDV-001 Skid' },
    { id:'7404-DG-012', slot:2, ch:11, type:'CH4', unit:'%LEL', min:0, max:100, lo:20, hi:30, x:430, y:390, zone:'Oil Expedition Manifold' },
    // Open-Path Detector 7404-DG-011R (Slot 2 Ch 12)
    { id:'7404-DG-011R', slot:2, ch:12, type:'LOS', unit:'LELm', min:0, max:5.0, lo:1.0, hi:3.0, x:690, y:210, zone:'Pump House Open-Path Beam' },
    // 3 New Gas Generator Room CH4 Detectors GD-001..003 (Slot 2 Ch 13..15)
    { id:'GD-001', slot:2, ch:13, type:'CH4_GEN', unit:'%LEL', min:0, max:100, lo:20, hi:30, x:890, y:135, zone:'Gas Generator Room Bay 1' },
    { id:'GD-002', slot:2, ch:14, type:'CH4_GEN', unit:'%LEL', min:0, max:100, lo:20, hi:30, x:960, y:135, zone:'Gas Generator Room Bay 2' },
    { id:'GD-003', slot:2, ch:15, type:'CH4_GEN', unit:'%LEL', min:0, max:100, lo:20, hi:30, x:925, y:195, zone:'Gas Generator Turbine Header' },
    // 12 New H2S Detectors H2S-001..012 (Slot 4 Ch 0..11)
    { id:'H2S-001', slot:4, ch:0,  type:'H2S', unit:'PPM', min:0, max:100, lo:10, hi:20, x:145, y:110, zone:'Tank T-100 Roof Vent' },
    { id:'H2S-002', slot:4, ch:1,  type:'H2S', unit:'PPM', min:0, max:100, lo:10, hi:20, x:345, y:110, zone:'Tank T-200 Roof Vent' },
    { id:'H2S-003', slot:4, ch:2,  type:'H2S', unit:'PPM', min:0, max:100, lo:10, hi:20, x:145, y:320, zone:'Tank T-300 Roof Vent' },
    { id:'H2S-004', slot:4, ch:3,  type:'H2S', unit:'PPM', min:0, max:100, lo:10, hi:20, x:345, y:320, zone:'Tank T-400 Roof Vent' },
    { id:'H2S-005', slot:4, ch:4,  type:'H2S', unit:'PPM', min:0, max:100, lo:10, hi:20, x:495, y:125, zone:'Treater V-710 Gas Boot' },
    { id:'H2S-006', slot:4, ch:5,  type:'H2S', unit:'PPM', min:0, max:100, lo:10, hi:20, x:495, y:305, zone:'Treater V-810 Gas Boot' },
    { id:'H2S-007', slot:4, ch:6,  type:'H2S', unit:'PPM', min:0, max:100, lo:10, hi:20, x:615, y:120, zone:'Power Oil Suction Header' },
    { id:'H2S-008', slot:4, ch:7,  type:'H2S', unit:'PPM', min:0, max:100, lo:10, hi:20, x:770, y:120, zone:'Power Oil Discharge Header' },
    { id:'H2S-009', slot:4, ch:8,  type:'H2S', unit:'PPM', min:0, max:100, lo:10, hi:20, x:615, y:300, zone:'Produced Water Pit' },
    { id:'H2S-010', slot:4, ch:9,  type:'H2S', unit:'PPM', min:0, max:100, lo:10, hi:20, x:770, y:300, zone:'Water Inj Manifold' },
    { id:'H2S-011', slot:4, ch:10, type:'H2S', unit:'PPM', min:0, max:100, lo:10, hi:20, x:395, y:435, zone:'Export Metering Skid' },
    { id:'H2S-012', slot:4, ch:11, type:'H2S', unit:'PPM', min:0, max:100, lo:10, hi:20, x:855, y:385, zone:'PCR Control Room Air Intake' },
    // 3 Flame Detectors 7404-DF-001..003 (Slot 4 Ch 12..14)
    { id:'7404-DF-001', slot:4, ch:12, type:'FLAME', unit:'%', min:0, max:100, lo:30, hi:30, x:245, y:215, zone:'Tank Farm Center Bund IR Flame 1' },
    { id:'7404-DF-002', slot:4, ch:13, type:'FLAME', unit:'%', min:0, max:100, lo:30, hi:30, x:490, y:215, zone:'Treater & Manifold Area Flame 2' },
    { id:'7404-DF-003', slot:4, ch:14, type:'FLAME', unit:'%', min:0, max:100, lo:30, hi:30, x:695, y:185, zone:'Pump House IR Flame 3 (New)' },
    // Smoke Detector SD-001/002 (Slot 4 Ch 15)
    { id:'SD-001/002',  slot:4, ch:15, type:'SMOKE', unit:'%', min:0, max:100, lo:30, hi:30, x:920, y:335, zone:'Electrical & PCR Room Smoke' },
    // 2 Manual Foam Release Call Points (Slot 3 Ch 6 & 7)
    { id:'7503-FR-001/002', slot:3, ch:7, type:'MAC', unit:'%', min:0, max:100, lo:30, hi:30, x:250, y:460, zone:'Outside Bund Foam Release MAC' },
    { id:'7503-FR-003',     slot:3, ch:6, type:'MAC', unit:'%', min:0, max:100, lo:30, hi:30, x:885, y:435, zone:'Inside PCR Foam Release MAC' }
  ];

  SimState.detectors = list.map(d => ({
    ...d,
    manualVal: 0.0,
    plumeVal: 0.0,
    val: 0.0,
    faultMode: 'NONE', // 'NONE' | 'WIRE_BREAK' | 'OVERRANGE' | 'OPTIC_BLOCK'
    inhibited: false,
    loActive: false,
    hiActive: false,
    faultActive: false
  }));
}
initDetectors();
"""

JS_ENGINE_PART2 = r"""
// ============================================================================
// 3. CONTINUOUS-TIME PHYSICAL TWIN ODE ENGINE (stepPhysicalTwin)
// ============================================================================
function stepPhysicalTwin(dt) {
  const p = SimState.phys;
  const plc = SimState.plc;
  const t = plc.tags;

  // --- A. 2D GAUSSIAN PLUME ADVECTION & DETECTOR SENSING ---
  const windRad = (SimState.windDirDeg * Math.PI) / 180.0;
  const wx = Math.cos(windRad) * SimState.windSpeedMs;
  const wy = Math.sin(windRad) * SimState.windSpeedMs;

  // Update each detector's plume contribution
  for (const d of SimState.detectors) {
    let pContrib = 0.0;
    for (const pl of SimState.plumes) {
      const match =
        (pl.type === 'CH4' && (d.type === 'CH4' || d.type === 'CH4_GEN' || d.type === 'LOS')) ||
        (pl.type === 'H2S' && d.type === 'H2S') ||
        (pl.type === 'FIRE' && d.type === 'FLAME') ||
        (pl.type === 'SMOKE' && d.type === 'SMOKE');
      if (!match) continue;

      const dx = d.x - pl.x;
      const dy = d.y - pl.y;
      const dist = Math.hypot(dx, dy);

      if (pl.type === 'FIRE') {
        // Radiant heat inverse-square + line-of-sight cone
        const rad = Math.max(25, pl.strength * 2.2);
        if (dist < rad * 1.6) {
          const inten = pl.strength * Math.exp(-(dist * dist) / (2 * rad * rad));
          pContrib = Math.max(pContrib, inten);
        }
      } else {
        // Advected Gaussian gas/smoke plume along wind vector
        const along = (dx * Math.cos(windRad) + dy * Math.sin(windRad));
        const cross = (-dx * Math.sin(windRad) + dy * Math.cos(windRad));
        const effAlong = along > 0 ? along / (1.0 + 0.18 * SimState.windSpeedMs) : along * 1.8;
        const sigma = 65 + Math.max(0, along) * 0.28;
        const conc = pl.strength * Math.exp(-(effAlong * effAlong + cross * cross * 1.8) / (2 * sigma * sigma));
        if (d.type === 'LOS') {
          pContrib = Math.max(pContrib, (conc / 100.0) * 5.0);
        } else {
          pContrib = Math.max(pContrib, conc);
        }
      }
    }
    d.plumeVal = pContrib;
    if (d.faultMode === 'WIRE_BREAK') {
      d.val = d.type === 'LOS' ? -0.95 : -6.5;
    } else if (d.faultMode === 'OVERRANGE') {
      d.val = d.type === 'LOS' ? 5.25 : 108.0;
    } else if (d.faultMode === 'OPTIC_BLOCK' && d.type === 'LOS') {
      d.val = -0.62; // Inside -0.78125 .. -0.46875 LELm beam block window
    } else {
      d.val = Math.min(d.max * 1.04, Math.max(d.min, d.manualVal + d.plumeVal));
    }
  }

  if (!SimState.coupledPhysics) return;

  // --- B. PNEUMATIC AIR ACCUMULATOR (7002-PST-001) & ESDV-001 (6401-ESDV-001) ---
  if (p.airLeakFault) {
    p.airAccPsi = Math.max(15.0, p.airAccPsi - 8.5 * dt);
  } else if (p.airCompressorOn) {
    p.airAccPsi += (82.0 - p.airAccPsi) * 0.6 * dt;
  } else {
    p.airAccPsi = Math.max(0.0, p.airAccPsi - 1.2 * dt);
  }

  // Solenoid 6401-EY-001/002 is Local:8:O.Data.1 (energized = open valve if air > 35 Psi)
  const eyEnergized = plc.slotO[8][1];
  if (!p.esdvStuckFault) {
    if (eyEnergized && p.airAccPsi > 35.0) {
      p.esdvPositionPct = Math.min(100.0, p.esdvPositionPct + 42.0 * dt); // 2.4s stroke open
    } else {
      p.esdvPositionPct = Math.max(0.0, p.esdvPositionPct - 55.0 * dt);   // 1.8s spring-return close
    }
  }

  // Fuel Gas Line Pressure 6401-PST-001 responds to ESDV position & upstream supply
  const targetFuelGasPsi = p.fuelGasSupplyPsi * (p.esdvPositionPct / 100.0);
  p.fuelGasLinePsi += (targetFuelGasPsi - p.fuelGasLinePsi) * Math.min(1.0, 2.5 * dt);

  // --- C. GAS GENERATORS (GE-01 / GE-02) ---
  const sdGeTrip = plc.slotO[8][21]; // SD_GE (Local:8:O.Data.21)
  if (sdGeTrip || p.fuelGasLinePsi < 25.0) {
    p.gasGenRunning = false;
  } else if (plc.tags.M00002_System_Reset) {
    p.gasGenRunning = true;
  }

  // --- D. POWER OIL BOOSTER & MULTIPLEX PUMPS (P-2100/2200, P-2300..P-2600, PIT-003) ---
  const oilBoosterHealthy = plc.slotO[8][8]; // P2100_P2200 (1=Healthy, 0=Trip)
  p.oilBoosterRun = oilBoosterHealthy;

  const crStops = [
    plc.slotO[8][15], // CR1 P-2300 Stop
    plc.slotO[8][16], // CR2 P-2400 Stop
    plc.slotO[8][17], // CR3 P-2500 Stop
    plc.slotO[8][18]  // CR4 P-2600 Stop
  ];
  const poKeys = ['P2300', 'P2400', 'P2500', 'P2600'];
  let activeOilPumps = 0;
  poKeys.forEach((k, idx) => {
    const pump = p.powerOilPumps[k];
    if (crStops[idx] || !p.oilBoosterRun) {
      pump.running = false;
      pump.rpm = Math.max(0, pump.rpm - 900 * dt);
    } else if (pump.cmdRun) {
      pump.running = true;
      pump.rpm += (1650 - pump.rpm) * Math.min(1.0, 2.0 * dt);
    } else {
      pump.running = false;
      pump.rpm = Math.max(0, pump.rpm - 600 * dt);
    }
    if (pump.rpm > 400) activeOilPumps += (pump.rpm / 1650.0);
  });

  // Power Oil Manifold Pressure PIT-003 ODE (normal ~2150 Psi with 3 pumps & 68% choke)
  const chokeFactorOil = Math.max(0.15, p.oilWellChokePct / 68.0);
  const targetOilPsi = activeOilPumps > 0 ? (activeOilPumps * 716.0) / chokeFactorOil : 0.0;
  p.oilManifoldPsi += (targetOilPsi - p.oilManifoldPsi) * Math.min(1.0, 1.8 * dt);

  // --- E. WATER INJECTION BOOSTER & TRIPLEX PUMPS (P-3600/3700, P-3800/3900, PIT-002) ---
  const waterBoosterHealthy = plc.slotO[8][9]; // P3600_P3700 (1=Healthy, 0=Trip)
  p.waterBoosterRun = waterBoosterHealthy;

  const wiStops = [plc.slotO[8][19], plc.slotO[8][20]]; // CR5, CR6
  const wiKeys = ['P3800', 'P3900'];
  let activeWaterPumps = 0;
  wiKeys.forEach((k, idx) => {
    const pump = p.waterInjPumps[k];
    if (wiStops[idx] || !p.waterBoosterRun) {
      pump.running = false;
      pump.rpm = Math.max(0, pump.rpm - 900 * dt);
    } else if (pump.cmdRun) {
      pump.running = true;
      pump.rpm += (1580 - pump.rpm) * Math.min(1.0, 2.0 * dt);
    } else {
      pump.running = false;
      pump.rpm = Math.max(0, pump.rpm - 600 * dt);
    }
    if (pump.rpm > 400) activeWaterPumps += (pump.rpm / 1580.0);
  });

  const chokeFactorWater = Math.max(0.18, p.waterWellChokePct / 70.0);
  const targetWaterPsi = activeWaterPumps > 0 ? (activeWaterPumps * 270.0) / chokeFactorWater : 0.0;
  p.waterManifoldPsi += (targetWaterPsi - p.waterManifoldPsi) * Math.min(1.0, 1.8 * dt);

  // --- F. CRUDE STORAGE TANKS (T-100..T-400) & EXPEDITION MANIFOLD (PIT-001, FT-001) ---
  let totalExportBblH = 0.0;
  Object.keys(p.tanks).forEach(tk => {
    const tank = p.tanks[tk];
    const qIn = (p.treaters.V710.online || p.treaters.V810.online) ? tank.fillBblH * (tank.inValve / 100.0) : 0.0;
    const qOut = p.esdvPositionPct > 50 ? tank.drainBblH * (tank.outValve / 100.0) * (p.oilExpChokePct / 75.0) : 0.0;
    totalExportBblH += qOut;
    // Convert bbl/h to m/s (scaled by 60x so level dynamics are visible during interactive testing)
    const dLevel = ((qIn - qOut) * 0.159 / tank.areaM2) * (dt / 60.0);
    tank.level = Math.max(0.0, Math.min(tank.maxH, tank.level + dLevel));
  });

  p.oilExpFlowBblH += (totalExportBblH - p.oilExpFlowBblH) * Math.min(1.0, 2.0 * dt);
  const targetExpPsi = p.oilExpFlowBblH > 5 ? 22.0 + (p.oilExpFlowBblH * 0.195) / Math.max(0.2, p.oilExpChokePct / 75.0) : 4.0;
  p.oilExpPressPsi += (targetExpPsi - p.oilExpPressPsi) * Math.min(1.0, 2.0 * dt);

  // --- G. FIREWATER & FOAM DELUGE HYDRAULICS (PUMP_A, PUMP_B, 7503-PST-001) ---
  const cmdPumpA = plc.slotO[8][4]; // PUMP_A (Local:8:O.Data.4)
  const cmdPumpBStart = plc.slotO[8][6]; // PUMP_B_START (Local:8:O.Data.6)
  const cmdPumpBStop = plc.slotO[8][7];  // PUMP_B_STOP (Local:8:O.Data.7)

  p.pumpARunning = cmdPumpA && !p.pumpAFailFault && !p.pumpAWireBreak;

  if (cmdPumpBStop || p.dieselTankPct <= 2.0) {
    p.pumpBRunning = false;
  } else if (cmdPumpBStart && !p.pumpBWireBreak && !SimState.di.Pump_B_Inhibited) {
    p.pumpBRunning = true;
  }

  const anyDelugePump = p.pumpARunning || p.pumpBRunning;
  const targetDelugePsi = anyDelugePump ? 78.0 : 0.0;
  p.delugeLinePsi += (targetDelugePsi - p.delugeLinePsi) * Math.min(1.0, 1.5 * dt);
  p.delugeValveOpenPct = p.delugeLinePsi > 35.0 ? 100.0 : 0.0;

  if (p.delugeLinePsi > 45.0) {
    p.foamTankPct = Math.max(0.0, p.foamTankPct - 0.35 * dt);
    // Deluge foam suppresses active fires gradually
    for (const pl of SimState.plumes) {
      if (pl.type === 'FIRE') pl.strength = Math.max(0, pl.strength - 6.0 * dt);
    }
  }
  if (p.pumpBRunning) {
    p.dieselTankPct = Math.max(0.0, p.dieselTankPct - 0.20 * dt);
  }
}

// ============================================================================
// 4. CONTROLLOGIX 5580 (1756-L82E) SOFT-PLC ENGINE (25 ST ROUTINES)
// ============================================================================
function evalTONR(name, enable, preMs, reset, dtMs) {
  const tmrs = SimState.plc.timers;
  if (!tmrs[name]) tmrs[name] = { PRE: preMs, ACC: 0, EN: false, TT: false, DN: false };
  const t = tmrs[name];
  t.PRE = preMs;
  if (reset) {
    t.ACC = 0; t.EN = false; t.TT = false; t.DN = false;
    return t;
  }
  if (enable) {
    t.EN = true;
    if (t.ACC < t.PRE) {
      t.ACC = Math.min(t.PRE, t.ACC + dtMs);
    }
    t.DN = (t.ACC >= t.PRE);
    t.TT = !t.DN;
  } else {
    t.EN = false;
    t.TT = false;
    if (!t.DN) t.ACC = 0;
  }
  return t;
}

function euToRaw(eu, zero, span) {
  return Math.round(((eu - zero) / (span - zero)) * 32000.0);
}

function stepSoftPLC(dtMs) {
  const p = SimState.phys;
  const di = SimState.di;
  const plc = SimState.plc;
  const T = plc.tags;
  const sI = plc.slotI;
  const sO = plc.slotO;

  // --- HARDWARE INPUT IMAGE UPDATE (1756-IF16, 1756-IF8H, 1756-IB32, MVI56E-MCM) ---
  // Slot 7: 1756-IB32 Digital Inputs (0..20)
  sI[7][0]  = (p.esdvPositionPct >= 95.0);        // 6401-ZSH-001 ESDV Open
  sI[7][1]  = (p.esdvPositionPct <= 5.0);         // 6401-ZSL-001 ESDV Closed
  sI[7][2]  = Boolean(di.FS_FGCP_E8);             // FS_FGCP_E8 Panel Foam Stop (NO: 1=Stop)
  sI[7][3]  = (p.dieselTankPct >= 20.0);          // 7503-LS-002 Diesel Tank Low (NC: 1=OK, 0=Low)
  sI[7][4]  = !di.FS_7503_001_Pressed;            // 7503-FS-001 Field Foam Stop (NC: 1=OK, 0=Stop)
  sI[7][5]  = (p.foamTankPct >= 20.0);            // 7503-LS-001 AFFF Foam Tank Low (NC: 1=OK, 0=Low)
  sI[7][6]  = !p.pumpAWireBreak && (sO[8][3] || p.pumpARunning); // 75-C-01A Pulse feedback
  sI[7][7]  = !p.pumpBWireBreak && (sO[8][5] || p.pumpBRunning); // 75-C-01B Pulse feedback
  sI[7][8]  = Boolean(di.Pump_B_Inhibited);       // 75-SB-01B Standby Pump B Inhibited
  sI[7][9]  = false;                              // SpareDI_11
  sI[7][10] = Boolean(di.Reset_PB_E11);           // Reset_PB_E11
  sI[7][11] = Boolean(di.Mute_PB_E12);            // Mute_PB_E12
  sI[7][12] = !di.ESDV_6401_E9_Pressed;           // 6401-ESDV-001 E9 Pushbutton (NC: 1=Healthy, 0=Pressed)
  sI[7][13] = Boolean(di.INHIBIT_FOAM_REL);       // S2 Inhibit Foam Release
  sI[7][14] = Boolean(di.INHIBIT_ALL_OUTPUTS);    // S3 Inhibit All Outputs
  sI[7][15] = Boolean(di.ESTOP_P2300_E1);         // E1
  sI[7][16] = Boolean(di.ESTOP_P2400_E2);         // E2
  sI[7][17] = Boolean(di.ESTOP_P2500_E3);         // E3
  sI[7][18] = Boolean(di.ESTOP_P2600_E4);         // E4
  sI[7][19] = Boolean(di.ESTOP_P3800_E5);         // E5
  sI[7][20] = Boolean(di.ESTOP_P3900_E6);         // E6

  // Map Detectors to Slots 2, 3, 4
  for (const d of SimState.detectors) {
    const effVal = d.inhibited ? 0.0 : d.val;
    sI[d.slot][d.ch] = euToRaw(effVal, d.min, d.max);
  }
  // Slot 3 Process Pressure Transmitters
  sI[3][0] = euToRaw(p.oilExpPressPsi, 0, 200);    // PIT-001 (0-200 Psi)
  sI[3][1] = euToRaw(p.waterManifoldPsi, 0, 1500); // PIT-002 (0-1500 Psi)
  sI[3][2] = euToRaw(p.oilManifoldPsi, 0, 3000);   // PIT-003 (0-3000 Psi)
  sI[3][3] = euToRaw(p.delugeLinePsi, 0, 100);     // 7503-PST-001 (0-100 Psi)
  sI[3][4] = euToRaw(p.airAccPsi, 0, 100);         // 7002-PST-001 (0-100 Psi)
  sI[3][5] = euToRaw(p.fuelGasLinePsi, 0, 150);    // 6401-PST-001 (0-150 Psi)

  // Slot 6: 1756-IF8H Radar Tank Level Transmitters (LIT-100..400)
  sI[6][0] = euToRaw(p.tanks.T100.level, 0, 10.0);
  sI[6][1] = euToRaw(p.tanks.T200.level, 0, 10.0);
  sI[6][2] = euToRaw(p.tanks.T300.level, 0, 10.0);
  sI[6][3] = euToRaw(p.tanks.T400.level, 0, 12.0);

  // Slot 9: MVI56E-MCM Modbus Registers
  sI[9][0] = p.powerOilPumps.P2300.running ? 1 : 0;
  sI[9][1] = p.powerOilPumps.P2400.running ? 1 : 0;
  sI[9][2] = p.powerOilPumps.P2500.running ? 1 : 0;
  sI[9][3] = p.powerOilPumps.P2600.running ? 1 : 0;
  sI[9][4] = p.waterInjPumps.P3800.running ? 1 : 0;
  sI[9][5] = p.waterInjPumps.P3900.running ? 1 : 0;
  sI[9][6] = Math.round(p.oilExpFlowBblH * 10.0); // 6401-FT-001 (0.1 bbl/h units)

  // ==========================================================================
  // ROUTINE 1 & 2: MainRoutine + Init
  // ==========================================================================
  if (plc.First_Scan) {
    T.R01598_0 = false; T.R01598_1 = false;
    T.SP_GD_Low_LEL = 20.0; T.SP_GD_High_LEL = 30.0;
    T.SP_H2S_Low_PPM = 10.0; T.SP_H2S_High_PPM = 20.0;
    T.SP_DF003_High = 30.0; T.SP_SD_High = 30.0;
    T.SP_PIT001_PAL = 10.0; T.SP_PIT001_PAH = 100.0;
    T.SP_PIT002_PAL = 200.0; T.SP_PIT002_PAH = 800.0; T.SP_PIT002_PAHH = 900.0;
    T.SP_PIT003_PAL = 1700.0; T.SP_PIT003_PAH = 2700.0; T.SP_PIT003_PAHH = 2800.0;
    T.SP_LIT100_LAL = 0.7; T.SP_LIT100_LAH = 9.0;
    T.SP_LIT200_LAL = 0.7; T.SP_LIT200_LAH = 9.0;
    T.SP_LIT300_LAL = 0.7; T.SP_LIT300_LAH = 9.0;
    T.SP_LIT400_LAL = 0.7; T.SP_LIT400_LAH = 11.0;
    T.SP_FT001_FAL = 30.0; T.SP_FT001_FAH = 300.0;
  }

  // Free-running 400ms flasher oscillator (R01598_0)
  const tSlow = evalTONR('TMR_Flash_Slow', !(plc.timers.TMR_Flash_Fast && plc.timers.TMR_Flash_Fast.DN), 400, plc.First_Scan, dtMs);
  const tFast = evalTONR('TMR_Flash_Fast', tSlow.DN, 400, plc.First_Scan, dtMs);
  if (tSlow.DN && !T.R01598_1) T.R01598_0 = !T.R01598_0;
  T.R01598_1 = tSlow.DN;
  if (tFast.DN) {
    plc.timers.TMR_Flash_Slow.ACC = 0; plc.timers.TMR_Flash_Slow.DN = false;
    plc.timers.TMR_Flash_Fast.ACC = 0; plc.timers.TMR_Flash_Fast.DN = false;
  }

  // ==========================================================================
  // ROUTINE 3, 4, 5: Input, DI_1, DI_2
  // ==========================================================================
  T.ZSH_6401_001 = sI[7][0]; T.G0001 = sI[7][0];
  T.ZSL_6401_001 = sI[7][1]; T.G0002 = sI[7][1];
  T.FS_FGCP_E8   = sI[7][2]; T.G0008 = sI[7][2];
  T.LS_7503_002  = sI[7][3]; T.G0005 = sI[7][3];
  T.FS_7503_001  = sI[7][4]; T.G0003 = sI[7][4];
  T.LS_7503_001  = sI[7][5]; T.G0004 = sI[7][5];
  T.Pump_A_PulsIn = sI[7][6]; T.G0006 = sI[7][6];
  T.Pump_B_Start_PulsIn = sI[7][7]; T.G0007 = sI[7][7];
  T.Pump_B_Inhibited = sI[7][8]; T.G0009 = sI[7][8];
  T.Reset_PB_E11 = sI[7][10];
  T.Mute_PB_E12  = sI[7][11];
  T.ESDV_6401_001 = sI[7][12]; T.G0010 = sI[7][12];
  T.INHIBIT_FOAM_REL = sI[7][13]; T.G0012 = sI[7][13];
  T.INHIBIT_ALL_OUTPUTS = sI[7][14]; T.G0013 = sI[7][14];
  T.ESTOP_P2300_E1 = sI[7][15];
  T.ESTOP_P2400_E2 = sI[7][16];
  T.ESTOP_P2500_E3 = sI[7][17];
  T.ESTOP_P2600_E4 = sI[7][18];
  T.ESTOP_P3800_E5 = sI[7][19];
  T.ESTOP_P3900_E6 = sI[7][20];

  T.M00001_System_Accept = Boolean(plc.M00001 || T.Mute_PB_E12);
  T.M00002_System_Reset  = Boolean(plc.M00002 || T.Reset_PB_E11);

  // DI_1: ESDV Position & Discrepancy Timers (10.0s)
  T.R00700_0 = T.G0001; // Open
  T.R00700_1 = T.G0002; // Closed
  T.R00700_2 = T.R00700_0 && T.R00700_1;
  T.R00700_3 = evalTONR('TMR_ESDV_Transit', !T.R00700_0 && !T.R00700_1, 10000, T.M00002_System_Reset, dtMs).DN;
  T.R00700_4 = evalTONR('TMR_ESDV_CmdOpen', Boolean(T.R01511_0) && !T.R00700_0, 10000, T.M00002_System_Reset, dtMs).DN;
  T.R00700_5 = evalTONR('TMR_ESDV_CmdClose', !T.R01511_0 && !T.R00700_1, 10000, T.M00002_System_Reset, dtMs).DN;
  if (T.R00700_2 || T.R00700_3 || T.R00700_4 || T.R00700_5) T.R00700_6 = true;
  else if (T.M00002_System_Reset) T.R00700_6 = false;

  // Foam Stop (Field NC G0003 or Panel NO G0008)
  T.R00701_0 = (!T.G0003) || T.G0008;
  if (T.R00701_0) T.R00701_1 = true;
  else if (T.M00002_System_Reset) T.R00701_1 = false;

  // AFFF Foam Tank Low Level (NC G0004) & Diesel Tank Low Level (NC G0005)
  T.R00702_0 = !T.G0004;
  if (T.R00702_0) T.R00702_1 = true; else if (T.M00002_System_Reset) T.R00702_1 = false;
  T.R00703_0 = !T.G0005;
  if (T.R00703_0) T.R00703_1 = true; else if (T.M00002_System_Reset) T.R00703_1 = false;

  // DI_2: Pump A & B Coil Continuity Check, E9 ESD Button, Keyswitches S2/S3, E1..E6
  T.R00704_1 = Boolean(p.pumpAWireBreak);
  T.R00705_1 = Boolean(p.pumpBWireBreak);
  T.R00706_0 = T.G0009; // Pump B Inhibited
  T.R00707_0 = !T.G0010; // E9 Pressed
  if (T.R00707_0) T.R00707_1 = true;
  else if (T.M00002_System_Reset && !T.R00707_0) T.R00707_1 = false;

  T.R00708_0 = T.G0012; // S2 Inhibit Foam Release
  T.R00709_0 = T.G0013; // S3 Inhibit All Outputs

  if (T.ESTOP_P2300_E1) T.Latch_ESTOP_P2300 = true; else if (T.M00002_System_Reset) T.Latch_ESTOP_P2300 = false;
  if (T.ESTOP_P2400_E2) T.Latch_ESTOP_P2400 = true; else if (T.M00002_System_Reset) T.Latch_ESTOP_P2400 = false;
  if (T.ESTOP_P2500_E3) T.Latch_ESTOP_P2500 = true; else if (T.M00002_System_Reset) T.Latch_ESTOP_P2500 = false;
  if (T.ESTOP_P2600_E4) T.Latch_ESTOP_P2600 = true; else if (T.M00002_System_Reset) T.Latch_ESTOP_P2600 = false;
  if (T.ESTOP_P3800_E5) T.Latch_ESTOP_P3800 = true; else if (T.M00002_System_Reset) T.Latch_ESTOP_P3800 = false;
  if (T.ESTOP_P3900_E6) T.Latch_ESTOP_P3900 = true; else if (T.M00002_System_Reset) T.Latch_ESTOP_P3900 = false;

  // ==========================================================================
  // ROUTINE 6..15: AI_1..AI_4_New, CalcVa1..3, Ai_AL_1..3, Vote_1
  // ==========================================================================
  let gasLoCnt = 0;
  let gasHiCnt = 0;
  let flameCnt = 0;
  let anyDetectorFault = false;

  // Evaluate all detectors & latch alarms
  const detMap = {};
  for (const d of SimState.detectors) {
    detMap[d.id] = d;
    if (d.inhibited) {
      d.faultActive = false; d.loActive = false; d.hiActive = false;
      continue;
    }
    if (d.type === 'LOS') {
      const hiFlt = d.val > 5.10;
      const loFlt = d.val < -0.78125;
      const optFlt = d.val >= -0.78125 && d.val <= -0.46875;
      d.faultActive = hiFlt || loFlt || optFlt;
      T.R00373 = d.val; T.R00375_2 = d.faultActive; T.R00375_7 = optFlt;
    } else {
      d.faultActive = (d.val > 105.0) || (d.val < -4.0);
    }
    if (d.faultActive) anyDetectorFault = true;

    const liveLo = !d.faultActive && (d.val >= d.lo);
    const liveHi = !d.faultActive && (d.val >= d.hi);

    if (liveLo) d.loActive = true;
    else if (T.M00002_System_Reset) d.loActive = false;

    if (liveHi) d.hiActive = true;
    else if (T.M00002_System_Reset) d.hiActive = false;

    if (d.type === 'CH4' || d.type === 'LOS') {
      if (d.loActive) gasLoCnt++;
      if (d.hiActive) gasHiCnt++;
    } else if (d.type === 'FLAME') {
      if (d.hiActive) flameCnt++;
    }
  }

  // Populate Legacy R00113..R00395_6 tags for ST Debugger fidelity
  const dgIds = ['7404-DG-001','7404-DG-002','7404-DG-003','7404-DG-004','7404-DG-005','7404-DG-006','7404-DG-007','7404-DG-008','7404-DG-009','7404-DG-010','7404-DG-011'];
  const regBases = [113,133,153,173,193,213,233,253,273,293,313];
  dgIds.forEach((id, i) => {
    const d = detMap[id];
    const b = regBases[i];
    const fb = b + 2;
    T[`R00${b}`] = d.val;
    T[`R00${fb}_2`] = d.faultActive;
    T[`R00${fb}_5`] = d.hiActive;
    T[`R00${fb}_6`] = d.loActive;
  });
  T.R00393 = detMap['7404-DG-012'].val;
  T.R00395_2 = detMap['7404-DG-012'].faultActive;
  T.R00395_5 = detMap['7404-DG-012'].hiActive;
  T.R00395_6 = detMap['7404-DG-012'].loActive;

  T.R00375_5 = detMap['7404-DG-011R'].hiActive;
  T.R00375_6 = detMap['7404-DG-011R'].loActive;

  T.R00333 = detMap['7404-DF-001'].val; T.R00335_5 = detMap['7404-DF-001'].hiActive;
  T.R00353 = detMap['7404-DF-002'].val; T.R00355_5 = detMap['7404-DF-002'].hiActive;
  T.DF_7404_003_EU = detMap['7404-DF-003'].val; T.DF_7404_003_Latch = detMap['7404-DF-003'].hiActive;

  // Foam MACs 7503-FR-001/002 & 7503-FR-003
  T.R00493 = detMap['7503-FR-001/002'].val; T.R00495_5 = detMap['7503-FR-001/002'].hiActive;
  T.R00533 = detMap['7503-FR-003'].val;     T.R00535_5 = detMap['7503-FR-003'].hiActive;

  // 7002-PST-001 Air Accumulator (PAL <= 50 Psi -> R00435_6)
  T.R00433 = p.airAccPsi;
  T.R00435_4 = (p.airAccPsi <= 50.0);
  if (T.R00435_4) T.R00435_6 = true;
  else if (T.M00002_System_Reset) T.R00435_6 = false;

  // 6401-PST-001 Fuel Gas Line (PAL <= 40 Psi -> R00455_6, PAH >= 100 Psi -> R00455_5)
  T.R00453 = p.fuelGasLinePsi;
  T.R00455_3 = (p.fuelGasLinePsi >= 100.0);
  T.R00455_4 = (p.fuelGasLinePsi <= 40.0);
  if (T.R00455_3) T.R00455_5 = true; else if (T.M00002_System_Reset) T.R00455_5 = false;
  if (T.R00455_4) T.R00455_6 = true; else if (T.M00002_System_Reset) T.R00455_6 = false;

  // 7503-PST-001 Deluge Line Pressure (PAH >= 50 Psi -> R00475_5)
  T.R00473 = p.delugeLinePsi;
  T.R00475_3 = (p.delugeLinePsi >= 50.0);
  if (T.R00475_3) T.R00475_5 = true;
  else if (T.M00002_System_Reset && !T.R00475_3) T.R00475_5 = false;

  // AI_4_New: GD-001..003, PIT-001..003, H2S-001..012, SD-001/002, LIT-100..400, FT-001
  T.GD_001_EU = detMap['GD-001'].val; T.GD_002_EU = detMap['GD-002'].val; T.GD_003_EU = detMap['GD-003'].val;
  T.GD_Any_Lo_Latch = detMap['GD-001'].loActive || detMap['GD-002'].loActive || detMap['GD-003'].loActive;
  T.GD_Any_Hi_Latch = detMap['GD-001'].hiActive || detMap['GD-002'].hiActive || detMap['GD-003'].hiActive;

  T.PIT_001_EU = p.oilExpPressPsi;
  T.PIT_001_PAL = (p.oilExpPressPsi <= T.SP_PIT001_PAL);
  T.PIT_001_PAH = (p.oilExpPressPsi >= T.SP_PIT001_PAH);

  T.PIT_002_EU = p.waterManifoldPsi;
  T.PIT_002_PAL = (p.waterManifoldPsi <= T.SP_PIT002_PAL);
  T.PIT_002_PAH = (p.waterManifoldPsi >= T.SP_PIT002_PAH);
  T.PIT_002_PAHH = (p.waterManifoldPsi >= T.SP_PIT002_PAHH);
  if (T.PIT_002_PAHH) T.PIT_002_PAHH_Latch = true;
  else if (T.M00002_System_Reset && !T.PIT_002_PAHH) T.PIT_002_PAHH_Latch = false;

  T.PIT_003_EU = p.oilManifoldPsi;
  T.PIT_003_PAL = (p.oilManifoldPsi <= T.SP_PIT003_PAL);
  T.PIT_003_PAH = (p.oilManifoldPsi >= T.SP_PIT003_PAH);
  T.PIT_003_PAHH = (p.oilManifoldPsi >= T.SP_PIT003_PAHH);
  if (T.PIT_003_PAHH) T.PIT_003_PAHH_Latch = true;
  else if (T.M00002_System_Reset && !T.PIT_003_PAHH) T.PIT_003_PAHH_Latch = false;

  let h2sLo = false, h2sHi = false;
  for (let i = 1; i <= 12; i++) {
    const id = `H2S-${String(i).padStart(3,'0')}`;
    const d = detMap[id];
    T[`H2S_${String(i).padStart(3,'0')}_EU`] = d.val;
    if (d.loActive) h2sLo = true;
    if (d.hiActive) h2sHi = true;
  }
  T.H2S_Any_Lo = h2sLo; T.H2S_Lo_Latch = h2sLo;
  T.H2S_Any_Hi = h2sHi; T.H2S_Hi_Latch = h2sHi;

  T.SD_001_002_EU = detMap['SD-001/002'].val;
  T.SD_001_002_Latch = detMap['SD-001/002'].hiActive;

  T.LIT_100_EU = p.tanks.T100.level; T.LIT_100_LAL = (T.LIT_100_EU <= T.SP_LIT100_LAL); T.LIT_100_LAH = (T.LIT_100_EU >= T.SP_LIT100_LAH);
  T.LIT_200_EU = p.tanks.T200.level; T.LIT_200_LAL = (T.LIT_200_EU <= T.SP_LIT200_LAL); T.LIT_200_LAH = (T.LIT_200_EU >= T.SP_LIT200_LAH);
  T.LIT_300_EU = p.tanks.T300.level; T.LIT_300_LAL = (T.LIT_300_EU <= T.SP_LIT300_LAL); T.LIT_300_LAH = (T.LIT_300_EU >= T.SP_LIT300_LAH);
  T.LIT_400_EU = p.tanks.T400.level; T.LIT_400_LAL = (T.LIT_400_EU <= T.SP_LIT400_LAL); T.LIT_400_LAH = (T.LIT_400_EU >= T.SP_LIT400_LAH);

  T.FT_6401_001_EU  = p.oilExpFlowBblH;
  T.FT_6401_001_FAL = (T.FT_6401_001_EU <= T.SP_FT001_FAL);
  T.FT_6401_001_FAH = (T.FT_6401_001_EU >= T.SP_FT001_FAH);

  // Vote_1
  T.Vote_Gas_Lo_Count = gasLoCnt;
  T.Vote_Gas_Hi_Count = gasHiCnt;
  T.R01500_0 = (gasLoCnt >= 1);
  T.R01500_1 = (gasLoCnt >= 2);
  T.R01500_2 = (gasHiCnt >= 1);
  T.R01500_3 = (gasHiCnt >= 2) || Boolean(T.R00375_5);
  T.Vote_Flame_Count = flameCnt;
  T.R01501_0 = (flameCnt >= 1);
  T.R01501_1 = (flameCnt >= 2);

  // ==========================================================================
  // ROUTINE 17: Logic (Deluge Firewater Pump A & Standby Diesel Pump B)
  // ==========================================================================
  T.Foam_Release_Demand = (T.R01501_0 || T.R00495_5 || T.R00535_5) && !T.R00708_0 && !T.R00709_0 && !T.R00701_0;
  if (T.Foam_Release_Demand && !T.R00704_1) T.R01512_0 = true;
  else if (T.R00701_0 || T.M00002_System_Reset || !T.Foam_Release_Demand) T.R01512_0 = false;

  const tPumpAFail = evalTONR('TMR_PumpA_FailToRun', T.Foam_Release_Demand && !T.R00475_3, 10000, T.M00002_System_Reset || T.R00701_0 || !T.Foam_Release_Demand, dtMs);
  T.Pump_B_Demand = T.Foam_Release_Demand && (tPumpAFail.DN || T.R00704_1) && !T.R00706_0 && !T.R00703_0;
  T.R01512_5 = Boolean(T.Pump_B_Demand);
  T.R01512_4 = Boolean(T.R00701_0);

  // ==========================================================================
  // ROUTINE 18..25: CE_LOG -> Indicat, Shutdow, Protect, Loc_Al, FLT_1, Sound, Output
  // ==========================================================================
  // Shutdow
  T.ESD_Trip_Condition = Boolean((T.R01500_2 || T.R01500_3 || T.R01501_0 || T.R00495_5 || T.R00535_5 || T.R00475_5 || T.R00455_5) && !T.R00709_0);
  T.R01510_0 = !T.ESD_Trip_Condition; // PumpShutdown (1=Healthy, 0=Trip)
  T.R01511_0 = !(T.ESD_Trip_Condition || (T.R00707_1 && !T.R00709_0)); // 6401-EY-001/002
  T.R01511_1 = !(T.ESD_Trip_Condition || (T.PIT_003_PAHH_Latch && !T.R00709_0) || (T.R00707_1 && !T.R00709_0)); // P2100/2200
  T.R01511_2 = !(T.ESD_Trip_Condition || (T.PIT_002_PAHH_Latch && !T.R00709_0) || (T.R00707_1 && !T.R00709_0)); // P3600/3700
  T.SD_GE    = Boolean((T.GD_Any_Hi_Latch || T.SD_001_002_Latch || T.ESD_Trip_Condition) && !T.R00709_0);

  // Indicat
  T.R01513_0 = T.R00700_0; // L15 ESDV Open
  T.R01513_1 = T.R00700_1; // L14 ESDV Closed
  T.R01513_2 = Boolean(T.R00435_6); // L16 Low Air
  T.LED_Low_Fuel_Gas_L17 = Boolean(T.R00455_6); // L17 Low Fuel Gas

  const fullPumpTrip = (!T.R01510_0) || (T.R00707_1 && !T.R00709_0) || !T.R00700_0;
  T.CR1_P2300_Stop = Boolean((T.Latch_ESTOP_P2300 || fullPumpTrip || T.PIT_003_PAHH_Latch) && !T.R00709_0);
  T.CR2_P2400_Stop = Boolean((T.Latch_ESTOP_P2400 || fullPumpTrip || T.PIT_003_PAHH_Latch) && !T.R00709_0);
  T.CR3_P2500_Stop = Boolean((T.Latch_ESTOP_P2500 || fullPumpTrip || T.PIT_003_PAHH_Latch) && !T.R00709_0);
  T.CR4_P2600_Stop = Boolean((T.Latch_ESTOP_P2600 || fullPumpTrip || T.PIT_003_PAHH_Latch) && !T.R00709_0);
  T.CR5_P3800_Stop = Boolean((T.Latch_ESTOP_P3800 || fullPumpTrip || T.PIT_002_PAHH_Latch) && !T.R00709_0);
  T.CR6_P3900_Stop = Boolean((T.Latch_ESTOP_P3900 || fullPumpTrip || T.PIT_002_PAHH_Latch) && !T.R00709_0);

  // Protect
  T.Deluge_Released_Status = Boolean(T.R00475_5);
  T.Foam_System_Inhibited  = Boolean(T.R00708_0 || T.R00709_0);

  // Loc_Al & Sound
  T.Bell_Mode_Discontinuous = Boolean((T.R01500_0 || T.GD_Any_Lo_Latch) && !T.R01500_2 && !T.R01501_0 && !T.R00495_5 && !T.R00535_5 && !T.R00475_5);
  T.Bell_Mode_Continuous    = Boolean(T.R01500_2 || T.R01501_0 || T.R00495_5 || T.R00535_5 || T.R00475_5);

  T.Any_Unaccepted_Alarm = Boolean(
    T.R01500_0 || T.R01500_2 || T.R01501_0 || T.R00495_5 || T.R00535_5 || T.R00475_5 ||
    T.R00435_6 || T.R00455_5 || T.R00455_6 || T.R00707_1 ||
    T.GD_Any_Lo_Latch || T.GD_Any_Hi_Latch || T.H2S_Lo_Latch || T.H2S_Hi_Latch || T.SD_001_002_Latch ||
    T.PIT_001_PAL || T.PIT_001_PAH || T.PIT_002_PAL || T.PIT_002_PAH || T.PIT_002_PAHH_Latch ||
    T.PIT_003_PAL || T.PIT_003_PAH || T.PIT_003_PAHH_Latch ||
    T.LIT_100_LAL || T.LIT_100_LAH || T.LIT_200_LAL || T.LIT_200_LAH ||
    T.LIT_300_LAL || T.LIT_300_LAH || T.LIT_400_LAL || T.LIT_400_LAH ||
    T.FT_6401_001_FAL || T.FT_6401_001_FAH ||
    T.R00702_1 || T.R00703_1 || T.R00708_0 || T.R00709_0 ||
    T.Latch_ESTOP_P2300 || T.Latch_ESTOP_P2400 || T.Latch_ESTOP_P2500 ||
    T.Latch_ESTOP_P2600 || T.Latch_ESTOP_P3800 || T.Latch_ESTOP_P3900
  );

  if (T.M00001_System_Accept) T.Alarm_Silence_Latch = true;
  else if (!T.Any_Unaccepted_Alarm || T.M00002_System_Reset) T.Alarm_Silence_Latch = false;

  T.R01513_3 = Boolean(T.Any_Unaccepted_Alarm && !T.Alarm_Silence_Latch); // Z1 PCR Horn
  const procCont = Boolean(T.PIT_001_PAH || T.PIT_002_PAH || T.PIT_002_PAHH_Latch || T.PIT_003_PAH || T.PIT_003_PAHH_Latch || T.FT_6401_001_FAH || T.R00455_5 || T.R00435_6 || T.Latch_ESTOP_P2300 || T.Latch_ESTOP_P2400 || T.Latch_ESTOP_P2500 || T.Latch_ESTOP_P2600 || T.Latch_ESTOP_P3800 || T.Latch_ESTOP_P3900);
  const procDisc = Boolean(T.PIT_001_PAL || T.PIT_002_PAL || T.PIT_003_PAL || T.LIT_100_LAL || T.LIT_100_LAH || T.LIT_200_LAL || T.LIT_200_LAH || T.LIT_300_LAL || T.LIT_300_LAH || T.LIT_400_LAL || T.LIT_400_LAH || T.FT_6401_001_FAL || T.R00455_6);
  T.PA_001 = Boolean((procCont || (procDisc && T.R01598_0)) && !T.Alarm_Silence_Latch && !T.R00709_0);
  T.H2SA_001_002 = Boolean((T.H2S_Hi_Latch || T.R00475_5 || (T.H2S_Lo_Latch && T.R01598_0)) && !T.Alarm_Silence_Latch && !T.R00709_0);
  T.SDA_001 = Boolean(T.SD_001_002_Latch && !T.Alarm_Silence_Latch && !T.R00709_0);

  // FLT_1
  T.Any_Channel_Fault = Boolean(anyDetectorFault || T.R00700_6 || T.R00704_1 || T.R00705_1);
  T.R01513_4 = !T.Any_Channel_Fault; // PLC_Fault (1=OK, 0=Fault)

  // Sound
  T.R01511_3 = Boolean((T.Bell_Mode_Continuous || (T.Bell_Mode_Discontinuous && T.R01598_0)) && !T.Alarm_Silence_Latch && !T.R00708_0 && !T.R00709_0);

  // Output: Write to Slot 8 1756-OB32 (Local:8:O.Data.0 .. 31)
  T.PumpShutdown = T.R01510_0;
  T.EY_6401_001_002 = T.R01511_0;
  T.SA_7404_001_002 = T.R01511_3;
  T.PUMP_A = Boolean(T.R01512_0);
  T.PUMP_B_START = Boolean(T.R01512_5);
  T.PUMP_B_STOP = Boolean(T.R01512_4);
  T.P2100_P2200 = T.R01511_1;
  T.P3600_P3700 = T.R01511_2;
  T.PLC_Fault = T.R01513_4;
  T.Tag_DO_13 = T.R01513_1; // L14 ESDV Closed
  T.Tag_DO_12 = T.R01513_0; // L15 ESDV Open
  T.Tag_DO_14 = T.R01513_2; // L16 Low Air
  T.Tag_DO_15 = T.R01513_3; // Z1 PCR Horn

  sO[8][0]  = T.PumpShutdown;
  sO[8][1]  = T.EY_6401_001_002;
  sO[8][2]  = T.SA_7404_001_002;
  sO[8][3]  = Boolean(T.R01513_12);
  sO[8][4]  = T.PUMP_A;
  sO[8][5]  = Boolean(T.R01513_13);
  sO[8][6]  = T.PUMP_B_START;
  sO[8][7]  = T.PUMP_B_STOP;
  sO[8][8]  = T.P2100_P2200;
  sO[8][9]  = T.P3600_P3700;
  sO[8][10] = T.PLC_Fault;
  sO[8][11] = T.Tag_DO_13; // L14
  sO[8][12] = T.Tag_DO_12; // L15
  sO[8][13] = T.Tag_DO_14; // L16
  sO[8][14] = T.LED_Low_Fuel_Gas_L17; // L17
  sO[8][15] = T.CR1_P2300_Stop;
  sO[8][16] = T.CR2_P2400_Stop;
  sO[8][17] = T.CR3_P2500_Stop;
  sO[8][18] = T.CR4_P2600_Stop;
  sO[8][19] = T.CR5_P3800_Stop;
  sO[8][20] = T.CR6_P3900_Stop;
  sO[8][21] = T.SD_GE;
  sO[8][22] = T.Tag_DO_15; // Z1
  sO[8][23] = T.PA_001;
  sO[8][30] = T.H2SA_001_002;
  sO[8][31] = T.SDA_001;

  // Clear one-shot HMI commands
  plc.First_Scan = false;
  plc.M00001 = false;
  plc.M00002 = false;
}
"""

JS_ENGINE_PART3 = r"""
// ============================================================================
// 5. TAB 1: INTERACTIVE P&ID SVG RENDERER & EQUIPMENT FACEPLATES
// ============================================================================
function buildPIDSVG() {
  const container = document.getElementById('pid-canvas-container');
  container.innerHTML = `
  <svg class="pid-svg" viewBox="0 0 1120 630" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="tankGrad" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="#1e293b"/>
        <stop offset="50%" stop-color="#334155"/>
        <stop offset="100%" stop-color="#0f172a"/>
      </linearGradient>
      <linearGradient id="oilGrad" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#f59e0b"/>
        <stop offset="100%" stop-color="#92400e"/>
      </linearGradient>
      <linearGradient id="waterGrad" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#38bdf8"/>
        <stop offset="100%" stop-color="#0369a1"/>
      </linearGradient>
    </defs>

    <!-- ZONE BOXES -->
    <rect x="12" y="12" width="510" height="315" rx="6" fill="rgba(15,23,42,0.55)" stroke="#233554" stroke-dasharray="4 3"/>
    <text x="22" y="28" fill="#64748b" font-size="10.5" font-weight="700">CRUDE TREATMENT (V-710/V-810), STORAGE TANKS (T-100..400) &amp; OIL EXPEDITION (PIT-001 / FT-001)</text>

    <rect x="532" y="12" width="575" height="190" rx="6" fill="rgba(15,23,42,0.55)" stroke="#233554" stroke-dasharray="4 3"/>
    <text x="542" y="28" fill="#64748b" font-size="10.5" font-weight="700">FUEL GAS LINE, AIR ACCUMULATOR (7002-PST-001), ESDV-001 &amp; GAS GENERATORS (GE-01/02)</text>

    <rect x="532" y="212" width="575" height="205" rx="6" fill="rgba(15,23,42,0.55)" stroke="#233554" stroke-dasharray="4 3"/>
    <text x="542" y="228" fill="#64748b" font-size="10.5" font-weight="700">HIGH-PRESSURE POWER OIL SKID (P-2100/2200, P-2300..2600, PIT-003 0–3000 PSI)</text>

    <rect x="12" y="337" width="510" height="280" rx="6" fill="rgba(15,23,42,0.55)" stroke="#233554" stroke-dasharray="4 3"/>
    <text x="22" y="353" fill="#64748b" font-size="10.5" font-weight="700">FIREWATER &amp; AFFF FOAM DELUGE SYSTEM (PUMP-A, DIESEL PUMP-B, 6401-EY, 7503-PST-001)</text>

    <rect x="532" y="427" width="575" height="190" rx="6" fill="rgba(15,23,42,0.55)" stroke="#233554" stroke-dasharray="4 3"/>
    <text x="542" y="443" fill="#64748b" font-size="10.5" font-weight="700">WATER INJECTION SKID (P-3600/3700 BOOSTERS, P-3800/3900 PUMPS, PIT-002 0–1500 PSI)</text>

    <!-- ================= 1. HEATER TREATERS & TANKS T-100..T-400 ================= -->
    <path class="pipe" d="M 85 95 L 145 95 L 145 62 L 440 62"/>
    <path class="pipe-flow oil active" id="flow-treaters" d="M 85 95 L 145 95 L 145 62 L 440 62"/>
    <path class="pipe" d="M 155 215 L 485 215 L 485 275 L 180 275"/>
    <path class="pipe-flow oil active" id="flow-export" d="M 155 215 L 485 215 L 485 275 L 180 275"/>

    <!-- V-710 & V-810 Treaters -->
    <g class="equip-node" onclick="selectEquip('TREATERS')">
      <rect x="24" y="55" width="62" height="36" rx="12" fill="url(#tankGrad)" stroke="#60a5fa" stroke-width="1.5"/>
      <text x="55" y="72" text-anchor="middle" fill="#e2e8f0" font-size="9.5" font-weight="700">V-710</text>
      <text x="55" y="84" text-anchor="middle" fill="#38bdf8" font-size="8.5" id="svg-v710-txt">66.5°C</text>

      <rect x="24" y="102" width="62" height="36" rx="12" fill="url(#tankGrad)" stroke="#60a5fa" stroke-width="1.5"/>
      <text x="55" y="119" text-anchor="middle" fill="#e2e8f0" font-size="9.5" font-weight="700">V-810</text>
      <text x="55" y="131" text-anchor="middle" fill="#38bdf8" font-size="8.5" id="svg-v810-txt">68.0°C</text>
    </g>

    <!-- Tank T-100 -->
    <g class="equip-node" onclick="selectEquip('T100')">
      <rect x="135" y="82" width="68" height="118" rx="4" fill="url(#tankGrad)" stroke="#64748b" stroke-width="1.5" id="svg-t100-box"/>
      <rect x="137" y="140" width="64" height="58" fill="url(#oilGrad)" opacity="0.88" id="svg-t100-lvl"/>
      <text x="169" y="100" text-anchor="middle" fill="#fff" font-size="10.5" font-weight="700">T-100</text>
      <text x="169" y="115" text-anchor="middle" fill="#fde68a" font-family="Consolas" font-size="10.5" font-weight="700" id="svg-t100-val">5.20 m</text>
      <text x="169" y="128" text-anchor="middle" fill="#94a3b8" font-size="8.5">LIT-100</text>
    </g>

    <!-- Tank T-200 -->
    <g class="equip-node" onclick="selectEquip('T200')">
      <rect x="220" y="82" width="68" height="118" rx="4" fill="url(#tankGrad)" stroke="#64748b" stroke-width="1.5" id="svg-t200-box"/>
      <rect x="222" y="125" width="64" height="73" fill="url(#oilGrad)" opacity="0.88" id="svg-t200-lvl"/>
      <text x="254" y="100" text-anchor="middle" fill="#fff" font-size="10.5" font-weight="700">T-200</text>
      <text x="254" y="115" text-anchor="middle" fill="#fde68a" font-family="Consolas" font-size="10.5" font-weight="700" id="svg-t200-val">6.40 m</text>
      <text x="254" y="128" text-anchor="middle" fill="#94a3b8" font-size="8.5">LIT-200</text>
    </g>

    <!-- Tank T-300 -->
    <g class="equip-node" onclick="selectEquip('T300')">
      <rect x="305" y="82" width="68" height="118" rx="4" fill="url(#tankGrad)" stroke="#64748b" stroke-width="1.5" id="svg-t300-box"/>
      <rect x="307" y="150" width="64" height="48" fill="url(#oilGrad)" opacity="0.88" id="svg-t300-lvl"/>
      <text x="339" y="100" text-anchor="middle" fill="#fff" font-size="10.5" font-weight="700">T-300</text>
      <text x="339" y="115" text-anchor="middle" fill="#fde68a" font-family="Consolas" font-size="10.5" font-weight="700" id="svg-t300-val">4.10 m</text>
      <text x="339" y="128" text-anchor="middle" fill="#94a3b8" font-size="8.5">LIT-300</text>
    </g>

    <!-- Tank T-400 (12m) -->
    <g class="equip-node" onclick="selectEquip('T400')">
      <rect x="390" y="72" width="76" height="128" rx="4" fill="url(#tankGrad)" stroke="#64748b" stroke-width="1.5" id="svg-t400-box"/>
      <rect x="392" y="118" width="72" height="80" fill="url(#oilGrad)" opacity="0.88" id="svg-t400-lvl"/>
      <text x="428" y="92" text-anchor="middle" fill="#fff" font-size="10.5" font-weight="700">T-400 (12m)</text>
      <text x="428" y="107" text-anchor="middle" fill="#fde68a" font-family="Consolas" font-size="10.5" font-weight="700" id="svg-t400-val">7.80 m</text>
      <text x="428" y="120" text-anchor="middle" fill="#94a3b8" font-size="8.5">LIT-400</text>
    </g>

    <!-- Deluge Foam Spray Overlay on Tanks (Visible when Deluge Active) -->
    <g id="svg-foam-spray" opacity="0">
      <path d="M 169 65 L 145 82 M 169 65 L 193 82 M 254 65 L 230 82 M 254 65 L 278 82 M 339 65 L 315 82 M 339 65 L 363 82 M 428 58 L 400 72 M 428 58 L 456 72" stroke="#22c55e" stroke-width="2.5" stroke-dasharray="3 2"/>
      <text x="295" y="53" text-anchor="middle" fill="#4ade80" font-size="11" font-weight="800">AFFF FOAM DELUGE SPRAY ACTIVE</text>
    </g>

    <!-- PIT-001 & 6401-FT-001 Oil Expedition -->
    <g class="equip-node" onclick="selectEquip('EXPEDITION')">
      <rect x="315" y="248" width="135" height="52" rx="5" fill="#0d1829" stroke="#38bdf8" stroke-width="1.5" id="svg-pit001-box"/>
      <text x="382" y="264" text-anchor="middle" fill="#93c5fd" font-size="10" font-weight="700">PIT-001 EXPEDITION</text>
      <text x="382" y="280" text-anchor="middle" fill="#fff" font-family="Consolas" font-size="12" font-weight="700" id="svg-pit001-val">58.0 Psi</text>
      <text x="382" y="293" text-anchor="middle" fill="#64748b" font-size="8.5">PAL:10 | PAH:100 Psi</text>

      <rect x="155" y="248" width="140" height="52" rx="5" fill="#0d1829" stroke="#22c55e" stroke-width="1.5" id="svg-ft001-box"/>
      <text x="225" y="264" text-anchor="middle" fill="#86efac" font-size="10" font-weight="700">6401-FT-001 EXPORT</text>
      <text x="225" y="280" text-anchor="middle" fill="#fff" font-family="Consolas" font-size="12" font-weight="700" id="svg-ft001-val">185.0 bbl/h</text>
      <text x="225" y="293" text-anchor="middle" fill="#64748b" font-size="8.5">FAL:30 | FAH:300 bbl/h</text>
    </g>

    <!-- ================= 2. FUEL GAS, ESDV-001, AIR ACC & GAS GENERATORS ================= -->
    <path class="pipe" d="M 555 115 L 950 115"/>
    <path class="pipe-flow gas active" id="flow-fuelgas" d="M 555 115 L 950 115"/>

    <!-- Air Accumulator 7002-PST-001 -->
    <g class="equip-node" onclick="selectEquip('ESDV')">
      <rect x="555" y="42" width="130" height="48" rx="5" fill="#0d1829" stroke="#38bdf8" stroke-width="1.5" id="svg-pst7002-box"/>
      <text x="620" y="57" text-anchor="middle" fill="#93c5fd" font-size="9.5" font-weight="700">7002-PST-001 AIR ACC</text>
      <text x="620" y="73" text-anchor="middle" fill="#fff" font-family="Consolas" font-size="11.5" font-weight="700" id="svg-pst7002-val">82.0 Psi</text>
      <text x="620" y="84" text-anchor="middle" fill="#64748b" font-size="8">PAL: 50 Psi (L16)</text>

      <!-- 6401-ESDV-001 Valve Symbol -->
      <polygon points="695,98 695,132 745,98 745,132" fill="#22c55e" stroke="#fff" stroke-width="1.5" id="svg-esdv-poly"/>
      <rect x="705" y="64" width="30" height="24" rx="4" fill="#1e293b" stroke="#94a3b8"/>
      <line x1="720" y1="88" x2="720" y2="115" stroke="#fff" stroke-width="2"/>
      <text x="720" y="56" text-anchor="middle" fill="#fff" font-size="10" font-weight="700">6401-ESDV-001</text>
      <text x="720" y="150" text-anchor="middle" fill="#4ade80" font-family="Consolas" font-size="10.5" font-weight="700" id="svg-esdv-val">OPEN (100%)</text>
      <text x="720" y="164" text-anchor="middle" fill="#94a3b8" font-size="8.5" id="svg-esdv-ls">ZSH:1 | ZSL:0 | EY:1</text>

      <!-- 6401-PST-001 Fuel Gas Line Pressure -->
      <rect x="775" y="42" width="135" height="48" rx="5" fill="#0d1829" stroke="#a855f7" stroke-width="1.5" id="svg-pst6401-box"/>
      <text x="842" y="57" text-anchor="middle" fill="#d8b4fe" font-size="9.5" font-weight="700">6401-PST-001 FUEL GAS</text>
      <text x="842" y="73" text-anchor="middle" fill="#fff" font-family="Consolas" font-size="11.5" font-weight="700" id="svg-pst6401-val">68.0 Psi</text>
      <text x="842" y="84" text-anchor="middle" fill="#64748b" font-size="8">PAL:40(L17) | PAH:100(ESD)</text>
    </g>

    <!-- Gas Generators GE-01/02 -->
    <g class="equip-node" onclick="selectEquip('GASGEN')">
      <rect x="935" y="58" width="155" height="122" rx="6" fill="#111c2d" stroke="#22c55e" stroke-width="2" id="svg-gasgen-box"/>
      <text x="1012" y="78" text-anchor="middle" fill="#fff" font-size="10.5" font-weight="700">GAS GENERATORS</text>
      <text x="1012" y="96" text-anchor="middle" fill="#4ade80" font-family="Consolas" font-size="11" font-weight="700" id="svg-gasgen-state">ONLINE (GE-01/02)</text>
      <text x="1012" y="116" text-anchor="middle" fill="#cbd5e1" font-family="Consolas" font-size="9.5" id="svg-gd-txt">GD-001..003: 0.0 %LEL</text>
      <text x="1012" y="132" text-anchor="middle" fill="#cbd5e1" font-family="Consolas" font-size="9.5" id="svg-sd-txt">SD-001/002: 0.0 %</text>
      <text x="1012" y="152" text-anchor="middle" fill="#94a3b8" font-family="Consolas" font-size="9" id="svg-sdge-txt">SD-GE TRIP: INACTIVE</text>
    </g>

    <!-- ================= 3. POWER OIL SKID (P-2100/2200, P-2300..2600, PIT-003) ================= -->
    <path class="pipe" d="M 555 315 L 950 315"/>
    <path class="pipe-flow oil active" id="flow-poweroil" d="M 555 315 L 950 315"/>

    <g class="equip-node" onclick="selectEquip('POWEROIL')">
      <!-- Booster P-2100/2200 -->
      <circle cx="590" cy="315" r="24" fill="#111c2d" stroke="#22c55e" stroke-width="2" id="svg-p2100-cir"/>
      <text x="590" y="313" text-anchor="middle" fill="#fff" font-size="8.5" font-weight="700">P-2100</text>
      <text x="590" y="324" text-anchor="middle" fill="#4ade80" font-size="8" id="svg-p2100-txt">RUN</text>
      <text x="590" y="352" text-anchor="middle" fill="#94a3b8" font-size="8.5">OIL BOOSTER</text>

      <!-- 4 Multiplex Pumps P-2300..P-2600 -->
      <rect x="640" y="242" width="62" height="145" rx="5" fill="#0f172a" stroke="#22c55e" stroke-width="1.5" id="svg-p2300-box"/>
      <text x="671" y="260" text-anchor="middle" fill="#fff" font-size="10" font-weight="700">P-2300</text>
      <text x="671" y="278" text-anchor="middle" fill="#4ade80" font-family="Consolas" font-size="9.5" id="svg-p2300-st">RUN</text>
      <text x="671" y="295" text-anchor="middle" fill="#cbd5e1" font-family="Consolas" font-size="8.5" id="svg-p2300-rpm">1650 RPM</text>
      <text x="671" y="375" text-anchor="middle" fill="#64748b" font-size="8">CR1 / E1</text>

      <rect x="710" y="242" width="62" height="145" rx="5" fill="#0f172a" stroke="#22c55e" stroke-width="1.5" id="svg-p2400-box"/>
      <text x="741" y="260" text-anchor="middle" fill="#fff" font-size="10" font-weight="700">P-2400</text>
      <text x="741" y="278" text-anchor="middle" fill="#4ade80" font-family="Consolas" font-size="9.5" id="svg-p2400-st">RUN</text>
      <text x="741" y="295" text-anchor="middle" fill="#cbd5e1" font-family="Consolas" font-size="8.5" id="svg-p2400-rpm">1650 RPM</text>
      <text x="741" y="375" text-anchor="middle" fill="#64748b" font-size="8">CR2 / E2</text>

      <rect x="780" y="242" width="62" height="145" rx="5" fill="#0f172a" stroke="#22c55e" stroke-width="1.5" id="svg-p2500-box"/>
      <text x="811" y="260" text-anchor="middle" fill="#fff" font-size="10" font-weight="700">P-2500</text>
      <text x="811" y="278" text-anchor="middle" fill="#4ade80" font-family="Consolas" font-size="9.5" id="svg-p2500-st">RUN</text>
      <text x="811" y="295" text-anchor="middle" fill="#cbd5e1" font-family="Consolas" font-size="8.5" id="svg-p2500-rpm">1620 RPM</text>
      <text x="811" y="375" text-anchor="middle" fill="#64748b" font-size="8">CR3 / E3</text>

      <rect x="850" y="242" width="62" height="145" rx="5" fill="#0f172a" stroke="#64748b" stroke-width="1.5" id="svg-p2600-box"/>
      <text x="881" y="260" text-anchor="middle" fill="#fff" font-size="10" font-weight="700">P-2600</text>
      <text x="881" y="278" text-anchor="middle" fill="#94a3b8" font-family="Consolas" font-size="9.5" id="svg-p2600-st">STBY</text>
      <text x="881" y="295" text-anchor="middle" fill="#cbd5e1" font-family="Consolas" font-size="8.5" id="svg-p2600-rpm">0 RPM</text>
      <text x="881" y="375" text-anchor="middle" fill="#64748b" font-size="8">CR4 / E4</text>

      <!-- PIT-003 Oil Injection Manifold -->
      <rect x="930" y="255" width="162" height="115" rx="6" fill="#0d1829" stroke="#f59e0b" stroke-width="1.8" id="svg-pit003-box"/>
      <text x="1011" y="275" text-anchor="middle" fill="#fde68a" font-size="10" font-weight="700">PIT-003 OIL MANIFOLD</text>
      <text x="1011" y="302" text-anchor="middle" fill="#fff" font-family="Consolas" font-size="15" font-weight="800" id="svg-pit003-val">2150 Psi</text>
      <text x="1011" y="322" text-anchor="middle" fill="#94a3b8" font-size="8.5">PAL: 1700 | PAH: 2700</text>
      <text x="1011" y="336" text-anchor="middle" fill="#fca5a5" font-size="8.5" font-weight="700">PAHH: 2800 Psi (ESD)</text>
    </g>

    <!-- ================= 4. FIREWATER & FOAM DELUGE SKID ================= -->
    <path class="pipe" d="M 90 480 L 470 480 L 470 365"/>
    <path class="pipe-flow foam" id="flow-deluge" d="M 90 480 L 470 480 L 470 365"/>

    <g class="equip-node" onclick="selectEquip('DELUGE')">
      <!-- AFFF Foam Tank & Diesel Tank -->
      <rect x="26" y="375" width="95" height="90" rx="5" fill="#0f172a" stroke="#22c55e" stroke-width="1.5" id="svg-foam-box"/>
      <text x="73" y="393" text-anchor="middle" fill="#86efac" font-size="9.5" font-weight="700">AFFF FOAM TK</text>
      <text x="73" y="415" text-anchor="middle" fill="#fff" font-family="Consolas" font-size="12" font-weight="700" id="svg-foam-val">92.0%</text>
      <text x="73" y="435" text-anchor="middle" fill="#94a3b8" font-size="8.5" id="svg-ls001-txt">7503-LS-001: OK</text>

      <rect x="26" y="485" width="95" height="90" rx="5" fill="#0f172a" stroke="#f59e0b" stroke-width="1.5" id="svg-diesel-box"/>
      <text x="73" y="503" text-anchor="middle" fill="#fde68a" font-size="9.5" font-weight="700">DIESEL TANK</text>
      <text x="73" y="525" text-anchor="middle" fill="#fff" font-family="Consolas" font-size="12" font-weight="700" id="svg-diesel-val">88.0%</text>
      <text x="73" y="545" text-anchor="middle" fill="#94a3b8" font-size="8.5" id="svg-ls002-txt">7503-LS-002: OK</text>

      <!-- Duty Pump A (Electric) -->
      <rect x="145" y="380" width="135" height="88" rx="6" fill="#111c2d" stroke="#64748b" stroke-width="2" id="svg-pumpa-box"/>
      <text x="212" y="400" text-anchor="middle" fill="#fff" font-size="10.5" font-weight="700">7503-PUMP-A (DUTY)</text>
      <text x="212" y="420" text-anchor="middle" fill="#94a3b8" font-family="Consolas" font-size="11" font-weight="700" id="svg-pumpa-st">STANDBY</text>
      <text x="212" y="440" text-anchor="middle" fill="#64748b" font-size="8.5" id="svg-pumpa-sub">Electric Motor Driven</text>

      <!-- Standby Pump B (Diesel) -->
      <rect x="145" y="485" width="135" height="88" rx="6" fill="#111c2d" stroke="#64748b" stroke-width="2" id="svg-pumpb-box"/>
      <text x="212" y="505" text-anchor="middle" fill="#fff" font-size="10.5" font-weight="700">7503-PUMP-B (STBY)</text>
      <text x="212" y="525" text-anchor="middle" fill="#94a3b8" font-family="Consolas" font-size="11" font-weight="700" id="svg-pumpb-st">STANDBY</text>
      <text x="212" y="545" text-anchor="middle" fill="#64748b" font-size="8.5" id="svg-pumpb-sub">10s Auto-Backup Diesel</text>

      <!-- Deluge Pressure 7503-PST-001 -->
      <rect x="310" y="415" width="185" height="115" rx="6" fill="#0d1829" stroke="#38bdf8" stroke-width="1.5" id="svg-pst7503-box"/>
      <text x="402" y="435" text-anchor="middle" fill="#93c5fd" font-size="10" font-weight="700">7503-PST-001 DELUGE HDR</text>
      <text x="402" y="462" text-anchor="middle" fill="#fff" font-family="Consolas" font-size="15" font-weight="800" id="svg-pst7503-val">0.0 Psi</text>
      <text x="402" y="482" text-anchor="middle" fill="#94a3b8" font-size="9" id="svg-deluge-tmr">PAH: 50 Psi (Foam Released)</text>
      <text x="402" y="502" text-anchor="middle" fill="#64748b" font-family="Consolas" font-size="9" id="svg-s2-status">S2 Foam Inhibit: OFF</text>
    </g>

    <!-- ================= 5. WATER INJECTION SKID (P-3600/3700, P-3800/3900, PIT-002) ================= -->
    <path class="pipe" d="M 555 525 L 950 525"/>
    <path class="pipe-flow water active" id="flow-waterinj" d="M 555 525 L 950 525"/>

    <g class="equip-node" onclick="selectEquip('WATERINJ')">
      <circle cx="595" cy="525" r="24" fill="#111c2d" stroke="#22c55e" stroke-width="2" id="svg-p3600-cir"/>
      <text x="595" y="523" text-anchor="middle" fill="#fff" font-size="8.5" font-weight="700">P-3600</text>
      <text x="595" y="534" text-anchor="middle" fill="#4ade80" font-size="8" id="svg-p3600-txt">RUN</text>
      <text x="595" y="562" text-anchor="middle" fill="#94a3b8" font-size="8.5">WATER BOOSTER</text>

      <rect x="665" y="460" width="95" height="130" rx="5" fill="#0f172a" stroke="#22c55e" stroke-width="1.5" id="svg-p3800-box"/>
      <text x="712" y="482" text-anchor="middle" fill="#fff" font-size="10.5" font-weight="700">P-3800</text>
      <text x="712" y="502" text-anchor="middle" fill="#4ade80" font-family="Consolas" font-size="10" id="svg-p3800-st">RUNNING</text>
      <text x="712" y="522" text-anchor="middle" fill="#cbd5e1" font-family="Consolas" font-size="9" id="svg-p3800-rpm">1580 RPM</text>
      <text x="712" y="575" text-anchor="middle" fill="#64748b" font-size="8.5">CR5 / E-Stop E5</text>

      <rect x="780" y="460" width="95" height="130" rx="5" fill="#0f172a" stroke="#22c55e" stroke-width="1.5" id="svg-p3900-box"/>
      <text x="827" y="482" text-anchor="middle" fill="#fff" font-size="10.5" font-weight="700">P-3900</text>
      <text x="827" y="502" text-anchor="middle" fill="#4ade80" font-family="Consolas" font-size="10" id="svg-p3900-st">RUNNING</text>
      <text x="827" y="522" text-anchor="middle" fill="#cbd5e1" font-family="Consolas" font-size="9" id="svg-p3900-rpm">1580 RPM</text>
      <text x="827" y="575" text-anchor="middle" fill="#64748b" font-size="8.5">CR6 / E-Stop E6</text>

      <!-- PIT-002 Water Injection Manifold -->
      <rect x="910" y="465" width="180" height="120" rx="6" fill="#0d1829" stroke="#00d4ff" stroke-width="1.8" id="svg-pit002-box"/>
      <text x="1000" y="485" text-anchor="middle" fill="#7dd3fc" font-size="10" font-weight="700">PIT-002 WATER MANIFOLD</text>
      <text x="1000" y="512" text-anchor="middle" fill="#fff" font-family="Consolas" font-size="15" font-weight="800" id="svg-pit002-val">540 Psi</text>
      <text x="1000" y="532" text-anchor="middle" fill="#94a3b8" font-size="8.5">PAL: 200 | PAH: 800 Psi</text>
      <text x="1000" y="546" text-anchor="middle" fill="#fca5a5" font-size="8.5" font-weight="700">PAHH: 900 Psi (ESD)</text>
    </g>
  </svg>`;
}

function updatePIDSVG() {
  const p = SimState.phys;
  const T = SimState.plc.tags;

  // Tanks T-100..400
  const tCfg = [
    { k:'T100', max:10.0, y0:200, hMax:114, lal:T.LIT_100_LAL, lah:T.LIT_100_LAH },
    { k:'T200', max:10.0, y0:200, hMax:114, lal:T.LIT_200_LAL, lah:T.LIT_200_LAH },
    { k:'T300', max:10.0, y0:200, hMax:114, lal:T.LIT_300_LAL, lah:T.LIT_300_LAH },
    { k:'T400', max:12.0, y0:200, hMax:124, lal:T.LIT_400_LAL, lah:T.LIT_400_LAH }
  ];
  tCfg.forEach(c => {
    const lvl = p.tanks[c.k].level;
    const h = Math.max(2, Math.min(c.hMax, (lvl / c.max) * c.hMax));
    const rect = document.getElementById(`svg-${c.k.toLowerCase()}-lvl`);
    const txt  = document.getElementById(`svg-${c.k.toLowerCase()}-val`);
    const box  = document.getElementById(`svg-${c.k.toLowerCase()}-box`);
    if (rect) { rect.setAttribute('y', c.y0 - h); rect.setAttribute('height', h); }
    if (txt) txt.textContent = `${lvl.toFixed(2)} m`;
    if (box) box.setAttribute('stroke', (c.lal || c.lah) ? '#ef4444' : '#64748b');
  });

  // Expedition PIT-001 & FT-001
  const pit1 = document.getElementById('svg-pit001-val');
  if (pit1) {
    pit1.textContent = `${p.oilExpPressPsi.toFixed(1)} Psi`;
    document.getElementById('svg-pit001-box').setAttribute('stroke', (T.PIT_001_PAL || T.PIT_001_PAH) ? '#ef4444' : '#38bdf8');
    document.getElementById('svg-ft001-val').textContent = `${p.oilExpFlowBblH.toFixed(1)} bbl/h`;
    document.getElementById('svg-ft001-box').setAttribute('stroke', (T.FT_6401_001_FAL || T.FT_6401_001_FAH) ? '#ef4444' : '#22c55e');
    document.getElementById('flow-export').classList.toggle('active', p.oilExpFlowBblH > 10);
  }

  // Fuel Gas & ESDV-001
  const esdvPoly = document.getElementById('svg-esdv-poly');
  if (esdvPoly) {
    const open = p.esdvPositionPct >= 95;
    const closed = p.esdvPositionPct <= 5;
    esdvPoly.setAttribute('fill', open ? '#22c55e' : (closed ? '#ef4444' : '#f59e0b'));
    const esdvTxt = document.getElementById('svg-esdv-val');
    esdvTxt.textContent = open ? `OPEN (${p.esdvPositionPct.toFixed(0)}%)` : (closed ? `CLOSED (0%)` : `TRANSIT (${p.esdvPositionPct.toFixed(0)}%)`);
    esdvTxt.setAttribute('fill', open ? '#4ade80' : '#f87171');
    document.getElementById('svg-esdv-ls').textContent = `ZSH:${T.ZSH_6401_001?1:0} | ZSL:${T.ZSL_6401_001?1:0} | EY:${T.EY_6401_001_002?1:0}`;
    document.getElementById('flow-fuelgas').classList.toggle('active', p.esdvPositionPct > 20);

    document.getElementById('svg-pst7002-val').textContent = `${p.airAccPsi.toFixed(1)} Psi`;
    document.getElementById('svg-pst7002-box').setAttribute('stroke', T.R00435_6 ? '#ef4444' : '#38bdf8');
    document.getElementById('svg-pst6401-val').textContent = `${p.fuelGasLinePsi.toFixed(1)} Psi`;
    document.getElementById('svg-pst6401-box').setAttribute('stroke', (T.R00455_5 || T.R00455_6) ? '#ef4444' : '#a855f7');
  }

  // Gas Generators
  const ggBox = document.getElementById('svg-gasgen-box');
  if (ggBox) {
    ggBox.setAttribute('stroke', p.gasGenRunning ? '#22c55e' : '#ef4444');
    const ggSt = document.getElementById('svg-gasgen-state');
    ggSt.textContent = p.gasGenRunning ? 'ONLINE (GE-01/02)' : 'SHUTDOWN (SD-GE)';
    ggSt.setAttribute('fill', p.gasGenRunning ? '#4ade80' : '#f87171');
    const maxGD = Math.max(T.GD_001_EU||0, T.GD_002_EU||0, T.GD_003_EU||0);
    document.getElementById('svg-gd-txt').textContent = `GD-001..003 Max: ${maxGD.toFixed(1)} %LEL`;
    document.getElementById('svg-sd-txt').textContent = `SD-001/002 Smoke: ${(T.SD_001_002_EU||0).toFixed(1)} %`;
    document.getElementById('svg-sdge-txt').textContent = `SD-GE Output: ${T.SD_GE ? 'TRIPPED (1)' : 'NORMAL (0)'}`;
  }

  // Power Oil Skid
  const p2100 = document.getElementById('svg-p2100-cir');
  if (p2100) {
    p2100.setAttribute('stroke', p.oilBoosterRun ? '#22c55e' : '#ef4444');
    document.getElementById('svg-p2100-txt').textContent = p.oilBoosterRun ? 'RUN' : 'TRIP';
    ['P2300','P2400','P2500','P2600'].forEach((k, idx) => {
      const pm = p.powerOilPumps[k];
      const cr = T[`CR${idx+1}_${k}_Stop`];
      const bx = document.getElementById(`svg-${k.toLowerCase()}-box`);
      const st = document.getElementById(`svg-${k.toLowerCase()}-st`);
      const rp = document.getElementById(`svg-${k.toLowerCase()}-rpm`);
      bx.setAttribute('stroke', cr ? '#ef4444' : (pm.running ? '#22c55e' : '#64748b'));
      st.textContent = cr ? 'ESD TRIP' : (pm.running ? 'RUNNING' : 'STOPPED');
      st.setAttribute('fill', cr ? '#f87171' : (pm.running ? '#4ade80' : '#94a3b8'));
      rp.textContent = `${pm.rpm.toFixed(0)} RPM`;
    });
    document.getElementById('svg-pit003-val').textContent = `${p.oilManifoldPsi.toFixed(0)} Psi`;
    document.getElementById('svg-pit003-box').setAttribute('stroke', (T.PIT_003_PAL || T.PIT_003_PAH || T.PIT_003_PAHH_Latch) ? '#ef4444' : '#f59e0b');
    document.getElementById('flow-poweroil').classList.toggle('active', p.oilManifoldPsi > 300);
  }

  // Water Injection Skid
  const p3600 = document.getElementById('svg-p3600-cir');
  if (p3600) {
    p3600.setAttribute('stroke', p.waterBoosterRun ? '#22c55e' : '#ef4444');
    document.getElementById('svg-p3600-txt').textContent = p.waterBoosterRun ? 'RUN' : 'TRIP';
    ['P3800','P3900'].forEach((k, idx) => {
      const pm = p.waterInjPumps[k];
      const cr = T[`CR${idx+5}_${k}_Stop`];
      const bx = document.getElementById(`svg-${k.toLowerCase()}-box`);
      const st = document.getElementById(`svg-${k.toLowerCase()}-st`);
      const rp = document.getElementById(`svg-${k.toLowerCase()}-rpm`);
      bx.setAttribute('stroke', cr ? '#ef4444' : (pm.running ? '#22c55e' : '#64748b'));
      st.textContent = cr ? 'ESD TRIP' : (pm.running ? 'RUNNING' : 'STOPPED');
      st.setAttribute('fill', cr ? '#f87171' : (pm.running ? '#4ade80' : '#94a3b8'));
      rp.textContent = `${pm.rpm.toFixed(0)} RPM`;
    });
    document.getElementById('svg-pit002-val').textContent = `${p.waterManifoldPsi.toFixed(0)} Psi`;
    document.getElementById('svg-pit002-box').setAttribute('stroke', (T.PIT_002_PAL || T.PIT_002_PAH || T.PIT_002_PAHH_Latch) ? '#ef4444' : '#00d4ff');
    document.getElementById('flow-waterinj').classList.toggle('active', p.waterManifoldPsi > 100);
  }

  // Deluge & Foam System
  const paBox = document.getElementById('svg-pumpa-box');
  if (paBox) {
    paBox.setAttribute('stroke', p.pumpARunning ? '#22c55e' : (p.pumpAFailFault ? '#ef4444' : '#64748b'));
    const paSt = document.getElementById('svg-pumpa-st');
    paSt.textContent = p.pumpARunning ? 'RUNNING' : (T.PUMP_A && p.pumpAFailFault ? 'FAIL TO RUN!' : 'STANDBY');
    paSt.setAttribute('fill', p.pumpARunning ? '#4ade80' : (p.pumpAFailFault ? '#f87171' : '#94a3b8'));

    const pbBox = document.getElementById('svg-pumpb-box');
    pbBox.setAttribute('stroke', p.pumpBRunning ? '#22c55e' : (T.R00706_0 ? '#f59e0b' : '#64748b'));
    const pbSt = document.getElementById('svg-pumpb-st');
    pbSt.textContent = p.pumpBRunning ? 'DIESEL RUNNING' : (T.R00706_0 ? 'INHIBITED' : 'STANDBY');
    pbSt.setAttribute('fill', p.pumpBRunning ? '#4ade80' : (T.R00706_0 ? '#fde68a' : '#94a3b8'));

    document.getElementById('svg-pst7503-val').textContent = `${p.delugeLinePsi.toFixed(1)} Psi`;
    document.getElementById('svg-pst7503-box').setAttribute('stroke', T.R00475_5 ? '#22c55e' : '#38bdf8');
    const tmrA = SimState.plc.timers.TMR_PumpA_FailToRun;
    document.getElementById('svg-deluge-tmr').textContent = T.Foam_Release_Demand
      ? `Demand ON | Proving Timer: ${((tmrA ? tmrA.ACC : 0)/1000).toFixed(1)}/10.0s`
      : 'PAH: 50 Psi (Foam Released)';
    document.getElementById('svg-s2-status').textContent = `S2 Foam Inhibit: ${T.R00708_0 ? 'ACTIVE' : 'OFF'} | S3 All Inhibit: ${T.R00709_0 ? 'ACTIVE' : 'OFF'}`;
    document.getElementById('svg-foam-val').textContent = `${p.foamTankPct.toFixed(1)}%`;
    document.getElementById('svg-ls001-txt').textContent = `7503-LS-001: ${T.R00702_1 ? 'LOW ALARM!' : 'OK'}`;
    document.getElementById('svg-diesel-val').textContent = `${p.dieselTankPct.toFixed(1)}%`;
    document.getElementById('svg-ls002-txt').textContent = `7503-LS-002: ${T.R00703_1 ? 'LOW ALARM!' : 'OK'}`;

    const delugeFlow = p.delugeLinePsi >= 45;
    document.getElementById('flow-deluge').classList.toggle('active', delugeFlow);
    document.getElementById('svg-foam-spray').setAttribute('opacity', delugeFlow ? '1' : '0');
  }
}

function selectEquip(eq) {
  SimState.selectedEquip = eq;
  renderFaceplate();
}

function renderFaceplate() {
  const eq = SimState.selectedEquip;
  const p = SimState.phys;
  const T = SimState.plc.tags;
  document.getElementById('fp-tag').textContent = eq;
  const body = document.getElementById('fp-body');

  let html = `
  <div style="display:flex;gap:4px;flex-wrap:wrap;margin-bottom:10px;">
    <button class="btn ${eq==='OVERVIEW'?'active':''}" style="padding:3px 7px;font-size:10.5px;" onclick="selectEquip('OVERVIEW')">All Sliders</button>
    <button class="btn ${eq==='T100'?'active':''}" style="padding:3px 7px;font-size:10.5px;" onclick="selectEquip('T100')">Tanks T100-400</button>
    <button class="btn ${eq==='ESDV'?'active':''}" style="padding:3px 7px;font-size:10.5px;" onclick="selectEquip('ESDV')">ESDV &amp; Fuel Gas</button>
    <button class="btn ${eq==='POWEROIL'?'active':''}" style="padding:3px 7px;font-size:10.5px;" onclick="selectEquip('POWEROIL')">Power Oil</button>
    <button class="btn ${eq==='WATERINJ'?'active':''}" style="padding:3px 7px;font-size:10.5px;" onclick="selectEquip('WATERINJ')">Water Inj</button>
    <button class="btn ${eq==='DELUGE'?'active':''}" style="padding:3px 7px;font-size:10.5px;" onclick="selectEquip('DELUGE')">Foam Deluge</button>
  </div>`;

  // Always show direct interactive process sliders & fault switches for the selected system (or all in OVERVIEW)
  if (eq === 'OVERVIEW' || eq === 'POWEROIL') {
    html += `
    <div style="background:var(--bg-2);border:1px solid var(--border);border-radius:5px;padding:8px;margin-bottom:8px;">
      <div style="font-weight:700;color:var(--amber);margin-bottom:6px;">POWER OIL MANIFOLD (PIT-003 &amp; P-2300..2600)</div>
      <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px;">
        <span>PIT-003 Pressure (PAL:1700, PAH:2700, PAHH:2800):</span>
        <strong id="fp-lbl-pit003">${p.oilManifoldPsi.toFixed(0)} Psi</strong>
      </div>
      <input type="range" min="0" max="3000" step="10" value="${p.oilManifoldPsi}" style="width:100%;margin-bottom:6px;"
        oninput="SimState.coupledPhysics=false;updatePhysModeBtns();SimState.phys.oilManifoldPsi=parseFloat(this.value);document.getElementById('fp-lbl-pit003').textContent=this.value+' Psi';">
      <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px;">
        <span>Wellhead Choke Opening (Coupled ODE):</span>
        <strong id="fp-lbl-oilchoke">${p.oilWellChokePct.toFixed(0)}%</strong>
      </div>
      <input type="range" min="20" max="100" value="${p.oilWellChokePct}" style="width:100%;margin-bottom:6px;"
        oninput="SimState.phys.oilWellChokePct=parseFloat(this.value);document.getElementById('fp-lbl-oilchoke').textContent=this.value+'%';">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:4px;margin-top:4px;">
        ${['P2300','P2400','P2500','P2600'].map((k,i) => `
          <button class="btn ${p.powerOilPumps[k].cmdRun?'success':''}" style="padding:3px 6px;font-size:10.5px;"
            onclick="SimState.phys.powerOilPumps['${k}'].cmdRun=!SimState.phys.powerOilPumps['${k}'].cmdRun;renderFaceplate();">
            ${k}: ${p.powerOilPumps[k].cmdRun?'CMD ON':'CMD OFF'}
          </button>
        `).join('')}
      </div>
    </div>`;
  }

  if (eq === 'OVERVIEW' || eq === 'WATERINJ') {
    html += `
    <div style="background:var(--bg-2);border:1px solid var(--border);border-radius:5px;padding:8px;margin-bottom:8px;">
      <div style="font-weight:700;color:var(--cyan);margin-bottom:6px;">WATER INJECTION MANIFOLD (PIT-002 &amp; P-3800/3900)</div>
      <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px;">
        <span>PIT-002 Pressure (PAL:200, PAH:800, PAHH:900):</span>
        <strong id="fp-lbl-pit002">${p.waterManifoldPsi.toFixed(0)} Psi</strong>
      </div>
      <input type="range" min="0" max="1500" step="10" value="${p.waterManifoldPsi}" style="width:100%;margin-bottom:6px;"
        oninput="SimState.coupledPhysics=false;updatePhysModeBtns();SimState.phys.waterManifoldPsi=parseFloat(this.value);document.getElementById('fp-lbl-pit002').textContent=this.value+' Psi';">
      <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px;">
        <span>Injection Choke Opening (Coupled ODE):</span>
        <strong id="fp-lbl-watchoke">${p.waterWellChokePct.toFixed(0)}%</strong>
      </div>
      <input type="range" min="20" max="100" value="${p.waterWellChokePct}" style="width:100%;"
        oninput="SimState.phys.waterWellChokePct=parseFloat(this.value);document.getElementById('fp-lbl-watchoke').textContent=this.value+'%';">
    </div>`;
  }

  if (eq === 'OVERVIEW' || eq === 'ESDV') {
    html += `
    <div style="background:var(--bg-2);border:1px solid var(--border);border-radius:5px;padding:8px;margin-bottom:8px;">
      <div style="font-weight:700;color:#d8b4fe;margin-bottom:6px;">FUEL GAS &amp; ESDV-001 PNEUMATICS</div>
      <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px;">
        <span>6401-PST-001 Fuel Gas (PAL:40, PAH:100):</span>
        <strong id="fp-lbl-fg">${p.fuelGasLinePsi.toFixed(1)} Psi</strong>
      </div>
      <input type="range" min="0" max="145" step="1" value="${p.fuelGasLinePsi}" style="width:100%;margin-bottom:6px;"
        oninput="SimState.phys.fuelGasSupplyPsi=parseFloat(this.value);SimState.phys.fuelGasLinePsi=parseFloat(this.value);document.getElementById('fp-lbl-fg').textContent=this.value+' Psi';">
      <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px;">
        <span>7002-PST-001 Air Accumulator (PAL:50):</span>
        <strong id="fp-lbl-air">${p.airAccPsi.toFixed(1)} Psi</strong>
      </div>
      <input type="range" min="0" max="100" step="1" value="${p.airAccPsi}" style="width:100%;margin-bottom:6px;"
        oninput="SimState.phys.airAccPsi=parseFloat(this.value);document.getElementById('fp-lbl-air').textContent=this.value+' Psi';">
      <div style="display:flex;gap:5px;flex-wrap:wrap;">
        <button class="btn ${p.airLeakFault?'danger':''}" style="padding:3px 7px;font-size:10.5px;" onclick="SimState.phys.airLeakFault=!SimState.phys.airLeakFault;renderFaceplate();">Air Leak: ${p.airLeakFault?'ON':'OFF'}</button>
        <button class="btn ${p.esdvStuckFault?'danger':''}" style="padding:3px 7px;font-size:10.5px;" onclick="SimState.phys.esdvStuckFault=!SimState.phys.esdvStuckFault;renderFaceplate();">Jam ESDV Stem: ${p.esdvStuckFault?'JAMMED':'FREE'}</button>
      </div>
    </div>`;
  }

  if (eq === 'OVERVIEW' || eq === 'T100' || eq === 'T200' || eq === 'T300' || eq === 'T400' || eq === 'EXPEDITION') {
    html += `
    <div style="background:var(--bg-2);border:1px solid var(--border);border-radius:5px;padding:8px;margin-bottom:8px;">
      <div style="font-weight:700;color:var(--green-hi);margin-bottom:6px;">STORAGE TANKS (LIT-100..400) &amp; EXPEDITION</div>
      ${['T100','T200','T300','T400'].map(tk => `
        <div style="display:flex;justify-content:space-between;font-size:11px;">
          <span>${tk} Level (LAL:0.7m, LAH:${tk==='T400'?'11.0':'9.0'}m):</span>
          <strong id="fp-lbl-${tk}">${p.tanks[tk].level.toFixed(2)} m</strong>
        </div>
        <input type="range" min="0" max="${p.tanks[tk].maxH}" step="0.1" value="${p.tanks[tk].level}" style="width:100%;margin-bottom:4px;"
          oninput="SimState.phys.tanks['${tk}'].level=parseFloat(this.value);document.getElementById('fp-lbl-${tk}').textContent=this.value+' m';">
      `).join('')}
      <div style="display:flex;justify-content:space-between;font-size:11px;margin-top:4px;">
        <span>PIT-001 Oil Expedition (PAL:10, PAH:100):</span>
        <strong id="fp-lbl-pit001">${p.oilExpPressPsi.toFixed(1)} Psi</strong>
      </div>
      <input type="range" min="0" max="160" step="1" value="${p.oilExpPressPsi}" style="width:100%;margin-bottom:4px;"
        oninput="SimState.coupledPhysics=false;updatePhysModeBtns();SimState.phys.oilExpPressPsi=parseFloat(this.value);document.getElementById('fp-lbl-pit001').textContent=this.value+' Psi';">
      <div style="display:flex;justify-content:space-between;font-size:11px;">
        <span>6401-FT-001 Export Flow (FAL:30, FAH:300):</span>
        <strong id="fp-lbl-ft001">${p.oilExpFlowBblH.toFixed(0)} bbl/h</strong>
      </div>
      <input type="range" min="0" max="420" step="5" value="${p.oilExpFlowBblH}" style="width:100%;"
        oninput="SimState.coupledPhysics=false;updatePhysModeBtns();SimState.phys.oilExpFlowBblH=parseFloat(this.value);document.getElementById('fp-lbl-ft001').textContent=this.value+' bbl/h';">
    </div>`;
  }

  if (eq === 'OVERVIEW' || eq === 'DELUGE') {
    html += `
    <div style="background:var(--bg-2);border:1px solid var(--border);border-radius:5px;padding:8px;">
      <div style="font-weight:700;color:#38bdf8;margin-bottom:6px;">DELUGE / FOAM SKID &amp; FAULT INJECTION</div>
      <div style="display:flex;gap:5px;flex-wrap:wrap;margin-bottom:6px;">
        <button class="btn ${p.pumpAFailFault?'danger':''}" style="padding:3px 7px;font-size:10.5px;"
          onclick="SimState.phys.pumpAFailFault=!SimState.phys.pumpAFailFault;renderFaceplate();">
          Simulate Pump A Fail-to-Run (10s -> Pump B): ${p.pumpAFailFault?'FAULT ON':'NORMAL'}
        </button>
        <button class="btn ${SimState.di.Pump_B_Inhibited?'warn':''}" style="padding:3px 7px;font-size:10.5px;"
          onclick="SimState.di.Pump_B_Inhibited=!SimState.di.Pump_B_Inhibited;renderFaceplate();">
          75-SB-01B Inhibit Pump B: ${SimState.di.Pump_B_Inhibited?'INHIBITED':'ENABLED'}
        </button>
      </div>
      <div style="display:flex;justify-content:space-between;font-size:11px;">
        <span>AFFF Foam Tank Level (Low &lt; 20%):</span>
        <strong id="fp-lbl-foam">${p.foamTankPct.toFixed(0)}%</strong>
      </div>
      <input type="range" min="0" max="100" value="${p.foamTankPct}" style="width:100%;margin-bottom:4px;"
        oninput="SimState.phys.foamTankPct=parseFloat(this.value);document.getElementById('fp-lbl-foam').textContent=this.value+'%';">
      <div style="display:flex;justify-content:space-between;font-size:11px;">
        <span>Diesel Fuel Tank Level (Low &lt; 20%):</span>
        <strong id="fp-lbl-dsl">${p.dieselTankPct.toFixed(0)}%</strong>
      </div>
      <input type="range" min="0" max="100" value="${p.dieselTankPct}" style="width:100%;"
        oninput="SimState.phys.dieselTankPct=parseFloat(this.value);document.getElementById('fp-lbl-dsl').textContent=this.value+'%';">
    </div>`;
  }

  body.innerHTML = html;
}
"""

JS_ENGINE_PART4 = r"""
// ============================================================================
// 6. TAB 2: 2D SPATIAL FIRE & GAS PLUME DISPERSION MAP & DETECTOR TABLE
// ============================================================================
function setHazardTool(type) {
  SimState.hazardTool = type;
  ['ch4','h2s','fire','smoke'].forEach(k => {
    const b = document.getElementById('hz-btn-' + k);
    if (b) b.classList.toggle('active', k.toUpperCase() === type);
  });
}

function updateWind() {
  SimState.windDirDeg = parseFloat(document.getElementById('sl-wind-dir').value);
  SimState.windSpeedMs = parseFloat(document.getElementById('sl-wind-spd').value);
  SimState.plumeReleaseStrength = parseFloat(document.getElementById('sl-plume-str').value);
  const dirs = ['E','SE','S','SW','W','NW','N','NE'];
  const compass = dirs[Math.round(SimState.windDirDeg / 45) % 8];
  document.getElementById('lbl-wind-dir').innerHTML = `${SimState.windDirDeg}&deg; ${compass}`;
  document.getElementById('lbl-wind-spd').textContent = `${SimState.windSpeedMs.toFixed(1)} m/s`;
  document.getElementById('lbl-plume-str').textContent = `${SimState.plumeReleaseStrength.toFixed(0)}%`;
}

function clearAllPlumes() {
  SimState.plumes = [];
  SimState.detectors.forEach(d => { d.manualVal = 0.0; d.faultMode = 'NONE'; });
  document.getElementById('lbl-plume-cnt').textContent = '0';
  renderFGDetectorTable();
}

function initFGCanvasEvents() {
  const cvs = document.getElementById('fg-plume-canvas');
  cvs.addEventListener('click', (e) => {
    const rect = cvs.getBoundingClientRect();
    const x = (e.clientX - rect.left) * (cvs.width / rect.width);
    const y = (e.clientY - rect.top) * (cvs.height / rect.height);
    SimState.plumes.push({
      x, y,
      type: SimState.hazardTool,
      strength: SimState.plumeReleaseStrength,
      created: SimState.simTimeSec
    });
    document.getElementById('lbl-plume-cnt').textContent = String(SimState.plumes.length);
    logSOE('HAZARD_INJECT', 'FIELD', `Injected ${SimState.hazardTool} source (${SimState.plumeReleaseStrength}%) at (${Math.round(x)},${Math.round(y)})`, 'WARN');
  });
}

function drawFGPlumeCanvas() {
  const cvs = document.getElementById('fg-plume-canvas');
  if (!cvs) return;
  const ctx = cvs.getContext('2d');
  const W = cvs.width, H = cvs.height;
  ctx.clearRect(0, 0, W, H);

  // Subtle plant grid
  ctx.strokeStyle = 'rgba(38,56,89,0.35)';
  ctx.lineWidth = 1;
  for (let x = 0; x < W; x += 50) { ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,H); ctx.stroke(); }
  for (let y = 0; y < H; y += 50) { ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(W,y); ctx.stroke(); }

  // Plant Zones matching General Arrangement 01-MAN-03-08
  const zones = [
    { x:95,  y:75,  w:295, h:285, title:'CRUDE STORAGE TANK BUND (T-100..T-400)', col:'#1e293b' },
    { x:425, y:95,  w:135, h:235, title:'HEATER TREATERS (V-710/810)', col:'#1e293b' },
    { x:590, y:95,  w:210, h:235, title:'PUMP HOUSE (POWER OIL & WATER INJ)', col:'#1e293b' },
    { x:845, y:95,  w:165, h:150, title:'GAS GENERATOR ROOM', col:'#1e293b' },
    { x:835, y:285, w:175, h:185, title:'PCR & ELECTRICAL ROOM', col:'#1e293b' },
    { x:380, y:360, w:230, h:110, title:'ESDV-001 & EXPORT MANIFOLD', col:'#1e293b' }
  ];
  zones.forEach(z => {
    ctx.fillStyle = 'rgba(15,23,42,0.75)';
    ctx.strokeStyle = '#334155';
    ctx.lineWidth = 1.5;
    ctx.fillRect(z.x, z.y, z.w, z.h);
    ctx.strokeRect(z.x, z.y, z.w, z.h);
    ctx.fillStyle = '#94a3b8';
    ctx.font = 'bold 10px Segoe UI';
    ctx.fillText(z.title, z.x + 8, z.y + 16);
  });

  // Draw Tanks inside Bund
  const tanks = [
    { x:180, y:165, r:34, lbl:'T-100' },
    { x:310, y:165, r:34, lbl:'T-200' },
    { x:180, y:265, r:34, lbl:'T-300' },
    { x:310, y:265, r:38, lbl:'T-400' }
  ];
  tanks.forEach(tk => {
    ctx.beginPath();
    ctx.arc(tk.x, tk.y, tk.r, 0, Math.PI * 2);
    ctx.fillStyle = '#0f172a';
    ctx.fill();
    ctx.strokeStyle = '#475569';
    ctx.stroke();
    ctx.fillStyle = '#64748b';
    ctx.font = 'bold 11px Consolas';
    ctx.textAlign = 'center';
    ctx.fillText(tk.lbl, tk.x, tk.y + 4);
  });
  ctx.textAlign = 'left';

  // Draw Open-Path IR Beam Line for 7404-DG-011R
  ctx.save();
  ctx.strokeStyle = '#38bdf8';
  ctx.setLineDash([6, 4]);
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(610, 210);
  ctx.lineTo(780, 210);
  ctx.stroke();
  ctx.restore();

  // Draw Active Plumes (Gaussian ellipses oriented along wind vector)
  const windRad = (SimState.windDirDeg * Math.PI) / 180.0;
  SimState.plumes.forEach(pl => {
    ctx.save();
    ctx.translate(pl.x, pl.y);
    ctx.rotate(windRad);
    const rMain = 75 + pl.strength * 1.4;
    const grad = ctx.createRadialGradient(rMain * 0.25, 0, 5, rMain * 0.35, 0, rMain);
    if (pl.type === 'CH4') {
      grad.addColorStop(0, 'rgba(245,158,11,0.65)');
      grad.addColorStop(0.5, 'rgba(245,158,11,0.25)');
      grad.addColorStop(1, 'rgba(245,158,11,0)');
    } else if (pl.type === 'H2S') {
      grad.addColorStop(0, 'rgba(236,72,153,0.65)');
      grad.addColorStop(0.5, 'rgba(168,85,247,0.25)');
      grad.addColorStop(1, 'rgba(168,85,247,0)');
    } else if (pl.type === 'FIRE') {
      grad.addColorStop(0, 'rgba(255,42,42,0.85)');
      grad.addColorStop(0.5, 'rgba(249,115,22,0.35)');
      grad.addColorStop(1, 'rgba(249,115,22,0)');
    } else {
      grad.addColorStop(0, 'rgba(148,163,184,0.75)');
      grad.addColorStop(0.5, 'rgba(100,116,139,0.3)');
      grad.addColorStop(1, 'rgba(100,116,139,0)');
    }
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.ellipse(rMain * 0.3, 0, rMain, rMain * 0.58, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  });

  // Draw All 33 Detectors on Map
  SimState.detectors.forEach(d => {
    ctx.save();
    let col = '#10b981'; // Healthy Green
    if (d.inhibited) col = '#64748b';
    else if (d.faultActive) col = '#a855f7';
    else if (d.hiActive) col = '#ff2a2a';
    else if (d.loActive) col = '#f59e0b';

    if (d.hiActive || d.loActive) {
      ctx.beginPath();
      ctx.arc(d.x, d.y, 16, 0, Math.PI * 2);
      ctx.fillStyle = d.hiActive ? 'rgba(239,68,68,0.28)' : 'rgba(245,158,11,0.24)';
      ctx.fill();
    }

    ctx.beginPath();
    ctx.arc(d.x, d.y, 7, 0, Math.PI * 2);
    ctx.fillStyle = col;
    ctx.fill();
    ctx.lineWidth = 1.5;
    ctx.strokeStyle = '#fff';
    ctx.stroke();

    ctx.fillStyle = '#e2e8f0';
    ctx.font = 'bold 9.5px Consolas';
    ctx.fillText(d.id.replace('7404-','').replace('7503-',''), d.x + 10, d.y - 2);
    ctx.fillStyle = col;
    ctx.font = '9px Consolas';
    ctx.fillText(`${d.val.toFixed(1)}${d.unit}`, d.x + 10, d.y + 9);
    ctx.restore();
  });
}

function renderFGDetectorTable() {
  const wrap = document.getElementById('fg-detector-table-wrap');
  if (!wrap) return;
  const q = (document.getElementById('fg-filter-inp')?.value || '').toLowerCase();
  const rows = SimState.detectors.filter(d => !q || d.id.toLowerCase().includes(q) || d.zone.toLowerCase().includes(q) || d.type.toLowerCase().includes(q));

  wrap.innerHTML = `
  <table class="data-table">
    <thead>
      <tr>
        <th>Tag / Slot</th>
        <th>Reading</th>
        <th>Override Slider</th>
        <th>Fault / Inhibit</th>
      </tr>
    </thead>
    <tbody>
      ${rows.map((d, idx) => {
        const realIdx = SimState.detectors.indexOf(d);
        let badge = `<span style="color:var(--green)">OK</span>`;
        if (d.inhibited) badge = `<span style="color:var(--text-2)">INHIB</span>`;
        else if (d.faultActive) badge = `<span style="color:var(--purple);font-weight:700">FAULT</span>`;
        else if (d.hiActive) badge = `<span style="color:var(--red-hi);font-weight:700">HIGH</span>`;
        else if (d.loActive) badge = `<span style="color:var(--amber);font-weight:700">LOW</span>`;

        return `
        <tr>
          <td>
            <div style="font-weight:700;color:var(--text-0)">${d.id}</div>
            <div style="font-size:9.5px;color:var(--text-2)">S${d.slot}:Ch${d.ch} | ${badge}</div>
          </td>
          <td id="fg-tbl-val-${realIdx}" style="font-weight:700;color:var(--cyan)">
            ${d.val.toFixed(1)} ${d.unit}
          </td>
          <td>
            <input type="range" min="${d.min}" max="${d.max}" step="${d.type==='LOS'?0.1:1}" value="${d.manualVal}" style="width:95px;"
              oninput="SimState.detectors[${realIdx}].manualVal=parseFloat(this.value);SimState.detectors[${realIdx}].faultMode='NONE';">
          </td>
          <td>
            <div style="display:flex;gap:3px;">
              <button class="btn ${d.faultMode!=='NONE'?'danger':''}" style="padding:2px 5px;font-size:9.5px;"
                onclick="cycleDetectorFault(${realIdx})">${d.faultMode==='NONE'?'Flt':d.faultMode.slice(0,4)}</button>
              <button class="btn ${d.inhibited?'warn':''}" style="padding:2px 5px;font-size:9.5px;"
                onclick="SimState.detectors[${realIdx}].inhibited=!SimState.detectors[${realIdx}].inhibited;renderFGDetectorTable();">Inh</button>
            </div>
          </td>
        </tr>`;
      }).join('')}
    </tbody>
  </table>`;
}

function cycleDetectorFault(idx) {
  const d = SimState.detectors[idx];
  const modes = d.type === 'LOS' ? ['NONE', 'WIRE_BREAK', 'OPTIC_BLOCK', 'OVERRANGE'] : ['NONE', 'WIRE_BREAK', 'OVERRANGE'];
  const next = modes[(modes.indexOf(d.faultMode) + 1) % modes.length];
  d.faultMode = next;
  renderFGDetectorTable();
}

// ============================================================================
// 7. TAB 3: PHYSICAL FGCP-7404-001 & PCR MATRIX PANEL MIMIC
// ============================================================================
function renderFGCPPanel() {
  const container = document.getElementById('fgcp-panel-container');
  if (!container) return;
  const di = SimState.di;
  const T = SimState.plc.tags;
  const sO = SimState.plc.slotO[8];

  const lamps = [
    { id:'L15', lbl:'L15: 6401-ESDV-001 OPEN',    col:'green', lit: sO[12] },
    { id:'L14', lbl:'L14: 6401-ESDV-001 CLOSED',  col:'red',   lit: sO[11] },
    { id:'L16', lbl:'L16: LOW AIR ACCUMULATOR',   col:'amber', lit: sO[13] },
    { id:'L17', lbl:'L17: LOW FUEL GAS LINE',     col:'amber', lit: sO[14] },
    { id:'L8',  lbl:'L8 / CR1: P-2300 STOPPED',   col:'red',   lit: sO[15] },
    { id:'L9',  lbl:'L9 / CR2: P-2400 STOPPED',   col:'red',   lit: sO[16] },
    { id:'L10', lbl:'L10 / CR3: P-2500 STOPPED',  col:'red',   lit: sO[17] },
    { id:'L11', lbl:'L11 / CR4: P-2600 STOPPED',  col:'red',   lit: sO[18] },
    { id:'L12', lbl:'L12 / CR5: P-3800 STOPPED',  col:'red',   lit: sO[19] },
    { id:'L13', lbl:'L13 / CR6: P-3900 STOPPED',  col:'red',   lit: sO[20] },
    { id:'SDGE',lbl:'SD-GE: GAS GEN SHUTDOWN',    col:'red',   lit: sO[21] },
    { id:'Z1',  lbl:'Z1: PROD CONTROL ROOM HORN', col:'red',   lit: sO[22] },
    { id:'PA1', lbl:'PA-001: PROCESS BLDG ALARM', col:'amber', lit: sO[23] },
    { id:'SA1', lbl:'7404-SA-001: PUMP HOUSE BELL',col:'red',  lit: sO[2] },
    { id:'H2SA',lbl:'H2SA-001/002: H2S BEACON',   col:'red',   lit: sO[30] },
    { id:'SDA', lbl:'SDA-001: SMOKE HORN/BEACON', col:'red',   lit: sO[31] },
    { id:'PMPA',lbl:'7503-PUMP-A DELUGE RUN',     col:'green', lit: sO[4] },
    { id:'PMPB',lbl:'7503-PUMP-B DIESEL START',   col:'amber', lit: sO[6] || SimState.phys.pumpBRunning },
    { id:'DELG',lbl:'FOAM / DELUGE RELEASED',     col:'red',   lit: T.R00475_5 },
    { id:'FLT', lbl:'SYSTEM / CHANNEL FAULT',     col:'amber', lit: !sO[10] }
  ];

  container.innerHTML = `
  <div class="fgcp-cabinet">
    <div style="display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #334155;padding-bottom:10px;margin-bottom:12px;">
      <div>
        <div style="font-size:15px;font-weight:800;letter-spacing:0.5px;color:#f8fafc;">FGCP-7404-001 &amp; PRODUCTION CONTROL ROOM (PCR) MATRIX PANEL</div>
        <div style="font-size:11px;color:#94a3b8;font-family:var(--font-mono)">Hardware Terminal Blocks TB-07 (1756-IB32) &amp; TB-08 (1756-OB32)</div>
      </div>
      <div style="display:flex;gap:8px;">
        <button class="btn warn" onclick="pressSystemMute()">E12 MUTE / ACCEPT</button>
        <button class="btn success" onclick="pressSystemReset()">E11 SYSTEM RESET</button>
      </div>
    </div>

    <div class="led-matrix-grid" style="margin-bottom:16px;">
      ${lamps.map(l => `
        <div class="panel-lamp">
          <div class="lamp-lens ${l.col} ${l.lit?'lit':''}" id="fgcp-lamp-${l.id}"></div>
          <div>
            <div style="font-weight:700;font-size:11px;color:#e2e8f0;">${l.lbl}</div>
            <div style="font-size:10px;font-family:var(--font-mono);color:${l.lit?'#fff':'#64748b'}">${l.lit?'ACTIVE (ON)':'OFF'}</div>
          </div>
        </div>
      `).join('')}
    </div>

    <!-- Keyswitches, Foam MACs & Individual Pump E-Stop Pushbuttons E1..E6 -->
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px;">
      <div class="card" style="background:#0b111c;">
        <div class="card-header">KEYSWITCHES (S2 / S3) &amp; STANDBY INHIBIT</div>
        <div class="card-body" style="display:flex;flex-direction:column;gap:8px;">
          <button class="btn ${di.INHIBIT_FOAM_REL?'warn':''}" onclick="SimState.di.INHIBIT_FOAM_REL=!SimState.di.INHIBIT_FOAM_REL;renderFGCPPanel();">
            &#128273; Keyswitch S2 (INHIBIT FOAM RELEASE): ${di.INHIBIT_FOAM_REL ? 'POS I (INHIBITED)' : 'POS O (NORMAL)'}
          </button>
          <button class="btn ${di.INHIBIT_ALL_OUTPUTS?'danger':''}" onclick="SimState.di.INHIBIT_ALL_OUTPUTS=!SimState.di.INHIBIT_ALL_OUTPUTS;renderFGCPPanel();">
            &#128273; Keyswitch S3 (INHIBIT ALL OUTPUTS): ${di.INHIBIT_ALL_OUTPUTS ? 'POS I (BYPASSED)' : 'POS O (NORMAL)'}
          </button>
          <button class="btn ${di.Pump_B_Inhibited?'warn':''}" onclick="SimState.di.Pump_B_Inhibited=!SimState.di.Pump_B_Inhibited;renderFGCPPanel();">
            75-SB-01B Standby Pump B Inhibit: ${di.Pump_B_Inhibited ? 'INHIBITED' : 'READY'}
          </button>
        </div>
      </div>

      <div class="card" style="background:#0b111c;">
        <div class="card-header">FOAM RELEASE MACs &amp; FOAM STOP BUTTONS</div>
        <div class="card-body" style="display:flex;flex-direction:column;gap:8px;">
          <button class="btn danger" onclick="triggerFoamMAC('7503-FR-003')">
            &#128293; Break Glass 7503-FR-003 (Inside PCR Foam Release)
          </button>
          <button class="btn danger" onclick="triggerFoamMAC('7503-FR-001/002')">
            &#128293; Break Glass 7503-FR-001/002 (Outside Bund Foam Release)
          </button>
          <button class="btn ${di.FS_FGCP_E8?'active':''}" onclick="pulseFoamStop()">
            &#9940; Press E8 / 7503-FS-001 (FOAM / DELUGE STOP)
          </button>
        </div>
      </div>

      <div class="card" style="background:#0b111c;">
        <div class="card-header">EMERGENCY SHUTDOWN MUSHROOM BUTTONS (E1–E6, E9)</div>
        <div class="card-body" style="display:grid;grid-template-columns:1fr 1fr;gap:6px;">
          <button class="btn ${di.ESTOP_P2300_E1?'danger':''}" onclick="SimState.di.ESTOP_P2300_E1=!SimState.di.ESTOP_P2300_E1;renderFGCPPanel();">E1: Stop P-2300 (${di.ESTOP_P2300_E1?'LATCHED':'OK'})</button>
          <button class="btn ${di.ESTOP_P2400_E2?'danger':''}" onclick="SimState.di.ESTOP_P2400_E2=!SimState.di.ESTOP_P2400_E2;renderFGCPPanel();">E2: Stop P-2400 (${di.ESTOP_P2400_E2?'LATCHED':'OK'})</button>
          <button class="btn ${di.ESTOP_P2500_E3?'danger':''}" onclick="SimState.di.ESTOP_P2500_E3=!SimState.di.ESTOP_P2500_E3;renderFGCPPanel();">E3: Stop P-2500 (${di.ESTOP_P2500_E3?'LATCHED':'OK'})</button>
          <button class="btn ${di.ESTOP_P2600_E4?'danger':''}" onclick="SimState.di.ESTOP_P2600_E4=!SimState.di.ESTOP_P2600_E4;renderFGCPPanel();">E4: Stop P-2600 (${di.ESTOP_P2600_E4?'LATCHED':'OK'})</button>
          <button class="btn ${di.ESTOP_P3800_E5?'danger':''}" onclick="SimState.di.ESTOP_P3800_E5=!SimState.di.ESTOP_P3800_E5;renderFGCPPanel();">E5: Stop P-3800 (${di.ESTOP_P3800_E5?'LATCHED':'OK'})</button>
          <button class="btn ${di.ESTOP_P3900_E6?'danger':''}" onclick="SimState.di.ESTOP_P3900_E6=!SimState.di.ESTOP_P3900_E6;renderFGCPPanel();">E6: Stop P-3900 (${di.ESTOP_P3900_E6?'LATCHED':'OK'})</button>
          <button class="btn ${di.ESDV_6401_E9_Pressed?'danger':''}" style="grid-column:span 2;" onclick="SimState.di.ESDV_6401_E9_Pressed=!SimState.di.ESDV_6401_E9_Pressed;renderFGCPPanel();">
            E9 (6401-ESDV-001): Station Fuel Gas ESD Button (${di.ESDV_6401_E9_Pressed?'PRESSED':'RELEASED'})
          </button>
        </div>
      </div>
    </div>
  </div>`;
}
"""

JS_ENGINE_PART5 = r"""
// ============================================================================
// 8. TAB 4: LIVE CAUSE & EFFECT MATRIX (01-MAN-03-07-PDF-C2C FINAL)
// ============================================================================
const CE_COLS = [
  { k:'EY',   lbl:'ESDV-001 Close',   fn: T => !T.EY_6401_001_002 },
  { k:'PO',   lbl:'P-2300..2600 Stop',fn: T => T.CR1_P2300_Stop },
  { k:'WI',   lbl:'P-3800/3900 Stop', fn: T => T.CR5_P3800_Stop },
  { k:'OB',   lbl:'P-2100/2200 Stop', fn: T => !T.P2100_P2200 },
  { k:'WB',   lbl:'P-3600/3700 Stop', fn: T => !T.P3600_P3700 },
  { k:'SDGE', lbl:'Gas Gen SD-GE',    fn: T => T.SD_GE },
  { k:'PMPA', lbl:'Deluge Pump A',    fn: T => T.PUMP_A },
  { k:'PMPB', lbl:'Diesel Pump B',    fn: T => T.PUMP_B_START || SimState.phys.pumpBRunning },
  { k:'L14',  lbl:'LED L14 Closed',   fn: T => T.Tag_DO_13 },
  { k:'L16',  lbl:'LED L16 Low Air',  fn: T => T.Tag_DO_14 },
  { k:'L17',  lbl:'LED L17 Low Gas',  fn: T => T.LED_Low_Fuel_Gas_L17 },
  { k:'Z1',   lbl:'Z1 PCR Horn',      fn: T => T.Tag_DO_15 },
  { k:'SA',   lbl:'SA-001 Bell',      fn: T => T.SA_7404_001_002 },
  { k:'PA',   lbl:'PA-001 Process',   fn: T => T.PA_001 },
  { k:'H2SA', lbl:'H2SA-001/002',     fn: T => T.H2SA_001_002 },
  { k:'SDA',  lbl:'SDA-001 Smoke',    fn: T => T.SDA_001 }
];

const CE_ROWS = [
  { id:'CH4_LO',  lbl:'7404-DG-001..012 / 011R Gas Low (20% LEL / 1 LELm)', act: T => T.R01500_0, spec:{Z1:'C', SA:'D'}, trig:()=>{SimState.detectors[0].manualVal=24;} },
  { id:'CH4_HI',  lbl:'7404-DG-001..012 / 011R Gas High (30% LEL / 3 LELm)',act: T => T.R01500_2, spec:{EY:'X',PO:'X',WI:'X',OB:'X',WB:'X',SDGE:'X',L14:'X',Z1:'C',SA:'C'}, trig:()=>{SimState.detectors[0].manualVal=35;} },
  { id:'GD_LO',   lbl:'GD-001..003 Gas Generator CH4 Low (20% LEL)',        act: T => T.GD_Any_Lo_Latch, spec:{Z1:'C', SA:'D'}, trig:()=>{SimState.detectors[13].manualVal=24;} },
  { id:'GD_HI',   lbl:'GD-001..003 Gas Generator CH4 High (30% LEL)',       act: T => T.GD_Any_Hi_Latch, spec:{SDGE:'X', Z1:'C'}, trig:()=>{SimState.detectors[13].manualVal=35;} },
  { id:'H2S_LO',  lbl:'H2S-001..012 Sour Gas Low (10 PPM)',                 act: T => T.H2S_Lo_Latch, spec:{Z1:'C', H2SA:'D'}, trig:()=>{SimState.detectors[16].manualVal=14;} },
  { id:'H2S_HI',  lbl:'H2S-001..012 Sour Gas High (20 PPM)',                act: T => T.H2S_Hi_Latch, spec:{Z1:'C', H2SA:'C'}, trig:()=>{SimState.detectors[16].manualVal=26;} },
  { id:'AIR_LO',  lbl:'7002-PST-001 Air Accumulator Low (<= 50 Psi)',       act: T => T.R00435_6, spec:{L16:'X', Z1:'C', PA:'C'}, trig:()=>{SimState.phys.airAccPsi=42;} },
  { id:'PIT3_LO', lbl:'PIT-003 Oil Manifold Low PAL (<= 1700 Psi)',         act: T => T.PIT_003_PAL, spec:{Z1:'C', PA:'D'}, trig:()=>{SimState.coupledPhysics=false;updatePhysModeBtns();SimState.phys.oilManifoldPsi=1550;} },
  { id:'PIT3_HI', lbl:'PIT-003 Oil Manifold High PAH (>= 2700 Psi)',        act: T => T.PIT_003_PAH, spec:{Z1:'C', PA:'C'}, trig:()=>{SimState.coupledPhysics=false;updatePhysModeBtns();SimState.phys.oilManifoldPsi=2740;} },
  { id:'PIT3_HH', lbl:'PIT-003 Oil Manifold High-High PAHH (>= 2800 Psi)',  act: T => T.PIT_003_PAHH_Latch, spec:{PO:'X',OB:'X',Z1:'C',PA:'C'}, trig:()=>{SimState.coupledPhysics=false;updatePhysModeBtns();SimState.phys.oilManifoldPsi=2860;} },
  { id:'PIT2_LO', lbl:'PIT-002 Water Manifold Low PAL (<= 200 Psi)',        act: T => T.PIT_002_PAL, spec:{Z1:'C', PA:'D'}, trig:()=>{SimState.coupledPhysics=false;updatePhysModeBtns();SimState.phys.waterManifoldPsi=150;} },
  { id:'PIT2_HI', lbl:'PIT-002 Water Manifold High PAH (>= 800 Psi)',       act: T => T.PIT_002_PAH, spec:{Z1:'C', PA:'C'}, trig:()=>{SimState.coupledPhysics=false;updatePhysModeBtns();SimState.phys.waterManifoldPsi=840;} },
  { id:'PIT2_HH', lbl:'PIT-002 Water Manifold High-High PAHH (>= 900 Psi)', act: T => T.PIT_002_PAHH_Latch, spec:{WI:'X',WB:'X',Z1:'C',PA:'C'}, trig:()=>{SimState.coupledPhysics=false;updatePhysModeBtns();SimState.phys.waterManifoldPsi=940;} },
  { id:'PIT1_AL', lbl:'PIT-001 Oil Expedition PAL (10) / PAH (100 Psi)',    act: T => T.PIT_001_PAL||T.PIT_001_PAH, spec:{Z1:'C', PA:'C'}, trig:()=>{SimState.coupledPhysics=false;updatePhysModeBtns();SimState.phys.oilExpPressPsi=115;} },
  { id:'FG_LO',   lbl:'6401-PST-001 Fuel Gas Line Low PAL (<= 40 Psi)',     act: T => T.R00455_6, spec:{L17:'X', Z1:'C', PA:'D'}, trig:()=>{SimState.phys.fuelGasSupplyPsi=32;SimState.phys.fuelGasLinePsi=32;} },
  { id:'FG_HI',   lbl:'6401-PST-001 Fuel Gas Line High PAH (>= 100 Psi)',   act: T => T.R00455_5, spec:{EY:'X',PO:'X',WI:'X',OB:'X',WB:'X',SDGE:'X',L14:'X',Z1:'C',PA:'C'}, trig:()=>{SimState.phys.fuelGasSupplyPsi=112;SimState.phys.fuelGasLinePsi=112;} },
  { id:'FT_AL',   lbl:'6401-FT-001 Flowmeter FAL (30) / FAH (300 bbl/h)',   act: T => T.FT_6401_001_FAL||T.FT_6401_001_FAH, spec:{Z1:'C', PA:'C'}, trig:()=>{SimState.coupledPhysics=false;updatePhysModeBtns();SimState.phys.oilExpFlowBblH=335;} },
  { id:'LIT_AL',  lbl:'LIT-100..400 Tank Level LAL (0.7m) / LAH (9m/11m)',  act: T => T.LIT_100_LAL||T.LIT_100_LAH||T.LIT_400_LAH, spec:{Z1:'C', PA:'D'}, trig:()=>{SimState.phys.tanks.T100.level=9.35;} },
  { id:'FLAME',   lbl:'7404-DF-001..003 Flame Detector Fire (>= 30%)',      act: T => T.R01501_0, spec:{EY:'X',PO:'X',WI:'X',OB:'X',WB:'X',SDGE:'X',PMPA:'X',PMPB:'10s',L14:'X',Z1:'C',SA:'C'}, trig:()=>{SimState.detectors[28].manualVal=55;} },
  { id:'SMOKE',   lbl:'SD-001/002 Electrical Room Smoke (>= 30%)',          act: T => T.SD_001_002_Latch, spec:{SDGE:'X', Z1:'C', SDA:'C'}, trig:()=>{SimState.detectors[31].manualVal=55;} },
  { id:'MAC_FM',  lbl:'7503-FR-001..003 Foam Release MAC Call Point',       act: T => T.R00495_5||T.R00535_5, spec:{EY:'X',PO:'X',WI:'X',OB:'X',WB:'X',SDGE:'X',PMPA:'X',PMPB:'10s',L14:'X',Z1:'C',SA:'C'}, trig:()=>{triggerFoamMAC('7503-FR-003');} },
  { id:'ESD_E9',  lbl:'6401-ESDV-001 (E9) ESD Fuel Gas Pushbutton',         act: T => T.R00707_1, spec:{EY:'X',PO:'X',WI:'X',OB:'X',WB:'X',L14:'X',Z1:'C'}, trig:()=>{triggerManualESD();} },
  { id:'ESTOP_14',lbl:'7404-SB-004..007 (E1..E4) Power Oil E-Stop',         act: T => T.Latch_ESTOP_P2300||T.Latch_ESTOP_P2400||T.Latch_ESTOP_P2500||T.Latch_ESTOP_P2600, spec:{PO:'X',Z1:'C',PA:'C'}, trig:()=>{SimState.di.ESTOP_P2300_E1=true;} },
  { id:'ESTOP_56',lbl:'7404-SB-008..009 (E5..E6) Water Inj E-Stop',         act: T => T.Latch_ESTOP_P3800||T.Latch_ESTOP_P3900, spec:{WI:'X',Z1:'C',PA:'C'}, trig:()=>{SimState.di.ESTOP_P3800_E5=true;} }
];

function renderCEMatrix() {
  const wrap = document.getElementById('ce-matrix-wrap');
  if (!wrap) return;
  const T = SimState.plc.tags;

  wrap.innerHTML = `
  <table class="ce-table">
    <thead>
      <tr>
        <th class="cause-col">CAUSE DESCRIPTION (01-MAN-03-07-PDF-C2C)</th>
        <th>TEST</th>
        ${CE_COLS.map(c => `<th style="writing-mode:vertical-rl;transform:rotate(180deg);height:110px;padding:6px 3px;color:${c.fn(T)?'#ff4d4d':'#cbd5e1'}">${c.lbl}</th>`).join('')}
      </tr>
    </thead>
    <tbody>
      ${CE_ROWS.map((r, rIdx) => {
        const isAct = Boolean(r.act(T));
        return `
        <tr class="${isAct?'cause-active':''}">
          <td class="cause-col">${r.lbl}</td>
          <td><button class="btn ${isAct?'danger':''}" style="padding:1px 6px;font-size:9.5px;" onclick="CE_ROWS[${rIdx}].trig();renderCEMatrix();">Trig</button></td>
          ${CE_COLS.map(c => {
            const sp = r.spec[c.k] || '';
            const hit = isAct && sp && c.fn(T);
            return `<td class="${hit?'ce-cell-hit':(sp?'ce-cell-spec':'')}">${sp}</td>`;
          }).join('')}
        </tr>`;
      }).join('')}
    </tbody>
  </table>`;
}

// ============================================================================
// 9. TAB 5: CONTROLLOGIX 1756 RACK & STUDIO 5000 LIVE ST DEBUGGER
// ============================================================================
function initSTSelector() {
  const sel = document.getElementById('sel-st-routine');
  if (!sel) return;
  sel.innerHTML = ROUTINE_ORDER.map((r, i) => `<option value="${r}">${String(i+1).padStart(2,'0')} - ${r}.st</option>`).join('');
  sel.value = 'MainRoutine';
}

function renderRackInspector() {
  const slot = parseInt(document.getElementById('sel-rack-slot')?.value || '2', 10);
  const body = document.getElementById('rack-inspector-body');
  if (!body) return;
  const sI = SimState.plc.slotI;
  const sO = SimState.plc.slotO;

  if (slot === 2 || slot === 3 || slot === 4) {
    const chLabels = {
      2: ['7404-DG-001','7404-DG-002','7404-DG-003','7404-DG-004','7404-DG-005','7404-DG-006','7404-DG-007','7404-DG-008','7404-DG-009','7404-DG-010','7404-DG-011','7404-DG-012','7404-DG-011R','GD-001 (New)','GD-002 (New)','GD-003 (New)'],
      3: ['PIT-001 Oil Exp','PIT-002 Water Inj','PIT-003 Power Oil','7503-PST-001 Deluge','7002-PST-001 Air Acc','6401-PST-001 Fuel Gas','7503-FR-003 Inside MAC','7503-FR-001/002 Out MAC','SpareAI_16','SpareAI_21','SpareAI_23','SpareAI_24','Spare_Ch12','Spare_Ch13','Spare_Ch14','Spare_Ch15'],
      4: ['H2S-001','H2S-002','H2S-003','H2S-004','H2S-005','H2S-006','H2S-007','H2S-008','H2S-009','H2S-010','H2S-011','H2S-012','7404-DF-001 Flame 1','7404-DF-002 Flame 2','7404-DF-003 Flame 3','SD-001/002 Smoke']
    }[slot];

    body.innerHTML = `
    <table class="data-table">
      <thead><tr><th>Address</th><th>Instrument Tag</th><th>Raw (0-32000)</th><th>Current</th></tr></thead>
      <tbody>
        ${chLabels.map((lbl, c) => {
          const raw = sI[slot][c] || 0;
          const mA = Math.max(0, Math.min(24, 4.0 + (raw / 32000.0) * 16.0));
          return `<tr>
            <td style="color:var(--cyan)">Local:${slot}:I.Ch${c}Data</td>
            <td>${lbl}</td>
            <td>${raw}</td>
            <td style="color:${mA<3.8||mA>20.8?'var(--red)':'var(--green)'}">${mA.toFixed(2)} mA</td>
          </tr>`;
        }).join('')}
      </tbody>
    </table>`;
  } else if (slot === 6) {
    const lts = [
      { c:0, t:'LIT-100 (Tank T-100)', v:SimState.phys.tanks.T100.level, u:'m' },
      { c:1, t:'LIT-200 (Tank T-200)', v:SimState.phys.tanks.T200.level, u:'m' },
      { c:2, t:'LIT-300 (Tank T-300)', v:SimState.phys.tanks.T300.level, u:'m' },
      { c:3, t:'LIT-400 (Tank T-400)', v:SimState.phys.tanks.T400.level, u:'m' }
    ];
    body.innerHTML = `
    <table class="data-table">
      <thead><tr><th>HART Address</th><th>Tag</th><th>Raw</th><th>EU Level</th></tr></thead>
      <tbody>
        ${lts.map(x => `<tr>
          <td style="color:var(--cyan)">Local:6:I.Ch${x.c}Data</td>
          <td>${x.t}</td>
          <td>${sI[6][x.c]}</td>
          <td style="color:var(--amber);font-weight:700">${x.v.toFixed(2)} ${x.u}</td>
        </tr>`).join('')}
      </tbody>
    </table>`;
  } else if (slot === 7) {
    const diNames = [
      '6401-ZSH-001 Open','6401-ZSL-001 Closed','FS_FGCP_E8 Foam Stop','7503-LS-002 Diesel Low',
      '7503-FS-001 Field Stop','7503-LS-001 Foam Low','75-C-01A Pump A Pulse','75-C-01B Pump B Pulse',
      '75-SB-01B Pump B Inh','SpareDI_11','Reset_PB_E11','Mute_PB_E12',
      '6401-ESDV-001 (E9)','INHIBIT_FOAM_REL (S2)','INHIBIT_ALL_OUTPUTS (S3)',
      '7404-SB-004 (E1 P2300)','7404-SB-005 (E2 P2400)','7404-SB-006 (E3 P2500)',
      '7404-SB-007 (E4 P2600)','7404-SB-008 (E5 P3800)','7404-SB-009 (E6 P3900)'
    ];
    body.innerHTML = `
    <table class="data-table">
      <thead><tr><th>Bit Address</th><th>Signal</th><th>State</th></tr></thead>
      <tbody>
        ${diNames.map((n, b) => `<tr>
          <td style="color:var(--cyan)">Local:7:I.Data.${b}</td>
          <td>${n}</td>
          <td><span class="${sI[7][b]?'st-val-true':'st-val-false'}">${sI[7][b]?'1 (TRUE)':'0 (FALSE)'}</span></td>
        </tr>`).join('')}
      </tbody>
    </table>`;
  } else if (slot === 8) {
    const doList = [
      [0,'PumpShutdown (ESD_TRIP)'],[1,'6401-EY-001/002 ESDV Solenoid'],[2,'7404-SA-001/002 Bell'],
      [3,'Pump_A_PulsOut'],[4,'7503-PUMP-A Start/Stop'],[5,'Pump_B_Start_PulsOut'],
      [6,'7503-PUMP-B Start'],[7,'7503-PUMP-B Stop'],[8,'P2100/2200 Oil Booster Relay'],
      [9,'P3600/3700 Water Booster Relay'],[10,'PLC_Fault (1=Healthy)'],[11,'L14 ESDV Closed LED'],
      [12,'L15 ESDV Open LED'],[13,'L16 Low Air Supply LED'],[14,'L17 Low Fuel Gas LED'],
      [15,'CR1 Stop P-2300 (L8)'],[16,'CR2 Stop P-2400 (L9)'],[17,'CR3 Stop P-2500 (L10)'],
      [18,'CR4 Stop P-2600 (L11)'],[19,'CR5 Stop P-3800 (L12)'],[20,'CR6 Stop P-3900 (L13)'],
      [21,'SD-GE Gas Gen Trip'],[22,'Z1 PCR Control Room Horn'],[23,'PA-001 Process Bldg Horn'],
      [30,'H2SA-001/002 H2S Horn'],[31,'SDA-001 Smoke Horn']
    ];
    body.innerHTML = `
    <table class="data-table">
      <thead><tr><th>Bit Address</th><th>Output Signal</th><th>State</th></tr></thead>
      <tbody>
        ${doList.map(([b, n]) => `<tr>
          <td style="color:var(--cyan)">Local:8:O.Data.${b}</td>
          <td>${n}</td>
          <td><span class="${sO[8][b]?'st-val-true':'st-val-false'}">${sO[8][b]?'1 (ON)':'0 (OFF)'}</span></td>
        </tr>`).join('')}
      </tbody>
    </table>`;
  } else {
    body.innerHTML = `
    <table class="data-table">
      <thead><tr><th>Modbus Reg</th><th>Equipment</th><th>Value</th></tr></thead>
      <tbody>
        <tr><td>Local:9:I.Data[0]</td><td>P-2300 TTD-H Run Status</td><td>${sI[9][0]} (${SimState.phys.powerOilPumps.P2300.rpm.toFixed(0)} RPM)</td></tr>
        <tr><td>Local:9:I.Data[1]</td><td>P-2400 TTD-H Run Status</td><td>${sI[9][1]} (${SimState.phys.powerOilPumps.P2400.rpm.toFixed(0)} RPM)</td></tr>
        <tr><td>Local:9:I.Data[2]</td><td>P-2500 TTD-H Run Status</td><td>${sI[9][2]} (${SimState.phys.powerOilPumps.P2500.rpm.toFixed(0)} RPM)</td></tr>
        <tr><td>Local:9:I.Data[3]</td><td>P-2600 S1501 Run Status</td><td>${sI[9][3]} (${SimState.phys.powerOilPumps.P2600.rpm.toFixed(0)} RPM)</td></tr>
        <tr><td>Local:9:I.Data[4]</td><td>P-3800 TTD-H Run Status</td><td>${sI[9][4]} (${SimState.phys.waterInjPumps.P3800.rpm.toFixed(0)} RPM)</td></tr>
        <tr><td>Local:9:I.Data[5]</td><td>P-3900 TTD-H Run Status</td><td>${sI[9][5]} (${SimState.phys.waterInjPumps.P3900.rpm.toFixed(0)} RPM)</td></tr>
        <tr><td>Local:9:I.Data[6]</td><td>6401-FT-001 Export Flow (x0.1 bbl/h)</td><td style="color:var(--green-hi);font-weight:700">${(sI[9][6]/10).toFixed(1)} bbl/h</td></tr>
      </tbody>
    </table>`;
  }
}

function renderSTDebugger() {
  const rName = document.getElementById('sel-st-routine')?.value || 'MainRoutine';
  const box = document.getElementById('st-debugger-box');
  if (!box) return;
  const rawCode = ST_ROUTINES[rName] || '';
  const T = SimState.plc.tags;

  // Escape HTML and overlay live tag values next to assignments
  const lines = rawCode.split('\n').map((line, idx) => {
    const numStr = String(idx + 1).padStart(3, ' ');
    let esc = line.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    if (esc.trim().startsWith('//')) {
      return `<span style="color:#475569">${numStr} | </span><span class="st-cmt">${esc}</span>`;
    }
    // Check if LHS of ':=' is a known tag in SimState.plc.tags
    let badge = '';
    const m = line.match(/^\s*([A-Za-z0-9_]+)\s*:=/);
    if (m && m[1] in T) {
      const val = T[m[1]];
      if (typeof val === 'boolean') {
        badge = ` <span class="${val?'st-val-true':'st-val-false'}">/* ${m[1]} = ${val?'TRUE':'FALSE'} */</span>`;
      } else if (typeof val === 'number') {
        badge = ` <span class="st-val-num">/* ${m[1]} = ${val.toFixed(2)} */</span>`;
      }
    }
    esc = esc.replace(/\b(IF|THEN|ELSIF|ELSE|END_IF|AND|OR|NOT|TRUE|FALSE|JSR|TONR|CTUD)\b/g, '<span class="st-kw">$1</span>');
    return `<span style="color:#475569">${numStr} | </span>${esc}${badge}`;
  });
  box.innerHTML = lines.join('\n');
}
"""

JS_ENGINE_PART6 = r"""
// ============================================================================
// 10. TAB 6: AUTOMATED FAT / SAT SCENARIO RUNNER
// ============================================================================
const FAT_SCENARIOS = [
  {
    id: 'FAT-01',
    title: 'FAT-01: Normal Steady-State Production & Reset',
    desc: 'Restores all tanks, manifolds, ESDV-001 (100% open), Power Oil pumps (P-2300..2500), Water Injection pumps (P-3800/3900), and 41 F&G channels to healthy steady state and issues System Reset (E11).',
    run: () => { resetPlantToNormal(); }
  },
  {
    id: 'FAT-02',
    title: 'FAT-02: CH4 Point Gas Leak Escalation (20% LEL Low -> 30% LEL High Station ESD)',
    desc: 'Injects 24% LEL on 7404-DG-001 (triggers Z1 Continuous + SA-001 Discontinuous Bell), then escalates to 36% LEL after 3s (triggers full Station ESD: closes 6401-ESDV-001, lights L14 Red LED, trips P-2300..2600, P-3800/3900, Boosters & Gas Generators).',
    run: () => {
      resetPlantToNormal();
      SimState.detectors[0].manualVal = 24.0;
      logSOE('FAT_STEP', '7404-DG-001', 'Step 1: Set 7404-DG-001 = 24.0 %LEL (Low Alarm >= 20%)', 'WARN');
      setTimeout(() => {
        SimState.detectors[0].manualVal = 36.0;
        logSOE('FAT_STEP', '7404-DG-001', 'Step 2: Escalated 7404-DG-001 = 36.0 %LEL (High Alarm >= 30% -> Full ESD)', 'ALARM');
      }, 3000);
    }
  },
  {
    id: 'FAT-03',
    title: 'FAT-03: Open-Path IR Detector 7404-DG-011R Optic Beam Block vs. Gas Cloud',
    desc: 'Tests the -0.78125 to -0.46875 LELm Optical Beam Block fault window (R00375_7 -> PLC_Fault without false ESD trip), then clears fault and injects 3.40 LELm gas cloud to verify High Gas ESD.',
    run: () => {
      resetPlantToNormal();
      SimState.detectors[12].faultMode = 'OPTIC_BLOCK';
      logSOE('FAT_STEP', '7404-DG-011R', 'Step 1: Injected Beam Block (-0.62 LELm) -> Optical Fault R00375_7', 'WARN');
      setTimeout(() => {
        SimState.detectors[12].faultMode = 'NONE';
        SimState.detectors[12].manualVal = 3.40;
        logSOE('FAT_STEP', '7404-DG-011R', 'Step 2: Cleared Beam Block & injected 3.40 LELm (>= 3.00 LELm High Gas ESD)', 'ALARM');
      }, 3500);
    }
  },
  {
    id: 'FAT-04',
    title: 'FAT-04: Gas Generator Room CH4 (GD-001) & Electrical Room Smoke (SD-001/002)',
    desc: 'Tests the new GNTF Upgrade inputs: triggers GD-001 >= 30% LEL and SD-001/002 >= 30% Smoke -> verifies SD-GE trips Gas Generators and activates SDA-001 & Z1 while main tank farm remains online.',
    run: () => {
      resetPlantToNormal();
      SimState.detectors[13].manualVal = 34.0;
      SimState.detectors[31].manualVal = 45.0;
      logSOE('FAT_STEP', 'GD-001 / SD-001', 'Triggered GD-001 (34% LEL) & SD-001/002 (45%) -> Verifying SD-GE & SDA-001', 'ALARM');
    }
  },
  {
    id: 'FAT-05',
    title: 'FAT-05: H2S Sour Gas Release (10 PPM Discontinuous -> 20 PPM Continuous)',
    desc: 'Sets H2S-001 to 14 PPM (verifying 1Hz pulsing H2SA-001/002 + Z1), then escalates to 25 PPM after 3.5s (verifying continuous H2SA-001/002 siren).',
    run: () => {
      resetPlantToNormal();
      SimState.detectors[16].manualVal = 14.0;
      logSOE('FAT_STEP', 'H2S-001', 'Step 1: Set H2S-001 = 14 PPM (Low H2S -> Discontinuous H2SA-001/002)', 'WARN');
      setTimeout(() => {
        SimState.detectors[16].manualVal = 25.0;
        logSOE('FAT_STEP', 'H2S-001', 'Step 2: Escalated H2S-001 = 25 PPM (High H2S -> Continuous H2SA-001/002)', 'ALARM');
      }, 3500);
    }
  },
  {
    id: 'FAT-06',
    title: 'FAT-06: Tank Farm Fire + Duty Deluge Pump A Failure -> 10s Auto-Start Diesel Pump B',
    desc: 'Arms Pump A Fail-to-Run fault and triggers Flame Detector 7404-DF-001 (60%). Verifies ESD trip, Pump A start command, 10-second pressure proving timer (TMR_PumpA_FailToRun), automatic changeover to Diesel Standby Pump B, and 7503-PST-001 > 50 Psi Foam Release!',
    run: () => {
      resetPlantToNormal();
      SimState.phys.pumpAFailFault = true;
      SimState.detectors[28].manualVal = 60.0;
      logSOE('FAT_STEP', '7404-DF-001', 'Triggered Flame Detector 1 (60%) with Pump A Fail-to-Run armed. Watch 10s timer start Diesel Pump B!', 'ALARM');
    }
  },
  {
    id: 'FAT-07',
    title: 'FAT-07: Power Oil Manifold Overpressure (PIT-003 -> 2700 PAH -> 2800 PAHH Trip)',
    desc: 'Ramps PIT-003 to 2730 Psi (PAH continuous PA-001 alarm), then to 2850 Psi (PAHH -> automatic shutdown of Power Oil Pumps P-2300..2600 via CR1..CR4 and Oil Booster P-2100/2200).',
    run: () => {
      resetPlantToNormal();
      SimState.coupledPhysics = false; updatePhysModeBtns();
      SimState.phys.oilManifoldPsi = 2730;
      logSOE('FAT_STEP', 'PIT-003', 'Step 1: PIT-003 = 2730 Psi (PAH >= 2700 Psi)', 'WARN');
      setTimeout(() => {
        SimState.phys.oilManifoldPsi = 2850;
        logSOE('FAT_STEP', 'PIT-003', 'Step 2: PIT-003 = 2850 Psi (PAHH >= 2800 Psi -> Trips Power Oil & Booster Pumps)', 'ALARM');
      }, 2500);
    }
  },
  {
    id: 'FAT-08',
    title: 'FAT-08: Water Injection Manifold Overpressure (PIT-002 -> 800 PAH -> 900 PAHH Trip)',
    desc: 'Ramps PIT-002 to 830 Psi (PAH), then to 935 Psi (PAHH -> automatic shutdown of Water Injection Pumps P-3800/3900 via CR5..CR6 and Water Booster P-3600/3700).',
    run: () => {
      resetPlantToNormal();
      SimState.coupledPhysics = false; updatePhysModeBtns();
      SimState.phys.waterManifoldPsi = 830;
      setTimeout(() => {
        SimState.phys.waterManifoldPsi = 935;
        logSOE('FAT_STEP', 'PIT-002', 'PIT-002 = 935 Psi (PAHH >= 900 Psi -> Trips Water Injection & Booster Pumps)', 'ALARM');
      }, 2500);
    }
  },
  {
    id: 'FAT-09',
    title: 'FAT-09: Maintenance Keyswitch S2 (Foam Inhibit) & S3 (All Outputs Inhibit) Proof Test',
    desc: 'Activates Keyswitch S3 (INHIBIT_ALL_OUTPUTS) and injects 40% LEL CH4 + Flame. Verifies that Z1 alarm activates in PCR while ESDV-001, Pumps, and Deluge remain un-tripped for online maintenance testing.',
    run: () => {
      resetPlantToNormal();
      SimState.di.INHIBIT_ALL_OUTPUTS = true;
      SimState.detectors[0].manualVal = 40.0;
      SimState.detectors[28].manualVal = 55.0;
      logSOE('FAT_STEP', 'S3_KEYSWITCH', 'Activated S3 (INHIBIT_ALL_OUTPUTS) + injected 40% LEL & Flame -> Outputs bypassed, Z1 active', 'WARN');
    }
  }
];

function renderScenariosView() {
  const body = document.getElementById('scenarios-body');
  if (!body) return;
  body.innerHTML = `
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:10px;">
    ${FAT_SCENARIOS.map((s, idx) => `
      <div class="card" style="background:var(--bg-2);">
        <div class="card-header">
          <span style="color:var(--cyan)">${s.title}</span>
        </div>
        <div class="card-body" style="display:flex;flex-direction:column;justify-content:space-between;gap:10px;">
          <p style="color:var(--text-1);line-height:1.45;font-size:12px;">${s.desc}</p>
          <button class="btn active" style="align-self:flex-start;" onclick="executeFATScenario(${idx})">&#9654; Execute ${s.id}</button>
        </div>
      </div>
    `).join('')}
  </div>`;
}

function executeFATScenario(idx) {
  const s = FAT_SCENARIOS[idx];
  document.getElementById('scen-active-status').textContent = `Running ${s.title}...`;
  s.run();
}

// ============================================================================
// 11. ISA-18.2 ALARM MANAGER, SOE HISTORIAN, MULTI-PEN TRENDS & WEB AUDIO
// ============================================================================
function formatSimTime(sec) {
  const hrs = Math.floor(sec / 3600);
  const mins = Math.floor((sec % 3600) / 60);
  const s = (sec % 60).toFixed(1);
  return `${String(hrs).padStart(2,'0')}:${String(mins).padStart(2,'0')}:${String(s).padStart(4,'0')}`;
}

function logSOE(type, tag, msg, prio='INFO') {
  SimState.soeLog.unshift({
    time: formatSimTime(SimState.simTimeSec),
    type, tag, msg, prio
  });
  if (SimState.soeLog.length > 250) SimState.soeLog.pop();
}

function syncAlarms() {
  const T = SimState.plc.tags;
  const defs = [
    { id:'ALM_ESD',    cond:!T.R01510_0,           tag:'ESD_TRIP',       grp:'ESD',     prio:'CRITICAL', msg:'MASTER EMERGENCY SHUTDOWN ACTIVE — ESDV-001 CLOSED & PUMPS TRIPPED' },
    { id:'ALM_GAS_HI', cond:T.R01500_2,            tag:'7404-DG-001..12',grp:'F&G',     prio:'CRITICAL', msg:`HIGH CH4 GAS DETECTED (>= 30% LEL / 3 LELm) — COUNT: ${T.Vote_Gas_Hi_Count}` },
    { id:'ALM_GAS_LO', cond:T.R01500_0,            tag:'7404-DG-001..12',grp:'F&G',     prio:'HIGH',     msg:`LOW CH4 GAS DETECTED (>= 20% LEL / 1 LELm) — COUNT: ${T.Vote_Gas_Lo_Count}` },
    { id:'ALM_FLAME',  cond:T.R01501_0,            tag:'7404-DF-001..03',grp:'F&G',     prio:'CRITICAL', msg:`FLAME / FIRE DETECTED — DELUGE & STATION ESD INITIATED` },
    { id:'ALM_DELUGE', cond:T.R00475_5,            tag:'7503-PST-001',   grp:'DELUGE',  prio:'CRITICAL', msg:`FOAM / DELUGE RELEASED (LINE PRESSURE >= 50 PSI)` },
    { id:'ALM_MAC',    cond:T.R00495_5||T.R00535_5,tag:'7503-FR-001..03',grp:'DELUGE',  prio:'CRITICAL', msg:`MANUAL FOAM RELEASE CALL POINT ACTIVATED` },
    { id:'ALM_GD_HI',  cond:T.GD_Any_Hi_Latch,     tag:'GD-001..003',    grp:'GAS_GEN', prio:'CRITICAL', msg:`GAS GENERATOR ROOM HIGH CH4 (>= 30% LEL) — SD-GE TRIPPED` },
    { id:'ALM_GD_LO',  cond:T.GD_Any_Lo_Latch,     tag:'GD-001..003',    grp:'GAS_GEN', prio:'HIGH',     msg:`GAS GENERATOR ROOM LOW CH4 (>= 20% LEL)` },
    { id:'ALM_SMOKE',  cond:T.SD_001_002_Latch,    tag:'SD-001/002',     grp:'ELEC_RM', prio:'CRITICAL', msg:`ELECTRICAL ROOM SMOKE DETECTED — SD-GE & SDA-001 ACTIVE` },
    { id:'ALM_H2S_HI', cond:T.H2S_Hi_Latch,        tag:'H2S-001..012',   grp:'F&G',     prio:'CRITICAL', msg:`HIGH H2S TOXIC GAS (>= 20 PPM) — CONTINUOUS H2SA SIREN` },
    { id:'ALM_H2S_LO', cond:T.H2S_Lo_Latch,        tag:'H2S-001..012',   grp:'F&G',     prio:'HIGH',     msg:`LOW H2S TOXIC GAS (>= 10 PPM) — DISCONTINUOUS H2SA SIREN` },
    { id:'ALM_PIT3_HH',cond:T.PIT_003_PAHH_Latch,  tag:'PIT-003',        grp:'PROCESS', prio:'CRITICAL', msg:`OIL MANIFOLD HIGH-HIGH PAHH (>= 2800 PSI) — POWER OIL PUMPS TRIPPED` },
    { id:'ALM_PIT3_H', cond:T.PIT_003_PAH,         tag:'PIT-003',        grp:'PROCESS', prio:'HIGH',     msg:`OIL MANIFOLD HIGH PRESSURE PAH (>= 2700 PSI)` },
    { id:'ALM_PIT3_L', cond:T.PIT_003_PAL,         tag:'PIT-003',        grp:'PROCESS', prio:'MEDIUM',   msg:`OIL MANIFOLD LOW PRESSURE PAL (<= 1700 PSI)` },
    { id:'ALM_PIT2_HH',cond:T.PIT_002_PAHH_Latch,  tag:'PIT-002',        grp:'PROCESS', prio:'CRITICAL', msg:`WATER MANIFOLD HIGH-HIGH PAHH (>= 900 PSI) — WATER PUMPS TRIPPED` },
    { id:'ALM_PIT2_H', cond:T.PIT_002_PAH,         tag:'PIT-002',        grp:'PROCESS', prio:'HIGH',     msg:`WATER MANIFOLD HIGH PRESSURE PAH (>= 800 PSI)` },
    { id:'ALM_PIT2_L', cond:T.PIT_002_PAL,         tag:'PIT-002',        grp:'PROCESS', prio:'MEDIUM',   msg:`WATER MANIFOLD LOW PRESSURE PAL (<= 200 PSI)` },
    { id:'ALM_PIT1',   cond:T.PIT_001_PAL||T.PIT_001_PAH, tag:'PIT-001', grp:'PROCESS', prio:'HIGH',     msg:`OIL EXPEDITION PRESSURE ALARM (${SimState.phys.oilExpPressPsi.toFixed(1)} PSI)` },
    { id:'ALM_FG_HI',  cond:T.R00455_5,            tag:'6401-PST-001',   grp:'PROCESS', prio:'CRITICAL', msg:`FUEL GAS HIGH PRESSURE PAH (>= 100 PSI) — ESD TRIPPED` },
    { id:'ALM_FG_LO',  cond:T.R00455_6,            tag:'6401-PST-001',   grp:'PROCESS', prio:'HIGH',     msg:`FUEL GAS LOW PRESSURE PAL (<= 40 PSI) — LED L17 ON` },
    { id:'ALM_AIR_LO', cond:T.R00435_6,            tag:'7002-PST-001',   grp:'PROCESS', prio:'HIGH',     msg:`ESDV AIR ACCUMULATOR LOW PRESSURE (<= 50 PSI) — LED L16 ON` },
    { id:'ALM_FT001',  cond:T.FT_6401_001_FAL||T.FT_6401_001_FAH, tag:'6401-FT-001', grp:'PROCESS', prio:'MEDIUM', msg:`EXPORT FLOWMETER ALARM (${SimState.phys.oilExpFlowBblH.toFixed(1)} BBL/H)` },
    { id:'ALM_TANKS',  cond:T.LIT_100_LAL||T.LIT_100_LAH||T.LIT_200_LAL||T.LIT_200_LAH||T.LIT_300_LAL||T.LIT_300_LAH||T.LIT_400_LAL||T.LIT_400_LAH, tag:'LIT-100..400', grp:'TANKS', prio:'HIGH', msg:`STORAGE TANK LEVEL ALARM (LAL <= 0.7m OR LAH >= 9m/11m)` },
    { id:'ALM_FOAM_LO',cond:T.R00702_1,            tag:'7503-LS-001',    grp:'DELUGE',  prio:'HIGH',     msg:`AFFF FOAM CONCENTRATE TANK LOW LEVEL` },
    { id:'ALM_DSL_LO', cond:T.R00703_1,            tag:'7503-LS-002',    grp:'DELUGE',  prio:'HIGH',     msg:`DIESEL FUEL TANK LOW LEVEL` },
    { id:'ALM_E9',     cond:T.R00707_1,            tag:'6401-ESDV-001',  grp:'ESD',     prio:'CRITICAL', msg:`MANUAL ESD FUEL GAS PUSHBUTTON E9 LATCHED` },
    { id:'ALM_ESTOP',  cond:T.Latch_ESTOP_P2300||T.Latch_ESTOP_P2400||T.Latch_ESTOP_P2500||T.Latch_ESTOP_P2600||T.Latch_ESTOP_P3800||T.Latch_ESTOP_P3900, tag:'7404-SB-004..09', grp:'ESD', prio:'CRITICAL', msg:`INDIVIDUAL PUMP EMERGENCY STOP BUTTON (E1..E6) ACTIVATED` },
    { id:'ALM_FLT',    cond:T.Any_Channel_Fault,   tag:'PLC_FAULT',      grp:'SYSTEM',  prio:'HIGH',     msg:`TRANSMITTER 4-20mA / OPTIC BEAM / VALVE DISCREPANCY FAULT` }
  ];

  defs.forEach(d => {
    const ex = SimState.activeAlarms[d.id];
    if (d.cond) {
      if (!ex) {
        SimState.activeAlarms[d.id] = {
          id: d.id, time: formatSimTime(SimState.simTimeSec),
          tag: d.tag, grp: d.grp, prio: d.prio, msg: d.msg,
          ack: Boolean(T.Alarm_Silence_Latch), active: true
        };
        logSOE('ALARM_ON', d.tag, d.msg, d.prio);
      } else {
        ex.msg = d.msg;
        if (T.M00001_System_Accept || T.Alarm_Silence_Latch) ex.ack = true;
      }
    } else if (ex) {
      logSOE('ALARM_RTN', d.tag, `Returned to normal: ${d.msg}`, 'INFO');
      delete SimState.activeAlarms[d.id];
    }
  });
}

function renderAlarmBanner() {
  const list = Object.values(SimState.activeAlarms);
  const unackCnt = list.filter(a => !a.ack).length;
  document.getElementById('alm-summary-counts').textContent = `${list.length} Active | ${unackCnt} Unacknowledged`;
  const bAlm = document.getElementById('badge-alm');
  if (bAlm) {
    bAlm.textContent = String(list.length);
    bAlm.classList.toggle('alert', list.length > 0);
  }

  const wrap = document.getElementById('live-alarm-banner');
  if (!wrap) return;
  if (list.length === 0) {
    wrap.innerHTML = `<div style="color:var(--green);padding:8px;">&#10004; ALL SYSTEMS NORMAL — NO ACTIVE ALARMS</div>`;
    return;
  }
  wrap.innerHTML = list.map(a => `
    <div class="alm-row ${a.ack?'ack':'unack'}">
      <span>${a.time}</span>
      <span style="font-weight:700">${a.prio}</span>
      <span style="color:var(--cyan);font-weight:700">${a.tag}</span>
      <span>${a.msg}</span>
      <span>${a.ack ? 'ACKNOWLEDGED' : 'UNACKNOWLEDGED'}</span>
      <button class="btn" style="padding:1px 6px;font-size:10px;" onclick="SimState.activeAlarms['${a.id}'].ack=true;renderAlarmBanner();">ACK</button>
    </div>
  `).join('');
}

function drawTrendCanvas() {
  const cvs = document.getElementById('trend-canvas');
  if (!cvs) return;
  const ctx = cvs.getContext('2d');
  const W = cvs.width, H = cvs.height;
  ctx.clearRect(0, 0, W, H);

  ctx.strokeStyle = 'rgba(38,56,89,0.45)';
  for (let y = 0; y <= H; y += H/5) {
    ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(W,y); ctx.stroke();
  }

  const hist = SimState.trendHistory;
  if (hist.length < 2) return;

  const pens = [
    { k:'pit3', max:3000, col:'#f59e0b' },
    { k:'pit2', max:1500, col:'#00d4ff' },
    { k:'fg',   max:150,  col:'#a855f7' },
    { k:'ft',   max:500,  col:'#22c55e' },
    { k:'ch4',  max:100,  col:'#ef4444' },
    { k:'h2s',  max:100,  col:'#ec4899' }
  ];

  pens.forEach(pen => {
    ctx.beginPath();
    ctx.strokeStyle = pen.col;
    ctx.lineWidth = 2;
    hist.forEach((pt, idx) => {
      const x = (idx / (hist.length - 1)) * W;
      const y = H - Math.min(1, Math.max(0, pt[pen.k] / pen.max)) * (H - 20) - 10;
      if (idx === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();
  });
}

function renderSOELog() {
  const wrap = document.getElementById('soe-log-wrap');
  if (!wrap) return;
  wrap.innerHTML = `
  <table class="data-table">
    <thead><tr><th>Sim Time</th><th>Event</th><th>Tag</th><th>Description</th></tr></thead>
    <tbody>
      ${SimState.soeLog.slice(0, 80).map(e => `
        <tr>
          <td>${e.time}</td>
          <td style="color:${e.prio==='CRITICAL'||e.prio==='ALARM'?'var(--red-hi)':(e.prio==='WARN'?'var(--amber)':'var(--cyan)')};font-weight:700">${e.type}</td>
          <td>${e.tag}</td>
          <td>${e.msg}</td>
        </tr>
      `).join('')}
    </tbody>
  </table>`;
}

function exportSOECSV() {
  const rows = [['SimTime','Type','Tag','Priority','Message']];
  SimState.soeLog.forEach(e => rows.push([e.time, e.type, e.tag, e.prio, `"${e.msg}"`]));
  const csv = rows.map(r => r.join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'GNTF_FAT_SAT_Event_Historian.csv';
  a.click();
}

// ============================================================================
// 12. TOP HEADER, QUICK FGCP STRIP & OPERATOR ACTION HANDLERS
// ============================================================================
function updateHeaderAndQuickStrip() {
  const p = SimState.phys;
  const T = SimState.plc.tags;
  const sO = SimState.plc.slotO[8];

  document.getElementById('kpi-sim-time').textContent = formatSimTime(SimState.simTimeSec);

  // ESD Status
  const esdDot = document.getElementById('kpi-esd-dot');
  const esdTxt = document.getElementById('kpi-esd-txt');
  if (sO[0]) {
    esdDot.className = 'kpi-dot';
    esdTxt.textContent = 'HEALTHY (1)';
    esdTxt.style.color = 'var(--green-hi)';
  } else {
    esdDot.className = 'kpi-dot alarm';
    esdTxt.textContent = 'ESD TRIPPED (0)';
    esdTxt.style.color = 'var(--red-hi)';
  }

  // ESDV-001
  const esdvDot = document.getElementById('kpi-esdv-dot');
  const esdvTxt = document.getElementById('kpi-esdv-txt');
  if (p.esdvPositionPct >= 95) {
    esdvDot.className = 'kpi-dot';
    esdvTxt.textContent = 'OPEN (100%)';
    esdvTxt.style.color = 'var(--green-hi)';
  } else if (p.esdvPositionPct <= 5) {
    esdvDot.className = 'kpi-dot alarm';
    esdvTxt.textContent = 'CLOSED (0%)';
    esdvTxt.style.color = 'var(--red-hi)';
  } else {
    esdvDot.className = 'kpi-dot warn';
    esdvTxt.textContent = `TRANSIT (${p.esdvPositionPct.toFixed(0)}%)`;
    esdvTxt.style.color = 'var(--amber)';
  }

  // Deluge Status
  const delDot = document.getElementById('kpi-deluge-dot');
  const delTxt = document.getElementById('kpi-deluge-txt');
  if (T.R00475_5) {
    delDot.className = 'kpi-dot alarm';
    delTxt.textContent = `RELEASED (${p.delugeLinePsi.toFixed(0)} Psi)`;
    delTxt.style.color = 'var(--red-hi)';
  } else if (T.Foam_Release_Demand) {
    delDot.className = 'kpi-dot warn';
    delTxt.textContent = 'STARTING PUMPS...';
    delTxt.style.color = 'var(--amber)';
  } else {
    delDot.className = 'kpi-dot';
    delTxt.textContent = 'STANDBY';
    delTxt.style.color = 'var(--cyan)';
  }

  // Quick FGCP LEDs
  const setChip = (id, on, cls) => {
    const el = document.getElementById(id);
    if (el) el.className = 'led-chip' + (on ? ' ' + cls : '');
  };
  setChip('qled-l15', sO[12], 'on-green');
  setChip('qled-l14', sO[11], 'on-red');
  setChip('qled-l16', sO[13], 'on-amber');
  setChip('qled-l17', sO[14], 'on-amber');
  setChip('qled-z1',  sO[22], 'on-red');
  setChip('qled-sa',  sO[2],  'on-red');
  setChip('qled-h2s', sO[30], 'on-red');
  setChip('qled-sda', sO[31], 'on-red');
  setChip('qled-sdge',sO[21], 'on-red');
}

function toggleSimRun() {
  SimState.running = !SimState.running;
  const b = document.getElementById('btn-play-pause');
  b.innerHTML = SimState.running ? '&#9654; RUNNING' : '&#10074;&#10074; PAUSED';
  b.classList.toggle('active', SimState.running);
}

function setSimSpeed(val) {
  SimState.speed = parseFloat(val);
}

function setPhysicsCoupling(coupled) {
  SimState.coupledPhysics = coupled;
  updatePhysModeBtns();
}

function updatePhysModeBtns() {
  document.getElementById('btn-phys-auto')?.classList.toggle('active', SimState.coupledPhysics);
  document.getElementById('btn-phys-man')?.classList.toggle('active', !SimState.coupledPhysics);
}

function pressSystemMute() {
  SimState.plc.M00001 = true;
  Object.values(SimState.activeAlarms).forEach(a => a.ack = true);
  logSOE('OPERATOR', 'Mute_PB_E12', 'Operator pressed E12 Mute / System Accept (M00001)', 'INFO');
  renderAlarmBanner();
}

function pressSystemReset() {
  SimState.plc.M00002 = true;
  SimState.di.ESDV_6401_E9_Pressed = false;
  SimState.di.FS_FGCP_E8 = false;
  SimState.di.FS_7503_001_Pressed = false;
  SimState.di.ESTOP_P2300_E1 = false;
  SimState.di.ESTOP_P2400_E2 = false;
  SimState.di.ESTOP_P2500_E3 = false;
  SimState.di.ESTOP_P2600_E4 = false;
  SimState.di.ESTOP_P3800_E5 = false;
  SimState.di.ESTOP_P3900_E6 = false;
  // Reset Foam MACs if active
  SimState.detectors.filter(d => d.type === 'MAC').forEach(d => d.manualVal = 0);
  logSOE('OPERATOR', 'Reset_PB_E11', 'Operator pressed E11 System Reset (M00002)', 'INFO');
}

function triggerManualESD() {
  SimState.di.ESDV_6401_E9_Pressed = true;
  logSOE('ESD_BUTTON', '6401-ESDV-001', 'Field/Panel ESD Fuel Gas Pushbutton E9 Pressed!', 'CRITICAL');
}

function triggerFoamMAC(id) {
  const d = SimState.detectors.find(x => x.id === id);
  if (d) d.manualVal = 65.0;
  logSOE('FOAM_MAC', id, `Manual Foam Release Call Point ${id} Activated!`, 'CRITICAL');
}

function pulseFoamStop() {
  SimState.di.FS_FGCP_E8 = true;
  SimState.detectors.filter(d => d.type === 'FLAME' || d.type === 'MAC').forEach(d => d.manualVal = 0);
  SimState.plumes = SimState.plumes.filter(p => p.type !== 'FIRE');
  logSOE('FOAM_STOP', 'FS_FGCP_E8', 'Foam Stop Button Pressed — Stopping Deluge Pumps A & B', 'WARN');
  setTimeout(() => { SimState.di.FS_FGCP_E8 = false; }, 1200);
}

function resetPlantToNormal() {
  SimState.coupledPhysics = true;
  updatePhysModeBtns();
  SimState.plumes = [];
  SimState.detectors.forEach(d => {
    d.manualVal = 0.0; d.plumeVal = 0.0; d.val = 0.0;
    d.faultMode = 'NONE'; d.inhibited = false;
    d.loActive = false; d.hiActive = false; d.faultActive = false;
  });
  const p = SimState.phys;
  p.tanks.T100.level = 5.20; p.tanks.T200.level = 6.40;
  p.tanks.T300.level = 4.10; p.tanks.T400.level = 7.80;
  p.airAccPsi = 82.0; p.airLeakFault = false;
  p.fuelGasSupplyPsi = 72.0; p.fuelGasLinePsi = 68.0;
  p.esdvPositionPct = 100.0; p.esdvStuckFault = false;
  p.oilExpPressPsi = 58.0; p.oilExpFlowBblH = 185.0; p.oilExpChokePct = 75.0;
  p.powerOilPumps.P2300.cmdRun = true; p.powerOilPumps.P2300.running = true; p.powerOilPumps.P2300.rpm = 1650;
  p.powerOilPumps.P2400.cmdRun = true; p.powerOilPumps.P2400.running = true; p.powerOilPumps.P2400.rpm = 1650;
  p.powerOilPumps.P2500.cmdRun = true; p.powerOilPumps.P2500.running = true; p.powerOilPumps.P2500.rpm = 1620;
  p.powerOilPumps.P2600.cmdRun = false; p.powerOilPumps.P2600.running = false; p.powerOilPumps.P2600.rpm = 0;
  p.oilManifoldPsi = 2150.0; p.oilWellChokePct = 68.0;
  p.waterInjPumps.P3800.cmdRun = true; p.waterInjPumps.P3800.running = true; p.waterInjPumps.P3800.rpm = 1580;
  p.waterInjPumps.P3900.cmdRun = true; p.waterInjPumps.P3900.running = true; p.waterInjPumps.P3900.rpm = 1580;
  p.waterManifoldPsi = 540.0; p.waterWellChokePct = 70.0;
  p.pumpARunning = false; p.pumpAFailFault = false; p.pumpAWireBreak = false;
  p.pumpBRunning = false; p.pumpBWireBreak = false;
  p.delugeLinePsi = 0.0; p.foamTankPct = 92.0; p.dieselTankPct = 88.0;
  p.gasGenRunning = true;
  SimState.di.INHIBIT_FOAM_REL = false;
  SimState.di.INHIBIT_ALL_OUTPUTS = false;
  SimState.di.Pump_B_Inhibited = false;
  pressSystemReset();
  renderFaceplate();
  renderFGDetectorTable();
}

// Web Audio API Synthesizer for realistic acoustic sirens/horns
let audioCtx = null;
let audioOsc = null;
let audioGain = null;

function toggleAudio() {
  SimState.audioEnabled = !SimState.audioEnabled;
  const b = document.getElementById('btn-audio-toggle');
  b.innerHTML = SimState.audioEnabled ? '&#128266; AUDIO: ON' : '&#128266; AUDIO: OFF';
  b.classList.toggle('active', SimState.audioEnabled);
  if (SimState.audioEnabled && !audioCtx) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    audioOsc = audioCtx.createOscillator();
    audioGain = audioCtx.createGain();
    audioOsc.type = 'sawtooth';
    audioOsc.frequency.value = 680;
    audioGain.gain.value = 0;
    audioOsc.connect(audioGain);
    audioGain.connect(audioCtx.destination);
    audioOsc.start();
  }
  if (!SimState.audioEnabled && audioGain) {
    audioGain.gain.value = 0;
  }
}

function stepWebAudio() {
  if (!SimState.audioEnabled || !audioGain) return;
  const sO = SimState.plc.slotO[8];
  const anyHorn = sO[2] || sO[22] || sO[23] || sO[30] || sO[31];
  if (anyHorn) {
    audioOsc.frequency.value = sO[30] ? 880 : (sO[2] ? 740 : 580);
    audioGain.gain.value = 0.04;
  } else {
    audioGain.gain.value = 0.0;
  }
}

function switchTab(tabId, btnEl) {
  document.querySelectorAll('.view-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-tab').forEach(b => b.classList.remove('active'));
  document.getElementById(tabId)?.classList.add('active');
  if (btnEl) btnEl.classList.add('active');
  refreshActiveTabUI();
}

function refreshActiveTabUI() {
  const activeId = document.querySelector('.view-panel.active')?.id;
  if (activeId === 'tab-pid') updatePIDSVG();
  else if (activeId === 'tab-fgmap') {
    drawFGPlumeCanvas();
    SimState.detectors.forEach((d, idx) => {
      const cell = document.getElementById(`fg-tbl-val-${idx}`);
      if (cell) cell.textContent = `${d.val.toFixed(1)} ${d.unit}`;
    });
  } else if (activeId === 'tab-fgcp') renderFGCPPanel();
  else if (activeId === 'tab-ce') renderCEMatrix();
  else if (activeId === 'tab-plc') {
    renderRackInspector();
    renderSTDebugger();
  } else if (activeId === 'tab-trends') {
    drawTrendCanvas();
    renderSOELog();
  }
}

// ============================================================================
// 13. MASTER REAL-TIME SIMULATION LOOP (20 Hz / 50 ms SCAN CYCLE)
// ============================================================================
function initSimulator() {
  buildPIDSVG();
  initSTSelector();
  initFGCanvasEvents();
  stepPhysicalTwin(0.05);
  stepSoftPLC(50);
  renderFaceplate();
  renderFGDetectorTable();
  renderFGCPPanel();
  renderCEMatrix();
  renderRackInspector();
  renderSTDebugger();
  renderScenariosView();
  logSOE('SYSTEM_BOOT', '1756-L82E', 'ControlLogix 5580 Soft-PLC & Quinguila Physical Twin Initialized (25 ST Routines Active)', 'INFO');

  let uiTick = 0;
  setInterval(() => {
    if (!SimState.running) return;
    const dtSec = 0.05 * SimState.speed;
    const dtMs  = 50.0 * SimState.speed;
    SimState.simTimeSec += dtSec;
    SimState.scanCount++;

    stepPhysicalTwin(dtSec);
    stepSoftPLC(dtMs);
    syncAlarms();
    stepWebAudio();
    updateHeaderAndQuickStrip();

    uiTick++;
    if (uiTick % 2 === 0) {
      refreshActiveTabUI();
      renderAlarmBanner();
    }
    if (uiTick % 5 === 0) {
      const maxCH4 = Math.max(...SimState.detectors.filter(d=>d.type==='CH4'||d.type==='CH4_GEN').map(d=>d.val));
      const maxH2S = Math.max(...SimState.detectors.filter(d=>d.type==='H2S').map(d=>d.val));
      SimState.trendHistory.push({
        t: SimState.simTimeSec,
        pit3: SimState.phys.oilManifoldPsi,
        pit2: SimState.phys.waterManifoldPsi,
        fg:   SimState.phys.fuelGasLinePsi,
        ft:   SimState.phys.oilExpFlowBblH,
        ch4:  maxCH4,
        h2s:  maxH2S
      });
      if (SimState.trendHistory.length > 240) SimState.trendHistory.shift();
    }
  }, 50);
}

window.addEventListener('DOMContentLoaded', initSimulator);
</script>
</body>
</html>
"""

def build_all():
    js1 = JS_ENGINE_PART1.replace("__ST_ROUTINES_JSON__", json.dumps(ST_ROUTINES))
    js1 = js1.replace("__ROUTINE_ORDER_JSON__", json.dumps(ROUTINE_ORDER))

    full_html = (
        HTML_TEMPLATE_PART1 +
        HTML_TEMPLATE_PART2 +
        js1 +
        JS_ENGINE_PART2 +
        JS_ENGINE_PART3 +
        JS_ENGINE_PART4 +
        JS_ENGINE_PART5 +
        JS_ENGINE_PART6
    )

    for out_p in OUT_PATHS:
        os.makedirs(os.path.dirname(out_p), exist_ok=True)
        with open(out_p, "w", encoding="utf-8") as f:
            f.write(full_html)
        print(f"Wrote {out_p} ({len(full_html):,} bytes)")

if __name__ == "__main__":
    build_all()
