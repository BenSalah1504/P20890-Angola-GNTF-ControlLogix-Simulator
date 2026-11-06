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
