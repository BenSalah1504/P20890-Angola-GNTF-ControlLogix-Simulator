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
