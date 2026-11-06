# -*- coding: utf-8 -*-
"""
Generate Allen-Bradley ControlLogix (1756-L82E, Studio 5000 Logix Designer)
Structured Text (ST) conversion of P20890_Angola (GE VersaMax FGCP-7404-001),
strictly aligned with the GNTF Quinguila Control System Upgrade project
documentation in C:\\Users\\Wajdi TAKTAK\\Desktop\\DOC\\ws_g\\project:
  - System Architecture: 01-MAN-03-11-PDF-C3A (1756-A13, 1756-L82E, 1756-PB72)
  - Equipment List:      01-MAN-02-02-PDF-C1
  - I/O List:            01-MAN-03-06-PDF-C2C Final
  - Terminal Block Diag: 01-MAN-02-13-PDF-C1A
  - Cause & Effect:      01-MAN-03-07-PDF-C2C Final
  - Alarms & Events:     01-MAN-03-02-PDF-C2 Final
  - Setpoints List:      01-MAN-03-13-PDF-C1
  - Functional Desc:     01-MAN-03-10-PDF-C1 (V2)
"""
import csv
import html
import os
import xml.sax.saxutils as saxutils

OUT_DIR_WS = r"c:\Users\Wajdi TAKTAK\Desktop\DOC\ws_g\pme_ladder_export"
OUT_DIR_DESKTOP = r"C:\Users\Wajdi TAKTAK\Desktop\P20890_Angola"

# ---------------------------------------------------------------------------
# 1. HARDWARE CONFIGURATION & COMPLETE I/O MAPPING TABLE
#    (Cross-referencing Legacy GE VersaMax <-> New Allen-Bradley 1756 Rack 1)
# ---------------------------------------------------------------------------
IO_MAP = [
    # === SLOT 2: 1756-IF16 (Analog Input Module - TB-02) ===
    ("AI", 1, 2, 0,  "TS2-00", "TB-02 (1&2&3)",   "7404-DG-001",     "DG_7404_001",      "Local:2:I.Ch0Data",  "%AI0001", "0-100 %LEL", "20% LEL",  "30% LEL",  "N/A",      "CH4 Gas detector (IR Point) pump house 1"),
    ("AI", 1, 2, 1,  "TS2-01", "TB-02 (4&5&6)",   "7404-DG-002",     "DG_7404_002",      "Local:2:I.Ch1Data",  "%AI0002", "0-100 %LEL", "20% LEL",  "30% LEL",  "N/A",      "CH4 Gas detector (IR Point) pump house 2"),
    ("AI", 1, 2, 2,  "TS2-02", "TB-02 (7&8&9)",   "7404-DG-003",     "DG_7404_003",      "Local:2:I.Ch2Data",  "%AI0003", "0-100 %LEL", "20% LEL",  "30% LEL",  "N/A",      "CH4 Gas detector (IR Point) pump house 3"),
    ("AI", 1, 2, 3,  "TS2-03", "TB-02 (10&11&12)","7404-DG-004",     "DG_7404_004",      "Local:2:I.Ch3Data",  "%AI0004", "0-100 %LEL", "20% LEL",  "30% LEL",  "N/A",      "CH4 Gas detector (IR Point) pump house 4"),
    ("AI", 1, 2, 4,  "TS2-04", "TB-02 (13&14&15)","7404-DG-005",     "DG_7404_005",      "Local:2:I.Ch4Data",  "%AI0005", "0-100 %LEL", "20% LEL",  "30% LEL",  "N/A",      "CH4 Gas detector (IR Point) pump house 5"),
    ("AI", 1, 2, 5,  "TS2-05", "TB-02 (16&17&18)","7404-DG-006",     "DG_7404_006",      "Local:2:I.Ch5Data",  "%AI0006", "0-100 %LEL", "20% LEL",  "30% LEL",  "N/A",      "CH4 Gas detector (IR Point) pump house 6"),
    ("AI", 1, 2, 6,  "TS2-06", "TB-02 (19&20&21)","7404-DG-007",     "DG_7404_007",      "Local:2:I.Ch6Data",  "%AI0007", "0-100 %LEL", "20% LEL",  "30% LEL",  "N/A",      "CH4 Gas detector (IR Point) pump house 7"),
    ("AI", 1, 2, 7,  "TS2-07", "TB-02 (22&23&24)","7404-DG-008",     "DG_7404_008",      "Local:2:I.Ch7Data",  "%AI0008", "0-100 %LEL", "20% LEL",  "30% LEL",  "N/A",      "CH4 Gas detector (IR Point) pump house 8"),
    ("AI", 1, 2, 8,  "TS2-08", "TB-02 (25&26&27)","7404-DG-009",     "DG_7404_009",      "Local:2:I.Ch8Data",  "%AI0009", "0-100 %LEL", "20% LEL",  "30% LEL",  "N/A",      "CH4 Gas detector (IR Point) pump house 9"),
    ("AI", 1, 2, 9,  "TS2-09", "TB-02 (28&29&30)","7404-DG-010",     "DG_7404_010",      "Local:2:I.Ch9Data",  "%AI0010", "0-100 %LEL", "20% LEL",  "30% LEL",  "N/A",      "CH4 Gas detector (IR Point) pump house 10"),
    ("AI", 1, 2, 10, "TS2-10", "TB-02 (31&32&33)","7404-DG-011",     "DG_7404_011",      "Local:2:I.Ch10Data", "%AI0011", "0-100 %LEL", "20% LEL",  "30% LEL",  "N/A",      "CH4 Gas detector (IR Point) pump house 11 (was SpareAI_11)"),
    ("AI", 1, 2, 11, "TS2-11", "TB-02 (34&35&36)","7404-DG-012",     "DG_7404_012",      "Local:2:I.Ch11Data", "%AI0015", "0-100 %LEL", "20% LEL",  "30% LEL",  "N/A",      "CH4 Gas detector (IR Point) pump house 12 (was SpareAI_15)"),
    ("AI", 1, 2, 12, "TS2-12", "TB-02 (37&38&39)","7404-DG-011R",    "DG_7404_011R",     "Local:2:I.Ch12Data", "%AI0014", "0-5.00 LELm","1.00 LELm","3.00 LELm","N/A",      "CH4 Line-of-Sight Open Path Gas Detector"),
    ("AI", 1, 2, 13, "TS2-13", "TB-02 (40&41&42)","GD-001",          "GD_001",           "Local:2:I.Ch13Data", "NEW",     "0-100 %LEL", "20% LEL",  "30% LEL",  "N/A",      "CH4 Gas detector 1 (Gas Generator Room)"),
    ("AI", 1, 2, 14, "TS2-14", "TB-02 (43&44&45)","GD-002",          "GD_002",           "Local:2:I.Ch14Data", "NEW",     "0-100 %LEL", "20% LEL",  "30% LEL",  "N/A",      "CH4 Gas detector 2 (Gas Generator Room)"),
    ("AI", 1, 2, 15, "TS2-15", "TB-02 (46&47&48)","GD-003",          "GD_003",           "Local:2:I.Ch15Data", "NEW",     "0-100 %LEL", "20% LEL",  "30% LEL",  "N/A",      "CH4 Gas detector 3 (Gas Generator Room)"),

    # === SLOT 3: 1756-IF16 (Analog Input Module - TB-03) ===
    ("AI", 1, 3, 0,  "TS3-00", "TB-03 (1&2)",     "PIT-001",         "PIT_001",          "Local:3:I.Ch0Data",  "NEW",     "0-200 Psi",  "10 Psi",   "100 Psi",  "N/A",      "PT Oil Expedition Manifold Pressure"),
    ("AI", 1, 3, 1,  "TS3-01", "TB-03 (4&5)",     "PIT-002",         "PIT_002",          "Local:3:I.Ch1Data",  "NEW",     "0-1500 Psi", "200 Psi",  "800 Psi",  "900 Psi",  "PT Water Injection Manifold Pressure"),
    ("AI", 1, 3, 2,  "TS3-02", "TB-03 (7&8)",     "PIT-003",         "PIT_003",          "Local:3:I.Ch2Data",  "NEW",     "0-3000 Psi", "1700 Psi", "2700 Psi", "2800 Psi", "PT Oil Injection Manifold Pressure"),
    ("AI", 1, 3, 3,  "TS4-03", "TB-03 (10&11)",   "7503-PST-001",    "PST_7503_001",     "Local:3:I.Ch3Data",  "%AI0019", "0-100 Psi",  "N/A",      "50 Psi",   "N/A",      "PT Deluge Line Pressure (Foam/Deluge Released)"),
    ("AI", 1, 3, 4,  "TS4-04", "TB-03 (13&14)",   "7002-PST-001",    "PST_7002_001",     "Local:3:I.Ch4Data",  "%AI0017", "0-100 Psi",  "50 Psi",   "N/A",      "N/A",      "PT Air Accumulator Pressure ESDV"),
    ("AI", 1, 3, 5,  "TS4-05", "TB-03 (16&17)",   "6401-PST-001",    "PST_6401_001",     "Local:3:I.Ch5Data",  "%AI0018", "0-150 Psi",  "40 Psi",   "100 Psi",  "N/A",      "PT Fuel Gas Pressure"),
    ("AI", 1, 3, 6,  "TS4-06", "TB-03 (19)",      "7503-FR-003",     "FR_7503_003",      "Local:3:I.Ch6Data",  "%AI0022", "4-20 mA",    "N/A",      "30 %",     "N/A",      "Manual Foam Release Button inside Local CP (PCR)"),
    ("AI", 1, 3, 7,  "TS4-07", "TB-03 (19&20)",   "7503-FR-001/002", "FR_7503_001_002",  "Local:3:I.Ch7Data",  "%AI0020", "4-20 mA",    "N/A",      "30 %",     "N/A",      "Manual Foam Release Buttons Outside (Field)"),
    ("AI", 1, 3, 8,  "TS3-08", "TB-03 (22&23)",   "SPARE",           "SpareAI_16",       "Local:3:I.Ch8Data",  "%AI0016", "0-100 %",    "20 %",     "30 %",     "N/A",      "Spare Analog Input (Legacy SpareAI_16)"),
    ("AI", 1, 3, 9,  "TS3-09", "TB-03 (25&26)",   "SPARE",           "SpareAI_21",       "Local:3:I.Ch9Data",  "%AI0021", "0-100 %",    "20 %",     "30 %",     "N/A",      "Spare Analog Input (Legacy SpareAI_21)"),
    ("AI", 1, 3, 10, "TS3-10", "TB-03 (28&29)",   "SPARE",           "SpareAI_23",       "Local:3:I.Ch10Data", "%AI0023", "0-100 %",    "20 %",     "30 %",     "N/A",      "Spare Analog Input (Legacy SpareAI_23)"),
    ("AI", 1, 3, 11, "TS3-11", "TB-03 (31&32)",   "SPARE",           "SpareAI_24",       "Local:3:I.Ch11Data", "%AI0024", "0-100 %",    "20 %",     "30 %",     "N/A",      "Spare Analog Input (Legacy SpareAI_24)"),

    # === SLOT 4: 1756-IF16 (Analog Input Module - TB-04) ===
    ("AI", 1, 4, 0,  "TS5-00", "TB-04 (1&2&3)",   "H2S-001",         "H2S_001",          "Local:4:I.Ch0Data",  "NEW",     "0-100 PPM",  "10 PPM",   "20 PPM",   "N/A",      "H2S Gas Detector 1"),
    ("AI", 1, 4, 1,  "TS5-01", "TB-04 (4&5&6)",   "H2S-002",         "H2S_002",          "Local:4:I.Ch1Data",  "NEW",     "0-100 PPM",  "10 PPM",   "20 PPM",   "N/A",      "H2S Gas Detector 2"),
    ("AI", 1, 4, 2,  "TS5-02", "TB-04 (7&8&9)",   "H2S-003",         "H2S_003",          "Local:4:I.Ch2Data",  "NEW",     "0-100 PPM",  "10 PPM",   "20 PPM",   "N/A",      "H2S Gas Detector 3"),
    ("AI", 1, 4, 3,  "TS5-03", "TB-04 (10&11&12)","H2S-004",         "H2S_004",          "Local:4:I.Ch3Data",  "NEW",     "0-100 PPM",  "10 PPM",   "20 PPM",   "N/A",      "H2S Gas Detector 4"),
    ("AI", 1, 4, 4,  "TS5-04", "TB-04 (13&14&15)","H2S-005",         "H2S_005",          "Local:4:I.Ch4Data",  "NEW",     "0-100 PPM",  "10 PPM",   "20 PPM",   "N/A",      "H2S Gas Detector 5"),
    ("AI", 1, 4, 5,  "TS5-05", "TB-04 (16&17&18)","H2S-006",         "H2S_006",          "Local:4:I.Ch5Data",  "NEW",     "0-100 PPM",  "10 PPM",   "20 PPM",   "N/A",      "H2S Gas Detector 6"),
    ("AI", 1, 4, 6,  "TS5-06", "TB-04 (19&20&21)","H2S-007",         "H2S_007",          "Local:4:I.Ch6Data",  "NEW",     "0-100 PPM",  "10 PPM",   "20 PPM",   "N/A",      "H2S Gas Detector 7"),
    ("AI", 1, 4, 7,  "TS5-07", "TB-04 (22&23&24)","H2S-008",         "H2S_008",          "Local:4:I.Ch7Data",  "NEW",     "0-100 PPM",  "10 PPM",   "20 PPM",   "N/A",      "H2S Gas Detector 8"),
    ("AI", 1, 4, 8,  "TS5-08", "TB-04 (25&26&27)","H2S-009",         "H2S_009",          "Local:4:I.Ch8Data",  "NEW",     "0-100 PPM",  "10 PPM",   "20 PPM",   "N/A",      "H2S Gas Detector 9"),
    ("AI", 1, 4, 9,  "TS5-09", "TB-04 (28&29&30)","H2S-010",         "H2S_010",          "Local:4:I.Ch9Data",  "NEW",     "0-100 PPM",  "10 PPM",   "20 PPM",   "N/A",      "H2S Gas Detector 10"),
    ("AI", 1, 4, 10, "TS5-10", "TB-04 (31&32&33)","H2S-011",         "H2S_011",          "Local:4:I.Ch10Data", "NEW",     "0-100 PPM",  "10 PPM",   "20 PPM",   "N/A",      "H2S Gas Detector 11"),
    ("AI", 1, 4, 11, "TS5-11", "TB-04 (34&35&36)","H2S-012",         "H2S_012",          "Local:4:I.Ch11Data", "NEW",     "0-100 PPM",  "10 PPM",   "20 PPM",   "N/A",      "H2S Gas Detector 12"),
    ("AI", 1, 4, 12, "TS4-12", "TB-04 (37&38&39)","7404-DF-001",     "DF_7404_001",      "Local:4:I.Ch12Data", "%AI0012", "4-20 mA",    "N/A",      "30 %",     "N/A",      "Flame Detector 1 Pump House"),
    ("AI", 1, 4, 13, "TS4-13", "TB-04 (40&41&42)","7404-DF-002",     "DF_7404_002",      "Local:4:I.Ch13Data", "%AI0013", "4-20 mA",    "N/A",      "30 %",     "N/A",      "Flame Detector 2 Pump House"),
    ("AI", 1, 4, 14, "TS4-14", "TB-04 (43&44&45)","7404-DF-003",     "DF_7404_003",      "Local:4:I.Ch14Data", "NEW",     "4-20 mA",    "N/A",      "30 %",     "N/A",      "Flame Detector 3 Pump House"),
    ("AI", 1, 4, 15, "TS4-15", "TB-04 (46..51)",  "SD-001/002",      "SD_001_002",       "Local:4:I.Ch15Data", "NEW",     "4-20 mA",    "N/A",      "30 %",     "N/A",      "Smoke Detectors (Electrical / Generator Room)"),

    # === SLOT 6: 1756-IF8H (HART Analog Input Module - TB-06) ===
    ("HART", 1, 6, 0,"TS6-00", "TB-06 (1&2)",     "LIT-100",         "LIT_100",          "Local:6:I.Ch0Data",  "NEW",     "0-10.0 m",   "0.7 m",    "9.0 m",    "N/A",      "LT Tank T100 Level Transmitter (4-20mA HART)"),
    ("HART", 1, 6, 1,"TS6-01", "TB-06 (3&4)",     "LIT-200",         "LIT_200",          "Local:6:I.Ch1Data",  "NEW",     "0-10.0 m",   "0.7 m",    "9.0 m",    "N/A",      "LT Tank T200 Level Transmitter (4-20mA HART)"),
    ("HART", 1, 6, 2,"TS6-02", "TB-06 (5&6)",     "LIT-300",         "LIT_300",          "Local:6:I.Ch2Data",  "NEW",     "0-10.0 m",   "0.7 m",    "9.0 m",    "N/A",      "LT Tank T300 Level Transmitter (4-20mA HART)"),
    ("HART", 1, 6, 3,"TS6-03", "TB-06 (7&8)",     "LIT-400",         "LIT_400",          "Local:6:I.Ch3Data",  "NEW",     "0-12.0 m",   "0.7 m",    "11.0 m",   "N/A",      "LT Tank T400 Level Transmitter (4-20mA HART)"),

    # === SLOT 7: 1756-IB32 (32-Point Digital Input Module - TB-07) ===
    ("DI", 1, 7, 0,  "TS7-00", "TB-07 (1&2)",     "6401-ZSH-001",    "ZSH_6401_001",     "Local:7:I.Data.0",   "%I00001", "24V DC",     "-",        "-",        "-",        "6401-ZSH-001 ESD Valve Open Limit Switch"),
    ("DI", 1, 7, 1,  "TS7-01", "TB-07 (3&4)",     "6401-ZSL-001",    "ZSL_6401_001",     "Local:7:I.Data.1",   "%I00002", "24V DC",     "-",        "-",        "-",        "6401-ZSL-001 ESD Valve Closed Limit Switch"),
    ("DI", 1, 7, 2,  "TS7-02", "TB-07 (5&6)",     "FGCP-7404-001 E8","FS_FGCP_E8",       "Local:7:I.Data.2",   "%I00008", "24V DC",     "-",        "-",        "-",        "Foam Stop Button on FGCP Panel (E8) / SpareDI_08"),
    ("DI", 1, 7, 3,  "TS7-03", "TB-07 (7&8)",     "7503-LS-002",     "LS_7503_002",      "Local:7:I.Data.3",   "%I00005", "24V DC",     "-",        "-",        "-",        "7503-LS-002 Diesel Tank Low Level Switch"),
    ("DI", 1, 7, 4,  "TS7-04", "TB-07 (9&10)",    "7503-FS-001",     "FS_7503_001",      "Local:7:I.Data.4",   "%I00003", "24V DC",     "-",        "-",        "-",        "7503-FS-001 Stop Foam Button (Field)"),
    ("DI", 1, 7, 5,  "TS7-05", "TB-07 (11&12)",   "7503-LS-001",     "LS_7503_001",      "Local:7:I.Data.5",   "%I00004", "24V DC",     "-",        "-",        "-",        "7503-LS-001 AFFF Foam Tank Low Level Switch"),
    ("DI", 1, 7, 6,  "TS7-06", "TB-07 (13&14)",   "75-C-01A",        "Pump_A_PulsIn",    "Local:7:I.Data.6",   "%I00006", "24V DC",     "-",        "-",        "-",        "Pulsed Input from Q05 for Pump A Open-Circuit Check"),
    ("DI", 1, 7, 7,  "TS7-07", "TB-07 (15&16)",   "75-C-01B",        "Pump_B_Start_PulsIn","Local:7:I.Data.7", "%I00007", "24V DC",     "-",        "-",        "-",        "Pulsed Input from Q07 for Pump B Open-Circuit Check"),
    ("DI", 1, 7, 8,  "TS7-08", "TB-07 (17&18)",   "75-SB-01B",       "Pump_B_Inhibited", "Local:7:I.Data.8",   "%I00009", "24V DC",     "-",        "-",        "-",        "Standby Pump B Inhibited Keyswitch"),
    ("DI", 1, 7, 9,  "TS7-09", "TB-07 (19&20)",   "SPARE",           "SpareDI_11",       "Local:7:I.Data.9",   "%I00011", "24V DC",     "-",        "-",        "-",        "Spare Digital Input 11"),
    ("DI", 1, 7, 10, "TS7-10", "TB-07 (21&22)",   "FGCP-7404-001 E11","Reset_PB_E11",    "Local:7:I.Data.10",  "NEW",     "24V DC",     "-",        "-",        "-",        "FGCP-7404-001 Reset Alarm Pushbutton (E11)"),
    ("DI", 1, 7, 11, "TS7-11", "TB-07 (23&24)",   "FGCP-7404-001 E12","Mute_PB_E12",     "Local:7:I.Data.11",  "NEW",     "24V DC",     "-",        "-",        "-",        "FGCP-7404-001 Mute Alarm Pushbutton (E12)"),
    ("DI", 1, 7, 12, "TS7-12", "TB-07 (25&26)",   "6401-ESDV-001",   "ESDV_6401_001",    "Local:7:I.Data.12",  "%I00010", "24V DC",     "-",        "-",        "-",        "6401-ESDV-001 ESD Fuel Gas Pushbutton (E9)"),
    ("DI", 1, 7, 13, "TS7-13", "TB-07 (27&28)",   "FGCP-7404-001 S2","INHIBIT_FOAM_REL","Local:7:I.Data.13",  "%I00012", "24V DC",     "-",        "-",        "-",        "Inhibition Foam Release Keyswitch (S2)"),
    ("DI", 1, 7, 14, "TS7-14", "TB-07 (29&30)",   "FGCP-7404-001 S3","INHIBIT_ALL_OUTPUTS","Local:7:I.Data.14","%I00013","24V DC",     "-",        "-",        "-",        "Inhibition All Outputs Keyswitch (S3)"),
    ("DI", 1, 7, 15, "TS7-15", "TB-07 (31&32)",   "7404-SB-004 (E1)","ESTOP_P2300_E1",   "Local:7:I.Data.15",  "NEW",     "24V DC",     "-",        "-",        "-",        "Emergency Stop Button Power Oil Pump P-2300 (E1)"),
    ("DI", 1, 7, 16, "TS7-16", "TB-07 (33&34)",   "7404-SB-005 (E2)","ESTOP_P2400_E2",   "Local:7:I.Data.16",  "NEW",     "24V DC",     "-",        "-",        "-",        "Emergency Stop Button Power Oil Pump P-2400 (E2)"),
    ("DI", 1, 7, 17, "TS7-17", "TB-07 (35&36)",   "7404-SB-006 (E3)","ESTOP_P2500_E3",   "Local:7:I.Data.17",  "NEW",     "24V DC",     "-",        "-",        "-",        "Emergency Stop Button Power Oil Pump P-2500 (E3)"),
    ("DI", 1, 7, 18, "TS7-18", "TB-07 (37&38)",   "7404-SB-007 (E4)","ESTOP_P2600_E4",   "Local:7:I.Data.18",  "NEW",     "24V DC",     "-",        "-",        "-",        "Emergency Stop Button Power Oil Pump P-2600 (E4)"),
    ("DI", 1, 7, 19, "TS7-19", "TB-07 (39&40)",   "7404-SB-008 (E5)","ESTOP_P3800_E5",   "Local:7:I.Data.19",  "NEW",     "24V DC",     "-",        "-",        "-",        "Emergency Stop Button Water Inj. Pump P-3800 (E5)"),
    ("DI", 1, 7, 20, "TS7-20", "TB-07 (41&42)",   "7404-SB-009 (E6)","ESTOP_P3900_E6",   "Local:7:I.Data.20",  "NEW",     "24V DC",     "-",        "-",        "-",        "Emergency Stop Button Water Inj. Pump P-3900 (E6)"),

    # === SLOT 8: 1756-OB32 (32-Point Digital Output Module - TB-08) ===
    ("DO", 1, 8, 0,  "TS8-00", "TB-08 (1&2)",     "ESD_TRIP",        "PumpShutdown",     "Local:8:O.Data.0",   "%Q00008", "24V DC",     "-",        "-",        "-",        "Fire & Gas Pump Shutdown (Inverted Fail-Safe Output)"),
    ("DO", 1, 8, 1,  "TS8-01", "TB-08 (3&4)",     "6401-EY-001/002", "EY_6401_001_002",  "Local:8:O.Data.1",   "%Q00001", "24V DC",     "-",        "-",        "-",        "6401-EY-001/002 ESD Fuel Gas Valve Shutdown"),
    ("DO", 1, 8, 2,  "TS8-02", "TB-08 (5&6)",     "7404-SA-001/002", "SA_7404_001_002",  "Local:8:O.Data.2",   "%Q00002", "24V DC",     "-",        "-",        "-",        "7404-SA-001/002 Local Alarm Bell Pump House"),
    ("DO", 1, 8, 3,  "TS8-03", "TB-08 (7)",       "7503-PUMP-A",     "Pump_A_PulsOut",   "Local:8:O.Data.3",   "%Q00009", "24V DC",     "-",        "-",        "-",        "Pulsed Output for Open-Circuit Check on Pump A"),
    ("DO", 1, 8, 4,  "TS8-04", "TB-08 (9)",       "7503-PUMP-A",     "PUMP_A",           "Local:8:O.Data.4",   "%Q00005", "24V DC",     "-",        "-",        "-",        "Deluge Pump A Start/Stop Output"),
    ("DO", 1, 8, 5,  "TS8-05", "TB-08 (11)",      "7503-PUMP-B",     "Pump_B_Start_PulsOut","Local:8:O.Data.5","%Q00010", "24V DC",     "-",        "-",        "-",        "Pulsed Output for Open-Circuit Check on Pump B"),
    ("DO", 1, 8, 6,  "TS8-06", "TB-08 (13)",      "7503-PUMP-B",     "PUMP_B_START",     "Local:8:O.Data.6",   "%Q00007", "24V DC",     "-",        "-",        "-",        "Deluge Pump B Start Output (2s Pulse x3 Attempts)"),
    ("DO", 1, 8, 7,  "TS8-07", "TB-08 (15&16)",   "7503-PUMP-B",     "PUMP_B_STOP",      "Local:8:O.Data.7",   "%Q00006", "24V DC",     "-",        "-",        "-",        "Deluge Pump B Stop Output (2s Pulse)"),
    ("DO", 1, 8, 8,  "TS8-08", "TB-08 (17&18)",   "EDB1 (P2100/2200)","P2100_P2200",     "Local:8:O.Data.8",   "%Q00003", "24V DC",     "-",        "-",        "-",        "P2100/P2200 Oil Booster Pump Shutdown Relay (Inverted)"),
    ("DO", 1, 8, 9,  "TS8-09", "TB-08 (19&20)",   "EDB1 (P3600/3700)","P3600_P3700",     "Local:8:O.Data.9",   "%Q00004", "24V DC",     "-",        "-",        "-",        "P3600/P3700 Water Booster Pump Shutdown Relay (Inverted)"),
    ("DO", 1, 8, 10, "TS8-10", "TB-08 (21&22)",   "PLC_FAULT",       "PLC_Fault",        "Local:8:O.Data.10",  "%Q00016", "24V DC",     "-",        "-",        "-",        "PLC System Fault Output"),
    ("DO", 1, 8, 11, "TS8-11", "TB-08 (23&24)",   "FGCP-7404-001 L14","Tag_DO_13",       "Local:8:O.Data.11",  "%Q00013", "24V DC",     "-",        "-",        "-",        "ESDV Fuel Gas Line Closed LED (L14)"),
    ("DO", 1, 8, 12, "TS8-12", "TB-08 (25&26)",   "FGCP-7404-001 L15","Tag_DO_12",       "Local:8:O.Data.12",  "%Q00012", "24V DC",     "-",        "-",        "-",        "ESDV Fuel Gas Line Open LED (L15)"),
    ("DO", 1, 8, 13, "TS8-13", "TB-08 (27&28)",   "FGCP-7404-001 L16","Tag_DO_14",       "Local:8:O.Data.13",  "%Q00014", "24V DC",     "-",        "-",        "-",        "ESDV Low Air Supply Indication LED (L16)"),
    ("DO", 1, 8, 14, "TS8-14", "TB-08 (29&30)",   "FGCP-7404-001 L17","LED_Low_Fuel_Gas_L17","Local:8:O.Data.14","NEW",   "24V DC",     "-",        "-",        "-",        "Low Fuel Gas Pressure Indication LED (L17)"),
    ("DO", 1, 8, 15, "TS8-15", "TB-08 (31..34)",  "FGCP-7404-001 CR1","CR1_P2300_Stop",  "Local:8:O.Data.15",  "NEW",     "24V DC",     "-",        "-",        "-",        "Relay CR1 for LED L2 & L8 (Trip Power Oil Pump P-2300)"),
    ("DO", 1, 8, 16, "TS8-16", "TB-08 (35..38)",  "FGCP-7404-001 CR2","CR2_P2400_Stop",  "Local:8:O.Data.16",  "NEW",     "24V DC",     "-",        "-",        "-",        "Relay CR2 for LED L3 & L9 (Trip Power Oil Pump P-2400)"),
    ("DO", 1, 8, 17, "TS8-17", "TB-08 (39..42)",  "FGCP-7404-001 CR3","CR3_P2500_Stop",  "Local:8:O.Data.17",  "NEW",     "24V DC",     "-",        "-",        "-",        "Relay CR3 for LED L4 & L10 (Trip Power Oil Pump P-2500)"),
    ("DO", 1, 8, 18, "TS8-18", "TB-08 (43..46)",  "FGCP-7404-001 CR4","CR4_P2600_Stop",  "Local:8:O.Data.18",  "NEW",     "24V DC",     "-",        "-",        "-",        "Relay CR4 for LED L5 & L11 (Trip Power Oil Pump P-2600)"),
    ("DO", 1, 8, 19, "TS8-19", "TB-08 (47..50)",  "FGCP-7404-001 CR5","CR5_P3800_Stop",  "Local:8:O.Data.19",  "NEW",     "24V DC",     "-",        "-",        "-",        "Relay CR5 for LED L6 & L12 (Trip Water Inj Pump P-3800)"),
    ("DO", 1, 8, 20, "TS8-20", "TB-08 (51..54)",  "FGCP-7404-001 CR6","CR6_P3900_Stop",  "Local:8:O.Data.20",  "NEW",     "24V DC",     "-",        "-",        "-",        "Relay CR6 for LED L7 & L13 (Trip Water Inj Pump P-3900)"),
    ("DO", 1, 8, 21, "TS8-21", "TB-08 (55&56)",   "SD-GE",           "SD_GE",            "Local:8:O.Data.21",  "NEW",     "24V DC",     "-",        "-",        "-",        "7404-ESD-GEN Shut Down of All Gas Generators"),
    ("DO", 1, 8, 22, "TS8-22", "TB-08 (57&58)",   "FGCP-7404-001 Z1","Tag_DO_15",        "Local:8:O.Data.22",  "%Q00015", "24V DC",     "-",        "-",        "-",        "PROD CONTROL ROOM Alarm Buzzer/Beacon (Z1)"),
    ("DO", 1, 8, 23, "TS8-23", "TB-08 (59&60)",   "PA-001",          "PA_001",           "Local:8:O.Data.23",  "NEW",     "24V DC",     "-",        "-",        "-",        "PROCESS (PROD, BUILDING) Alarm Horn/Beacon"),
    ("DO", 1, 8, 30, "TS8-30", "TB-08 (73&74)",   "H2SA-001/002",    "H2SA_001_002",     "Local:8:O.Data.30",  "NEW",     "24V DC",     "-",        "-",        "-",        "H2S Alarm Horn/Beacon (Discontinuous 10ppm / Cont. 20ppm)"),
    ("DO", 1, 8, 31, "TS8-31", "TB-08 (75&76)",   "SDA-001",         "SDA_001",          "Local:8:O.Data.31",  "NEW",     "24V DC",     "-",        "-",        "-",        "Smoke Detection Alarm Horn/Beacon"),

    # === SLOT 9: MVI56E-MCM (Modbus RS-485 Master/Slave Module) ===
    ("MODBUS", 1, 9, 1, "RS-485", "P1/P2",        "P2300",           "MCM_P2300_Status", "Local:9:I.Data[0]",  "MODBUS",  "RS-485",     "-",        "-",        "-",        "Murphy Panel P-2300 Power Oil Pump (TTD-H Annunciator)"),
    ("MODBUS", 1, 9, 2, "RS-485", "P1/P2",        "P2400",           "MCM_P2400_Status", "Local:9:I.Data[1]",  "MODBUS",  "RS-485",     "-",        "-",        "-",        "Murphy Panel P-2400 Power Oil Pump (TTD-H Annunciator)"),
    ("MODBUS", 1, 9, 3, "RS-485", "P1/P2",        "P2500",           "MCM_P2500_Status", "Local:9:I.Data[2]",  "MODBUS",  "RS-485",     "-",        "-",        "-",        "Murphy Panel P-2500 Power Oil Pump (TTD-H Annunciator)"),
    ("MODBUS", 1, 9, 4, "RS-485", "P1/P2",        "P2600",           "MCM_P2600_Status", "Local:9:I.Data[3]",  "MODBUS",  "RS-485",     "-",        "-",        "-",        "Murphy Panel P-2600 Power Oil Pump (Murphy S1501)"),
    ("MODBUS", 1, 9, 5, "RS-485", "P1/P2",        "P3800",           "MCM_P3800_Status", "Local:9:I.Data[4]",  "MODBUS",  "RS-485",     "-",        "-",        "-",        "Murphy Panel P-3800 Water Injection Pump (TTD-H)"),
    ("MODBUS", 1, 9, 6, "RS-485", "P1/P2",        "P3900",           "MCM_P3900_Status", "Local:9:I.Data[5]",  "MODBUS",  "RS-485",     "-",        "-",        "-",        "Murphy Panel P-3900 Water Injection Pump (TTD-H)"),
    ("MODBUS", 1, 9, 7, "RS-485", "P1/P2",        "6401-FT-001",     "FT_6401_001",      "Local:9:I.Data[6]",  "MODBUS",  "0-500 bbl/h","30 bbl/h", "300 bbl/h","N/A",      "Flowmeter Oil Expedition (FIT-001 / 6401-FT-001)"),
    ("MODBUS", 1, 9, 8, "RS-485", "P1/P2",        "V-710",           "MCM_V710_Status",  "Local:9:I.Data[7]",  "MODBUS",  "RS-485",     "-",        "-",        "-",        "Heater Treater V-710 CompactLogix 1769-L30ER"),
    ("MODBUS", 1, 9, 9, "RS-485", "P1/P2",        "V-810",           "MCM_V810_Status",  "Local:9:I.Data[8]",  "MODBUS",  "RS-485",     "-",        "-",        "-",        "Heater Treater V-810 CompactLogix 1769-L30ER"),
]


