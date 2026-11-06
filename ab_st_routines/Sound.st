// ============================================================================
// Routine: Sound (7404-SA-001/002 Pump House Alarm Bell Driver)
// ============================================================================

// Drive 7404-SA-001/002 (R01511_3) Continuous or Discontinuous (modulated by 0.8s flasher R01598_0),
// silenced by M00001_System_Accept (E12) or inhibited by S3 (R00709_0)
R01511_3 := (Bell_Mode_Continuous OR (Bell_Mode_Discontinuous AND R01598_0))
            AND NOT Alarm_Silence_Latch
            AND NOT R00709_0;
