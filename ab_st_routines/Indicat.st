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
