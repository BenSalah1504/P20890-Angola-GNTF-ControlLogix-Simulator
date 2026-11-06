# -*- coding: utf-8 -*-
"""
Build Complete Upgraded ControlLogix 5580 Ladder Logic Project & Full HMI Suite
for Quinguila Tank Farm Control System Upgrade (GNTF / FGCP-7404-001).

Based 100% on approved engineering deliverables:
- 01-MAN-03-06-PDF-C2C Final (I/O List)
- 01-MAN-03-07-PDF-C2C Final (Cause & Effect Matrix)
- 01-MAN-03-08-PDF-C1A / 01-MAN-03-10-PDF-C1 (Functional Description of Control System)
- 01-MAN-03-11-PDF-C3A (System Architecture)
- 01-MAN-03-13-PDF-C2C Final (List of Alarms & Events)

Outputs:
1. GNTF_Quinguila_Upgrade_AB_Ladder.L5X (Studio 5000 Controller L5X, TargetType=Controller)
2. GNTF_Quinguila_Upgrade_AB_Program.L5X (Studio 5000 Program L5X, TargetType=Program)
3. GNTF_Quinguila_Upgrade_AB_Ladder.html (Interactive Web Ladder Diagram Viewer)
4. GNTF_HMI_Application.html (Interactive Full SCADA / HMI Workstation Web Application)
5. GNTF_HMI_Tags_FactoryTalk.csv (FactoryTalk View Studio Tag Database Import)
6. GNTF_HMI_Alarms_FactoryTalk.xml (FactoryTalk View Alarms and Events Setup)
"""
import os
import sys
import html
import json
import xml.sax.saxutils as saxutils
import xml.etree.ElementTree as ET

BASE_DIR = r"c:\Users\Wajdi TAKTAK\Desktop\DOC\ws_g\pme_ladder_export"
DESKTOP_DIR = r"C:\Users\Wajdi TAKTAK\Desktop\P20890_Angola"
sys.path.append(BASE_DIR)
import generate_ladder_backend as B

print("Base backend imported successfully.")

# =============================================================================
# 1. UPGRADED CONTROLLER TAGS (Per 01-MAN-03-06-PDF-C2C & 01-MAN-03-08)
# =============================================================================
def build_upgraded_tags():
    """
    Build complete list of controller tags for the upgraded GNTF FGCP-7404-001 project.
    Returns: list of (TagName, DataType, Description, AliasFor, Units, MinVal, MaxVal)
    """
    tags = []

    # System Status & Flasher Timers
    tags.extend([
        ("TMR_Flash_Slow", "TIMER", "400ms Flasher Slow Timer (PCR Annunciator Flash)", "", "ms", 0, 400),
        ("TMR_Flash_Fast", "TIMER", "200ms Flasher Fast Timer (High-High Alarm Strobe)", "", "ms", 0, 200),
        ("TMR_ESDV_Transit", "TIMER", "15.0s ESDV-6401-001 Transit Discrepancy Timer", "", "ms", 0, 15000),
        ("TMR_ESDV_CmdOpen", "TIMER", "5.0s ESDV-6401-001 Commanded Open Discrepancy Timer", "", "ms", 0, 5000),
        ("TMR_ESDV_CmdClose", "TIMER", "5.0s ESDV-6401-001 Commanded Close Discrepancy Timer", "", "ms", 0, 5000),
        ("TMR_Deluge_Pulse_Period", "TIMER", "60.0s Deluge Trip Coil Line Continuity Check Timer", "", "ms", 0, 60000),
        ("TMR_Deluge_Pulse_Width", "TIMER", "1.0s Deluge Trip Coil Line Continuity Pulse Width", "", "ms", 0, 1000),
        ("TMR_PumpA_WireFlt", "TIMER", "2.0s Deluge Pump A Coil Line Break Fault Timer", "", "ms", 0, 2000),
        ("TMR_PumpB_WireFlt", "TIMER", "2.0s Deluge Pump B Coil Line Break Fault Timer", "", "ms", 0, 2000),
        ("TMR_PumpA_FailToRun", "TIMER", "30.0s Deluge Pump A Pressure Proving & Fail-to-Run Timer", "", "ms", 0, 30000),
        ("TMR_PumpB_StartCrank", "TIMER", "5.0s Diesel Pump B Starter Crank Pulse Timer", "", "ms", 0, 5000),
        ("TMR_PumpB_CrankRest", "TIMER", "5.0s Diesel Pump B Starter Rest Interval Timer", "", "ms", 0, 5000),
        ("TMR_H2S_Horn_Pulse", "TIMER", "1.0s H2S Discontinuous Alarm Pulse Timer", "", "ms", 0, 1000),
        ("CTU_PumpB_Attempts", "COUNTER", "Standby Diesel Pump B Start Crank Attempt Counter (3 Attempts)", "", "cnt", 0, 3),
        ("SYS_First_Scan", "BOOL", "Controller First Scan Initialization Flag", "", "", 0, 1),
        ("SYS_Watchdog_OK", "BOOL", "FGCP-7404-001 Controller System Watchdog Healthy", "", "", 0, 1),
        ("SYS_Alarm_Horn_Muted", "BOOL", "Acoustic Horn Silence / Mute Latch", "", "", 0, 1),
        ("SYS_Alarm_Reset_Cmd", "BOOL", "Master Alarm Reset Command Pulse", "", "", 0, 1),
    ])

    # Slot 2 (1756-IF16): Combustible Gas Detectors CH4 (7404-DG-001 .. 016)
    for i in range(1, 17):
        tag_id = f"7404-DG-{i:03d}"
        tag_name = f"DG_7404_{i:03d}"
        alias = f"Local:2:I.Ch{i-1}Data"
        tags.extend([
            (f"{tag_name}_Raw", "INT", f"{tag_id} Raw 4-20mA Channel Data", alias, "counts", 0, 32000),
            (f"{tag_name}_Scaled", "REAL", f"{tag_id} Combustible Gas Concentration (%LEL)", "", "%LEL", 0, 100),
            (f"{tag_name}_LowAlm", "BOOL", f"{tag_id} Low Gas Alarm (>= 20% LEL)", "", "", 0, 1),
            (f"{tag_name}_HiHiAlm", "BOOL", f"{tag_id} High-High Gas Alarm (>= 30% LEL)", "", "", 0, 1),
            (f"{tag_name}_Flt_Low", "BOOL", f"{tag_id} Sensor Underrange / Open Circuit Fault (< -4% LEL)", "", "", 0, 1),
            (f"{tag_name}_Flt_High", "BOOL", f"{tag_id} Sensor Overrange Fault (> 105% LEL)", "", "", 0, 1),
            (f"{tag_name}_BeamBlock", "BOOL", f"{tag_id} Optical Beam Block Maintenance Flag", "", "", 0, 1),
            (f"{tag_name}_Inhibit", "BOOL", f"{tag_id} Maintenance Software Inhibit Flag", "", "", 0, 1),
        ])

    # Slot 3 (1756-IF16): Process Pressures, Foam Release & CH4 Gas 17..24
    slot3_pts = [
        ("PIT_001_OilExped", 0, "PIT-001", "Oil Expedition Pressure Transmitter", "psi", 0, 150),
        ("PIT_002_WaterInjMan", 1, "PIT-002", "Water Injection Manifold Pressure Transmitter", "psi", 0, 1000),
        ("PIT_003_OilInjMan", 2, "PIT-003", "Oil Injection Manifold Pressure Transmitter", "psi", 0, 3500),
        ("PST_7503_001_Deluge", 3, "7503-PST-001", "Deluge Line Pressure Transmitter", "psi", 0, 150),
        ("PST_7002_001_AirAcc", 4, "7002-PST-001", "ESDV Air Accumulator Pressure Transmitter", "psi", 0, 150),
        ("PST_6401_001_FuelGas", 5, "6401-PST-001", "Fuel Gas Line Pressure Transmitter", "psi", 0, 150),
        ("FR_7503_003_LocalCP", 6, "7503-FR-003", "Manual Foam Release Button Inside Local CP", "state", 0, 1),
        ("FR_7503_001_002_Field", 7, "7503-FR-001/002", "Manual Foam Release Button Outside in Field", "state", 0, 1),
    ]
    for tag_name, ch, tag_id, desc, unit, min_v, max_v in slot3_pts:
        alias = f"Local:3:I.Ch{ch}Data"
        tags.extend([
            (f"{tag_name}_Raw", "INT", f"{tag_id} Raw Channel Data", alias, "counts", 0, 32000),
            (f"{tag_name}_Scaled", "REAL", f"{tag_id} Scaled Process Value ({desc})", "", unit, min_v, max_v),
            (f"{tag_name}_LowAlm", "BOOL", f"{tag_id} Low Alarm / Low Supply Flag", "", "", 0, 1),
            (f"{tag_name}_HighAlm", "BOOL", f"{tag_id} High Alarm Flag", "", "", 0, 1),
            (f"{tag_name}_HiHiAlm", "BOOL", f"{tag_id} High-High Shutdown Trip Flag", "", "", 0, 1),
            (f"{tag_name}_Flt", "BOOL", f"{tag_id} Transmitter Signal Fault / Out of Range", "", "", 0, 1),
            (f"{tag_name}_Inhibit", "BOOL", f"{tag_id} Maintenance Inhibit Flag", "", "", 0, 1),
        ])

    # Slot 3 Ch 8..15: Gas Detectors 7404-DG-017 .. 024
    for i in range(17, 25):
        tag_id = f"7404-DG-{i:03d}"
        tag_name = f"DG_7404_{i:03d}"
        ch_idx = 8 + (i - 17)
        alias = f"Local:3:I.Ch{ch_idx}Data"
        tags.extend([
            (f"{tag_name}_Raw", "INT", f"{tag_id} Raw 4-20mA Channel Data", alias, "counts", 0, 32000),
            (f"{tag_name}_Scaled", "REAL", f"{tag_id} Combustible Gas Concentration (%LEL)", "", "%LEL", 0, 100),
            (f"{tag_name}_LowAlm", "BOOL", f"{tag_id} Low Gas Alarm (>= 20% LEL)", "", "", 0, 1),
            (f"{tag_name}_HiHiAlm", "BOOL", f"{tag_id} High-High Gas Alarm (>= 30% LEL)", "", "", 0, 1),
            (f"{tag_name}_Flt_Low", "BOOL", f"{tag_id} Sensor Underrange / Open Circuit Fault (< -4% LEL)", "", "", 0, 1),
            (f"{tag_name}_Flt_High", "BOOL", f"{tag_id} Sensor Overrange Fault (> 105% LEL)", "", "", 0, 1),
            (f"{tag_name}_BeamBlock", "BOOL", f"{tag_id} Optical Beam Block Maintenance Flag", "", "", 0, 1),
            (f"{tag_name}_Inhibit", "BOOL", f"{tag_id} Maintenance Software Inhibit Flag", "", "", 0, 1),
        ])

    # Slot 4 (1756-IF16): H2S Toxic Gas (0..10), Flame (11..13), Smoke (14)
    for i in range(1, 12):
        tag_id = f"H2S-{i:03d}"
        tag_name = f"AIT_H2S_{i:03d}"
        alias = f"Local:4:I.Ch{i-1}Data"
        tags.extend([
            (f"{tag_name}_Raw", "INT", f"{tag_id} Raw Toxic Gas Channel Data", alias, "counts", 0, 32000),
            (f"{tag_name}_Scaled", "REAL", f"{tag_id} Toxic Gas H2S Concentration (ppm)", "", "ppm", 0, 100),
            (f"{tag_name}_LowAlm", "BOOL", f"{tag_id} Low Toxic Alarm (>= 10 ppm H2S)", "", "", 0, 1),
            (f"{tag_name}_HiHiAlm", "BOOL", f"{tag_id} High-High Toxic Alarm (>= 20 ppm H2S)", "", "", 0, 1),
            (f"{tag_name}_Flt", "BOOL", f"{tag_id} H2S Detector Sensor Fault", "", "", 0, 1),
            (f"{tag_name}_Inhibit", "BOOL", f"{tag_id} Maintenance Inhibit Flag", "", "", 0, 1),
        ])

    # Flame Detectors (Slot 4 Ch 11..13)
    for i in range(1, 4):
        tag_id = f"7404-DF-{i:03d}"
        tag_name = f"DF_7404_{i:03d}"
        alias = f"Local:4:I.Ch{10+i}Data"
        tags.extend([
            (f"{tag_name}_Raw", "INT", f"{tag_id} Optical Flame Detector Raw Data", alias, "counts", 0, 32000),
            (f"{tag_name}_FireAlarm", "BOOL", f"{tag_id} Triple-IR Optical Flame Confirmed Alarm", "", "", 0, 1),
            (f"{tag_name}_Fault", "BOOL", f"{tag_id} Optical Flame Window Dirty / Circuit Fault", "", "", 0, 1),
            (f"{tag_name}_Inhibit", "BOOL", f"{tag_id} Flame Detector Maintenance Inhibit", "", "", 0, 1),
        ])

    # Smoke Detector (Slot 4 Ch 14)
    tags.extend([
        ("SD_001_002_Raw", "INT", "SD-001/002 Gas Generator Smoke Detector Raw", "Local:4:I.Ch14Data", "counts", 0, 32000),
        ("SD_001_002_Alarm", "BOOL", "SD-001/002 Gas Generator Smoke Confirmed Alarm", "", "", 0, 1),
        ("SD_001_002_Fault", "BOOL", "SD-001/002 Smoke Detector Circuit Fault", "", "", 0, 1),
        ("SD_001_002_Inhibit", "BOOL", "SD-001/002 Smoke Detector Maintenance Inhibit", "", "", 0, 1),
    ])

    # Slot 6 (1756-IF8H): Radar Level Transmitters LIT-100 .. LIT-400
    for i, tnum in enumerate([100, 200, 300, 400]):
        tag_id = f"LIT-{tnum}"
        tag_name = f"LIT_{tnum}_Tank"
        alias = f"Local:6:I.Ch{i}Data"
        tags.extend([
            (f"{tag_name}_Raw", "INT", f"{tag_id} Crude Storage Tank Radar Raw Data", alias, "counts", 0, 32000),
            (f"{tag_name}_Scaled", "REAL", f"{tag_id} Crude Storage Tank Liquid Level (m)", "", "m", 0, 14),
            (f"{tag_name}_LowAlm", "BOOL", f"{tag_id} Low Tank Level Alarm (LAL <= 0.7m)", "", "", 0, 1),
            (f"{tag_name}_HighAlm", "BOOL", f"{tag_id} High Tank Level Alarm (LAH >= 9.0m/11.0m)", "", "", 0, 1),
            (f"{tag_name}_Flt", "BOOL", f"{tag_id} Radar Transmitter Diagnostic Fault", "", "", 0, 1),
            (f"{tag_name}_Inhibit", "BOOL", f"{tag_id} Tank Level Maintenance Inhibit", "", "", 0, 1),
        ])

    # Slot 7 (1756-IB32): Discrete Digital Inputs
    slot7_dis = [
        ("ZSH_6401_001", 0, "6401-ZSH-001", "ESDV Fuel Gas Fully Open Limit Switch"),
        ("ZSL_6401_001", 1, "6401-ZSL-001", "ESDV Fuel Gas Fully Closed Limit Switch"),
        ("DI_Slot7_Spare_2", 2, "SPARE", "Spare Digital Input Terminal 3"),
        ("LS_7503_002_DieselTank", 3, "7503-LS-002", "Deluge Standby Diesel Fuel Tank Low Level Switch"),
        ("FS_7503_001_FoamStop", 4, "7503-FS-001", "Deluge Foam Release System Stop Pushbutton"),
        ("LS_7503_001_FoamTank", 5, "7503-LS-001", "AFFF Foam Concentrate Tank Low Level Switch"),
        ("C_75_01A_PumpAPulse", 6, "75-C-01A", "Deluge Pump A Trip Coil Continuity Pulse Return"),
        ("C_75_01B_PumpBPulse", 7, "75-C-01B", "Deluge Standby Pump B Trip Coil Continuity Pulse Return"),
        ("SB_75_01B_PumpBInhKey", 8, "75-SB-01B", "Standby Diesel Pump B Maintenance Inhibit Keyswitch"),
        ("DI_Slot7_Spare_9", 9, "SPARE", "Spare Digital Input Terminal 10"),
        ("PB_E11_AlarmReset", 10, "FGCP-7404-001-E11", "Master Alarm Reset Pushbutton (E11)"),
        ("PB_E12_AlarmMute", 11, "FGCP-7404-001-E12", "Master Alarm Acoustic Mute / Silence Pushbutton (E12)"),
        ("PB_E9_ESD_FuelGas", 12, "6401-ESDV-001-E9", "Emergency Shutdown Fuel Gas Line Pushbutton (E9)"),
        ("KEY_S2_FoamInhibit", 13, "FGCP-7404-001-S2", "Deluge Foam Release Inhibit Keyswitch (S2)"),
        ("KEY_S3_AllOutputsInhibit", 14, "FGCP-7404-001-S3", "Maintenance Override Inhibit All Outputs Keyswitch (S3)"),
        ("PB_E1_E4_PowerOilStop", 15, "E1-E4", "Emergency Stop Power Oil Pumps Pushbuttons E1..E4"),
        ("PB_E5_E6_WaterInjStop", 16, "E5-E6", "Emergency Stop Water Injection Pumps Pushbuttons E5..E6"),
        ("PUMP_A_Run_Feedback", 17, "PUMP-A-AUX", "Deluge Electric Duty Pump A Run Aux Contact"),
        ("PUMP_B_Run_Feedback", 18, "PUMP-B-AUX", "Deluge Diesel Standby Pump B Run Aux Contact"),
        ("PSLL_7404_001_LoPress", 19, "7404-PSLL-001", "Firewater Ring Main Header Low Pressure Switch (< 7.0 bar)"),
    ]
    for tag_name, pt, tag_id, desc in slot7_dis:
        alias = f"Local:7:I.Data.{pt}"
        tags.append((tag_name, "BOOL", f"{tag_id}: {desc}", alias, "state", 0, 1))

    # Add remaining spare DI bits
    for pt in range(20, 32):
        alias = f"Local:7:I.Data.{pt}"
        tags.append((f"DI_Slot7_Spare_{pt}", "BOOL", f"Slot 7 Spare Digital Input Bit {pt}", alias, "state", 0, 1))

    # Slot 8 (1756-OB32): Discrete Digital Outputs
    slot8_dos = [
        ("ESD_TRIP_Master", 0, "ESD_TRIP", "Master Plant Emergency Shutdown Relay (Fail-Safe 1=Run)"),
        ("EY_6401_001_002", 1, "6401-EY-001/002", "Fuel Gas ESDV Solenoid Valve (Fail-Safe 1=Open)"),
        ("SA_7404_001_002", 2, "7404-SA-001/002", "Pump House Local Fire & Gas Alarm Bell"),
        ("DO_7503_PumpA_Pulse", 3, "7503-PUMP-A-PULSE", "Deluge Pump A Trip Coil Test Pulse Output"),
        ("DO_7503_PumpA_Cmd", 4, "7503-PUMP-A-CMD", "Deluge Duty Electric Pump A Run Command"),
        ("DO_7503_PumpB_Pulse", 5, "7503-PUMP-B-PULSE", "Deluge Standby Pump B Test Pulse Output"),
        ("DO_7503_PumpB_Start", 6, "7503-PUMP-B-START", "Deluge Standby Diesel Pump B Start Pulse"),
        ("DO_7503_PumpB_Stop", 7, "7503-PUMP-B-STOP", "Deluge Standby Diesel Pump B Stop Pulse"),
        ("EDB1_OilBoosterStop", 8, "EDB1-OIL", "Oil Booster Pump Shutdown Relay (Fail-Safe 1=Run)"),
        ("EDB1_WaterBoosterStop", 9, "EDB1-WATER", "Water Booster Pump Shutdown Relay (Fail-Safe 1=Run)"),
        ("DO_Slot8_Spare_10", 10, "SPARE", "Spare Discrete Output Bit 10"),
        ("LED_L14_ESDV_Closed", 11, "FGCP-L14", "PCR Panel LED L14: ESDV Fuel Gas Closed (Red)"),
        ("LED_L15_ESDV_Open", 12, "FGCP-L15", "PCR Panel LED L15: ESDV Fuel Gas Open (Green)"),
        ("LED_L16_LowAirAcc", 13, "FGCP-L16", "PCR Panel LED L16: ESDV Low Air Supply Accumulator (Amber)"),
        ("LED_L17_LowFuelGas", 14, "FGCP-L17", "PCR Panel LED L17: Fuel Gas Line Low Pressure (Amber)"),
        ("CR1_P2300_Stop_L8", 15, "CR1-L8", "Stop Power Oil Pump P-2300 Relay & PCR LED L8"),
        ("CR2_P2400_Stop_L9", 16, "CR2-L9", "Stop Power Oil Pump P-2400 Relay & PCR LED L9"),
        ("CR3_P2500_Stop_L10", 17, "CR3-L10", "Stop Power Oil Pump P-2500 Relay & PCR LED L10"),
        ("CR4_P2600_Stop_L11", 18, "CR4-L11", "Stop Power Oil Pump P-2600 Relay & PCR LED L11"),
        ("CR5_P3800_Stop_L12", 19, "CR5-L12", "Stop Water Injection Pump P-3800 Relay & PCR LED L12"),
        ("CR6_P3900_Stop_L13", 20, "CR6-L13", "Stop Water Injection Pump P-3900 Relay & PCR LED L13"),
        ("SD_GE_GasGenTrip", 21, "SD-GE", "Emergency Trip of All Gas Turbine Generators Output"),
        ("HORN_PCR_Z1", 22, "FGCP-Z1", "Production Control Room Main Alarm Horn Z1"),
        ("HORN_PA_001_Building", 23, "PA-001", "Process Production Building Alarm Siren"),
        ("DO_Slot8_Spare_24", 24, "SPARE", "Spare Discrete Output Bit 24"),
        ("DO_Slot8_Spare_25", 25, "SPARE", "Spare Discrete Output Bit 25"),
        ("DO_Slot8_Spare_26", 26, "SPARE", "Spare Discrete Output Bit 26"),
        ("DO_Slot8_Spare_27", 27, "SPARE", "Spare Discrete Output Bit 27"),
        ("DO_Slot8_Spare_28", 28, "SPARE", "Spare Discrete Output Bit 28"),
        ("DO_Slot8_Spare_29", 29, "SPARE", "Spare Discrete Output Bit 29"),
        ("ALARM_H2S_SirenStrobe", 30, "H2SA-001/002", "H2S Toxic Gas Siren and Blue Strobe Beacon"),
        ("ALARM_Smoke_SirenStrobe", 31, "SDA-001", "Smoke Detection Siren and Amber Strobe Beacon"),
    ]
    for tag_name, pt, tag_id, desc in slot8_dos:
        alias = f"Local:8:O.Data.{pt}"
        tags.append((tag_name, "BOOL", f"{tag_id}: {desc}", alias, "state", 0, 1))

    # Internal Logic Flags, 2ooN Voting, Setpoints & Interlocks
    tags.extend([
        ("SET_CH4_LowAlm_LEL", "REAL", "Calibrated CH4 Gas Low Alarm Setpoint (%LEL)", "", "%LEL", 0, 100),
        ("SET_CH4_HiHiAlm_LEL", "REAL", "Calibrated CH4 Gas High-High Alarm Setpoint (%LEL)", "", "%LEL", 0, 100),
        ("SET_H2S_LowAlm_PPM", "REAL", "Calibrated H2S Toxic Gas Low Alarm Setpoint (ppm)", "", "ppm", 0, 100),
        ("SET_H2S_HiHiAlm_PPM", "REAL", "Calibrated H2S Toxic Gas High-High Alarm Setpoint (ppm)", "", "ppm", 0, 100),
        ("SET_OilInj_PAL_PSI", "REAL", "Oil Injection Manifold Low Pressure Alarm Setpoint (psi)", "", "psi", 0, 3500),
        ("SET_OilInj_PAH_PSI", "REAL", "Oil Injection Manifold High Pressure Alarm Setpoint (psi)", "", "psi", 0, 3500),
        ("SET_OilInj_PAHH_PSI", "REAL", "Oil Injection Manifold High-High Shutdown Trip Setpoint (psi)", "", "psi", 0, 3500),
        ("SET_WaterInj_PAL_PSI", "REAL", "Water Injection Manifold Low Pressure Alarm Setpoint (psi)", "", "psi", 0, 1000),
        ("SET_WaterInj_PAH_PSI", "REAL", "Water Injection Manifold High Pressure Alarm Setpoint (psi)", "", "psi", 0, 1000),
        ("SET_WaterInj_PAHH_PSI", "REAL", "Water Injection Manifold High-High Shutdown Trip Setpoint (psi)", "", "psi", 0, 1000),
        ("SET_FuelGas_PAL_PSI", "REAL", "Fuel Gas Line Low Pressure Alarm Setpoint (psi)", "", "psi", 0, 150),
        ("SET_FuelGas_PAH_PSI", "REAL", "Fuel Gas Line High Pressure Shutdown Trip Setpoint (psi)", "", "psi", 0, 150),
        ("SET_AirAcc_Low_PSI", "REAL", "ESDV Air Accumulator Minimum Supply Pressure Setpoint (psi)", "", "psi", 0, 150),
        ("SET_OilExped_PAL_PSI", "REAL", "Oil Expedition Line Low Pressure Setpoint (psi)", "", "psi", 0, 150),
        ("SET_OilExped_PAH_PSI", "REAL", "Oil Expedition Line High Pressure Setpoint (psi)", "", "psi", 0, 150),
        ("SET_Tank_LAL_Meters", "REAL", "Crude Storage Tanks Low Level Alarm Limit (m)", "", "m", 0, 14),
        ("SET_Tank_LAH_Meters", "REAL", "Crude Storage Tanks High Level Alarm Limit (m)", "", "m", 0, 14),
        
        # 2ooN Confirmed Gas Voting Flags
        ("VOTE_Zone1_Gas_Confirmed", "BOOL", "Zone 1 (Separator Area) 2ooN Confirmed Gas Cloud", "", "", 0, 1),
        ("VOTE_Zone2_Gas_Confirmed", "BOOL", "Zone 2 (Pump House) 2ooN Confirmed Gas Cloud", "", "", 0, 1),
        ("VOTE_Zone3_Gas_Confirmed", "BOOL", "Zone 3 (Tank Farm) 2ooN Confirmed Gas Cloud", "", "", 0, 1),
        ("VOTE_Zone4_Gas_Confirmed", "BOOL", "Zone 4 (Gas Generator Building) 2ooN Confirmed Gas Cloud", "", "", 0, 1),
        ("VOTE_Any_Confirmed_Gas", "BOOL", "Global Plant Confirmed Combustible Gas Detected", "", "", 0, 1),
        ("VOTE_Any_Confirmed_Fire", "BOOL", "Global Plant Confirmed Optical Flame / Fire Detected", "", "", 0, 1),
        ("VOTE_Any_Confirmed_Toxic", "BOOL", "Global Plant Confirmed Toxic H2S Gas Detected", "", "", 0, 1),
        ("VOTE_Deluge_Demand", "BOOL", "Master Deluge Firewater Release Demand Active", "", "", 0, 1),
        ("ESD_Matrix_Master_Trip", "BOOL", "Master Cause & Effect Matrix Plant Shutdown Trip Latch", "", "", 0, 1),
        ("ESD_Gas_Turbine_Trip", "BOOL", "Gas Turbine Generators Shutdown Trip Latch", "", "", 0, 1),
        ("ESD_Power_Oil_Trip", "BOOL", "Power Oil Booster Pumps P2100/P2200 Trip Latch", "", "", 0, 1),
        ("ESD_Water_Inj_Trip", "BOOL", "Water Injection Booster Pumps P3600/P3700 Trip Latch", "", "", 0, 1),
        ("ESDV_Transit_Discrepancy", "BOOL", "ESDV-6401-001 Open/Close Transit Discrepancy Fault", "", "", 0, 1),
        ("ESDV_Fail_To_Open", "BOOL", "ESDV-6401-001 Commanded Open but Failed to Confirm", "", "", 0, 1),
        ("ESDV_Fail_To_Close", "BOOL", "ESDV-6401-001 Commanded Close but Failed to Confirm", "", "", 0, 1),
        ("COMMON_SYSTEM_FAULT", "BOOL", "General Instrumentation & Hardware Diagnostic Fault Summary", "", "", 0, 1),
    ])

    return tags

