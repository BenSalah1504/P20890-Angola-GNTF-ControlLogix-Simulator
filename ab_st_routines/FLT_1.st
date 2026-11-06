// ============================================================================
// Routine: FLT_1 (System, I/O Module & Transmitter Fault Aggregation)
// ============================================================================

// Aggregate Transmitter Out-of-Range Faults, Open-Path Beam Block, Deluge Line Faults & ESDV Discrepancy
Any_Channel_Fault := R00115_2 OR R00135_2 OR R00155_2 OR R00175_2 OR
                     R00195_2 OR R00215_2 OR R00235_2 OR R00255_2 OR
                     R00275_2 OR R00295_2 OR R00315_2 OR R00335_2 OR
                     R00355_2 OR R00375_2 OR R00395_2 OR R00435_2 OR
                     R00455_2 OR R00475_2 OR R00495_2 OR R00535_2 OR
                     GD_001_Fault OR GD_002_Fault OR GD_003_Fault OR
                     PIT_001_Fault OR PIT_002_Fault OR PIT_003_Fault OR
                     DF_7404_003_Fault OR SD_001_002_Fault OR
                     R00700_6 OR R00704_1 OR R00705_1;

// PLC_Fault Output (Local:8:O.Data.10 / R01513_4): Fail-Safe (Energized = No Fault, De-energized = Fault)
R01513_4 := NOT Any_Channel_Fault;
