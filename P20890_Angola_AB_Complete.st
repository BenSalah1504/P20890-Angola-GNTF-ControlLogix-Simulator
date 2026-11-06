// ============================================================================
// ALLEN-BRADLEY CONTROLLOGIX 5580 (1756-L82E) STRUCTURED TEXT PROGRAM
// Project : GNTF QUINGUILA CONTROL SYSTEM UPGRADE (P20890_Angola / FGCP-7404-001)
// Client  : SONANGOL P&P / EPPM ANGOLA / ASTRE
// Chassis : 1756-A13 (13-Slot), Power Supply: 1756-PB72 (24V DC)
// CPU     : Slot 0 = 1756-L82E (IP: 192.168.20.10/24)
// Modules : Slot 1 = 1756-N2, Slots 2..5 = 4x 1756-IF16, Slot 6 = 1756-IF8H,
//           Slot 7 = 1756-IB32, Slot 8 = 1756-OB32, Slot 9 = MVI56E-MCM
// ============================================================================

// ****************************************************************************
// ROUTINE: MainRoutine — Main Executive Routine (Converted from GE VersaMax _MAIN + GNTF Upgrade Extensions)
// ****************************************************************************
// ============================================================================
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

// ****************************************************************************
// ROUTINE: Init — First-Scan Setpoint & Calibration Initialization (01-MAN-03-13-PDF-C1 & Legacy Init)
// ****************************************************************************
// ============================================================================
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

// ****************************************************************************
// ROUTINE: Input — Hardware Input Acquisition & Mapping (Slot 2-7 1756 Modules -> Internal Tags)
// ****************************************************************************
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

// ****************************************************************************
// ROUTINE: DI_1 — Digital Input Conditioning & ESDV Discrepancy Logic (6401-ZSH/ZSL-001, 7503-FS/LS)
// ****************************************************************************
// ============================================================================
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

// ****************************************************************************
// ROUTINE: DI_2 — Digital Input Conditioning Part 2 (Deluge Line Continuity, Pump B Inhibit, E9 ESDV, S2/S3 Inhibits, E1..E6 Pump E-Stops)
// ****************************************************************************
// ============================================================================
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

// ****************************************************************************
// ROUTINE: CalcVa1 — Analog Scaling Subroutine 1 (7404-DG-001 .. 7404-DG-008)
// ****************************************************************************
// ============================================================================
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

// ****************************************************************************
// ROUTINE: CalcVa2 — Analog Scaling Subroutine 2 (7404-DG-009..012, DF-001..002, DG-011R, SpareAI_16)
// ****************************************************************************
// ============================================================================
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

// ****************************************************************************
// ROUTINE: CalcVa3 — Analog Scaling Subroutine 3 (7002-PST-001, 6401-PST-001, 7503-PST-001, 7503-FR-001/002/003)
// ****************************************************************************
// ============================================================================
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

// ****************************************************************************
// ROUTINE: AI_1 — Analog Input Processing & Fault Detection Group 1 (7404-DG-001 .. 7404-DG-008)
// ****************************************************************************
// ============================================================================
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

// ****************************************************************************
// ROUTINE: AI_2 — Analog Input Processing & Fault Detection Group 2 (7404-DG-009..012, DF-001..002, DG-011R)
// ****************************************************************************
// ============================================================================
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

// ****************************************************************************
// ROUTINE: AI_3 — Analog Input Processing & Fault Detection Group 3 (PST-001s & Foam Call Points FR-001..003)
// ****************************************************************************
// ============================================================================
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

// ****************************************************************************
// ROUTINE: AI_4_New — GNTF Upgrade New Analog, HART & Modbus Channels (GD-001..003, PIT-001..003, H2S-001..012, DF-003, SD-001/002, LIT-100..400, FT-001)
// ****************************************************************************
// ============================================================================
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

// ****************************************************************************
// ROUTINE: Ai_AL_1 — Analog Alarm Threshold & Latching Group 1 (7404-DG-001 .. 7404-DG-008)
// ****************************************************************************
// ============================================================================
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

