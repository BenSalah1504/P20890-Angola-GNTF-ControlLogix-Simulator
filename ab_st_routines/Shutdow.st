// ============================================================================
// Routine: Shutdow (Emergency Shutdown Matrix per 01-MAN-03-07-PDF-C2C Final)
// Note: Fail-safe outputs are energized (TRUE) when healthy and de-energized (FALSE) on trip.
// ============================================================================

// --- 1. Master Fire & Gas / Process ESD Trip Condition ---
// Causes per 01-MAN-03-07-PDF-C2C Final:
//   - High Gas 30% LEL (R01500_2 / R01500_3) or Open-Path 3.00 LELm (R00375_5)
//   - Flame Detection >= 30% (7404-DF-001, 7404-DF-002, or 7404-DF-003 -> R01501_0)
//   - Manual Foam Release Call Points (7503-FR-001/002 or 7503-FR-003)
//   - Deluge Line Pressure High >= 50 Psi (7503-PST-001 -> R00475_5)
//   - High Fuel Gas Pressure >= 100 Psi (6401-PST-001 -> R00455_5)
//   - ESD Fuel Gas Pushbutton E9 (6401-ESDV-001 -> R00707_1)
ESD_Trip_Condition := (R01500_2 OR R01500_3 OR R01501_0 OR R00495_5 OR R00535_5 OR R00475_5 OR R00455_5)
                      AND NOT R00709_0; // Bypassed if S3 (INHIBIT_ALL_OUTPUTS) is active

// R01510_0 -> PumpShutdown (ESD_TRIP, Local:8:O.Data.0): Energized (1) = Healthy, De-energized (0) = Trip
R01510_0 := NOT ESD_Trip_Condition;

// R01511_0 -> 6401-EY-001/002 Fuel Gas ESDV Solenoid (Local:8:O.Data.1)
// Tripped by ESD_Trip_Condition OR E9 Pushbutton (6401-ESDV-001 / R00707_1)
R01511_0 := NOT (ESD_Trip_Condition OR (R00707_1 AND NOT R00709_0));

// R01511_1 -> P2100/P2200 Oil Booster Pump Shutdown Relay (Local:8:O.Data.8)
// Tripped by ESD_Trip_Condition OR High-High Oil Injection Manifold Pressure PIT-003 (2800 Psi)
R01511_1 := NOT (ESD_Trip_Condition OR (PIT_003_PAHH_Latch AND NOT R00709_0));

// R01511_2 -> P3600/P3700 Water Booster Pump Shutdown Relay (Local:8:O.Data.9)
// Tripped by ESD_Trip_Condition OR High-High Water Injection Manifold Pressure PIT-002 (900 Psi)
R01511_2 := NOT (ESD_Trip_Condition OR (PIT_002_PAHH_Latch AND NOT R00709_0));

// --- 2. GNTF Upgrade: SD-GE (7404-ESD-GEN Shut Down of All Gas Generators, Local:8:O.Data.21) ---
// Tripped by:
//   - High Gas 30% LEL in Gas Generator Room (GD-001, GD-002, or GD-003 -> GD_Any_Hi_Latch)
//   - Smoke Detection >= 30% in Electrical/Generator Room (SD-001/002 -> SD_001_002_Latch)
//   - Master ESD Trip Condition (ESD_Trip_Condition)
SD_GE := (GD_Any_Hi_Latch OR SD_001_002_Latch OR ESD_Trip_Condition) AND NOT R00709_0;
