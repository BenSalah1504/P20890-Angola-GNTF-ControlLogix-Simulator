# -*- coding: utf-8 -*-
"""
Ladder Diagram Backend & Exporter for Allen-Bradley ControlLogix 5580.
Generates:
1. P20890_Angola_AB_Ladder.L5X (Studio 5000 v32+ RLL Project File)
2. P20890_Angola_AB_Ladder.html (Interactive High-Fidelity SVG/HTML Ladder Viewer)
"""
import os
import sys
import html
import json
import xml.sax.saxutils as saxutils
import xml.etree.ElementTree as ET

BASE_DIR = r"c:\Users\Wajdi TAKTAK\Desktop\DOC\ws_g\pme_ladder_export"
DESKTOP_DIR = r"C:\Users\Wajdi TAKTAK\Desktop\P20890_Angola"


# =============================================================================
# 1. LOGIX RLL PARSER
# =============================================================================
def parse_rung_elements(text):
    """
    Parse a Logix RLL rung text into a structured tree of instructions and branches.
    Returns a list of ('INST', name, args_str, args_list) and ('BRANCH', [leg0, leg1, ...]).
    """
    text = text.strip()
    if text.endswith(';'):
        text = text[:-1].strip()

    n = len(text)

    def parse_instruction(start_idx):
        paren_idx = text.find('(', start_idx)
        if paren_idx == -1:
            return None, start_idx + 1
        name = text[start_idx:paren_idx].strip()
        depth = 1
        k = paren_idx + 1
        while k < n and depth > 0:
            if text[k] == '(':
                depth += 1
            elif text[k] == ')':
                depth -= 1
            k += 1
        args_str = text[paren_idx + 1 : k - 1].strip()
        # Parse top-level comma-separated arguments
        args_list = []
        cur = []
        d = 0
        for ch in args_str:
            if ch in '([{':
                d += 1
                cur.append(ch)
            elif ch in ')]}':
                d -= 1
                cur.append(ch)
            elif ch == ',' and d == 0:
                args_list.append(''.join(cur).strip())
                cur = []
            else:
                cur.append(ch)
        if cur:
            args_list.append(''.join(cur).strip())
        return ('INST', name, args_str, args_list), k

    def parse_branch(start_idx):
        idx = start_idx + 1  # skip '['
        legs = [[]]
        while idx < n and text[idx] != ']':
            if text[idx] == ',':
                legs.append([])
                idx += 1
            elif text[idx] == '[':
                sub_legs, next_idx = parse_branch(idx)
                legs[-1].append(('BRANCH', sub_legs))
                idx = next_idx
            elif text[idx].isspace():
                idx += 1
            else:
                inst, next_idx = parse_instruction(idx)
                if inst:
                    legs[-1].append(inst)
                    idx = next_idx
                else:
                    idx += 1
        return legs, idx + 1  # skip ']'

    items = []
    i = 0
    while i < n:
        if text[i] == '[':
            legs, i = parse_branch(i)
            items.append(('BRANCH', legs))
        elif text[i].isspace() or text[i] == ';':
            i += 1
        else:
            inst, i = parse_instruction(i)
            if inst:
                items.append(inst)
            else:
                i += 1
    return items


