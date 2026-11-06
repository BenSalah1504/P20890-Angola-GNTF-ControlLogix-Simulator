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
