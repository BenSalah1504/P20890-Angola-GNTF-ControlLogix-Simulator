"""Generate an interactive HTML viewer + printable PDF of a GE Proficy Machine
Edition (.SwxCF) ladder logic project.
"""
import html
import json
import os
import re
import subprocess
import sys

import pme_parse as P

FUNC_INFO = {
    33:  ('TMR_TENTHS',   ['PV', ''],          ['Q', '']),
    36:  ('ONDTR_TENTHS', ['R', 'PV'],         ['Q', '', '']),
    42:  ('UPCTR',        ['CTU', 'R', 'PV'],  ['Q', '', '']),
    47:  ('SUB_INT',      ['', 'I1', 'I2'],    ['', 'Q', '']),
    51:  ('DIV_INT',      ['', 'I1', 'I2'],    ['', 'Q', '']),
    70:  ('MUL_DINT',     ['', 'I1', 'I2'],    ['', 'Q', '']),
    71:  ('DIV_DINT',     ['', 'I1', 'I2'],    ['', 'Q', '']),
    73:  ('SUB_REAL',     ['', 'I1', 'I2'],    ['', 'Q', '']),
    74:  ('MUL_REAL',     ['', 'I1', 'I2'],    ['', 'Q', '']),
    75:  ('DIV_REAL',     ['', 'I1', 'I2'],    ['', 'Q', '']),
    83:  ('MOVE_REAL',    ['', 'IN'],          ['', 'Q']),
    93:  ('GE_INT',       ['', 'I1', 'I2'],    ['', '', '']),
    95:  ('GE_REAL',      ['', 'I1', 'I2'],    ['', '', '']),
    101: ('LE_INT',       ['', 'I1', 'I2'],    ['', '', '']),
    103: ('LE_REAL',      ['', 'I1', 'I2'],    ['', '', '']),
    208: ('INT_TO_REAL',  ['', 'IN'],          ['', 'Q']),
    233: ('MOVE_WORD',    ['', 'IN'],          ['', 'Q']),
    235: ('MOVE_INT',     ['', 'IN'],          ['', 'Q']),
    266: ('BLK_CLR_WORD', ['', 'IN'],          ['', '']),
    302: ('SVC_REQ',      ['', 'FNC', 'PRM'],  ['', '', '']),
}

LOGICAL_ORDER = [
    '_MAIN',
    'Init',
    'Input', 'DI_1', 'DI_2', 'AI_1', 'AI_2', 'AI_3',
    'CalcVa1', 'CalcVa2', 'CalcVa3', 'Ai_AL_1', 'Ai_AL_2', 'Ai_AL_3',
    'Vote_1',
    'Logic', 'CE_LOG', 'Sound',
    'Output', 'Indicat', 'Shutdow', 'Protect', 'Loc_Al', 'FLT_1',
]


def esc(s):
    return html.escape(str(s or ''), quote=True)


def split_rungs(rows):
    rungs = []
    i = 0
    while i < len(rows):
        if not any(rows[i]):
            i += 1
            continue
        if rows[i][1] and rows[i][1].cls == 'LDComment':
            rungs.append([i])
            i += 1
            continue
        rg = [i]
        i += 1
        while i < len(rows):
            if not any(rows[i]) or (rows[i][1] and rows[i][1].cls == 'LDComment'):
                break
            up = any(
                (e.flags[0] & 2)
                for e in rows[i]
                if e and e.flags and e.cls not in ('LDFunctionHead', 'LDDataInput', 'LDDataOutput')
            )
            sub = up or any(
                e.cls in ('LDFunctionSegment', 'LDDataInput', 'LDDataOutput', 'LDShuntVert', 'LDContactContinue')
                for e in rows[i]
                if e
            )
            if not sub:
                break
            rg.append(i)
            i += 1
        rungs.append(rg)
    return rungs