# ---------------------------------------------------------------------------
# 2. ALLEN-BRADLEY STUDIO 5000 STRUCTURED TEXT (ST) ROUTINES
# ---------------------------------------------------------------------------
ROUTINES = [
    (
        "MainRoutine",
        "Main Executive Routine (Converted from GE VersaMax _MAIN + GNTF Upgrade Extensions)",
        """// ============================================================================
// Routine: MainRoutine (Converted from GE VersaMax _MAIN)
// Project: GNTF QUINGUILA CONTROL SYSTEM UPGRADE (01-MAN-03-11 / P20890_Angola)
// Target : Allen-Bradley ControlLogix 5580 (1756-L82E), Studio 5000 v28+
// ============================================================================

// Rung 1: First Scan Initialization & Free-Running Flasher Timers
First_Scan := S:FS;

TMR_Flash_Slow.PRE := 400; // 400 ms (0.4s)
TMR_Flash_Slow.TimerEnable := NOT TMR_Flash_Fast.DN;
TMR_Flash_Slow.Reset := First_Scan;
TONR(TMR_Flash_Slow);

TMR_Flash_Fast.PRE := 400; // 400 ms (0.4s)
TMR_Flash_Fast.TimerEnable := TMR_Flash_Slow.DN;
TMR_Flash_Fast.Reset := First_Scan;
TONR(TMR_Flash_Fast);

// Rung 2: 0.4s Toggle Flasher (R01598_0)
IF TMR_Flash_Slow.DN AND NOT R01598_1 THEN
    R01598_0 := NOT R01598_0;
END_IF;
R01598_1 := TMR_Flash_Slow.DN;

// Rung 3: Secondary Toggle Divider (R01598_2)
IF R01598_0 AND NOT R01598_3 THEN
    R01598_2 := NOT R01598_2;
END_IF;
R01598_3 := R01598_0;

// Rung 4: Tertiary Toggle Divider (R01598_4)
IF R01598_2 AND NOT R01598_5 THEN
    R01598_4 := NOT R01598_4;
END_IF;
R01598_5 := R01598_2;

// Rung 5: Quaternary Toggle Divider (R01598_6)
IF R01598_4 AND NOT R01598_7 THEN
    R01598_6 := NOT R01598_6;
END_IF;
R01598_7 := R01598_4;

// Rung 6: Execute Initialization Subroutine on First Scan
IF First_Scan THEN
    JSR(Init);
END_IF;

// Rung 7: Input Mapping & Digital/Analog Input Processing
JSR(Input);
JSR(DI_1);
JSR(DI_2);
JSR(AI_1);
JSR(AI_2);
JSR(AI_3);
JSR(AI_4_New); // GNTF Upgrade: New AI channels (GD-001..003, PIT-001..003, H2S-001..012, DF-003, SD-001/002, LIT-100..400, FT-001)

// Rung 8: Analog Alarm Threshold Evaluation & Voting
JSR(Ai_AL_1);
JSR(Ai_AL_2);
JSR(Ai_AL_3);
JSR(Vote_1);

// Rung 9: Cause & Effect Logic, Deluge Pump Control, Sounders & Outputs
JSR(Logic);
JSR(CE_LOG);
JSR(Sound);
JSR(Output);
"""
    ),
    (
        "Init",
        "First-Scan Setpoint & Calibration Initialization (01-MAN-03-13-PDF-C1 & Legacy Init)",
        """// ============================================================================
// Routine: Init (Initialization of Calibration Ranges & Alarm Setpoints)
// Reference: List of Parameters and Set Points (01-MAN-03-13-PDF-C1)
//            Cause & Effect Matrix (01-MAN-03-07-PDF-C2C Final)
// ============================================================================

// --- 1. CH4 Point Gas Detectors 7404-DG-001..012 (0 - 100 %LEL, Low=20, High=30) ---
// Legacy GE raw counts (32000 = 100%): 0-100% LEL, HiFault=105, LoFault=-4, HiAlarm=30, LoAlarm=20
R00101 := 0.0;     R00103 := 100.0;   R00105 := 105.0;   R00107 := -4.0;    R00109 := 30.0;    R00111 := 20.0; // 7404-DG-001
R00121 := 0.0;     R00123 := 100.0;   R00125 := 105.0;   R00127 := -4.0;    R00129 := 30.0;    R00131 := 20.0; // 7404-DG-002
R00141 := 0.0;     R00143 := 100.0;   R00145 := 105.0;   R00147 := -4.0;    R00149 := 30.0;    R00151 := 20.0; // 7404-DG-003
R00161 := 0.0;     R00163 := 100.0;   R00165 := 105.0;   R00167 := -4.0;    R00169 := 30.0;    R00171 := 20.0; // 7404-DG-004
R00181 := 0.0;     R00183 := 100.0;   R00185 := 105.0;   R00187 := -4.0;    R00189 := 30.0;    R00191 := 20.0; // 7404-DG-005
R00201 := 0.0;     R00203 := 100.0;   R00205 := 105.0;   R00207 := -4.0;    R00209 := 30.0;    R00211 := 20.0; // 7404-DG-006
R00221 := 0.0;     R00223 := 100.0;   R00225 := 105.0;   R00227 := -4.0;    R00229 := 30.0;    R00231 := 20.0; // 7404-DG-007
R00241 := 0.0;     R00243 := 100.0;   R00245 := 105.0;   R00247 := -4.0;    R00249 := 30.0;    R00251 := 20.0; // 7404-DG-008
R00261 := 0.0;     R00263 := 100.0;   R00265 := 105.0;   R00267 := -4.0;    R00269 := 30.0;    R00271 := 20.0; // 7404-DG-009
R00281 := 0.0;     R00283 := 100.0;   R00285 := 105.0;   R00287 := -4.0;    R00289 := 30.0;    R00291 := 20.0; // 7404-DG-010
R00301 := 0.0;     R00303 := 100.0;   R00305 := 105.0;   R00307 := -4.0;    R00309 := 30.0;    R00311 := 20.0; // 7404-DG-011 (was SpareAI_11)
R00381 := 0.0;     R00383 := 100.0;   R00385 := 105.0;   R00387 := -4.0;    R00389 := 30.0;    R00391 := 20.0; // 7404-DG-012 (was SpareAI_15)

// --- 2. Flame Detectors 7404-DF-001..002 (0 - 100%, HiAlarm=30%) ---
R00321 := 0.0;     R00323 := 100.0;   R00325 := 105.0;   R00327 := -4.0;    R00329 := 30.0;    R00331 := 101.0; // 7404-DF-001
R00341 := 0.0;     R00343 := 100.0;   R00345 := 105.0;   R00347 := -4.0;    R00349 := 30.0;    R00351 := 101.0; // 7404-DF-002

// --- 3. Open-Path Gas Detector 7404-DG-011R (0 - 5.00 LELm, Low=1.00, High=3.00) ---
R00361 := 0.0;     R00363 := 5.00;    R00365 := 5.10;    R00367 := -0.78125; R00369 := 3.00;   R00371 := 1.00;  // 7404-DG-011R
R00581 := -0.46875; // Beam Block / Optic Fault upper window (-0.78125 to -0.46875 LELm)

// --- 4. Pressure Transmitters & Manual Call Points (Slot 3) ---
R00401 := 0.0;     R00403 := 100.0;   R00405 := 105.0;   R00407 := -4.0;    R00409 := 30.0;    R00411 := 20.0;  // SpareAI_16
R00421 := 0.0;     R00423 := 100.0;   R00425 := 105.0;   R00427 := -4.0;    R00429 := -10.0;   R00431 := 50.0;  // 7002-PST-001 (Air Accumulator PAL=50 psi)
R00441 := 0.0;     R00443 := 150.0;   R00445 := 155.0;   R00447 := -4.0;    R00449 := 100.0;   R00451 := 40.0;  // 6401-PST-001 (Fuel Gas PAL=40 psi, PAH=100 psi)
R00461 := 0.0;     R00463 := 100.0;   R00465 := 102.0;   R00467 := -4.0;    R00469 := 50.0;    R00471 := 101.0; // 7503-PST-001 (Deluge Pressure PAH=50 psi)
R00481 := 0.0;     R00483 := 100.0;   R00485 := 105.0;   R00487 := -4.0;    R00489 := 30.0;    R00491 := 101.0; // 7503-FR-001/002 (Outside Foam MAC)
R00501 := 0.0;     R00503 := 100.0;   R00505 := 105.0;   R00507 := -4.0;    R00509 := 30.0;    R00511 := 20.0;  // SpareAI_21
R00521 := 0.0;     R00523 := 100.0;   R00525 := 105.0;   R00527 := -4.0;    R00529 := 30.0;    R00531 := 101.0; // 7503-FR-003 (Inside Foam MAC)
R00541 := 0.0;     R00543 := 100.0;   R00545 := 105.0;   R00547 := -4.0;    R00549 := 30.0;    R00551 := 20.0;  // SpareAI_23
R00561 := 0.0;     R00563 := 100.0;   R00565 := 105.0;   R00567 := -4.0;    R00569 := 30.0;    R00571 := 20.0;  // SpareAI_24

// --- 5. GNTF Upgrade New Instrument Setpoints (01-MAN-03-13-PDF-C1) ---
// Gas Generator Room CH4 Detectors GD-001..003 (0-100 %LEL)
SP_GD_Low_LEL        := 20.0;   // Low Gas Alarm = 20% LEL
SP_GD_High_LEL       := 30.0;   // High Gas Alarm = 30% LEL (Trips SD-GE on 2oo3 or 1ooN per C&E)

// H2S Detectors H2S-001..012 (0-100 PPM)
SP_H2S_Low_PPM       := 10.0;   // Low H2S Alarm = 10 PPM (Discontinuous H2SA-001/002 + Z1)
SP_H2S_High_PPM      := 20.0;   // High H2S Alarm = 20 PPM (Continuous H2SA-001/002 + Z1)

// Flame Detector 7404-DF-003 & Smoke Detectors SD-001/002 (0-100 %)
SP_DF003_High        := 30.0;   // Flame Detector 3 Fire Threshold = 30%
SP_SD_High           := 30.0;   // Smoke Detector 1/2 Fire Threshold = 30% (Trips SD-GE + SDA-001 + Z1)

// Manifold Pressure Transmitters PIT-001, PIT-002, PIT-003
SP_PIT001_PAL        := 10.0;   // Oil Expedition Low Pressure = 10 Psi
SP_PIT001_PAH        := 100.0;  // Oil Expedition High Pressure = 100 Psi
SP_PIT002_PAL        := 200.0;  // Water Injection Low Pressure = 200 Psi
SP_PIT002_PAH        := 800.0;  // Water Injection High Pressure = 800 Psi
SP_PIT002_PAHH       := 900.0;  // Water Injection High-High Pressure = 900 Psi (Trips P-3800/3900 & P-3600/3700)
SP_PIT003_PAL        := 1700.0; // Oil Injection Low Pressure = 1700 Psi
SP_PIT003_PAH        := 2700.0; // Oil Injection High Pressure = 2700 Psi
SP_PIT003_PAHH       := 2800.0; // Oil Injection High-High Pressure = 2800 Psi (Trips P-2300..2600 & P-2100/2200)

// Tank Level Transmitters LIT-100..400 (Slot 6 1756-IF8H)
SP_LIT100_LAL        := 0.7;    SP_LIT100_LAH := 9.0;   // Tank T-100 (0-10.0 m)
SP_LIT200_LAL        := 0.7;    SP_LIT200_LAH := 9.0;   // Tank T-200 (0-10.0 m)
SP_LIT300_LAL        := 0.7;    SP_LIT300_LAH := 9.0;   // Tank T-300 (0-10.0 m)
SP_LIT400_LAL        := 0.7;    SP_LIT400_LAH := 11.0;  // Tank T-400 (0-12.0 m)

// Oil Expedition Flowmeter 6401-FT-001 (Slot 9 Modbus MVI56E-MCM)
SP_FT001_FAL         := 30.0;   // Low Flow Alarm = 30 bbl/h
SP_FT001_FAH         := 300.0;  // High Flow Alarm = 300 bbl/h
"""
    ),
    (
        "Input",
        "Hardware Input Acquisition & Mapping (Slot 2-7 1756 Modules -> Internal Tags)",
        """// ============================================================================
// Routine: Input (Hardware Input Mapping from 1756 ControlLogix I/O Modules)
// Reference: IO List 01-MAN-03-06-PDF-C2C Final & Terminal Block 01-MAN-02-13
// ============================================================================

// --- 1. SLOT 7: 1756-IB32 Digital Inputs (Local:7:I.Data.0 .. 20) ---
ZSH_6401_001         := Local:7:I.Data.0;  // TS7-00: 6401-ZSH-001 ESD Valve Open
ZSL_6401_001         := Local:7:I.Data.1;  // TS7-01: 6401-ZSL-001 ESD Valve Closed
FS_FGCP_E8           := Local:7:I.Data.2;  // TS7-02: FGCP-7404-001 E8 Stop Foam Button (Legacy SpareDI_08)
SpareDI_08           := FS_FGCP_E8;
LS_7503_002          := Local:7:I.Data.3;  // TS7-03: 7503-LS-002 Diesel Tank Low Level
FS_7503_001          := Local:7:I.Data.4;  // TS7-04: 7503-FS-001 Field Stop Foam Button
LS_7503_001          := Local:7:I.Data.5;  // TS7-05: 7503-LS-001 AFFF Foam Tank Low Level
Pump_A_PulsIn        := Local:7:I.Data.6;  // TS7-06: 75-C-01A Pulsed Input from Q05 for Open Circuit Check
Pump_B_Start_PulsIn  := Local:7:I.Data.7;  // TS7-07: 75-C-01B Pulsed Input from Q07 for Open Circuit Check
Pump_B_Inhibited     := Local:7:I.Data.8;  // TS7-08: 75-SB-01B Standby Pump B Inhibited
SpareDI_11           := Local:7:I.Data.9;  // TS7-09: Spare Digital Input 11
Reset_PB_E11         := Local:7:I.Data.10; // TS7-10: FGCP-7404-001 E11 Reset Alarm Pushbutton
Mute_PB_E12          := Local:7:I.Data.11; // TS7-11: FGCP-7404-001 E12 Mute Alarm Pushbutton
ESDV_6401_001        := Local:7:I.Data.12; // TS7-12: 6401-ESDV-001 (E9) ESD Fuel Gas Button
INHIBIT_FOAM_REL     := Local:7:I.Data.13; // TS7-13: FGCP-7404-001 S2 Inhibit Foam Release Keyswitch
INHIBIT_ALL_OUTPUTS  := Local:7:I.Data.14; // TS7-14: FGCP-7404-001 S3 Inhibit All Outputs Keyswitch
ESTOP_P2300_E1       := Local:7:I.Data.15; // TS7-15: 7404-SB-004 (E1) E-Stop Power Oil Pump P-2300
ESTOP_P2400_E2       := Local:7:I.Data.16; // TS7-16: 7404-SB-005 (E2) E-Stop Power Oil Pump P-2400
ESTOP_P2500_E3       := Local:7:I.Data.17; // TS7-17: 7404-SB-006 (E3) E-Stop Power Oil Pump P-2500
ESTOP_P2600_E4       := Local:7:I.Data.18; // TS7-18: 7404-SB-007 (E4) E-Stop Power Oil Pump P-2600
ESTOP_P3800_E5       := Local:7:I.Data.19; // TS7-19: 7404-SB-008 (E5) E-Stop Water Inj Pump P-3800
ESTOP_P3900_E6       := Local:7:I.Data.20; // TS7-20: 7404-SB-009 (E6) E-Stop Water Inj Pump P-3900

// Combine Panel Pushbuttons (E11 Reset / E12 Mute) with SCADA HMI Commands (M00001 / M00002)
M00001_System_Accept := M00001 OR Mute_PB_E12;
M00002_System_Reset  := M00002 OR Reset_PB_E11;

// Map Legacy Digital Input Image Bits (G0001..G0013)
G0001 := ZSH_6401_001;
G0002 := ZSL_6401_001;
G0003 := FS_7503_001;
G0004 := LS_7503_001;
G0005 := LS_7503_002;
G0006 := Pump_A_PulsIn;
G0007 := Pump_B_Start_PulsIn;
G0008 := FS_FGCP_E8;
G0009 := Pump_B_Inhibited;
G0010 := ESDV_6401_001;
G0011 := SpareDI_11;
G0012 := INHIBIT_FOAM_REL;
G0013 := INHIBIT_ALL_OUTPUTS;

// --- 2. SLOT 2, 3, 4: 1756-IF16 Analog Inputs (Mapped to Legacy Raw 0..32000 Register Image R00001..R00024) ---
// Note: 1756-IF16 channels configured for 0..32000 raw counts (4mA=0, 20mA=32000) to preserve exact CalcVa1/2/3 scaling
DG_7404_001      := Local:2:I.Ch0Data;   R00001 := DG_7404_001;      // Slot 2 Ch 0: 7404-DG-001
DG_7404_002      := Local:2:I.Ch1Data;   R00002 := DG_7404_002;      // Slot 2 Ch 1: 7404-DG-002
DG_7404_003      := Local:2:I.Ch2Data;   R00003 := DG_7404_003;      // Slot 2 Ch 2: 7404-DG-003
DG_7404_004      := Local:2:I.Ch3Data;   R00004 := DG_7404_004;      // Slot 2 Ch 3: 7404-DG-004
DG_7404_005      := Local:2:I.Ch4Data;   R00005 := DG_7404_005;      // Slot 2 Ch 4: 7404-DG-005
DG_7404_006      := Local:2:I.Ch5Data;   R00006 := DG_7404_006;      // Slot 2 Ch 5: 7404-DG-006
DG_7404_007      := Local:2:I.Ch6Data;   R00007 := DG_7404_007;      // Slot 2 Ch 6: 7404-DG-007
DG_7404_008      := Local:2:I.Ch7Data;   R00008 := DG_7404_008;      // Slot 2 Ch 7: 7404-DG-008
DG_7404_009      := Local:2:I.Ch8Data;   R00009 := DG_7404_009;      // Slot 2 Ch 8: 7404-DG-009
DG_7404_010      := Local:2:I.Ch9Data;   R00010 := DG_7404_010;      // Slot 2 Ch 9: 7404-DG-010
DG_7404_011      := Local:2:I.Ch10Data;  R00011 := DG_7404_011;      // Slot 2 Ch 10: 7404-DG-011 (was SpareAI_11)
DF_7404_001      := Local:4:I.Ch12Data;  R00012 := DF_7404_001;      // Slot 4 Ch 12: 7404-DF-001
DF_7404_002      := Local:4:I.Ch13Data;  R00013 := DF_7404_002;      // Slot 4 Ch 13: 7404-DF-002
DG_7404_011R     := Local:2:I.Ch12Data;  R00014 := DG_7404_011R;     // Slot 2 Ch 12: 7404-DG-011R Open Path
DG_7404_012      := Local:2:I.Ch11Data;  R00015 := DG_7404_012;      // Slot 2 Ch 11: 7404-DG-012 (was SpareAI_15)
SpareAI_16       := Local:3:I.Ch8Data;   R00016 := SpareAI_16;       // Slot 3 Ch 8: SpareAI_16
PST_7002_001     := Local:3:I.Ch4Data;   R00017 := PST_7002_001;     // Slot 3 Ch 4: 7002-PST-001 Air Accumulator
PST_6401_001     := Local:3:I.Ch5Data;   R00018 := PST_6401_001;     // Slot 3 Ch 5: 6401-PST-001 Fuel Gas Pressure
PST_7503_001     := Local:3:I.Ch3Data;   R00019 := PST_7503_001;     // Slot 3 Ch 3: 7503-PST-001 Deluge Pressure
FR_7503_001_002  := Local:3:I.Ch7Data;   R00020 := FR_7503_001_002;  // Slot 3 Ch 7: 7503-FR-001/002 Outside Foam MAC
SpareAI_21       := Local:3:I.Ch9Data;   R00021 := SpareAI_21;       // Slot 3 Ch 9: SpareAI_21
FR_7503_003      := Local:3:I.Ch6Data;   R00022 := FR_7503_003;      // Slot 3 Ch 6: 7503-FR-003 Inside Foam MAC
SpareAI_23       := Local:3:I.Ch10Data;  R00023 := SpareAI_23;       // Slot 3 Ch 10: SpareAI_23
SpareAI_24       := Local:3:I.Ch11Data;  R00024 := SpareAI_24;       // Slot 3 Ch 11: SpareAI_24
"""
    ),
    (
        "DI_1",
        "Digital Input Conditioning & ESDV Discrepancy Logic (6401-ZSH/ZSL-001, 7503-FS/LS)",
        """// ============================================================================
// Routine: DI_1 (Digital Input Conditioning & ESD Valve Discrepancy Timers)
// ============================================================================

// --- 1. 6401-ZSH-001 & 6401-ZSL-001 (ESDV Limit Switches & Position Discrepancy) ---
R00700_0 := G0001; // 6401-ZSH-001 Open
R00700_1 := G0002; // 6401-ZSL-001 Closed

// Both Open & Closed switches active simultaneously (Fault)
R00700_2 := R00700_0 AND R00700_1;

// Neither Open nor Closed switch active (Valve in transit > 10.0s -> Discrepancy Fault)
TMR_ESDV_Transit.PRE := 10000; // 10.0s (100 * 0.1s)
TMR_ESDV_Transit.TimerEnable := NOT R00700_0 AND NOT R00700_1;
TMR_ESDV_Transit.Reset := FALSE;
TONR(TMR_ESDV_Transit);
R00700_3 := TMR_ESDV_Transit.DN;

// Valve commanded open (R01511_0) but not open within 10.0s
TMR_ESDV_CmdOpen.PRE := 10000;
TMR_ESDV_CmdOpen.TimerEnable := R01511_0 AND NOT R00700_0;
TMR_ESDV_CmdOpen.Reset := FALSE;
TONR(TMR_ESDV_CmdOpen);
R00700_4 := TMR_ESDV_CmdOpen.DN;

// Valve commanded closed (NOT R01511_0) but not closed within 10.0s
TMR_ESDV_CmdClose.PRE := 10000;
TMR_ESDV_CmdClose.TimerEnable := NOT R01511_0 AND NOT R00700_1;
TMR_ESDV_CmdClose.Reset := FALSE;
TONR(TMR_ESDV_CmdClose);
R00700_5 := TMR_ESDV_CmdClose.DN;

// Consolidated ESDV Discrepancy Latch (R00700_6)
IF R00700_2 OR R00700_3 OR R00700_4 OR R00700_5 THEN
    R00700_6 := TRUE;
ELSIF M00002_System_Reset THEN
    R00700_6 := FALSE;
END_IF;

// --- 2. 7503-FS-001 Field Stop Foam Button & FGCP E8 Stop Foam Button ---
// Field Stop Foam Button is Normally-Closed (0 = Pressed/Stop, 1 = Healthy)
R00701_0 := NOT G0003 OR G0008; // Foam Stop Requested (Field FS-001 or Panel E8)
IF R00701_0 THEN
    R00701_1 := TRUE;
ELSIF M00002_System_Reset AND NOT R00701_0 THEN
    R00701_1 := FALSE;
END_IF;

// --- 3. 7503-LS-001 AFFF Foam Tank Low Level Switch (NC: 0 = Low Level Alarm) ---
R00702_0 := NOT G0004;
IF R00702_0 THEN
    R00702_1 := TRUE;
ELSIF M00002_System_Reset AND NOT R00702_0 THEN
    R00702_1 := FALSE;
END_IF;

// --- 4. 7503-LS-002 Diesel Tank Low Level Switch (NC: 0 = Low Level Alarm) ---
R00703_0 := NOT G0005;
IF R00703_0 THEN
    R00703_1 := TRUE;
ELSIF M00002_System_Reset AND NOT R00703_0 THEN
    R00703_1 := FALSE;
END_IF;
"""
    ),
    (
        "DI_2",
        "Digital Input Conditioning Part 2 (Deluge Line Continuity, Pump B Inhibit, E9 ESDV, S2/S3 Inhibits, E1..E6 Pump E-Stops)",
        """// ============================================================================
// Routine: DI_2 (Deluge Coil Continuity Check, Keyswitches & E1..E6 E-Stops)
// ============================================================================

// --- 1. Pump A & Pump B Start Coil Open-Circuit Monitoring (Pulsed Check) ---
// Every 60s, pulse Q09 (Pump_A_PulsOut) & Q10 (Pump_B_Start_PulsOut) for 1.0s and verify G0006/G0007
TMR_Pulse_Period.PRE := 60000; // 60.0s interval
TMR_Pulse_Period.TimerEnable := NOT TMR_Pulse_Width.DN;
TMR_Pulse_Period.Reset := First_Scan;
TONR(TMR_Pulse_Period);

TMR_Pulse_Width.PRE := 1000; // 1.0s test pulse
TMR_Pulse_Width.TimerEnable := TMR_Pulse_Period.DN;
TMR_Pulse_Width.Reset := First_Scan;
TONR(TMR_Pulse_Width);

R01513_12 := TMR_Pulse_Period.DN AND NOT R01512_0; // Pump_A_PulsOut
R01513_13 := TMR_Pulse_Period.DN AND NOT R01512_5; // Pump_B_Start_PulsOut

// Fault if test pulse is active for > 500ms without feedback on G0006 / G0007
TMR_PumpA_WireFlt.PRE := 500;
TMR_PumpA_WireFlt.TimerEnable := R01513_12 AND NOT G0006;
TMR_PumpA_WireFlt.Reset := M00002_System_Reset;
TONR(TMR_PumpA_WireFlt);
IF TMR_PumpA_WireFlt.DN THEN
    R00704_1 := TRUE; // Pump A Start Line Open-Circuit Fault
ELSIF M00002_System_Reset THEN
    R00704_1 := FALSE;
END_IF;

TMR_PumpB_WireFlt.PRE := 500;
TMR_PumpB_WireFlt.TimerEnable := R01513_13 AND NOT G0007;
TMR_PumpB_WireFlt.Reset := M00002_System_Reset;
TONR(TMR_PumpB_WireFlt);
IF TMR_PumpB_WireFlt.DN THEN
    R00705_1 := TRUE; // Pump B Start Line Open-Circuit Fault
ELSIF M00002_System_Reset THEN
    R00705_1 := FALSE;
END_IF;

// --- 2. Standby Pump B Inhibited (G0009 / 75-SB-01B) ---
R00706_0 := G0009;

// --- 3. 6401-ESDV-001 (E9) ESD Fuel Gas Pushbutton (NC Fail-Safe: 0 = Pressed) ---
R00707_0 := NOT G0010;
IF R00707_0 THEN
    R00707_1 := TRUE; // Latched ESD Fuel Gas Pushbutton Trip
ELSIF M00002_System_Reset AND NOT R00707_0 THEN
    R00707_1 := FALSE;
END_IF;

// --- 4. Keyswitches S2 (Inhibit Foam Release) & S3 (Inhibit All Outputs) ---
R00708_0 := G0012; // INHIBIT_FOAM_REL (S2)
R00709_0 := G0013; // INHIBIT_ALL_OUTPUTS (S3)

// --- 5. GNTF Upgrade: Emergency Stop Pushbuttons E1..E6 (7404-SB-004..009) ---
// Per Cause & Effect 01-MAN-03-07-PDF-C2C:
//   E1 (7404-SB-004) -> Trips Power Oil Pump P-2300 (CR1: LED L2 & L8) + Z1
//   E2 (7404-SB-005) -> Trips Power Oil Pump P-2400 (CR2: LED L3 & L9) + Z1
//   E3 (7404-SB-006) -> Trips Power Oil Pump P-2500 (CR3: LED L4 & L10) + Z1
//   E4 (7404-SB-007) -> Trips Power Oil Pump P-2600 (CR4: LED L5 & L11) + Z1
//   E5 (7404-SB-008) -> Trips Water Inj Pump P-3800 (CR5: LED L6 & L12) + Z1
//   E6 (7404-SB-009) -> Trips Water Inj Pump P-3900 (CR6: LED L7 & L13) + Z1
IF ESTOP_P2300_E1 THEN Latch_ESTOP_P2300 := TRUE; ELSIF M00002_System_Reset THEN Latch_ESTOP_P2300 := FALSE; END_IF;
IF ESTOP_P2400_E2 THEN Latch_ESTOP_P2400 := TRUE; ELSIF M00002_System_Reset THEN Latch_ESTOP_P2400 := FALSE; END_IF;
IF ESTOP_P2500_E3 THEN Latch_ESTOP_P2500 := TRUE; ELSIF M00002_System_Reset THEN Latch_ESTOP_P2500 := FALSE; END_IF;
IF ESTOP_P2600_E4 THEN Latch_ESTOP_P2600 := TRUE; ELSIF M00002_System_Reset THEN Latch_ESTOP_P2600 := FALSE; END_IF;
IF ESTOP_P3800_E5 THEN Latch_ESTOP_P3800 := TRUE; ELSIF M00002_System_Reset THEN Latch_ESTOP_P3800 := FALSE; END_IF;
IF ESTOP_P3900_E6 THEN Latch_ESTOP_P3900 := TRUE; ELSIF M00002_System_Reset THEN Latch_ESTOP_P3900 := FALSE; END_IF;
"""
    ),
    (
        "CalcVa1",
        "Analog Scaling Subroutine 1 (7404-DG-001 .. 7404-DG-008)",
        """// ============================================================================
// Routine: CalcVa1 (Engineering Unit Scaling for Analog Channels 1..8)
// Formula: EU = ((Span - Zero) / 32000.0) * Raw + Zero
// ============================================================================

R00113 := ((R00103 - R00101) / 32000.0) * DINT_TO_REAL(R00001) + R00101; // 7404-DG-001 (%LEL)
R00133 := ((R00123 - R00121) / 32000.0) * DINT_TO_REAL(R00002) + R00121; // 7404-DG-002 (%LEL)
R00153 := ((R00143 - R00141) / 32000.0) * DINT_TO_REAL(R00003) + R00141; // 7404-DG-003 (%LEL)
R00173 := ((R00163 - R00161) / 32000.0) * DINT_TO_REAL(R00004) + R00161; // 7404-DG-004 (%LEL)
R00193 := ((R00183 - R00181) / 32000.0) * DINT_TO_REAL(R00005) + R00181; // 7404-DG-005 (%LEL)
R00213 := ((R00203 - R00201) / 32000.0) * DINT_TO_REAL(R00006) + R00201; // 7404-DG-006 (%LEL)
R00233 := ((R00223 - R00221) / 32000.0) * DINT_TO_REAL(R00007) + R00221; // 7404-DG-007 (%LEL)
R00253 := ((R00243 - R00241) / 32000.0) * DINT_TO_REAL(R00008) + R00241; // 7404-DG-008 (%LEL)
"""
    ),
    (
        "CalcVa2",
        "Analog Scaling Subroutine 2 (7404-DG-009..012, DF-001..002, DG-011R, SpareAI_16)",
        """// ============================================================================
// Routine: CalcVa2 (Engineering Unit Scaling for Analog Channels 9..16)
// Formula: EU = ((Span - Zero) / 32000.0) * Raw + Zero
// ============================================================================

R00273 := ((R00263 - R00261) / 32000.0) * DINT_TO_REAL(R00009) + R00261; // 7404-DG-009 (%LEL)
R00293 := ((R00283 - R00281) / 32000.0) * DINT_TO_REAL(R00010) + R00281; // 7404-DG-010 (%LEL)
R00313 := ((R00303 - R00301) / 32000.0) * DINT_TO_REAL(R00011) + R00301; // 7404-DG-011 (%LEL)
R00333 := ((R00323 - R00321) / 32000.0) * DINT_TO_REAL(R00012) + R00321; // 7404-DF-001 (%)
R00353 := ((R00343 - R00341) / 32000.0) * DINT_TO_REAL(R00013) + R00341; // 7404-DF-002 (%)
R00373 := ((R00363 - R00361) / 32000.0) * DINT_TO_REAL(R00014) + R00361; // 7404-DG-011R (LELm)
R00393 := ((R00383 - R00381) / 32000.0) * DINT_TO_REAL(R00015) + R00381; // 7404-DG-012 (%LEL)
R00413 := ((R00403 - R00401) / 32000.0) * DINT_TO_REAL(R00016) + R00401; // SpareAI_16 (%)
"""
    ),
    (
        "CalcVa3",
        "Analog Scaling Subroutine 3 (7002-PST-001, 6401-PST-001, 7503-PST-001, 7503-FR-001/002/003)",
        """// ============================================================================
// Routine: CalcVa3 (Engineering Unit Scaling for Analog Channels 17..24)
// Formula: EU = ((Span - Zero) / 32000.0) * Raw + Zero
// ============================================================================

R00433 := ((R00423 - R00421) / 32000.0) * DINT_TO_REAL(R00017) + R00421; // 7002-PST-001 Air Accumulator (Psi)
R00453 := ((R00443 - R00441) / 32000.0) * DINT_TO_REAL(R00018) + R00441; // 6401-PST-001 Fuel Gas Pressure (Psi)
R00473 := ((R00463 - R00461) / 32000.0) * DINT_TO_REAL(R00019) + R00461; // 7503-PST-001 Deluge Pressure (Psi)
R00493 := ((R00483 - R00481) / 32000.0) * DINT_TO_REAL(R00020) + R00481; // 7503-FR-001/002 Outside Foam MAC (%)
R00513 := ((R00503 - R00501) / 32000.0) * DINT_TO_REAL(R00021) + R00501; // SpareAI_21 (%)
R00533 := ((R00523 - R00521) / 32000.0) * DINT_TO_REAL(R00022) + R00521; // 7503-FR-003 Inside Foam MAC (%)
R00553 := ((R00543 - R00541) / 32000.0) * DINT_TO_REAL(R00023) + R00541; // SpareAI_23 (%)
R00573 := ((R00563 - R00561) / 32000.0) * DINT_TO_REAL(R00024) + R00561; // SpareAI_24 (%)
"""
    ),
    (
        "AI_1",
        "Analog Input Processing & Fault Detection Group 1 (7404-DG-001 .. 7404-DG-008)",
        """// ============================================================================
// Routine: AI_1 (Scaling & Out-of-Range Fault Detection for Channels 1..8)
// ============================================================================

JSR(CalcVa1);

// Channel 1: 7404-DG-001
R00115_0 := (R00113 > R00105); // High Fault (> 105%)
R00115_1 := (R00113 < R00107); // Low Fault (< -4%)
R00115_2 := R00115_0 OR R00115_1;

// Channel 2: 7404-DG-002
R00135_0 := (R00133 > R00125);
R00135_1 := (R00133 < R00127);
R00135_2 := R00135_0 OR R00135_1;

// Channel 3: 7404-DG-003
R00155_0 := (R00153 > R00145);
R00155_1 := (R00153 < R00147);
R00155_2 := R00155_0 OR R00155_1;

// Channel 4: 7404-DG-004
R00175_0 := (R00173 > R00165);
R00175_1 := (R00173 < R00167);
R00175_2 := R00175_0 OR R00175_1;

// Channel 5: 7404-DG-005
R00195_0 := (R00193 > R00185);
R00195_1 := (R00193 < R00187);
R00195_2 := R00195_0 OR R00195_1;

// Channel 6: 7404-DG-006
R00215_0 := (R00213 > R00205);
R00215_1 := (R00213 < R00207);
R00215_2 := R00215_0 OR R00215_1;

// Channel 7: 7404-DG-007
R00235_0 := (R00233 > R00225);
R00235_1 := (R00233 < R00227);
R00235_2 := R00235_0 OR R00235_1;

// Channel 8: 7404-DG-008
R00255_0 := (R00253 > R00245);
R00255_1 := (R00253 < R00247);
R00255_2 := R00255_0 OR R00255_1;
"""
    ),
    (
        "AI_2",
        "Analog Input Processing & Fault Detection Group 2 (7404-DG-009..012, DF-001..002, DG-011R)",
        """// ============================================================================
// Routine: AI_2 (Scaling & Out-of-Range Fault Detection for Channels 9..16)
// ============================================================================

JSR(CalcVa2);

// Channel 9: 7404-DG-009
R00275_0 := (R00273 > R00265);
R00275_1 := (R00273 < R00267);
R00275_2 := R00275_0 OR R00275_1;

// Channel 10: 7404-DG-010
R00295_0 := (R00293 > R00285);
R00295_1 := (R00293 < R00287);
R00295_2 := R00295_0 OR R00295_1;

// Channel 11: 7404-DG-011 (Pump House IR Point Detector 11)
R00315_0 := (R00313 > R00305);
R00315_1 := (R00313 < R00307);
R00315_2 := R00315_0 OR R00315_1;

// Channel 12: 7404-DF-001 (Flame Detector 1)
R00335_0 := (R00333 > R00325);
R00335_1 := (R00333 < R00327);
R00335_2 := R00335_0 OR R00335_1;

// Channel 13: 7404-DF-002 (Flame Detector 2)
R00355_0 := (R00353 > R00345);
R00355_1 := (R00353 < R00347);
R00355_2 := R00355_0 OR R00355_1;

// Channel 14: 7404-DG-011R (Open Path Gas Detector 0..5.00 LELm)
R00375_0 := (R00373 > R00365); // High Fault (> 5.10 LELm)
R00375_1 := (R00373 < R00367); // Low Fault (< -0.78125 LELm)
// Optic Fault / Beam Block window (-0.78125 <= EU <= -0.46875 LELm)
R00375_7 := (R00373 >= R00367) AND (R00373 <= R00581);
R00375_2 := R00375_0 OR R00375_1 OR R00375_7;

// Channel 15: 7404-DG-012 (Pump House IR Point Detector 12)
R00395_0 := (R00393 > R00385);
R00395_1 := (R00393 < R00387);
R00395_2 := R00395_0 OR R00395_1;

// Channel 16: SpareAI_16
R00415_0 := (R00413 > R00405);
R00415_1 := (R00413 < R00407);
R00415_2 := R00415_0 OR R00415_1;
"""
    ),
    (
        "AI_3",
        "Analog Input Processing & Fault Detection Group 3 (PST-001s & Foam Call Points FR-001..003)",
        """// ============================================================================
// Routine: AI_3 (Scaling & Out-of-Range Fault Detection for Channels 17..24)
// ============================================================================

JSR(CalcVa3);

// Channel 17: 7002-PST-001 (Air Accumulator Pressure 0..100 Psi)
R00435_0 := (R00433 > R00425);
R00435_1 := (R00433 < R00427);
R00435_2 := R00435_0 OR R00435_1;

// Channel 18: 6401-PST-001 (Fuel Gas Pressure 0..150 Psi)
R00455_0 := (R00453 > R00445);
R00455_1 := (R00453 < R00447);
R00455_2 := R00455_0 OR R00455_1;

// Channel 19: 7503-PST-001 (Deluge Line Pressure 0..100 Psi)
R00475_0 := (R00473 > R00465);
R00475_1 := (R00473 < R00467);
R00475_2 := R00475_0 OR R00475_1;

// Channel 20: 7503-FR-001/002 (Outside Manual Foam Release Call Points)
R00495_0 := (R00493 > R00485);
R00495_1 := (R00493 < R00487);
R00495_2 := R00495_0 OR R00495_1;

// Channel 21: SpareAI_21
R00515_0 := (R00513 > R00505);
R00515_1 := (R00513 < R00507);
R00515_2 := R00515_0 OR R00515_1;

// Channel 22: 7503-FR-003 (Inside Control Room Manual Foam Release Call Point)
R00535_0 := (R00533 > R00525);
R00535_1 := (R00533 < R00527);
R00535_2 := R00535_0 OR R00535_1;

// Channel 23: SpareAI_23
R00555_0 := (R00553 > R00545);
R00555_1 := (R00553 < R00547);
R00555_2 := R00555_0 OR R00555_1;

// Channel 24: SpareAI_24
R00575_0 := (R00573 > R00565);
R00575_1 := (R00573 < R00567);
R00575_2 := R00575_0 OR R00575_1;
"""
    ),
    (
        "AI_4_New",
        "GNTF Upgrade New Analog, HART & Modbus Channels (GD-001..003, PIT-001..003, H2S-001..012, DF-003, SD-001/002, LIT-100..400, FT-001)",
        """// ============================================================================
// Routine: AI_4_New (GNTF Control System Upgrade New Instruments Scaling & Alarms)
// Reference:
//   - IO List:          01-MAN-03-06-PDF-C2C Final
//   - Terminal Blocks:  01-MAN-02-13-PDF-C1A
//   - Setpoints List:   01-MAN-03-13-PDF-C1
//   - Cause & Effect:   01-MAN-03-07-PDF-C2C Final
//   - Alarms & Events:  01-MAN-03-02-PDF-C2 Final
// ============================================================================

// --- 1. SLOT 2 (Ch 13..15): Gas Generator Room CH4 Detectors GD-001..003 (0-100 %LEL) ---
GD_001_EU := (100.0 / 32000.0) * DINT_TO_REAL(Local:2:I.Ch13Data);
GD_002_EU := (100.0 / 32000.0) * DINT_TO_REAL(Local:2:I.Ch14Data);
GD_003_EU := (100.0 / 32000.0) * DINT_TO_REAL(Local:2:I.Ch15Data);

GD_001_Fault := (GD_001_EU > 105.0) OR (GD_001_EU < -4.0);
GD_002_Fault := (GD_002_EU > 105.0) OR (GD_002_EU < -4.0);
GD_003_Fault := (GD_003_EU > 105.0) OR (GD_003_EU < -4.0);

GD_001_Lo := NOT GD_001_Fault AND (GD_001_EU >= SP_GD_Low_LEL);
GD_002_Lo := NOT GD_002_Fault AND (GD_002_EU >= SP_GD_Low_LEL);
GD_003_Lo := NOT GD_003_Fault AND (GD_003_EU >= SP_GD_Low_LEL);

GD_001_Hi := NOT GD_001_Fault AND (GD_001_EU >= SP_GD_High_LEL);
GD_002_Hi := NOT GD_002_Fault AND (GD_002_EU >= SP_GD_High_LEL);
GD_003_Hi := NOT GD_003_Fault AND (GD_003_EU >= SP_GD_High_LEL);

// Latching Gas Generator Room Alarms (Reset via M00002_System_Reset)
IF GD_001_Lo OR GD_002_Lo OR GD_003_Lo THEN
    GD_Any_Lo_Latch := TRUE;
ELSIF M00002_System_Reset THEN
    GD_Any_Lo_Latch := FALSE;
END_IF;

// Per C&E 01-MAN-03-07: High Gas (>=30% LEL) on GD-001..003 initiates SD-GE (Shut Down of All Gas Generators)
IF GD_001_Hi OR GD_002_Hi OR GD_003_Hi THEN
    GD_Any_Hi_Latch := TRUE;
ELSIF M00002_System_Reset THEN
    GD_Any_Hi_Latch := FALSE;
END_IF;

// --- 2. SLOT 3 (Ch 0..2): Manifold Pressure Transmitters PIT-001, PIT-002, PIT-003 ---
// PIT-001: Oil Expedition Manifold Pressure (0 - 200 Psi, PAL=10 Psi, PAH=100 Psi)
PIT_001_EU    := (200.0 / 32000.0) * DINT_TO_REAL(Local:3:I.Ch0Data);
PIT_001_Fault := (PIT_001_EU > 210.0) OR (PIT_001_EU < -8.0);
PIT_001_PAL   := NOT PIT_001_Fault AND (PIT_001_EU <= SP_PIT001_PAL);
PIT_001_PAH   := NOT PIT_001_Fault AND (PIT_001_EU >= SP_PIT001_PAH);

// PIT-002: Water Injection Manifold Pressure (0 - 1500 Psi, PAL=200, PAH=800, PAHH=900 Psi)
PIT_002_EU    := (1500.0 / 32000.0) * DINT_TO_REAL(Local:3:I.Ch1Data);
PIT_002_Fault := (PIT_002_EU > 1575.0) OR (PIT_002_EU < -60.0);
PIT_002_PAL   := NOT PIT_002_Fault AND (PIT_002_EU <= SP_PIT002_PAL);
PIT_002_PAH   := NOT PIT_002_Fault AND (PIT_002_EU >= SP_PIT002_PAH);
PIT_002_PAHH  := NOT PIT_002_Fault AND (PIT_002_EU >= SP_PIT002_PAHH);
IF PIT_002_PAHH THEN
    PIT_002_PAHH_Latch := TRUE; // Trips Water Injection Pumps P-3800/3900 & Booster P-3600/3700
ELSIF M00002_System_Reset AND NOT PIT_002_PAHH THEN
    PIT_002_PAHH_Latch := FALSE;
END_IF;

// PIT-003: Oil Injection Manifold Pressure (0 - 3000 Psi, PAL=1700, PAH=2700, PAHH=2800 Psi)
PIT_003_EU    := (3000.0 / 32000.0) * DINT_TO_REAL(Local:3:I.Ch2Data);
PIT_003_Fault := (PIT_003_EU > 3150.0) OR (PIT_003_EU < -120.0);
PIT_003_PAL   := NOT PIT_003_Fault AND (PIT_003_EU <= SP_PIT003_PAL);
PIT_003_PAH   := NOT PIT_003_Fault AND (PIT_003_EU >= SP_PIT003_PAH);
PIT_003_PAHH  := NOT PIT_003_Fault AND (PIT_003_EU >= SP_PIT003_PAHH);
IF PIT_003_PAHH THEN
    PIT_003_PAHH_Latch := TRUE; // Trips Power Oil Pumps P-2300..2600 & Oil Booster P-2100/2200
ELSIF M00002_System_Reset AND NOT PIT_003_PAHH THEN
    PIT_003_PAHH_Latch := FALSE;
END_IF;

// --- 3. SLOT 4 (Ch 0..11): H2S Gas Detectors H2S-001..012 (0 - 100 PPM, Low=10 PPM, High=20 PPM) ---
H2S_001_EU := (100.0 / 32000.0) * DINT_TO_REAL(Local:4:I.Ch0Data);
H2S_002_EU := (100.0 / 32000.0) * DINT_TO_REAL(Local:4:I.Ch1Data);
H2S_003_EU := (100.0 / 32000.0) * DINT_TO_REAL(Local:4:I.Ch2Data);
H2S_004_EU := (100.0 / 32000.0) * DINT_TO_REAL(Local:4:I.Ch3Data);
H2S_005_EU := (100.0 / 32000.0) * DINT_TO_REAL(Local:4:I.Ch4Data);
H2S_006_EU := (100.0 / 32000.0) * DINT_TO_REAL(Local:4:I.Ch5Data);
H2S_007_EU := (100.0 / 32000.0) * DINT_TO_REAL(Local:4:I.Ch6Data);
H2S_008_EU := (100.0 / 32000.0) * DINT_TO_REAL(Local:4:I.Ch7Data);
H2S_009_EU := (100.0 / 32000.0) * DINT_TO_REAL(Local:4:I.Ch8Data);
H2S_010_EU := (100.0 / 32000.0) * DINT_TO_REAL(Local:4:I.Ch9Data);
H2S_011_EU := (100.0 / 32000.0) * DINT_TO_REAL(Local:4:I.Ch10Data);
H2S_012_EU := (100.0 / 32000.0) * DINT_TO_REAL(Local:4:I.Ch11Data);

H2S_Any_Lo := (H2S_001_EU >= SP_H2S_Low_PPM) OR (H2S_002_EU >= SP_H2S_Low_PPM) OR
              (H2S_003_EU >= SP_H2S_Low_PPM) OR (H2S_004_EU >= SP_H2S_Low_PPM) OR
              (H2S_005_EU >= SP_H2S_Low_PPM) OR (H2S_006_EU >= SP_H2S_Low_PPM) OR
              (H2S_007_EU >= SP_H2S_Low_PPM) OR (H2S_008_EU >= SP_H2S_Low_PPM) OR
              (H2S_009_EU >= SP_H2S_Low_PPM) OR (H2S_010_EU >= SP_H2S_Low_PPM) OR
              (H2S_011_EU >= SP_H2S_Low_PPM) OR (H2S_012_EU >= SP_H2S_Low_PPM);

H2S_Any_Hi := (H2S_001_EU >= SP_H2S_High_PPM) OR (H2S_002_EU >= SP_H2S_High_PPM) OR
              (H2S_003_EU >= SP_H2S_High_PPM) OR (H2S_004_EU >= SP_H2S_High_PPM) OR
              (H2S_005_EU >= SP_H2S_High_PPM) OR (H2S_006_EU >= SP_H2S_High_PPM) OR
              (H2S_007_EU >= SP_H2S_High_PPM) OR (H2S_008_EU >= SP_H2S_High_PPM) OR
              (H2S_009_EU >= SP_H2S_High_PPM) OR (H2S_010_EU >= SP_H2S_High_PPM) OR
              (H2S_011_EU >= SP_H2S_High_PPM) OR (H2S_012_EU >= SP_H2S_High_PPM);

IF H2S_Any_Lo THEN H2S_Lo_Latch := TRUE; ELSIF M00002_System_Reset THEN H2S_Lo_Latch := FALSE; END_IF;
IF H2S_Any_Hi THEN H2S_Hi_Latch := TRUE; ELSIF M00002_System_Reset THEN H2S_Hi_Latch := FALSE; END_IF;

// --- 4. SLOT 4 (Ch 14 & Ch 15): 7404-DF-003 (Flame Det 3) & SD-001/002 (Smoke Detectors) ---
DF_7404_003_EU    := (100.0 / 32000.0) * DINT_TO_REAL(Local:4:I.Ch14Data);
DF_7404_003_Fault := (DF_7404_003_EU > 105.0) OR (DF_7404_003_EU < -4.0);
DF_7404_003_Alarm := NOT DF_7404_003_Fault AND (DF_7404_003_EU >= SP_DF003_High);
IF DF_7404_003_Alarm THEN
    DF_7404_003_Latch := TRUE;
ELSIF M00002_System_Reset AND NOT DF_7404_003_Alarm THEN
    DF_7404_003_Latch := FALSE;
END_IF;

SD_001_002_EU    := (100.0 / 32000.0) * DINT_TO_REAL(Local:4:I.Ch15Data);
SD_001_002_Fault := (SD_001_002_EU > 105.0) OR (SD_001_002_EU < -4.0);
SD_001_002_Alarm := NOT SD_001_002_Fault AND (SD_001_002_EU >= SP_SD_High);
IF SD_001_002_Alarm THEN
    SD_001_002_Latch := TRUE; // Trips SD-GE (Gas Generators) + SDA-001 + Z1
ELSIF M00002_System_Reset AND NOT SD_001_002_Alarm THEN
    SD_001_002_Latch := FALSE;
END_IF;

// --- 5. SLOT 6 (Ch 0..3): 1756-IF8H HART Tank Level Transmitters LIT-100..400 ---
LIT_100_EU  := (10.0 / 32000.0) * DINT_TO_REAL(Local:6:I.Ch0Data);
LIT_200_EU  := (10.0 / 32000.0) * DINT_TO_REAL(Local:6:I.Ch1Data);
LIT_300_EU  := (10.0 / 32000.0) * DINT_TO_REAL(Local:6:I.Ch2Data);
LIT_400_EU  := (12.0 / 32000.0) * DINT_TO_REAL(Local:6:I.Ch3Data);

LIT_100_LAL := (LIT_100_EU <= SP_LIT100_LAL);  LIT_100_LAH := (LIT_100_EU >= SP_LIT100_LAH);
LIT_200_LAL := (LIT_200_EU <= SP_LIT200_LAL);  LIT_200_LAH := (LIT_200_EU >= SP_LIT200_LAH);
LIT_300_LAL := (LIT_300_EU <= SP_LIT300_LAL);  LIT_300_LAH := (LIT_300_EU >= SP_LIT300_LAH);
LIT_400_LAL := (LIT_400_EU <= SP_LIT400_LAL);  LIT_400_LAH := (LIT_400_EU >= SP_LIT400_LAH);

// --- 6. SLOT 9 (MVI56E-MCM): Oil Expedition Flowmeter 6401-FT-001 (0 - 500 bbl/h) ---
FT_6401_001_EU  := INT_TO_REAL(Local:9:I.Data[6]) / 10.0;
FT_6401_001_FAL := (FT_6401_001_EU <= SP_FT001_FAL);
FT_6401_001_FAH := (FT_6401_001_EU >= SP_FT001_FAH);
"""
    ),
    (
        "Ai_AL_1",
        "Analog Alarm Threshold & Latching Group 1 (7404-DG-001 .. 7404-DG-008)",
        """// ============================================================================
// Routine: Ai_AL_1 (Low & High Gas Alarm Evaluation for 7404-DG-001 .. 008)
// ============================================================================

// 7404-DG-001 (20% LEL Low, 30% LEL High)
R00115_3 := NOT R00115_2 AND (R00113 >= R00109); // High Gas Live
R00115_4 := NOT R00115_2 AND (R00113 >= R00111); // Low Gas Live
IF R00115_3 THEN R00115_5 := TRUE; ELSIF M00002_System_Reset THEN R00115_5 := FALSE; END_IF;
IF R00115_4 THEN R00115_6 := TRUE; ELSIF M00002_System_Reset THEN R00115_6 := FALSE; END_IF;

// 7404-DG-002
R00135_3 := NOT R00135_2 AND (R00133 >= R00129);
R00135_4 := NOT R00135_2 AND (R00133 >= R00131);
IF R00135_3 THEN R00135_5 := TRUE; ELSIF M00002_System_Reset THEN R00135_5 := FALSE; END_IF;
IF R00135_4 THEN R00135_6 := TRUE; ELSIF M00002_System_Reset THEN R00135_6 := FALSE; END_IF;

// 7404-DG-003
R00155_3 := NOT R00155_2 AND (R00153 >= R00149);
R00155_4 := NOT R00155_2 AND (R00153 >= R00151);
IF R00155_3 THEN R00155_5 := TRUE; ELSIF M00002_System_Reset THEN R00155_5 := FALSE; END_IF;
IF R00155_4 THEN R00155_6 := TRUE; ELSIF M00002_System_Reset THEN R00155_6 := FALSE; END_IF;

// 7404-DG-004
R00175_3 := NOT R00175_2 AND (R00173 >= R00169);
R00175_4 := NOT R00175_2 AND (R00173 >= R00171);
IF R00175_3 THEN R00175_5 := TRUE; ELSIF M00002_System_Reset THEN R00175_5 := FALSE; END_IF;
IF R00175_4 THEN R00175_6 := TRUE; ELSIF M00002_System_Reset THEN R00175_6 := FALSE; END_IF;

// 7404-DG-005
R00195_3 := NOT R00195_2 AND (R00193 >= R00189);
R00195_4 := NOT R00195_2 AND (R00193 >= R00191);
IF R00195_3 THEN R00195_5 := TRUE; ELSIF M00002_System_Reset THEN R00195_5 := FALSE; END_IF;
IF R00195_4 THEN R00195_6 := TRUE; ELSIF M00002_System_Reset THEN R00195_6 := FALSE; END_IF;

// 7404-DG-006
R00215_3 := NOT R00215_2 AND (R00213 >= R00209);
R00215_4 := NOT R00215_2 AND (R00213 >= R00211);
IF R00215_3 THEN R00215_5 := TRUE; ELSIF M00002_System_Reset THEN R00215_5 := FALSE; END_IF;
IF R00215_4 THEN R00215_6 := TRUE; ELSIF M00002_System_Reset THEN R00215_6 := FALSE; END_IF;

// 7404-DG-007
R00235_3 := NOT R00235_2 AND (R00233 >= R00229);
R00235_4 := NOT R00235_2 AND (R00233 >= R00231);
IF R00235_3 THEN R00235_5 := TRUE; ELSIF M00002_System_Reset THEN R00235_5 := FALSE; END_IF;
IF R00235_4 THEN R00235_6 := TRUE; ELSIF M00002_System_Reset THEN R00235_6 := FALSE; END_IF;

// 7404-DG-008
R00255_3 := NOT R00255_2 AND (R00253 >= R00249);
R00255_4 := NOT R00255_2 AND (R00253 >= R00251);
IF R00255_3 THEN R00255_5 := TRUE; ELSIF M00002_System_Reset THEN R00255_5 := FALSE; END_IF;
IF R00255_4 THEN R00255_6 := TRUE; ELSIF M00002_System_Reset THEN R00255_6 := FALSE; END_IF;
"""
    ),
    (
        "Ai_AL_2",
        "Analog Alarm Threshold & Latching Group 2 (7404-DG-009..012, DF-001..002, DG-011R)",
        """// ============================================================================
// Routine: Ai_AL_2 (Alarm Evaluation for DG-009..012, DF-001..002, DG-011R)
// ============================================================================

// 7404-DG-009
R00275_3 := NOT R00275_2 AND (R00273 >= R00269);
R00275_4 := NOT R00275_2 AND (R00273 >= R00271);
IF R00275_3 THEN R00275_5 := TRUE; ELSIF M00002_System_Reset THEN R00275_5 := FALSE; END_IF;
IF R00275_4 THEN R00275_6 := TRUE; ELSIF M00002_System_Reset THEN R00275_6 := FALSE; END_IF;

// 7404-DG-010
R00295_3 := NOT R00295_2 AND (R00293 >= R00289);
R00295_4 := NOT R00295_2 AND (R00293 >= R00291);
IF R00295_3 THEN R00295_5 := TRUE; ELSIF M00002_System_Reset THEN R00295_5 := FALSE; END_IF;
IF R00295_4 THEN R00295_6 := TRUE; ELSIF M00002_System_Reset THEN R00295_6 := FALSE; END_IF;

// 7404-DG-011 (Pump House Gas Detector 11)
R00315_3 := NOT R00315_2 AND (R00313 >= R00309);
R00315_4 := NOT R00315_2 AND (R00313 >= R00311);
IF R00315_3 THEN R00315_5 := TRUE; ELSIF M00002_System_Reset THEN R00315_5 := FALSE; END_IF;
IF R00315_4 THEN R00315_6 := TRUE; ELSIF M00002_System_Reset THEN R00315_6 := FALSE; END_IF;

// 7404-DF-001 (Flame Detector 1: Fire >= 30%)
R00335_3 := NOT R00335_2 AND (R00333 >= R00329);
IF R00335_3 THEN R00335_5 := TRUE; ELSIF M00002_System_Reset THEN R00335_5 := FALSE; END_IF;

// 7404-DF-002 (Flame Detector 2: Fire >= 30%)
R00355_3 := NOT R00355_2 AND (R00353 >= R00349);
IF R00355_3 THEN R00355_5 := TRUE; ELSIF M00002_System_Reset THEN R00355_5 := FALSE; END_IF;

// 7404-DG-011R (Open Path Gas Detector: Low >= 1.00 LELm, High >= 3.00 LELm)
R00375_3 := NOT R00375_2 AND (R00373 >= R00369);
R00375_4 := NOT R00375_2 AND (R00373 >= R00371);
IF R00375_3 THEN R00375_5 := TRUE; ELSIF M00002_System_Reset THEN R00375_5 := FALSE; END_IF;
IF R00375_4 THEN R00375_6 := TRUE; ELSIF M00002_System_Reset THEN R00375_6 := FALSE; END_IF;

// 7404-DG-012 (Pump House Gas Detector 12)
R00395_3 := NOT R00395_2 AND (R00393 >= R00389);
R00395_4 := NOT R00395_2 AND (R00393 >= R00391);
IF R00395_3 THEN R00395_5 := TRUE; ELSIF M00002_System_Reset THEN R00395_5 := FALSE; END_IF;
IF R00395_4 THEN R00395_6 := TRUE; ELSIF M00002_System_Reset THEN R00395_6 := FALSE; END_IF;
"""
    ),
    (
        "Ai_AL_3",
        "Analog Alarm Threshold & Latching Group 3 (PST-001s & Manual Foam Call Points FR-001..003)",
        """// ============================================================================
// Routine: Ai_AL_3 (Alarm Evaluation for PST-001s & Foam Call Points FR-001..003)
// ============================================================================

// 7002-PST-001: Air Accumulator Pressure ESDV (Low Pressure <= 50 Psi -> L16)
R00435_4 := NOT R00435_2 AND (R00433 <= R00431);
IF R00435_4 THEN R00435_6 := TRUE; ELSIF M00002_System_Reset THEN R00435_6 := FALSE; END_IF;

// 6401-PST-001: Fuel Gas Pressure (PAL <= 40 Psi -> L17, PAH >= 100 Psi -> ESD Trip)
R00455_3 := NOT R00455_2 AND (R00453 >= R00449); // High Pressure >= 100 Psi
R00455_4 := NOT R00455_2 AND (R00453 <= R00451); // Low Pressure <= 40 Psi
IF R00455_3 THEN R00455_5 := TRUE; ELSIF M00002_System_Reset THEN R00455_5 := FALSE; END_IF;
IF R00455_4 THEN R00455_6 := TRUE; ELSIF M00002_System_Reset THEN R00455_6 := FALSE; END_IF;

// 7503-PST-001: Deluge Line Pressure (PAH >= 50 Psi -> Foam/Deluge Released)
R00475_3 := NOT R00475_2 AND (R00473 >= R00469);
IF R00475_3 THEN R00475_5 := TRUE; ELSIF M00002_System_Reset THEN R00475_5 := FALSE; END_IF;

// 7503-FR-001/002: Manual Foam Release Call Points Outside (>= 30%)
R00495_3 := NOT R00495_2 AND (R00493 >= R00489);
IF R00495_3 THEN R00495_5 := TRUE; ELSIF M00002_System_Reset THEN R00495_5 := FALSE; END_IF;

// 7503-FR-003: Manual Foam Release Call Point Inside Local Control Panel (>= 30%)
R00535_3 := NOT R00535_2 AND (R00533 >= R00529);
IF R00535_3 THEN R00535_5 := TRUE; ELSIF M00002_System_Reset THEN R00535_5 := FALSE; END_IF;
"""
    ),
    (
        "Vote_1",
        "Detector Voting Logic (1oo12 / 2oo12 CH4 Point Gas Detectors, Open Path & Flame Detectors)",
        """// ============================================================================
// Routine: Vote_1 (Gas & Flame Detector Voting Matrix)
// Reference: Cause & Effect Matrix (01-MAN-03-07-PDF-C2C Final)
// ============================================================================

// --- 1. Count Active Low Gas (20% LEL) & High Gas (30% LEL) Across 7404-DG-001..012 + DG-011R ---
Vote_Gas_Lo_Count := 0;
IF R00115_6 THEN Vote_Gas_Lo_Count := Vote_Gas_Lo_Count + 1; END_IF; // DG-001
IF R00135_6 THEN Vote_Gas_Lo_Count := Vote_Gas_Lo_Count + 1; END_IF; // DG-002
IF R00155_6 THEN Vote_Gas_Lo_Count := Vote_Gas_Lo_Count + 1; END_IF; // DG-003
IF R00175_6 THEN Vote_Gas_Lo_Count := Vote_Gas_Lo_Count + 1; END_IF; // DG-004
IF R00195_6 THEN Vote_Gas_Lo_Count := Vote_Gas_Lo_Count + 1; END_IF; // DG-005
IF R00215_6 THEN Vote_Gas_Lo_Count := Vote_Gas_Lo_Count + 1; END_IF; // DG-006
IF R00235_6 THEN Vote_Gas_Lo_Count := Vote_Gas_Lo_Count + 1; END_IF; // DG-007
IF R00255_6 THEN Vote_Gas_Lo_Count := Vote_Gas_Lo_Count + 1; END_IF; // DG-008
IF R00275_6 THEN Vote_Gas_Lo_Count := Vote_Gas_Lo_Count + 1; END_IF; // DG-009
IF R00295_6 THEN Vote_Gas_Lo_Count := Vote_Gas_Lo_Count + 1; END_IF; // DG-010
IF R00315_6 THEN Vote_Gas_Lo_Count := Vote_Gas_Lo_Count + 1; END_IF; // DG-011
IF R00395_6 THEN Vote_Gas_Lo_Count := Vote_Gas_Lo_Count + 1; END_IF; // DG-012
IF R00375_6 THEN Vote_Gas_Lo_Count := Vote_Gas_Lo_Count + 1; END_IF; // DG-011R (1.00 LELm)

Vote_Gas_Hi_Count := 0;
IF R00115_5 THEN Vote_Gas_Hi_Count := Vote_Gas_Hi_Count + 1; END_IF; // DG-001
IF R00135_5 THEN Vote_Gas_Hi_Count := Vote_Gas_Hi_Count + 1; END_IF; // DG-002
IF R00155_5 THEN Vote_Gas_Hi_Count := Vote_Gas_Hi_Count + 1; END_IF; // DG-003
IF R00175_5 THEN Vote_Gas_Hi_Count := Vote_Gas_Hi_Count + 1; END_IF; // DG-004
IF R00195_5 THEN Vote_Gas_Hi_Count := Vote_Gas_Hi_Count + 1; END_IF; // DG-005
IF R00215_5 THEN Vote_Gas_Hi_Count := Vote_Gas_Hi_Count + 1; END_IF; // DG-006
IF R00235_5 THEN Vote_Gas_Hi_Count := Vote_Gas_Hi_Count + 1; END_IF; // DG-007
IF R00255_5 THEN Vote_Gas_Hi_Count := Vote_Gas_Hi_Count + 1; END_IF; // DG-008
IF R00275_5 THEN Vote_Gas_Hi_Count := Vote_Gas_Hi_Count + 1; END_IF; // DG-009
IF R00295_5 THEN Vote_Gas_Hi_Count := Vote_Gas_Hi_Count + 1; END_IF; // DG-010
IF R00315_5 THEN Vote_Gas_Hi_Count := Vote_Gas_Hi_Count + 1; END_IF; // DG-011
IF R00395_5 THEN Vote_Gas_Hi_Count := Vote_Gas_Hi_Count + 1; END_IF; // DG-012
IF R00375_5 THEN Vote_Gas_Hi_Count := Vote_Gas_Hi_Count + 1; END_IF; // DG-011R (3.00 LELm)

// Voting Outputs (R01500_0 = 1ooN Low Gas, R01500_1 = 2ooN Low Gas, R01500_2 = 1ooN High Gas, R01500_3 = 2ooN High Gas)
R01500_0 := (Vote_Gas_Lo_Count >= 1);
R01500_1 := (Vote_Gas_Lo_Count >= 2);
R01500_2 := (Vote_Gas_Hi_Count >= 1);
R01500_3 := (Vote_Gas_Hi_Count >= 2) OR R00375_5; // 2ooN Point High OR Open-Path DG-011R High (3.00 LELm)

// --- 2. Flame Detector Voting Across 7404-DF-001, 7404-DF-002 & New 7404-DF-003 ---
Vote_Flame_Count := 0;
IF R00335_5 THEN Vote_Flame_Count := Vote_Flame_Count + 1; END_IF; // 7404-DF-001
IF R00355_5 THEN Vote_Flame_Count := Vote_Flame_Count + 1; END_IF; // 7404-DF-002
IF DF_7404_003_Latch THEN Vote_Flame_Count := Vote_Flame_Count + 1; END_IF; // 7404-DF-003

R01501_0 := (Vote_Flame_Count >= 1); // 1oo3 Flame Alarm (Fire Warning / Bell / ESD Trip per C&E)
R01501_1 := (Vote_Flame_Count >= 2); // 2oo3 Confirmed Flame (Deluge / Foam Release)
"""
    ),
    (
        "Logic",
        "Deluge Pump A & Standby Pump B Automatic Start/Stop Sequencing",
        """// ============================================================================
// Routine: Logic (Deluge Firewater/Foam Pump A & Standby Pump B Sequencing)
// ============================================================================

// --- 1. Foam / Deluge Demand Trigger (R01512_10) ---
// Demand from: Confirmed Fire (R01501_0 / R01501_1), Outside Foam MAC (7503-FR-001/002),
// or Inside Control Room Foam MAC (7503-FR-003), unless inhibited by S2 (INHIBIT_FOAM_REL)
// or stopped by Foam Stop pushbuttons (7503-FS-001 / FGCP E8).
Foam_Release_Demand := (R01501_0 OR R00495_5 OR R00535_5)
                       AND NOT R00708_0
                       AND NOT R00709_0
                       AND NOT R00701_0;

// --- 2. Duty Deluge Pump A Control (PUMP_A / R01512_0) ---
IF Foam_Release_Demand AND NOT R00704_1 THEN
    R01512_0 := TRUE; // Start Duty Deluge Pump A
ELSIF R00701_0 OR M00002_System_Reset THEN
    R01512_0 := FALSE; // Stop Duty Deluge Pump A on Foam Stop PB or System Reset
END_IF;

// --- 3. Deluge Pressure Proving Timer (10.0s for 7503-PST-001 >= 50 Psi) ---
TMR_PumpA_FailToRun.PRE := 10000; // 10.0s
TMR_PumpA_FailToRun.TimerEnable := Foam_Release_Demand AND NOT R00475_3;
TMR_PumpA_FailToRun.Reset := M00002_System_Reset OR R00701_0;
TONR(TMR_PumpA_FailToRun);

// Standby Diesel Pump B Demand if Pump A fails to build 50 Psi within 10s (or Pump A wire fault)
Pump_B_Demand := Foam_Release_Demand
                 AND (TMR_PumpA_FailToRun.DN OR R00704_1)
                 AND NOT R00706_0  // Not Pump_B_Inhibited (75-SB-01B)
                 AND NOT R00703_0; // Not Diesel Tank Low Level (7503-LS-002)

// --- 4. Standby Pump B 3-Attempt Start Crank Sequence (2.0s ON / 2.0s OFF x 3) ---
TMR_PumpB_StartOn.PRE := 2000; // 2.0s crank pulse
TMR_PumpB_StartOn.TimerEnable := Pump_B_Demand AND NOT R00475_3 AND NOT TMR_PumpB_StartOff.DN AND (CTU_PumpB_Attempts.CV < 3);
TMR_PumpB_StartOn.Reset := NOT Pump_B_Demand OR R00475_3 OR M00002_System_Reset;
TONR(TMR_PumpB_StartOn);

TMR_PumpB_StartOff.PRE := 2000; // 2.0s rest between crank pulses
TMR_PumpB_StartOff.TimerEnable := TMR_PumpB_StartOn.DN;
TMR_PumpB_StartOff.Reset := NOT Pump_B_Demand OR R00475_3 OR M00002_System_Reset;
TONR(TMR_PumpB_StartOff);

CTU_PumpB_Attempts.PRE := 3;
CTU_PumpB_Attempts.CU := TMR_PumpB_StartOn.DN;
CTU_PumpB_Attempts.Reset := NOT Pump_B_Demand OR M00002_System_Reset;
CTUD(CTU_PumpB_Attempts);

// PUMP_B_START Output Pulse (R01512_5)
R01512_5 := Pump_B_Demand AND NOT R00475_3 AND NOT TMR_PumpB_StartOn.DN AND (CTU_PumpB_Attempts.CV < 3);

// --- 5. Standby Pump B Stop Pulse (2.0s pulse on Foam Stop button) ---
TMR_PumpB_StopPulse.PRE := 2000;
TMR_PumpB_StopPulse.TimerEnable := R00701_0;
TMR_PumpB_StopPulse.Reset := FALSE;
TONR(TMR_PumpB_StopPulse);
R01512_4 := R00701_0 AND NOT TMR_PumpB_StopPulse.DN; // PUMP_B_STOP
"""
    ),
    (
        "CE_LOG",
        "Master Cause & Effect Matrix Orchestrator (Calls Indicat, Shutdow, Protect, Loc_Al, FLT_1)",
        """// ============================================================================
// Routine: CE_LOG (Cause & Effect Matrix Orchestrator)
// Reference: CAUSE & EFFECT 01-MAN-03-07-PDF-C2C Final
// ============================================================================

JSR(Indicat);
JSR(Shutdow);
JSR(Protect);
JSR(Loc_Al);
JSR(FLT_1);
"""
    ),
    (
        "Indicat",
        "FGCP Front Panel LED Indicators (L14 Closed, L15 Open, L16 Low Air, L17 Low Fuel Gas, CR1..CR6 Pump LEDs)",
        """// ============================================================================
// Routine: Indicat (FGCP-7404-001 Panel LEDs & Individual Pump Relay Indicators)
// Reference: Cause & Effect 01-MAN-03-07-PDF-C2C & Terminal Block 01-MAN-02-13
// ============================================================================

// L15 (Tag_DO_12 / Local:8:O.Data.12): ESDV Fuel Gas Line Open LED (6401-ZSH-001)
R01513_0 := R00700_0;

// L14 (Tag_DO_13 / Local:8:O.Data.11): ESDV Fuel Gas Line Closed LED (6401-ZSL-001)
R01513_1 := R00700_1;

// L16 (Tag_DO_14 / Local:8:O.Data.13): ESDV Low Air Supply Pressure LED (7002-PST-001 <= 50 Psi)
R01513_2 := R00435_6;

// L17 (LED_Low_Fuel_Gas_L17 / Local:8:O.Data.14): Low Fuel Gas Pressure LED (6401-PST-001 <= 40 Psi)
LED_Low_Fuel_Gas_L17 := R00455_6;

// CR1..CR4 (Power Oil Pumps P-2300..P-2600 Stop & Panel LEDs L2..L5 / L8..L11)
// Tripped by: Individual E-Stop (E1..E4), Full ESD Trip (R01510_0), or High-High Oil Inj Pressure PIT-003 (2800 Psi)
CR1_P2300_Stop := (Latch_ESTOP_P2300 OR NOT R01510_0 OR PIT_003_PAHH_Latch) AND NOT R00709_0;
CR2_P2400_Stop := (Latch_ESTOP_P2400 OR NOT R01510_0 OR PIT_003_PAHH_Latch) AND NOT R00709_0;
CR3_P2500_Stop := (Latch_ESTOP_P2500 OR NOT R01510_0 OR PIT_003_PAHH_Latch) AND NOT R00709_0;
CR4_P2600_Stop := (Latch_ESTOP_P2600 OR NOT R01510_0 OR PIT_003_PAHH_Latch) AND NOT R00709_0;

// CR5..CR6 (Water Injection Pumps P-3800..P-3900 Stop & Panel LEDs L6..L7 / L12..L13)
// Tripped by: Individual E-Stop (E5..E6), Full ESD Trip (R01510_0), or High-High Water Inj Pressure PIT-002 (900 Psi)
CR5_P3800_Stop := (Latch_ESTOP_P3800 OR NOT R01510_0 OR PIT_002_PAHH_Latch) AND NOT R00709_0;
CR6_P3900_Stop := (Latch_ESTOP_P3900 OR NOT R01510_0 OR PIT_002_PAHH_Latch) AND NOT R00709_0;
"""
    ),
    (
        "Shutdow",
        "Emergency Shutdown Logic (ESD_TRIP, 6401-EY-001/002, P2100/2200, P3600/3700, SD-GE Gas Generators)",
        """// ============================================================================
// Routine: Shutdow (Emergency Shutdown Matrix per 01-MAN-03-07-PDF-C2C Final)
// Note: Fail-safe outputs are energized (TRUE) when healthy and de-energized (FALSE) on trip.
// ============================================================================

// --- 1. Master Fire & Gas / Process ESD Trip Condition ---
// Causes per 01-MAN-03-07-PDF-C2C Final:
//   - High Gas 30% LEL (R01500_2 / R01500_3) or Open-Path 3.00 LELm (R00375_5)
//   - Flame Detection >= 30% (7404-DF-001, 7404-DF-002, or 7404-DF-003 -> R01501_0)
//   - Manual Foam Release Call Points (7503-FR-001/002 or 7503-FR-003)
//   - Deluge Line Pressure High >= 50 Psi (7503-PST-001 -> R00475_5)
//   - High Fuel Gas Pressure >= 100 Psi (6401-PST-001 -> R00455_5)
//   - ESD Fuel Gas Pushbutton E9 (6401-ESDV-001 -> R00707_1)
ESD_Trip_Condition := (R01500_2 OR R01500_3 OR R01501_0 OR R00495_5 OR R00535_5 OR R00475_5 OR R00455_5)
                      AND NOT R00709_0; // Bypassed if S3 (INHIBIT_ALL_OUTPUTS) is active

// R01510_0 -> PumpShutdown (ESD_TRIP, Local:8:O.Data.0): Energized (1) = Healthy, De-energized (0) = Trip
R01510_0 := NOT ESD_Trip_Condition;

// R01511_0 -> 6401-EY-001/002 Fuel Gas ESDV Solenoid (Local:8:O.Data.1)
// Tripped by ESD_Trip_Condition OR E9 Pushbutton (6401-ESDV-001 / R00707_1)
R01511_0 := NOT (ESD_Trip_Condition OR (R00707_1 AND NOT R00709_0));

// R01511_1 -> P2100/P2200 Oil Booster Pump Shutdown Relay (Local:8:O.Data.8)
// Tripped by ESD_Trip_Condition OR High-High Oil Injection Manifold Pressure PIT-003 (2800 Psi)
R01511_1 := NOT (ESD_Trip_Condition OR (PIT_003_PAHH_Latch AND NOT R00709_0));

// R01511_2 -> P3600/P3700 Water Booster Pump Shutdown Relay (Local:8:O.Data.9)
// Tripped by ESD_Trip_Condition OR High-High Water Injection Manifold Pressure PIT-002 (900 Psi)
R01511_2 := NOT (ESD_Trip_Condition OR (PIT_002_PAHH_Latch AND NOT R00709_0));

// --- 2. GNTF Upgrade: SD-GE (7404-ESD-GEN Shut Down of All Gas Generators, Local:8:O.Data.21) ---
// Tripped by:
//   - High Gas 30% LEL in Gas Generator Room (GD-001, GD-002, or GD-003 -> GD_Any_Hi_Latch)
//   - Smoke Detection >= 30% in Electrical/Generator Room (SD-001/002 -> SD_001_002_Latch)
//   - Master ESD Trip Condition (ESD_Trip_Condition)
SD_GE := (GD_Any_Hi_Latch OR SD_001_002_Latch OR ESD_Trip_Condition) AND NOT R00709_0;
"""
    ),
    (
        "Protect",
        "Deluge & Foam Protection Status Mapping",
        """// ============================================================================
// Routine: Protect (Firewater / Foam Protection Status & Deluge Confirmation)
// ============================================================================

// Deluge / Foam System Activated Status (7503-PST-001 >= 50 Psi or Pump A/B Running)
Deluge_Released_Status := R00475_5;
Foam_System_Inhibited  := R00708_0 OR R00709_0;
"""
    ),
    (
        "Loc_Al",
        "Audible/Visual Alarm Sounder Modes (7404-SA-001/002, Z1, PA-001, H2SA-001/002, SDA-001)",
        """// ============================================================================
// Routine: Loc_Al (Audible & Visual Alarm Pattern Selection per C&E 01-MAN-03-07)
// ============================================================================

// --- 1. Pump House Bell 7404-SA-001/002 Mode Selection ---
// Discontinuous (Pulsing) on 1ooN Low Gas (20% LEL) or 1.00 LELm Open-Path
Bell_Mode_Discontinuous := R01500_0 AND NOT R01500_2 AND NOT R01501_0 AND NOT R00495_5 AND NOT R00535_5 AND NOT R00475_5;

// Continuous on High Gas (30% LEL / 3.00 LELm), Flame (DF-001..003), Foam MAC (FR-001..003), or Deluge Released (PST-001)
Bell_Mode_Continuous    := R01500_2 OR R01501_0 OR R00495_5 OR R00535_5 OR R00475_5;

// --- 2. PROD CONTROL ROOM Alarm Z1 (Tag_DO_15 / Local:8:O.Data.22) ---
// Triggered by any Fire, Gas, H2S, Smoke, Process Alarm, or System Fault, silenced by M00001_System_Accept (E12)
Any_Unaccepted_Alarm := R01500_0 OR R01500_2 OR R01501_0 OR R00495_5 OR R00535_5 OR R00475_5 OR
                        R00435_6 OR R00455_5 OR R00455_6 OR R00707_1 OR
                        GD_Any_Lo_Latch OR GD_Any_Hi_Latch OR
                        H2S_Lo_Latch OR H2S_Hi_Latch OR
                        SD_001_002_Latch OR
                        PIT_001_PAL OR PIT_001_PAH OR
                        PIT_002_PAL OR PIT_002_PAH OR PIT_002_PAHH_Latch OR
                        PIT_003_PAL OR PIT_003_PAH OR PIT_003_PAHH_Latch OR
                        LIT_100_LAL OR LIT_100_LAH OR LIT_200_LAL OR LIT_200_LAH OR
                        LIT_300_LAL OR LIT_300_LAH OR LIT_400_LAL OR LIT_400_LAH OR
                        FT_6401_001_FAL OR FT_6401_001_FAH OR
                        Latch_ESTOP_P2300 OR Latch_ESTOP_P2400 OR Latch_ESTOP_P2500 OR
                        Latch_ESTOP_P2600 OR Latch_ESTOP_P3800 OR Latch_ESTOP_P3900;

IF M00001_System_Accept THEN
    Alarm_Silence_Latch := TRUE;
ELSIF NOT Any_Unaccepted_Alarm OR M00002_System_Reset THEN
    Alarm_Silence_Latch := FALSE;
END_IF;

R01513_3 := Any_Unaccepted_Alarm AND NOT Alarm_Silence_Latch; // Z1 (Tag_DO_15)

// --- 3. PROCESS (PROD, BUILDING) Alarm PA-001 (Local:8:O.Data.23) ---
// Activated on Process Alarms (PIT-001..003, LIT-100..400, FT-001, 6401-PST-001, 7002-PST-001)
PA_001 := (PIT_001_PAL OR PIT_001_PAH OR PIT_002_PAL OR PIT_002_PAH OR PIT_002_PAHH_Latch OR
           PIT_003_PAL OR PIT_003_PAH OR PIT_003_PAHH_Latch OR
           LIT_100_LAL OR LIT_100_LAH OR LIT_200_LAL OR LIT_200_LAH OR
           LIT_300_LAL OR LIT_300_LAH OR LIT_400_LAL OR LIT_400_LAH OR
           FT_6401_001_FAL OR FT_6401_001_FAH OR R00435_6 OR R00455_5 OR R00455_6)
          AND NOT Alarm_Silence_Latch AND NOT R00709_0;

// --- 4. H2S Alarm Horn/Beacon H2SA-001/002 (Local:8:O.Data.30) ---
// Per C&E 01-MAN-03-07:
//   - 10 PPM (Low H2S): Discontinuous alarm (pulsed with R01598_0)
//   - 20 PPM (High H2S): Continuous alarm
H2SA_001_002 := ((H2S_Hi_Latch) OR (H2S_Lo_Latch AND R01598_0))
                AND NOT Alarm_Silence_Latch AND NOT R00709_0;

// --- 5. Smoke Detection Alarm Horn/Beacon SDA-001 (Local:8:O.Data.31) ---
// Per C&E 01-MAN-03-07: Continuous alarm on SD-001/002 >= 30%
SDA_001 := SD_001_002_Latch AND NOT Alarm_Silence_Latch AND NOT R00709_0;
"""
    ),
    (
        "FLT_1",
        "System, Transmitter & Line Fault Aggregation (PLC_Fault Output)",
        """// ============================================================================
// Routine: FLT_1 (System, I/O Module & Transmitter Fault Aggregation)
// ============================================================================

// Aggregate Transmitter Out-of-Range Faults, Open-Path Beam Block, Deluge Line Faults & ESDV Discrepancy
Any_Channel_Fault := R00115_2 OR R00135_2 OR R00155_2 OR R00175_2 OR
                     R00195_2 OR R00215_2 OR R00235_2 OR R00255_2 OR
                     R00275_2 OR R00295_2 OR R00315_2 OR R00335_2 OR
                     R00355_2 OR R00375_2 OR R00395_2 OR R00435_2 OR
                     R00455_2 OR R00475_2 OR R00495_2 OR R00535_2 OR
                     GD_001_Fault OR GD_002_Fault OR GD_003_Fault OR
                     PIT_001_Fault OR PIT_002_Fault OR PIT_003_Fault OR
                     DF_7404_003_Fault OR SD_001_002_Fault OR
                     R00700_6 OR R00704_1 OR R00705_1;

// PLC_Fault Output (Local:8:O.Data.10 / R01513_4): Fail-Safe (Energized = No Fault, De-energized = Fault)
R01513_4 := NOT Any_Channel_Fault;
"""
    ),
    (
        "Sound",
        "Pump House Alarm Bell Driver (7404-SA-001/002 Continuous vs Discontinuous Modulation)",
        """// ============================================================================
// Routine: Sound (7404-SA-001/002 Pump House Alarm Bell Driver)
// ============================================================================

// Drive 7404-SA-001/002 (R01511_3) Continuous or Discontinuous (modulated by 0.8s flasher R01598_0),
// silenced by M00001_System_Accept (E12) or inhibited by S3 (R00709_0)
R01511_3 := (Bell_Mode_Continuous OR (Bell_Mode_Discontinuous AND R01598_0))
            AND NOT Alarm_Silence_Latch
            AND NOT R00709_0;
"""
    ),
    (
        "Output",
        "Hardware Digital Output Driver (Internal Tags -> Slot 8 1756-OB32 Local:8:O.Data.0..31)",
        """// ============================================================================
// Routine: Output (Map Internal Control Signals to Slot 8 1756-OB32 Module)
// Reference: IO List 01-MAN-03-06-PDF-C2C Final & Terminal Block 01-MAN-02-13
// ============================================================================

// Map Legacy Internal Bits to Named Output Tags
PumpShutdown          := R01510_0;  // TS8-00: ESD_TRIP (Fail-safe: 1=Healthy, 0=Trip)
EY_6401_001_002       := R01511_0;  // TS8-01: 6401-EY-001/002 ESD Fuel Gas Valve
SA_7404_001_002       := R01511_3;  // TS8-02: 7404-SA-001/002 Local Alarm Bell Pump House
Pump_A_PulsOut        := R01513_12; // TS8-03: Pulsed Output for Pump A Line Check
PUMP_A                := R01512_0;  // TS8-04: Deluge Pump A Start/Stop
Pump_B_Start_PulsOut  := R01513_13; // TS8-05: Pulsed Output for Pump B Line Check
PUMP_B_START          := R01512_5;  // TS8-06: Deluge Pump B Start Pulse
PUMP_B_STOP           := R01512_4;  // TS8-07: Deluge Pump B Stop Pulse
P2100_P2200           := R01511_1;  // TS8-08: Oil Booster Pump Shutdown Relay (Fail-safe)
P3600_P3700           := R01511_2;  // TS8-09: Water Booster Pump Shutdown Relay (Fail-safe)
PLC_Fault             := R01513_4;  // TS8-10: PLC Fault Output
Tag_DO_13             := R01513_1;  // TS8-11: FGCP-7404-001 L14 ESDV Closed LED
Tag_DO_12             := R01513_0;  // TS8-12: FGCP-7404-001 L15 ESDV Open LED
Tag_DO_14             := R01513_2;  // TS8-13: FGCP-7404-001 L16 Low Air Supply LED
Tag_DO_15             := R01513_3;  // TS8-22: FGCP-7404-001 Z1 PROD CONTROL ROOM Alarm

// Write to Slot 8: 1756-OB32 Hardware Output Points (Local:8:O.Data.0 .. 31)
Local:8:O.Data.0      := PumpShutdown;          // TS8-00: ESD_TRIP
Local:8:O.Data.1      := EY_6401_001_002;       // TS8-01: 6401-EY-001/002
Local:8:O.Data.2      := SA_7404_001_002;       // TS8-02: 7404-SA-001/002
Local:8:O.Data.3      := Pump_A_PulsOut;        // TS8-03: 7503-PUMP-A Pulse Check
Local:8:O.Data.4      := PUMP_A;                // TS8-04: 7503-PUMP-A Start/Stop
Local:8:O.Data.5      := Pump_B_Start_PulsOut;  // TS8-05: 7503-PUMP-B Pulse Check
Local:8:O.Data.6      := PUMP_B_START;          // TS8-06: 7503-PUMP-B Start
Local:8:O.Data.7      := PUMP_B_STOP;           // TS8-07: 7503-PUMP-B Stop
Local:8:O.Data.8      := P2100_P2200;           // TS8-08: EDB1 (P2100/2200)
Local:8:O.Data.9      := P3600_P3700;           // TS8-09: EDB1 (P3600/3700)
Local:8:O.Data.10     := PLC_Fault;             // TS8-10: PLC_FAULT
Local:8:O.Data.11     := Tag_DO_13;             // TS8-11: FGCP-7404-001 L14 (ESDV Closed)
Local:8:O.Data.12     := Tag_DO_12;             // TS8-12: FGCP-7404-001 L15 (ESDV Open)
Local:8:O.Data.13     := Tag_DO_14;             // TS8-13: FGCP-7404-001 L16 (ESDV Low Air)
Local:8:O.Data.14     := LED_Low_Fuel_Gas_L17;  // TS8-14: FGCP-7404-001 L17 (Low Fuel Gas)
Local:8:O.Data.15     := CR1_P2300_Stop;        // TS8-15: CR1 (L2 & L8 / Stop P-2300)
Local:8:O.Data.16     := CR2_P2400_Stop;        // TS8-16: CR2 (L3 & L9 / Stop P-2400)
Local:8:O.Data.17     := CR3_P2500_Stop;        // TS8-17: CR3 (L4 & L10 / Stop P-2500)
Local:8:O.Data.18     := CR4_P2600_Stop;        // TS8-18: CR4 (L5 & L11 / Stop P-2600)
Local:8:O.Data.19     := CR5_P3800_Stop;        // TS8-19: CR5 (L6 & L12 / Stop P-3800)
Local:8:O.Data.20     := CR6_P3900_Stop;        // TS8-20: CR6 (L7 & L13 / Stop P-3900)
Local:8:O.Data.21     := SD_GE;                 // TS8-21: SD-GE (7404-ESD-GEN Gas Generators Shutdown)
Local:8:O.Data.22     := Tag_DO_15;             // TS8-22: FGCP-7404-001 Z1 (PROD CONTROL ROOM Alarm)
Local:8:O.Data.23     := PA_001;                // TS8-23: PA-001 (PROCESS PROD BUILDING Alarm)
Local:8:O.Data.30     := H2SA_001_002;          // TS8-30: H2SA-001/002 (H2S Alarm Horn/Beacon)
Local:8:O.Data.31     := SDA_001;               // TS8-31: SDA-001 (Smoke Detection Alarm Horn/Beacon)
"""
    ),
]