// ****************************************************************************
// ROUTINE: Ai_AL_2 — Analog Alarm Threshold & Latching Group 2 (7404-DG-009..012, DF-001..002, DG-011R)
// ****************************************************************************
// ============================================================================
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

// ****************************************************************************
// ROUTINE: Ai_AL_3 — Analog Alarm Threshold & Latching Group 3 (PST-001s & Manual Foam Call Points FR-001..003)
// ****************************************************************************
// ============================================================================
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

// ****************************************************************************
// ROUTINE: Vote_1 — Detector Voting Logic (1oo12 / 2oo12 CH4 Point Gas Detectors, Open Path & Flame Detectors)
// ****************************************************************************
// ============================================================================
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

// ****************************************************************************
// ROUTINE: Logic — Deluge Pump A & Standby Pump B Automatic Start/Stop Sequencing
// ****************************************************************************
// ============================================================================
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

// ****************************************************************************
// ROUTINE: CE_LOG — Master Cause & Effect Matrix Orchestrator (Calls Indicat, Shutdow, Protect, Loc_Al, FLT_1)
// ****************************************************************************
// ============================================================================
// Routine: CE_LOG (Cause & Effect Matrix Orchestrator)
// Reference: CAUSE & EFFECT 01-MAN-03-07-PDF-C2C Final
// ============================================================================

JSR(Indicat);
JSR(Shutdow);
JSR(Protect);
JSR(Loc_Al);
JSR(FLT_1);

// ****************************************************************************
// ROUTINE: Indicat — FGCP Front Panel LED Indicators (L14 Closed, L15 Open, L16 Low Air, L17 Low Fuel Gas, CR1..CR6 Pump LEDs)
// ****************************************************************************
// ============================================================================
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

// ****************************************************************************
// ROUTINE: Shutdow — Emergency Shutdown Logic (ESD_TRIP, 6401-EY-001/002, P2100/2200, P3600/3700, SD-GE Gas Generators)
// ****************************************************************************
// ============================================================================
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

// ****************************************************************************
// ROUTINE: Protect — Deluge & Foam Protection Status Mapping
// ****************************************************************************
// ============================================================================
// Routine: Protect (Firewater / Foam Protection Status & Deluge Confirmation)
// ============================================================================

// Deluge / Foam System Activated Status (7503-PST-001 >= 50 Psi or Pump A/B Running)
Deluge_Released_Status := R00475_5;
Foam_System_Inhibited  := R00708_0 OR R00709_0;

// ****************************************************************************
// ROUTINE: Loc_Al — Audible/Visual Alarm Sounder Modes (7404-SA-001/002, Z1, PA-001, H2SA-001/002, SDA-001)
// ****************************************************************************
// ============================================================================
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

// ****************************************************************************
// ROUTINE: FLT_1 — System, Transmitter & Line Fault Aggregation (PLC_Fault Output)
// ****************************************************************************
// ============================================================================
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

// ****************************************************************************
// ROUTINE: Sound — Pump House Alarm Bell Driver (7404-SA-001/002 Continuous vs Discontinuous Modulation)
// ****************************************************************************
// ============================================================================
// Routine: Sound (7404-SA-001/002 Pump House Alarm Bell Driver)
// ============================================================================

// Drive 7404-SA-001/002 (R01511_3) Continuous or Discontinuous (modulated by 0.8s flasher R01598_0),
// silenced by M00001_System_Accept (E12) or inhibited by S3 (R00709_0)
R01511_3 := (Bell_Mode_Continuous OR (Bell_Mode_Discontinuous AND R01598_0))
            AND NOT Alarm_Silence_Latch
            AND NOT R00709_0;

// ****************************************************************************
// ROUTINE: Output — Hardware Digital Output Driver (Internal Tags -> Slot 8 1756-OB32 Local:8:O.Data.0..31)
// ****************************************************************************
// ============================================================================
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