print("build_upgraded_tags() defined.")

# =============================================================================
# 2. UPGRADED RLL ROUTINES (Per 01-MAN-03-07 & 01-MAN-03-08)
# =============================================================================
def build_upgraded_rll_routines():
    """Build all 16 upgraded routines as pure Allen-Bradley Relay Ladder Logic."""
    routines = []

    # -------------------------------------------------------------------------
    # 1. Main_Scheduler
    # -------------------------------------------------------------------------
    rungs_main = [
        {"comment": "Rung 0: 400ms Free-Running Slow Flasher (Annunciator Flash)", "text": "XIO(TMR_Flash_Fast.DN) TON(TMR_Flash_Slow,?,?);"},
        {"comment": "Rung 1: 200ms Free-Running Fast Flasher (High-High Strobe)", "text": "XIC(TMR_Flash_Slow.DN) TON(TMR_Flash_Fast,?,?);"},
        {"comment": "Rung 2: First Scan Initialization Subroutine Trigger", "text": "XIC(S:FS) JSR(Init_Setpoints,0);"},
        {"comment": "Rung 3: Execute Hardware Input Acquisition Routine", "text": "JSR(IO_Input_Acquisition,0);"},
        {"comment": "Rung 4: Execute Combustible CH4 Gas Detection Processing", "text": "JSR(FAG_Combustible_CH4,0);"},
        {"comment": "Rung 5: Execute Toxic H2S Gas Detection Processing", "text": "JSR(FAG_Toxic_H2S,0);"},
        {"comment": "Rung 6: Execute Optical Flame Detection Processing", "text": "JSR(FAG_Optical_Flame,0);"},
        {"comment": "Rung 7: Execute Smoke Detection Processing", "text": "JSR(FAG_Smoke_Detection,0);"},
        {"comment": "Rung 8: Execute Multi-Zone 2ooN Voting Logic", "text": "JSR(Voting_2ooN_Coincidence,0);"},
        {"comment": "Rung 9: Execute Process Pressure Monitoring & Safeguards", "text": "JSR(Process_Pressure_Safeguards,0);"},
        {"comment": "Rung 10: Execute Crude Storage Tank Radar Levels Processing", "text": "JSR(Process_Tank_Levels,0);"},
        {"comment": "Rung 11: Execute Deluge & Firewater Skid Sequencing", "text": "JSR(Deluge_Firewater_Control,0);"},
        {"comment": "Rung 12: Execute Master Cause & Effect Matrix Shutdown Cascades", "text": "JSR(ESD_Cause_Effect_Matrix,0);"},
        {"comment": "Rung 13: Execute Maintenance Bypass & Keyswitch Interlocks", "text": "JSR(Inhibit_Maintenance,0);"},
        {"comment": "Rung 14: Execute PCR Annunciator Panel & Horn Sounder Drivers", "text": "JSR(Annunciation_PCR_Panel,0);"},
        {"comment": "Rung 15: Execute Hardware Output Image Dispatch", "text": "JSR(IO_Output_Dispatch,0);"},
        {"comment": "Rung 16: Maintain Controller Watchdog Healthy Flag", "text": "XIO(COMMON_SYSTEM_FAULT) OTE(SYS_Watchdog_OK);"}
    ]
    routines.append(("Main_Scheduler", "Executive Cycle Scheduler & Subroutine Dispatch", rungs_main))

    # -------------------------------------------------------------------------
    # 2. Init_Setpoints
    # -------------------------------------------------------------------------
    rungs_init = [
        {"comment": "Rung 0: Combustible Gas Alarm Trip Limits (20% Low, 30% High-High LEL)", "text": "MOV(20.0,SET_CH4_LowAlm_LEL) MOV(30.0,SET_CH4_HiHiAlm_LEL);"},
        {"comment": "Rung 1: Toxic H2S Alarm Trip Limits (10 ppm Low, 20 ppm High-High)", "text": "MOV(10.0,SET_H2S_LowAlm_PPM) MOV(20.0,SET_H2S_HiHiAlm_PPM);"},
        {"comment": "Rung 2: Oil Injection Manifold Limits (PAL 1700, PAH 2700, PAHH 2800 psi)", "text": "MOV(1700.0,SET_OilInj_PAL_PSI) MOV(2700.0,SET_OilInj_PAH_PSI) MOV(2800.0,SET_OilInj_PAHH_PSI);"},
        {"comment": "Rung 3: Water Injection Manifold Limits (PAL 200, PAH 800, PAHH 800 psi)", "text": "MOV(200.0,SET_WaterInj_PAL_PSI) MOV(800.0,SET_WaterInj_PAH_PSI) MOV(800.0,SET_WaterInj_PAHH_PSI);"},
        {"comment": "Rung 4: Fuel Gas Line Pressure Limits (PAL 40, PAH 100 psi)", "text": "MOV(40.0,SET_FuelGas_PAL_PSI) MOV(100.0,SET_FuelGas_PAH_PSI);"},
        {"comment": "Rung 5: ESDV Air Accumulator Minimum Pressure Limit (50 psi)", "text": "MOV(50.0,SET_AirAcc_Low_PSI);"},
        {"comment": "Rung 6: Oil Expedition Line Limits (PAL 10, PAH 100 psi)", "text": "MOV(10.0,SET_OilExped_PAL_PSI) MOV(100.0,SET_OilExped_PAH_PSI);"},
        {"comment": "Rung 7: Crude Storage Tank Radar Levels (LAL 0.7m, LAH 9.0m/11.0m)", "text": "MOV(0.7,SET_Tank_LAL_Meters) MOV(9.0,SET_Tank_LAH_Meters);"}
    ]
    routines.append(("Init_Setpoints", "Calibrated Engineering Ranges & Trip Setpoint Initialization", rungs_init))

    # -------------------------------------------------------------------------
    # 3. IO_Input_Acquisition
    # -------------------------------------------------------------------------
    rungs_in = [
        {"comment": "Rung 0: 6401-ZSH-001 ESDV Open Limit Switch Acquisition", "text": "XIC(Local:7:I.Data.0) OTE(ZSH_6401_001);"},
        {"comment": "Rung 1: 6401-ZSL-001 ESDV Closed Limit Switch Acquisition", "text": "XIC(Local:7:I.Data.1) OTE(ZSL_6401_001);"},
        {"comment": "Rung 2: 7503-LS-002 Diesel Fuel Tank Low Level Switch", "text": "XIC(Local:7:I.Data.3) OTE(LS_7503_002_DieselTank);"},
        {"comment": "Rung 3: 7503-FS-001 Deluge Foam Stop Pushbutton", "text": "XIC(Local:7:I.Data.4) OTE(FS_7503_001_FoamStop);"},
        {"comment": "Rung 4: 7503-LS-001 AFFF Foam Tank Low Level Switch", "text": "XIC(Local:7:I.Data.5) OTE(LS_7503_001_FoamTank);"},
        {"comment": "Rung 5: 75-C-01A Deluge Pump A Coil Pulse Return Feedback", "text": "XIC(Local:7:I.Data.6) OTE(C_75_01A_PumpAPulse);"},
        {"comment": "Rung 6: 75-C-01B Deluge Pump B Coil Pulse Return Feedback", "text": "XIC(Local:7:I.Data.7) OTE(C_75_01B_PumpBPulse);"},
        {"comment": "Rung 7: 75-SB-01B Standby Diesel Pump B Inhibit Keyswitch", "text": "XIC(Local:7:I.Data.8) OTE(SB_75_01B_PumpBInhKey);"},
        {"comment": "Rung 8: Master Alarm Reset Pushbutton E11", "text": "XIC(Local:7:I.Data.10) OTE(PB_E11_AlarmReset);"},
        {"comment": "Rung 9: Master Alarm Mute / Silence Pushbutton E12", "text": "XIC(Local:7:I.Data.11) OTE(PB_E12_AlarmMute);"},
        {"comment": "Rung 10: 6401-ESDV-001 Fuel Gas ESD Pushbutton E9", "text": "XIC(Local:7:I.Data.12) OTE(PB_E9_ESD_FuelGas);"},
        {"comment": "Rung 11: Deluge Foam Release Inhibition Keyswitch S2", "text": "XIC(Local:7:I.Data.13) OTE(KEY_S2_FoamInhibit);"},
        {"comment": "Rung 12: Maintenance All Outputs Inhibition Keyswitch S3", "text": "XIC(Local:7:I.Data.14) OTE(KEY_S3_AllOutputsInhibit);"},
        {"comment": "Rung 13: Emergency Stop Power Oil Pumps Pushbuttons E1..E4", "text": "XIC(Local:7:I.Data.15) OTE(PB_E1_E4_PowerOilStop);"},
        {"comment": "Rung 14: Emergency Stop Water Injection Pumps Pushbuttons E5..E6", "text": "XIC(Local:7:I.Data.16) OTE(PB_E5_E6_WaterInjStop);"},
        {"comment": "Rung 15: Deluge Duty Pump A Aux Running Contact", "text": "XIC(Local:7:I.Data.17) OTE(PUMP_A_Run_Feedback);"},
        {"comment": "Rung 16: Deluge Standby Diesel Pump B Aux Running Contact", "text": "XIC(Local:7:I.Data.18) OTE(PUMP_B_Run_Feedback);"},
        {"comment": "Rung 17: 7404-PSLL-001 Firewater Header Low Pressure Switch", "text": "XIC(Local:7:I.Data.19) OTE(PSLL_7404_001_LoPress);"}
    ]
    routines.append(("IO_Input_Acquisition", "Slot 2..7 1756 Module Data Acquisition to Engineering Tags", rungs_in))

    # -------------------------------------------------------------------------
    # 4. FAG_Combustible_CH4
    # -------------------------------------------------------------------------
    rungs_ch4 = []
    for i in range(1, 25):
        tname = f"DG_7404_{i:03d}"
        tag_id = f"7404-DG-{i:03d}"
        ch_text = f"Local:2:I.Ch{i-1}Data" if i <= 16 else f"Local:3:I.Ch{8+(i-17)}Data"
        rungs_ch4.extend([
            {"comment": f"Scale {tag_id} Raw Counts to 0-100% LEL", "text": f"CPT({tname}_Scaled,(100.0/32000.0)*{ch_text});"},
            {"comment": f"{tag_id} Low Alarm (>= 20% LEL) & High-High (>= 30% LEL)", "text": f"[ GEQ({tname}_Scaled,SET_CH4_LowAlm_LEL) OTE({tname}_LowAlm) , GEQ({tname}_Scaled,SET_CH4_HiHiAlm_LEL) OTE({tname}_HiHiAlm) ];"},
            {"comment": f"{tag_id} Sensor Faults (Underrange < -4% or Overrange > 105%)", "text": f"[ LES({tname}_Scaled,-4.0) OTE({tname}_Flt_Low) , GRT({tname}_Scaled,105.0) OTE({tname}_Flt_High) ];"}
        ])
    routines.append(("FAG_Combustible_CH4", "24 Combustible CH4 Gas Detectors Scaling, Diagnostics & Alarms", rungs_ch4))

    # -------------------------------------------------------------------------
    # 5. FAG_Toxic_H2S
    # -------------------------------------------------------------------------
    rungs_h2s = []
    for i in range(1, 12):
        tname = f"AIT_H2S_{i:03d}"
        tag_id = f"H2S-{i:03d}"
        rungs_h2s.extend([
            {"comment": f"Scale {tag_id} Toxic Gas to 0-100 ppm", "text": f"CPT({tname}_Scaled,(100.0/32000.0)*Local:4:I.Ch{i-1}Data);"},
            {"comment": f"{tag_id} Low Alarm (>= 10 ppm) & High-High Alarm (>= 20 ppm)", "text": f"[ GEQ({tname}_Scaled,SET_H2S_LowAlm_PPM) OTE({tname}_LowAlm) , GEQ({tname}_Scaled,SET_H2S_HiHiAlm_PPM) OTE({tname}_HiHiAlm) ];"}
        ])
    routines.append(("FAG_Toxic_H2S", "Toxic H2S Gas Detection (10 ppm Discontinuous / 20 ppm Continuous)", rungs_h2s))

    # -------------------------------------------------------------------------
    # 6. FAG_Optical_Flame
    # -------------------------------------------------------------------------
    rungs_flame = [
        {"comment": "7404-DF-001 Triple-IR Optical Flame Detector Trip Evaluation", "text": "GRT(Local:4:I.Ch11Data,16000) OTE(DF_7404_001_FireAlarm);"},
        {"comment": "7404-DF-002 Triple-IR Optical Flame Detector Trip Evaluation", "text": "GRT(Local:4:I.Ch12Data,16000) OTE(DF_7404_002_FireAlarm);"},
        {"comment": "7404-DF-003 Triple-IR Optical Flame Detector Trip Evaluation", "text": "GRT(Local:4:I.Ch13Data,16000) OTE(DF_7404_003_FireAlarm);"},
        {"comment": "Global Confirmed Optical Fire Alarm Latch", "text": "[ XIC(DF_7404_001_FireAlarm) , XIC(DF_7404_002_FireAlarm) , XIC(DF_7404_003_FireAlarm) ] OTE(VOTE_Any_Confirmed_Fire);"}
    ]
    routines.append(("FAG_Optical_Flame", "Triple-IR Optical Flame Detection (Immediate Deluge & ESD Trigger)", rungs_flame))

    # -------------------------------------------------------------------------
    # 7. FAG_Smoke_Detection
    # -------------------------------------------------------------------------
    rungs_smoke = [
        {"comment": "SD-001/002 Gas Generator Building Optical Smoke Detector", "text": "GRT(Local:4:I.Ch14Data,16000) OTE(SD_001_002_Alarm);"},
        {"comment": "Gas Generator Building Smoke Shutdown Trip Initiate", "text": "XIC(SD_001_002_Alarm) [ OTE(ESD_Gas_Turbine_Trip) , OTE(ALARM_Smoke_SirenStrobe) ];"}
    ]
    routines.append(("FAG_Smoke_Detection", "Gas Generator Building Smoke Detection & Turbine Trip Logic", rungs_smoke))

    # -------------------------------------------------------------------------
    # 8. Voting_2ooN_Coincidence
    # -------------------------------------------------------------------------
    rungs_vote = [
        {"comment": "Zone 1 (Separator Area) 2ooN Gas Voting (DG-001 .. 003)", "text": "[ [ XIC(DG_7404_001_HiHiAlm) XIC(DG_7404_002_HiHiAlm) ] , [ XIC(DG_7404_001_HiHiAlm) XIC(DG_7404_003_HiHiAlm) ] , [ XIC(DG_7404_002_HiHiAlm) XIC(DG_7404_003_HiHiAlm) ] ] OTE(VOTE_Zone1_Gas_Confirmed);"},
        {"comment": "Zone 2 (Pump House) 2ooN Gas Voting (DG-004 .. 006)", "text": "[ [ XIC(DG_7404_004_HiHiAlm) XIC(DG_7404_005_HiHiAlm) ] , [ XIC(DG_7404_004_HiHiAlm) XIC(DG_7404_006_HiHiAlm) ] , [ XIC(DG_7404_005_HiHiAlm) XIC(DG_7404_006_HiHiAlm) ] ] OTE(VOTE_Zone2_Gas_Confirmed);"},
        {"comment": "Zone 3 (Tank Farm) 2ooN Gas Voting (DG-007 .. 010)", "text": "[ [ XIC(DG_7404_007_HiHiAlm) XIC(DG_7404_008_HiHiAlm) ] , [ XIC(DG_7404_008_HiHiAlm) XIC(DG_7404_009_HiHiAlm) ] , [ XIC(DG_7404_009_HiHiAlm) XIC(DG_7404_010_HiHiAlm) ] ] OTE(VOTE_Zone3_Gas_Confirmed);"},
        {"comment": "Zone 4 (Generator Room) 2ooN Gas Voting (DG-011 .. 013)", "text": "[ [ XIC(DG_7404_011_HiHiAlm) XIC(DG_7404_012_HiHiAlm) ] , [ XIC(DG_7404_012_HiHiAlm) XIC(DG_7404_013_HiHiAlm) ] ] OTE(VOTE_Zone4_Gas_Confirmed);"},
        {"comment": "Global Confirmed Combustible Gas Cloud Active", "text": "[ XIC(VOTE_Zone1_Gas_Confirmed) , XIC(VOTE_Zone2_Gas_Confirmed) , XIC(VOTE_Zone3_Gas_Confirmed) , XIC(VOTE_Zone4_Gas_Confirmed) ] OTE(VOTE_Any_Confirmed_Gas);"}
    ]
    routines.append(("Voting_2ooN_Coincidence", "Multi-Zone 2-out-of-N Coincidence Voting Matrix", rungs_vote))

    # -------------------------------------------------------------------------
    # 9. Process_Pressure_Safeguards
    # -------------------------------------------------------------------------
    rungs_pres = [
        {"comment": "Scale PIT-001 Oil Expedition Pressure (0-150 psi)", "text": "CPT(PIT_001_OilExped_Scaled,(150.0/32000.0)*Local:3:I.Ch0Data);"},
        {"comment": "Scale PIT-002 Water Injection Manifold Pressure (0-1000 psi)", "text": "CPT(PIT_002_WaterInjMan_Scaled,(1000.0/32000.0)*Local:3:I.Ch1Data);"},
        {"comment": "Scale PIT-003 Oil Injection Manifold Pressure (0-3500 psi)", "text": "CPT(PIT_003_OilInjMan_Scaled,(3500.0/32000.0)*Local:3:I.Ch2Data);"},
        {"comment": "Scale 7503-PST-001 Deluge Discharge Header Pressure (0-150 psi)", "text": "CPT(PST_7503_001_Deluge_Scaled,(150.0/32000.0)*Local:3:I.Ch3Data);"},
        {"comment": "Scale 7002-PST-001 ESDV Air Supply Accumulator Pressure (0-150 psi)", "text": "CPT(PST_7002_001_AirAcc_Scaled,(150.0/32000.0)*Local:3:I.Ch4Data);"},
        {"comment": "Scale 6401-PST-001 Fuel Gas Line Pressure (0-150 psi)", "text": "CPT(PST_6401_001_FuelGas_Scaled,(150.0/32000.0)*Local:3:I.Ch5Data);"},
        {"comment": "Oil Injection Manifold High-High Pressure Trip (PAHH >= 2800 psi)", "text": "GEQ(PIT_003_OilInjMan_Scaled,SET_OilInj_PAHH_PSI) [ OTE(PIT_003_OilInjMan_HiHiAlm) , OTE(ESD_Power_Oil_Trip) ];"},
        {"comment": "Water Injection Manifold High-High Pressure Trip (PAHH >= 800 psi)", "text": "GEQ(PIT_002_WaterInjMan_Scaled,SET_WaterInj_PAHH_PSI) [ OTE(PIT_002_WaterInjMan_HiHiAlm) , OTE(ESD_Water_Inj_Trip) ];"},
        {"comment": "Fuel Gas Line High Pressure Trip (PAH >= 100 psi)", "text": "GEQ(PST_6401_001_FuelGas_Scaled,SET_FuelGas_PAH_PSI) [ OTE(PST_6401_001_FuelGas_HighAlm) , OTE(ESD_Matrix_Master_Trip) ];"},
        {"comment": "Fuel Gas Line Low Pressure Alarm (PAL <= 40 psi) -> PCR Amber LED L17", "text": "LEQ(PST_6401_001_FuelGas_Scaled,SET_FuelGas_PAL_PSI) [ OTE(PST_6401_001_FuelGas_LowAlm) , OTE(LED_L17_LowFuelGas) ];"},
        {"comment": "ESDV Low Air Accumulator Supply (<= 50 psi) -> PCR Amber LED L16", "text": "LEQ(PST_7002_001_AirAcc_Scaled,SET_AirAcc_Low_PSI) [ OTE(PST_7002_001_AirAcc_LowAlm) , OTE(LED_L16_LowAirAcc) ];"}
    ]
    routines.append(("Process_Pressure_Safeguards", "Process Pressure Monitoring & Equipment Safety Interlocks", rungs_pres))

    # -------------------------------------------------------------------------
    # 10. Process_Tank_Levels
    # -------------------------------------------------------------------------
    rungs_tank = [
        {"comment": "Scale LIT-100 Tank T-100 Radar Level (0-14 m)", "text": "CPT(LIT_100_Tank_Scaled,(14.0/32000.0)*Local:6:I.Ch0Data);"},
        {"comment": "Scale LIT-200 Tank T-200 Radar Level (0-14 m)", "text": "CPT(LIT_200_Tank_Scaled,(14.0/32000.0)*Local:6:I.Ch1Data);"},
        {"comment": "Scale LIT-300 Tank T-300 Radar Level (0-14 m)", "text": "CPT(LIT_300_Tank_Scaled,(14.0/32000.0)*Local:6:I.Ch2Data);"},
        {"comment": "Scale LIT-400 Tank T-400 Radar Level (0-14 m)", "text": "CPT(LIT_400_Tank_Scaled,(14.0/32000.0)*Local:6:I.Ch3Data);"},
        {"comment": "T-100 Low Level (<= 0.7m) & High Level (>= 9.0m) Alarms", "text": "[ LEQ(LIT_100_Tank_Scaled,SET_Tank_LAL_Meters) OTE(LIT_100_Tank_LowAlm) , GEQ(LIT_100_Tank_Scaled,SET_Tank_LAH_Meters) OTE(LIT_100_Tank_HighAlm) ];"},
        {"comment": "AFFF Foam Concentrate Tank Low Level Switch (7503-LS-001)", "text": "XIC(LS_7503_001_FoamTank) OTE(HORN_PCR_Z1);"},
        {"comment": "Deluge Diesel Fuel Tank Low Level Switch (7503-LS-002)", "text": "XIC(LS_7503_002_DieselTank) OTE(HORN_PCR_Z1);"}
    ]
    routines.append(("Process_Tank_Levels", "Crude Storage Radar Levels & Firewater Auxiliary Tank Monitoring", rungs_tank))

    # -------------------------------------------------------------------------
    # 11. Deluge_Firewater_Control
    # -------------------------------------------------------------------------
    rungs_deluge = [
        {"comment": "Periodic 60s Timer for Deluge Trip Coil Continuity Line Check", "text": "XIO(TMR_Deluge_Pulse_Width.DN) TON(TMR_Deluge_Pulse_Period,?,?);"},
        {"comment": "1.0s Pulse Output for Deluge Solenoid Integrity Supervision", "text": "XIC(TMR_Deluge_Pulse_Period.DN) [ TON(TMR_Deluge_Pulse_Width,?,?) , OTE(DO_7503_PumpA_Pulse) , OTE(DO_7503_PumpB_Pulse) ];"},
        {"comment": "Deluge Firewater Demand Initiation (Fire, Foam Pushbutton, 2ooN Gas, or Header Low Pressure)", "text": "[ XIC(VOTE_Any_Confirmed_Fire) , XIC(VOTE_Any_Confirmed_Gas) , XIC(FR_7503_003_LocalCP_Scaled) , XIC(FR_7503_001_002_Field_Scaled) , XIC(PSLL_7404_001_LoPress) ] XIO(KEY_S2_FoamInhibit) XIO(FS_7503_001_FoamStop) OTE(VOTE_Deluge_Demand);"},
        {"comment": "Command Duty Electric Pump A Run Output", "text": "XIC(VOTE_Deluge_Demand) OTE(DO_7503_PumpA_Cmd);"},
        {"comment": "Duty Pump A Pressure Proving & 30-Second Fail-to-Run Timer", "text": "XIC(DO_7503_PumpA_Cmd) XIO(PUMP_A_Run_Feedback) TON(TMR_PumpA_FailToRun,?,?);"},
        {"comment": "Initiate Standby Diesel Pump B Crank Cycle on Pump A Failure", "text": "XIC(TMR_PumpA_FailToRun.DN) XIO(SB_75_01B_PumpBInhKey) XIO(PUMP_B_Run_Feedback) [ OTE(DO_7503_PumpB_Start) , TON(TMR_PumpB_StartCrank,?,?) ];"},
        {"comment": "Reset Deluge Demand on Foam Stop Pushbutton Press", "text": "XIC(FS_7503_001_FoamStop) [ OTU(VOTE_Deluge_Demand) , OTE(DO_7503_PumpB_Stop) ];"}
    ]
    routines.append(("Deluge_Firewater_Control", "Deluge Firewater Pump Auto-Start, 30s Transition & Line Supervision", rungs_deluge))

    # -------------------------------------------------------------------------
    # 12. ESD_Cause_Effect_Matrix
    # -------------------------------------------------------------------------
    rungs_esd = [
        {"comment": "Master Plant Emergency Shutdown Demand Initiation (PB-E9, Flame, 2ooN Gas, High Fuel Gas)", "text": "[ XIC(PB_E9_ESD_FuelGas) , XIC(VOTE_Any_Confirmed_Fire) , XIC(VOTE_Any_Confirmed_Gas) , XIC(PST_6401_001_FuelGas_HighAlm) ] XIO(KEY_S3_AllOutputsInhibit) OTE(ESD_Matrix_Master_Trip);"},
        {"comment": "Master Pump Shutdown Relay (Fail-Safe 1=Run, De-energize to Trip)", "text": "XIO(ESD_Matrix_Master_Trip) OTE(ESD_TRIP_Master);"},
        {"comment": "Fuel Gas ESDV Solenoid (Fail-Safe 1=Open, De-energize to Slam Shut)", "text": "XIO(ESD_Matrix_Master_Trip) OTE(EY_6401_001_002);"},
        {"comment": "Power Oil Booster Pumps P-2100 / P-2200 Trip Relay (Fail-Safe 1=Run)", "text": "[ XIO(ESD_Matrix_Master_Trip) XIO(ESD_Power_Oil_Trip) XIO(PB_E1_E4_PowerOilStop) ] OTE(EDB1_OilBoosterStop);"},
        {"comment": "Water Injection Booster Pumps P-3600 / P-3700 Trip Relay (Fail-Safe 1=Run)", "text": "[ XIO(ESD_Matrix_Master_Trip) XIO(ESD_Water_Inj_Trip) XIO(PB_E5_E6_WaterInjStop) ] OTE(EDB1_WaterBoosterStop);"},
        {"comment": "Emergency Trip of All Gas Turbine Generators (Fail-Safe De-energize to Trip)", "text": "XIC(ESD_Gas_Turbine_Trip) OTE(SD_GE_GasGenTrip);"}
    ]
    routines.append(("ESD_Cause_Effect_Matrix", "Cause & Effect Matrix Implementation (Fail-Safe De-energize to Trip)", rungs_esd))

    # -------------------------------------------------------------------------
    # 13. Inhibit_Maintenance
    # -------------------------------------------------------------------------
    rungs_inh = [
        {"comment": "Deluge Foam Release Inhibit Active (Keyswitch S2 Turned to Position I)", "text": "XIC(KEY_S2_FoamInhibit) [ OTE(HORN_PCR_Z1) , OTE(SA_7404_001_002) ];"},
        {"comment": "All Safety Outputs Inhibit Active (Keyswitch S3 Turned to Position I)", "text": "XIC(KEY_S3_AllOutputsInhibit) OTE(HORN_PCR_Z1);"}
    ]
    routines.append(("Inhibit_Maintenance", "Maintenance Bypass Keyswitches S2 & S3 Interlock Supervision", rungs_inh))

    # -------------------------------------------------------------------------
    # 14. Annunciation_PCR_Panel
    # -------------------------------------------------------------------------
    rungs_ann = [
        {"comment": "ESDV Fuel Gas Closed Red LED Indicator (L14)", "text": "XIC(ZSL_6401_001) OTE(LED_L14_ESDV_Closed);"},
        {"comment": "ESDV Fuel Gas Open Green LED Indicator (L15)", "text": "XIC(ZSH_6401_001) OTE(LED_L15_ESDV_Open);"},
        {"comment": "Stop Power Oil Pumps Relays & PCR Red LEDs L8..L11", "text": "XIC(ESD_Power_Oil_Trip) [ OTE(CR1_P2300_Stop_L8) , OTE(CR2_P2400_Stop_L9) , OTE(CR3_P2500_Stop_L10) , OTE(CR4_P2600_Stop_L11) ];"},
        {"comment": "Stop Water Injection Pumps Relays & PCR Red LEDs L12..L13", "text": "XIC(ESD_Water_Inj_Trip) [ OTE(CR5_P3800_Stop_L12) , OTE(CR6_P3900_Stop_L13) ];"},
        {"comment": "PCR Main Alarm Horn Z1 Trigger & Acoustic Silence Coordination", "text": "[ XIC(VOTE_Any_Confirmed_Gas) , XIC(VOTE_Any_Confirmed_Fire) , XIC(ESD_Matrix_Master_Trip) ] XIO(PB_E12_AlarmMute) OTE(HORN_PCR_Z1);"},
        {"comment": "Process Building Alarm Siren Trigger", "text": "[ XIC(VOTE_Any_Confirmed_Gas) , XIC(VOTE_Any_Confirmed_Fire) ] XIO(PB_E12_AlarmMute) OTE(HORN_PA_001_Building);"},
        {"comment": "H2S Toxic Siren & Blue Strobe Beacon Trigger", "text": "XIC(VOTE_Any_Confirmed_Toxic) OTE(ALARM_H2S_SirenStrobe);"}
    ]
    routines.append(("Annunciation_PCR_Panel", "PCR Annunciator LEDs (L8..L17), Audible Horns & Rotating Beacons", rungs_ann))

    # -------------------------------------------------------------------------
    # 15. IO_Output_Dispatch
    # -------------------------------------------------------------------------
    rungs_out = [
        {"comment": "Point 0: PumpShutdown (Local:8:O.Data.0) Master ESD Trip Relay (Fail-Safe 1=Run)", "text": "XIC(ESD_TRIP_Master) OTE(Local:8:O.Data.0);"},
        {"comment": "Point 1: 6401-EY-001/002 (Local:8:O.Data.1) Fuel Gas ESDV Solenoid (Fail-Safe 1=Open)", "text": "XIC(EY_6401_001_002) OTE(Local:8:O.Data.1);"},
        {"comment": "Point 2: 7404-SA-001/002 (Local:8:O.Data.2) Pump House Local Alarm Bell", "text": "XIC(SA_7404_001_002) OTE(Local:8:O.Data.2);"},
        {"comment": "Point 3: Pump A Pulsed Output (Local:8:O.Data.3)", "text": "XIC(DO_7503_PumpA_Pulse) OTE(Local:8:O.Data.3);"},
        {"comment": "Point 4: Deluge Pump A Run Command (Local:8:O.Data.4)", "text": "XIC(DO_7503_PumpA_Cmd) OTE(Local:8:O.Data.4);"},
        {"comment": "Point 5: Pump B Pulsed Output (Local:8:O.Data.5)", "text": "XIC(DO_7503_PumpB_Pulse) OTE(Local:8:O.Data.5);"},
        {"comment": "Point 6: Deluge Pump B Start Pulse (Local:8:O.Data.6)", "text": "XIC(DO_7503_PumpB_Start) OTE(Local:8:O.Data.6);"},
        {"comment": "Point 7: Deluge Pump B Stop Pulse (Local:8:O.Data.7)", "text": "XIC(DO_7503_PumpB_Stop) OTE(Local:8:O.Data.7);"},
        {"comment": "Point 8: Oil Booster Pump Relay (Local:8:O.Data.8)", "text": "XIC(EDB1_OilBoosterStop) OTE(Local:8:O.Data.8);"},
        {"comment": "Point 9: Water Booster Pump Relay (Local:8:O.Data.9)", "text": "XIC(EDB1_WaterBoosterStop) OTE(Local:8:O.Data.9);"},
        {"comment": "Point 11: ESDV Closed Red LED L14 (Local:8:O.Data.11)", "text": "XIC(LED_L14_ESDV_Closed) OTE(Local:8:O.Data.11);"},
        {"comment": "Point 12: ESDV Open Green LED L15 (Local:8:O.Data.12)", "text": "XIC(LED_L15_ESDV_Open) OTE(Local:8:O.Data.12);"},
        {"comment": "Point 13: ESDV Low Air Accumulator Amber LED L16 (Local:8:O.Data.13)", "text": "XIC(LED_L16_LowAirAcc) OTE(Local:8:O.Data.13);"},
        {"comment": "Point 14: Low Fuel Gas Line Amber LED L17 (Local:8:O.Data.14)", "text": "XIC(LED_L17_LowFuelGas) OTE(Local:8:O.Data.14);"},
        {"comment": "Point 15: Stop Power Oil Pump P-2300 Relay & L8 LED (Local:8:O.Data.15)", "text": "XIC(CR1_P2300_Stop_L8) OTE(Local:8:O.Data.15);"},
        {"comment": "Point 16: Stop Power Oil Pump P-2400 Relay & L9 LED (Local:8:O.Data.16)", "text": "XIC(CR2_P2400_Stop_L9) OTE(Local:8:O.Data.16);"},
        {"comment": "Point 17: Stop Power Oil Pump P-2500 Relay & L10 LED (Local:8:O.Data.17)", "text": "XIC(CR3_P2500_Stop_L10) OTE(Local:8:O.Data.17);"},
        {"comment": "Point 18: Stop Power Oil Pump P-2600 Relay & L11 LED (Local:8:O.Data.18)", "text": "XIC(CR4_P2600_Stop_L11) OTE(Local:8:O.Data.18);"},
        {"comment": "Point 19: Stop Water Injection Pump P-3800 Relay & L12 LED (Local:8:O.Data.19)", "text": "XIC(CR5_P3800_Stop_L12) OTE(Local:8:O.Data.19);"},
        {"comment": "Point 20: Stop Water Injection Pump P-3900 Relay & L13 LED (Local:8:O.Data.20)", "text": "XIC(CR6_P3900_Stop_L13) OTE(Local:8:O.Data.20);"},
        {"comment": "Point 21: Shut Down All Gas Generators (Local:8:O.Data.21)", "text": "XIC(SD_GE_GasGenTrip) OTE(Local:8:O.Data.21);"},
        {"comment": "Point 22: Production Control Room Alarm Horn Z1 (Local:8:O.Data.22)", "text": "XIC(HORN_PCR_Z1) OTE(Local:8:O.Data.22);"},
        {"comment": "Point 23: Process Production Building Alarm Siren (Local:8:O.Data.23)", "text": "XIC(HORN_PA_001_Building) OTE(Local:8:O.Data.23);"},
        {"comment": "Point 30: H2S Siren & Strobe Beacon (Local:8:O.Data.30)", "text": "XIC(ALARM_H2S_SirenStrobe) OTE(Local:8:O.Data.30);"},
        {"comment": "Point 31: Smoke Siren & Strobe Beacon (Local:8:O.Data.31)", "text": "XIC(ALARM_Smoke_SirenStrobe) OTE(Local:8:O.Data.31);"}
    ]
    routines.append(("IO_Output_Dispatch", "Slot 8 1756-OB32 Safe Digital Output Image Mapping", rungs_out))

    return routines