# ---------------------------------------------------------------------------
# 3. CONTROLLER TAGS REGISTRY (For Studio 5000 CSV & L5X Export)
# ---------------------------------------------------------------------------
def build_controller_tags():
    """Return list of (TagName, DataType, Description, AliasFor) tuples."""
    tags = []
    # 1. Hardware-mapped tags from IO_MAP
    for io_type, rack, slot, ch, ts, tb, inst_tag, ab_tag, ab_hw, ge_addr, rng, sp_lo, sp_hi, sp_hh, desc in IO_MAP:
        dtype = "BOOL" if io_type in ("DI", "DO") else ("INT" if io_type == "MODBUS" else "DINT")
        full_desc = f"[{inst_tag}] {desc} (Slot {slot} Ch {ch}, {tb}, Legacy: {ge_addr}, Range: {rng})"
        tags.append((ab_tag, dtype, full_desc, ab_hw))

    # 2. Internal Legacy GE Register & Bit Tags
    for i in range(1, 25):
        tags.append((f"R000{i:02d}", "DINT", f"Legacy GE Raw Analog Input Word %R000{i:02d} (0..32000)", ""))
    for i in range(1, 14):
        tags.append((f"G00{i:02d}", "BOOL", f"Legacy GE Digital Input Image Bit %G00{i:02d}", ""))

    # Analog calibration & EU registers (Channels 1..24: base = 100 + (ch-1)*20)
    for ch in range(1, 25):
        base = 100 + (ch - 1) * 20
        tags.append((f"R{base+1:05d}", "REAL", f"AI Ch {ch} Calibration Zero (Min EU)", ""))
        tags.append((f"R{base+3:05d}", "REAL", f"AI Ch {ch} Calibration Span (Max EU)", ""))
        tags.append((f"R{base+5:05d}", "REAL", f"AI Ch {ch} High Fault Threshold", ""))
        tags.append((f"R{base+7:05d}", "REAL", f"AI Ch {ch} Low Fault Threshold", ""))
        tags.append((f"R{base+9:05d}", "REAL", f"AI Ch {ch} High Alarm Setpoint (PAH/LAH)", ""))
        tags.append((f"R{base+11:05d}", "REAL", f"AI Ch {ch} Low Alarm Setpoint (PAL/LAL)", ""))
        tags.append((f"R{base+13:05d}", "REAL", f"AI Ch {ch} Scaled Engineering Value (EU)", ""))
        for b, bdesc in [
            (0, "High Out-of-Range Fault"),
            (1, "Low Out-of-Range Fault"),
            (2, "Combined Channel Fault"),
            (3, "High Alarm Live"),
            (4, "Low Alarm Live"),
            (5, "High Alarm Latched"),
            (6, "Low Alarm Latched"),
            (7, "Optic / Beam Block Fault"),
        ]:
            tags.append((f"R{base+15:05d}_{b}", "BOOL", f"AI Ch {ch} Status Bit {b}: {bdesc}", ""))

    tags.append(("R00581", "REAL", "7404-DG-011R Open Path Beam Block Upper Window (-0.46875 LELm)", ""))

    # Internal control & status bits
    internal_bools = [
        ("First_Scan", "Controller First Scan Bit (S:FS)"),
        ("M00001", "SCADA HMI System Accept / Mute Command (%M00001)"),
        ("M00002", "SCADA HMI System Reset Command (%M00002)"),
        ("M00001_System_Accept", "Combined System Accept / Mute (SCADA M00001 OR Panel PB E12)"),
        ("M00002_System_Reset", "Combined System Reset (SCADA M00002 OR Panel PB E11)"),
        ("SpareDI_08", "Legacy SpareDI_08 (Mapped to FGCP E8 Foam Stop Pushbutton)"),
        ("R01598_0", "0.4s / 0.8s Free-Running Flasher Bit 0"),
        ("R01598_1", "Flasher One-Shot Memory Bit 1"),
        ("R01598_2", "Flasher Divider Bit 2"),
        ("R01598_3", "Flasher One-Shot Memory Bit 3"),
        ("R01598_4", "Flasher Divider Bit 4"),
        ("R01598_5", "Flasher One-Shot Memory Bit 5"),
        ("R01598_6", "Flasher Divider Bit 6"),
        ("R01598_7", "Flasher One-Shot Memory Bit 7"),
        ("R00700_0", "6401-ZSH-001 ESDV Open Status"),
        ("R00700_1", "6401-ZSL-001 ESDV Closed Status"),
        ("R00700_2", "ESDV Both Open & Closed Limit Switches Active Fault"),
        ("R00700_3", "ESDV Transit Timeout Fault (>10s neither open nor closed)"),
        ("R00700_4", "ESDV Commanded Open Discrepancy Fault (>10s)"),
        ("R00700_5", "ESDV Commanded Closed Discrepancy Fault (>10s)"),
        ("R00700_6", "ESDV Position Discrepancy Latched Fault"),
        ("R00701_0", "Stop Foam Pushbutton Active (7503-FS-001 or Panel E8)"),
        ("R00701_1", "Stop Foam Pushbutton Latched"),
        ("R00702_0", "7503-LS-001 AFFF Foam Tank Low Level Live"),
        ("R00702_1", "7503-LS-001 AFFF Foam Tank Low Level Latched"),
        ("R00703_0", "7503-LS-002 Diesel Tank Low Level Live"),
        ("R00703_1", "7503-LS-002 Diesel Tank Low Level Latched"),
        ("R00704_1", "Deluge Pump A Start Line Open-Circuit Fault Latched"),
        ("R00705_1", "Deluge Pump B Start Line Open-Circuit Fault Latched"),
        ("R00706_0", "75-SB-01B Standby Deluge Pump B Inhibited"),
        ("R00707_0", "6401-ESDV-001 (E9) ESD Fuel Gas Pushbutton Live"),
        ("R00707_1", "6401-ESDV-001 (E9) ESD Fuel Gas Pushbutton Latched"),
        ("R00708_0", "FGCP Keyswitch S2 Inhibit Foam Release Active"),
        ("R00709_0", "FGCP Keyswitch S3 Inhibit All Outputs Active"),
        ("R01500_0", "1ooN Low Gas Alarm Voting Output (20% LEL / 1.00 LELm)"),
        ("R01500_1", "2ooN Low Gas Alarm Voting Output"),
        ("R01500_2", "1ooN High Gas Alarm Voting Output (30% LEL / 3.00 LELm)"),
        ("R01500_3", "2ooN High Gas / Open-Path High Voting Output"),
        ("R01501_0", "1oo3 Flame Detector Voting Output (7404-DF-001..003)"),
        ("R01501_1", "2oo3 Confirmed Flame Voting Output"),
        ("R01510_0", "Internal ESD_TRIP Healthy Signal (1=Healthy, 0=Trip)"),
        ("R01511_0", "Internal 6401-EY-001/002 Fuel Gas ESDV Healthy Signal"),
        ("R01511_1", "Internal P2100/2200 Oil Booster Healthy Signal"),
        ("R01511_2", "Internal P3600/3700 Water Booster Healthy Signal"),
        ("R01511_3", "Internal 7404-SA-001/002 Pump House Alarm Bell Signal"),
        ("R01512_0", "Internal Deluge Pump A Start/Stop Command"),
        ("R01512_4", "Internal Deluge Pump B Stop Pulse Command"),
        ("R01512_5", "Internal Deluge Pump B Start Pulse Command"),
        ("R01513_0", "Internal L15 ESDV Open LED Signal"),
        ("R01513_1", "Internal L14 ESDV Closed LED Signal"),
        ("R01513_2", "Internal L16 ESDV Low Air Pressure LED Signal"),
        ("R01513_3", "Internal Z1 PROD CONTROL ROOM Alarm Signal"),
        ("R01513_4", "Internal PLC Fault Healthy Signal"),
        ("R01513_12", "Internal Pump A Open-Circuit Test Pulse"),
        ("R01513_13", "Internal Pump B Open-Circuit Test Pulse"),
        ("Foam_Release_Demand", "Active Deluge / Foam Release Demand"),
        ("Pump_B_Demand", "Standby Diesel Fire Pump B Demand"),
        ("ESD_Trip_Condition", "Master Fire & Gas ESD Trip Condition Active"),
        ("Deluge_Released_Status", "Deluge Water/Foam Released Status (7503-PST-001 >= 50 Psi)"),
        ("Foam_System_Inhibited", "Foam System Inhibited Status (S2 or S3)"),
        ("Bell_Mode_Discontinuous", "Pump House Bell Discontinuous (Pulsing) Mode"),
        ("Bell_Mode_Continuous", "Pump House Bell Continuous Mode"),
        ("Any_Unaccepted_Alarm", "Any Unacknowledged Alarm Present"),
        ("Alarm_Silence_Latch", "Alarm Horn/Bell Silenced by Mute/Accept"),
        ("Any_Channel_Fault", "Any Transmitter or Line Continuity Fault Active"),
        # GNTF Upgrade New Bools
        ("Latch_ESTOP_P2300", "Latched E-Stop E1 (7404-SB-004) Power Oil Pump P-2300"),
        ("Latch_ESTOP_P2400", "Latched E-Stop E2 (7404-SB-005) Power Oil Pump P-2400"),
        ("Latch_ESTOP_P2500", "Latched E-Stop E3 (7404-SB-006) Power Oil Pump P-2500"),
        ("Latch_ESTOP_P2600", "Latched E-Stop E4 (7404-SB-007) Power Oil Pump P-2600"),
        ("Latch_ESTOP_P3800", "Latched E-Stop E5 (7404-SB-008) Water Inj Pump P-3800"),
        ("Latch_ESTOP_P3900", "Latched E-Stop E6 (7404-SB-009) Water Inj Pump P-3900"),
        ("GD_001_Fault", "GD-001 Gas Generator Room CH4 Detector 1 Fault"),
        ("GD_002_Fault", "GD-002 Gas Generator Room CH4 Detector 2 Fault"),
        ("GD_003_Fault", "GD-003 Gas Generator Room CH4 Detector 3 Fault"),
        ("GD_001_Lo", "GD-001 Low Gas Alarm (>= 20% LEL)"),
        ("GD_002_Lo", "GD-002 Low Gas Alarm (>= 20% LEL)"),
        ("GD_003_Lo", "GD-003 Low Gas Alarm (>= 20% LEL)"),
        ("GD_001_Hi", "GD-001 High Gas Alarm (>= 30% LEL)"),
        ("GD_002_Hi", "GD-002 High Gas Alarm (>= 30% LEL)"),
        ("GD_003_Hi", "GD-003 High Gas Alarm (>= 30% LEL)"),
        ("GD_Any_Lo_Latch", "Latched Low Gas Alarm in Gas Generator Room (GD-001..003)"),
        ("GD_Any_Hi_Latch", "Latched High Gas Trip in Gas Generator Room (Trips SD-GE)"),
        ("PIT_001_Fault", "PIT-001 Oil Expedition PT Fault"),
        ("PIT_001_PAL", "PIT-001 Oil Expedition Low Pressure Alarm (<= 10 Psi)"),
        ("PIT_001_PAH", "PIT-001 Oil Expedition High Pressure Alarm (>= 100 Psi)"),
        ("PIT_002_Fault", "PIT-002 Water Injection PT Fault"),
        ("PIT_002_PAL", "PIT-002 Water Injection Low Pressure Alarm (<= 200 Psi)"),
        ("PIT_002_PAH", "PIT_002 Water Injection High Pressure Alarm (>= 800 Psi)"),
        ("PIT_002_PAHH", "PIT-002 Water Injection High-High Pressure Live (>= 900 Psi)"),
        ("PIT_002_PAHH_Latch", "PIT-002 Water Injection High-High Pressure Trip Latched"),
        ("PIT_003_Fault", "PIT-003 Oil Injection PT Fault"),
        ("PIT_003_PAL", "PIT-003 Oil Injection Low Pressure Alarm (<= 1700 Psi)"),
        ("PIT_003_PAH", "PIT-003 Oil Injection High Pressure Alarm (>= 2700 Psi)"),
        ("PIT_003_PAHH", "PIT-003 Oil Injection High-High Pressure Live (>= 2800 Psi)"),
        ("PIT_003_PAHH_Latch", "PIT-003 Oil Injection High-High Pressure Trip Latched"),
        ("H2S_Any_Lo", "Any H2S Detector H2S-001..012 >= 10 PPM Live"),
        ("H2S_Any_Hi", "Any H2S Detector H2S-001..012 >= 20 PPM Live"),
        ("H2S_Lo_Latch", "H2S Low Alarm (10 PPM) Latched -> Discontinuous H2SA-001/002"),
        ("H2S_Hi_Latch", "H2S High Alarm (20 PPM) Latched -> Continuous H2SA-001/002"),
        ("DF_7404_003_Fault", "7404-DF-003 Flame Detector 3 Fault"),
        ("DF_7404_003_Alarm", "7404-DF-003 Flame Detector 3 Fire Live (>= 30%)"),
        ("DF_7404_003_Latch", "7404-DF-003 Flame Detector 3 Fire Latched"),
        ("SD_001_002_Fault", "SD-001/002 Smoke Detector Fault"),
        ("SD_001_002_Alarm", "SD-001/002 Smoke Detector Alarm Live (>= 30%)"),
        ("SD_001_002_Latch", "SD-001/002 Smoke Detector Latched (Trips SD-GE + SDA-001)"),
        ("LIT_100_LAL", "Tank T-100 Low Level Alarm (<= 0.7 m)"),
        ("LIT_100_LAH", "Tank T-100 High Level Alarm (>= 9.0 m)"),
        ("LIT_200_LAL", "Tank T-200 Low Level Alarm (<= 0.7 m)"),
        ("LIT_200_LAH", "Tank T-200 High Level Alarm (>= 9.0 m)"),
        ("LIT_300_LAL", "Tank T-300 Low Level Alarm (<= 0.7 m)"),
        ("LIT_300_LAH", "Tank T-300 High Level Alarm (>= 9.0 m)"),
        ("LIT_400_LAL", "Tank T-400 Low Level Alarm (<= 0.7 m)"),
        ("LIT_400_LAH", "Tank T-400 High Level Alarm (>= 11.0 m)"),
        ("FT_6401_001_FAL", "6401-FT-001 Oil Expedition Low Flow Alarm (<= 30 bbl/h)"),
        ("FT_6401_001_FAH", "6401-FT-001 Oil Expedition High Flow Alarm (>= 300 bbl/h)"),
    ]
    for bname, bdesc in internal_bools:
        tags.append((bname, "BOOL", bdesc, ""))

    # Voting counters (DINT)
    tags.append(("Vote_Gas_Lo_Count", "DINT", "Active CH4 Gas Detectors >= Low Alarm (20% LEL)", ""))
    tags.append(("Vote_Gas_Hi_Count", "DINT", "Active CH4 Gas Detectors >= High Alarm (30% LEL)", ""))
    tags.append(("Vote_Flame_Count", "DINT", "Active Flame Detectors >= Fire Threshold (30%)", ""))

    # GNTF Upgrade Engineering Units & Setpoints (REAL)
    new_reals = [
        ("GD_001_EU", "GD-001 Gas Generator Room CH4 Detector 1 (%LEL)"),
        ("GD_002_EU", "GD-002 Gas Generator Room CH4 Detector 2 (%LEL)"),
        ("GD_003_EU", "GD-003 Gas Generator Room CH4 Detector 3 (%LEL)"),
        ("PIT_001_EU", "PIT-001 Oil Expedition Manifold Pressure (Psi)"),
        ("PIT_002_EU", "PIT-002 Water Injection Manifold Pressure (Psi)"),
        ("PIT_003_EU", "PIT-003 Oil Injection Manifold Pressure (Psi)"),
        ("H2S_001_EU", "H2S-001 Gas Detector 1 (PPM)"),
        ("H2S_002_EU", "H2S-002 Gas Detector 2 (PPM)"),
        ("H2S_003_EU", "H2S-003 Gas Detector 3 (PPM)"),
        ("H2S_004_EU", "H2S-004 Gas Detector 4 (PPM)"),
        ("H2S_005_EU", "H2S-005 Gas Detector 5 (PPM)"),
        ("H2S_006_EU", "H2S-006 Gas Detector 6 (PPM)"),
        ("H2S_007_EU", "H2S-007 Gas Detector 7 (PPM)"),
        ("H2S_008_EU", "H2S-008 Gas Detector 8 (PPM)"),
        ("H2S_009_EU", "H2S-009 Gas Detector 9 (PPM)"),
        ("H2S_010_EU", "H2S-010 Gas Detector 10 (PPM)"),
        ("H2S_011_EU", "H2S-011 Gas Detector 11 (PPM)"),
        ("H2S_012_EU", "H2S-012 Gas Detector 12 (PPM)"),
        ("DF_7404_003_EU", "7404-DF-003 Flame Detector 3 (%)"),
        ("SD_001_002_EU", "SD-001/002 Smoke Detectors (%)"),
        ("LIT_100_EU", "LIT-100 Tank T-100 Level (m)"),
        ("LIT_200_EU", "LIT-200 Tank T-200 Level (m)"),
        ("LIT_300_EU", "LIT-300 Tank T-300 Level (m)"),
        ("LIT_400_EU", "LIT-400 Tank T-400 Level (m)"),
        ("FT_6401_001_EU", "6401-FT-001 Oil Expedition Flowrate (bbl/h)"),
        ("SP_GD_Low_LEL", "Setpoint: GD-001..003 Low Gas Alarm (20.0 %LEL)"),
        ("SP_GD_High_LEL", "Setpoint: GD-001..003 High Gas Alarm (30.0 %LEL)"),
        ("SP_H2S_Low_PPM", "Setpoint: H2S-001..012 Low Alarm (10.0 PPM)"),
        ("SP_H2S_High_PPM", "Setpoint: H2S-001..012 High Alarm (20.0 PPM)"),
        ("SP_DF003_High", "Setpoint: 7404-DF-003 Flame Alarm (30.0 %)"),
        ("SP_SD_High", "Setpoint: SD-001/002 Smoke Alarm (30.0 %)"),
        ("SP_PIT001_PAL", "Setpoint: PIT-001 Low Pressure (10.0 Psi)"),
        ("SP_PIT001_PAH", "Setpoint: PIT-001 High Pressure (100.0 Psi)"),
        ("SP_PIT002_PAL", "Setpoint: PIT-002 Low Pressure (200.0 Psi)"),
        ("SP_PIT002_PAH", "Setpoint: PIT-002 High Pressure (800.0 Psi)"),
        ("SP_PIT002_PAHH", "Setpoint: PIT-002 High-High Trip (900.0 Psi)"),
        ("SP_PIT003_PAL", "Setpoint: PIT-003 Low Pressure (1700.0 Psi)"),
        ("SP_PIT003_PAH", "Setpoint: PIT-003 High Pressure (2700.0 Psi)"),
        ("SP_PIT003_PAHH", "Setpoint: PIT-003 High-High Trip (2800.0 Psi)"),
        ("SP_LIT100_LAL", "Setpoint: LIT-100 Low Level (0.7 m)"),
        ("SP_LIT100_LAH", "Setpoint: LIT-100 High Level (9.0 m)"),
        ("SP_LIT200_LAL", "Setpoint: LIT-200 Low Level (0.7 m)"),
        ("SP_LIT200_LAH", "Setpoint: LIT-200 High Level (9.0 m)"),
        ("SP_LIT300_LAL", "Setpoint: LIT-300 Low Level (0.7 m)"),
        ("SP_LIT300_LAH", "Setpoint: LIT-300 High Level (9.0 m)"),
        ("SP_LIT400_LAL", "Setpoint: LIT-400 Low Level (0.7 m)"),
        ("SP_LIT400_LAH", "Setpoint: LIT-400 High Level (11.0 m)"),
        ("SP_FT001_FAL", "Setpoint: 6401-FT-001 Low Flow (30.0 bbl/h)"),
        ("SP_FT001_FAH", "Setpoint: 6401-FT-001 High Flow (300.0 bbl/h)"),
    ]
    for rname, rdesc in new_reals:
        tags.append((rname, "REAL", rdesc, ""))

    # FBD_TIMER and FBD_COUNTER structures for Studio 5000 ST TONR / CTUD instructions
    timers = [
        ("TMR_Flash_Slow", "0.4s Slow Flasher Timer"),
        ("TMR_Flash_Fast", "0.4s Fast Flasher Timer"),
        ("TMR_ESDV_Transit", "10.0s ESDV Transit Discrepancy Timer"),
        ("TMR_ESDV_CmdOpen", "10.0s ESDV Commanded Open Discrepancy Timer"),
        ("TMR_ESDV_CmdClose", "10.0s ESDV Commanded Closed Discrepancy Timer"),
        ("TMR_Pulse_Period", "60.0s Deluge Pump Line Continuity Check Period Timer"),
        ("TMR_Pulse_Width", "1.0s Deluge Pump Line Continuity Test Pulse Timer"),
        ("TMR_PumpA_WireFlt", "0.5s Deluge Pump A Open-Circuit Fault Timer"),
        ("TMR_PumpB_WireFlt", "0.5s Deluge Pump B Open-Circuit Fault Timer"),
        ("TMR_PumpA_FailToRun", "10.0s Deluge Pump A Pressure Proving Timer"),
        ("TMR_PumpB_StartOn", "2.0s Standby Pump B Crank ON Timer"),
        ("TMR_PumpB_StartOff", "2.0s Standby Pump B Crank Rest OFF Timer"),
        ("TMR_PumpB_StopPulse", "2.0s Standby Pump B Stop Pulse Timer"),
    ]
    for tname, tdesc in timers:
        tags.append((tname, "FBD_TIMER", tdesc, ""))

    tags.append(("CTU_PumpB_Attempts", "FBD_COUNTER", "Standby Pump B Start Attempt Counter (3 Attempts)", ""))
    return tags


