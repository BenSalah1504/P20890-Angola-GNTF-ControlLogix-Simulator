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