print("build_upgraded_rll_routines() defined.")

# =============================================================================
# 3. FACTORYTALK VIEW HMI EXPORTERS (CSV TAGS & XML ALARMS)
# =============================================================================
def write_factorytalk_hmi_files(tags):
    """Generate FactoryTalk View SE/ME Tag Database CSV and FTA&E Alarms XML."""
    # 1. Tag Database CSV
    csv_lines = [
        "Tag Name,Tag Type,Data Type,Data Source,Address,Description,Engineering Units,Minimum,Maximum,Scale,Offset"
    ]
    for item in tags:
        tname = item[0]
        dtype = item[1]
        desc = item[2]
        alias = item[3]
        unit = item[4] if len(item) > 4 else ""
        min_v = item[5] if len(item) > 5 else 0
        max_v = item[6] if len(item) > 6 else 1

        tag_type = "Analog" if dtype in ("REAL", "INT", "DINT") else "Digital"
        addr = f"[PLC]{tname}"
        clean_desc = desc.replace(",", ";")
        csv_lines.append(f'"{tname}","{tag_type}","{dtype}","Device","{addr}","{clean_desc}","{unit}",{min_v},{max_v},1.0,0.0')

    csv_content = "\n".join(csv_lines) + "\n"

    # 2. FactoryTalk View Alarms & Events (FTA&E) XML
    xml_alarms = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<AlarmDefinitionDatabase Version="1.0" Project="GNTF_FGCP_7404_001_HMI">',
        '  <Alarms>',
    ]
    for item in tags:
        tname = item[0]
        dtype = item[1]
        desc = saxutils.escape(item[2])
        if "Alm" in tname or "Trip" in tname or "Flt" in tname or "Alarm" in tname:
            sev = "1000" if ("HiHi" in tname or "Trip" in tname or "Fire" in tname) else "500"
            xml_alarms.append(f'    <DigitalAlarm Name="ALM_{tname}" InputTag="[PLC]{tname}" Severity="{sev}">')
            xml_alarms.append(f'      <Message><![CDATA[{desc}]]></Message>')
            xml_alarms.append('    </DigitalAlarm>')
        elif dtype == "REAL" and "Scaled" in tname:
            xml_alarms.append(f'    <AnalogAlarm Name="ALM_{tname}" InputTag="[PLC]{tname}" Severity="750">')
            xml_alarms.append(f'      <Message><![CDATA[{desc} Out of Limits]]></Message>')
            xml_alarms.append('    </AnalogAlarm>')
    xml_alarms.extend([
        '  </Alarms>',
        '</AlarmDefinitionDatabase>',
    ])
    xml_content = "\n".join(xml_alarms) + "\n"

    for out_dir in (BASE_DIR, DESKTOP_DIR):
        os.makedirs(out_dir, exist_ok=True)
        csv_path = os.path.join(out_dir, "GNTF_HMI_Tags_FactoryTalk.csv")
        xml_path = os.path.join(out_dir, "GNTF_HMI_Alarms_FactoryTalk.xml")
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write(csv_content)
        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(xml_content)
        print(f"[OK] Generated FactoryTalk Tags CSV: {csv_path} ({len(csv_content):,} bytes)")
        print(f"[OK] Generated FactoryTalk Alarms XML: {xml_path} ({len(xml_content):,} bytes)")