def fmt_op(op, tags, names):
    """Return (primary_label, addr_label, desc_label, tag_id)."""
    if not op:
        return ('', '', '', None)
    if op[0] == 'const':
        return (op[1], 'CONST', '', None)
    if op[0] == 'var':
        tid = op[1]
        info = tags.get(tid, {})
        nm = info.get('name') or names.get(tid) or ('VAR_%d' % tid)
        return (nm, info.get('addr', ''), info.get('desc', ''), tid)
    if op[0] == 'index':
        b_nm, b_ad, b_ds, tid = fmt_op(op[1], tags, names)
        i_nm, _, _, _ = fmt_op(op[2], tags, names)
        return ('%s[%s]' % (b_nm, i_nm), b_ad, b_ds, tid)
    return (str(op), '', '', None)


def trunc(s, n=22):
    s = str(s or '')
    return s if len(s) <= n else s[:n - 1] + '…'


def render_rung_svg(rows, rg, calls, tags, names):
    """Render a logic rung (list of row indices) as an SVG diagram."""
    CW = 104
    CH = 68
    RAIL_L = 38
    WY = 34
    max_col = max((c for r in rg for c, e in enumerate(rows[r]) if e), default=10)
    ncols = max(max_col, 10)
    RAIL_R = RAIL_L + ncols * CW
    W = RAIL_R + 24
    H = len(rg) * CH + 12

    out = [
        f'<svg class="ladder-svg" viewBox="0 0 {W} {H}" width="100%" '
        f'style="max-width:{W}px;height:auto" xmlns="http://www.w3.org/2000/svg">'
    ]
    # Power rails
    out.append(f'<line x1="{RAIL_L}" y1="4" x2="{RAIL_L}" y2="{H-4}" class="rail"/>')
    out.append(f'<line x1="{RAIL_R}" y1="4" x2="{RAIL_R}" y2="{H-4}" class="rail"/>')

    for ri, r in enumerate(rg):
        y0 = ri * CH + 4
        wy = y0 + WY
        row = rows[r]
        for c in range(1, ncols + 1):
            e = row[c] if c < len(row) else None
            if not e:
                continue
            x0 = RAIL_L + (c - 1) * CW
            xc = x0 + CW / 2
            x1 = x0 + CW
            fl = e.flags[0] if e.flags else 0
            has_l = bool(fl & 1)
            has_u = bool(fl & 2)
            has_r = bool(fl & 4)
            has_d = bool(fl & 8)

            cls = e.cls

            # Vertical shunt links on the right edge of the cell
            if cls in ('LDShunt', 'LDShuntVert'):
                if has_l:
                    out.append(f'<line x1="{x0}" y1="{wy}" x2="{x1}" y2="{wy}" class="wire"/>')
                if has_r:
                    out.append(f'<line x1="{x0}" y1="{wy}" x2="{x1}" y2="{wy}" class="wire"/>')
                if has_u:
                    out.append(f'<line x1="{x1}" y1="{y0}" x2="{x1}" y2="{wy}" class="wire"/>')
                if has_d:
                    out.append(f'<line x1="{x1}" y1="{wy}" x2="{x1}" y2="{y0+CH}" class="wire"/>')
                continue

            if cls == 'LDShuntHorz':
                out.append(f'<line x1="{x0}" y1="{wy}" x2="{x1}" y2="{wy}" class="wire"/>')
                if has_u:
                    out.append(f'<line x1="{x1}" y1="{y0}" x2="{x1}" y2="{wy}" class="wire"/>')
                if has_d:
                    out.append(f'<line x1="{x1}" y1="{wy}" x2="{x1}" y2="{y0+CH}" class="wire"/>')
                continue

            # Vertical drop on right border for contacts/shunts with Down/Up flags
            if cls in ('LDContactNO', 'LDContactNC', 'LDContactContinue'):
                if has_u:
                    out.append(f'<line x1="{x1}" y1="{y0}" x2="{x1}" y2="{wy}" class="wire"/>')
                if has_d:
                    out.append(f'<line x1="{x1}" y1="{wy}" x2="{x1}" y2="{y0+CH}" class="wire"/>')

            if cls in ('LDContactNO', 'LDContactNC'):
                nm, ad, ds, tid = fmt_op(e.op, tags, names)
                out.append(f'<g class="el" data-tag="{esc(nm)}"><title>{esc(nm)} ({esc(ad)})\n{esc(ds)}</title>')
                out.append(f'<line x1="{x0}" y1="{wy}" x2="{xc-12}" y2="{wy}" class="wire"/>')
                if has_r:
                    out.append(f'<line x1="{xc+12}" y1="{wy}" x2="{x1}" y2="{wy}" class="wire"/>')
                out.append(f'<line x1="{xc-12}" y1="{wy-11}" x2="{xc-12}" y2="{wy+11}" class="sym"/>')
                out.append(f'<line x1="{xc+12}" y1="{wy-11}" x2="{xc+12}" y2="{wy+11}" class="sym"/>')
                if cls == 'LDContactNC':
                    out.append(f'<line x1="{xc-9}" y1="{wy+9}" x2="{xc+9}" y2="{wy-9}" class="sym"/>')
                if ad:
                    out.append(f'<text x="{xc}" y="{wy-15}" class="addr">{esc(ad)}</text>')
                out.append(f'<text x="{xc}" y="{wy+23}" class="tag">{esc(trunc(nm, 18))}</text>')
                if ds:
                    out.append(f'<text x="{xc}" y="{wy+32}" class="desc">{esc(trunc(ds, 22))}</text>')
                out.append('</g>')

            elif cls == 'LDContactContinue':
                out.append(f'<line x1="{xc}" y1="{wy}" x2="{x1}" y2="{wy}" class="wire"/>')
                out.append(f'<polygon points="{xc-10},{wy-7} {xc},{wy} {xc-10},{wy+7}" class="cont"/>')
                out.append(f'<text x="{xc}" y="{wy-12}" class="addr">CONT</text>')

            elif cls == 'LDCoilContinue':
                out.append(f'<line x1="{x0}" y1="{wy}" x2="{xc}" y2="{wy}" class="wire"/>')
                out.append(f'<polygon points="{xc},{wy-7} {xc+10},{wy} {xc},{wy+7}" class="cont"/>')
                out.append(f'<text x="{xc}" y="{wy-12}" class="addr">CONT</text>')

            elif cls.startswith('LDCoil'):
                nm, ad, ds, tid = fmt_op(e.op, tags, names)
                out.append(f'<g class="el" data-tag="{esc(nm)}"><title>{esc(nm)} ({esc(ad)})\n{esc(ds)}</title>')
                out.append(f'<line x1="{x0}" y1="{wy}" x2="{xc-13}" y2="{wy}" class="wire"/>')
                out.append(f'<line x1="{xc+13}" y1="{wy}" x2="{x1}" y2="{wy}" class="wire"/>')
                out.append(f'<path d="M{xc-7},{wy-11} A12,12 0 0,0 {xc-7},{wy+11}" class="sym" fill="none"/>')
                out.append(f'<path d="M{xc+7},{wy-11} A12,12 0 0,1 {xc+7},{wy+11}" class="sym" fill="none"/>')
                ltr = {
                    'LDCoilNC': '/',
                    'LDCoilSet': 'S',
                    'LDCoilReset': 'R',
                    'LDCoilPtrans': '↑',
                }.get(cls, '')
                if ltr:
                    out.append(f'<text x="{xc}" y="{wy+4}" class="coil-ltr">{ltr}</text>')
                if ad:
                    out.append(f'<text x="{xc}" y="{wy-15}" class="addr">{esc(ad)}</text>')
                out.append(f'<text x="{xc}" y="{wy+23}" class="tag">{esc(trunc(nm, 18))}</text>')
                if ds:
                    out.append(f'<text x="{xc}" y="{wy+32}" class="desc">{esc(trunc(ds, 22))}</text>')
                out.append('</g>')

            elif cls == 'LDCall':
                t_id = calls[e.target] if e.target < len(calls) else e.target
                t_nm = names.get(t_id, f'Block_{t_id}')
                out.append(f'<g class="el call-box" onclick="jumpBlock(\'{esc(t_nm)}\')">')
                out.append(f'<line x1="{x0}" y1="{wy}" x2="{x0+10}" y2="{wy}" class="wire"/>')
                if has_r:
                    out.append(f'<line x1="{x1-10}" y1="{wy}" x2="{x1}" y2="{wy}" class="wire"/>')
                out.append(f'<rect x="{x0+10}" y="{wy-16}" width="{CW-20}" height="32" rx="4" class="fbox call-rect"/>')
                out.append(f'<text x="{xc}" y="{wy-3}" class="fname">CALL</text>')
                out.append(f'<text x="{xc}" y="{wy+10}" class="ftarg">{esc(t_nm)}</text>')
                out.append('</g>')

            elif cls in ('LDDataInput', 'LDDataOutput'):
                nm, ad, ds, tid = fmt_op(e.op, tags, names)
                out.append(f'<g class="el" data-tag="{esc(nm)}"><title>{esc(nm)} ({esc(ad)})\n{esc(ds)}</title>')
                if cls == 'LDDataInput':
                    out.append(f'<line x1="{x1-18}" y1="{wy}" x2="{x1}" y2="{wy}" class="wire-data"/>')
                    tx = x1 - 22
                    anc = 'end'
                else:
                    out.append(f'<line x1="{x0}" y1="{wy}" x2="{x0+18}" y2="{wy}" class="wire-data"/>')
                    tx = x0 + 22
                    anc = 'start'
                if ad and ad != 'CONST':
                    out.append(f'<text x="{tx}" y="{wy-9}" text-anchor="{anc}" class="addr">{esc(ad)}</text>')
                out.append(f'<text x="{tx}" y="{wy+4}" text-anchor="{anc}" class="dval">{esc(trunc(nm, 17))}</text>')
                out.append('</g>')

            elif cls == 'LDFunctionHead':
                fnm, in_pins, out_pins = FUNC_INFO.get(e.func, (f'FUNC_{e.func}', [], []))
                nsegs = len(e.segs)
                bh = (nsegs + 1) * CH - 16
                by = y0 + 10
                bx = x0 + 8
                bw = CW - 16
                out.append(f'<g class="el func-group">')
                # Left/right enable wires on head row
                out.append(f'<line x1="{x0}" y1="{wy}" x2="{bx}" y2="{wy}" class="wire"/>')
                if has_r or (c + 1 < len(row) and row[c + 1] is not None):
                    out.append(f'<line x1="{bx+bw}" y1="{wy}" x2="{x1}" y2="{wy}" class="wire"/>')
                # Segment row wires if adjacent contact/shunt is present
                for si in range(1, nsegs + 1):
                    if ri + si < len(rg):
                        r_s = rg[ri + si]
                        wy_s = (ri + si) * CH + 4 + WY
                        left_e = rows[r_s][c - 1] if c - 1 >= 0 else None
                        if left_e and left_e.cls not in ('LDDataInput',):
                            out.append(f'<line x1="{x0}" y1="{wy_s}" x2="{bx}" y2="{wy_s}" class="wire"/>')
                out.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="5" class="fbox"/>')
                out.append(f'<text x="{xc}" y="{by+16}" class="fname">{esc(fnm)}</text>')
                # Instance / length parameter inside box
                if e.op1:
                    p1, a1, d1, _ = fmt_op(e.op1, tags, names)
                    out.append(f'<text x="{xc}" y="{by+30}" class="finst">{esc(trunc(p1, 15))}</text>')
                    if a1:
                        out.append(f'<text x="{xc}" y="{by+40}" class="addr">{esc(a1)}</text>')
                elif e.op2:
                    p2, _, _, _ = fmt_op(e.op2, tags, names)
                    out.append(f'<text x="{xc}" y="{by+30}" class="finst">LEN={esc(p2)}</text>')
                # Pin labels
                for pi, pl in enumerate(in_pins):
                    if pl:
                        py = (ri + pi) * CH + 4 + WY + 4
                        out.append(f'<text x="{bx+4}" y="{py}" class="pin-l">{esc(pl)}</text>')
                for pi, pl in enumerate(out_pins):
                    if pl:
                        py = (ri + pi) * CH + 4 + WY + 4
                        out.append(f'<text x="{bx+bw-4}" y="{py}" class="pin-r">{esc(pl)}</text>')
                out.append('</g>')

    out.append('</svg>')
    return ''.join(out)