# =============================================================================
# 2. HTML ELEMENT RENDERER
# =============================================================================
def render_element_to_html(item, tag_map):
    """Render a single rung element (Instruction or Branch) into clean HTML."""
    kind = item[0]
    if kind == 'BRANCH':
        legs = item[1]
        legs_html = []
        for leg in legs:
            leg_items_html = ''.join(render_element_to_html(sub, tag_map) for sub in leg)
            legs_html.append(f'<div class="branch-leg"><div class="branch-wire"></div><div class="leg-content">{leg_items_html}</div><div class="branch-wire"></div></div>')
        return f'<div class="ladder-branch"><div class="branch-bar left-bar"></div><div class="branch-stack">{"".join(legs_html)}</div><div class="branch-bar right-bar"></div></div>'

    # Instruction
    _, name, args_str, args_list = item
    primary_tag = args_list[0] if args_list else ""
    tag_info = tag_map.get(primary_tag, {})
    tag_desc = tag_info.get("desc", "")
    tag_type = tag_info.get("type", "")
    alias = tag_info.get("alias", "")

    # Clean display description
    desc_disp = html.escape(tag_desc[:30] + ("..." if len(tag_desc) > 30 else ""))
    tag_disp = html.escape(primary_tag)

    if name in ('XIC', 'XIO'):
        is_xio = (name == 'XIO')
        inst_label = "Normally Closed" if is_xio else "Normally Open"
        slash = '<div class="contact-slash">/</div>' if is_xio else '<div class="contact-gap"></div>'
        cls_name = 'xio' if is_xio else 'xic'
        return f'''<div class="ladder-elem contact-box {cls_name}" onclick="inspectTag('{tag_disp}')" title="{inst_label}: {tag_disp} &#10;{html.escape(tag_desc)}">
            <div class="elem-lead"></div>
            <div class="elem-main">
                <div class="elem-tagname">{tag_disp}</div>
                <div class="contact-symbol">
                    <span class="plate-left">[</span>
                    {slash}
                    <span class="plate-right">]</span>
                </div>
                <div class="elem-desc">{desc_disp or '&nbsp;'}</div>
            </div>
            <div class="elem-trail"></div>
        </div>'''

    elif name in ('OTE', 'OTL', 'OTU'):
        sym_char = "( )" if name == 'OTE' else ("( L )" if name == 'OTL' else "( U )")
        badge_cls = "ote" if name == 'OTE' else ("otl" if name == 'OTL' else "otu")
        coil_type = "Energize Coil" if name == 'OTE' else ("Latch Coil" if name == 'OTL' else "Unlatch Coil")
        return f'''<div class="ladder-elem coil-box {badge_cls}" onclick="inspectTag('{tag_disp}')" title="{coil_type}: {tag_disp} &#10;{html.escape(tag_desc)}">
            <div class="elem-lead"></div>
            <div class="elem-main">
                <div class="elem-tagname">{tag_disp}</div>
                <div class="coil-symbol">{sym_char}</div>
                <div class="elem-desc">{desc_disp or '&nbsp;'}</div>
            </div>
            <div class="elem-trail"></div>
        </div>'''

    elif name == 'TON':
        pre_val = args_list[1] if len(args_list) > 1 and args_list[1] != '?' else tag_info.get("pre", "Preset")
        acc_val = args_list[2] if len(args_list) > 2 and args_list[2] != '?' else "0"
        return f'''<div class="ladder-elem block-box ton-block" onclick="inspectTag('{tag_disp}')" title="Timer On Delay: {tag_disp}">
            <div class="elem-lead"></div>
            <div class="block-card">
                <div class="block-header">TON &bull; Timer On Delay</div>
                <div class="block-body">
                    <div class="block-row"><span class="lbl">Timer:</span><span class="val font-mono">{tag_disp}</span></div>
                    <div class="block-row"><span class="lbl">Time Base:</span><span class="val">0.001 s</span></div>
                    <div class="block-row"><span class="lbl">Preset:</span><span class="val font-mono">{pre_val}</span></div>
                    <div class="block-row"><span class="lbl">Accum:</span><span class="val font-mono">{acc_val}</span></div>
                </div>
                <div class="block-footer"><span>(EN)</span><span>(DN)</span></div>
            </div>
            <div class="elem-trail"></div>
        </div>'''

    elif name == 'CPT':
        dest = args_list[0] if len(args_list) > 0 else ""
        expr = args_list[1] if len(args_list) > 1 else ""
        dest_disp = html.escape(dest)
        expr_disp = html.escape(expr)
        return f'''<div class="ladder-elem block-box cpt-block" onclick="inspectTag('{dest_disp}')" title="Compute Expression: {dest_disp} = {expr_disp}">
            <div class="elem-lead"></div>
            <div class="block-card">
                <div class="block-header">CPT &bull; Compute</div>
                <div class="block-body">
                    <div class="block-row"><span class="lbl">Dest:</span><span class="val font-mono">{dest_disp}</span></div>
                    <div class="block-row"><span class="lbl">Expr:</span><span class="val font-mono expr-txt">{expr_disp}</span></div>
                </div>
            </div>
            <div class="elem-trail"></div>
        </div>'''

    elif name == 'MOV':
        src = args_list[0] if len(args_list) > 0 else ""
        dest = args_list[1] if len(args_list) > 1 else ""
        src_disp = html.escape(src)
        dest_disp = html.escape(dest)
        return f'''<div class="ladder-elem block-box mov-block" onclick="inspectTag('{dest_disp}')" title="Move Data: {src_disp} &rarr; {dest_disp}">
            <div class="elem-lead"></div>
            <div class="block-card">
                <div class="block-header">MOV &bull; Move</div>
                <div class="block-body">
                    <div class="block-row"><span class="lbl">Source:</span><span class="val font-mono">{src_disp}</span></div>
                    <div class="block-row"><span class="lbl">Dest:</span><span class="val font-mono">{dest_disp}</span></div>
                </div>
            </div>
            <div class="elem-trail"></div>
        </div>'''

    elif name in ('GRT', 'GEQ', 'LES', 'LEQ', 'EQU', 'NEQ'):
        s_a = args_list[0] if len(args_list) > 0 else ""
        s_b = args_list[1] if len(args_list) > 1 else ""
        op_map = {'GRT': '>', 'GEQ': '&ge;', 'LES': '<', 'LEQ': '&le;', 'EQU': '==', 'NEQ': '<>'}
        op_sym = op_map.get(name, name)
        return f'''<div class="ladder-elem block-box cmp-block" title="Compare: {s_a} {op_sym} {s_b}">
            <div class="elem-lead"></div>
            <div class="block-card">
                <div class="block-header">{name} &bull; Compare ({op_sym})</div>
                <div class="block-body">
                    <div class="block-row"><span class="lbl">Source A:</span><span class="val font-mono">{html.escape(s_a)}</span></div>
                    <div class="block-row"><span class="lbl">Source B:</span><span class="val font-mono">{html.escape(s_b)}</span></div>
                </div>
            </div>
            <div class="elem-trail"></div>
        </div>'''

    elif name == 'LIM':
        low = args_list[0] if len(args_list) > 0 else ""
        test = args_list[1] if len(args_list) > 1 else ""
        high = args_list[2] if len(args_list) > 2 else ""
        return f'''<div class="ladder-elem block-box lim-block" title="Limit Test: {low} &le; {test} &le; {high}">
            <div class="elem-lead"></div>
            <div class="block-card">
                <div class="block-header">LIM &bull; Limit Test</div>
                <div class="block-body">
                    <div class="block-row"><span class="lbl">Low:</span><span class="val font-mono">{html.escape(low)}</span></div>
                    <div class="block-row"><span class="lbl">Test:</span><span class="val font-mono">{html.escape(test)}</span></div>
                    <div class="block-row"><span class="lbl">High:</span><span class="val font-mono">{html.escape(high)}</span></div>
                </div>
            </div>
            <div class="elem-trail"></div>
        </div>'''

    elif name == 'JSR':
        r_target = args_list[0] if len(args_list) > 0 else ""
        return f'''<div class="ladder-elem block-box jsr-block" onclick="selectRoutine('{html.escape(r_target)}')" title="Jump To Subroutine: {r_target}">
            <div class="elem-lead"></div>
            <div class="block-card jsr-card">
                <div class="block-header">JSR &bull; Jump To Subroutine</div>
                <div class="block-body">
                    <div class="block-row"><span class="lbl">Routine:</span><span class="val font-mono text-blue-600 font-bold">{html.escape(r_target)}</span></div>
                    <div class="block-row"><span class="lbl">Inputs:</span><span class="val">0</span></div>
                </div>
            </div>
            <div class="elem-trail"></div>
        </div>'''

    else:
        # Generic Rockwell instruction block
        joined_args = html.escape(", ".join(args_list))
        return f'''<div class="ladder-elem block-box generic-block" title="{name}({joined_args})">
            <div class="elem-lead"></div>
            <div class="block-card">
                <div class="block-header">{name}</div>
                <div class="block-body">
                    <div class="block-row"><span class="lbl">Operands:</span><span class="val font-mono">{joined_args}</span></div>
                </div>
            </div>
            <div class="elem-trail"></div>
        </div>'''


# =============================================================================
# 3. L5X RELAY LADDER LOGIC (RLL) XML EXPORTER
# =============================================================================
TIMER_PRESETS = {
    'TMR_Flash_Slow': 400,
    'TMR_Flash_Fast': 200,
    'TMR_ESDV_Transit': 15000,
    'TMR_ESDV_CmdOpen': 5000,
    'TMR_ESDV_CmdClose': 5000,
    'TMR_Pulse_Period': 60000,
    'TMR_Pulse_Width': 1000,
    'TMR_PumpA_WireFlt': 2000,
    'TMR_PumpB_WireFlt': 2000,
    'TMR_PumpA_FailToRun': 10000,
    'TMR_PumpB_StartOn': 2000,
    'TMR_PumpB_StartOff': 2000,
    'TMR_PumpB_StopPulse': 2000,
}

