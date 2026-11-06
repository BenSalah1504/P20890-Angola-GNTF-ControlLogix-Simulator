# GNTF Quinguila Tank Farm — ControlLogix 5580 (`1756-L82E`) ST & Ladder Migration & Physical Twin Simulator

[![PLC Platform](https://img.shields.io/badge/PLC-Allen--Bradley%201756--L82E%20(v32)-blue)](#controllogix-1756-a13-hardware-architecture)
[![Ladder Diagram](https://img.shields.io/badge/Rockwell%20RLL-Ladder%20Diagram%20(432%20Rungs)-orange)](#allen-bradley-relay-ladder-logic-rll--l5x-viewer)
[![Language](https://img.shields.io/badge/IEC%2061131--3-Structured%20Text%20(25%20Routines)-00d4ff)](#structured-text-routine-architecture)
[![Legacy PLC](https://img.shields.io/badge/Legacy-GE%20VersaMax%20(P20890__Angola)-f59e0b)](#repository-deliverables)
[![Simulator](https://img.shields.io/badge/Digital%20Twin-HTML5%20Physical%20Twin%20%2B%20Soft--PLC-22c55e)](#physical-twin--soft-plc-web-simulator)

Complete PLC migration, documentation suite, and real-time **Physical Twin + ControlLogix 5580 Soft-PLC Web Simulator** for the **Quinguila Tank Farm (`GNTF`) Control System Upgrade** (`FGCP-7404-001` / `P20890_Angola`).

This project decodes the legacy **GE Fanuc Proficy Machine Edition 7.00 (`VersaMax`)** ladder logic program, translates and upgrades it into **both**:
1. **Allen-Bradley Relay Ladder Logic (RLL)** `.L5X` file (`Type="RLL"`, 432 rungs, 25 routines) viewable in any standard L5X Viewer or Rockwell Studio 5000 Logix Designer.
2. **Allen-Bradley Structured Text (ST)** `.L5X` file (`Type="ST"`) and individual `.st` routines.
3. A standalone, zero-dependency **Physical Twin Web Application** for Factory Acceptance Testing (FAT), Site Acceptance Testing (SAT), and operator training.

---

## Repository Deliverables

| File / Directory | Description |
| :--- | :--- |
| **[`P20890_Angola_AB_Ladder.L5X`](./P20890_Angola_AB_Ladder.L5X)** | **Studio 5000 Full Controller Project (`.L5X`)** (`TargetType="Controller"`). Opens directly via `File` &rarr; `Open` in Studio 5000 to reconstruct the complete ControlLogix 5580 `1756-L82E` chassis, hardware modules, 683 tags (with `<Data Format="Decorated">`), and all 25 RLL routines (432 rungs). |
| **[`P20890_Angola_AB_Program_Ladder.L5X`](./P20890_Angola_AB_Program_Ladder.L5X)** | **Studio 5000 Importable Program (`.L5X`)** (`TargetType="Program"`). Designed for right-clicking any Task/Program in an existing Studio 5000 project and selecting **"Import Program..."** to import all 25 routines directly without hardware reconfiguration. |
| **[`P20890_Angola_AB_Ladder.html`](./P20890_Angola_AB_Ladder.html)** | **Interactive Allen-Bradley Ladder Diagram Viewer** (Standalone HTML/SVG app with dual power rails, graphical contact/coil/block symbols, parallel branch rendering, real-time tag cross-reference inspector, search, and print stylesheet). |
| **[`GNTF_Physical_Twin_Simulator.html`](./GNTF_Physical_Twin_Simulator.html)** / **[`index.html`](./index.html)** | **Interactive Physical Twin & ControlLogix 5580 Soft-PLC Web App** (7 SCADA/Twin views, 2D Gaussian gas/fire plume dispersion, ODE fluid/tank/manifold physics, FGCP hardware mimic, live Cause & Effect verifier, Studio 5000 online ST debugger, and 9 automated FAT/SAT scenarios). |
| **[`P20890_Angola_AB_ST.L5X`](./P20890_Angola_AB_ST.L5X)** | **Studio 5000 Logix Designer Structured Text Project (`.L5X`)** (`Type="ST"`) for `1756-L82E` (v32) in a 13-slot `1756-A13` chassis with all 683 tags and 25 routines. |
| **[`P20890_Angola_AB_Complete.st`](./P20890_Angola_AB_Complete.st)** | Combined Allen-Bradley Structured Text source code for all 25 routines. |
| **[`ab_st_routines/`](./ab_st_routines/)** | Individual `.st` files for all 25 Structured Text routines (`MainRoutine.st` through `Output.st`). |
| **[`P20890_Angola_AB_Tags.csv`](./P20890_Angola_AB_Tags.csv)** | Studio 5000 Tag Database CSV export containing all 683 controller tags, hardware aliases, timer/counter structures, and engineering descriptions. |
| **[`P20890_Angola_AB_ST.pdf`](./P20890_Angola_AB_ST.pdf)** | **46-Page Printable A4-Landscape Engineering Report** containing the `1756-A13` rack architecture, complete I/O & terminal block cross-reference (`TB-02`..`TB-08`), setpoints, and formatted ST code. |
| **[`P20890_Angola_AB_ST.html`](./P20890_Angola_AB_ST.html)** | Interactive dark-mode Structured Text code viewer & I/O cross-reference browser with one-click copy. |
| **[`P20890_Angola_Ladder.pdf`](./P20890_Angola_Ladder.pdf)** | **34-Page Printable A4-Landscape Ladder Diagram Export** decoded directly from the legacy GE Proficy Machine Edition `.SwxCF` binaries (226 rungs across 24 blocks). |
| **[`P20890_Angola_Ladder.html`](./P20890_Angola_Ladder.html)** | Interactive vector SVG Ladder Diagram viewer for the legacy GE VersaMax program. |
| **[`generate_ab_ladder.py`](./generate_ab_ladder.py)** / **[`generate_ladder_backend.py`](./generate_ladder_backend.py)** | Python generator for the Rockwell Relay Ladder Logic (RLL) `.L5X` and interactive SVG/HTML ladder viewer. |
| **[`build_physical_twin.py`](./build_physical_twin.py)** | Python build script that compiles the Physical Twin & Soft-PLC Web Simulator (`GNTF_Physical_Twin_Simulator.html`). |
| **[`generate_ab_st.py`](./generate_ab_st.py)** | Python generator for the Studio 5000 `.L5X`, `.st` routines, `.csv` tag database, `.pdf`, and `.html` reports. |
| **[`pme_parse.py`](./pme_parse.py)** / **[`export_ladder.py`](./export_ladder.py)** / **[`export_pdf.py`](./export_pdf.py)** | Binary decoders and vector PDF/HTML exporters for GE Proficy Machine Edition `.SwxCF` archives without requiring PME installation or administrator privileges. |

---

## Allen-Bradley Relay Ladder Logic (RLL) & L5X Viewer

For engineers and technicians who require **Ladder Diagram (LD / RLL)** viewing rather than Structured Text, the complete project is exported in official Rockwell Automation **`Type="RLL"`** XML format inside **[`P20890_Angola_AB_Ladder.L5X`](./P20890_Angola_AB_Ladder.L5X)**.

### Viewing Options:
1. **With an L5X Viewer / Studio 5000 Logix Designer**:
   - Open **`P20890_Angola_AB_Ladder.L5X`** in your preferred L5X Viewer or Studio 5000 Logix Designer (`File` &rarr; `Open` / `Import Component`).
   - Every routine is structured with `<Routine Name="..." Type="RLL"><RLLContent><Rung Number="x" Type="N">` so viewers render pure graphical ladder rungs with power rails, contacts, coils, and blocks.
2. **With the Included Web Ladder Viewer (`P20890_Angola_AB_Ladder.html`)**:
   - Double-click **`P20890_Angola_AB_Ladder.html`** in any web browser.
   - Features:
     - Full graphical electrical rails (`L1 +24VDC` and `0VDC Neutral Return`).
     - Standard graphical symbols: `XIC` (`--[ ]--`), `XIO` (`--[/]--`), `OTE` (`--( )--`), `OTL` (`--(L)--`), `OTU` (`--(U)--`).
     - Function blocks: `TON` (Timer On Delay), `CPT` (Compute Expression), `MOV` (Move), `GRT`/`LES`/`LIM` (Comparisons), `JSR` (Jump to Subroutine).
     - Parallel branch rendering with electrical split and merge bars.
     - Interactive **Tag Cross-Reference Inspector**: click any tag to view its Data Type, Hardware Alias (e.g. `Local:7:I.Data.0`), Terminal Number, Description, and list of all logic rungs where it is read or written.
     - Real-time search by tag name, instruction, or rung comment.

### Summary of RLL Routines & Rungs (432 Total Rungs):

| Routine | Rungs | Function | Key Instructions Used |
| :--- | :---: | :--- | :--- |
| **`MainRoutine`** | 12 | Executive Cycle, Timers & JSR Scheduler | `XIO`, `TON`, `OTE`, `JSR` |
| **`Init`** | 23 | Sensor Engineering Scaling & Limits Initialization | `MOV` (0.0, 100.0, 105.0, -4.0, 30.0, 20.0, etc.) |
| **`Input`** | 47 | Slot 2, 3, 4, 6, 7 Hardware Input Image Mapping | `XIC`, `OTE`, `MOV`, `CPT` |
| **`DI_1`** | 17 | ESD Valve Discrepancy & Transit Timers | `XIC`, `XIO`, `OTE`, `TON` |
| **`DI_2`** | 27 | Deluge Pump Pulse Supervision & E-Stops | `XIO`, `TON`, `XIC`, `OTE` |
| **`CalcVa1`** | 8 | Analog Channels 1..8 %LEL Engineering Scaling | `CPT` (`((Span-Zero)/32000.0)*Raw + Zero`) |
| **`AI_1`** | 25 | Channels 1..8 Beam Block & Fault Detection | `JSR`, `GRT`, `LES`, `LIM`, `OTE` |
| **`CalcVa2`** | 8 | Analog Channels 9..16 %LEL Engineering Scaling | `CPT` |
| **`AI_2`** | 26 | Channels 9..16 Sensor Faults & Beam Block | `JSR`, `GRT`, `LES`, `LIM`, `OTE` |
| **`CalcVa3`** | 8 | Analog Channels 17..24 Scaling | `CPT` |
| **`AI_3`** | 25 | Channels 17..24 Faults & Out-of-Range Monitoring | `JSR`, `GRT`, `LES`, `LIM`, `OTE` |
| **`AI_4_New`** | 34 | New Phase 1 4-20mA Transmitter Scalers (H2S, Flame, Pressure) | `CPT`, `GRT`, `OTE` |
| **`Ai_AL_1`** | 32 | Combustible Gas High-High (30%) & High (20%) Alarms | `GEQ`, `OTE` |
| **`Ai_AL_2`** | 26 | Gas Channels 9..16 High & High-High Alarms | `GEQ`, `OTE` |
| **`Ai_AL_3`** | 12 | Gas Channels 17..24 High & High-High Alarms | `GEQ`, `OTE` |
| **`Vote_1`** | 14 | 2ooN Gas Detector Voting & Deluge Interlocks | `XIC`, `OTE` (Combinatorial 2ooN branches) |
| **`Logic`** | 7 | Firewater Pump Auto-Start Demand & ESD Cascades | `XIC`, `XIO`, `OTE`, `TON` |
| **`CE_LOG`** | 5 | Master Cause & Effect Matrix Shutdown Logic | `XIC`, `OTE` (Multi-branch Matrix) |
| **`Indicat`** | 10 | Panel LED Flashers & Beacon Driver Logic | `XIC`, `OTE` |
| **`Shutdow`** | 6 | Master Plant ESD, Generator & Pump Trip Outputs | `XIC`, `OTE` |
| **`Protect`** | 2 | Deluge & ESD Override / Bypass Inhibit Logic | `XIC`, `OTE` |
| **`Loc_Al`** | 9 | Local Annunciator Horns & Rotating Beacons | `XIC`, `OTE` |
| **`FLT_1`** | 2 | Common System & Hardware Diagnostic Summary | `XIC`, `OTE` |
| **`Sound`** | 1 | Master Alarm Acoustic Horn Silence & Acknowledge | `XIC`, `XIO`, `OTE` |
| **`Output`** | 26 | Slot 8 1756-OB32 Hardware Output Driver Mapping | `XIC`, `OTE` (Local:8:O.Data.x) |

---

## ControlLogix `1756-A13` Hardware Architecture

Per engineering documents **`01-MAN-03-11-PDF-C3A`** (System Architecture), **`01-MAN-03-06-PDF-C2C Final`** (I/O List), and **`01-MAN-02-13-PDF-C1A`** (Terminal Block Connection Diagrams):

```mermaid
flowchart LR
  subgraph Rack["1756-A13 Chassis (13 Slots) + 1756-PB72 PSU"]
    S0["Slot 0: 1756-L82E\nControlLogix 5580 CPU\n192.168.20.10/24"]
    S1["Slot 1: 1756-N2\nSlot Filler"]
    S2["Slot 2: 1756-IF16 (TB-02)\n7404-DG-001..012 (CH4)\n7404-DG-011R (Open Path)\nGD-001..003 (Gas Gen CH4)"]
    S3["Slot 3: 1756-IF16 (TB-03)\nPIT-001..003 Manifolds\n7503/7002/6401-PST-001\n7503-FR-001..003 Foam MACs"]
    S4["Slot 4: 1756-IF16 (TB-04)\nH2S-001..012 (0-100 PPM)\n7404-DF-001..003 (Flame)\nSD-001/002 (Smoke)"]
    S5["Slot 5: 1756-IF16 (TB-05)\n16x Wired Spare AI"]
    S6["Slot 6: 1756-IF8H (TB-06)\nHART Radar Level Transmitters\nLIT-100, 200, 300, 400"]
    S7["Slot 7: 1756-IB32 (TB-07)\n21x Digital Inputs\nZSH/ZSL, LS, FS, S2/S3, E1..E12"]
    S8["Slot 8: 1756-OB32 (TB-08)\n26x Digital Outputs\nESD, EY, Pump A/B, CR1..6, Horns"]
    S9["Slot 9: MVI56E-MCM\nModbus RS-485 Master/Slave\nP-2300..2600, P-3800..3900\n6401-FT-001, V-710, V-810"]
  end
  S0 --- S2 & S3 & S4 & S5 & S6 & S7 & S8 & S9
```

| Slot | Module | Terminal Block | Assigned Instruments & Signals |
| :--- | :--- | :--- | :--- |
| **Slot 0** | `1756-L82E` | Ethernet | ControlLogix 5580 Controller (`192.168.20.10`) |
| **Slot 1** | `1756-N2` | — | Empty Slot Filler |
| **Slot 2** | `1756-IF16` | `TB-02` | `Ch0..11`: **CH4 Point Gas Detectors** `7404-DG-001..012` (0–100 %LEL, Low=20%, High=30%)<br>`Ch12`: **Open-Path IR Detector** `7404-DG-011R` (0–5.00 LELm, Low=1.00, High=3.00, Optic Fault `-0.78125`..`-0.46875` LELm)<br>`Ch13..15`: **Gas Generator Room CH4 Detectors** `GD-001..003` (0–100 %LEL, Low=20%, High=30% -> `SD-GE`) |
| **Slot 3** | `1756-IF16` | `TB-03` | `Ch0`: `PIT-001` Oil Expedition (0–200 Psi, PAL=10, PAH=100)<br>`Ch1`: `PIT-002` Water Injection Manifold (0–1500 Psi, PAL=200, PAH=800, PAHH=900 -> trips `P-3800/3900` & `P-3600/3700`)<br>`Ch2`: `PIT-003` Power Oil Manifold (0–3000 Psi, PAL=1700, PAH=2700, PAHH=2800 -> trips `P-2300..2600` & `P-2100/2200`)<br>`Ch3`: `7503-PST-001` Deluge Line Pressure (0–100 Psi, PAH=50 -> Foam Released)<br>`Ch4`: `7002-PST-001` Air Accumulator ESDV (0–100 Psi, PAL=50 -> `L16`)<br>`Ch5`: `6401-PST-001` Fuel Gas Line (0–150 Psi, PAL=40 -> `L17`, PAH=100 -> Station ESD)<br>`Ch6..7`: Manual Foam Release Call Points `7503-FR-003` (Inside PCR) & `7503-FR-001/002` (Outside Bund) |
| **Slot 4** | `1756-IF16` | `TB-04` | `Ch0..11`: **H2S Gas Detectors** `H2S-001..012` (0–100 PPM, Low=10 PPM Discontinuous `H2SA-001/002`, High=20 PPM Continuous)<br>`Ch12..14`: **Flame Detectors** `7404-DF-001..003` (0–100%, Alarm=30%)<br>`Ch15`: **Smoke Detectors** `SD-001/002` (0–100%, Alarm=30% -> `SD-GE` & `SDA-001`) |
| **Slot 5** | `1756-IF16` | `TB-05` | `Ch0..15`: 16x Wired Spare 4–20 mA Analog Inputs |
| **Slot 6** | `1756-IF8H` | `TB-06` | `Ch0..2`: **Tank Radar Level Transmitters** `LIT-100`, `LIT-200`, `LIT-300` (0–10.0 m, LAL=0.7 m, LAH=9.0 m)<br>`Ch3`: **Tank Radar Level Transmitter** `LIT-400` (0–12.0 m, LAL=0.7 m, LAH=11.0 m) |
| **Slot 7** | `1756-IB32` | `TB-07` | `Pt0..20`: `6401-ZSH-001` (Open), `6401-ZSL-001` (Closed), `FS_FGCP_E8` (Panel Foam Stop), `7503-LS-002` (Diesel Low), `7503-FS-001` (Field Foam Stop), `7503-LS-001` (Foam Low), `75-C-01A/B` (Pump A/B Line Check), `75-SB-01B` (Pump B Inhibit), `Reset_PB_E11`, `Mute_PB_E12`, `6401-ESDV-001` (`E9`), `INHIBIT_FOAM_REL` (`S2`), `INHIBIT_ALL_OUTPUTS` (`S3`), `7404-SB-004..009` (`E1..E6` Pump E-Stops) |
| **Slot 8** | `1756-OB32` | `TB-08` | `Pt0..31`: `PumpShutdown` (`ESD_TRIP`), `6401-EY-001/002`, `7404-SA-001/002`, `Pump_A_PulsOut`, `PUMP_A`, `Pump_B_Start_PulsOut`, `PUMP_B_START`, `PUMP_B_STOP`, `P2100_P2200`, `P3600_P3700`, `PLC_Fault`, `L14..L17` LEDs, `CR1..CR6` Pump Trip Relays (`L8..L13`), `SD_GE`, `Z1` PCR Horn, `PA_001`, `H2SA_001_002`, `SDA_001` |
| **Slot 9** | `MVI56E-MCM` | RS-485 | Modbus Master/Slave to Power Oil Pumps (`P-2300..2500` TTD-H, `P-2600` S1501), Water Injection Pumps (`P-3800..3900` TTD-H), Expedition Flowmeter `6401-FT-001` (0–500 bbl/h, FAL=30, FAH=300), and Heater Treaters (`V-710`, `V-810`) |

---

## Structured Text Routine Architecture

All 25 Structured Text routines inside `MainProgram` (in [`ab_st_routines/`](./ab_st_routines/)):

1. **`MainRoutine.st`**: Executive scheduler, first-scan initialization, 400 ms flasher oscillator (`R01598_0`), and `JSR` calls.
2. **`Init.st`**: Calibration zero/span ranges and alarm thresholds per `01-MAN-03-13-PDF-C1`.
3. **`Input.st`**: Hardware input mapping from `Local:2:I`..`Local:9:I` to internal tag registers.
4. **`DI_1.st`**: ESDV limit switch discrepancy timers (`10.0s`), Foam Stop pushbuttons, and Foam/Diesel tank low-level switches.
5. **`DI_2.st`**: 60-second pulsed open-circuit continuity monitoring for Deluge Pumps A & B, Keyswitches `S2`/`S3`, `E9` ESD button, and `E1..E6` Pump E-Stops.
6. **`AI_1.st` & `CalcVa1.st`**: Linear engineering unit scaling (`0–32000` raw counts) and wire-break/overrange fault detection for `7404-DG-001..008`.
7. **`AI_2.st` & `CalcVa2.st`**: Scaling and fault detection for `7404-DG-009..012`, `7404-DF-001..002`, and Open-Path `7404-DG-011R` (including `-0.78125` to `-0.46875 LELm` optical beam block window).
8. **`AI_3.st` & `CalcVa3.st`**: Scaling and fault detection for `7002-PST-001`, `6401-PST-001`, `7503-PST-001`, and Foam Call Points `7503-FR-001..003`.
9. **`AI_4_New.st`**: GNTF Upgrade scaling and alarm latches for `GD-001..003`, `PIT-001..003` (`PAL`/`PAH`/`PAHH`), `H2S-001..012`, `7404-DF-003`, `SD-001/002`, `LIT-100..400`, and `6401-FT-001`.
10. **`Ai_AL_1.st`, `Ai_AL_2.st`, `Ai_AL_3.st`**: Latched Low/High alarm evaluation with `M00002_System_Reset` release.
11. **`Vote_1.st`**: `1ooN` and `2ooN` voting across CH4 gas detectors (`R01500_0..3`) and flame detectors (`R01501_0..1`).
12. **`Logic.st`**: Firewater/Foam Deluge duty `PUMP_A` control, 10-second pressure proving timer (`TMR_PumpA_FailToRun` for `7503-PST-001 >= 50 Psi`), and automatic 3-attempt crank start sequence for standby diesel `PUMP_B`.
13. **`CE_LOG.st`, `Indicat.st`, `Shutdow.st`, `Protect.st`, `Loc_Al.st`, `FLT_1.st`, `Sound.st`, `Output.st`**: Complete Cause & Effect Matrix (`01-MAN-03-07-PDF-C2C Final`) driving fail-safe ESD outputs, individual pump trip relays `CR1..CR6`, `SD-GE`, discontinuous (1 Hz) vs. continuous horns/beacons, and `Local:8:O.Data.0..31`.

---

## Physical Twin & Soft-PLC Web Simulator

Open **[`GNTF_Physical_Twin_Simulator.html`](./GNTF_Physical_Twin_Simulator.html)** directly in any modern browser (Chrome, Edge, Firefox) — no server or installation needed:

- **Tab 1 — `P&ID PROCESS TWIN`**: Interactive animated P&ID of the Quinguila Tank Farm with coupled ODE fluid/pressure dynamics and equipment faceplates.
- **Tab 2 — `2D F&G PLUME MAP`**: Site layout with real-time 2D Gaussian plume advection (click map to inject CH4, H2S, Pool Fire, or Smoke with wind speed/direction sliders) + individual channel overrides and fault injection.
- **Tab 3 — `FGCP-7404-001 PANEL`**: Interactive hardware annunciator panel with `L8..L17` lamps, `S2`/`S3` keyswitches, `E1..E6`/`E9` E-Stops, `E8` Foam Stop, `E11` Reset, `E12` Mute, and optional Web Audio horn synthesizer.
- **Tab 4 — `LIVE C&E MATRIX`**: Real-time Cause & Effect intersection table with one-click test triggers for all 24 Cause rows.
- **Tab 5 — `1756 RACK & ST DEBUGGER`**: Live `1756-A13` slot/channel inspector (`4–20 mA` currents, raw counts, DI/DO states) and Studio 5000 Online ST Code Monitor.
- **Tab 6 — `FAT / SAT SCENARIOS`**: 9 automated Factory/Site Acceptance Test sequences (`FAT-01` through `FAT-09`).
- **Tab 7 — `TRENDS & HISTORIAN`**: High-speed 6-pen strip chart recorder and ISA-18.2 Sequence of Events (SOE) historian with CSV export.

---

## Importing into Studio 5000 Logix Designer

1. Launch **Studio 5000 Logix Designer** (v28 or v32+).
2. Click **File -> Open** and select **[`P20890_Angola_AB_ST.L5X`](./P20890_Angola_AB_ST.L5X)**.
3. Specify the target `.ACD` filename (`P20890_Angola_AB_ST.ACD`) and click **Import**.
4. Verify the 13-slot `1756-A13` I/O Configuration tree, Controller Tags (683 tags), and `MainProgram` (25 ST routines).
