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
