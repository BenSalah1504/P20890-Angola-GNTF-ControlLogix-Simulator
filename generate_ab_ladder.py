# -*- coding: utf-8 -*-
"""
Generate Allen-Bradley ControlLogix 5580 (1756-L82E) Relay Ladder Logic (RLL)
project file (.L5X) and Interactive HTML Ladder Diagram Viewer.

Target: Studio 5000 Logix Designer (v32+), 13-slot 1756-A13 chassis with 1756-PB72
Project: GNTF Quinguila Control System Upgrade (P20890_Angola / FGCP-7404-001)
"""
import os
import sys
import html
import xml.sax.saxutils as saxutils

BASE_DIR = r"c:\Users\Wajdi TAKTAK\Desktop\DOC\ws_g\pme_ladder_export"
DESKTOP_DIR = r"C:\Users\Wajdi TAKTAK\Desktop\P20890_Angola"
sys.path.append(BASE_DIR)
import generate_ab_st as G

print("Imported base modules successfully.")

def build_rll_routines():
    """Build all 25 routines as Allen-Bradley Relay Ladder Logic (RLL) rungs."""
    routines = []

    # =========================================================================
    # 1. MainRoutine (Executive Cycle & Subroutine Scheduler)
    # =========================================================================
    rungs = [
        {
            "comment": "Rung 0: 400ms Free-Running Flasher Slow Timer (TMR_Flash_Slow)",
            "text": "XIO(TMR_Flash_Fast.DN)TON(TMR_Flash_Slow,?,?);"
        },
        {
            "comment": "Rung 1: 400ms Flasher Reset Timer (TMR_Flash_Fast)",
            "text": "XIC(TMR_Flash_Slow.DN)TON(TMR_Flash_Fast,?,?);"
        },
        {
            "comment": "Rung 2: Toggle 0.4s Flasher Bit (R01598_0) on Slow Timer Done",
            "text": "XIC(TMR_Flash_Slow.DN)XIO(R01598_1)[XIC(R01598_0)OTU(R01598_0),XIO(R01598_0)OTL(R01598_0)];"
        },
        {
            "comment": "Rung 3: Flasher One-Shot Follower Bit (R01598_1)",
            "text": "XIC(TMR_Flash_Slow.DN)OTE(R01598_1);"
        },
        {
            "comment": "Rung 4: Secondary Toggle Divider Bit (R01598_2)",
            "text": "XIC(R01598_0)XIO(R01598_3)[XIC(R01598_2)OTU(R01598_2),XIO(R01598_2)OTL(R01598_2)];"
        },
        {
            "comment": "Rung 5: Secondary Follower Bit (R01598_3)",
            "text": "XIC(R01598_0)OTE(R01598_3);"
        },
        {
            "comment": "Rung 6: Tertiary Toggle Divider Bit (R01598_4)",
            "text": "XIC(R01598_2)XIO(R01598_5)[XIC(R01598_4)OTU(R01598_4),XIO(R01598_4)OTL(R01598_4)];"
        },
        {
            "comment": "Rung 7: Tertiary Follower Bit (R01598_5)",
            "text": "XIC(R01598_2)OTE(R01598_5);"
        },
        {
            "comment": "Rung 8: First Scan Initialization Subroutine Call (Init)",
            "text": "XIC(S:FS)JSR(Init,0);"
        },
        {
            "comment": "Rung 9: Hardware Digital & Analog Input Processing Subroutine Calls",
            "text": "JSR(Input,0)JSR(DI_1,0)JSR(DI_2,0)JSR(AI_1,0)JSR(AI_2,0)JSR(AI_3,0)JSR(AI_4_New,0);"
        },
        {
            "comment": "Rung 10: Analog Alarm Evaluation & F&G Detector Voting Subroutines",
            "text": "JSR(Ai_AL_1,0)JSR(Ai_AL_2,0)JSR(Ai_AL_3,0)JSR(Vote_1,0);"
        },
        {
            "comment": "Rung 11: Control Logic, Cause & Effect Matrix & Hardware Output Drivers",
            "text": "JSR(Logic,0)JSR(CE_LOG,0)JSR(Sound,0)JSR(Output,0);"
        }
    ]
    routines.append(("MainRoutine", "Main Executive Cycle & Subroutine Scheduler", rungs))

    # =========================================================================
    # 2. Init (Setpoint & Engineering Range Calibration)
    # =========================================================================
    rungs_init = []
    # DG-001..DG-012
    dg_regs = [
        (1, 101, "7404-DG-001 CH4 Gas Detector 1"),
        (2, 121, "7404-DG-002 CH4 Gas Detector 2"),
        (3, 141, "7404-DG-003 CH4 Gas Detector 3"),
        (4, 161, "7404-DG-004 CH4 Gas Detector 4"),
        (5, 181, "7404-DG-005 CH4 Gas Detector 5"),
        (6, 201, "7404-DG-006 CH4 Gas Detector 6"),
        (7, 221, "7404-DG-007 CH4 Gas Detector 7"),
        (8, 241, "7404-DG-008 CH4 Gas Detector 8"),
        (9, 261, "7404-DG-009 CH4 Gas Detector 9"),
        (10, 281, "7404-DG-010 CH4 Gas Detector 10"),
        (11, 301, "7404-DG-011 CH4 Gas Detector 11 (was SpareAI_11)"),
        (12, 381, "7404-DG-012 CH4 Gas Detector 12 (was SpareAI_15)")
    ]
    for ch, base, desc in dg_regs:
        rungs_init.append({
            "comment": f"Initialize {desc}: Zero=0%, Span=100%, HiFlt=105%, LoFlt=-4%, HiAlm=30%, LoAlm=20%",
            "text": f"MOV(0.0,R{base:05d})MOV(100.0,R{base+2:05d})MOV(105.0,R{base+4:05d})MOV(-4.0,R{base+6:05d})MOV(30.0,R{base+8:05d})MOV(20.0,R{base+10:05d});"
        })
    # Flame detectors
    rungs_init.append({
        "comment": "Initialize 7404-DF-001 Flame Detector 1: Zero=0%, Span=100%, Alarm=30%",
        "text": "MOV(0.0,R00321)MOV(100.0,R00323)MOV(105.0,R00325)MOV(-4.0,R00327)MOV(30.0,R00329)MOV(101.0,R00331);"
    })
    rungs_init.append({
        "comment": "Initialize 7404-DF-002 Flame Detector 2: Zero=0%, Span=100%, Alarm=30%",
        "text": "MOV(0.0,R00341)MOV(100.0,R00343)MOV(105.0,R00345)MOV(-4.0,R00347)MOV(30.0,R00349)MOV(101.0,R00351);"
    })
    # Open-path
    rungs_init.append({
        "comment": "Initialize 7404-DG-011R Open Path IR Gas Detector: 0-5.00 LELm, Lo=1.00, Hi=3.00, Optic Fault Window -0.78125 to -0.46875",
        "text": "MOV(0.0,R00361)MOV(5.00,R00363)MOV(5.10,R00365)MOV(-0.78125,R00367)MOV(3.00,R00369)MOV(1.00,R00371)MOV(-0.46875,R00581);"
    })
    # Pressure & Foam MACs
    rungs_init.append({
        "comment": "Initialize 7002-PST-001 Air Accumulator Pressure: 0-100 Psi, Low Alarm PAL=50 Psi (LED L16)",
        "text": "MOV(0.0,R00421)MOV(100.0,R00423)MOV(105.0,R00425)MOV(-4.0,R00427)MOV(-10.0,R00429)MOV(50.0,R00431);"
    })
    rungs_init.append({
        "comment": "Initialize 6401-PST-001 Fuel Gas Pressure: 0-150 Psi, PAL=40 Psi (LED L17), PAH=100 Psi (Station ESD)",
        "text": "MOV(0.0,R00441)MOV(150.0,R00443)MOV(155.0,R00445)MOV(-4.0,R00447)MOV(100.0,R00449)MOV(40.0,R00451);"
    })
    rungs_init.append({
        "comment": "Initialize 7503-PST-001 Deluge Line Pressure: 0-100 Psi, High Alarm PAH=50 Psi (Deluge Released)",
        "text": "MOV(0.0,R00461)MOV(100.0,R00463)MOV(102.0,R00465)MOV(-4.0,R00467)MOV(50.0,R00469)MOV(101.0,R00471);"
    })
    rungs_init.append({
        "comment": "Initialize 7503-FR-001/002 Outside Foam Release MAC Call Points (Alarm Threshold = 30%)",
        "text": "MOV(0.0,R00481)MOV(100.0,R00483)MOV(105.0,R00485)MOV(-4.0,R00487)MOV(30.0,R00489)MOV(101.0,R00491);"
    })
    rungs_init.append({
        "comment": "Initialize 7503-FR-003 Inside PCR Local CP Foam Release MAC Call Point (Alarm Threshold = 30%)",
        "text": "MOV(0.0,R00521)MOV(100.0,R00523)MOV(105.0,R00525)MOV(-4.0,R00527)MOV(30.0,R00529)MOV(101.0,R00531);"
    })
    rungs_init.append({
        "comment": "Initialize GNTF Upgrade Setpoints: GD-001..003 (20%/30%), H2S-001..012 (10/20 PPM), DF-003 (30%), SD-001/002 (30%)",
        "text": "MOV(20.0,SP_GD_Low_LEL)MOV(30.0,SP_GD_High_LEL)MOV(10.0,SP_H2S_Low_PPM)MOV(20.0,SP_H2S_High_PPM)MOV(30.0,SP_DF003_High)MOV(30.0,SP_SD_High);"
    })
    rungs_init.append({
        "comment": "Initialize Manifold Pressure Setpoints: PIT-001 (10/100 Psi), PIT-002 (200/800/900 Psi), PIT-003 (1700/2700/2800 Psi)",
        "text": "MOV(10.0,SP_PIT001_PAL)MOV(100.0,SP_PIT001_PAH)MOV(200.0,SP_PIT002_PAL)MOV(800.0,SP_PIT002_PAH)MOV(900.0,SP_PIT002_PAHH)MOV(1700.0,SP_PIT003_PAL)MOV(2700.0,SP_PIT003_PAH)MOV(2800.0,SP_PIT003_PAHH);"
    })
    rungs_init.append({
        "comment": "Initialize Tank Level (LIT-100..400) & Flowmeter (6401-FT-001) Setpoints: LAL=0.7m, LAH=9.0/11.0m, FAL=30, FAH=300 bbl/h",
        "text": "MOV(0.7,SP_LIT100_LAL)MOV(9.0,SP_LIT100_LAH)MOV(0.7,SP_LIT200_LAL)MOV(9.0,SP_LIT200_LAH)MOV(0.7,SP_LIT300_LAL)MOV(9.0,SP_LIT300_LAH)MOV(0.7,SP_LIT400_LAL)MOV(11.0,SP_LIT400_LAH)MOV(30.0,SP_FT001_FAL)MOV(300.0,SP_FT001_FAH);"
    })
    routines.append(("Init", "Setpoint & Engineering Range Calibration Initialization", rungs_init))

    # =========================================================================
    # 3. Input (Hardware Input Mapping from Slots 2, 3, 4, 7)
    # =========================================================================
    rungs_in = [
        {"comment": "Slot 7 Bit 0: 6401-ZSH-001 ESD Valve Open Limit Switch", "text": "XIC(Local:7:I.Data.0)[OTE(ZSH_6401_001),OTE(G0001)];"},
        {"comment": "Slot 7 Bit 1: 6401-ZSL-001 ESD Valve Closed Limit Switch", "text": "XIC(Local:7:I.Data.1)[OTE(ZSL_6401_001),OTE(G0002)];"},
        {"comment": "Slot 7 Bit 2: FGCP-7404-001 Panel Stop Foam Button (E8) / SpareDI_08", "text": "XIC(Local:7:I.Data.2)[OTE(FS_FGCP_E8),OTE(G0008),OTE(SpareDI_08)];"},
        {"comment": "Slot 7 Bit 3: 7503-LS-002 Diesel Fuel Tank Low Level Switch (NC: 1=OK, 0=Low)", "text": "XIC(Local:7:I.Data.3)[OTE(LS_7503_002),OTE(G0005)];"},
        {"comment": "Slot 7 Bit 4: 7503-FS-001 Field Stop Foam Button (NC: 1=OK, 0=Stop)", "text": "XIC(Local:7:I.Data.4)[OTE(FS_7503_001),OTE(G0003)];"},
        {"comment": "Slot 7 Bit 5: 7503-LS-001 AFFF Foam Concentrate Tank Low Level Switch (NC: 1=OK, 0=Low)", "text": "XIC(Local:7:I.Data.5)[OTE(LS_7503_001),OTE(G0004)];"},
        {"comment": "Slot 7 Bit 6: 75-C-01A Pulsed Line Continuity Feedback for Deluge Pump A", "text": "XIC(Local:7:I.Data.6)[OTE(Pump_A_PulsIn),OTE(G0006)];"},
        {"comment": "Slot 7 Bit 7: 75-C-01B Pulsed Line Continuity Feedback for Deluge Pump B", "text": "XIC(Local:7:I.Data.7)[OTE(Pump_B_Start_PulsIn),OTE(G0007)];"},
        {"comment": "Slot 7 Bit 8: 75-SB-01B Standby Diesel Pump B Inhibited Keyswitch", "text": "XIC(Local:7:I.Data.8)[OTE(Pump_B_Inhibited),OTE(G0009)];"},
        {"comment": "Slot 7 Bit 9: Spare Digital Input 11", "text": "XIC(Local:7:I.Data.9)[OTE(SpareDI_11),OTE(G0011)];"},
        {"comment": "Slot 7 Bit 10: FGCP-7404-001 Alarm Reset Pushbutton (E11)", "text": "XIC(Local:7:I.Data.10)OTE(Reset_PB_E11);"},
        {"comment": "Slot 7 Bit 11: FGCP-7404-001 Alarm Mute / Silence Pushbutton (E12)", "text": "XIC(Local:7:I.Data.11)OTE(Mute_PB_E12);"},
        {"comment": "Slot 7 Bit 12: 6401-ESDV-001 Station Fuel Gas ESD Pushbutton (E9) (NC: 1=Normal, 0=Trip)", "text": "XIC(Local:7:I.Data.12)[OTE(ESDV_6401_001),OTE(G0010)];"},
        {"comment": "Slot 7 Bit 13: FGCP-7404-001 Keyswitch S2 (Inhibition Foam Release)", "text": "XIC(Local:7:I.Data.13)[OTE(INHIBIT_FOAM_REL),OTE(G0012)];"},
        {"comment": "Slot 7 Bit 14: FGCP-7404-001 Keyswitch S3 (Inhibition All Outputs)", "text": "XIC(Local:7:I.Data.14)[OTE(INHIBIT_ALL_OUTPUTS),OTE(G0013)];"},
        {"comment": "Slot 7 Bit 15: 7404-SB-004 Emergency Stop Pushbutton E1 (Power Oil Pump P-2300)", "text": "XIC(Local:7:I.Data.15)OTE(ESTOP_P2300_E1);"},
        {"comment": "Slot 7 Bit 16: 7404-SB-005 Emergency Stop Pushbutton E2 (Power Oil Pump P-2400)", "text": "XIC(Local:7:I.Data.16)OTE(ESTOP_P2400_E2);"},
        {"comment": "Slot 7 Bit 17: 7404-SB-006 Emergency Stop Pushbutton E3 (Power Oil Pump P-2500)", "text": "XIC(Local:7:I.Data.17)OTE(ESTOP_P2500_E3);"},
        {"comment": "Slot 7 Bit 18: 7404-SB-007 Emergency Stop Pushbutton E4 (Power Oil Pump P-2600)", "text": "XIC(Local:7:I.Data.18)OTE(ESTOP_P2600_E4);"},
        {"comment": "Slot 7 Bit 19: 7404-SB-008 Emergency Stop Pushbutton E5 (Water Injection Pump P-3800)", "text": "XIC(Local:7:I.Data.19)OTE(ESTOP_P3800_E5);"},
        {"comment": "Slot 7 Bit 20: 7404-SB-009 Emergency Stop Pushbutton E6 (Water Injection Pump P-3900)", "text": "XIC(Local:7:I.Data.20)OTE(ESTOP_P3900_E6);"},
        {"comment": "Combine E12 Panel Mute Pushbutton with SCADA HMI Accept Bit (M00001)", "text": "[XIC(M00001),XIC(Mute_PB_E12)]OTE(M00001_System_Accept);"},
        {"comment": "Combine E11 Panel Reset Pushbutton with SCADA HMI Reset Bit (M00002)", "text": "[XIC(M00002),XIC(Reset_PB_E11)]OTE(M00002_System_Reset);"}
    ]
    # Analog inputs mapping
    ai_raw_map = [
        ("Slot 2 Ch 0: 7404-DG-001 (Local:2:I.Ch0Data)", "Local:2:I.Ch0Data", "DG_7404_001", "R00001"),
        ("Slot 2 Ch 1: 7404-DG-002 (Local:2:I.Ch1Data)", "Local:2:I.Ch1Data", "DG_7404_002", "R00002"),
        ("Slot 2 Ch 2: 7404-DG-003 (Local:2:I.Ch2Data)", "Local:2:I.Ch2Data", "DG_7404_003", "R00003"),
        ("Slot 2 Ch 3: 7404-DG-004 (Local:2:I.Ch3Data)", "Local:2:I.Ch3Data", "DG_7404_004", "R00004"),
        ("Slot 2 Ch 4: 7404-DG-005 (Local:2:I.Ch4Data)", "Local:2:I.Ch4Data", "DG_7404_005", "R00005"),
        ("Slot 2 Ch 5: 7404-DG-006 (Local:2:I.Ch5Data)", "Local:2:I.Ch5Data", "DG_7404_006", "R00006"),
        ("Slot 2 Ch 6: 7404-DG-007 (Local:2:I.Ch6Data)", "Local:2:I.Ch6Data", "DG_7404_007", "R00007"),
        ("Slot 2 Ch 7: 7404-DG-008 (Local:2:I.Ch7Data)", "Local:2:I.Ch7Data", "DG_7404_008", "R00008"),
        ("Slot 2 Ch 8: 7404-DG-009 (Local:2:I.Ch8Data)", "Local:2:I.Ch8Data", "DG_7404_009", "R00009"),
        ("Slot 2 Ch 9: 7404-DG-010 (Local:2:I.Ch9Data)", "Local:2:I.Ch9Data", "DG_7404_010", "R00010"),
        ("Slot 2 Ch 10: 7404-DG-011 (Local:2:I.Ch10Data)", "Local:2:I.Ch10Data", "DG_7404_011", "R00011"),
        ("Slot 4 Ch 12: 7404-DF-001 (Local:4:I.Ch12Data)", "Local:4:I.Ch12Data", "DF_7404_001", "R00012"),
        ("Slot 4 Ch 13: 7404-DF-002 (Local:4:I.Ch13Data)", "Local:4:I.Ch13Data", "DF_7404_002", "R00013"),
        ("Slot 2 Ch 12: 7404-DG-011R Open Path (Local:2:I.Ch12Data)", "Local:2:I.Ch12Data", "DG_7404_011R", "R00014"),
        ("Slot 2 Ch 11: 7404-DG-012 (Local:2:I.Ch11Data)", "Local:2:I.Ch11Data", "DG_7404_012", "R00015"),
        ("Slot 3 Ch 8: SpareAI_16 (Local:3:I.Ch8Data)", "Local:3:I.Ch8Data", "SpareAI_16", "R00016"),
        ("Slot 3 Ch 4: 7002-PST-001 Air Accumulator (Local:3:I.Ch4Data)", "Local:3:I.Ch4Data", "PST_7002_001", "R00017"),
        ("Slot 3 Ch 5: 6401-PST-001 Fuel Gas (Local:3:I.Ch5Data)", "Local:3:I.Ch5Data", "PST_6401_001", "R00018"),
        ("Slot 3 Ch 3: 7503-PST-001 Deluge Pressure (Local:3:I.Ch3Data)", "Local:3:I.Ch3Data", "PST_7503_001", "R00019"),
        ("Slot 3 Ch 7: 7503-FR-001/002 Outside Foam MAC (Local:3:I.Ch7Data)", "Local:3:I.Ch7Data", "FR_7503_001_002", "R00020"),
        ("Slot 3 Ch 9: SpareAI_21 (Local:3:I.Ch9Data)", "Local:3:I.Ch9Data", "SpareAI_21", "R00021"),
        ("Slot 3 Ch 6: 7503-FR-003 Inside Foam MAC (Local:3:I.Ch6Data)", "Local:3:I.Ch6Data", "FR_7503_003", "R00022"),
        ("Slot 3 Ch 10: SpareAI_23 (Local:3:I.Ch10Data)", "Local:3:I.Ch10Data", "SpareAI_23", "R00023"),
        ("Slot 3 Ch 11: SpareAI_24 (Local:3:I.Ch11Data)", "Local:3:I.Ch11Data", "SpareAI_24", "R00024"),
    ]
    for cmt, src, tag1, tag2 in ai_raw_map:
        rungs_in.append({
            "comment": f"Map {cmt} to Studio 5000 Tag and Register Image",
            "text": f"MOV({src},{tag1})MOV({src},{tag2});"
        })
    routines.append(("Input", "Hardware Input Mapping from Slots 2, 3, 4, 7 to Internal Image", rungs_in))

    # =========================================================================
    # 4. DI_1 (ESDV Position & Discrepancy Timers, Foam Stop, Tank Levels)
    # =========================================================================
    rungs_di1 = [
        {"comment": "Rung 0: 6401-ZSH-001 Valve Open Limit Switch Condition", "text": "XIC(G0001)OTE(R00700_0);"},
        {"comment": "Rung 1: 6401-ZSL-001 Valve Closed Limit Switch Condition", "text": "XIC(G0002)OTE(R00700_1);"},
        {"comment": "Rung 2: ESDV Switch Conflict (Both Open and Closed Active Simultaneously)", "text": "XIC(R00700_0)XIC(R00700_1)OTE(R00700_2);"},
        {"comment": "Rung 3: ESDV Transit Timer (Valve in Transit Neither Open Nor Closed > 10.0s)", "text": "XIO(R00700_0)XIO(R00700_1)TON(TMR_ESDV_Transit,?,?);"},
        {"comment": "Rung 4: ESDV Transit Fault Latch", "text": "XIC(TMR_ESDV_Transit.DN)OTE(R00700_3);"},
        {"comment": "Rung 5: ESDV Commanded Open (EY Energized) but Not Open within 10.0s", "text": "XIC(R01511_0)XIO(R00700_0)TON(TMR_ESDV_CmdOpen,?,?);"},
        {"comment": "Rung 6: ESDV Fail to Open Fault Flag", "text": "XIC(TMR_ESDV_CmdOpen.DN)OTE(R00700_4);"},
        {"comment": "Rung 7: ESDV Commanded Closed (EY De-energized) but Not Closed within 10.0s", "text": "XIO(R01511_0)XIO(R00700_1)TON(TMR_ESDV_CmdClose,?,?);"},
        {"comment": "Rung 8: ESDV Fail to Close Fault Flag", "text": "XIC(TMR_ESDV_CmdClose.DN)OTE(R00700_5);"},
        {"comment": "Rung 9: Consolidated ESDV Position Discrepancy Latch (R00700_6)", "text": "[XIC(R00700_2),XIC(R00700_3),XIC(R00700_4),XIC(R00700_5)]OTL(R00700_6);"},
        {"comment": "Rung 10: Reset ESDV Discrepancy Latch on System Reset", "text": "XIC(M00002_System_Reset)OTU(R00700_6);"},
        {"comment": "Rung 11: 7503-FS-001 Field Stop Foam (NC) or E8 Panel Stop Foam (NO)", "text": "[XIO(G0003),XIC(G0008)][OTE(R00701_0),OTL(R00701_1)];"},
        {"comment": "Rung 12: Reset Foam Stop Latch on System Reset", "text": "XIC(M00002_System_Reset)XIC(G0003)XIO(G0008)OTU(R00701_1);"},
        {"comment": "Rung 13: 7503-LS-001 AFFF Foam Concentrate Tank Low Level Switch (NC: 0=Low)", "text": "XIO(G0004)[OTE(R00702_0),OTL(R00702_1)];"},
        {"comment": "Rung 14: Reset Foam Tank Low Level Latch on System Reset", "text": "XIC(M00002_System_Reset)XIC(G0004)OTU(R00702_1);"},
        {"comment": "Rung 15: 7503-LS-002 Diesel Fuel Tank Low Level Switch (NC: 0=Low)", "text": "XIO(G0005)[OTE(R00703_0),OTL(R00703_1)];"},
        {"comment": "Rung 16: Reset Diesel Tank Low Level Latch on System Reset", "text": "XIC(M00002_System_Reset)XIC(G0005)OTU(R00703_1);"}
    ]
    routines.append(("DI_1", "Digital Input Conditioning & ESD Valve Discrepancy Timers", rungs_di1))

    # =========================================================================
    # 5. DI_2 (Deluge Continuity Check, Keyswitches & E-Stops)
    # =========================================================================
    rungs_di2 = [
        {"comment": "Rung 0: 60-Second Periodic Timer for Deluge Coil Continuity Pulse Test", "text": "XIO(TMR_Pulse_Width.DN)TON(TMR_Pulse_Period,?,?);"},
        {"comment": "Rung 1: 1.0-Second Pulse Width Timer for Deluge Coil Line Check", "text": "XIC(TMR_Pulse_Period.DN)TON(TMR_Pulse_Width,?,?);"},
        {"comment": "Rung 2: Generate Pulse Test Output for Deluge Pump A (Pump_A_PulsOut)", "text": "XIC(TMR_Pulse_Period.DN)XIO(R01512_0)OTE(R01513_12);"},
        {"comment": "Rung 3: Generate Pulse Test Output for Deluge Pump B (Pump_B_Start_PulsOut)", "text": "XIC(TMR_Pulse_Period.DN)XIO(R01512_5)OTE(R01513_13);"},
        {"comment": "Rung 4: Deluge Pump A Line Check Discrepancy Timer (500ms without feedback)", "text": "XIC(R01513_12)XIO(G0006)TON(TMR_PumpA_WireFlt,?,?);"},
        {"comment": "Rung 5: Deluge Pump A Coil Open-Circuit Fault Latch (R00704_1)", "text": "XIC(TMR_PumpA_WireFlt.DN)OTL(R00704_1);"},
        {"comment": "Rung 6: Reset Pump A Open-Circuit Fault on System Reset", "text": "XIC(M00002_System_Reset)OTU(R00704_1);"},
        {"comment": "Rung 7: Deluge Pump B Line Check Discrepancy Timer (500ms without feedback)", "text": "XIC(R01513_13)XIO(G0007)TON(TMR_PumpB_WireFlt,?,?);"},
        {"comment": "Rung 8: Deluge Pump B Coil Open-Circuit Fault Latch (R00705_1)", "text": "XIC(TMR_PumpB_WireFlt.DN)OTL(R00705_1);"},
        {"comment": "Rung 9: Reset Pump B Open-Circuit Fault on System Reset", "text": "XIC(M00002_System_Reset)OTU(R00705_1);"},
        {"comment": "Rung 10: 75-SB-01B Standby Diesel Pump B Inhibited Status", "text": "XIC(G0009)OTE(R00706_0);"},
        {"comment": "Rung 11: 6401-ESDV-001 (E9) Station ESD Pushbutton Condition (NC: 0=Pressed)", "text": "XIO(G0010)[OTE(R00707_0),OTL(R00707_1)];"},
        {"comment": "Rung 12: Reset Station ESD Pushbutton Latch on System Reset", "text": "XIC(M00002_System_Reset)XIC(G0010)OTU(R00707_1);"},
        {"comment": "Rung 13: FGCP-7404-001 Keyswitch S2 (Inhibition Foam Release)", "text": "XIC(G0012)OTE(R00708_0);"},
        {"comment": "Rung 14: FGCP-7404-001 Keyswitch S3 (Inhibition All Outputs)", "text": "XIC(G0013)OTE(R00709_0);"},
        {"comment": "Rung 15: 7404-SB-004 (E1) E-Stop Power Oil Pump P-2300 Latch", "text": "XIC(ESTOP_P2300_E1)OTL(Latch_ESTOP_P2300);"},
        {"comment": "Rung 16: Reset E1 E-Stop on System Reset", "text": "XIC(M00002_System_Reset)OTU(Latch_ESTOP_P2300);"},
        {"comment": "Rung 17: 7404-SB-005 (E2) E-Stop Power Oil Pump P-2400 Latch", "text": "XIC(ESTOP_P2400_E2)OTL(Latch_ESTOP_P2400);"},
        {"comment": "Rung 18: Reset E2 E-Stop on System Reset", "text": "XIC(M00002_System_Reset)OTU(Latch_ESTOP_P2400);"},
        {"comment": "Rung 19: 7404-SB-006 (E3) E-Stop Power Oil Pump P-2500 Latch", "text": "XIC(ESTOP_P2500_E3)OTL(Latch_ESTOP_P2500);"},
        {"comment": "Rung 20: Reset E3 E-Stop on System Reset", "text": "XIC(M00002_System_Reset)OTU(Latch_ESTOP_P2500);"},
        {"comment": "Rung 21: 7404-SB-007 (E4) E-Stop Power Oil Pump P-2600 Latch", "text": "XIC(ESTOP_P2600_E4)OTL(Latch_ESTOP_P2600);"},
        {"comment": "Rung 22: Reset E4 E-Stop on System Reset", "text": "XIC(M00002_System_Reset)OTU(Latch_ESTOP_P2600);"},
        {"comment": "Rung 23: 7404-SB-008 (E5) E-Stop Water Injection Pump P-3800 Latch", "text": "XIC(ESTOP_P3800_E5)OTL(Latch_ESTOP_P3800);"},
        {"comment": "Rung 24: Reset E5 E-Stop on System Reset", "text": "XIC(M00002_System_Reset)OTU(Latch_ESTOP_P3800);"},
        {"comment": "Rung 25: 7404-SB-009 (E6) E-Stop Water Injection Pump P-3900 Latch", "text": "XIC(ESTOP_P3900_E6)OTL(Latch_ESTOP_P3900);"},
        {"comment": "Rung 26: Reset E6 E-Stop on System Reset", "text": "XIC(M00002_System_Reset)OTU(Latch_ESTOP_P3900);"}
    ]
    routines.append(("DI_2", "Deluge Coil Continuity Pulse Monitoring, Keyswitches & E-Stops", rungs_di2))

    # =========================================================================
    # 6. CalcVa1 (Scaling Channels 1..8)
    # =========================================================================
    rungs_cva1 = []
    for ch in range(1, 9):
        base = 101 + (ch - 1) * 20
        eu_reg = base + 12
        raw_reg = ch
        rungs_cva1.append({
            "comment": f"Scale Analog Input Channel {ch} (7404-DG-{ch:03d}) to Engineering Units (%LEL)",
            "text": f"CPT(R{eu_reg:05d},((R{base+2:05d}-R{base:05d})/32000.0)*R{raw_reg:05d}+R{base:05d});"
        })
    routines.append(("CalcVa1", "Engineering Unit Scaling for Analog Channels 1..8 (CPT)", rungs_cva1))

    # =========================================================================
    # 7. AI_1 (Fault Evaluation for Channels 1..8)
    # =========================================================================
    rungs_ai1 = [{"comment": "Execute Engineering Unit Scaling Subroutine CalcVa1", "text": "JSR(CalcVa1,0);"}]
    for ch in range(1, 9):
        base = 101 + (ch - 1) * 20
        eu_reg = base + 12
        flt_base = base + 14
        rungs_ai1.append({
            "comment": f"Channel {ch} (7404-DG-{ch:03d}) High Overrange Fault (> 105% LEL)",
            "text": f"GRT(R{eu_reg:05d},R{base+4:05d})OTE(R{flt_base:05d}_0);"
        })
        rungs_ai1.append({
            "comment": f"Channel {ch} (7404-DG-{ch:03d}) Low Underrange / Wire-Break Fault (< -4% LEL)",
            "text": f"LES(R{eu_reg:05d},R{base+6:05d})OTE(R{flt_base:05d}_1);"
        })
        rungs_ai1.append({
            "comment": f"Channel {ch} (7404-DG-{ch:03d}) Consolidated Transmitter Fault",
            "text": f"[XIC(R{flt_base:05d}_0),XIC(R{flt_base:05d}_1)]OTE(R{flt_base:05d}_2);"
        })
    routines.append(("AI_1", "Scaling & Out-of-Range Fault Detection for Channels 1..8", rungs_ai1))

    # =========================================================================
    # 8. CalcVa2 (Scaling Channels 9..16)
    # =========================================================================
    rungs_cva2 = []
    ch_cva2_info = [
        (9, 261, 9, "7404-DG-009 (%LEL)"),
        (10, 281, 10, "7404-DG-010 (%LEL)"),
        (11, 301, 11, "7404-DG-011 (%LEL)"),
        (12, 321, 12, "7404-DF-001 Flame 1 (%)"),
        (13, 341, 13, "7404-DF-002 Flame 2 (%)"),
        (14, 361, 14, "7404-DG-011R Open Path (LELm)"),
        (15, 381, 15, "7404-DG-012 (%LEL)"),
        (16, 401, 16, "SpareAI_16 (%)"),
    ]
    for ch, base, raw, desc in ch_cva2_info:
        rungs_cva2.append({
            "comment": f"Scale Channel {ch}: {desc} to Engineering Units",
            "text": f"CPT(R{base+12:05d},((R{base+2:05d}-R{base:05d})/32000.0)*R{raw:05d}+R{base:05d});"
        })
    routines.append(("CalcVa2", "Engineering Unit Scaling for Analog Channels 9..16 (CPT)", rungs_cva2))

    # =========================================================================
    # 9. AI_2 (Fault Evaluation for Channels 9..16)
    # =========================================================================
    rungs_ai2 = [{"comment": "Execute Engineering Unit Scaling Subroutine CalcVa2", "text": "JSR(CalcVa2,0);"}]
    for ch, base, raw, desc in ch_cva2_info:
        eu_reg = base + 12
        flt_base = base + 14
        rungs_ai2.append({
            "comment": f"Channel {ch} ({desc}) High Overrange Fault",
            "text": f"GRT(R{eu_reg:05d},R{base+4:05d})OTE(R{flt_base:05d}_0);"
        })
        rungs_ai2.append({
            "comment": f"Channel {ch} ({desc}) Low Underrange Fault",
            "text": f"LES(R{eu_reg:05d},R{base+6:05d})OTE(R{flt_base:05d}_1);"
        })
        if ch == 14:  # Open Path DG-011R: Optical Fault window -0.78125 to -0.46875 LELm
            rungs_ai2.append({
                "comment": "7404-DG-011R Open Path Optical Fault / Beam Block Window (-0.78125 to -0.46875 LELm)",
                "text": f"LIM(R{base+6:05d},R{eu_reg:05d},R00581)OTE(R{flt_base:05d}_7);"
            })
            rungs_ai2.append({
                "comment": "7404-DG-011R Consolidated Transmitter Fault (Overrange, Wire Break or Beam Block)",
                "text": f"[XIC(R{flt_base:05d}_0),XIC(R{flt_base:05d}_1),XIC(R{flt_base:05d}_7)]OTE(R{flt_base:05d}_2);"
            })
        else:
            rungs_ai2.append({
                "comment": f"Channel {ch} ({desc}) Consolidated Transmitter Fault",
                "text": f"[XIC(R{flt_base:05d}_0),XIC(R{flt_base:05d}_1)]OTE(R{flt_base:05d}_2);"
            })
    routines.append(("AI_2", "Scaling & Fault Detection for Channels 9..16 (DG-011R Beam Block)", rungs_ai2))

    # =========================================================================
    # 10. CalcVa3 (Scaling Channels 17..24)
    # =========================================================================
    rungs_cva3 = []
    ch_cva3_info = [
        (17, 421, 17, "7002-PST-001 Air Accumulator Pressure (Psi)"),
        (18, 441, 18, "6401-PST-001 Fuel Gas Pressure (Psi)"),
        (19, 461, 19, "7503-PST-001 Deluge Line Pressure (Psi)"),
        (20, 481, 20, "7503-FR-001/002 Outside Foam Release MAC (%)"),
        (21, 501, 21, "SpareAI_21 (%)"),
        (22, 521, 22, "7503-FR-003 Inside PCR Foam Release MAC (%)"),
        (23, 541, 23, "SpareAI_23 (%)"),
        (24, 561, 24, "SpareAI_24 (%)"),
    ]
    for ch, base, raw, desc in ch_cva3_info:
        rungs_cva3.append({
            "comment": f"Scale Channel {ch}: {desc} to Engineering Units",
            "text": f"CPT(R{base+12:05d},((R{base+2:05d}-R{base:05d})/32000.0)*R{raw:05d}+R{base:05d});"
        })
    routines.append(("CalcVa3", "Engineering Unit Scaling for Analog Channels 17..24 (CPT)", rungs_cva3))

    # =========================================================================
    # 11. AI_3 (Fault Evaluation for Channels 17..24)
    # =========================================================================
    rungs_ai3 = [{"comment": "Execute Engineering Unit Scaling Subroutine CalcVa3", "text": "JSR(CalcVa3,0);"}]
    for ch, base, raw, desc in ch_cva3_info:
        eu_reg = base + 12
        flt_base = base + 14
        rungs_ai3.append({
            "comment": f"Channel {ch} ({desc}) High Overrange Fault",
            "text": f"GRT(R{eu_reg:05d},R{base+4:05d})OTE(R{flt_base:05d}_0);"
        })
        rungs_ai3.append({
            "comment": f"Channel {ch} ({desc}) Low Underrange Fault",
            "text": f"LES(R{eu_reg:05d},R{base+6:05d})OTE(R{flt_base:05d}_1);"
        })
        rungs_ai3.append({
            "comment": f"Channel {ch} ({desc}) Consolidated Transmitter Fault",
            "text": f"[XIC(R{flt_base:05d}_0),XIC(R{flt_base:05d}_1)]OTE(R{flt_base:05d}_2);"
        })
    routines.append(("AI_3", "Scaling & Fault Detection for Channels 17..24 (PST & Foam MACs)", rungs_ai3))

    # =========================================================================
    # 12. AI_4_New (GNTF Upgrade New Instruments Scaling & Alarms)
    # =========================================================================
    rungs_ai4 = [
        # Gas Generator Room GD-001..003
        {"comment": "Scale GD-001 CH4 Gas Detector (Gas Generator Room) 0-100 %LEL", "text": "CPT(GD_001_EU,(100.0/32000.0)*Local:2:I.Ch13Data);"},
        {"comment": "GD-001 Fault Evaluation (< -4% or > 105% LEL)", "text": "[GRT(GD_001_EU,105.0),LES(GD_001_EU,-4.0)]OTE(GD_001_Fault);"},
        {"comment": "GD-001 Low Gas Alarm (>= 20% LEL)", "text": "XIO(GD_001_Fault)GEQ(GD_001_EU,SP_GD_Low_LEL)OTE(GD_001_Lo);"},
        {"comment": "GD-001 High Gas Alarm (>= 30% LEL - Trips SD-GE)", "text": "XIO(GD_001_Fault)GEQ(GD_001_EU,SP_GD_High_LEL)OTE(GD_001_Hi);"},

        {"comment": "Scale GD-002 CH4 Gas Detector (Gas Generator Room) 0-100 %LEL", "text": "CPT(GD_002_EU,(100.0/32000.0)*Local:2:I.Ch14Data);"},
        {"comment": "GD-002 Fault Evaluation (< -4% or > 105% LEL)", "text": "[GRT(GD_002_EU,105.0),LES(GD_002_EU,-4.0)]OTE(GD_002_Fault);"},
        {"comment": "GD-002 Low Gas Alarm (>= 20% LEL)", "text": "XIO(GD_002_Fault)GEQ(GD_002_EU,SP_GD_Low_LEL)OTE(GD_002_Lo);"},
        {"comment": "GD-002 High Gas Alarm (>= 30% LEL - Trips SD-GE)", "text": "XIO(GD_002_Fault)GEQ(GD_002_EU,SP_GD_High_LEL)OTE(GD_002_Hi);"},

        {"comment": "Scale GD-003 CH4 Gas Detector (Gas Generator Room) 0-100 %LEL", "text": "CPT(GD_003_EU,(100.0/32000.0)*Local:2:I.Ch15Data);"},
        {"comment": "GD-003 Fault Evaluation (< -4% or > 105% LEL)", "text": "[GRT(GD_003_EU,105.0),LES(GD_003_EU,-4.0)]OTE(GD_003_Fault);"},
        {"comment": "GD-003 Low Gas Alarm (>= 20% LEL)", "text": "XIO(GD_003_Fault)GEQ(GD_003_EU,SP_GD_Low_LEL)OTE(GD_003_Lo);"},
        {"comment": "GD-003 High Gas Alarm (>= 30% LEL - Trips SD-GE)", "text": "XIO(GD_003_Fault)GEQ(GD_003_EU,SP_GD_High_LEL)OTE(GD_003_Hi);"},

        {"comment": "Gas Generator Room Low Gas Alarm Latch (GD_Any_Lo_Latch)", "text": "[XIC(GD_001_Lo),XIC(GD_002_Lo),XIC(GD_003_Lo)]OTL(GD_Any_Lo_Latch);"},
        {"comment": "Reset Gas Generator Room Low Gas Alarm on System Reset", "text": "XIC(M00002_System_Reset)OTU(GD_Any_Lo_Latch);"},
        {"comment": "Gas Generator Room High Gas Alarm Latch (GD_Any_Hi_Latch -> Trips SD-GE)", "text": "[XIC(GD_001_Hi),XIC(GD_002_Hi),XIC(GD_003_Hi)]OTL(GD_Any_Hi_Latch);"},
        {"comment": "Reset Gas Generator Room High Gas Alarm on System Reset", "text": "XIC(M00002_System_Reset)OTU(GD_Any_Hi_Latch);"},

        # PIT-001 (0-200 Psi)
        {"comment": "Scale PIT-001 Oil Expedition Manifold Pressure 0-200 Psi", "text": "CPT(PIT_001_EU,(200.0/32000.0)*Local:3:I.Ch0Data);"},
        {"comment": "PIT-001 Fault Evaluation", "text": "[GRT(PIT_001_EU,210.0),LES(PIT_001_EU,-8.0)]OTE(PIT_001_Fault);"},
        {"comment": "PIT-001 Low Pressure PAL (<= 10 Psi)", "text": "XIO(PIT_001_Fault)LEQ(PIT_001_EU,SP_PIT001_PAL)OTE(PIT_001_PAL);"},
        {"comment": "PIT-001 High Pressure PAH (>= 100 Psi)", "text": "XIO(PIT_001_Fault)GEQ(PIT_001_EU,SP_PIT001_PAH)OTE(PIT_001_PAH);"},

        # PIT-002 (0-1500 Psi)
        {"comment": "Scale PIT-002 Water Injection Manifold Pressure 0-1500 Psi", "text": "CPT(PIT_002_EU,(1500.0/32000.0)*Local:3:I.Ch1Data);"},
        {"comment": "PIT-002 Fault Evaluation", "text": "[GRT(PIT_002_EU,1575.0),LES(PIT_002_EU,-60.0)]OTE(PIT_002_Fault);"},
        {"comment": "PIT-002 Low Pressure PAL (<= 200 Psi)", "text": "XIO(PIT_002_Fault)LEQ(PIT_002_EU,SP_PIT002_PAL)OTE(PIT_002_PAL);"},
        {"comment": "PIT-002 High Pressure PAH (>= 800 Psi)", "text": "XIO(PIT_002_Fault)GEQ(PIT_002_EU,SP_PIT002_PAH)OTE(PIT_002_PAH);"},
        {"comment": "PIT-002 High-High Pressure PAHH (>= 900 Psi -> Trips Water Inj & Booster Pumps)", "text": "XIO(PIT_002_Fault)GEQ(PIT_002_EU,SP_PIT002_PAHH)[OTE(PIT_002_PAHH),OTL(PIT_002_PAHH_Latch)];"},
        {"comment": "Reset PIT-002 PAHH Latch on System Reset", "text": "XIC(M00002_System_Reset)XIO(PIT_002_PAHH)OTU(PIT_002_PAHH_Latch);"},

        # PIT-003 (0-3000 Psi)
        {"comment": "Scale PIT-003 Power Oil Manifold Pressure 0-3000 Psi", "text": "CPT(PIT_003_EU,(3000.0/32000.0)*Local:3:I.Ch2Data);"},
        {"comment": "PIT-003 Fault Evaluation", "text": "[GRT(PIT_003_EU,3150.0),LES(PIT_003_EU,-120.0)]OTE(PIT_003_Fault);"},
        {"comment": "PIT-003 Low Pressure PAL (<= 1700 Psi)", "text": "XIO(PIT_003_Fault)LEQ(PIT_003_EU,SP_PIT003_PAL)OTE(PIT_003_PAL);"},
        {"comment": "PIT-003 High Pressure PAH (>= 2700 Psi)", "text": "XIO(PIT_003_Fault)GEQ(PIT_003_EU,SP_PIT003_PAH)OTE(PIT_003_PAH);"},
        {"comment": "PIT-003 High-High Pressure PAHH (>= 2800 Psi -> Trips Power Oil & Booster Pumps)", "text": "XIO(PIT_003_Fault)GEQ(PIT_003_EU,SP_PIT003_PAHH)[OTE(PIT_003_PAHH),OTL(PIT_003_PAHH_Latch)];"},
        {"comment": "Reset PIT-003 PAHH Latch on System Reset", "text": "XIC(M00002_System_Reset)XIO(PIT_003_PAHH)OTU(PIT_003_PAHH_Latch);"},

        # H2S-001..012 (0-100 PPM)
        {"comment": "Scale H2S-001..012 Toxic Gas Detectors (Slot 4 Ch 0..11) to 0-100 PPM", "text": "CPT(H2S_001_EU,(100.0/32000.0)*Local:4:I.Ch0Data)CPT(H2S_002_EU,(100.0/32000.0)*Local:4:I.Ch1Data)CPT(H2S_003_EU,(100.0/32000.0)*Local:4:I.Ch2Data);"},
        {"comment": "Scale H2S-004..006 Toxic Gas Detectors", "text": "CPT(H2S_004_EU,(100.0/32000.0)*Local:4:I.Ch3Data)CPT(H2S_005_EU,(100.0/32000.0)*Local:4:I.Ch4Data)CPT(H2S_006_EU,(100.0/32000.0)*Local:4:I.Ch5Data);"},
        {"comment": "Scale H2S-007..009 Toxic Gas Detectors", "text": "CPT(H2S_007_EU,(100.0/32000.0)*Local:4:I.Ch6Data)CPT(H2S_008_EU,(100.0/32000.0)*Local:4:I.Ch7Data)CPT(H2S_009_EU,(100.0/32000.0)*Local:4:I.Ch8Data);"},
        {"comment": "Scale H2S-010..012 Toxic Gas Detectors", "text": "CPT(H2S_010_EU,(100.0/32000.0)*Local:4:I.Ch9Data)CPT(H2S_011_EU,(100.0/32000.0)*Local:4:I.Ch10Data)CPT(H2S_012_EU,(100.0/32000.0)*Local:4:I.Ch11Data);"},
        {"comment": "Evaluate Any H2S Low Alarm (>= 10 PPM -> Discontinuous Siren + Z1)", "text": "[GEQ(H2S_001_EU,SP_H2S_Low_PPM),GEQ(H2S_002_EU,SP_H2S_Low_PPM),GEQ(H2S_003_EU,SP_H2S_Low_PPM),GEQ(H2S_004_EU,SP_H2S_Low_PPM),GEQ(H2S_005_EU,SP_H2S_Low_PPM),GEQ(H2S_006_EU,SP_H2S_Low_PPM),GEQ(H2S_007_EU,SP_H2S_Low_PPM),GEQ(H2S_008_EU,SP_H2S_Low_PPM),GEQ(H2S_009_EU,SP_H2S_Low_PPM),GEQ(H2S_010_EU,SP_H2S_Low_PPM),GEQ(H2S_011_EU,SP_H2S_Low_PPM),GEQ(H2S_012_EU,SP_H2S_Low_PPM)][OTE(H2S_Any_Lo),OTL(H2S_Lo_Latch)];"},
        {"comment": "Reset H2S Low Alarm Latch on System Reset", "text": "XIC(M00002_System_Reset)OTU(H2S_Lo_Latch);"},
        {"comment": "Evaluate Any H2S High Alarm (>= 20 PPM -> Continuous Siren + Z1)", "text": "[GEQ(H2S_001_EU,SP_H2S_High_PPM),GEQ(H2S_002_EU,SP_H2S_High_PPM),GEQ(H2S_003_EU,SP_H2S_High_PPM),GEQ(H2S_004_EU,SP_H2S_High_PPM),GEQ(H2S_005_EU,SP_H2S_High_PPM),GEQ(H2S_006_EU,SP_H2S_High_PPM),GEQ(H2S_007_EU,SP_H2S_High_PPM),GEQ(H2S_008_EU,SP_H2S_High_PPM),GEQ(H2S_009_EU,SP_H2S_High_PPM),GEQ(H2S_010_EU,SP_H2S_High_PPM),GEQ(H2S_011_EU,SP_H2S_High_PPM),GEQ(H2S_012_EU,SP_H2S_High_PPM)][OTE(H2S_Any_Hi),OTL(H2S_Hi_Latch)];"},
        {"comment": "Reset H2S High Alarm Latch on System Reset", "text": "XIC(M00002_System_Reset)OTU(H2S_Hi_Latch);"},

        # Flame 3 & Smoke Detectors
        {"comment": "Scale 7404-DF-003 Flame Detector 3 (Slot 4 Ch 14)", "text": "CPT(DF_7404_003_EU,(100.0/32000.0)*Local:4:I.Ch14Data);"},
        {"comment": "7404-DF-003 Alarm Evaluation (>= 30% Fire Alarm)", "text": "XIO(DF_7404_003_Fault)GEQ(DF_7404_003_EU,SP_DF003_High)[OTE(DF_7404_003_Alarm),OTL(DF_7404_003_Latch)];"},
        {"comment": "Reset 7404-DF-003 Alarm Latch on System Reset", "text": "XIC(M00002_System_Reset)XIO(DF_7404_003_Alarm)OTU(DF_7404_003_Latch);"},

        {"comment": "Scale SD-001/002 Electrical & Generator Room Smoke Detectors (Slot 4 Ch 15)", "text": "CPT(SD_001_002_EU,(100.0/32000.0)*Local:4:I.Ch15Data);"},
        {"comment": "SD-001/002 Smoke Alarm Evaluation (>= 30% -> Trips SD-GE, SDA-001 & Z1)", "text": "XIO(SD_001_002_Fault)GEQ(SD_001_002_EU,SP_SD_High)[OTE(SD_001_002_Alarm),OTL(SD_001_002_Latch)];"},
        {"comment": "Reset SD-001/002 Smoke Alarm Latch on System Reset", "text": "XIC(M00002_System_Reset)XIO(SD_001_002_Alarm)OTU(SD_001_002_Latch);"},

        # Slot 6: 1756-IF8H Tank Level Transmitters
        {"comment": "Scale LIT-100 Crude Oil Tank T-100 Level (0-10.0 m)", "text": "CPT(LIT_100_EU,(10.0/32000.0)*Local:6:I.Ch0Data);"},
        {"comment": "LIT-100 Tank Level Alarms: Low LAL (<= 0.7m) and High LAH (>= 9.0m)", "text": "[LEQ(LIT_100_EU,SP_LIT100_LAL)OTE(LIT_100_LAL),GEQ(LIT_100_EU,SP_LIT100_LAH)OTE(LIT_100_LAH)];"},

        {"comment": "Scale LIT-200 Crude Oil Tank T-200 Level (0-10.0 m)", "text": "CPT(LIT_200_EU,(10.0/32000.0)*Local:6:I.Ch1Data);"},
        {"comment": "LIT-200 Tank Level Alarms: Low LAL (<= 0.7m) and High LAH (>= 9.0m)", "text": "[LEQ(LIT_200_EU,SP_LIT200_LAL)OTE(LIT_200_LAL),GEQ(LIT_200_EU,SP_LIT200_LAH)OTE(LIT_200_LAH)];"},

        {"comment": "Scale LIT-300 Crude Oil Tank T-300 Level (0-10.0 m)", "text": "CPT(LIT_300_EU,(10.0/32000.0)*Local:6:I.Ch2Data);"},
        {"comment": "LIT-300 Tank Level Alarms: Low LAL (<= 0.7m) and High LAH (>= 9.0m)", "text": "[LEQ(LIT_300_EU,SP_LIT300_LAL)OTE(LIT_300_LAL),GEQ(LIT_300_EU,SP_LIT300_LAH)OTE(LIT_300_LAH)];"},

        {"comment": "Scale LIT-400 Crude Oil Tank T-400 Level (0-12.0 m)", "text": "CPT(LIT_400_EU,(12.0/32000.0)*Local:6:I.Ch3Data);"},
        {"comment": "LIT-400 Tank Level Alarms: Low LAL (<= 0.7m) and High LAH (>= 11.0m)", "text": "[LEQ(LIT_400_EU,SP_LIT400_LAL)OTE(LIT_400_LAL),GEQ(LIT_400_EU,SP_LIT400_LAH)OTE(LIT_400_LAH)];"},

        # Slot 9: MVI56E-MCM Modbus 6401-FT-001 (0-500 bbl/h)
        {"comment": "Scale 6401-FT-001 Oil Expedition Flowmeter (0-500 bbl/h from Modbus Word)", "text": "CPT(FT_6401_001_EU,Local:9:I.Data[6]/10.0);"},
        {"comment": "6401-FT-001 Flowmeter Alarms: Low FAL (<= 30 bbl/h) and High FAH (>= 300 bbl/h)", "text": "[LEQ(FT_6401_001_EU,SP_FT001_FAL)OTE(FT_6401_001_FAL),GEQ(FT_6401_001_EU,SP_FT001_FAH)OTE(FT_6401_001_FAH)];"}
    ]
    routines.append(("AI_4_New", "GNTF Control System Upgrade New Instruments Scaling & Alarms", rungs_ai4))

    # =========================================================================
    # 13. Ai_AL_1 (Alarm Evaluation for Channels 1..8)
    # =========================================================================
    rungs_alm1 = []
    for ch in range(1, 9):
        base = 101 + (ch - 1) * 20
        eu_reg = base + 12
        flt_base = base + 14
        rungs_alm1.append({
            "comment": f"7404-DG-{ch:03d} High Gas Alarm (>= 30% LEL) Condition & Latch",
            "text": f"XIO(R{flt_base:05d}_2)GEQ(R{eu_reg:05d},R{base+8:05d})[OTE(R{flt_base:05d}_3),OTL(R{flt_base:05d}_5)];"
        })
        rungs_alm1.append({
            "comment": f"Reset 7404-DG-{ch:03d} High Gas Alarm Latch on System Reset",
            "text": f"XIC(M00002_System_Reset)OTU(R{flt_base:05d}_5);"
        })
        rungs_alm1.append({
            "comment": f"7404-DG-{ch:03d} Low Gas Alarm (>= 20% LEL) Condition & Latch",
            "text": f"XIO(R{flt_base:05d}_2)GEQ(R{eu_reg:05d},R{base+10:05d})[OTE(R{flt_base:05d}_4),OTL(R{flt_base:05d}_6)];"
        })
        rungs_alm1.append({
            "comment": f"Reset 7404-DG-{ch:03d} Low Gas Alarm Latch on System Reset",
            "text": f"XIC(M00002_System_Reset)OTU(R{flt_base:05d}_6);"
        })
    routines.append(("Ai_AL_1", "Low & High Gas Alarm Evaluation for 7404-DG-001..008", rungs_alm1))

    # =========================================================================
    # 14. Ai_AL_2 (Alarm Evaluation for Channels 9..16)
    # =========================================================================
    rungs_alm2 = []
    # DG-009, DG-010, DG-011
    for ch, base, desc in [(9, 261, "7404-DG-009"), (10, 281, "7404-DG-010"), (11, 301, "7404-DG-011")]:
        eu_reg = base + 12
        flt_base = base + 14
        rungs_alm2.append({
            "comment": f"{desc} High Gas Alarm (>= 30% LEL) Condition & Latch",
            "text": f"XIO(R{flt_base:05d}_2)GEQ(R{eu_reg:05d},R{base+8:05d})[OTE(R{flt_base:05d}_3),OTL(R{flt_base:05d}_5)];"
        })
        rungs_alm2.append({
            "comment": f"Reset {desc} High Gas Alarm Latch on System Reset",
            "text": f"XIC(M00002_System_Reset)OTU(R{flt_base:05d}_5);"
        })
        rungs_alm2.append({
            "comment": f"{desc} Low Gas Alarm (>= 20% LEL) Condition & Latch",
            "text": f"XIO(R{flt_base:05d}_2)GEQ(R{eu_reg:05d},R{base+10:05d})[OTE(R{flt_base:05d}_4),OTL(R{flt_base:05d}_6)];"
        })
        rungs_alm2.append({
            "comment": f"Reset {desc} Low Gas Alarm Latch on System Reset",
            "text": f"XIC(M00002_System_Reset)OTU(R{flt_base:05d}_6);"
        })
    # Flame detectors DF-001 & DF-002
    rungs_alm2.append({
        "comment": "7404-DF-001 Flame Detector 1 Fire Alarm (>= 30%) Condition & Latch",
        "text": "XIO(R00335_2)GEQ(R00333,R00329)[OTE(R00335_3),OTL(R00335_5)];"
    })
    rungs_alm2.append({
        "comment": "Reset 7404-DF-001 Fire Alarm Latch on System Reset",
        "text": "XIC(M00002_System_Reset)OTU(R00335_5);"
    })
    rungs_alm2.append({
        "comment": "7404-DF-002 Flame Detector 2 Fire Alarm (>= 30%) Condition & Latch",
        "text": "XIO(R00355_2)GEQ(R00353,R00349)[OTE(R00355_3),OTL(R00355_5)];"
    })
    rungs_alm2.append({
        "comment": "Reset 7404-DF-002 Fire Alarm Latch on System Reset",
        "text": "XIC(M00002_System_Reset)OTU(R00355_5);"
    })
    # Open path DG-011R
    rungs_alm2.append({
        "comment": "7404-DG-011R Open Path High Gas Alarm (>= 3.00 LELm) Condition & Latch",
        "text": "XIO(R00375_2)GEQ(R00373,R00369)[OTE(R00375_3),OTL(R00375_5)];"
    })
    rungs_alm2.append({
        "comment": "Reset 7404-DG-011R High Gas Alarm Latch on System Reset",
        "text": "XIC(M00002_System_Reset)OTU(R00375_5);"
    })
    rungs_alm2.append({
        "comment": "7404-DG-011R Open Path Low Gas Alarm (>= 1.00 LELm) Condition & Latch",
        "text": "XIO(R00375_2)GEQ(R00373,R00371)[OTE(R00375_4),OTL(R00375_6)];"
    })
    rungs_alm2.append({
        "comment": "Reset 7404-DG-011R Low Gas Alarm Latch on System Reset",
        "text": "XIC(M00002_System_Reset)OTU(R00375_6);"
    })
    # DG-012
    rungs_alm2.append({
        "comment": "7404-DG-012 High Gas Alarm (>= 30% LEL) Condition & Latch",
        "text": "XIO(R00395_2)GEQ(R00393,R00389)[OTE(R00395_3),OTL(R00395_5)];"
    })
    rungs_alm2.append({
        "comment": "Reset 7404-DG-012 High Gas Alarm Latch on System Reset",
        "text": "XIC(M00002_System_Reset)OTU(R00395_5);"
    })
    rungs_alm2.append({
        "comment": "7404-DG-012 Low Gas Alarm (>= 20% LEL) Condition & Latch",
        "text": "XIO(R00395_2)GEQ(R00393,R00391)[OTE(R00395_4),OTL(R00395_6)];"
    })
    rungs_alm2.append({
        "comment": "Reset 7404-DG-012 Low Gas Alarm Latch on System Reset",
        "text": "XIC(M00002_System_Reset)OTU(R00395_6);"
    })
    routines.append(("Ai_AL_2", "Alarm Evaluation for DG-009..012, DF-001..002, DG-011R", rungs_alm2))

    # =========================================================================
    # 15. Ai_AL_3 (Alarm Evaluation for PSTs & Foam Call Points)
    # =========================================================================
    rungs_alm3 = [
        {"comment": "7002-PST-001 Air Accumulator Low Pressure PAL (<= 50 Psi -> LED L16)", "text": "XIO(R00435_2)LEQ(R00433,R00431)[OTE(R00435_4),OTL(R00435_6)];"},
        {"comment": "Reset 7002-PST-001 Low Pressure Latch on System Reset", "text": "XIC(M00002_System_Reset)OTU(R00435_6);"},

        {"comment": "6401-PST-001 Fuel Gas High Pressure PAH (>= 100 Psi -> Station ESD)", "text": "XIO(R00455_2)GEQ(R00453,R00449)[OTE(R00455_3),OTL(R00455_5)];"},
        {"comment": "Reset 6401-PST-001 High Pressure Latch on System Reset", "text": "XIC(M00002_System_Reset)OTU(R00455_5);"},
        {"comment": "6401-PST-001 Fuel Gas Low Pressure PAL (<= 40 Psi -> LED L17)", "text": "XIO(R00455_2)LEQ(R00453,R00451)[OTE(R00455_4),OTL(R00455_6)];"},
        {"comment": "Reset 6401-PST-001 Low Pressure Latch on System Reset", "text": "XIC(M00002_System_Reset)OTU(R00455_6);"},

        {"comment": "7503-PST-001 Deluge Line High Pressure PAH (>= 50 Psi -> Foam Released)", "text": "XIO(R00475_2)GEQ(R00473,R00469)[OTE(R00475_3),OTL(R00475_5)];"},
        {"comment": "Reset 7503-PST-001 Deluge Released Latch on System Reset", "text": "XIC(M00002_System_Reset)OTU(R00475_5);"},

        {"comment": "7503-FR-001/002 Outside Manual Foam Release Call Points (>= 30%)", "text": "XIO(R00495_2)GEQ(R00493,R00489)[OTE(R00495_3),OTL(R00495_5)];"},
        {"comment": "Reset Outside Foam Release Call Points on System Reset", "text": "XIC(M00002_System_Reset)OTU(R00495_5);"},

        {"comment": "7503-FR-003 Inside PCR Local CP Manual Foam Release Call Point (>= 30%)", "text": "XIO(R00535_2)GEQ(R00533,R00529)[OTE(R00535_3),OTL(R00535_5)];"},
        {"comment": "Reset Inside Foam Release Call Point on System Reset", "text": "XIC(M00002_System_Reset)OTU(R00535_5);"}
    ]
    routines.append(("Ai_AL_3", "Alarm Evaluation for PST-001s & Foam Call Points FR-001..003", rungs_alm3))

    # =========================================================================
    # 16. Vote_1 (Gas & Flame Detector Voting Matrix)
    # =========================================================================
    rungs_vote = [
        {"comment": "Clear CH4 Gas Low and High Detector Voting Accumulators", "text": "MOV(0,Vote_Gas_Lo_Count)MOV(0,Vote_Gas_Hi_Count);"},
        {"comment": "Count Low Gas on DG-001..DG-004", "text": "XIC(R00115_6)ADD(Vote_Gas_Lo_Count,1,Vote_Gas_Lo_Count)XIC(R00135_6)ADD(Vote_Gas_Lo_Count,1,Vote_Gas_Lo_Count)XIC(R00155_6)ADD(Vote_Gas_Lo_Count,1,Vote_Gas_Lo_Count)XIC(R00175_6)ADD(Vote_Gas_Lo_Count,1,Vote_Gas_Lo_Count);"},
        {"comment": "Count Low Gas on DG-005..DG-008", "text": "XIC(R00195_6)ADD(Vote_Gas_Lo_Count,1,Vote_Gas_Lo_Count)XIC(R00215_6)ADD(Vote_Gas_Lo_Count,1,Vote_Gas_Lo_Count)XIC(R00235_6)ADD(Vote_Gas_Lo_Count,1,Vote_Gas_Lo_Count)XIC(R00255_6)ADD(Vote_Gas_Lo_Count,1,Vote_Gas_Lo_Count);"},
        {"comment": "Count Low Gas on DG-009..DG-012 and Open Path DG-011R", "text": "XIC(R00275_6)ADD(Vote_Gas_Lo_Count,1,Vote_Gas_Lo_Count)XIC(R00295_6)ADD(Vote_Gas_Lo_Count,1,Vote_Gas_Lo_Count)XIC(R00315_6)ADD(Vote_Gas_Lo_Count,1,Vote_Gas_Lo_Count)XIC(R00395_6)ADD(Vote_Gas_Lo_Count,1,Vote_Gas_Lo_Count)XIC(R00375_6)ADD(Vote_Gas_Lo_Count,1,Vote_Gas_Lo_Count);"},
        {"comment": "Count High Gas on DG-001..DG-004", "text": "XIC(R00115_5)ADD(Vote_Gas_Hi_Count,1,Vote_Gas_Hi_Count)XIC(R00135_5)ADD(Vote_Gas_Hi_Count,1,Vote_Gas_Hi_Count)XIC(R00155_5)ADD(Vote_Gas_Hi_Count,1,Vote_Gas_Hi_Count)XIC(R00175_5)ADD(Vote_Gas_Hi_Count,1,Vote_Gas_Hi_Count);"},
        {"comment": "Count High Gas on DG-005..DG-008", "text": "XIC(R00195_5)ADD(Vote_Gas_Hi_Count,1,Vote_Gas_Hi_Count)XIC(R00215_5)ADD(Vote_Gas_Hi_Count,1,Vote_Gas_Hi_Count)XIC(R00235_5)ADD(Vote_Gas_Hi_Count,1,Vote_Gas_Hi_Count)XIC(R00255_5)ADD(Vote_Gas_Hi_Count,1,Vote_Gas_Hi_Count);"},
        {"comment": "Count High Gas on DG-009..DG-012 and Open Path DG-011R", "text": "XIC(R00275_5)ADD(Vote_Gas_Hi_Count,1,Vote_Gas_Hi_Count)XIC(R00295_5)ADD(Vote_Gas_Hi_Count,1,Vote_Gas_Hi_Count)XIC(R00315_5)ADD(Vote_Gas_Hi_Count,1,Vote_Gas_Hi_Count)XIC(R00395_5)ADD(Vote_Gas_Hi_Count,1,Vote_Gas_Hi_Count)XIC(R00375_5)ADD(Vote_Gas_Hi_Count,1,Vote_Gas_Hi_Count);"},
        {"comment": "1ooN Low Gas Voting Output (R01500_0: >= 1 Detector at 20% LEL)", "text": "GEQ(Vote_Gas_Lo_Count,1)OTE(R01500_0);"},
        {"comment": "2ooN Low Gas Voting Output (R01500_1: >= 2 Detectors at 20% LEL)", "text": "GEQ(Vote_Gas_Lo_Count,2)OTE(R01500_1);"},
        {"comment": "1ooN High Gas Voting Output (R01500_2: >= 1 Detector at 30% LEL)", "text": "GEQ(Vote_Gas_Hi_Count,1)OTE(R01500_2);"},
        {"comment": "2ooN High Gas Voting Output (R01500_3: >= 2 Detectors at 30% LEL or Open Path High)", "text": "[GEQ(Vote_Gas_Hi_Count,2),XIC(R00375_5)]OTE(R01500_3);"},
        {"comment": "Count Active Flame Detectors 7404-DF-001, 7404-DF-002, 7404-DF-003", "text": "MOV(0,Vote_Flame_Count)XIC(R00335_5)ADD(Vote_Flame_Count,1,Vote_Flame_Count)XIC(R00355_5)ADD(Vote_Flame_Count,1,Vote_Flame_Count)XIC(DF_7404_003_Latch)ADD(Vote_Flame_Count,1,Vote_Flame_Count);"},
        {"comment": "1oo3 Flame Alarm Voting (R01501_0: >= 1 Flame Detector Active)", "text": "GEQ(Vote_Flame_Count,1)OTE(R01501_0);"},
        {"comment": "2oo3 Confirmed Flame Voting (R01501_1: >= 2 Flame Detectors Active)", "text": "GEQ(Vote_Flame_Count,2)OTE(R01501_1);"}
    ]
    routines.append(("Vote_1", "Gas & Flame Detector Voting Matrix (1ooN, 2ooN, 1oo3, 2oo3)", rungs_vote))

    # =========================================================================
    # 17. Logic (Deluge Firewater / Foam Pump A & Standby Pump B Sequencing)
    # =========================================================================
    rungs_logic = [
        {"comment": "Deluge / Foam Release Demand: Triggered by Flame Alarm or Foam MACs (FR-001..003) unless inhibited by S2/S3 or stopped", "text": "[XIC(R01501_0),XIC(R00495_5),XIC(R00535_5)]XIO(R00708_0)XIO(R00709_0)XIO(R00701_0)OTE(Foam_Release_Demand);"},
        {"comment": "Duty Deluge Pump A Run Command (PUMP_A / R01512_0) Start on Demand", "text": "XIC(Foam_Release_Demand)XIO(R00704_1)OTL(R01512_0);"},
        {"comment": "Stop Duty Deluge Pump A on Foam Stop Button (E8 / FS-001) or System Reset", "text": "[XIC(R00701_0),XIC(M00002_System_Reset)]OTU(R01512_0);"},
        {"comment": "Deluge Header Pressure Proving Timer (10.0s for 7503-PST-001 to reach 50 Psi)", "text": "XIC(Foam_Release_Demand)XIO(R00475_3)TON(TMR_PumpA_FailToRun,?,?);"},
        {"comment": "Standby Diesel Pump B Demand: Auto-backup if Pump A fails to reach 50 Psi in 10s or Pump A wire fault", "text": "XIC(Foam_Release_Demand)[XIC(TMR_PumpA_FailToRun.DN),XIC(R00704_1)]XIO(R00706_0)XIO(R00703_0)OTE(Pump_B_Demand);"},
        {"comment": "Standby Pump B Start Crank Pulse Output (PUMP_B_START / R01512_5)", "text": "XIC(Pump_B_Demand)XIO(R00475_3)OTE(R01512_5);"},
        {"comment": "Standby Pump B Stop Pulse Output (PUMP_B_STOP / R01512_4) on Foam Stop Button", "text": "XIC(R00701_0)OTE(R01512_4);"}
    ]
    routines.append(("Logic", "Deluge Firewater/Foam Pump A & Standby Pump B Sequencing", rungs_logic))

    # =========================================================================
    # 18. CE_LOG (Cause & Effect Matrix Orchestrator)
    # =========================================================================
    rungs_celog = [
        {"comment": "Execute Panel Indicators Subroutine (Indicat)", "text": "JSR(Indicat,0);"},
        {"comment": "Execute Master Shutdown Subroutine (Shutdow)", "text": "JSR(Shutdow,0);"},
        {"comment": "Execute Foam/Deluge Protection Status Subroutine (Protect)", "text": "JSR(Protect,0);"},
        {"comment": "Execute Audible & Visual Alarm Mode Subroutine (Loc_Al)", "text": "JSR(Loc_Al,0);"},
        {"comment": "Execute System Fault Aggregator Subroutine (FLT_1)", "text": "JSR(FLT_1,0);"}
    ]
    routines.append(("CE_LOG", "Cause & Effect Matrix Orchestrator (01-MAN-03-07)", rungs_celog))

    # =========================================================================
    # 19. Indicat (Panel LEDs & Individual Pump Trip Relays)
    # =========================================================================
    rungs_ind = [
        {"comment": "L15 (Local:8:O.Data.12): ESDV Fuel Gas Line Open Green LED", "text": "XIC(R00700_0)OTE(R01513_0);"},
        {"comment": "L14 (Local:8:O.Data.11): ESDV Fuel Gas Line Closed Red LED", "text": "XIC(R00700_1)OTE(R01513_1);"},
        {"comment": "L16 (Local:8:O.Data.13): ESDV Low Air Accumulator Supply Amber LED", "text": "XIC(R00435_6)OTE(R01513_2);"},
        {"comment": "L17 (Local:8:O.Data.14): Low Fuel Gas Line Pressure Amber LED", "text": "XIC(R00455_6)OTE(LED_Low_Fuel_Gas_L17);"},
        {"comment": "CR1 (Local:8:O.Data.15): Trip Power Oil Pump P-2300 (E1, ESD Trip, or PIT-003 PAHH 2800 Psi)", "text": "[XIC(Latch_ESTOP_P2300),XIO(R01510_0),XIC(PIT_003_PAHH_Latch)]XIO(R00709_0)OTE(CR1_P2300_Stop);"},
        {"comment": "CR2 (Local:8:O.Data.16): Trip Power Oil Pump P-2400 (E2, ESD Trip, or PIT-003 PAHH 2800 Psi)", "text": "[XIC(Latch_ESTOP_P2400),XIO(R01510_0),XIC(PIT_003_PAHH_Latch)]XIO(R00709_0)OTE(CR2_P2400_Stop);"},
        {"comment": "CR3 (Local:8:O.Data.17): Trip Power Oil Pump P-2500 (E3, ESD Trip, or PIT-003 PAHH 2800 Psi)", "text": "[XIC(Latch_ESTOP_P2500),XIO(R01510_0),XIC(PIT_003_PAHH_Latch)]XIO(R00709_0)OTE(CR3_P2500_Stop);"},
        {"comment": "CR4 (Local:8:O.Data.18): Trip Power Oil Pump P-2600 (E4, ESD Trip, or PIT-003 PAHH 2800 Psi)", "text": "[XIC(Latch_ESTOP_P2600),XIO(R01510_0),XIC(PIT_003_PAHH_Latch)]XIO(R00709_0)OTE(CR4_P2600_Stop);"},
        {"comment": "CR5 (Local:8:O.Data.19): Trip Water Injection Pump P-3800 (E5, ESD Trip, or PIT-002 PAHH 900 Psi)", "text": "[XIC(Latch_ESTOP_P3800),XIO(R01510_0),XIC(PIT_002_PAHH_Latch)]XIO(R00709_0)OTE(CR5_P3800_Stop);"},
        {"comment": "CR6 (Local:8:O.Data.20): Trip Water Injection Pump P-3900 (E6, ESD Trip, or PIT-002 PAHH 900 Psi)", "text": "[XIC(Latch_ESTOP_P3900),XIO(R01510_0),XIC(PIT_002_PAHH_Latch)]XIO(R00709_0)OTE(CR6_P3900_Stop);"}
    ]
    routines.append(("Indicat", "FGCP-7404-001 Panel LEDs & Individual Pump Relay Indicators", rungs_ind))

    # =========================================================================
    # 20. Shutdow (Master ESD Matrix per 01-MAN-03-07)
    # =========================================================================
    rungs_shut = [
        {"comment": "Master Station ESD Trip Condition: High Gas 30%, Flame >=30%, Foam MAC, Deluge >=50 Psi, Fuel Gas >=100 Psi", "text": "[XIC(R01500_2),XIC(R01500_3),XIC(R01501_0),XIC(R00495_5),XIC(R00535_5),XIC(R00475_5),XIC(R00455_5)]XIO(R00709_0)OTE(ESD_Trip_Condition);"},
        {"comment": "PumpShutdown (Local:8:O.Data.0): Fail-Safe Energize-to-Run (1=Healthy, 0=Station ESD Trip)", "text": "XIO(ESD_Trip_Condition)OTE(R01510_0);"},
        {"comment": "6401-EY-001/002 ESDV Solenoid (Local:8:O.Data.1): Fail-Safe Energize-to-Open (Tripped by ESD or E9)", "text": "XIO(ESD_Trip_Condition)[XIO(R00707_1),XIC(R00709_0)]OTE(R01511_0);"},
        {"comment": "P-2100/2200 Oil Booster Pump Shutdown Relay (Local:8:O.Data.8): Tripped by ESD or PIT-003 PAHH 2800 Psi", "text": "XIO(ESD_Trip_Condition)[XIO(PIT_003_PAHH_Latch),XIC(R00709_0)]OTE(R01511_1);"},
        {"comment": "P-3600/3700 Water Booster Pump Shutdown Relay (Local:8:O.Data.9): Tripped by ESD or PIT-002 PAHH 900 Psi", "text": "XIO(ESD_Trip_Condition)[XIO(PIT_002_PAHH_Latch),XIC(R00709_0)]OTE(R01511_2);"},
        {"comment": "SD-GE (Local:8:O.Data.21): Shut Down All Gas Generators (GD-001..003 >= 30%, Smoke >= 30%, or Station ESD)", "text": "[XIC(GD_Any_Hi_Latch),XIC(SD_001_002_Latch),XIC(ESD_Trip_Condition)]XIO(R00709_0)OTE(SD_GE);"}
    ]
    routines.append(("Shutdow", "Master Emergency Shutdown Matrix (Fail-Safe Logic)", rungs_shut))

    # =========================================================================
    # 21. Protect (Firewater / Foam Protection Status)
    # =========================================================================
    rungs_prot = [
        {"comment": "Deluge Released Confirmation Status (7503-PST-001 >= 50 Psi)", "text": "XIC(R00475_5)OTE(Deluge_Released_Status);"},
        {"comment": "Foam System Inhibited Status (Keyswitch S2 or S3 active)", "text": "[XIC(R00708_0),XIC(R00709_0)]OTE(Foam_System_Inhibited);"}
    ]
    routines.append(("Protect", "Firewater & Foam Deluge Protection System Status", rungs_prot))

    # =========================================================================
    # 22. Loc_Al (Audible & Visual Alarm Pattern Selection)
    # =========================================================================
    rungs_local = [
        {"comment": "Pump House Bell Discontinuous Mode (1ooN Low Gas 20% LEL or Open Path 1.00 LELm)", "text": "XIC(R01500_0)XIO(R01500_2)XIO(R01501_0)XIO(R00495_5)XIO(R00535_5)XIO(R00475_5)OTE(Bell_Mode_Discontinuous);"},
        {"comment": "Pump House Bell Continuous Mode (High Gas 30%, Flame >=30%, Foam MAC, Deluge Released)", "text": "[XIC(R01500_2),XIC(R01501_0),XIC(R00495_5),XIC(R00535_5),XIC(R00475_5)]OTE(Bell_Mode_Continuous);"},
        {"comment": "Aggregate Any Unaccepted Plant Alarm Condition", "text": "[XIC(R01500_0),XIC(R01500_2),XIC(R01501_0),XIC(R00495_5),XIC(R00535_5),XIC(R00475_5),XIC(R00435_6),XIC(R00455_5),XIC(R00455_6),XIC(R00707_1),XIC(GD_Any_Lo_Latch),XIC(GD_Any_Hi_Latch),XIC(H2S_Lo_Latch),XIC(H2S_Hi_Latch),XIC(SD_001_002_Latch),XIC(PIT_001_PAL),XIC(PIT_001_PAH),XIC(PIT_002_PAL),XIC(PIT_002_PAH),XIC(PIT_002_PAHH_Latch),XIC(PIT_003_PAL),XIC(PIT_003_PAH),XIC(PIT_003_PAHH_Latch),XIC(LIT_100_LAL),XIC(LIT_100_LAH),XIC(LIT_200_LAL),XIC(LIT_200_LAH),XIC(LIT_300_LAL),XIC(LIT_300_LAH),XIC(LIT_400_LAL),XIC(LIT_400_LAH),XIC(FT_6401_001_FAL),XIC(FT_6401_001_FAH)]OTE(Any_Unaccepted_Alarm);"},
        {"comment": "Silence / Acknowledge Alarm Latch via E12 Mute Pushbutton or HMI M00001", "text": "XIC(M00001_System_Accept)OTL(Alarm_Silence_Latch);"},
        {"comment": "Reset Alarm Silence Latch when all alarms clear or System Reset", "text": "[XIO(Any_Unaccepted_Alarm),XIC(M00002_System_Reset)]OTU(Alarm_Silence_Latch);"},
        {"comment": "Z1 (Local:8:O.Data.22): Production Control Room Audible Alarm Horn", "text": "XIC(Any_Unaccepted_Alarm)XIO(Alarm_Silence_Latch)OTE(R01513_3);"},
        {"comment": "PA-001 (Local:8:O.Data.23): Process Production Building Audible Alarm", "text": "[XIC(PIT_001_PAL),XIC(PIT_001_PAH),XIC(PIT_002_PAL),XIC(PIT_002_PAH),XIC(PIT_002_PAHH_Latch),XIC(PIT_003_PAL),XIC(PIT_003_PAH),XIC(PIT_003_PAHH_Latch),XIC(LIT_100_LAL),XIC(LIT_100_LAH),XIC(LIT_200_LAL),XIC(LIT_200_LAH),XIC(LIT_300_LAL),XIC(LIT_300_LAH),XIC(LIT_400_LAL),XIC(LIT_400_LAH),XIC(FT_6401_001_FAL),XIC(FT_6401_001_FAH),XIC(R00435_6),XIC(R00455_5),XIC(R00455_6)]XIO(Alarm_Silence_Latch)XIO(R00709_0)OTE(PA_001);"},
        {"comment": "H2SA-001/002 (Local:8:O.Data.30): Toxic H2S Gas Horn & Strobe Beacon (Pulsing 1Hz on Low, Continuous on High)", "text": "[XIC(H2S_Hi_Latch),[XIC(H2S_Lo_Latch),XIC(R01598_0)]]XIO(Alarm_Silence_Latch)XIO(R00709_0)OTE(H2SA_001_002);"},
        {"comment": "SDA-001 (Local:8:O.Data.31): Smoke Detection Horn & Strobe Beacon", "text": "XIC(SD_001_002_Latch)XIO(Alarm_Silence_Latch)XIO(R00709_0)OTE(SDA_001);"}
    ]
    routines.append(("Loc_Al", "Audible & Visual Alarm Pattern Selection (Z1, PA-001, H2SA, SDA)", rungs_local))

    # =========================================================================
    # 23. FLT_1 (System & Hardware Fault Aggregator)
    # =========================================================================
    rungs_flt = [
        {"comment": "Aggregate All Transmitter Wire Breaks, Optical Beam Block, ESDV Discrepancy & Line Faults", "text": "[XIC(R00115_2),XIC(R00135_2),XIC(R00155_2),XIC(R00175_2),XIC(R00195_2),XIC(R00215_2),XIC(R00235_2),XIC(R00255_2),XIC(R00275_2),XIC(R00295_2),XIC(R00315_2),XIC(R00335_2),XIC(R00355_2),XIC(R00375_2),XIC(R00395_2),XIC(R00435_2),XIC(R00455_2),XIC(R00475_2),XIC(R00495_2),XIC(R00535_2),XIC(GD_001_Fault),XIC(GD_002_Fault),XIC(GD_003_Fault),XIC(PIT_001_Fault),XIC(PIT_002_Fault),XIC(PIT_003_Fault),XIC(DF_7404_003_Fault),XIC(SD_001_002_Fault),XIC(R00700_6),XIC(R00704_1),XIC(R00705_1)]OTE(Any_Channel_Fault);"},
        {"comment": "PLC_Fault (Local:8:O.Data.10): Fail-Safe System Healthy Output (1=No Fault, 0=Fault Present)", "text": "XIO(Any_Channel_Fault)OTE(R01513_4);"}
    ]
    routines.append(("FLT_1", "System, I/O Module & Transmitter Fault Aggregation (PLC_Fault)", rungs_flt))

    # =========================================================================
    # 24. Sound (7404-SA-001/002 Pump House Alarm Bell Driver)
    # =========================================================================
    rungs_snd = [
        {"comment": "7404-SA-001/002 (Local:8:O.Data.2): Drive Pump House Bell Continuous or Discontinuous (0.8s Flasher R01598_0)", "text": "[XIC(Bell_Mode_Continuous),[XIC(Bell_Mode_Discontinuous),XIC(R01598_0)]]XIO(Alarm_Silence_Latch)XIO(R00708_0)XIO(R00709_0)OTE(R01511_3);"}
    ]
    routines.append(("Sound", "7404-SA-001/002 Pump House Alarm Bell Driver", rungs_snd))

    # =========================================================================
    # 25. Output (Mapping to Slot 8 1756-OB32 Digital Outputs)
    # =========================================================================
    rungs_out = [
        {"comment": "Point 0: PumpShutdown (Local:8:O.Data.0) Master ESD Trip Relay (Fail-Safe 1=Run)", "text": "XIC(R01510_0)[OTE(PumpShutdown),OTE(Local:8:O.Data.0)];"},
        {"comment": "Point 1: 6401-EY-001/002 (Local:8:O.Data.1) Fuel Gas ESDV Solenoid (Fail-Safe 1=Open)", "text": "XIC(R01511_0)[OTE(EY_6401_001_002),OTE(Local:8:O.Data.1)];"},
        {"comment": "Point 2: 7404-SA-001/002 (Local:8:O.Data.2) Local Alarm Bell Pump House", "text": "XIC(R01511_3)[OTE(SA_7404_001_002),OTE(Local:8:O.Data.2)];"},
        {"comment": "Point 3: Pump_A_PulsOut (Local:8:O.Data.3) Deluge Pump A Pulse Line Check", "text": "XIC(R01513_12)[OTE(Pump_A_PulsOut),OTE(Local:8:O.Data.3)];"},
        {"comment": "Point 4: PUMP_A (Local:8:O.Data.4) Deluge Duty Firewater Pump A Run Output", "text": "XIC(R01512_0)[OTE(PUMP_A),OTE(Local:8:O.Data.4)];"},
        {"comment": "Point 5: Pump_B_Start_PulsOut (Local:8:O.Data.5) Deluge Pump B Pulse Line Check", "text": "XIC(R01513_13)[OTE(Pump_B_Start_PulsOut),OTE(Local:8:O.Data.5)];"},
        {"comment": "Point 6: PUMP_B_START (Local:8:O.Data.6) Deluge Standby Diesel Pump B Start Pulse", "text": "XIC(R01512_5)[OTE(PUMP_B_START),OTE(Local:8:O.Data.6)];"},
        {"comment": "Point 7: PUMP_B_STOP (Local:8:O.Data.7) Deluge Standby Diesel Pump B Stop Pulse", "text": "XIC(R01512_4)[OTE(PUMP_B_STOP),OTE(Local:8:O.Data.7)];"},
        {"comment": "Point 8: P2100_P2200 (Local:8:O.Data.8) Oil Booster Pump Shutdown Relay (Fail-Safe 1=Run)", "text": "XIC(R01511_1)[OTE(P2100_P2200),OTE(Local:8:O.Data.8)];"},
        {"comment": "Point 9: P3600_P3700 (Local:8:O.Data.9) Water Booster Pump Shutdown Relay (Fail-Safe 1=Run)", "text": "XIC(R01511_2)[OTE(P3600_P3700),OTE(Local:8:O.Data.9)];"},
        {"comment": "Point 10: PLC_Fault (Local:8:O.Data.10) PLC / System Fault Contact (Fail-Safe 1=Healthy)", "text": "XIC(R01513_4)[OTE(PLC_Fault),OTE(Local:8:O.Data.10)];"},
        {"comment": "Point 11: Tag_DO_13 / L14 (Local:8:O.Data.11) ESDV Fuel Gas Closed Red LED Indicator", "text": "XIC(R01513_1)[OTE(Tag_DO_13),OTE(Local:8:O.Data.11)];"},
        {"comment": "Point 12: Tag_DO_12 / L15 (Local:8:O.Data.12) ESDV Fuel Gas Open Green LED Indicator", "text": "XIC(R01513_0)[OTE(Tag_DO_12),OTE(Local:8:O.Data.12)];"},
        {"comment": "Point 13: Tag_DO_14 / L16 (Local:8:O.Data.13) ESDV Low Air Accumulator Supply Amber LED", "text": "XIC(R01513_2)[OTE(Tag_DO_14),OTE(Local:8:O.Data.13)];"},
        {"comment": "Point 14: LED_Low_Fuel_Gas_L17 / L17 (Local:8:O.Data.14) Low Fuel Gas Line Amber LED", "text": "XIC(LED_Low_Fuel_Gas_L17)OTE(Local:8:O.Data.14);"},
        {"comment": "Point 15: CR1 (Local:8:O.Data.15) Stop Power Oil Pump P-2300 Relay & L8 LED", "text": "XIC(CR1_P2300_Stop)OTE(Local:8:O.Data.15);"},
        {"comment": "Point 16: CR2 (Local:8:O.Data.16) Stop Power Oil Pump P-2400 Relay & L9 LED", "text": "XIC(CR2_P2400_Stop)OTE(Local:8:O.Data.16);"},
        {"comment": "Point 17: CR3 (Local:8:O.Data.17) Stop Power Oil Pump P-2500 Relay & L10 LED", "text": "XIC(CR3_P2500_Stop)OTE(Local:8:O.Data.17);"},
        {"comment": "Point 18: CR4 (Local:8:O.Data.18) Stop Power Oil Pump P-2600 Relay & L11 LED", "text": "XIC(CR4_P2600_Stop)OTE(Local:8:O.Data.18);"},
        {"comment": "Point 19: CR5 (Local:8:O.Data.19) Stop Water Injection Pump P-3800 Relay & L12 LED", "text": "XIC(CR5_P3800_Stop)OTE(Local:8:O.Data.19);"},
        {"comment": "Point 20: CR6 (Local:8:O.Data.20) Stop Water Injection Pump P-3900 Relay & L13 LED", "text": "XIC(CR6_P3900_Stop)OTE(Local:8:O.Data.20);"},
        {"comment": "Point 21: SD_GE (Local:8:O.Data.21) Shut Down All Gas Generators Output", "text": "XIC(SD_GE)OTE(Local:8:O.Data.21);"},
        {"comment": "Point 22: Tag_DO_15 / Z1 (Local:8:O.Data.22) Production Control Room Alarm Horn", "text": "XIC(R01513_3)[OTE(Tag_DO_15),OTE(Local:8:O.Data.22)];"},
        {"comment": "Point 23: PA_001 (Local:8:O.Data.23) Process Production Building Alarm Horn", "text": "XIC(PA_001)OTE(Local:8:O.Data.23);"},
        {"comment": "Point 30: H2SA_001_002 (Local:8:O.Data.30) H2S Alarm Horn & Strobe Beacon", "text": "XIC(H2SA_001_002)OTE(Local:8:O.Data.30);"},
        {"comment": "Point 31: SDA_001 (Local:8:O.Data.31) Smoke Detection Alarm Horn & Strobe Beacon", "text": "XIC(SDA_001)OTE(Local:8:O.Data.31);"}
    ]
    routines.append(("Output", "Slot 8 1756-OB32 Discrete Hardware Output Driver Mapping", rungs_out))

    return routines


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================
def main():
    import generate_ladder_backend as B

    print("=" * 72)
    print("ALLEN-BRADLEY CONTROLLOGIX 5580 RELAY LADDER LOGIC (RLL) GENERATOR")
    print("Converting GE VersaMax P20890_Angola to Studio 5000 RLL (.L5X & HTML)")
    print("=" * 72)

    tags = G.build_controller_tags()
    print(f"[OK] Controller Tags defined: {len(tags)}")

    routines = build_rll_routines()
    total_rungs = sum(len(r[2]) for r in routines)
    print(f"[OK] RLL Routines built: {len(routines)} routines, {total_rungs} total rungs")

    # Generate L5X Ladder Project (Controller Level)
    print("\n--- Generating Studio 5000 Controller L5X Project File (Type=RLL) ---")
    B.write_l5x_rll(tags, routines)

    # Generate L5X Ladder Program (Program Level for direct Import Program)
    print("\n--- Generating Studio 5000 Program L5X Import File (TargetType=Program) ---")
    B.write_l5x_program_rll(tags, routines)

    # Generate Interactive HTML Ladder Viewer
    print("\n--- Generating Interactive HTML Ladder Diagram Viewer ---")
    B.write_ladder_html(tags, routines)

    print("\n" + "=" * 72)
    print("[SUCCESS] All Allen-Bradley Ladder deliverables generated successfully!")
    print("=" * 72)


if __name__ == "__main__":
    main()

