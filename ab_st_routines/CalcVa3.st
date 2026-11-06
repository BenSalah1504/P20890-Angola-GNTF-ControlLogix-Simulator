// ============================================================================
// Routine: CalcVa3 (Engineering Unit Scaling for Analog Channels 17..24)
// Formula: EU = ((Span - Zero) / 32000.0) * Raw + Zero
// ============================================================================

R00433 := ((R00423 - R00421) / 32000.0) * DINT_TO_REAL(R00017) + R00421; // 7002-PST-001 Air Accumulator (Psi)
R00453 := ((R00443 - R00441) / 32000.0) * DINT_TO_REAL(R00018) + R00441; // 6401-PST-001 Fuel Gas Pressure (Psi)
R00473 := ((R00463 - R00461) / 32000.0) * DINT_TO_REAL(R00019) + R00461; // 7503-PST-001 Deluge Pressure (Psi)
R00493 := ((R00483 - R00481) / 32000.0) * DINT_TO_REAL(R00020) + R00481; // 7503-FR-001/002 Outside Foam MAC (%)
R00513 := ((R00503 - R00501) / 32000.0) * DINT_TO_REAL(R00021) + R00501; // SpareAI_21 (%)
R00533 := ((R00523 - R00521) / 32000.0) * DINT_TO_REAL(R00022) + R00521; // 7503-FR-003 Inside Foam MAC (%)
R00553 := ((R00543 - R00541) / 32000.0) * DINT_TO_REAL(R00023) + R00541; // SpareAI_23 (%)
R00573 := ((R00563 - R00561) / 32000.0) * DINT_TO_REAL(R00024) + R00561; // SpareAI_24 (%)