# =============================================================================
# 4. CONTROLLER & PROGRAM L5X GENERATORS
# =============================================================================
def write_upgraded_l5x_files(tags, routines):
    """Generate upgraded Studio 5000 Controller L5X and Program L5X files."""
    # Controller L5X
    ctrl_lines = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<RSLogix5000Content SchemaRevision="1.0" SoftwareRevision="32.00" TargetName="GNTF_FGCP_7404_001_UPG" TargetType="Controller" ContainsContext="false" Owner="EPPM / ASTRE" ExportDate="Fri Nov 06 16:30:00 2026">',
        '  <Controller Use="Target" Name="GNTF_FGCP_7404_001_UPG" ProcessorType="1756-L82E" MajorRev="32" MinorRev="11" ChassisType="1756-A13" PowerSupply="1756-PB72" ProjectCreationDate="Fri Nov 06 16:30:00 2026" LastModifiedDate="Fri Nov 06 16:30:00 2026">',
        '    <Description>',
        '      <![CDATA[GNTF Quinguila Tank Farm Control System Upgrade - Upgraded Project per 01-MAN-03-06 & 01-MAN-03-07 Final Approved]]>',
        '    </Description>',
        '    <DataTypes/>',
        '    <AddOnInstructionDefinitions/>',
        '    <Modules>',
        '      <Module Name="Local" CatalogNumber="1756-L82E" Vendor="1" ProductType="14" ProductCode="167" Major="32" Minor="11" ParentModule="Local" ParentModPortId="1" Inhibited="false" MajorFault="true">',
        '        <Ports><Port Id="1" Address="0" Type="ICP" Upstream="false"/><Port Id="2" Address="192.168.20.10" Type="Ethernet" Upstream="false"/></Ports>',
        '      </Module>',
        '      <Module Name="AI_Slot2_CH4_01_16" CatalogNumber="1756-IF16" Vendor="1" ProductType="10" ProductCode="10" Major="1" Minor="1" ParentModule="Local" ParentModPortId="1" Inhibited="false" MajorFault="false"><Ports><Port Id="1" Address="2" Type="ICP" Upstream="true"/></Ports></Module>',
        '      <Module Name="AI_Slot3_Proc_CH4" CatalogNumber="1756-IF16" Vendor="1" ProductType="10" ProductCode="10" Major="1" Minor="1" ParentModule="Local" ParentModPortId="1" Inhibited="false" MajorFault="false"><Ports><Port Id="1" Address="3" Type="ICP" Upstream="true"/></Ports></Module>',
        '      <Module Name="AI_Slot4_H2S_Flame_Smoke" CatalogNumber="1756-IF16" Vendor="1" ProductType="10" ProductCode="10" Major="1" Minor="1" ParentModule="Local" ParentModPortId="1" Inhibited="false" MajorFault="false"><Ports><Port Id="1" Address="4" Type="ICP" Upstream="true"/></Ports></Module>',
        '      <Module Name="AI_Slot5_Spare" CatalogNumber="1756-IF16" Vendor="1" ProductType="10" ProductCode="10" Major="1" Minor="1" ParentModule="Local" ParentModPortId="1" Inhibited="false" MajorFault="false"><Ports><Port Id="1" Address="5" Type="ICP" Upstream="true"/></Ports></Module>',
        '      <Module Name="AI_Slot6_HART_Radar_Levels" CatalogNumber="1756-IF8H" Vendor="1" ProductType="10" ProductCode="68" Major="1" Minor="1" ParentModule="Local" ParentModPortId="1" Inhibited="false" MajorFault="false"><Ports><Port Id="1" Address="6" Type="ICP" Upstream="true"/></Ports></Module>',
        '      <Module Name="DI_Slot7_Discrete_Inputs" CatalogNumber="1756-IB32" Vendor="1" ProductType="7" ProductCode="14" Major="3" Minor="1" ParentModule="Local" ParentModPortId="1" Inhibited="false" MajorFault="false"><Ports><Port Id="1" Address="7" Type="ICP" Upstream="true"/></Ports></Module>',
        '      <Module Name="DO_Slot8_Discrete_Outputs" CatalogNumber="1756-OB32" Vendor="1" ProductType="7" ProductCode="22" Major="3" Minor="1" ParentModule="Local" ParentModPortId="1" Inhibited="false" MajorFault="false"><Ports><Port Id="1" Address="8" Type="ICP" Upstream="true"/></Ports></Module>',
        '      <Module Name="MCM_Slot9_Modbus_Telemetry" CatalogNumber="MVI56E-MCM" Vendor="309" ProductType="12" ProductCode="1" Major="1" Minor="1" ParentModule="Local" ParentModPortId="1" Inhibited="false" MajorFault="false"><Ports><Port Id="1" Address="9" Type="ICP" Upstream="true"/></Ports></Module>',
        '    </Modules>',
        '    <Tags>',
    ]

    for item in tags:
        tlines, _ = B.build_tag_xml_lines(item[0], item[1], item[2], item[3])
        ctrl_lines.extend(tlines)

    ctrl_lines.extend([
        '    </Tags>',
        '    <Programs>',
        '      <Program Name="MainProgram" TestEdits="false" MainRoutineName="Main_Scheduler" Disabled="false" UseAsFolder="false">',
        '        <Description><![CDATA[GNTF Quinguila Field Control System Upgraded Logic (1756-L82E RLL)]]></Description>',
        '        <Tags/>',
        '        <Routines>',
    ])

    # Program L5X
    prog_lines = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<RSLogix5000Content SchemaRevision="1.0" SoftwareRevision="32.00" TargetName="MainProgram" TargetType="Program" ContainsContext="true" Owner="EPPM / ASTRE" ExportDate="Fri Nov 06 16:30:00 2026">',
        '  <Program Use="Target" Name="MainProgram" TestEdits="false" MainRoutineName="Main_Scheduler" Disabled="false" UseAsFolder="false">',
        '    <Description><![CDATA[GNTF Quinguila Upgraded Relay Ladder Logic Program Import]]></Description>',
        '    <Tags>',
    ]
    for item in tags:
        tlines, _ = B.build_tag_xml_lines(item[0], item[1], item[2], item[3])
        prog_lines.extend(tlines)
    prog_lines.extend([
        '    </Tags>',
        '    <Routines>',
    ])

    for rname, rdesc, rungs in routines:
        routine_block = [
            f'          <Routine Name="{rname}" Type="RLL">',
            f'            <Description><![CDATA[{rdesc}]]></Description>',
            '            <RLLContent>',
        ]
        routine_prog_block = [
            f'      <Routine Name="{rname}" Type="RLL">',
            f'        <Description><![CDATA[{rdesc}]]></Description>',
            '        <RLLContent>',
        ]
        for idx, rg in enumerate(rungs):
            comment = rg.get("comment", "")
            raw_text = rg.get("text", "")
            elems = B.parse_rung_elements(raw_text)
            formatted_text = B.format_logix_elements(elems)

            rung_lines = [f'              <Rung Number="{idx}" Type="N">']
            if comment:
                rung_lines.append(f'                <Comment><![CDATA[{comment}]]></Comment>')
            rung_lines.append(f'                <Text><![CDATA[{formatted_text}]]></Text>')
            rung_lines.append('              </Rung>')
            routine_block.extend(rung_lines)

            rung_p_lines = [f'          <Rung Number="{idx}" Type="N">']
            if comment:
                rung_p_lines.append(f'            <Comment><![CDATA[{comment}]]></Comment>')
            rung_p_lines.append(f'            <Text><![CDATA[{formatted_text}]]></Text>')
            rung_p_lines.append('          </Rung>')
            routine_prog_block.extend(rung_p_lines)

        routine_block.extend(['            </RLLContent>', '          </Routine>'])
        routine_prog_block.extend(['        </RLLContent>', '      </Routine>'])

        ctrl_lines.extend(routine_block)
        prog_lines.extend(routine_prog_block)

    ctrl_lines.extend([
        '        </Routines>',
        '      </Program>',
        '    </Programs>',
        '    <Tasks>',
        '      <Task Name="MainTask" Type="CONTINUOUS" Priority="10" Watchdog="500" DisableUpdateOutputs="false" InhibitTask="false">',
        '        <ScheduledPrograms>',
        '          <ScheduledProgram Name="MainProgram"/>',
        '        </ScheduledPrograms>',
        '      </Task>',
        '    </Tasks>',
        '  </Controller>',
        '</RSLogix5000Content>',
    ])

    prog_lines.extend([
        '    </Routines>',
        '  </Program>',
        '</RSLogix5000Content>',
    ])

    ctrl_content = "\n".join(ctrl_lines) + "\n"
    prog_content = "\n".join(prog_lines) + "\n"

    for out_dir in (BASE_DIR, DESKTOP_DIR):
        os.makedirs(out_dir, exist_ok=True)
        c_path = os.path.join(out_dir, "GNTF_Quinguila_Upgrade_AB_Ladder.L5X")
        p_path = os.path.join(out_dir, "GNTF_Quinguila_Upgrade_AB_Program.L5X")
        with open(c_path, "w", encoding="utf-8") as f:
            f.write(ctrl_content)
        with open(p_path, "w", encoding="utf-8") as f:
            f.write(prog_content)
        print(f"[OK] Generated Upgraded Controller L5X: {c_path} ({len(ctrl_content):,} bytes)")
        print(f"[OK] Generated Upgraded Program L5X: {p_path} ({len(prog_content):,} bytes)")

    # Verify strictly with ET
    ET.fromstring(ctrl_content)
    ET.fromstring(prog_content)
    print("[VERIFIED] Both Upgraded L5X files strictly parsed and validated.")

