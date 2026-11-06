// ============================================================================
// Routine: Protect (Firewater / Foam Protection Status & Deluge Confirmation)
// ============================================================================

// Deluge / Foam System Activated Status (7503-PST-001 >= 50 Psi or Pump A/B Running)
Deluge_Released_Status := R00475_5;
Foam_System_Inhibited  := R00708_0 OR R00709_0;