def format_logix_elements(elems):
    """Format parsed elements into standardized Studio 5000 RLL mnemonic string."""
    def fmt_item(item):
        if item[0] == 'BRANCH':
            legs_str = ' , '.join(' '.join(fmt_item(sub) for sub in leg) for leg in item[1])
            return f'[ {legs_str} ]'
        else:
            name = item[1]
            args_str = item[2]
            return f'{name}({args_str})'
    res = ' '.join(fmt_item(el) for el in elems)
    if not res.endswith(';'):
        res += ';'
    return res


def build_tag_xml_lines(tname, dtype, desc, alias_for):
    """Build compliant Studio 5000 Tag XML lines with <Data Format='Decorated'>."""
    esc_desc = saxutils.escape(desc)
    # In Relay Ladder Logic (RLL), Studio 5000 strictly requires TIMER and COUNTER, not FBD types
    if dtype == 'FBD_TIMER' or tname.startswith('TMR_'):
        clean_dtype = 'TIMER'
    elif dtype == 'FBD_COUNTER' or tname.startswith('CTU_') or tname.startswith('CTR_'):
        clean_dtype = 'COUNTER'
    else:
        clean_dtype = dtype

    lines = []
    if alias_for and not alias_for.startswith("MODBUS"):
        lines.append(f'      <Tag Name="{tname}" TagType="Alias" AliasFor="{alias_for}" ExternalAccess="Read/Write">')
        lines.append(f'        <Description><![CDATA[{esc_desc}]]></Description>')
        lines.append('      </Tag>')
    else:
        lines.append(f'      <Tag Name="{tname}" TagType="Base" DataType="{clean_dtype}" Constant="false" ExternalAccess="Read/Write">')
        lines.append(f'        <Description><![CDATA[{esc_desc}]]></Description>')
        lines.append('        <Data Format="Decorated">')
        if clean_dtype == 'BOOL':
            lines.append('          <DataValue DataType="BOOL" Value="0"/>')
        elif clean_dtype == 'REAL':
            lines.append('          <DataValue DataType="REAL" Value="0.0"/>')
        elif clean_dtype == 'DINT':
            lines.append('          <DataValue DataType="DINT" Value="0"/>')
        elif clean_dtype == 'INT':
            lines.append('          <DataValue DataType="INT" Value="0"/>')
        elif clean_dtype == 'TIMER':
            pre = TIMER_PRESETS.get(tname, 1000)
            lines.append('          <Structure DataType="TIMER">')
            lines.append(f'            <DataValueMember Name="PRE" DataType="DINT" Value="{pre}"/>')
            lines.append('            <DataValueMember Name="ACC" DataType="DINT" Value="0"/>')
            lines.append('            <DataValueMember Name="EN" DataType="BOOL" Value="0"/>')
            lines.append('            <DataValueMember Name="TT" DataType="BOOL" Value="0"/>')
            lines.append('            <DataValueMember Name="DN" DataType="BOOL" Value="0"/>')
            lines.append('          </Structure>')
        elif clean_dtype == 'COUNTER':
            lines.append('          <Structure DataType="COUNTER">')
            lines.append('            <DataValueMember Name="PRE" DataType="DINT" Value="3"/>')
            lines.append('            <DataValueMember Name="ACC" DataType="DINT" Value="0"/>')
            lines.append('            <DataValueMember Name="CU" DataType="BOOL" Value="0"/>')
            lines.append('            <DataValueMember Name="CD" DataType="BOOL" Value="0"/>')
            lines.append('            <DataValueMember Name="DN" DataType="BOOL" Value="0"/>')
            lines.append('            <DataValueMember Name="OV" DataType="BOOL" Value="0"/>')
            lines.append('            <DataValueMember Name="UN" DataType="BOOL" Value="0"/>')
            lines.append('          </Structure>')
        else:
            lines.append(f'          <DataValue DataType="{clean_dtype}" Value="0"/>')
        lines.append('        </Data>')
        lines.append('      </Tag>')
    return lines, clean_dtype


