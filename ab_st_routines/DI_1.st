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
