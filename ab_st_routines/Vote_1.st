// ============================================================================
// Routine: Vote_1 (Gas & Flame Detector Voting Matrix)
// Reference: Cause & Effect Matrix (01-MAN-03-07-PDF-C2C Final)
// ============================================================================

// --- 1. Count Active Low Gas (20% LEL) & High Gas (30% LEL) Across 7404-DG-001..012 + DG-011R ---
Vote_Gas_Lo_Count := 0;
IF R00115_6 THEN Vote_Gas_Lo_Count := Vote_Gas_Lo_Count + 1; END_IF; // DG-001
IF R00135_6 THEN Vote_Gas_Lo_Count := Vote_Gas_Lo_Count + 1; END_IF; // DG-002
IF R00155_6 THEN Vote_Gas_Lo_Count := Vote_Gas_Lo_Count + 1; END_IF; // DG-003
IF R00175_6 THEN Vote_Gas_Lo_Count := Vote_Gas_Lo_Count + 1; END_IF; // DG-004
IF R00195_6 THEN Vote_Gas_Lo_Count := Vote_Gas_Lo_Count + 1; END_IF; // DG-005
IF R00215_6 THEN Vote_Gas_Lo_Count := Vote_Gas_Lo_Count + 1; END_IF; // DG-006
IF R00235_6 THEN Vote_Gas_Lo_Count := Vote_Gas_Lo_Count + 1; END_IF; // DG-007
IF R00255_6 THEN Vote_Gas_Lo_Count := Vote_Gas_Lo_Count + 1; END_IF; // DG-008
IF R00275_6 THEN Vote_Gas_Lo_Count := Vote_Gas_Lo_Count + 1; END_IF; // DG-009
IF R00295_6 THEN Vote_Gas_Lo_Count := Vote_Gas_Lo_Count + 1; END_IF; // DG-010
IF R00315_6 THEN Vote_Gas_Lo_Count := Vote_Gas_Lo_Count + 1; END_IF; // DG-011
IF R00395_6 THEN Vote_Gas_Lo_Count := Vote_Gas_Lo_Count + 1; END_IF; // DG-012
IF R00375_6 THEN Vote_Gas_Lo_Count := Vote_Gas_Lo_Count + 1; END_IF; // DG-011R (1.00 LELm)

Vote_Gas_Hi_Count := 0;
IF R00115_5 THEN Vote_Gas_Hi_Count := Vote_Gas_Hi_Count + 1; END_IF; // DG-001
IF R00135_5 THEN Vote_Gas_Hi_Count := Vote_Gas_Hi_Count + 1; END_IF; // DG-002
IF R00155_5 THEN Vote_Gas_Hi_Count := Vote_Gas_Hi_Count + 1; END_IF; // DG-003
IF R00175_5 THEN Vote_Gas_Hi_Count := Vote_Gas_Hi_Count + 1; END_IF; // DG-004
IF R00195_5 THEN Vote_Gas_Hi_Count := Vote_Gas_Hi_Count + 1; END_IF; // DG-005
IF R00215_5 THEN Vote_Gas_Hi_Count := Vote_Gas_Hi_Count + 1; END_IF; // DG-006
IF R00235_5 THEN Vote_Gas_Hi_Count := Vote_Gas_Hi_Count + 1; END_IF; // DG-007
IF R00255_5 THEN Vote_Gas_Hi_Count := Vote_Gas_Hi_Count + 1; END_IF; // DG-008
IF R00275_5 THEN Vote_Gas_Hi_Count := Vote_Gas_Hi_Count + 1; END_IF; // DG-009
IF R00295_5 THEN Vote_Gas_Hi_Count := Vote_Gas_Hi_Count + 1; END_IF; // DG-010
IF R00315_5 THEN Vote_Gas_Hi_Count := Vote_Gas_Hi_Count + 1; END_IF; // DG-011
IF R00395_5 THEN Vote_Gas_Hi_Count := Vote_Gas_Hi_Count + 1; END_IF; // DG-012
IF R00375_5 THEN Vote_Gas_Hi_Count := Vote_Gas_Hi_Count + 1; END_IF; // DG-011R (3.00 LELm)

// Voting Outputs (R01500_0 = 1ooN Low Gas, R01500_1 = 2ooN Low Gas, R01500_2 = 1ooN High Gas, R01500_3 = 2ooN High Gas)
R01500_0 := (Vote_Gas_Lo_Count >= 1);
R01500_1 := (Vote_Gas_Lo_Count >= 2);
R01500_2 := (Vote_Gas_Hi_Count >= 1);
R01500_3 := (Vote_Gas_Hi_Count >= 2) OR R00375_5; // 2ooN Point High OR Open-Path DG-011R High (3.00 LELm)

// --- 2. Flame Detector Voting Across 7404-DF-001, 7404-DF-002 & New 7404-DF-003 ---
Vote_Flame_Count := 0;
IF R00335_5 THEN Vote_Flame_Count := Vote_Flame_Count + 1; END_IF; // 7404-DF-001
IF R00355_5 THEN Vote_Flame_Count := Vote_Flame_Count + 1; END_IF; // 7404-DF-002
IF DF_7404_003_Latch THEN Vote_Flame_Count := Vote_Flame_Count + 1; END_IF; // 7404-DF-003

R01501_0 := (Vote_Flame_Count >= 1); // 1oo3 Flame Alarm (Fire Warning / Bell / ESD Trip per C&E)
R01501_1 := (Vote_Flame_Count >= 2); // 2oo3 Confirmed Flame (Deluge / Foam Release)