def write_l5x_rll(tags, routines):
    """Generate official Rockwell Automation Studio 5000 v32.00 Controller-level L5X Project File."""
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<RSLogix5000Content SchemaRevision="1.0" SoftwareRevision="32.00" TargetName="GNTF_FGCP_7404_001" TargetType="Controller" ContainsContext="false" Owner="EPPM / ASTRE" ExportDate="Fri Nov 06 15:30:00 2026">',
        '  <Controller Use="Target" Name="GNTF_FGCP_7404_001" ProcessorType="1756-L82E" MajorRev="32" MinorRev="11" ChassisType="1756-A13" PowerSupply="1756-PB72" ProjectCreationDate="Fri Nov 06 15:30:00 2026" LastModifiedDate="Fri Nov 06 15:30:00 2026">',
        '    <Description>',
        '      <![CDATA[GNTF Quinguila Tank Farm Control System Upgrade - FGCP-7404-001 (Allen-Bradley Relay Ladder Logic / RLL Converted from GE VersaMax P20890_Angola + New Phase 1 I/O per 01-MAN-03-06 & 01-MAN-03-07)]]>',
        '    </Description>',
        '    <DataTypes/>',
        '    <AddOnInstructionDefinitions/>',
        '    <Modules>',
        '      <Module Name="Local" CatalogNumber="1756-L82E" Vendor="1" ProductType="14" ProductCode="167" Major="32" Minor="11" ParentModule="Local" ParentModPortId="1" Inhibited="false" MajorFault="true">',
        '        <Ports>',
        '          <Port Id="1" Address="0" Type="ICP" Upstream="false"/>',
        '          <Port Id="2" Address="192.168.20.10" Type="Ethernet" Upstream="false"/>',
        '        </Ports>',
        '      </Module>',
        '      <Module Name="AI_Slot2_TB02" CatalogNumber="1756-IF16" Vendor="1" ProductType="10" ProductCode="10" Major="1" Minor="1" ParentModule="Local" ParentModPortId="1" Inhibited="false" MajorFault="false">',
        '        <Ports><Port Id="1" Address="2" Type="ICP" Upstream="true"/></Ports>',
        '      </Module>',
        '      <Module Name="AI_Slot3_TB03" CatalogNumber="1756-IF16" Vendor="1" ProductType="10" ProductCode="10" Major="1" Minor="1" ParentModule="Local" ParentModPortId="1" Inhibited="false" MajorFault="false">',
        '        <Ports><Port Id="1" Address="3" Type="ICP" Upstream="true"/></Ports>',
        '      </Module>',
        '      <Module Name="AI_Slot4_TB04" CatalogNumber="1756-IF16" Vendor="1" ProductType="10" ProductCode="10" Major="1" Minor="1" ParentModule="Local" ParentModPortId="1" Inhibited="false" MajorFault="false">',
        '        <Ports><Port Id="1" Address="4" Type="ICP" Upstream="true"/></Ports>',
        '      </Module>',
        '      <Module Name="AI_Slot5_TB05_Spare" CatalogNumber="1756-IF16" Vendor="1" ProductType="10" ProductCode="10" Major="1" Minor="1" ParentModule="Local" ParentModPortId="1" Inhibited="false" MajorFault="false">',
        '        <Ports><Port Id="1" Address="5" Type="ICP" Upstream="true"/></Ports>',
        '      </Module>',
        '      <Module Name="HART_Slot6_TB06" CatalogNumber="1756-IF8H" Vendor="1" ProductType="10" ProductCode="68" Major="1" Minor="1" ParentModule="Local" ParentModPortId="1" Inhibited="false" MajorFault="false">',
        '        <Ports><Port Id="1" Address="6" Type="ICP" Upstream="true"/></Ports>',
        '      </Module>',
        '      <Module Name="DI_Slot7_TB07" CatalogNumber="1756-IB32" Vendor="1" ProductType="7" ProductCode="14" Major="3" Minor="1" ParentModule="Local" ParentModPortId="1" Inhibited="false" MajorFault="false">',
        '        <Ports><Port Id="1" Address="7" Type="ICP" Upstream="true"/></Ports>',
        '      </Module>',
        '      <Module Name="DO_Slot8_TB08" CatalogNumber="1756-OB32" Vendor="1" ProductType="7" ProductCode="22" Major="3" Minor="1" ParentModule="Local" ParentModPortId="1" Inhibited="false" MajorFault="false">',
        '        <Ports><Port Id="1" Address="8" Type="ICP" Upstream="true"/></Ports>',
        '      </Module>',
        '      <Module Name="MCM_Slot9_Modbus" CatalogNumber="MVI56E-MCM" Vendor="309" ProductType="12" ProductCode="1" Major="1" Minor="1" ParentModule="Local" ParentModPortId="1" Inhibited="false" MajorFault="false">',
        '        <Ports><Port Id="1" Address="9" Type="ICP" Upstream="true"/></Ports>',
        '      </Module>',
        '    </Modules>',
        '    <Tags>',
    ]

    for tname, dtype, desc, alias_for in tags:
        tag_lines, _ = build_tag_xml_lines(tname, dtype, desc, alias_for)
        xml_lines.extend(tag_lines)

    xml_lines.extend([
        '    </Tags>',
        '    <Programs>',
        '      <Program Name="MainProgram" TestEdits="false" MainRoutineName="MainRoutine" Disabled="false" UseAsFolder="false">',
        '        <Description><![CDATA[FGCP-7404-001 Fire, Gas, ESD & Process Control Program (Relay Ladder Logic)]]></Description>',
        '        <Tags/>',
        '        <Routines>',
    ])

    for rname, rdesc, rungs in routines:
        xml_lines.append(f'          <Routine Name="{rname}" Type="RLL">')
        xml_lines.append(f'            <Description><![CDATA[{rdesc}]]></Description>')
        xml_lines.append('            <RLLContent>')
        for idx, rg in enumerate(rungs):
            comment = rg.get("comment", "")
            raw_text = rg.get("text", "")
            elems = parse_rung_elements(raw_text)
            formatted_text = format_logix_elements(elems)

            xml_lines.append(f'              <Rung Number="{idx}" Type="N">')
            if comment:
                xml_lines.append(f'                <Comment><![CDATA[{comment}]]></Comment>')
            xml_lines.append(f'                <Text><![CDATA[{formatted_text}]]></Text>')
            xml_lines.append('              </Rung>')
        xml_lines.append('            </RLLContent>')
        xml_lines.append('          </Routine>')

    xml_lines.extend([
        '        </Routines>',
        '      </Program>',
        '    </Programs>',
        '    <Tasks>',
        '      <Task Name="MainTask" Type="CONTINUOUS" Priority="10" Watchdog="500" DisableUpdateOutputs="false" InhibitTask="false">',
        '        <ScheduledPrograms>',
        '          <ScheduledProgram Name="MainProgram"/>',
        '        </ScheduledPrograms>',
        '      </Task>',
        '    </Tasks>',
        '  </Controller>',
        '</RSLogix5000Content>',
    ])

    l5x_content = "\n".join(xml_lines) + "\n"

    for out_dir in (BASE_DIR, DESKTOP_DIR):
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "P20890_Angola_AB_Ladder.L5X")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(l5x_content)
        print(f"[OK] Generated L5X Controller Ladder: {out_path} ({len(l5x_content):,} bytes)")

    # Verify XML well-formedness
    test_path = os.path.join(BASE_DIR, "P20890_Angola_AB_Ladder.L5X")
    try:
        ET.parse(test_path)
        print(f"[VERIFIED] XML parsed successfully! Controller L5X is strictly well-formed.")
    except Exception as e:
        print(f"[ERROR] XML parse failed: {e}")
        raise


