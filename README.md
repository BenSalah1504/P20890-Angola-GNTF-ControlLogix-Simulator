# GNTF Quinguila Tank Farm — ControlLogix 5580 (`1756-L82E`) Upgraded Project, Complete HMI Suite & Legacy Migration

[![PLC Platform](https://img.shields.io/badge/PLC-Allen--Bradley%201756--L82E%20(v32)-blue)](#controllogix-1756-a13-hardware-architecture)
[![Upgraded Project](https://img.shields.io/badge/Upgraded%20Project-01--MAN--03--06%20%26%2007%20Final-emerald)](#1-upgraded-controllogix-5580-project-phase-1--2-approved-architecture)
[![Complete HMI Suite](https://img.shields.io/badge/HMI%20Suite-FactoryTalk%20%2B%20Web%20SCADA-purple)](#2-complete-hmi--scada-workstation-suite)
[![Rockwell RLL](https://img.shields.io/badge/Rockwell%20RLL-Type%3D%22RLL%22%20(L5X)-orange)](#1-upgraded-controllogix-5580-project-phase-1--2-approved-architecture)
[![Digital Twin](https://img.shields.io/badge/Digital%20Twin-HTML5%20Physical%20Twin%20%2B%20Soft--PLC-22c55e)](#3-interactive-physical-twin--soft-plc-simulator)

Complete industrial automation project suite for the **Quinguila Tank Farm (`GNTF`) Control System Upgrade** (`FGCP-7404-001`).

This repository contains:
1. **The Complete Upgraded Project Suite (Phase 1 & Phase 2 Upgrades)**: Fully engineered to the final EPPM / ASTRE approved deliverables (**`01-MAN-03-06-PDF-C2C Final`** I/O List, **`01-MAN-03-07-PDF-C2C Final`** Cause & Effect Matrix, **`01-MAN-03-08-PDF-C1A`** Functional Description, and **`01-MAN-03-11-PDF-C3A`** System Architecture). Features symbolic tag naming, 15 modernized RLL routines, and a full **HMI / SCADA Suite**.
2. **The Complete HMI / SCADA Workstation Suite**: Interactive standalone HTML5 SCADA workstation (`GNTF_HMI_Application.html`) with 7 graphic screens, plus official Rockwell **FactoryTalk View Studio SE/ME** tag database (`.csv`) and alarms definition (`.xml`).
3. **The Legacy GE VersaMax Migration Suite**: 1:1 decoded and converted relay ladder logic (`P20890_Angola_AB_Ladder.L5X`) and structured text (`P20890_Angola_AB_ST.L5X`) for historical verification.

---

## Complete Project Deliverables Directory

### 1. Upgraded ControlLogix 5580 Project (Phase 1 & 2 Approved Architecture)

| Deliverable | Description |
| :--- | :--- |
| **[`GNTF_Quinguila_Upgrade_AB_Ladder.L5X`](./GNTF_Quinguila_Upgrade_AB_Ladder.L5X)** | **Studio 5000 Controller L5X Project File (`TargetType="Controller"`)**. Reconstructs the complete upgraded ControlLogix 5580 `1756-L82E` chassis (`1756-A13`), 8 I/O modules, 469 upgraded engineering tags (with `<Data Format="Decorated">`), and 15 modernized Relay Ladder Logic routines (213 rungs) implementing the approved Cause & Effect matrix. |
| **[`GNTF_Quinguila_Upgrade_AB_Program.L5X`](./GNTF_Quinguila_Upgrade_AB_Program.L5X)** | **Studio 5000 Program L5X Import File (`TargetType="Program"`)**. Designed for right-clicking any Task/Program in an existing Studio 5000 project and clicking **"Import Program..."** to import all 15 routines and tags directly into any chassis without hardware conflicts. |
| **[`GNTF_Quinguila_Upgrade_AB_Ladder.html`](./GNTF_Quinguila_Upgrade_AB_Ladder.html)** | **Interactive Web Ladder Diagram Viewer (Upgraded Project)**. Graphical viewer rendering electrical power rails (`L1` / `0V`), contacts, coils, timer blocks, parallel branches, real-time search, and interactive tag cross-reference inspector. |
| **[`build_upgraded_suite.py`](./build_upgraded_suite.py)** | Python generator script that compiles the upgraded controller project, program import, and HMI files. |

---

### 2. Complete HMI & SCADA Workstation Suite

| Deliverable | Description |
| :--- | :--- |
| **[`GNTF_HMI_Application.html`](./GNTF_HMI_Application.html)** | **Full Interactive Web HMI / SCADA Workstation Application**. Professional standalone industrial SCADA client featuring **7 dynamic graphic screens** (Plant Overview Mimic, Fire & Gas 2ooN Matrix, Deluge & Firewater Skid, Pressures & Tank Farm, Cause & Effect Live Matrix, PCR Panel LCP Door Mimic, and Alarms & Events Chronology) with interactive test controls! |
| **[`GNTF_HMI_Tags_FactoryTalk.csv`](./GNTF_HMI_Tags_FactoryTalk.csv)** | **Rockwell FactoryTalk View Studio Tag Database Import CSV**. Ready for direct import into FactoryTalk View Site Edition (SE) or Machine Edition (ME) tag database (`Tag Name`, `Tag Type`, `Data Type`, `[PLC]Address`, `Min`, `Max`, `Description`, `Engineering Units`). |
| **[`GNTF_HMI_Alarms_FactoryTalk.xml`](./GNTF_HMI_Alarms_FactoryTalk.xml)** | **Rockwell FactoryTalk View Alarms and Events (FTA&E) Import XML**. Official alarm definition database with High-High, High, Low, Low-Low, and Digital trip alarms per document `01-MAN-03-13-PDF-C2C Final`. |
| **[`GNTF_Physical_Twin_Simulator.html`](./GNTF_Physical_Twin_Simulator.html)** / **[`index.html`](./index.html)** | **Interactive Physical Twin & ControlLogix 5580 Soft-PLC Web App** (Gaussian gas dispersion physics, ODE fluid/tank dynamics, live C&E verifier, Studio 5000 online ST debugger). |

---

### 3. Legacy GE VersaMax Migration Deliverables (For Reference)

| Deliverable | Description |
| :--- | :--- |
| **[`P20890_Angola_AB_Ladder.L5X`](./P20890_Angola_AB_Ladder.L5X)** | Legacy project converted to Studio 5000 Controller L5X (`Type="RLL"`, 432 rungs, 25 routines, 683 tags). |
| **[`P20890_Angola_AB_Program_Ladder.L5X`](./P20890_Angola_AB_Program_Ladder.L5X)** | Legacy project converted to Studio 5000 Program L5X (`TargetType="Program"`). |
| **[`P20890_Angola_AB_Ladder.html`](./P20890_Angola_AB_Ladder.html)** | Interactive Web Ladder Diagram Viewer for legacy converted routines. |
| **[`P20890_Angola_AB_ST.L5X`](./P20890_Angola_AB_ST.L5X)** | Studio 5000 Structured Text project (`Type="ST"`). |
| **[`P20890_Angola_AB_ST.pdf`](./P20890_Angola_AB_ST.pdf)** | 46-Page Printable Engineering Report. |
| **[`P20890_Angola_Ladder.pdf`](./P20890_Angola_Ladder.pdf)** | 34-Page Printable GE VersaMax decoded ladder report. |

---

## Upgraded ControlLogix 5580 Architecture & Routine Breakdown

Per approved engineering documents **`01-MAN-03-06-PDF-C2C Final`** and **`01-MAN-03-07-PDF-C2C Final`**:

| Routine | Functionality & Control Philosophy | Key Inputs / Outputs |
| :--- | :--- | :--- |
| **`Main_Scheduler`** | Executive scheduler, 400ms slow flasher, 200ms fast flasher, first-scan init, watchdog. | `TMR_Flash_Slow`, `TMR_Flash_Fast`, `S:FS` |
| **`Init_Setpoints`** | Calibrated setpoint loading: 20% / 30% LEL, 10 / 20 ppm H2S, 1700/2700/2800 psi oil inj, 200/800 psi water inj, 40/100 psi fuel gas, 50 psi air acc, 0.7m / 9m / 11m tanks. | `SET_CH4_*`, `SET_H2S_*`, `SET_OilInj_*`, `SET_WaterInj_*` |
| **`IO_Input_Acquisition`** | Slot 2..7 1756 module data acquisition into engineering tags. | `Local:7:I.Data.*`, `Local:x:I.Ch*Data` |
| **`FAG_Combustible_CH4`** | 24 CH4 gas detectors (`7404-DG-001`..`024`): $0-100\% \text{ LEL}$ scaling, Low Alarm ($20\%$), High-High Alarm ($30\%$), Beam Block maintenance flag, low fault ($<-4\%$) and high overrange ($>105\%$). | `DG_7404_001_Scaled`..`024_Scaled` |
| **`FAG_Toxic_H2S`** | 12 Toxic gas transmitters (`H2S-001`..`012`): $0-100\text{ ppm}$ scaling, Low Alarm ($10\text{ ppm}$ - discontinuous alarm), High-High Alarm ($20\text{ ppm}$ - continuous alarm). | `AIT_H2S_001_Scaled`..`012_Scaled` |
| **`FAG_Optical_Flame`** | 3 Triple-IR Optical Flame Detectors (`7404-DF-001`..`003`): instant deluge initiation and ESD trip. | `DF_7404_001_FireAlarm`..`003_FireAlarm` |
| **`FAG_Smoke_Detection`** | Turbine generator room smoke detector (`SD-001/002`): generator trip (`SD_GE`) and dedicated strobe. | `SD_001_002_Alarm`, `SD_GE_GasGenTrip` |
| **`Voting_2ooN_Coincidence`** | 2-out-of-N coincidence voting across Zone 1 (Separator), Zone 2 (Pump House), Zone 3 (Tank Farm), and Zone 4 (Turbines). | `VOTE_Zone1_Gas_Confirmed`..`Zone4_Gas_Confirmed` |
| **`Process_Pressure_Safeguards`** | Oil injection manifold (PAHH 2800 psi), Water injection manifold (PAHH 800 psi), Fuel gas line (PAL 40 psi, PAH 100 psi), ESDV Air Accumulator ($<50\text{ psi}$), Oil expedition (PAL 10 psi, PAH 100 psi). | `PIT_001_OilExped`..`PIT_003_OilInjMan`, `PST_6401_001` |
| **`Process_Tank_Levels`** | Crude storage radar levels (`LIT-100`..`LIT-400`, $0-14\text{ m}$), Low Level ($0.7\text{ m}$), High Level ($9\text{ m}$ / $11\text{ m}$), AFFF foam tank level switch, Diesel fuel level switch. | `LIT_100_Tank_Scaled`..`400_Tank_Scaled` |
| **`Deluge_Firewater_Control`** | Duty Electric Pump A run command, 30-second fail-to-run timer transition to Standby Diesel Pump B, 3-attempt crank cycling, periodic 60s/1.0s line continuity test, manual foam release, foam stop. | `DO_7503_PumpA_Cmd`, `DO_7503_PumpB_Start`, `TMR_PumpA_FailToRun` |
| **`ESD_Cause_Effect_Matrix`** | Approved Cause & Effect Matrix (`01-MAN-03-07-PDF-C2C Final`): Fail-Safe De-energize to Trip for Master ESD (`DO 0`), Fuel Gas ESDV (`DO 1`), Booster Pumps (`DO 8/9`), and Turbines (`DO 21`). | `ESD_TRIP_Master`, `EY_6401_001_002`, `EDB1_OilBoosterStop` |
| **`Inhibit_Maintenance`** | Maintenance bypasses: Keyswitch S2 (Foam Release Inhibit) and Keyswitch S3 (All Outputs Inhibit) with PCR warning indicators. | `KEY_S2_FoamInhibit`, `KEY_S3_AllOutputsInhibit` |
| **`Annunciation_PCR_Panel`** | PCR Cabinet LEDs L8..L17, Main Alarm Horn Z1, Building Siren PA-001, Pump House Bell SA-001/002, H2S Siren/Beacon, Smoke Strobe. | `LED_L14`..`LED_L17`, `CR1`..`CR6`, `HORN_PCR_Z1` |
| **`IO_Output_Dispatch`** | Writing all safe output images to `Local:8:O.Data.0`..`31`. | `Local:8:O.Data.*` |

---

## Complete HMI / SCADA Workstation Features

The standalone **[`GNTF_HMI_Application.html`](./GNTF_HMI_Application.html)** provides a full-featured operator control room environment:
1. **Plant Process Overview Screen**: Real-time animated vector mimic with dynamic flow arrows, live pump rotation status, ESD valve position (Green=Open, Red=Closed), and tank liquid level fills.
2. **Fire & Gas System Screen**: 2D station layout with all 24 CH4 detectors, 12 H2S detectors, 3 Flame detectors, and 2 Smoke detectors, featuring live bargraphs, LEL% readouts, Beam Block badges, and 2ooN voting indicators.
3. **Deluge & Firewater Skid Screen**: Electric Duty Pump A & Diesel Standby Pump B running status, discharge pressure gauge, coil pulse line check, AFFF foam level, start/stop and foam release controls.
4. **Process Pressures & Tank Farm Screen**: Gauges and trends for Oil injection, water injection, fuel gas line, air accumulator, radar levels LIT-100..400.
5. **Cause & Effect Live Matrix Screen**: Dynamic matrix showing real-time states of inputs vs outputs.
6. **PCR / Local Control Panel Mimic (LCP)**: Exact front panel mimic of cabinet `FGCP-7404-001` with LEDs L8..L17, keyswitches S2/S3, pushbuttons, and acoustic silence.
7. **Alarm & Event Management Screen**: Chronological alarm log with timestamp, priority badge, Ack/Reset, and CSV export.
8. **Interactive Live Hardware Simulator**: Slide-out testing drawer allowing operators to inject gas leaks, trigger flame, spike manifold pressure, press E-Stops, test deluge auto-start, and verify plant shutdown cascades live!
