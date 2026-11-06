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
