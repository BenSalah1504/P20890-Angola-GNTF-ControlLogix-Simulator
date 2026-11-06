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