def parse_xref_rungs(ole, blk_name, tags, names):
    """Return {rung_no: [formatted strings]} from the XRef stream."""
    raw = ole.openstream(f'Document 2/LDBlocks/{blk_name}/XRef').read().decode('latin1')
    res = {}
    for r_str, body in sorted(set(re.findall(r'Rung (\d+)\] ([^\x00-\x1f]*)', raw))):
        rno = int(r_str)
        def repl_var(m):
            tid = int(m.group(1))
            info = tags.get(tid, {})
            nm = info.get('name') or names.get(tid) or f'VAR_{tid}'
            ad = info.get('addr', '')
            return f'{nm} ({ad})' if ad else nm
        body = re.sub(r'<223,(\d+)>', repl_var, body)
        body = re.sub(r'\{(\d+)\}', lambda m: names.get(int(m.group(1)), m.group(0)), body)
        res.setdefault(rno, []).append(body)
    return res


def build_html(swxcf_path, out_html):
    names, tags, _, blocks_raw, ole = P.load_project(swxcf_path)
    ordered = [b for b in LOGICAL_ORDER if b in blocks_raw] + [
        b for b in sorted(blocks_raw) if b not in LOGICAL_ORDER
    ]

    nav_items = []
    sections = []
    total_rungs = 0

    for bname in ordered:
        data = blocks_raw[bname]
        rows, w, calls, p, L = P.parse_block(data)
        rungs = split_rungs(rows)
        xref_map = parse_xref_rungs(ole, bname, tags, names)
        max_xr = max(xref_map) if xref_map else len(rungs)
        n_rungs = max(len(rungs), max_xr)
        total_rungs += n_rungs

        # Summary description from first comment if present
        first_cmt = ''
        if rungs and rows[rungs[0][0]][1] and rows[rungs[0][0]][1].cls == 'LDComment':
            first_cmt = rows[rungs[0][0]][1].text.strip().splitlines()[0]

        nav_items.append(
            f'<a class="nav-item" href="#blk-{esc(bname)}" onclick="showBlock(\'{esc(bname)}\')">'
            f'<span class="bname">{esc(bname)}</span>'
            f'<span class="bmeta">{n_rungs} rungs</span></a>'
        )

        sec = [
            f'<section class="block-sec" id="blk-{esc(bname)}" data-block="{esc(bname)}">',
            f'<div class="block-hdr">'
            f'<div><h2>Block: {esc(bname)}</h2>'
            f'<p class="block-sub">{esc(first_cmt)}</p></div>'
            f'<div class="block-badges">'
            f'<span class="badge">{n_rungs} Rungs</span>'
            + (f'<span class="badge badge-call">Calls: {", ".join(names.get(c, str(c)) for c in calls)}</span>' if calls else '')
            + '</div></div>',
        ]

        for idx, rg in enumerate(rungs, 1):
            r0 = rg[0]
            first_cell = rows[r0][1]
            if first_cell and first_cell.cls == 'LDComment':
                txt = esc(first_cell.text).replace('\r\n', '\n')
                sec.append(
                    f'<div class="rung rung-comment" id="{esc(bname)}-r{idx}">'
                    f'<div class="rung-num">Rung {idx}</div>'
                    f'<pre class="comment-box">{txt}</pre>'
                    f'</div>'
                )
            else:
                svg = render_rung_svg(rows, rg, calls, tags, names)
                sec.append(
                    f'<div class="rung rung-logic" id="{esc(bname)}-r{idx}">'
                    f'<div class="rung-num">Rung {idx}</div>'
                    f'<div class="rung-body">{svg}</div>'
                    f'</div>'
                )

        # Only Init and FLT_1 have additional rungs in XRef beyond the CObArray header count
        if bname in ('Init', 'FLT_1'):
            for x_rno in sorted(k for k in xref_map if k > len(rungs)):
                ops = xref_map[x_rno]
                chips = ''.join(f'<span class="xref-chip">{esc(op)}</span>' for op in ops)
                sec.append(
                    f'<div class="rung rung-logic" id="{esc(bname)}-r{x_rno}">'
                    f'<div class="rung-num">Rung {x_rno}</div>'
                    f'<div class="rung-body xref-rung">{chips}</div>'
                    f'</div>'
                )

        sec.append('</section>')
        sections.append(''.join(sec))

    # Build Tag Database table
    tag_rows = []
    for tid, info in sorted(tags.items(), key=lambda kv: (kv[1].get('addr') or 'ZZZ', kv[1].get('name') or '')):
        nm = info.get('name', '')
        ad = info.get('addr', '')
        ds = info.get('desc', '')
        if not nm:
            continue
        tag_rows.append(
            f'<tr><td class="t-name">{esc(nm)}</td>'
            f'<td class="t-addr">{esc(ad)}</td>'
            f'<td class="t-desc">{esc(ds)}</td></tr>'
        )

    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>P20890_Angola — GE VersaMax PLC Ladder Program (PME)</title>