# ---------------------------------------------------------------------------
# 4. STUDIO 5000 .ST, .CSV, AND .L5X WRITERS
# ---------------------------------------------------------------------------
def write_st_files(tags):
    st_dir = os.path.join(OUT_DIR_WS, "ab_st_routines")
    os.makedirs(st_dir, exist_ok=True)

    complete_lines = [
        "// ============================================================================",
        "// ALLEN-BRADLEY CONTROLLOGIX 5580 (1756-L82E) STRUCTURED TEXT PROGRAM",
        "// Project : GNTF QUINGUILA CONTROL SYSTEM UPGRADE (P20890_Angola / FGCP-7404-001)",
        "// Client  : SONANGOL P&P / EPPM ANGOLA / ASTRE",
        "// Chassis : 1756-A13 (13-Slot), Power Supply: 1756-PB72 (24V DC)",
        "// CPU     : Slot 0 = 1756-L82E (IP: 192.168.20.10/24)",
        "// Modules : Slot 1 = 1756-N2, Slots 2..5 = 4x 1756-IF16, Slot 6 = 1756-IF8H,",
        "//           Slot 7 = 1756-IB32, Slot 8 = 1756-OB32, Slot 9 = MVI56E-MCM",
        "// ============================================================================",
        "",
    ]

    for rname, rdesc, rcode in ROUTINES:
        routine_path = os.path.join(st_dir, f"{rname}.st")
        with open(routine_path, "w", encoding="utf-8") as f:
            f.write(rcode.strip() + "\n")
        complete_lines.append(f"// ****************************************************************************")
        complete_lines.append(f"// ROUTINE: {rname} — {rdesc}")
        complete_lines.append(f"// ****************************************************************************")
        complete_lines.append(rcode.strip())
        complete_lines.append("")

    complete_text = "\n".join(complete_lines)
    for out_dir in (OUT_DIR_WS, OUT_DIR_DESKTOP):
        with open(os.path.join(out_dir, "P20890_Angola_AB_Complete.st"), "w", encoding="utf-8") as f:
            f.write(complete_text)