def write_l5x_program_rll(tags, routines):
    """Generate Program-level L5X file for direct 'Import Program...' into ANY existing Studio 5000 project."""
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<RSLogix5000Content SchemaRevision="1.0" SoftwareRevision="32.00" TargetName="MainProgram" TargetType="Program" ContainsContext="true" Owner="EPPM / ASTRE" ExportDate="Fri Nov 06 15:30:00 2026">',
        '  <Program Use="Target" Name="MainProgram" TestEdits="false" MainRoutineName="MainRoutine" Disabled="false" UseAsFolder="false">',
        '    <Description>',
        '      <![CDATA[GNTF Quinguila Tank Farm Fire, Gas & ESD Control Panel (FGCP-7404-001) Program Import]]>',
        '    </Description>',
        '    <Tags>',
    ]

    for tname, dtype, desc, alias_for in tags:
        tag_lines, _ = build_tag_xml_lines(tname, dtype, desc, alias_for)
        xml_lines.extend(tag_lines)

    xml_lines.extend([
        '    </Tags>',
        '    <Routines>',
    ])

    for rname, rdesc, rungs in routines:
        xml_lines.append(f'      <Routine Name="{rname}" Type="RLL">')
        xml_lines.append(f'        <Description><![CDATA[{rdesc}]]></Description>')
        xml_lines.append('        <RLLContent>')
        for idx, rg in enumerate(rungs):
            comment = rg.get("comment", "")
            raw_text = rg.get("text", "")
            elems = parse_rung_elements(raw_text)
            formatted_text = format_logix_elements(elems)

            xml_lines.append(f'          <Rung Number="{idx}" Type="N">')
            if comment:
                xml_lines.append(f'            <Comment><![CDATA[{comment}]]></Comment>')
            xml_lines.append(f'            <Text><![CDATA[{formatted_text}]]></Text>')
            xml_lines.append('          </Rung>')
        xml_lines.append('        </RLLContent>')
        xml_lines.append('      </Routine>')

    xml_lines.extend([
        '    </Routines>',
        '  </Program>',
        '</RSLogix5000Content>',
    ])

    l5x_prog_content = "\n".join(xml_lines) + "\n"

    for out_dir in (BASE_DIR, DESKTOP_DIR):
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "P20890_Angola_AB_Program_Ladder.L5X")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(l5x_prog_content)
        print(f"[OK] Generated L5X Program Ladder: {out_path} ({len(l5x_prog_content):,} bytes)")

    test_path = os.path.join(BASE_DIR, "P20890_Angola_AB_Program_Ladder.L5X")
    try:
        ET.parse(test_path)
        print(f"[VERIFIED] XML parsed successfully! Program L5X is strictly well-formed.")
    except Exception as e:
        print(f"[ERROR] Program XML parse failed: {e}")
        raise