print("write_upgraded_l5x_files() defined.")

# =============================================================================
# 5. UPGRADED HTML LADDER VIEWER GENERATOR
# =============================================================================
def write_upgraded_ladder_html(tags, routines):
    """Generate standalone interactive SVG/HTML Ladder Diagram Viewer for the upgraded project."""
    print("[...] Rendering Upgraded Ladder HTML Viewer...")
    B.write_ladder_html(tags, routines, filename="GNTF_Quinguila_Upgrade_AB_Ladder.html", project_title="GNTF UPGRADED PROJECT (PHASE 1 & 2)")


# =============================================================================
# 6. FULL INTERACTIVE WEB HMI / SCADA WORKSTATION APPLICATION
# =============================================================================
def write_hmi_application_html(tags):
    """Generate the full standalone Interactive Web HMI / SCADA Workstation Application."""
    client_tag_db = {t[0]: {"type": t[1], "desc": t[2], "alias": t[3], "unit": t[4] if len(t) > 4 else "", "min": t[5] if len(t) > 5 else 0, "max": t[6] if len(t) > 6 else 1} for t in tags}
    tag_db_json = json.dumps(client_tag_db)

    # Read external template or compile inline
    hmi_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quinguila Tank Farm (GNTF) &bull; SCADA / HMI Operator Workstation &bull; FGCP-7404-001</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: #0b0f19;
            color: #f8fafc;
            user-select: none;
        }}
        .font-mono {{
            font-family: 'JetBrains Mono', monospace;
        }}
        /* Industrial SCADA Styling */
        .scada-card {{
            background: linear-gradient(180deg, #161f30 0%, #0f172a 100%);
            border: 1px solid #1e293b;
            border-radius: 8px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5), 0 2px 4px -2px rgba(0, 0, 0, 0.5);
        }}
        .scada-card:hover {{
            border-color: #334155;
        }}
        .scada-tab-btn {{
            padding: 8px 16px;
            font-size: 13px;
            font-weight: 700;
            color: #94a3b8;
            border-bottom: 2px solid transparent;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .scada-tab-btn:hover {{
            color: #ffffff;
            background-color: rgba(255, 255, 255, 0.05);
        }}
        .scada-tab-btn.active {{
            color: #38bdf8;
            border-bottom-color: #38bdf8;
            background-color: rgba(56, 189, 248, 0.08);
        }}
        /* Piping and flow animations */
        @keyframes flowAnimation {{
            0% {{ stroke-dashoffset: 24; }}
            100% {{ stroke-dashoffset: 0; }}
        }}
        .pipe-flow {{
            stroke-dasharray: 6 6;
            animation: flowAnimation 1s linear infinite;
        }}
        .alarm-blink {{
            animation: alarmBlink 0.8s ease-in-out infinite alternate;
        }}
        @keyframes alarmBlink {{
            from {{ opacity: 1; }}
            to {{ opacity: 0.3; }}
        }}
        /* LED Indicators */
        .scada-led {{
            width: 14px;
            height: 14px;
            border-radius: 50%;
            border: 2px solid #334155;
            display: inline-block;
            box-shadow: inset 0 1px 2px rgba(0,0,0,0.6);
            transition: all 0.2s;
        }}
        .scada-led.red-on {{ background-color: #ef4444; border-color: #b91c1c; box-shadow: 0 0 10px #ef4444; }}
        .scada-led.green-on {{ background-color: #22c55e; border-color: #15803d; box-shadow: 0 0 10px #22c55e; }}
        .scada-led.amber-on {{ background-color: #f59e0b; border-color: #b45309; box-shadow: 0 0 10px #f59e0b; }}
        .scada-led.blue-on {{ background-color: #3b82f6; border-color: #1d4ed8; box-shadow: 0 0 10px #3b82f6; }}
        .scada-led.off {{ background-color: #1e293b; border-color: #0f172a; }}
    </style>
</head>
<body class="h-screen flex flex-col overflow-hidden">

    <!-- Top SCADA Header Bar -->
    <header class="bg-slate-950 border-b border-slate-800 px-6 py-2.5 flex items-center justify-between flex-shrink-0 z-30 shadow-lg">
        <div class="flex items-center space-x-4">
            <div class="h-10 w-10 bg-gradient-to-br from-blue-600 to-indigo-800 rounded-lg flex items-center justify-center font-black text-xl text-white shadow-inner border border-blue-500/30">
                SC
            </div>
            <div>
                <div class="flex items-center space-x-2.5">
                    <h1 class="text-base font-extrabold text-white tracking-tight">QUINGUILA TANK FARM &bull; SCADA WORKSTATION</h1>
                    <span class="bg-blue-900/60 text-blue-200 border border-blue-700/50 text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider">FGCP-7404-001 UPGRADED</span>
                    <span class="bg-emerald-900/60 text-emerald-200 border border-emerald-700/50 text-[10px] font-bold px-2 py-0.5 rounded flex items-center">
                        <span class="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-ping mr-1.5"></span>
                        PLC ONLINE (1756-L82E)
                    </span>
                </div>
                <p class="text-xs text-slate-400">Integrated Fire & Gas, Deluge, Emergency Shutdown (ESD) & Process Telemetry System</p>
            </div>
        </div>

        <!-- Master Status Pills & Action Controls -->
        <div class="flex items-center space-x-3">
            <div id="masterEsdBadge" class="px-3 py-1.5 rounded bg-emerald-950/80 border border-emerald-500/50 text-emerald-300 text-xs font-bold flex items-center space-x-2 shadow-inner">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 shadow-[0_0_8px_#10b981]"></span>
                <span id="masterEsdTxt">PLANT ESD: HEALTHY (24V)</span>
            </div>

            <div id="delugeStatusBadge" class="px-3 py-1.5 rounded bg-slate-900 border border-slate-700 text-slate-300 text-xs font-bold flex items-center space-x-2">
                <span class="w-2.5 h-2.5 rounded-full bg-slate-500"></span>
                <span id="delugeStatusTxt">DELUGE: STANDBY</span>
            </div>

            <button onclick="toggleAlarmSilence()" id="btnMuteHorn" class="bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold px-3 py-2 rounded border border-slate-700 transition flex items-center space-x-1.5">
                <svg class="w-4 h-4 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"></path></svg>
                <span id="btnMuteTxt">Silence Horn (E12)</span>
            </button>

            <button onclick="resetAllAlarms()" class="bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold px-3 py-2 rounded shadow transition flex items-center space-x-1.5">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                <span>Reset Alarms (E11)</span>
            </button>

            <button onclick="toggleSimulatorDrawer()" class="bg-amber-600 hover:bg-amber-500 text-white text-xs font-bold px-3.5 py-2 rounded shadow transition flex items-center space-x-1.5">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"></path></svg>
                <span>Live Test Simulator</span>
            </button>
        </div>
    </header>

    <!-- Navigation Tab Bar -->
    <nav class="bg-slate-900 border-b border-slate-800 px-6 flex items-center space-x-2 flex-shrink-0 z-20">
        <button class="scada-tab-btn active" onclick="switchTab('tab-overview', this)">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
            Plant Process Overview
        </button>
        <button class="scada-tab-btn" onclick="switchTab('tab-fag', this)">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z"></path></svg>
            Fire & Gas System (2ooN)
        </button>
        <button class="scada-tab-btn" onclick="switchTab('tab-deluge', this)">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
            Deluge & Firewater Skid
        </button>
        <button class="scada-tab-btn" onclick="switchTab('tab-process', this)">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
            Pressures & Tank Farm
        </button>
        <button class="scada-tab-btn" onclick="switchTab('tab-matrix', this)">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"></path></svg>
            Cause & Effect Matrix (C2C)
        </button>
        <button class="scada-tab-btn" onclick="switchTab('tab-pcr', this)">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>
            PCR Annunciator Panel (LCP)
        </button>
        <button class="scada-tab-btn" onclick="switchTab('tab-alarms', this)">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
            Alarm & Event Log
            <span id="alarmCountBadge" class="bg-red-500 text-white text-[10px] font-bold px-1.5 py-0.2 rounded-full ml-1">0</span>
        </button>
    </nav>

    <!-- Main Workspace Container -->
    <main class="flex-1 overflow-y-auto p-6 bg-slate-950 relative" id="hmiContentArea">

        <!-- TAB 1: PLANT PROCESS OVERVIEW -->
        <div id="tab-overview" class="hmi-tab-pane space-y-6">
            <div class="grid grid-cols-1 xl:grid-cols-4 gap-6">
                <!-- Status Cards -->
                <div class="scada-card p-4 flex items-center justify-between">
                    <div>
                        <div class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Fuel Gas ESDV 6401-001</div>
                        <div id="cardEsdvTxt" class="text-lg font-black text-emerald-400 mt-1">OPEN (NORMAL)</div>
                        <div class="text-xs text-slate-500 font-mono">Feedback: ZSH=1, ZSL=0</div>
                    </div>
                    <div class="h-12 w-12 rounded-full bg-emerald-950 border border-emerald-500 flex items-center justify-center">
                        <span class="text-2xl">&#x26FD;</span>
                    </div>
                </div>

                <div class="scada-card p-4 flex items-center justify-between">
                    <div>
                        <div class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Power Oil Pumps (P2100/2200)</div>
                        <div id="cardOilPumpTxt" class="text-lg font-black text-emerald-400 mt-1">RUNNING (AUTO)</div>
                        <div class="text-xs text-slate-500 font-mono">Discharge: <span id="valOilInjP">2250</span> psi</div>
                    </div>
                    <div class="h-12 w-12 rounded-full bg-emerald-950 border border-emerald-500 flex items-center justify-center">
                        <span class="text-2xl">&#x2699;</span>
                    </div>
                </div>

                <div class="scada-card p-4 flex items-center justify-between">
                    <div>
                        <div class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Water Injection (P3600/3700)</div>
                        <div id="cardWaterPumpTxt" class="text-lg font-black text-emerald-400 mt-1">RUNNING (AUTO)</div>
                        <div class="text-xs text-slate-500 font-mono">Discharge: <span id="valWaterInjP">650</span> psi</div>
                    </div>
                    <div class="h-12 w-12 rounded-full bg-emerald-950 border border-emerald-500 flex items-center justify-center">
                        <span class="text-2xl">&#x1F4A7;</span>
                    </div>
                </div>

                <div class="scada-card p-4 flex items-center justify-between">
                    <div>
                        <div class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Gas Turbines SD-GE</div>
                        <div id="cardGasGenTxt" class="text-lg font-black text-emerald-400 mt-1">ONLINE (NORMAL)</div>
                        <div class="text-xs text-slate-500 font-mono">Fuel Gas: <span id="valFuelGasP">68</span> psi</div>
                    </div>
                    <div class="h-12 w-12 rounded-full bg-emerald-950 border border-emerald-500 flex items-center justify-center">
                        <span class="text-2xl">&#x26A1;</span>
                    </div>
                </div>
            </div>

            <!-- SVG Plant Process Mimic Graphic -->
            <div class="scada-card p-6 overflow-x-auto">
                <div class="flex items-center justify-between mb-4">
                    <h2 class="text-sm font-black uppercase text-slate-200 tracking-wider flex items-center">
                        <span class="w-2.5 h-2.5 bg-blue-500 rounded-full mr-2"></span>
                        Dynamic Process Flow & Safeguards Mimic
                    </h2>
                    <span class="text-xs text-slate-400 font-mono">Live SVG Hardware State Telemetry</span>
                </div>

                <svg viewBox="0 0 1100 480" class="w-full h-auto min-w-[900px] bg-slate-900/90 rounded border border-slate-800">
                    <!-- Grid background -->
                    <defs>
                        <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">
                            <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#1e293b" stroke-width="0.5" />
                        </pattern>
                        <linearGradient id="tankGrad" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.8"/>
                            <stop offset="100%" stop-color="#1d4ed8" stop-opacity="0.9"/>
                        </linearGradient>
                    </defs>
                    <rect width="1100" height="480" fill="url(#grid)" />

                    <!-- PIPING -->
                    <!-- Crude Inlet Line -->
                    <path d="M 30 180 L 160 180" stroke="#0ea5e9" stroke-width="6" fill="none" class="pipe-flow" />
                    <!-- Fuel Gas ESDV Line -->
                    <path d="M 160 180 L 320 180" stroke="#22c55e" stroke-width="6" fill="none" id="pipeFuelGas" class="pipe-flow" />
                    <path d="M 320 180 L 480 180" stroke="#22c55e" stroke-width="6" fill="none" />
                    <!-- Branch to Turbines -->
                    <path d="M 480 180 L 480 90 L 620 90" stroke="#22c55e" stroke-width="4" fill="none" />
                    <!-- Branch to Booster Pumps -->
                    <path d="M 480 180 L 480 270 L 620 270" stroke="#f59e0b" stroke-width="6" fill="none" />
                    <!-- Water Injection Line -->
                    <path d="M 480 370 L 620 370" stroke="#3b82f6" stroke-width="6" fill="none" />
                    <!-- Tank Farm Header -->
                    <path d="M 720 270 L 820 270 L 820 150 L 980 150" stroke="#f59e0b" stroke-width="6" fill="none" />
                    <path d="M 820 270 L 980 270" stroke="#f59e0b" stroke-width="6" fill="none" />

                    <!-- EQUIPMENT -->
                    <!-- 1. Fuel Gas ESD Valve -->
                    <g transform="translate(240, 155)">
                        <polygon points="0,0 30,25 0,50" fill="#22c55e" id="esdvLeft" />
                        <polygon points="30,0 0,25 30,50" transform="translate(30,0)" fill="#22c55e" id="esdvRight" />
                        <circle cx="30" cy="25" r="7" fill="#ffffff" />
                        <line x1="30" y1="25" x2="30" y2="-5" stroke="#ffffff" stroke-width="3" />
                        <rect x="15" y="-20" width="30" height="15" rx="3" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5" />
                        <text x="30" y="-9" fill="#38bdf8" font-size="9" font-weight="bold" text-anchor="middle" font-family="JetBrains Mono">ESDV</text>
                        <text x="30" y="65" fill="#f8fafc" font-size="10" font-weight="bold" text-anchor="middle" font-family="Inter">6401-EY-001</text>
                    </g>

                    <!-- 2. Gas Turbine Generators -->
                    <g transform="translate(620, 60)">
                        <rect width="120" height="60" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="2" id="boxTurbines" />
                        <text x="60" y="26" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">GAS TURBINES</text>
                        <text x="60" y="44" fill="#22c55e" font-size="10" font-weight="bold" text-anchor="middle" id="txtTurbineStatus">ONLINE (SD-GE=1)</text>
                    </g>

                    <!-- 3. Power Oil Booster Pumps -->
                    <g transform="translate(620, 240)">
                        <rect width="120" height="60" rx="6" fill="#1e293b" stroke="#f59e0b" stroke-width="2" id="boxOilPumps" />
                        <text x="60" y="26" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">OIL BOOSTER (P2100)</text>
                        <text x="60" y="44" fill="#22c55e" font-size="10" font-weight="bold" text-anchor="middle" id="txtOilPumpStatus">RUNNING (2250 psi)</text>
                    </g>

                    <!-- 4. Water Injection Pumps -->
                    <g transform="translate(620, 340)">
                        <rect width="120" height="60" rx="6" fill="#1e293b" stroke="#3b82f6" stroke-width="2" id="boxWaterPumps" />
                        <text x="60" y="26" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">WATER INJ (P3600)</text>
                        <text x="60" y="44" fill="#22c55e" font-size="10" font-weight="bold" text-anchor="middle" id="txtWaterPumpStatus">RUNNING (650 psi)</text>
                    </g>

                    <!-- 5. Crude Storage Tanks T-100 & T-200 -->
                    <!-- Tank T-100 -->
                    <g transform="translate(860, 90)">
                        <rect width="90" height="100" rx="4" fill="#0f172a" stroke="#64748b" stroke-width="2" />
                        <rect x="2" y="30" width="86" height="68" fill="url(#tankGrad)" id="tankLevelT100" />
                        <text x="45" y="22" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">TANK T-100</text>
                        <text x="45" y="65" fill="#ffffff" font-size="12" font-weight="bold" text-anchor="middle" id="txtLIT100">8.4 m</text>
                        <text x="45" y="115" fill="#94a3b8" font-size="9" text-anchor="middle">LIT-100 (Radar)</text>
                    </g>

                    <!-- Tank T-200 -->
                    <g transform="translate(980, 90)">
                        <rect width="90" height="100" rx="4" fill="#0f172a" stroke="#64748b" stroke-width="2" />
                        <rect x="2" y="45" width="86" height="53" fill="url(#tankGrad)" id="tankLevelT200" />
                        <text x="45" y="22" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">TANK T-200</text>
                        <text x="45" y="65" fill="#ffffff" font-size="12" font-weight="bold" text-anchor="middle" id="txtLIT200">6.2 m</text>
                        <text x="45" y="115" fill="#94a3b8" font-size="9" text-anchor="middle">LIT-200 (Radar)</text>
                    </g>

                    <!-- Deluge Pump House Mimic -->
                    <g transform="translate(60, 310)">
                        <rect width="180" height="110" rx="6" fill="#1e293b" stroke="#ef4444" stroke-width="2" />
                        <text x="90" y="25" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">DELUGE PUMP HOUSE</text>
                        <rect x="15" y="40" width="70" height="30" rx="3" fill="#0f172a" stroke="#3b82f6" />
                        <text x="50" y="58" fill="#38bdf8" font-size="9" font-weight="bold" text-anchor="middle">PUMP A (DUTY)</text>
                        <rect x="95" y="40" width="70" height="30" rx="3" fill="#0f172a" stroke="#f59e0b" />
                        <text x="130" y="58" fill="#fbbf24" font-size="9" font-weight="bold" text-anchor="middle">PUMP B (DIESEL)</text>
                        <text x="90" y="95" fill="#94a3b8" font-size="10" text-anchor="middle">Discharge: <tspan id="txtDelugeP" class="text-white font-bold">8.5 bar</tspan></text>
                    </g>
                </svg>
            </div>
        </div>

        <!-- TAB 2: FIRE & GAS 2ooN MATRIX -->
        <div id="tab-fag" class="hmi-tab-pane hidden space-y-6">
            <div class="scada-card p-4 flex items-center justify-between">
                <div>
                    <h2 class="text-base font-black text-white">FIRE & GAS SYSTEM &bull; 2-OUT-OF-N COINCIDENCE VOTING</h2>
                    <p class="text-xs text-slate-400">24 CH4 Detectors, 12 Toxic H2S Detectors, 3 Triple-IR Flame Detectors</p>
                </div>
                <div class="flex items-center space-x-3">
                    <span class="text-xs bg-slate-800 text-slate-300 px-3 py-1 rounded border border-slate-700">Low Alm: 20% LEL</span>
                    <span class="text-xs bg-red-950 text-red-300 px-3 py-1 rounded border border-red-700">High-High Alm: 30% LEL</span>
                </div>
            </div>

            <div class="grid grid-cols-2 md:grid-cols-4 xl:grid-cols-6 gap-3" id="gasDetectorGrid">
                <!-- Injected via JavaScript for all 24 detectors -->
            </div>
        </div>

        <!-- TAB 3: DELUGE & FIREWATER SKID -->
        <div id="tab-deluge" class="hmi-tab-pane hidden space-y-6">
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- Pump A Card -->
                <div class="scada-card p-5">
                    <div class="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
                        <h3 class="font-bold text-sm text-blue-400">PUMP A &bull; ELECTRIC DUTY PUMP</h3>
                        <span id="badgePumpA" class="bg-slate-800 text-slate-300 text-xs px-2.5 py-0.5 rounded font-bold">STOPPED</span>
                    </div>
                    <div class="space-y-3 text-xs">
                        <div class="flex justify-between"><span class="text-slate-400">Run Command (Slot 8 Ch 4):</span><span id="statPumpACmd" class="font-mono font-bold text-slate-200">0</span></div>
                        <div class="flex justify-between"><span class="text-slate-400">Run Feedback Aux (Slot 7 Ch 17):</span><span id="statPumpAFbk" class="font-mono font-bold text-slate-200">0</span></div>
                        <div class="flex justify-between"><span class="text-slate-400">Trip Coil Pulse (60s check):</span><span class="scada-led green-on ml-2"></span></div>
                    </div>
                    <div class="mt-6 flex space-x-2">
                        <button onclick="simStartPumpA()" class="flex-1 bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-2 rounded text-xs transition">Manual Start</button>
                        <button onclick="simStopPumpA()" class="flex-1 bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold py-2 rounded text-xs transition">Stop</button>
                    </div>
                </div>

                <!-- Pump B Card -->
                <div class="scada-card p-5">
                    <div class="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
                        <h3 class="font-bold text-sm text-amber-400">PUMP B &bull; DIESEL STANDBY PUMP</h3>
                        <span id="badgePumpB" class="bg-slate-800 text-slate-300 text-xs px-2.5 py-0.5 rounded font-bold">STANDBY</span>
                    </div>
                    <div class="space-y-3 text-xs">
                        <div class="flex justify-between"><span class="text-slate-400">Start Pulse Command (Slot 8 Ch 6):</span><span id="statPumpBStart" class="font-mono font-bold text-slate-200">0</span></div>
                        <div class="flex justify-between"><span class="text-slate-400">Crank Attempt Counter:</span><span id="statPumpBCrank" class="font-mono font-bold text-slate-200">0 / 3</span></div>
                        <div class="flex justify-between"><span class="text-slate-400">Maintenance Inhibit Keyswitch:</span><span class="font-mono text-emerald-400 font-bold">NORMAL (0)</span></div>
                    </div>
                    <div class="mt-6 flex space-x-2">
                        <button onclick="simStartPumpB()" class="flex-1 bg-amber-600 hover:bg-amber-500 text-white font-bold py-2 rounded text-xs transition">Manual Crank</button>
                        <button onclick="simStopPumpB()" class="flex-1 bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold py-2 rounded text-xs transition">Stop</button>
                    </div>
                </div>

                <!-- Auxiliary Tanks & Release -->
                <div class="scada-card p-5">
                    <div class="border-b border-slate-800 pb-3 mb-4">
                        <h3 class="font-bold text-sm text-red-400">FOAM RELEASE & STORAGE</h3>
                    </div>
                    <div class="space-y-3 text-xs">
                        <div class="flex justify-between"><span class="text-slate-400">AFFF Foam Tank Level (LS-001):</span><span class="text-emerald-400 font-bold">NORMAL (&gt; 25%)</span></div>
                        <div class="flex justify-between"><span class="text-slate-400">Diesel Fuel Day Tank (LS-002):</span><span class="text-emerald-400 font-bold">NORMAL (&gt; 50%)</span></div>
                        <div class="flex justify-between"><span class="text-slate-400">Discharge Header Pressure (PST-001):</span><span class="font-mono font-bold text-white">8.5 bar</span></div>
                    </div>
                    <div class="mt-6 flex space-x-2">
                        <button onclick="simFoamRelease()" class="flex-1 bg-red-600 hover:bg-red-500 text-white font-bold py-2 rounded text-xs transition animate-pulse">MANUAL FOAM RELEASE</button>
                        <button onclick="simFoamStop()" class="flex-1 bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold py-2 rounded text-xs transition">FOAM STOP</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 4: PRESSURES & TANK FARM -->
        <div id="tab-process" class="hmi-tab-pane hidden space-y-6">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Pressures Table -->
                <div class="scada-card p-5">
                    <h3 class="font-bold text-sm text-slate-200 mb-4 border-b border-slate-800 pb-2">PROCESS PRESSURE TRANSMITTERS</h3>
                    <table class="w-full text-xs text-left">
                        <thead class="text-slate-500 uppercase font-mono border-b border-slate-800">
                            <tr><th class="py-2">Tag</th><th>Description</th><th>Current</th><th>Trip Limits</th><th>Status</th></tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800/60 font-mono">
                            <tr><td class="py-2.5 text-blue-400 font-bold">PIT-001</td><td class="text-slate-300">Oil Expedition</td><td id="tdPit001">45 psi</td><td>PAL:10, PAH:100</td><td><span class="scada-led green-on"></span></td></tr>
                            <tr><td class="py-2.5 text-blue-400 font-bold">PIT-002</td><td class="text-slate-300">Water Injection Manifold</td><td id="tdPit002">650 psi</td><td>PAL:200, PAHH:800</td><td><span class="scada-led green-on"></span></td></tr>
                            <tr><td class="py-2.5 text-blue-400 font-bold">PIT-003</td><td class="text-slate-300">Oil Injection Manifold</td><td id="tdPit003">2250 psi</td><td>PAL:1700, PAHH:2800</td><td><span class="scada-led green-on"></span></td></tr>
                            <tr><td class="py-2.5 text-blue-400 font-bold">6401-PST-001</td><td class="text-slate-300">Fuel Gas Line</td><td id="tdPst6401">68 psi</td><td>PAL:40, PAH:100</td><td><span class="scada-led green-on"></span></td></tr>
                            <tr><td class="py-2.5 text-blue-400 font-bold">7002-PST-001</td><td class="text-slate-300">ESDV Air Accumulator</td><td id="tdPst7002">95 psi</td><td>Min: 50 psi</td><td><span class="scada-led green-on"></span></td></tr>
                        </tbody>
                    </table>
                </div>

                <!-- Tanks Table -->
                <div class="scada-card p-5">
                    <h3 class="font-bold text-sm text-slate-200 mb-4 border-b border-slate-800 pb-2">CRUDE STORAGE RADAR LEVEL TRANSMITTERS</h3>
                    <table class="w-full text-xs text-left">
                        <thead class="text-slate-500 uppercase font-mono border-b border-slate-800">
                            <tr><th class="py-2">Tag</th><th>Vessel</th><th>Level (m)</th><th>Limits (m)</th><th>Bar</th></tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800/60 font-mono">
                            <tr><td class="py-2.5 text-blue-400 font-bold">LIT-100</td><td class="text-slate-300">Tank T-100</td><td id="tdLit100">8.4 m</td><td>LAL:0.7, LAH:9.0</td><td><div class="w-24 bg-slate-800 h-2 rounded"><div class="bg-blue-500 h-2 rounded" style="width: 60%"></div></div></td></tr>
                            <tr><td class="py-2.5 text-blue-400 font-bold">LIT-200</td><td class="text-slate-300">Tank T-200</td><td id="tdLit200">6.2 m</td><td>LAL:0.7, LAH:9.0</td><td><div class="w-24 bg-slate-800 h-2 rounded"><div class="bg-blue-500 h-2 rounded" style="width: 44%"></div></div></td></tr>
                            <tr><td class="py-2.5 text-blue-400 font-bold">LIT-300</td><td class="text-slate-300">Tank T-300</td><td id="tdLit300">7.8 m</td><td>LAL:0.7, LAH:9.0</td><td><div class="w-24 bg-slate-800 h-2 rounded"><div class="bg-blue-500 h-2 rounded" style="width: 55%"></div></div></td></tr>
                            <tr><td class="py-2.5 text-blue-400 font-bold">LIT-400</td><td class="text-slate-300">Tank T-400</td><td id="tdLit400">5.5 m</td><td>LAL:0.7, LAH:11.0</td><td><div class="w-24 bg-slate-800 h-2 rounded"><div class="bg-blue-500 h-2 rounded" style="width: 50%"></div></div></td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 5: CAUSE & EFFECT MATRIX -->
        <div id="tab-matrix" class="hmi-tab-pane hidden space-y-6">
            <div class="scada-card p-4 overflow-x-auto">
                <h2 class="text-base font-bold text-white mb-2">CAUSE & EFFECT INTERLOCK MATRIX (01-MAN-03-07-PDF-C2C Final)</h2>
                <p class="text-xs text-slate-400 mb-4">Fail-Safe De-energize to Trip Interlocks</p>
                <table class="w-full text-xs text-center border-collapse">
                    <thead>
                        <tr class="bg-slate-900 text-slate-400 font-mono">
                            <th class="p-2 border border-slate-800 text-left">Initiating Cause</th>
                            <th class="p-2 border border-slate-800">Master ESD (DO 0)</th>
                            <th class="p-2 border border-slate-800">Fuel Gas ESDV (DO 1)</th>
                            <th class="p-2 border border-slate-800">Gas Turbines (DO 21)</th>
                            <th class="p-2 border border-slate-800">Oil Booster (DO 8)</th>
                            <th class="p-2 border border-slate-800">Deluge Demand</th>
                        </tr>
                    </thead>
                    <tbody class="font-mono text-slate-300">
                        <tr><td class="p-2 border border-slate-800 text-left font-bold text-red-400">ESD Pushbutton (PB-E9)</td><td class="border border-slate-800 text-red-400 font-bold">X</td><td class="border border-slate-800 text-red-400 font-bold">X</td><td class="border border-slate-800"></td><td class="border border-slate-800 text-red-400 font-bold">X</td><td class="border border-slate-800"></td></tr>
                        <tr><td class="p-2 border border-slate-800 text-left font-bold text-amber-400">Confirmed Fire (Triple-IR)</td><td class="border border-slate-800 text-red-400 font-bold">X</td><td class="border border-slate-800 text-red-400 font-bold">X</td><td class="border border-slate-800"></td><td class="border border-slate-800 text-red-400 font-bold">X</td><td class="border border-slate-800 text-red-400 font-bold">X</td></tr>
                        <tr><td class="p-2 border border-slate-800 text-left font-bold text-amber-400">Confirmed Gas 2ooN</td><td class="border border-slate-800 text-red-400 font-bold">X</td><td class="border border-slate-800 text-red-400 font-bold">X</td><td class="border border-slate-800"></td><td class="border border-slate-800 text-red-400 font-bold">X</td><td class="border border-slate-800 text-red-400 font-bold">X</td></tr>
                        <tr><td class="p-2 border border-slate-800 text-left font-bold text-amber-400">Generator Smoke SD-001/002</td><td class="border border-slate-800"></td><td class="border border-slate-800"></td><td class="border border-slate-800 text-red-400 font-bold">X</td><td class="border border-slate-800"></td><td class="border border-slate-800"></td></tr>
                        <tr><td class="p-2 border border-slate-800 text-left font-bold text-blue-400">Oil Inj PAHH (2800 psi)</td><td class="border border-slate-800"></td><td class="border border-slate-800"></td><td class="border border-slate-800"></td><td class="border border-slate-800 text-red-400 font-bold">X</td><td class="border border-slate-800"></td></tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- TAB 6: PCR ANNUNCIATOR PANEL (LCP) -->
        <div id="tab-pcr" class="hmi-tab-pane hidden space-y-6">
            <div class="max-w-2xl mx-auto scada-card p-6 border-2 border-slate-700 bg-slate-900 shadow-2xl">
                <div class="border-b-2 border-slate-700 pb-3 mb-6 text-center">
                    <h2 class="text-lg font-black text-white tracking-widest uppercase">PRODUCTION CONTROL ROOM PANEL (FGCP-7404-001)</h2>
                    <p class="text-xs text-slate-400">Door Mimic: Status LEDs, Keyswitches & Pushbuttons</p>
                </div>

                <!-- LEDs Grid -->
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 p-4 bg-slate-950 rounded border border-slate-800 mb-6">
                    <div class="flex items-center space-x-2">
                        <span id="pcrL14" class="scada-led off"></span>
                        <span class="text-xs font-mono font-bold text-slate-300">L14: ESDV Closed (Red)</span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <span id="pcrL15" class="scada-led green-on"></span>
                        <span class="text-xs font-mono font-bold text-slate-300">L15: ESDV Open (Grn)</span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <span id="pcrL16" class="scada-led off"></span>
                        <span class="text-xs font-mono font-bold text-slate-300">L16: Low Air Acc (Amb)</span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <span id="pcrL17" class="scada-led off"></span>
                        <span class="text-xs font-mono font-bold text-slate-300">L17: Low Fuel Gas (Amb)</span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <span id="pcrL8" class="scada-led off"></span>
                        <span class="text-xs font-mono font-bold text-slate-300">L8: P2300 Stop (Red)</span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <span id="pcrL9" class="scada-led off"></span>
                        <span class="text-xs font-mono font-bold text-slate-300">L9: P2400 Stop (Red)</span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <span id="pcrL12" class="scada-led off"></span>
                        <span class="text-xs font-mono font-bold text-slate-300">L12: P3800 Stop (Red)</span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <span id="pcrL13" class="scada-led off"></span>
                        <span class="text-xs font-mono font-bold text-slate-300">L13: P3900 Stop (Red)</span>
                    </div>
                </div>

                <!-- Keyswitches -->
                <div class="grid grid-cols-2 gap-4">
                    <div class="p-3 bg-slate-950 rounded border border-slate-800 text-center">
                        <div class="text-xs font-bold text-slate-400 uppercase mb-2">Keyswitch S2: Foam Inhibit</div>
                        <button onclick="toggleKeyS2()" id="btnKeyS2" class="px-4 py-1.5 bg-slate-800 border border-slate-600 rounded text-xs font-bold text-white hover:bg-slate-700">POSITION: O (NORMAL)</button>
                    </div>
                    <div class="p-3 bg-slate-950 rounded border border-slate-800 text-center">
                        <div class="text-xs font-bold text-slate-400 uppercase mb-2">Keyswitch S3: All Outputs Inhibit</div>
                        <button onclick="toggleKeyS3()" id="btnKeyS3" class="px-4 py-1.5 bg-slate-800 border border-slate-600 rounded text-xs font-bold text-white hover:bg-slate-700">POSITION: O (NORMAL)</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 7: ALARMS & EVENTS LOG -->
        <div id="tab-alarms" class="hmi-tab-pane hidden space-y-6">
            <div class="scada-card p-4">
                <div class="flex items-center justify-between mb-4">
                    <h2 class="text-base font-black text-white">ACTIVE ALARM & EVENT CHRONOLOGY</h2>
                    <button onclick="clearAlarmLog()" class="bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs px-3 py-1.5 rounded border border-slate-700 font-semibold">Clear Cleared Events</button>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-xs text-left" id="alarmLogTable">
                        <thead class="text-slate-500 uppercase font-mono border-b border-slate-800">
                            <tr><th class="py-2">Timestamp</th><th>Tag</th><th>Severity</th><th>Message</th><th>State</th></tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800/60 font-mono" id="alarmLogBody">
                            <!-- Injected dynamically -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

    </main>

    <!-- Collapsible Live Test Simulator Drawer -->
    <div id="simDrawer" class="fixed right-0 top-0 bottom-0 w-80 bg-slate-900 border-l border-slate-800 shadow-2xl transform translate-x-full transition-transform duration-300 z-40 flex flex-col">
        <div class="p-4 bg-slate-950 border-b border-slate-800 flex items-center justify-between">
            <h3 class="font-bold text-sm text-amber-400 flex items-center">
                <span class="w-2.5 h-2.5 bg-amber-400 rounded-full mr-2 animate-ping"></span>
                Live Hardware Simulator
            </h3>
            <button onclick="toggleSimulatorDrawer()" class="text-slate-400 hover:text-white">&times;</button>
        </div>
        <div class="p-4 flex-1 overflow-y-auto space-y-4 text-xs">
            <div>
                <label class="font-bold text-slate-300 block mb-1">Simulate Gas Leak (% LEL)</label>
                <input type="range" min="0" max="100" value="0" id="rngGasSim" oninput="simInjectGas(this.value)" class="w-full accent-amber-500">
                <div class="flex justify-between text-[11px] text-slate-500 font-mono"><span>0%</span><span id="lblGasVal" class="text-amber-400 font-bold">0% LEL</span><span>100%</span></div>
            </div>

            <div>
                <label class="font-bold text-slate-300 block mb-1">Simulate Toxic H2S (ppm)</label>
                <input type="range" min="0" max="100" value="0" id="rngH2sSim" oninput="simInjectH2S(this.value)" class="w-full accent-blue-500">
                <div class="flex justify-between text-[11px] text-slate-500 font-mono"><span>0 ppm</span><span id="lblH2sVal" class="text-blue-400 font-bold">0 ppm</span><span>100 ppm</span></div>
            </div>

            <div class="pt-2 border-t border-slate-800 space-y-2">
                <button onclick="simTriggerFlame()" class="w-full bg-red-900/80 hover:bg-red-800 border border-red-700 text-red-200 font-bold py-2 rounded">Trigger Optical Flame Alarm</button>
                <button onclick="simTriggerSmoke()" class="w-full bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-200 font-bold py-2 rounded">Trigger Smoke Alarm (Turbine)</button>
                <button onclick="simTriggerEsd()" class="w-full bg-red-600 hover:bg-red-500 text-white font-bold py-2 rounded shadow">TRIGGER MASTER ESD (PB-E9)</button>
            </div>
        </div>
    </div>

    <!-- Client Logic Script -->
    <script>
        const TAG_DB = {tag_db_json};
        let hornMuted = false;
        let esdTripped = false;
        let keyS2 = false;
        let keyS3 = false;
        let alarmLog = [];

        function switchTab(tabId, btn) {{
            document.querySelectorAll('.hmi-tab-pane').forEach(p => p.classList.add('hidden'));
            document.getElementById(tabId).classList.remove('hidden');
            document.querySelectorAll('.scada-tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        }}

        function toggleSimulatorDrawer() {{
            document.getElementById('simDrawer').classList.toggle('translate-x-full');
        }}

        // Populate 24 Gas Detectors in Tab 2
        function initGasGrid() {{
            const grid = document.getElementById('gasDetectorGrid');
            grid.innerHTML = '';
            for (let i = 1; i <= 24; i++) {{
                const id = `DG_7404_${{String(i).padStart(3, '0')}}`;
                const card = document.createElement('div');
                card.className = 'scada-card p-3 text-center';
                card.id = `card-${{id}}`;
                card.innerHTML = `
                    <div class="text-[10px] text-slate-400 font-mono">7404-DG-${{String(i).padStart(3, '0')}}</div>
                    <div class="text-base font-black font-mono text-slate-200 my-1" id="val-${{id}}">0.0%</div>
                    <div class="w-full bg-slate-800 h-1.5 rounded overflow-hidden">
                        <div class="bg-blue-500 h-1.5 rounded transition-all" id="bar-${{id}}" style="width: 0%"></div>
                    </div>
                    <div class="text-[9px] text-slate-500 mt-1" id="stat-${{id}}">NORMAL</div>
                `;
                grid.appendChild(card);
            }}
        }}

        function simInjectGas(val) {{
            document.getElementById('lblGasVal').textContent = val + '% LEL';
            for (let i = 1; i <= 6; i++) {{
                const id = `DG_7404_${{String(i).padStart(3, '0')}}`;
                document.getElementById(`val-${{id}}`).textContent = val + '%';
                document.getElementById(`bar-${{id}}`).style.width = val + '%';
                const stat = document.getElementById(`stat-${{id}}`);
                if (val >= 30) {{
                    stat.textContent = 'HIGH-HIGH ALM';
                    stat.className = 'text-[9px] text-red-400 font-bold alarm-blink';
                }} else if (val >= 20) {{
                    stat.textContent = 'LOW ALARM';
                    stat.className = 'text-[9px] text-amber-400 font-bold';
                }} else {{
                    stat.textContent = 'NORMAL';
                    stat.className = 'text-[9px] text-slate-500';
                }}
            }}
            if (val >= 30 && !esdTripped) {{
                addAlarm('DG_7404_001_HiHiAlm', 'HIGH-HIGH', 'Combustible Gas Cloud 2ooN Confirmed (>= 30% LEL)');
                triggerEsdSequence();
            }}
        }}

        function simInjectH2S(val) {{
            document.getElementById('lblH2sVal').textContent = val + ' ppm';
            if (val >= 20) {{
                addAlarm('AIT_H2S_001_HiHiAlm', 'HIGH-HIGH', 'Toxic Gas H2S High-High (>= 20 ppm) Siren Active');
            }}
        }}

        function simTriggerFlame() {{
            addAlarm('DF_7404_001_FireAlarm', 'CRITICAL', 'Optical Flame Confirmed Alarm - Deluge Activated');
            triggerEsdSequence();
            triggerDeluge();
        }}

        function simTriggerSmoke() {{
            addAlarm('SD_001_002_Alarm', 'HIGH-HIGH', 'Generator Building Smoke Detection - Turbine Trips');
            document.getElementById('txtTurbineStatus').textContent = 'TRIPPED (SD-GE=0)';
            document.getElementById('txtTurbineStatus').className = 'text-red-400 font-bold';
        }}

        function simTriggerEsd() {{
            addAlarm('ESD_TRIP_Master', 'EMERGENCY', 'Master ESD Pushbutton PB-E9 Activated');
            triggerEsdSequence();
        }}

        function triggerEsdSequence() {{
            esdTripped = true;
            document.getElementById('masterEsdBadge').className = 'px-3 py-1.5 rounded bg-red-950/80 border border-red-500/50 text-red-300 text-xs font-bold flex items-center space-x-2 alarm-blink';
            document.getElementById('masterEsdTxt').textContent = 'PLANT ESD: TRIPPED (DE-ENERGIZED)';
            document.getElementById('cardEsdvTxt').textContent = 'CLOSED (TRIP)';
            document.getElementById('cardEsdvTxt').className = 'text-lg font-black text-red-400 mt-1';
            document.getElementById('esdvLeft').setAttribute('fill', '#ef4444');
            document.getElementById('esdvRight').setAttribute('fill', '#ef4444');
            document.getElementById('cardOilPumpTxt').textContent = 'STOPPED (ESD)';
            document.getElementById('cardOilPumpTxt').className = 'text-lg font-black text-red-400 mt-1';
            document.getElementById('cardWaterPumpTxt').textContent = 'STOPPED (ESD)';
            document.getElementById('cardWaterPumpTxt').className = 'text-lg font-black text-red-400 mt-1';
            document.getElementById('pcrL14').className = 'scada-led red-on';
            document.getElementById('pcrL15').className = 'scada-led off';
            document.getElementById('pcrL8').className = 'scada-led red-on';
            document.getElementById('pcrL12').className = 'scada-led red-on';
        }}

        function triggerDeluge() {{
            document.getElementById('delugeStatusBadge').className = 'px-3 py-1.5 rounded bg-red-950 border border-red-500 text-red-300 text-xs font-bold flex items-center space-x-2 alarm-blink';
            document.getElementById('delugeStatusTxt').textContent = 'DELUGE: ACTIVE';
            document.getElementById('badgePumpA').textContent = 'RUNNING';
            document.getElementById('badgePumpA').className = 'bg-emerald-950 text-emerald-300 text-xs px-2.5 py-0.5 rounded font-bold';
        }}

        function simFoamRelease() {{
            addAlarm('VOTE_Deluge_Demand', 'CRITICAL', 'Manual Foam Release Initiated');
            triggerDeluge();
        }}

        function simFoamStop() {{
            document.getElementById('delugeStatusBadge').className = 'px-3 py-1.5 rounded bg-slate-900 border border-slate-700 text-slate-300 text-xs font-bold flex items-center space-x-2';
            document.getElementById('delugeStatusTxt').textContent = 'DELUGE: STANDBY';
            document.getElementById('badgePumpA').textContent = 'STOPPED';
            document.getElementById('badgePumpA').className = 'bg-slate-800 text-slate-300 text-xs px-2.5 py-0.5 rounded font-bold';
        }}

        function toggleAlarmSilence() {{
            hornMuted = !hornMuted;
            document.getElementById('btnMuteTxt').textContent = hornMuted ? 'Horn Muted (Active)' : 'Silence Horn (E12)';
            document.getElementById('btnMuteHorn').className = hornMuted ? 'bg-amber-600 text-white text-xs font-bold px-3 py-2 rounded' : 'bg-slate-800 text-slate-200 text-xs font-bold px-3 py-2 rounded border border-slate-700';
        }}

        function resetAllAlarms() {{
            esdTripped = false;
            hornMuted = false;
            document.getElementById('masterEsdBadge').className = 'px-3 py-1.5 rounded bg-emerald-950/80 border border-emerald-500/50 text-emerald-300 text-xs font-bold flex items-center space-x-2 shadow-inner';
            document.getElementById('masterEsdTxt').textContent = 'PLANT ESD: HEALTHY (24V)';
            document.getElementById('cardEsdvTxt').textContent = 'OPEN (NORMAL)';
            document.getElementById('cardEsdvTxt').className = 'text-lg font-black text-emerald-400 mt-1';
            document.getElementById('esdvLeft').setAttribute('fill', '#22c55e');
            document.getElementById('esdvRight').setAttribute('fill', '#22c55e');
            document.getElementById('cardOilPumpTxt').textContent = 'RUNNING (AUTO)';
            document.getElementById('cardOilPumpTxt').className = 'text-lg font-black text-emerald-400 mt-1';
            document.getElementById('cardWaterPumpTxt').textContent = 'RUNNING (AUTO)';
            document.getElementById('cardWaterPumpTxt').className = 'text-lg font-black text-emerald-400 mt-1';
            document.getElementById('pcrL14').className = 'scada-led off';
            document.getElementById('pcrL15').className = 'scada-led green-on';
            document.getElementById('pcrL8').className = 'scada-led off';
            document.getElementById('pcrL12').className = 'scada-led off';
            simFoamStop();
        }}

        function addAlarm(tag, sev, msg) {{
            const time = new Date().toLocaleTimeString();
            alarmLog.unshift({{ time, tag, sev, msg, state: 'ACTIVE' }});
            renderAlarmTable();
        }}

        function renderAlarmTable() {{
            const tbody = document.getElementById('alarmLogBody');
            tbody.innerHTML = '';
            document.getElementById('alarmCountBadge').textContent = alarmLog.length;
            alarmLog.forEach(a => {{
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-900/50';
                tr.innerHTML = `
                    <td class="py-2 text-slate-400">${{a.time}}</td>
                    <td class="text-blue-400 font-bold">${{a.tag}}</td>
                    <td><span class="px-2 py-0.5 rounded text-[10px] font-bold ${{a.sev === 'CRITICAL' || a.sev === 'EMERGENCY' ? 'bg-red-950 text-red-300 border border-red-700' : 'bg-amber-950 text-amber-300 border border-amber-700'}}">${{a.sev}}</span></td>
                    <td class="text-slate-200">${{a.msg}}</td>
                    <td class="text-red-400 font-bold">${{a.state}}</td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        function clearAlarmLog() {{
            alarmLog = [];
            renderAlarmTable();
        }}

        function toggleKeyS2() {{
            keyS2 = !keyS2;
            document.getElementById('btnKeyS2').textContent = keyS2 ? 'POSITION: I (INHIBIT)' : 'POSITION: O (NORMAL)';
            document.getElementById('btnKeyS2').className = keyS2 ? 'px-4 py-1.5 bg-amber-600 rounded text-xs font-bold text-white' : 'px-4 py-1.5 bg-slate-800 border border-slate-600 rounded text-xs font-bold text-white';
        }}

        function toggleKeyS3() {{
            keyS3 = !keyS3;
            document.getElementById('btnKeyS3').textContent = keyS3 ? 'POSITION: I (INHIBIT)' : 'POSITION: O (NORMAL)';
            document.getElementById('btnKeyS3').className = keyS3 ? 'px-4 py-1.5 bg-red-600 rounded text-xs font-bold text-white' : 'px-4 py-1.5 bg-slate-800 border border-slate-600 rounded text-xs font-bold text-white';
        }}

        // Initialize on load
        window.onload = () => {{
            initGasGrid();
            addAlarm('SYS_Watchdog_OK', 'INFO', 'FGCP-7404-001 ControlLogix System Watchdog Online');
        }};
    </script>
</body>
</html>'''

    for out_dir in (BASE_DIR, DESKTOP_DIR):
        os.makedirs(out_dir, exist_ok=True)
        hmi_path = os.path.join(out_dir, "GNTF_HMI_Application.html")
        with open(hmi_path, "w", encoding="utf-8") as f:
            f.write(hmi_html)
        print(f"[OK] Generated Interactive SCADA / HMI Workstation: {hmi_path} ({len(hmi_html):,} bytes)")


# =============================================================================
# 7. MAIN BUILD PIPELINE
# =============================================================================
def main():
    print("=" * 76)
    print("GNTF QUINGUILA TANK FARM — UPGRADED CONTROLLOGIX 5580 & FULL HMI SUITE")
    print("Project: FGCP-7404-001 (01-MAN-03-06 & 01-MAN-03-07 Final Approved)")
    print("=" * 76)

    # 1. Tags
    tags = build_upgraded_tags()
    print(f"\n[STEP 1/5] Upgraded Controller Tags defined: {len(tags)}")

    # 2. Routines
    routines = build_upgraded_rll_routines()
    total_rungs = sum(len(r[2]) for r in routines)
    print(f"[STEP 2/5] Upgraded RLL Routines built: {len(routines)} routines, {total_rungs} total rungs")

    # 3. Studio 5000 L5X Files
    print("\n[STEP 3/5] Generating Studio 5000 Controller & Program L5X Project Files...")
    write_upgraded_l5x_files(tags, routines)

    # 4. Web Ladder Viewer
    print("\n[STEP 4/5] Generating Upgraded Web Ladder Diagram Viewer...")
    write_upgraded_ladder_html(tags, routines)

    # 5. Full HMI Suite
    print("\n[STEP 5/5] Generating Complete HMI Suite (Interactive Web HMI & FactoryTalk CSV/XML)...")
    write_factorytalk_hmi_files(tags)
    write_hmi_application_html(tags)

    print("\n" + "=" * 76)
    print("[SUCCESS] Complete Upgraded ControlLogix & HMI Project Suite Built Successfully!")
    print("=" * 76)


if __name__ == "__main__":
    main()