<style>
:root {{
  --bg: #f4f6f9;
  --card: #ffffff;
  --ink: #0f172a;
  --muted: #475569;
  --accent: #0284c7;
  --wire: #1e293b;
  --rail: #0f172a;
  --border: #cbd5e1;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background: var(--bg);
  color: var(--ink);
}}
.topbar {{
  position: sticky; top: 0; z-index: 20;
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 20px; background: #0f172a; color: #fff;
  box-shadow: 0 2px 6px rgba(0,0,0,.15);
}}
.topbar h1 {{ margin: 0; font-size: 16px; font-weight: 600; }}
.topbar .controls {{ display: flex; gap: 10px; align-items: center; }}
.topbar input {{
  padding: 6px 10px; border-radius: 5px; border: 1px solid #334155;
  background: #1e293b; color: #fff; width: 240px; font-size: 13px;
}}
.topbar button {{
  padding: 6px 12px; border-radius: 5px; border: none;
  background: var(--accent); color: #fff; cursor: pointer; font-size: 13px; font-weight: 500;
}}
.topbar button:hover {{ opacity: .9; }}
.layout {{ display: flex; min-height: calc(100vh - 48px); }}
.sidebar {{
  width: 230px; flex-shrink: 0; background: #fff;
  border-right: 1px solid var(--border); padding: 12px 8px;
  position: sticky; top: 48px; height: calc(100vh - 48px); overflow-y: auto;
}}
.sidebar h3 {{
  margin: 6px 10px 8px; font-size: 11px; text-transform: uppercase;
  letter-spacing: .06em; color: var(--muted);
}}
.nav-item {{
  display: flex; justify-content: space-between; align-items: center;
  padding: 6px 10px; border-radius: 5px; color: var(--ink);
  text-decoration: none; font-size: 13px; margin-bottom: 2px;
}}
.nav-item:hover {{ background: #e2e8f0; }}
.nav-item .bname {{ font-weight: 600; font-family: Consolas, monospace; }}
.nav-item .bmeta {{ font-size: 11px; color: var(--muted); }}
.content {{ flex: 1; padding: 20px 26px; max-width: 1450px; }}
.proj-summary {{
  background: #fff; border: 1px solid var(--border); border-radius: 8px;
  padding: 16px 20px; margin-bottom: 20px;
}}
.proj-summary h2 {{ margin: 0 0 8px; font-size: 18px; }}
.proj-grid {{
  display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 10px; font-size: 13px; color: var(--muted);
}}
.proj-grid strong {{ color: var(--ink); }}
.block-sec {{
  background: var(--card); border: 1px solid var(--border);
  border-radius: 8px; margin-bottom: 24px; overflow: hidden;
}}
.block-hdr {{
  display: flex; justify-content: space-between; align-items: center;
  padding: 12px 18px; background: #f8fafc; border-bottom: 1px solid var(--border);
}}
.block-hdr h2 {{ margin: 0; font-size: 17px; font-family: Consolas, monospace; color: #0369a1; }}
.block-sub {{ margin: 3px 0 0; font-size: 12.5px; color: var(--muted); }}
.block-badges {{ display: flex; gap: 6px; flex-wrap: wrap; }}
.badge {{
  font-size: 11px; padding: 3px 8px; border-radius: 4px;
  background: #e2e8f0; color: #1e293b; font-weight: 600;
}}
.badge-call {{ background: #dbeafe; color: #1e40af; }}
.rung {{
  display: flex; border-bottom: 1px solid #e2e8f0;
  page-break-inside: avoid; break-inside: avoid;
}}
.rung:last-child {{ border-bottom: none; }}
.rung-num {{
  width: 68px; flex-shrink: 0; padding: 10px 8px;
  font-size: 11px; font-family: Consolas, monospace; color: var(--muted);
  background: #f8fafc; border-right: 1px solid #e2e8f0;
  display: flex; align-items: flex-start; justify-content: center; font-weight: 600;
}}
.rung-body {{ flex: 1; padding: 4px 10px; overflow-x: auto; }}
.comment-box {{
  margin: 0; padding: 10px 14px; flex: 1;
  font-family: Consolas, "Courier New", monospace; font-size: 12px;
  background: #fefce8; color: #713f12; white-space: pre-wrap; line-height: 1.45;
}}
.xref-rung {{
  display: flex; flex-wrap: wrap; gap: 6px; align-items: center; padding: 10px 14px;
}}
.xref-chip {{
  font-family: Consolas, monospace; font-size: 12px;
  background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 4px; padding: 3px 8px;
}}
/* SVG ladder styling */
.ladder-svg .rail {{ stroke: var(--rail); stroke-width: 3; }}
.ladder-svg .wire {{ stroke: var(--wire); stroke-width: 1.8; fill: none; }}
.ladder-svg .wire-data {{ stroke: #0369a1; stroke-width: 1.5; stroke-dasharray: 3,2; }}
.ladder-svg .sym {{ stroke: #0f172a; stroke-width: 2.2; }}
.ladder-svg .cont {{ fill: #0284c7; }}
.ladder-svg .fbox {{ fill: #f8fafc; stroke: #0369a1; stroke-width: 1.8; }}
.ladder-svg .call-rect {{ fill: #eff6ff; stroke: #1d4ed8; cursor: pointer; }}
.ladder-svg .fname {{ font: 700 10.5px Consolas, monospace; fill: #0369a1; text-anchor: middle; }}
.ladder-svg .ftarg {{ font: 700 11px Consolas, monospace; fill: #1d4ed8; text-anchor: middle; text-decoration: underline; }}
.ladder-svg .finst {{ font: 600 9.5px Consolas, monospace; fill: #334155; text-anchor: middle; }}
.ladder-svg .pin-l {{ font: 600 8.5px Consolas, monospace; fill: #64748b; text-anchor: start; }}
.ladder-svg .pin-r {{ font: 600 8.5px Consolas, monospace; fill: #64748b; text-anchor: end; }}
.ladder-svg .addr {{ font: 600 9px Consolas, monospace; fill: #0284c7; text-anchor: middle; }}
.ladder-svg .tag {{ font: 700 9.5px Consolas, monospace; fill: #0f172a; text-anchor: middle; }}
.ladder-svg .desc {{ font: 400 8px -apple-system, Segoe UI, sans-serif; fill: #64748b; text-anchor: middle; }}
.ladder-svg .dval {{ font: 700 9.5px Consolas, monospace; fill: #0f172a; }}
.ladder-svg .coil-ltr {{ font: 700 11px Consolas, monospace; fill: #b91c1c; text-anchor: middle; }}
.el.highlight rect, .el.highlight line, .el.highlight path {{ stroke: #dc2626 !important; stroke-width: 3px !important; }}
.el.highlight text.tag {{ fill: #dc2626 !important; }}
/* Tag table */
.tag-table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
.tag-table th, .tag-table td {{ padding: 6px 10px; border-bottom: 1px solid #e2e8f0; text-align: left; }}
.tag-table th {{ background: #f8fafc; font-weight: 600; position: sticky; top: 0; }}
.t-name {{ font-family: Consolas, monospace; font-weight: 600; color: #0f172a; }}
.t-addr {{ font-family: Consolas, monospace; color: #0284c7; }}
.t-desc {{ color: var(--muted); }}
@media print {{
  @page {{ size: A4 landscape; margin: 8mm; }}
  body {{ background: #fff; }}
  .topbar, .sidebar {{ display: none !important; }}
  .content {{ padding: 0; max-width: none; }}
  .block-sec {{ page-break-before: always; break-before: page; border: 1px solid #94a3b8; margin-bottom: 12px; }}
  .proj-summary {{ page-break-after: always; }}
}}
</style>
</head>
<body>
<div class="topbar">
  <h1>P20890_Angola — GE VersaMax PLC Ladder Program (F&amp;G Angola)</h1>
  <div class="controls">
    <input id="searchBox" type="search" placeholder="Search tag, %I/%Q/%R/%M, comment..." oninput="filterLadder(this.value)"/>
    <button onclick="showAll()">Show All ({len(ordered)} Blocks)</button>
    <button onclick="window.print()">Print / Save PDF</button>
  </div>
</div>
<div class="layout">
  <nav class="sidebar">
    <h3>LD Blocks ({len(ordered)})</h3>
    {''.join(nav_items)}
    <h3>Reference</h3>
    <a class="nav-item" href="#blk-TAGS" onclick="showBlock('TAGS')"><span class="bname">Tag Database</span><span class="bmeta">{len(tag_rows)} tags</span></a>
  </nav>
  <main class="content">
    <div class="proj-summary">
      <h2>Project Overview: P20890_Angola (Fire &amp; Gas System — Angola)</h2>
      <div class="proj-grid">
        <div><strong>Target PLC:</strong> GE Fanuc VersaMax (IC200CPU001)</div>
        <div><strong>Software:</strong> Proficy Machine Edition (saved with build 2425)</div>
        <div><strong>Author:</strong> Vidar Pedersen — Origo-e (Mar–Jun 2003)</div>
        <div><strong>Ladder Blocks:</strong> {len(ordered)} LD blocks ({total_rungs} total rungs)</div>
        <div><strong>Rack 0:</strong> IC200PWR002, IC200CPU001, 3× IC200ALG262 (24 AI), IC200MDL650 (32 DI)</div>
        <div><strong>Rack 1:</strong> IC200PWR002, IC200ERM002, 2× IC200MDL940 (32 Relay DO)</div>
      </div>
    </div>
    {''.join(sections)}
    <section class="block-sec" id="blk-TAGS" data-block="TAGS">
      <div class="block-hdr">
        <div><h2>Variable / Tag Database ({len(tag_rows)} tags)</h2>
        <p class="block-sub">Complete symbol table extracted from P20890_Angola.SwxCF</p></div>
      </div>
      <div style="padding:0 12px 12px">
        <table class="tag-table">
          <thead><tr><th>Tag Name</th><th>PLC Address</th><th>Description</th></tr></thead>
          <tbody>{''.join(tag_rows)}</tbody>
        </table>
      </div>
    </section>
  </main>
</div>
<script>
function showBlock(name) {{
  const el = document.getElementById('blk-' + name);
  if (el) el.scrollIntoView({{behavior: 'smooth', block: 'start'}});
}}
function jumpBlock(name) {{
  showBlock(name);
}}
function showAll() {{
  document.getElementById('searchBox').value = '';
  filterLadder('');
}}
function filterLadder(q) {{
  q = (q || '').trim().toLowerCase();
  document.querySelectorAll('.el').forEach(g => {{
    const t = (g.getAttribute('data-tag') || '').toLowerCase();
    g.classList.toggle('highlight', q.length >= 2 && t.includes(q));
  }});
  document.querySelectorAll('.rung').forEach(r => {{
    if (!q) {{ r.style.display = ''; return; }}
    const txt = r.innerText.toLowerCase() + ' ' + Array.from(r.querySelectorAll('[title]')).map(x => x.textContent.toLowerCase()).join(' ');
    r.style.display = txt.includes(q) ? '' : 'none';
  }});
}}
</script>
</body>
</html>
"""
    with open(out_html, 'w', encoding='utf-8') as f:
        f.write(html_doc)
    print(f'Wrote HTML viewer: {out_html} ({os.path.getsize(out_html):,} bytes)')


if __name__ == '__main__':
    swx = sys.argv[1]
    out_html = sys.argv[2]
    build_html(swx, out_html)
