// ============================================================================
// Routine: Init (Initialization of Calibration Ranges & Alarm Setpoints)
// Reference: List of Parameters and Set Points (01-MAN-03-13-PDF-C1)
//            Cause & Effect Matrix (01-MAN-03-07-PDF-C2C Final)
// ============================================================================

// --- 1. CH4 Point Gas Detectors 7404-DG-001..012 (0 - 100 %LEL, Low=20, High=30) ---
// Legacy GE raw counts (32000 = 100%): 0-100% LEL, HiFault=105, LoFault=-4, HiAlarm=30, LoAlarm=20
R00101 := 0.0;     R00103 := 100.0;   R00105 := 105.0;   R00107 := -4.0;    R00109 := 30.0;    R00111 := 20.0; // 7404-DG-001
R00121 := 0.0;     R00123 := 100.0;   R00125 := 105.0;   R00127 := -4.0;    R00129 := 30.0;    R00131 := 20.0; // 7404-DG-002
R00141 := 0.0;     R00143 := 100.0;   R00145 := 105.0;   R00147 := -4.0;    R00149 := 30.0;    R00151 := 20.0; // 7404-DG-003
R00161 := 0.0;     R00163 := 100.0;   R00165 := 105.0;   R00167 := -4.0;    R00169 := 30.0;    R00171 := 20.0; // 7404-DG-004
R00181 := 0.0;     R00183 := 100.0;   R00185 := 105.0;   R00187 := -4.0;    R00189 := 30.0;    R00191 := 20.0; // 7404-DG-005
R00201 := 0.0;     R00203 := 100.0;   R00205 := 105.0;   R00207 := -4.0;    R00209 := 30.0;    R00211 := 20.0; // 7404-DG-006
R00221 := 0.0;     R00223 := 100.0;   R00225 := 105.0;   R00227 := -4.0;    R00229 := 30.0;    R00231 := 20.0; // 7404-DG-007
R00241 := 0.0;     R00243 := 100.0;   R00245 := 105.0;   R00247 := -4.0;    R00249 := 30.0;    R00251 := 20.0; // 7404-DG-008
R00261 := 0.0;     R00263 := 100.0;   R00265 := 105.0;   R00267 := -4.0;    R00269 := 30.0;    R00271 := 20.0; // 7404-DG-009
R00281 := 0.0;     R00283 := 100.0;   R00285 := 105.0;   R00287 := -4.0;    R00289 := 30.0;    R00291 := 20.0; // 7404-DG-010
R00301 := 0.0;     R00303 := 100.0;   R00305 := 105.0;   R00307 := -4.0;    R00309 := 30.0;    R00311 := 20.0; // 7404-DG-011 (was SpareAI_11)
R00381 := 0.0;     R00383 := 100.0;   R00385 := 105.0;   R00387 := -4.0;    R00389 := 30.0;    R00391 := 20.0; // 7404-DG-012 (was SpareAI_15)

// --- 2. Flame Detectors 7404-DF-001..002 (0 - 100%, HiAlarm=30%) ---
R00321 := 0.0;     R00323 := 100.0;   R00325 := 105.0;   R00327 := -4.0;    R00329 := 30.0;    R00331 := 101.0; // 7404-DF-001
R00341 := 0.0;     R00343 := 100.0;   R00345 := 105.0;   R00347 := -4.0;    R00349 := 30.0;    R00351 := 101.0; // 7404-DF-002

// --- 3. Open-Path Gas Detector 7404-DG-011R (0 - 5.00 LELm, Low=1.00, High=3.00) ---
R00361 := 0.0;     R00363 := 5.00;    R00365 := 5.10;    R00367 := -0.78125; R00369 := 3.00;   R00371 := 1.00;  // 7404-DG-011R
R00581 := -0.46875; // Beam Block / Optic Fault upper window (-0.78125 to -0.46875 LELm)

