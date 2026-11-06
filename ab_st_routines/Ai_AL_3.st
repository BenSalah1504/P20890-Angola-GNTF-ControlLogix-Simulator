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