def write_csv_tags(tags):
    for out_dir in (OUT_DIR_WS, OUT_DIR_DESKTOP):
        csv_path = os.path.join(out_dir, "P20890_Angola_AB_Tags.csv")
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["remark", "CSV-Import-Export"])
            writer.writerow(["remark", "Project: GNTF Quinguila Control System Upgrade (P20890_Angola -> 1756-L82E)"])
            writer.writerow(["0.3"])
            writer.writerow(["TYPE", "SCOPE", "NAME", "DESCRIPTION", "DATATYPE", "SPECIFIER", "ATTRIBUTES"])
            for tname, dtype, desc, alias_for in tags:
                if alias_for and not alias_for.startswith("MODBUS"):
                    writer.writerow(["ALIAS", "", tname, desc, "", alias_for, "(Constant := false, ExternalAccess := Read/Write)"])
                else:
                    writer.writerow(["TAG", "", tname, desc, dtype, "", "(Constant := false, ExternalAccess := Read/Write)"])


def write_l5x_file(tags):
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<RSLogix5000Content SchemaRevision="1.0" SoftwareRevision="32.00" TargetName="GNTF_FGCP_7404_001" TargetType="Controller" ContainsContext="false" Owner="EPPM / ASTRE" ExportDate="Fri Nov 06 09:00:00 2026">',
        '  <Controller Use="Target" Name="GNTF_FGCP_7404_001" ProcessorType="1756-L82E" MajorRev="32" MinorRev="11" ChassisType="1756-A13" PowerSupply="1756-PB72" ProjectCreationDate="Fri Nov 06 09:00:00 2026" LastModifiedDate="Fri Nov 06 09:00:00 2026">',
        '    <Description>',
        '      <![CDATA[GNTF Quinguila Tank Farm Control System Upgrade - FGCP-7404-001 (Converted from GE VersaMax P20890_Angola + New Phase 1 I/O per 01-MAN-03-06 & 01-MAN-03-07)]]>',
        '    </Description>',
        '    <Modules>',
        '      <Module Name="Local" CatalogNumber="1756-L82E" Vendor="1" ProductType="14" ProductCode="167" Major="32" Minor="11" ParentModule="Local" ParentModPortId="1" Inhibited="false" MajorFault="true">',
        '        <Ports>',
        '          <Port Id="1" Address="0" Type="ICP" Upstream="false"/>',
        '          <Port Id="2" Address="192.168.20.10" Type="Ethernet" Upstream="false"/>',
        '        </Ports>',
        '      </Module>',
        '      <Module Name="AI_Slot2_TB02" CatalogNumber="1756-IF16" Vendor="1" ProductType="10" ProductCode="10" Major="1" Minor="1" ParentModule="Local" ParentModPortId="1" Inhibited="false" MajorFault="false">',
        '        <Ports><Port Id="1" Address="2" Type="ICP" Upstream="true"/></Ports>',
        '      </Module>',
        '      <Module Name="AI_Slot3_TB03" CatalogNumber="1756-IF16" Vendor="1" ProductType="10" ProductCode="10" Major="1" Minor="1" ParentModule="Local" ParentModPortId="1" Inhibited="false" MajorFault="false">',
        '        <Ports><Port Id="1" Address="3" Type="ICP" Upstream="true"/></Ports>',
        '      </Module>',
        '      <Module Name="AI_Slot4_TB04" CatalogNumber="1756-IF16" Vendor="1" ProductType="10" ProductCode="10" Major="1" Minor="1" ParentModule="Local" ParentModPortId="1" Inhibited="false" MajorFault="false">',
        '        <Ports><Port Id="1" Address="4" Type="ICP" Upstream="true"/></Ports>',
        '      </Module>',
        '      <Module Name="AI_Slot5_TB05_Spare" CatalogNumber="1756-IF16" Vendor="1" ProductType="10" ProductCode="10" Major="1" Minor="1" ParentModule="Local" ParentModPortId="1" Inhibited="false" MajorFault="false">',
        '        <Ports><Port Id="1" Address="5" Type="ICP" Upstream="true"/></Ports>',
        '      </Module>',
        '      <Module Name="HART_Slot6_TB06" CatalogNumber="1756-IF8H" Vendor="1" ProductType="10" ProductCode="68" Major="1" Minor="1" ParentModule="Local" ParentModPortId="1" Inhibited="false" MajorFault="false">',
        '        <Ports><Port Id="1" Address="6" Type="ICP" Upstream="true"/></Ports>',
        '      </Module>',
        '      <Module Name="DI_Slot7_TB07" CatalogNumber="1756-IB32" Vendor="1" ProductType="7" ProductCode="14" Major="3" Minor="1" ParentModule="Local" ParentModPortId="1" Inhibited="false" MajorFault="false">',
        '        <Ports><Port Id="1" Address="7" Type="ICP" Upstream="true"/></Ports>',
        '      </Module>',
        '      <Module Name="DO_Slot8_TB08" CatalogNumber="1756-OB32" Vendor="1" ProductType="7" ProductCode="22" Major="3" Minor="1" ParentModule="Local" ParentModPortId="1" Inhibited="false" MajorFault="false">',
        '        <Ports><Port Id="1" Address="8" Type="ICP" Upstream="true"/></Ports>',
        '      </Module>',
        '      <Module Name="MCM_Slot9_Modbus" CatalogNumber="MVI56E-MCM" Vendor="309" ProductType="12" ProductCode="1" Major="1" Minor="1" ParentModule="Local" ParentModPortId="1" Inhibited="false" MajorFault="false">',
        '        <Ports><Port Id="1" Address="9" Type="ICP" Upstream="true"/></Ports>',
        '      </Module>',
        '    </Modules>',
        '    <Tags>',
    ]

    for tname, dtype, desc, alias_for in tags:
        esc_desc = saxutils.escape(desc)
        if alias_for and not alias_for.startswith("MODBUS"):
            xml_lines.append(f'      <Tag Name="{tname}" TagType="Alias" AliasFor="{alias_for}" ExternalAccess="Read/Write">')
            xml_lines.append(f'        <Description><![CDATA[{esc_desc}]]></Description>')
            xml_lines.append('      </Tag>')
        else:
            xml_lines.append(f'      <Tag Name="{tname}" TagType="Base" DataType="{dtype}" Constant="false" ExternalAccess="Read/Write">')
            xml_lines.append(f'        <Description><![CDATA[{esc_desc}]]></Description>')
            xml_lines.append('      </Tag>')

    xml_lines.extend([
        '    </Tags>',
        '    <Programs>',
        '      <Program Name="MainProgram" TestEdits="false" MainRoutineName="MainRoutine" Disabled="false" UseAsFolder="false">',
        '        <Description><![CDATA[FGCP-7404-001 Fire, Gas, ESD & Process Control Program (Structured Text)]]></Description>',
        '        <Tags/>',
        '        <Routines>',
    ])

    for rname, rdesc, rcode in ROUTINES:
        xml_lines.append(f'          <Routine Name="{rname}" Type="ST">')
        xml_lines.append(f'            <Description><![CDATA[{rdesc}]]></Description>')
        xml_lines.append('            <STContent>')
        for line in rcode.strip().splitlines():
            xml_lines.append(f'              <Line><![CDATA[{line}]]></Line>')
        xml_lines.append('            </STContent>')
        xml_lines.append('          </Routine>')

    xml_lines.extend([
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

    l5x_content = "\n".join(xml_lines) + "\n"
    for out_dir in (OUT_DIR_WS, OUT_DIR_DESKTOP):
        with open(os.path.join(out_dir, "P20890_Angola_AB_ST.L5X"), "w", encoding="utf-8") as f:
            f.write(l5x_content)


# ---------------------------------------------------------------------------
# 5. PRINTABLE VECTOR PDF REPORT GENERATOR (ReportLab)
# ---------------------------------------------------------------------------
def write_pdf_report(tags):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.pdfgen import canvas

    W, H = landscape(A4)  # 841.89 x 595.27 pt
    pdf_path_ws = os.path.join(OUT_DIR_WS, "P20890_Angola_AB_ST.pdf")
    c = canvas.Canvas(pdf_path_ws, pagesize=(W, H))
    c.setTitle("GNTF Quinguila Control System Upgrade — Allen-Bradley 1756-L82E Structured Text (P20890_Angola)")
    c.setAuthor("EPPM / ASTRE — Studio 5000 ControlLogix 5580 Conversion")

    def add_header_footer(page_title, pno):
        c.saveState()
        # Header bar
        c.setFillColor(colors.HexColor("#19386b"))
        c.rect(25, H - 46, W - 50, 28, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(34, H - 31, "GNTF QUINGUILA CONTROL SYSTEM UPGRADE — ALLEN-BRADLEY 1756-L82E STRUCTURED TEXT (ST)")
        c.setFillColor(colors.HexColor("#d1e6ff"))
        c.setFont("Helvetica", 7.5)
        c.drawString(34, H - 41, page_title[:115])
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 8)
        c.drawRightString(W - 34, H - 31, f"Doc Ref: 01-MAN-03-06 / 03-07 | Page {pno}")

        # Footer line
        c.setStrokeColor(colors.HexColor("#bfdbfe"))
        c.setLineWidth(0.6)
        c.line(25, 22, W - 25, 22)
        c.setFillColor(colors.HexColor("#475569"))
        c.setFont("Helvetica", 7.2)
        c.drawString(28, 11, "Legacy PLC: GE Fanuc VersaMax (P20890_Angola / FGCP-7404-001)  -->  New PLC: Allen-Bradley ControlLogix 5580 1756-L82E (Studio 5000 v32)")
        c.restoreState()

    # --- PAGE 1: Cover, Architecture & Rack 1 Slot Overview ---
    pno = 1
    add_header_footer("Section 1: ControlLogix 1756-A13 Hardware Architecture & Conversion Summary", pno)
    c.bookmarkPage("sec_arch")
    c.addOutlineEntry("1. ControlLogix 1756-A13 Hardware & ST Routine Architecture", "sec_arch", level=0)

    c.setFillColor(colors.HexColor("#19386b"))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(30, H - 64, "1. ControlLogix 5580 (1756-L82E) Chassis & Module Configuration (Ref: 01-MAN-03-11-PDF-C3A & 01-MAN-03-06-PDF-C2C)")

    slots_summary = [
        ("Slot 0", "1756-L82E",   "ControlLogix 5580 Controller (32MB, Ethernet 192.168.20.10/24)", "Replaces GE VersaMax CPU IC200CPU001 (FGCP-7404-001)"),
        ("Slot 1", "1756-N2",     "ControlLogix Empty Slot Filler Card", "Reserved / Spare Slot"),
        ("Slot 2", "1756-IF16",   "16-Ch Analog Input Module (TB-02: Local:2:I.Ch0Data..Ch15Data)", "7404-DG-001..012 (CH4 Point), 7404-DG-011R (Open Path), GD-001..003 (Gen Room)"),
        ("Slot 3", "1756-IF16",   "16-Ch Analog Input Module (TB-03: Local:3:I.Ch0Data..Ch15Data)", "PIT-001..003, 7503-PST-001, 7002-PST-001, 6401-PST-001, 7503-FR-001/002/003"),
        ("Slot 4", "1756-IF16",   "16-Ch Analog Input Module (TB-04: Local:4:I.Ch0Data..Ch15Data)", "H2S-001..012 (0-100 PPM), 7404-DF-001..003 (Flame), SD-001/002 (Smoke)"),
        ("Slot 5", "1756-IF16",   "16-Ch Analog Input Module (TB-05: Local:5:I.Ch0Data..Ch15Data)", "16x Spare Analog Input Channels (20% Spare Capacity)"),
        ("Slot 6", "1756-IF8H",   "8-Ch HART Analog Input Module (TB-06: Local:6:I.Ch0Data..Ch7Data)", "Tank Level Transmitters LIT-100, LIT-200, LIT-300 (0-10m), LIT-400 (0-12m)"),
        ("Slot 7", "1756-IB32",   "32-Pt 24VDC Digital Input Module (TB-07: Local:7:I.Data.0..31)", "6401-ZSH/ZSL-001, 7503-FS/LS, E8/E9/E11/E12, S2/S3, E1..E6 (7404-SB-004..009)"),
        ("Slot 8", "1756-OB32",   "32-Pt 24VDC Digital Output Module (TB-08: Local:8:O.Data.0..31)", "ESD_TRIP, 6401-EY-001/002, 7404-SA-001/002, PUMP-A/B, L14..L17, CR1..CR6, SD-GE, Z1, PA/H2SA/SDA"),
        ("Slot 9", "MVI56E-MCM",  "ProSoft Modbus Master/Slave Module (RS-485 P1 & P2)", "Murphy Panels P-2300..P-2600, P-3800..P-3900, Flowmeter 6401-FT-001, Treaters V-710/V-810"),
        ("Slot 10-12", "1756-N2", "3x ControlLogix Empty Slot Filler Cards", "Future Expansion Slots in 1756-A13 (13-Slot Chassis) with 1756-PB72 PSU"),
    ]

    y_top = H - 74
    c.setFillColor(colors.HexColor("#2e528c"))
    c.rect(30, y_top - 15, W - 60, 15, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 7.8)
    c.drawString(35, y_top - 11, "Slot")
    c.drawString(95, y_top - 11, "Catalog No.")
    c.drawString(185, y_top - 11, "Module Description & Studio 5000 I/O Address")
    c.drawString(475, y_top - 11, "Assigned Field Instruments / Function")
    y_top -= 15

    for idx, (sl, cat, mdesc, fdesc) in enumerate(slots_summary):
        bg = colors.HexColor("#f2f7ff") if idx % 2 == 0 else colors.white
        c.setFillColor(bg)
        c.setStrokeColor(colors.HexColor("#d1d9e6"))
        c.rect(30, y_top - 13.5, W - 60, 13.5, stroke=1, fill=1)
        c.setFillColor(colors.HexColor("#193366"))
        c.setFont("Helvetica-Bold", 7.2)
        c.drawString(35, y_top - 10, sl)
        c.setFillColor(colors.HexColor("#0d5926"))
        c.setFont("Courier-Bold", 7.2)
        c.drawString(95, y_top - 10, cat)
        c.setFillColor(colors.HexColor("#1e293b"))
        c.setFont("Helvetica", 7.2)
        c.drawString(185, y_top - 10, mdesc)
        c.drawString(475, y_top - 10, fdesc)
        y_top -= 13.5

    y_top -= 14
    c.setFillColor(colors.HexColor("#19386b"))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(30, y_top, "2. Structured Text (ST) Program Routine Architecture (MainTask -> MainProgram)")
    y_top -= 6

    c.setFillColor(colors.HexColor("#2e528c"))
    c.rect(30, y_top - 14, W - 60, 14, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 7.8)
    c.drawString(35, y_top - 10, "Routine Name")
    c.drawString(145, y_top - 10, "Type")
    c.drawString(200, y_top - 10, "Functional Description & Project Reference")
    y_top -= 14

    for idx, (rname, rdesc, _) in enumerate(ROUTINES):
        bg = colors.HexColor("#f2f7ff") if idx % 2 == 0 else colors.white
        c.setFillColor(bg)
        c.setStrokeColor(colors.HexColor("#d1d9e6"))
        c.rect(30, y_top - 12.2, W - 60, 12.2, stroke=1, fill=1)
        c.setFillColor(colors.HexColor("#143873"))
        c.setFont("Courier-Bold", 7.2)
        c.drawString(35, y_top - 9, rname)
        c.setFillColor(colors.HexColor("#197333"))
        c.setFont("Helvetica-Bold", 7.2)
        c.drawString(145, y_top - 9, "ST")
        c.setFillColor(colors.HexColor("#1e293b"))
        c.setFont("Helvetica", 7.0)
        c.drawString(200, y_top - 9, rdesc)
        y_top -= 12.2

    c.showPage()

    # --- PAGES 2..3: Complete Hardware I/O & Setpoints Cross-Reference Table ---
    rows_per_page = 32
    for start_idx in range(0, len(IO_MAP), rows_per_page):
        pno += 1
        add_header_footer("Section 2: Complete Hardware I/O, Terminal Block & Setpoint Cross-Reference (GE VersaMax <-> AB 1756)", pno)
        if start_idx == 0:
            c.bookmarkPage("sec_io")
            c.addOutlineEntry("2. Hardware I/O & Setpoints Cross-Reference Table", "sec_io", level=0)

        y_top = H - 54
        c.setFillColor(colors.HexColor("#2e528c"))
        c.rect(25, y_top - 15, W - 50, 15, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 7.0)
        cols = [
            (28, "Type"), (64, "Slot/Ch"), (102, "TB / Term"), (168, "Instrument Tag"),
            (250, "Studio 5000 Tag"), (350, "AB Hardware Address"), (455, "Legacy GE"),
            (505, "Range"), (565, "Low / High / HH"), (645, "Service Description"),
        ]
        for cx, ctitle in cols:
            c.drawString(cx, y_top - 10.5, ctitle)
        y_top -= 15

        chunk = IO_MAP[start_idx:start_idx + rows_per_page]
        for idx, (io_type, rack, slot, ch, ts, tb, inst_tag, ab_tag, ab_hw, ge_addr, rng, sp_lo, sp_hi, sp_hh, desc) in enumerate(chunk):
            bg = colors.HexColor("#f2f7ff") if idx % 2 == 0 else colors.white
            c.setFillColor(bg)
            c.setStrokeColor(colors.HexColor("#d6deeb"))
            c.rect(25, y_top - 14, W - 50, 14, stroke=1, fill=1)
            sp_str = f"{sp_lo} / {sp_hi}" + (f" / {sp_hh}" if sp_hh not in ("-", "N/A") else "")

            c.setFillColor(colors.HexColor("#194073"))
            c.setFont("Helvetica-Bold", 6.7)
            c.drawString(28, y_top - 10, io_type)

            c.setFillColor(colors.HexColor("#1e293b"))
            c.setFont("Courier", 6.7)
            c.drawString(64, y_top - 10, f"S{slot}:Ch{ch}")

            c.setFont("Helvetica", 6.4)
            c.drawString(102, y_top - 10, tb[:14])

            c.setFillColor(colors.HexColor("#0d2659"))
            c.setFont("Helvetica-Bold", 6.7)
            c.drawString(168, y_top - 10, inst_tag[:16])

            c.setFillColor(colors.HexColor("#0d6126"))
            c.setFont("Courier-Bold", 6.6)
            c.drawString(250, y_top - 10, ab_tag[:19])

            c.setFillColor(colors.HexColor("#73260d"))
            c.setFont("Courier", 6.6)
            c.drawString(350, y_top - 10, ab_hw[:21])

            c.setFillColor(colors.HexColor("#4d1966"))
            c.setFont("Courier-Bold", 6.7)
            c.drawString(455, y_top - 10, ge_addr)

            c.setFillColor(colors.HexColor("#1e293b"))
            c.setFont("Helvetica", 6.4)
            c.drawString(505, y_top - 10, rng[:12])

            c.setFillColor(colors.HexColor("#8c1919"))
            c.setFont("Helvetica-Bold", 6.2)
            c.drawString(565, y_top - 10, sp_str[:16])

            c.setFillColor(colors.HexColor("#1e293b"))
            c.setFont("Helvetica", 6.3)
            c.drawString(645, y_top - 10, desc[:36])
            y_top -= 14

        c.showPage()

    # --- STRUCTURED TEXT CODE PAGES ---
    for rname, rdesc, rcode in ROUTINES:
        lines = rcode.strip().splitlines()
        lines_per_page = 42
        for l_idx in range(0, len(lines), lines_per_page):
            pno += 1
            part_suffix = f" (Part {l_idx // lines_per_page + 1})" if len(lines) > lines_per_page else ""
            add_header_footer(f"Structured Text Routine: {rname}{part_suffix} — {rdesc}", pno)
            if l_idx == 0:
                bm = f"rt_{rname}"
                c.bookmarkPage(bm)
                c.addOutlineEntry(f"Routine: {rname} — {rdesc[:45]}", bm, level=0)

            # Code box
            c.setFillColor(colors.HexColor("#f9fbff"))
            c.setStrokeColor(colors.HexColor("#c7d1e0"))
            c.rect(25, 28, W - 50, H - 82, stroke=1, fill=1)

            y_top = H - 66
            for line_no, code_line in enumerate(lines[l_idx:l_idx + lines_per_page], start=l_idx + 1):
                c.setFillColor(colors.HexColor("#8c94a6"))
                c.setFont("Courier", 7.2)
                c.drawString(32, y_top, f"{line_no:03d}")

                if code_line.strip().startswith("//"):
                    c.setFillColor(colors.HexColor("#267339"))
                    c.setFont("Courier-Oblique", 7.4)
                elif any(k in code_line for k in ("IF ", "ELSIF ", "ELSE", "END_IF;", "JSR(", "TONR(", "CTUD(")):
                    c.setFillColor(colors.HexColor("#14338c"))
                    c.setFont("Courier-Bold", 7.4)
                else:
                    c.setFillColor(colors.HexColor("#1e1e26"))
                    c.setFont("Courier", 7.4)
                c.drawString(58, y_top, code_line[:132])
                y_top -= 11.4

            c.showPage()

    c.save()
    import shutil
    shutil.copyfile(pdf_path_ws, os.path.join(OUT_DIR_DESKTOP, "P20890_Angola_AB_ST.pdf"))


# ---------------------------------------------------------------------------
# 6. INTERACTIVE STANDALONE HTML VIEWER GENERATOR
# ---------------------------------------------------------------------------
def write_html_viewer(tags):
    io_rows_html = []
    for io_type, rack, slot, ch, ts, tb, inst_tag, ab_tag, ab_hw, ge_addr, rng, sp_lo, sp_hi, sp_hh, desc in IO_MAP:
        badge_cls = "badge-ai" if io_type in ("AI", "HART") else ("badge-di" if io_type == "DI" else ("badge-do" if io_type == "DO" else "badge-mb"))
        ge_badge = f'<span class="ge-new">NEW</span>' if ge_addr == "NEW" else f'<code>{html.escape(ge_addr)}</code>'
        io_rows_html.append(
            f"<tr>"
            f"<td><span class='badge {badge_cls}'>{html.escape(io_type)}</span></td>"
            f"<td><code>Slot {slot} / Ch {ch}</code></td>"
            f"<td>{html.escape(tb)}</td>"
            f"<td><strong>{html.escape(inst_tag)}</strong></td>"
            f"<td><code class='ab-tag'>{html.escape(ab_tag)}</code></td>"
            f"<td><code class='ab-hw'>{html.escape(ab_hw)}</code></td>"
            f"<td>{ge_badge}</td>"
            f"<td>{html.escape(rng)}</td>"
            f"<td>{html.escape(sp_lo)} / {html.escape(sp_hi)} / {html.escape(sp_hh)}</td>"
            f"<td>{html.escape(desc)}</td>"
            f"</tr>"
        )

    nav_buttons = []
    routine_cards = []
    for idx, (rname, rdesc, rcode) in enumerate(ROUTINES):
        nav_buttons.append(f'<button class="nav-btn" onclick="scrollToRoutine(\'rt-{rname}\')">{html.escape(rname)}</button>')
        escaped_code = html.escape(rcode.strip())
        routine_cards.append(f"""
        <section class="routine-card" id="rt-{rname}">
          <div class="routine-header">
            <div>
              <h2>{idx+1:02d}. {html.escape(rname)} <span class="st-badge">Studio 5000 ST</span></h2>
              <p>{html.escape(rdesc)}</p>
            </div>
            <button class="copy-btn" onclick="copyCode('code-{rname}', this)">Copy ST Code</button>
          </div>
          <pre id="code-{rname}"><code>{escaped_code}</code></pre>
        </section>
        """)

    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>GNTF Quinguila — Allen-Bradley ControlLogix 1756-L82E Structured Text (P20890_Angola)</title>
<style>
  :root {{
    --bg: #0f172a; --panel: #1e293b; --border: #334155; --text: #f1f5f9;
    --muted: #94a3b8; --accent: #38bdf8; --green: #4ade80; --amber: #fbbf24;
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; font-family: 'Segoe UI', system-ui, sans-serif; background: var(--bg); color: var(--text); display: flex; height: 100vh; overflow: hidden; }}
  aside {{ width: 270px; background: #0b1120; border-right: 1px solid var(--border); display: flex; flex-direction: column; padding: 16px; overflow-y: auto; }}
  aside h1 {{ font-size: 15px; margin: 0 0 6px; color: var(--accent); }}
  aside p {{ font-size: 12px; color: var(--muted); margin: 0 0 14px; line-height: 1.4; }}
  .nav-btn {{ width: 100%; text-align: left; background: transparent; color: var(--text); border: 1px solid transparent; padding: 7px 10px; border-radius: 6px; cursor: pointer; font-family: Consolas, monospace; font-size: 12.5px; margin-bottom: 3px; }}
  .nav-btn:hover {{ background: var(--panel); border-color: var(--border); color: var(--accent); }}
  main {{ flex: 1; overflow-y: auto; padding: 24px 32px; }}
  .hero {{ background: linear-gradient(135deg, #1e3a8a, #0f172a); border: 1px solid var(--border); border-radius: 10px; padding: 20px 24px; margin-bottom: 24px; }}
  .hero h1 {{ margin: 0 0 8px; font-size: 22px; }}
  .hero p {{ margin: 0; color: #cbd5e1; font-size: 13.5px; line-height: 1.5; }}
  .search-bar {{ width: 100%; padding: 10px 14px; border-radius: 8px; border: 1px solid var(--border); background: var(--panel); color: var(--text); font-size: 14px; margin-bottom: 20px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 12px; background: var(--panel); border-radius: 8px; overflow: hidden; margin-bottom: 28px; }}
  th, td {{ padding: 8px 10px; border-bottom: 1px solid var(--border); text-align: left; }}
  th {{ background: #0f172a; color: var(--accent); font-weight: 600; position: sticky; top: 0; }}
  tr:hover {{ background: rgba(56, 189, 248, 0.06); }}
  .badge {{ padding: 2px 7px; border-radius: 4px; font-size: 11px; font-weight: 700; }}
  .badge-ai {{ background: rgba(56, 189, 248, 0.2); color: #38bdf8; }}
  .badge-di {{ background: rgba(74, 222, 128, 0.2); color: #4ade80; }}
  .badge-do {{ background: rgba(251, 191, 36, 0.2); color: #fbbf24; }}
  .badge-mb {{ background: rgba(192, 132, 252, 0.2); color: #c084fc; }}
  .ge-new {{ background: #065f46; color: #6ee7b7; padding: 2px 6px; border-radius: 4px; font-size: 10.5px; font-weight: 700; }}
  .ab-tag {{ color: var(--green); font-weight: 600; }}
  .ab-hw {{ color: var(--amber); }}
  .routine-card {{ background: var(--panel); border: 1px solid var(--border); border-radius: 10px; margin-bottom: 22px; overflow: hidden; }}
  .routine-header {{ display: flex; justify-content: space-between; align-items: center; padding: 14px 18px; background: #131c31; border-bottom: 1px solid var(--border); }}
  .routine-header h2 {{ margin: 0 0 4px; font-size: 16px; color: var(--accent); font-family: Consolas, monospace; }}
  .routine-header p {{ margin: 0; font-size: 12.5px; color: var(--muted); }}
  .st-badge {{ background: rgba(56, 189, 248, 0.15); color: var(--accent); font-size: 11px; padding: 2px 8px; border-radius: 4px; margin-left: 8px; }}
  .copy-btn {{ background: #0284c7; color: white; border: none; padding: 7px 14px; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 12px; }}
  .copy-btn:hover {{ background: #0369a1; }}
  pre {{ margin: 0; padding: 16px 20px; overflow-x: auto; font-family: Consolas, 'Courier New', monospace; font-size: 12.8px; line-height: 1.5; color: #e2e8f0; background: #0b1324; }}
</style>
</head>
<body>
  <aside>
    <h1>1756-L82E ST Program</h1>
    <p>GNTF Quinguila Control System Upgrade<br>P20890_Angola &rarr; Studio 5000</p>
    <button class="nav-btn" onclick="scrollToRoutine('io-table-sec')">&bull; Hardware &amp; I/O Table</button>
    {"".join(nav_buttons)}
  </aside>
  <main>
    <div class="hero">
      <h1>GNTF Quinguila Control System Upgrade — Allen-Bradley 1756-L82E Structured Text</h1>
      <p>Complete conversion of GE Fanuc VersaMax <code>P20890_Angola</code> (<code>FGCP-7404-001</code>) to Rockwell Automation Studio 5000 Structured Text (ST) for ControlLogix 5580 <code>1756-L82E</code> (13-Slot <code>1756-A13</code>, <code>1756-PB72</code>), incorporating all approved EPPM project documents (<code>01-MAN-03-06-PDF-C2C</code>, <code>01-MAN-03-07-PDF-C2C</code>, <code>01-MAN-02-13-PDF-C1A</code>, <code>01-MAN-03-11-PDF-C3A</code>, <code>01-MAN-03-13-PDF-C1</code>).</p>
    </div>

    <input type="text" id="filterInput" class="search-bar" placeholder="Filter I/O table or routines by Tag, Instrument (e.g. 7404-DG-001, H2S-001, PIT-002, Local:8:O)..." onkeyup="filterContent()">

    <section id="io-table-sec">
      <h2 style="color: var(--accent); margin-top: 0;">Hardware I/O, Terminal Block &amp; Setpoint Cross-Reference (Slots 2–9)</h2>
      <table id="ioTable">
        <thead>
          <tr>
            <th>Type</th><th>Slot / Ch</th><th>Terminal Block</th><th>Instrument Tag</th>
            <th>Studio 5000 Tag</th><th>AB Hardware Address</th><th>Legacy GE</th>
            <th>Range</th><th>Setpoints (Lo / Hi / HH)</th><th>Description</th>
          </tr>
        </thead>
        <tbody>
          {"".join(io_rows_html)}
        </tbody>
      </table>
    </section>

    {"".join(routine_cards)}
  </main>
  <script>
    function scrollToRoutine(id) {{
      const el = document.getElementById(id);
      if (el) el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    }}
    function copyCode(preId, btn) {{
      const text = document.getElementById(preId).innerText;
      navigator.clipboard.writeText(text).then(() => {{
        const orig = btn.innerText;
        btn.innerText = 'Copied!';
        setTimeout(() => btn.innerText = orig, 1500);
      }});
    }}
    function filterContent() {{
      const q = document.getElementById('filterInput').value.toLowerCase();
      document.querySelectorAll('#ioTable tbody tr').forEach(tr => {{
        tr.style.display = tr.innerText.toLowerCase().includes(q) ? '' : 'none';
      }});
      document.querySelectorAll('.routine-card').forEach(card => {{
        card.style.display = card.innerText.toLowerCase().includes(q) ? '' : 'none';
      }});
    }}
  </script>
</body>
</html>
"""
    for out_dir in (OUT_DIR_WS, OUT_DIR_DESKTOP):
        with open(os.path.join(out_dir, "P20890_Angola_AB_ST.html"), "w", encoding="utf-8") as f:
            f.write(html_doc)


def main():
    os.makedirs(OUT_DIR_WS, exist_ok=True)
    os.makedirs(OUT_DIR_DESKTOP, exist_ok=True)
    tags = build_controller_tags()
    write_st_files(tags)
    write_csv_tags(tags)
    write_l5x_file(tags)
    write_pdf_report(tags)
    write_html_viewer(tags)
    print(f"Successfully generated {len(ROUTINES)} ST routines and {len(tags)} Controller Tags.")
    for fn in ("P20890_Angola_AB_ST.L5X", "P20890_Angola_AB_Complete.st", "P20890_Angola_AB_Tags.csv", "P20890_Angola_AB_ST.pdf", "P20890_Angola_AB_ST.html"):
        p = os.path.join(OUT_DIR_DESKTOP, fn)
        print(f"  -> {p} ({os.path.getsize(p):,} bytes)")


if __name__ == "__main__":
    main()