// --- 4. Pressure Transmitters & Manual Call Points (Slot 3) ---
R00401 := 0.0;     R00403 := 100.0;   R00405 := 105.0;   R00407 := -4.0;    R00409 := 30.0;    R00411 := 20.0;  // SpareAI_16
R00421 := 0.0;     R00423 := 100.0;   R00425 := 105.0;   R00427 := -4.0;    R00429 := -10.0;   R00431 := 50.0;  // 7002-PST-001 (Air Accumulator PAL=50 psi)
R00441 := 0.0;     R00443 := 150.0;   R00445 := 155.0;   R00447 := -4.0;    R00449 := 100.0;   R00451 := 40.0;  // 6401-PST-001 (Fuel Gas PAL=40 psi, PAH=100 psi)
R00461 := 0.0;     R00463 := 100.0;   R00465 := 102.0;   R00467 := -4.0;    R00469 := 50.0;    R00471 := 101.0; // 7503-PST-001 (Deluge Pressure PAH=50 psi)
R00481 := 0.0;     R00483 := 100.0;   R00485 := 105.0;   R00487 := -4.0;    R00489 := 30.0;    R00491 := 101.0; // 7503-FR-001/002 (Outside Foam MAC)
R00501 := 0.0;     R00503 := 100.0;   R00505 := 105.0;   R00507 := -4.0;    R00509 := 30.0;    R00511 := 20.0;  // SpareAI_21
R00521 := 0.0;     R00523 := 100.0;   R00525 := 105.0;   R00527 := -4.0;    R00529 := 30.0;    R00531 := 101.0; // 7503-FR-003 (Inside Foam MAC)
R00541 := 0.0;     R00543 := 100.0;   R00545 := 105.0;   R00547 := -4.0;    R00549 := 30.0;    R00551 := 20.0;  // SpareAI_23
R00561 := 0.0;     R00563 := 100.0;   R00565 := 105.0;   R00567 := -4.0;    R00569 := 30.0;    R00571 := 20.0;  // SpareAI_24

// --- 5. GNTF Upgrade New Instrument Setpoints (01-MAN-03-13-PDF-C1) ---
// Gas Generator Room CH4 Detectors GD-001..003 (0-100 %LEL)
SP_GD_Low_LEL        := 20.0;   // Low Gas Alarm = 20% LEL
SP_GD_High_LEL       := 30.0;   // High Gas Alarm = 30% LEL (Trips SD-GE on 2oo3 or 1ooN per C&E)

// H2S Detectors H2S-001..012 (0-100 PPM)
SP_H2S_Low_PPM       := 10.0;   // Low H2S Alarm = 10 PPM (Discontinuous H2SA-001/002 + Z1)
SP_H2S_High_PPM      := 20.0;   // High H2S Alarm = 20 PPM (Continuous H2SA-001/002 + Z1)

// Flame Detector 7404-DF-003 & Smoke Detectors SD-001/002 (0-100 %)
SP_DF003_High        := 30.0;   // Flame Detector 3 Fire Threshold = 30%
SP_SD_High           := 30.0;   // Smoke Detector 1/2 Fire Threshold = 30% (Trips SD-GE + SDA-001 + Z1)

// Manifold Pressure Transmitters PIT-001, PIT-002, PIT-003
SP_PIT001_PAL        := 10.0;   // Oil Expedition Low Pressure = 10 Psi
SP_PIT001_PAH        := 100.0;  // Oil Expedition High Pressure = 100 Psi
SP_PIT002_PAL        := 200.0;  // Water Injection Low Pressure = 200 Psi
SP_PIT002_PAH        := 800.0;  // Water Injection High Pressure = 800 Psi
SP_PIT002_PAHH       := 900.0;  // Water Injection High-High Pressure = 900 Psi (Trips P-3800/3900 & P-3600/3700)
SP_PIT003_PAL        := 1700.0; // Oil Injection Low Pressure = 1700 Psi
SP_PIT003_PAH        := 2700.0; // Oil Injection High Pressure = 2700 Psi
SP_PIT003_PAHH       := 2800.0; // Oil Injection High-High Pressure = 2800 Psi (Trips P-2300..2600 & P-2100/2200)

// Tank Level Transmitters LIT-100..400 (Slot 6 1756-IF8H)
SP_LIT100_LAL        := 0.7;    SP_LIT100_LAH := 9.0;   // Tank T-100 (0-10.0 m)
SP_LIT200_LAL        := 0.7;    SP_LIT200_LAH := 9.0;   // Tank T-200 (0-10.0 m)
SP_LIT300_LAL        := 0.7;    SP_LIT300_LAH := 9.0;   // Tank T-300 (0-10.0 m)
SP_LIT400_LAL        := 0.7;    SP_LIT400_LAH := 11.0;  // Tank T-400 (0-12.0 m)

// Oil Expedition Flowmeter 6401-FT-001 (Slot 9 Modbus MVI56E-MCM)
SP_FT001_FAL         := 30.0;   // Low Flow Alarm = 30 bbl/h
SP_FT001_FAH         := 300.0;  // High Flow Alarm = 300 bbl/h
