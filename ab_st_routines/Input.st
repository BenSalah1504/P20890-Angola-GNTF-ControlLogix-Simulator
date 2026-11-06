// ============================================================================
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