# =============================================================================
# 4. INTERACTIVE HTML LADDER DIAGRAM VIEWER GENERATOR
# =============================================================================
def write_ladder_html(tags, routines):
    """Generate standalone high-fidelity interactive SVG/HTML Ladder Diagram Viewer."""
    import re

    # Build tag map and cross reference dictionary
    tag_map = {t[0]: {"type": t[1], "desc": t[2], "alias": t[3], "reads": [], "writes": []} for t in tags}

    # Populate cross references
    for rname, rdesc, rungs in routines:
        for idx, rg in enumerate(rungs):
            text = rg['text']
            insts = re.findall(r'([A-Za-z0-9_]+)\((.*?)\)', text)
            for iname, iargs in insts:
                args = [a.strip() for a in iargs.split(',')]
                if iname in ('XIC', 'XIO', 'GRT', 'GEQ', 'LES', 'LEQ', 'EQU', 'NEQ', 'LIM'):
                    for a in args:
                        base = a.split('.')[0]
                        if base in tag_map:
                            ref_item = f"{rname}:Rung {idx}"
                            if ref_item not in tag_map[base]["reads"]:
                                tag_map[base]["reads"].append(ref_item)
                elif iname in ('OTE', 'OTL', 'OTU', 'RES'):
                    target = args[0].split('.')[0] if args else ""
                    if target in tag_map:
                        ref_item = f"{rname}:Rung {idx}"
                        if ref_item not in tag_map[target]["writes"]:
                            tag_map[target]["writes"].append(ref_item)
                elif iname in ('MOV', 'CPT', 'ADD', 'SUB', 'MUL', 'DIV'):
                    dest = args[0].split('.')[0] if iname == 'CPT' else (args[1].split('.')[0] if len(args) > 1 else "")
                    if dest in tag_map:
                        ref_item = f"{rname}:Rung {idx}"
                        if ref_item not in tag_map[dest]["writes"]:
                            tag_map[dest]["writes"].append(ref_item)

    # Render HTML routines
    routines_html = []
    routine_nav_items = []

    for r_idx, (rname, rdesc, rungs) in enumerate(routines):
        routine_nav_items.append(f'''
        <button class="routine-nav-btn {'active' if r_idx == 0 else ''}" onclick="selectRoutine('{rname}')" id="nav-{rname}">
            <div class="flex items-center justify-between">
                <span class="font-bold text-slate-800">{rname}</span>
                <span class="text-xs bg-slate-200 text-slate-700 px-2 py-0.5 rounded-full font-semibold">{len(rungs)}</span>
            </div>
            <div class="text-xs text-slate-500 truncate mt-0.5">{rdesc}</div>
        </button>
        ''')

        rungs_html = []
        for idx, rg in enumerate(rungs):
            comment = rg.get("comment", "")
            raw_text = rg.get("text", "")
            parsed_elems = parse_rung_elements(raw_text)
            elems_rendered = "".join(render_element_to_html(el, tag_map) for el in parsed_elems)

            comment_badge = f'<div class="rung-comment"><span class="comment-icon">&#x1F4AC;</span> {html.escape(comment)}</div>' if comment else ""
            escaped_raw = html.escape(raw_text)

            rungs_html.append(f'''
            <div class="rung-card" id="rung-{rname}-{idx}" data-routine="{rname}" data-rung="{idx}">
                <div class="rung-header">
                    <div class="flex items-center space-x-2">
                        <span class="rung-badge">RUNG {idx:03d}</span>
                        <span class="text-xs text-slate-400 font-mono">Routine: {rname}</span>
                    </div>
                    <button class="copy-btn" onclick="copyMnemonic('{escaped_raw}', this)" title="Copy Logix Mnemonic">
                        <svg class="w-3.5 h-3.5 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
                        Copy Mnemonic
                    </button>
                </div>
                {comment_badge}
                <div class="ladder-diagram-viewport">
                    <div class="power-rail left-rail" title="L1 +24VDC Bus Rail"><span class="rail-tag">L1</span></div>
                    <div class="rung-logic-track">
                        <div class="rung-main-wire"></div>
                        <div class="rung-elements-container">
                            {elems_rendered}
                        </div>
                        <div class="rung-main-wire"></div>
                    </div>
                    <div class="power-rail right-rail" title="N Neutral Return Bus Rail"><span class="rail-tag">0V</span></div>
                </div>
                <div class="mnemonic-bar font-mono text-xs text-slate-600 bg-slate-50 px-3 py-1.5 border-t border-slate-200">
                    <span class="text-slate-400 mr-2 select-none">MNEMONIC:</span>{escaped_raw}
                </div>
            </div>
            ''')

        routines_html.append(f'''
        <section class="routine-section {'hidden' if r_idx > 0 else ''}" id="section-{rname}">
            <div class="routine-title-bar">
                <div>
                    <h2 class="text-xl font-black text-slate-900 tracking-tight flex items-center space-x-2">
                        <span class="px-2.5 py-1 bg-blue-600 text-white rounded text-sm font-mono">{rname}</span>
                        <span>{rdesc}</span>
                    </h2>
                    <p class="text-xs text-slate-500 mt-1">Total Logic Rungs: <span class="font-bold text-slate-700">{len(rungs)}</span> &bull; Routine Type: Relay Ladder Logic (RLL)</p>
                </div>
            </div>
            <div class="space-y-4">
                {"".join(rungs_html)}
            </div>
        </section>
        ''')

    client_tag_db = {k: {"type": v["type"], "desc": v["desc"], "alias": v["alias"], "reads": v["reads"], "writes": v["writes"]} for k, v in tag_map.items()}
    tag_db_json = json.dumps(client_tag_db)

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Allen-Bradley ControlLogix 5580 Ladder Diagram Viewer &bull; FGCP-7404-001</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;500;600;700;900&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: #f1f5f9;
            color: #0f172a;
        }}
        .font-mono {{
            font-family: 'JetBrains Mono', monospace;
        }}
        /* Ladder Diagram Graphical Styling */
        .power-rail {{
            width: 14px;
            background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            user-select: none;
            box-shadow: 1px 0 3px rgba(0,0,0,0.2);
        }}
        .left-rail {{ border-right: 2px solid #0f172a; }}
        .right-rail {{ border-left: 2px solid #0f172a; }}
        .rail-tag {{
            writing-mode: vertical-rl;
            text-orientation: mixed;
            font-size: 9px;
            font-weight: 800;
            color: #f8fafc;
            letter-spacing: 2px;
            opacity: 0.8;
        }}
        .ladder-diagram-viewport {{
            display: flex;
            background-color: #ffffff;
            border-top: 1px solid #e2e8f0;
            border-bottom: 1px solid #e2e8f0;
            overflow-x: auto;
            min-height: 110px;
        }}
        .rung-logic-track {{
            display: flex;
            align-items: center;
            flex-grow: 1;
            position: relative;
            padding: 12px 0;
            min-width: max-content;
        }}
        .rung-main-wire {{
            height: 3px;
            background-color: #1e293b;
            flex-grow: 1;
            min-width: 24px;
        }}
        .rung-elements-container {{
            display: flex;
            align-items: center;
        }}
        /* Contact Box */
        .ladder-elem {{
            display: inline-flex;
            align-items: center;
            cursor: pointer;
            transition: all 0.15s ease-in-out;
            user-select: none;
        }}
        .elem-lead, .elem-trail {{
            width: 20px;
            height: 3px;
            background-color: #1e293b;
        }}
        .elem-main {{
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 2px 6px;
            border-radius: 4px;
            border: 1px solid transparent;
            min-width: 80px;
        }}
        .ladder-elem:hover .elem-main {{
            background-color: #eff6ff;
            border-color: #93c5fd;
            box-shadow: 0 2px 4px rgba(59, 130, 246, 0.15);
        }}
        .elem-tagname {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            font-weight: 700;
            color: #1d4ed8;
            margin-bottom: 2px;
            text-align: center;
            max-width: 140px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        .elem-desc {{
            font-size: 9px;
            color: #64748b;
            max-width: 130px;
            text-align: center;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            margin-top: 2px;
        }}
        .contact-symbol {{
            display: flex;
            align-items: center;
            font-family: 'JetBrains Mono', monospace;
            font-size: 24px;
            font-weight: 900;
            color: #0f172a;
            line-height: 1;
            height: 28px;
        }}
        .contact-slash {{
            font-size: 26px;
            font-weight: 900;
            color: #dc2626;
            transform: scale(1.1) rotate(10deg);
            margin: 0 -2px;
        }}
        .contact-gap {{
            width: 12px;
        }}
        /* Coil Box */
        .coil-box .elem-tagname {{
            color: #059669;
        }}
        .coil-box.otl .elem-tagname {{
            color: #d97706;
        }}
        .coil-box.otu .elem-tagname {{
            color: #b45309;
        }}
        .coil-symbol {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 20px;
            font-weight: 800;
            color: #059669;
            line-height: 1;
            height: 28px;
            display: flex;
            align-items: center;
        }}
        .coil-box.otl .coil-symbol {{
            color: #d97706;
        }}
        .coil-box.otu .coil-symbol {{
            color: #b45309;
        }}
        /* Blocks */
        .block-card {{
            border: 2px solid #334155;
            background-color: #f8fafc;
            border-radius: 4px;
            padding: 4px 8px;
            font-size: 11px;
            min-width: 150px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }}
        .block-header {{
            font-weight: 800;
            font-size: 10px;
            text-transform: uppercase;
            border-bottom: 1px solid #cbd5e1;
            padding-bottom: 2px;
            margin-bottom: 4px;
            color: #0f172a;
        }}
        .block-row {{
            display: flex;
            justify-content: space-between;
            gap: 8px;
            font-size: 10px;
            line-height: 1.3;
        }}
        .block-row .lbl {{
            color: #64748b;
        }}
        .block-row .val {{
            color: #0f172a;
            font-weight: 600;
        }}
        .block-footer {{
            display: flex;
            justify-content: space-between;
            font-size: 9px;
            font-weight: 700;
            color: #059669;
            margin-top: 4px;
            border-top: 1px dashed #cbd5e1;
            padding-top: 2px;
        }}
        .cpt-block .block-card {{ border-color: #2563eb; background-color: #eff6ff; }}
        .mov-block .block-card {{ border-color: #0d9488; background-color: #f0fdfa; }}
        .ton-block .block-card {{ border-color: #7c3aed; background-color: #faf5ff; }}
        .cmp-block .block-card {{ border-color: #c026d3; background-color: #fdf4ff; }}
        .jsr-card {{ border-color: #ea580c; background-color: #fff7ed; }}

        /* Branches */
        .ladder-branch {{
            display: inline-flex;
            align-items: center;
            position: relative;
            margin: 0 4px;
        }}
        .branch-bar {{
            width: 3px;
            background-color: #1e293b;
            align-self: stretch;
        }}
        .branch-stack {{
            display: flex;
            flex-direction: column;
            gap: 12px;
            padding: 8px 0;
        }}
        .branch-leg {{
            display: flex;
            align-items: center;
        }}
        .branch-wire {{
            height: 3px;
            width: 14px;
            background-color: #1e293b;
        }}
        .leg-content {{
            display: flex;
            align-items: center;
        }}

        /* Rung Card */
        .rung-card {{
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            overflow: hidden;
            transition: all 0.2s ease;
        }}
        .rung-card:hover {{
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border-color: #94a3b8;
        }}
        .rung-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 6px 12px;
            background-color: #f8fafc;
            border-bottom: 1px solid #e2e8f0;
        }}
        .rung-badge {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            font-weight: 800;
            background-color: #0f172a;
            color: #ffffff;
            padding: 2px 6px;
            border-radius: 4px;
        }}
        .rung-comment {{
            background-color: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 6px 12px;
            font-size: 12px;
            font-weight: 500;
            color: #78350f;
            display: flex;
            align-items: center;
        }}
        .comment-icon {{
            margin-right: 6px;
        }}
        .copy-btn {{
            font-size: 11px;
            color: #475569;
            background-color: #ffffff;
            border: 1px solid #cbd5e1;
            padding: 2px 8px;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.15s;
        }}
        .copy-btn:hover {{
            background-color: #f1f5f9;
            color: #0f172a;
            border-color: #94a3b8;
        }}
        .routine-nav-btn {{
            width: 100%;
            text-align: left;
            padding: 8px 12px;
            border-radius: 6px;
            transition: all 0.15s ease;
            margin-bottom: 2px;
        }}
        .routine-nav-btn:hover {{
            background-color: #e2e8f0;
        }}
        .routine-nav-btn.active {{
            background-color: #2563eb;
            color: #ffffff;
        }}
        .routine-nav-btn.active span {{
            color: #ffffff !important;
        }}
        .routine-nav-btn.active div {{
            color: #bfdbfe !important;
        }}
        .routine-title-bar {{
            background-color: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}
    </style>
</head>
<body class="h-screen flex flex-col overflow-hidden">

    <!-- Top Navigation Header -->
    <header class="bg-slate-900 text-white flex-shrink-0 border-b border-slate-800 shadow-lg z-20">
        <div class="px-6 py-3 flex items-center justify-between">
            <div class="flex items-center space-x-4">
                <div class="h-9 w-9 bg-orange-500 rounded-lg flex items-center justify-center font-black text-lg text-white shadow-inner">
                    AB
                </div>
                <div>
                    <div class="flex items-center space-x-2">
                        <h1 class="text-base font-bold tracking-tight text-white">Allen-Bradley ControlLogix 5580 &bull; Studio 5000 RLL</h1>
                        <span class="bg-blue-600/80 text-blue-100 text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider">Project P20890</span>
                    </div>
                    <p class="text-xs text-slate-400">GNTF Quinguila Tank Farm Fire, Gas & ESD Control Panel (FGCP-7404-001)</p>
                </div>
            </div>

            <div class="flex items-center space-x-3">
                <div class="text-right mr-2 hidden md:block">
                    <div class="text-xs font-semibold text-emerald-400">&bull; 432 Ladder Rungs &bull; 25 Routines</div>
                    <div class="text-[11px] text-slate-400 font-mono">1756-L82E Chassis Slot 0 &bull; v32.011</div>
                </div>

                <a href="P20890_Angola_AB_Ladder.L5X" download="P20890_Angola_AB_Ladder.L5X" class="bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold px-3.5 py-2 rounded-md shadow flex items-center space-x-1.5 transition">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                    <span>Download .L5X</span>
                </a>

                <button onclick="window.print()" class="bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold px-3 py-2 rounded-md border border-slate-700 flex items-center space-x-1 transition">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path></svg>
                    <span>Print</span>
                </button>
            </div>
        </div>
    </header>

    <!-- Main Workspace -->
    <div class="flex flex-1 overflow-hidden">
        
        <!-- Sidebar: Routines & Search -->
        <aside class="w-80 bg-slate-100 border-r border-slate-300 flex flex-col flex-shrink-0 z-10">
            <!-- Search & Filter -->
            <div class="p-3 border-b border-slate-200 bg-white">
                <div class="relative">
                    <input type="text" id="searchInput" oninput="filterRungs()" placeholder="Search tag, operand, comment..." class="w-full bg-slate-50 border border-slate-300 rounded-md py-1.5 pl-8 pr-3 text-xs focus:ring-2 focus:ring-blue-500 focus:outline-none">
                    <svg class="w-4 h-4 text-slate-400 absolute left-2.5 top-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                </div>
                <div class="flex items-center justify-between mt-2 text-[11px] text-slate-500 font-medium">
                    <span>Program Routines (25)</span>
                    <button onclick="showAllRoutines()" class="text-blue-600 hover:underline">Show All</button>
                </div>
            </div>

            <!-- Routine Navigation List -->
            <div class="flex-1 overflow-y-auto p-2 space-y-1" id="routineNavList">
                {"".join(routine_nav_items)}
            </div>
            
            <div class="p-3 bg-slate-200/80 border-t border-slate-300 text-[11px] text-slate-600 font-mono">
                <div>CHASSIS: 1756-A13 (13 Slots)</div>
                <div>POWER: 1756-PB72 24VDC</div>
            </div>
        </aside>

        <!-- Center: Ladder Diagrams Canvas -->
        <main class="flex-1 overflow-y-auto p-6 bg-slate-100" id="mainCanvas">
            {"".join(routines_html)}
        </main>

        <!-- Right Drawer: Tag Inspector -->
        <div id="tagInspector" class="fixed right-0 top-0 bottom-0 w-96 bg-white shadow-2xl border-l border-slate-300 transform translate-x-full transition-transform duration-300 ease-in-out z-30 flex flex-col">
            <div class="p-4 bg-slate-900 text-white flex items-center justify-between">
                <div class="flex items-center space-x-2">
                    <span class="w-2.5 h-2.5 bg-emerald-400 rounded-full"></span>
                    <h3 class="font-bold text-sm">Tag Cross-Reference Inspector</h3>
                </div>
                <button onclick="closeInspector()" class="text-slate-400 hover:text-white">&times;</button>
            </div>
            <div class="p-4 flex-1 overflow-y-auto space-y-4">
                <div>
                    <span class="text-[10px] font-bold uppercase text-slate-400 tracking-wider">Tag Name</span>
                    <div id="inspectTagName" class="text-base font-black font-mono text-blue-600 mt-0.5 break-all"></div>
                </div>
                <div class="grid grid-cols-2 gap-2 text-xs">
                    <div class="bg-slate-50 p-2.5 rounded border border-slate-200">
                        <span class="text-[10px] font-semibold text-slate-500 uppercase">Data Type</span>
                        <div id="inspectTagType" class="font-bold text-slate-800 font-mono mt-0.5"></div>
                    </div>
                    <div class="bg-slate-50 p-2.5 rounded border border-slate-200">
                        <span class="text-[10px] font-semibold text-slate-500 uppercase">Hardware Alias</span>
                        <div id="inspectTagAlias" class="font-bold text-slate-800 font-mono mt-0.5 truncate"></div>
                    </div>
                </div>
                <div>
                    <span class="text-[10px] font-bold uppercase text-slate-400 tracking-wider">Engineering Description</span>
                    <div id="inspectTagDesc" class="text-xs text-slate-700 bg-slate-50 p-2.5 rounded border border-slate-200 mt-0.5 leading-relaxed"></div>
                </div>
                <div>
                    <span class="text-[10px] font-bold uppercase text-slate-400 tracking-wider">Referenced In Logic</span>
                    <div class="mt-2 space-y-3">
                        <div>
                            <div class="text-xs font-bold text-blue-700 mb-1 flex items-center">
                                <span class="w-2 h-2 rounded-full bg-blue-600 mr-1.5"></span>
                                Read References (XIC / XIO / Compare):
                            </div>
                            <div id="inspectReads" class="flex flex-wrap gap-1"></div>
                        </div>
                        <div>
                            <div class="text-xs font-bold text-emerald-700 mb-1 flex items-center">
                                <span class="w-2 h-2 rounded-full bg-emerald-600 mr-1.5"></span>
                                Write References (OTE / OTL / OTU / CPT):
                            </div>
                            <div id="inspectWrites" class="flex flex-wrap gap-1"></div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="p-3 bg-slate-50 border-t border-slate-200">
                <button onclick="closeInspector()" class="w-full bg-slate-200 hover:bg-slate-300 text-slate-700 text-xs font-bold py-2 rounded transition">Close Inspector</button>
            </div>
        </div>

    </div>

    <!-- Client Script -->
    <script>
        const TAG_DB = {tag_db_json};

        function selectRoutine(rname) {{
            document.querySelectorAll('.routine-section').forEach(sec => sec.classList.add('hidden'));
            const targetSec = document.getElementById('section-' + rname);
            if (targetSec) targetSec.classList.remove('hidden');

            document.querySelectorAll('.routine-nav-btn').forEach(btn => btn.classList.remove('active'));
            const targetBtn = document.getElementById('nav-' + rname);
            if (targetBtn) targetBtn.classList.add('active');

            document.getElementById('mainCanvas').scrollTop = 0;
        }}

        function showAllRoutines() {{
            document.querySelectorAll('.routine-section').forEach(sec => sec.classList.remove('hidden'));
            document.querySelectorAll('.routine-nav-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById('mainCanvas').scrollTop = 0;
        }}

        function filterRungs() {{
            const query = document.getElementById('searchInput').value.toLowerCase().trim();
            if (!query) {{
                const activeNav = document.querySelector('.routine-nav-btn.active');
                if (activeNav) {{
                    const rname = activeNav.id.replace('nav-', '');
                    selectRoutine(rname);
                }} else {{
                    showAllRoutines();
                }}
                return;
            }}

            document.querySelectorAll('.routine-section').forEach(sec => sec.classList.remove('hidden'));

            document.querySelectorAll('.rung-card').forEach(card => {{
                const text = card.textContent.toLowerCase();
                if (text.includes(query)) {{
                    card.style.display = '';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
        }}

        function inspectTag(rawTag) {{
            const baseTag = rawTag.split('.')[0];
            const info = TAG_DB[baseTag] || {{ type: 'TAG', desc: 'System / Operand Reference', alias: '', reads: [], writes: [] }};

            document.getElementById('inspectTagName').textContent = rawTag;
            document.getElementById('inspectTagType').textContent = info.type || 'BOOL';
            document.getElementById('inspectTagAlias').textContent = info.alias || 'Internal Controller Tag';
            document.getElementById('inspectTagDesc').textContent = info.desc || 'No description provided in tag database.';

            const readsContainer = document.getElementById('inspectReads');
            readsContainer.innerHTML = '';
            if (info.reads && info.reads.length > 0) {{
                info.reads.forEach(ref => {{
                    const span = document.createElement('span');
                    span.className = 'text-[11px] font-mono bg-blue-100 text-blue-800 px-2 py-0.5 rounded cursor-pointer hover:bg-blue-200';
                    span.textContent = ref;
                    span.onclick = () => jumpToRung(ref);
                    readsContainer.appendChild(span);
                }});
            }} else {{
                readsContainer.innerHTML = '<span class="text-xs text-slate-400 italic">No direct read instructions found.</span>';
            }}

            const writesContainer = document.getElementById('inspectWrites');
            writesContainer.innerHTML = '';
            if (info.writes && info.writes.length > 0) {{
                info.writes.forEach(ref => {{
                    const span = document.createElement('span');
                    span.className = 'text-[11px] font-mono bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded cursor-pointer hover:bg-emerald-200';
                    span.textContent = ref;
                    span.onclick = () => jumpToRung(ref);
                    writesContainer.appendChild(span);
                }});
            }} else {{
                writesContainer.innerHTML = '<span class="text-xs text-slate-400 italic">No direct write instructions found.</span>';
            }}

            document.getElementById('tagInspector').classList.remove('translate-x-full');
        }}

        function jumpToRung(ref) {{
            const parts = ref.split(':Rung ');
            if (parts.length === 2) {{
                const rname = parts[0];
                const rnum = parseInt(parts[1], 10);
                selectRoutine(rname);
                const rungElem = document.getElementById(`rung-${{rname}}-${{rnum}}`);
                if (rungElem) {{
                    rungElem.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                    rungElem.classList.add('ring-4', 'ring-blue-500');
                    setTimeout(() => rungElem.classList.remove('ring-4', 'ring-blue-500'), 2000);
                }}
            }}
        }}

        function closeInspector() {{
            document.getElementById('tagInspector').classList.add('translate-x-full');
        }}

        function copyMnemonic(txt, btn) {{
            navigator.clipboard.writeText(txt).then(() => {{
                const old = btn.innerHTML;
                btn.innerHTML = '<span class="text-emerald-600 font-bold">&#10003; Copied!</span>';
                setTimeout(() => btn.innerHTML = old, 1500);
            }});
        }}
    </script>
</body>
</html>'''

    for out_dir in (BASE_DIR, DESKTOP_DIR):
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "P20890_Angola_AB_Ladder.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"[OK] Generated HTML Ladder Viewer: {out_path} ({len(html_content):,} bytes)")
