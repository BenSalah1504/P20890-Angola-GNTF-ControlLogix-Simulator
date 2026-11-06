"""Render the decoded GE Proficy Machine Edition (.SwxCF) ladder logic program
directly to a vector PDF using ReportLab (A4 Landscape, bookmarks for all 24
blocks + tag table).
"""
import os
import sys
import textwrap

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas

import export_ladder as E
import pme_parse as P

PAGE_W, PAGE_H = landscape(A4)  # 841.89 x 595.27 pt
MARGIN_X = 24
MARGIN_TOP = 36
MARGIN_BOT = 26


def draw_header_footer(c, title, page_no):
    c.saveState()
    c.setFillColor(colors.HexColor('#0f172a'))
    c.rect(0, PAGE_H - 24, PAGE_W, 24, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont('Helvetica-Bold', 9.5)
    c.drawString(MARGIN_X, PAGE_H - 16, 'P20890_Angola — GE VersaMax PLC Ladder Program (Proficy Machine Edition)')
    c.setFont('Helvetica', 9)
    c.drawRightString(PAGE_W - MARGIN_X, PAGE_H - 16, title)

    c.setStrokeColor(colors.HexColor('#cbd5e1'))
    c.setLineWidth(0.5)
    c.line(MARGIN_X, MARGIN_BOT - 6, PAGE_W - MARGIN_X, MARGIN_BOT - 6)
    c.setFillColor(colors.HexColor('#64748b'))
    c.setFont('Helvetica', 8)
    c.drawString(MARGIN_X, MARGIN_BOT - 16, 'Source: P20890_Angola.SwxCF  |  Target: VersaMax IC200CPU001  |  Author: Vidar Pedersen (Origo-e, 2003)')
    c.drawRightString(PAGE_W - MARGIN_X, MARGIN_BOT - 16, f'Page {page_no}')
    c.restoreState()


def draw_rung_pdf(c, x_left, y_top, avail_w, rows, rg, calls, tags, names):
    """Draw a logic rung at (x_left, y_top) downwards and return height used."""
    max_col = max((col for r in rg for col, e in enumerate(rows[r]) if e), default=10)
    ncols = max(max_col, 10)
    cw = min(64.0, (avail_w - 20.0) / ncols)
    ch = 44.0
    wy_off = 21.0
    rail_l = x_left + 8.0
    rail_r = rail_l + ncols * cw
    total_h = len(rg) * ch + 6.0

    c.saveState()
    # Power rails
    c.setStrokeColor(colors.HexColor('#0f172a'))
    c.setLineWidth(1.8)
    c.line(rail_l, y_top - 2, rail_l, y_top - total_h + 2)
    c.line(rail_r, y_top - 2, rail_r, y_top - total_h + 2)

    for ri, r in enumerate(rg):
        ry_top = y_top - ri * ch - 2
        wy = ry_top - wy_off
        ry_bot = ry_top - ch
        row = rows[r]

        for col in range(1, ncols + 1):
            e = row[col] if col < len(row) else None
            if not e:
                continue
            x0 = rail_l + (col - 1) * cw
            xc = x0 + cw / 2.0
            x1 = x0 + cw
            fl = e.flags[0] if e.flags else 0
            has_l = bool(fl & 1)
            has_u = bool(fl & 2)
            has_r = bool(fl & 4)
            has_d = bool(fl & 8)
            cls = e.cls

            c.setStrokeColor(colors.HexColor('#1e293b'))
            c.setLineWidth(1.1)

            if cls in ('LDShunt', 'LDShuntVert'):
                if has_l or has_r:
                    c.line(x0, wy, x1, wy)
                if has_u:
                    c.line(x1, ry_top, x1, wy)
                if has_d:
                    c.line(x1, wy, x1, ry_bot)
                continue

            if cls == 'LDShuntHorz':
                c.line(x0, wy, x1, wy)
                if has_u:
                    c.line(x1, ry_top, x1, wy)
                if has_d:
                    c.line(x1, wy, x1, ry_bot)
                continue

            if cls in ('LDContactNO', 'LDContactNC', 'LDContactContinue'):
                if has_u:
                    c.line(x1, ry_top, x1, wy)
                if has_d:
                    c.line(x1, wy, x1, ry_bot)

            if cls in ('LDContactNO', 'LDContactNC'):
                nm, ad, ds, _ = E.fmt_op(e.op, tags, names)
                c.line(x0, wy, xc - 7, wy)
                if has_r:
                    c.line(xc + 7, wy, x1, wy)
                c.setLineWidth(1.4)
                c.line(xc - 7, wy - 7, xc - 7, wy + 7)
                c.line(xc + 7, wy - 7, xc + 7, wy + 7)
                if cls == 'LDContactNC':
                    c.line(xc - 5, wy - 5, xc + 5, wy + 5)
                if ad:
                    c.setFillColor(colors.HexColor('#0284c7'))
                    c.setFont('Courier-Bold', 5.8)
                    c.drawCentredString(xc, wy + 9, E.trunc(ad, 14))
                c.setFillColor(colors.HexColor('#0f172a'))
                c.setFont('Courier-Bold', 5.8)
                c.drawCentredString(xc, wy - 14, E.trunc(nm, 16))
                if ds:
                    c.setFillColor(colors.HexColor('#64748b'))
                    c.setFont('Helvetica', 5.0)
                    c.drawCentredString(xc, wy - 20, E.trunc(ds, 20))

            elif cls == 'LDContactContinue':
                c.line(xc, wy, x1, wy)
                c.setFillColor(colors.HexColor('#0284c7'))
                c.setFont('Courier-Bold', 6)
                c.drawCentredString(xc - 4, wy - 2, 'CONT>')

            elif cls == 'LDCoilContinue':
                c.line(x0, wy, xc, wy)
                c.setFillColor(colors.HexColor('#0284c7'))
                c.setFont('Courier-Bold', 6)
                c.drawCentredString(xc + 6, wy - 2, '>CONT')

            elif cls.startswith('LDCoil'):
                nm, ad, ds, _ = E.fmt_op(e.op, tags, names)
                c.line(x0, wy, xc - 8, wy)
                c.line(xc + 8, wy, x1, wy)
                c.setLineWidth(1.3)
                c.circle(xc, wy, 7.5, stroke=1, fill=0)
                ltr = {
                    'LDCoilNC': '/',
                    'LDCoilSet': 'S',
                    'LDCoilReset': 'R',
                    'LDCoilPtrans': 'P',
                }.get(cls, '')
                if ltr:
                    c.setFillColor(colors.HexColor('#b91c1c'))
                    c.setFont('Courier-Bold', 7)
                    c.drawCentredString(xc, wy - 2.5, ltr)
                if ad:
                    c.setFillColor(colors.HexColor('#0284c7'))
                    c.setFont('Courier-Bold', 5.8)
                    c.drawCentredString(xc, wy + 9, E.trunc(ad, 14))
                c.setFillColor(colors.HexColor('#0f172a'))
                c.setFont('Courier-Bold', 5.8)
                c.drawCentredString(xc, wy - 14, E.trunc(nm, 16))
                if ds:
                    c.setFillColor(colors.HexColor('#64748b'))
                    c.setFont('Helvetica', 5.0)
                    c.drawCentredString(xc, wy - 20, E.trunc(ds, 20))

            elif cls == 'LDCall':
                t_id = calls[e.target] if e.target < len(calls) else e.target
                t_nm = names.get(t_id, f'Block_{t_id}')
                c.line(x0, wy, x0 + 6, wy)
                if has_r:
                    c.line(x1 - 6, wy, x1, wy)
                c.setFillColor(colors.HexColor('#eff6ff'))
                c.setStrokeColor(colors.HexColor('#1d4ed8'))
                c.roundRect(x0 + 6, wy - 10, cw - 12, 20, 3, stroke=1, fill=1)
                c.setFillColor(colors.HexColor('#1d4ed8'))
                c.setFont('Courier-Bold', 6.2)
                c.drawCentredString(xc, wy + 2, 'CALL')
                c.setFont('Courier-Bold', 6.8)
                c.drawCentredString(xc, wy - 6, t_nm)

            elif cls in ('LDDataInput', 'LDDataOutput'):
                nm, ad, _, _ = E.fmt_op(e.op, tags, names)
                c.setStrokeColor(colors.HexColor('#0369a1'))
                c.setLineWidth(0.9)
                if cls == 'LDDataInput':
                    c.line(x1 - 10, wy, x1, wy)
                    c.setFillColor(colors.HexColor('#0f172a'))
                    c.setFont('Courier-Bold', 5.8)
                    c.drawRightString(x1 - 12, wy - 2, E.trunc(nm, 15))
                    if ad and ad != 'CONST':
                        c.setFillColor(colors.HexColor('#0284c7'))
                        c.setFont('Courier', 5.3)
                        c.drawRightString(x1 - 12, wy + 5, ad)
                else:
                    c.line(x0, wy, x0 + 10, wy)
                    c.setFillColor(colors.HexColor('#0f172a'))
                    c.setFont('Courier-Bold', 5.8)
                    c.drawString(x0 + 12, wy - 2, E.trunc(nm, 15))
                    if ad and ad != 'CONST':
                        c.setFillColor(colors.HexColor('#0284c7'))
                        c.setFont('Courier', 5.3)
                        c.drawString(x0 + 12, wy + 5, ad)

            elif cls == 'LDFunctionHead':
                fnm, in_pins, out_pins = E.FUNC_INFO.get(e.func, (f'FUNC_{e.func}', [], []))
                nsegs = len(e.segs)
                bh = (nsegs + 1) * ch - 10.0
                by_top = ry_top - 5.0
                by_bot = by_top - bh
                bx = x0 + 5.0
                bw = cw - 10.0
                c.line(x0, wy, bx, wy)
                if has_r or (col + 1 < len(row) and row[col + 1] is not None):
                    c.line(bx + bw, wy, x1, wy)
                for si in range(1, nsegs + 1):
                    if ri + si < len(rg):
                        r_s = rg[ri + si]
                        wy_s = y_top - (ri + si) * ch - 2 - wy_off
                        left_e = rows[r_s][col - 1] if col - 1 >= 0 else None
                        if left_e and left_e.cls not in ('LDDataInput',):
                            c.line(x0, wy_s, bx, wy_s)
                c.setFillColor(colors.HexColor('#f8fafc'))
                c.setStrokeColor(colors.HexColor('#0369a1'))
                c.setLineWidth(1.2)
                c.roundRect(bx, by_bot, bw, bh, 3, stroke=1, fill=1)
                c.setFillColor(colors.HexColor('#0369a1'))
                c.setFont('Courier-Bold', 6.0)
                c.drawCentredString(xc, by_top - 10, E.trunc(fnm, 13))
                if e.op1:
                    p1, a1, _, _ = E.fmt_op(e.op1, tags, names)
                    c.setFillColor(colors.HexColor('#334155'))
                    c.setFont('Courier-Bold', 5.5)
                    c.drawCentredString(xc, by_top - 19, E.trunc(p1, 13))
                    if a1:
                        c.setFillColor(colors.HexColor('#0284c7'))
                        c.setFont('Courier', 5.2)
                        c.drawCentredString(xc, by_top - 26, a1)
                elif e.op2:
                    p2, _, _, _ = E.fmt_op(e.op2, tags, names)
                    c.setFillColor(colors.HexColor('#334155'))
                    c.setFont('Courier', 5.5)
                    c.drawCentredString(xc, by_top - 19, f'LEN={p2}')
                c.setFillColor(colors.HexColor('#64748b'))
                c.setFont('Courier', 5.0)
                for pi, pl in enumerate(in_pins):
                    if pl:
                        py = y_top - (ri + pi) * ch - 2 - wy_off - 2
                        c.drawString(bx + 2, py, pl)
                for pi, pl in enumerate(out_pins):
                    if pl:
                        py = y_top - (ri + pi) * ch - 2 - wy_off - 2
                        c.drawRightString(bx + bw - 2, py, pl)

    c.restoreState()
    return total_h


def build_pdf(swxcf_path, out_pdf):
    names, tags, _, blocks_raw, ole = P.load_project(swxcf_path)
    ordered = [b for b in E.LOGICAL_ORDER if b in blocks_raw] + [
        b for b in sorted(blocks_raw) if b not in E.LOGICAL_ORDER
    ]

    c = canvas.Canvas(out_pdf, pagesize=landscape(A4))
    c.setTitle('P20890_Angola — GE VersaMax PLC Ladder Program')
    c.setAuthor('Vidar Pedersen (Origo-e, 2003)')
    page_no = 1

    # Cover / Summary page
    draw_header_footer(c, 'Project Summary & Block Index', page_no)
    c.bookmarkPage('COVER')
    c.addOutlineEntry('Project Summary & Hardware', 'COVER', level=0)

    y = PAGE_H - MARGIN_TOP - 10
    c.setFillColor(colors.HexColor('#0f172a'))
    c.setFont('Helvetica-Bold', 16)
    c.drawString(MARGIN_X, y, 'P20890_Angola — Fire & Gas PLC Ladder Program')
    y -= 18
    c.setFont('Helvetica', 10)
    c.setFillColor(colors.HexColor('#334155'))
    c.drawString(MARGIN_X, y, 'Target: GE Fanuc VersaMax PLC (IC200CPU001)   |   HMI: QuickPanel (Target 2)   |   Saved with PME Build 2425')
    y -= 22

    # Hardware summary box
    c.setFillColor(colors.HexColor('#f8fafc'))
    c.setStrokeColor(colors.HexColor('#cbd5e1'))
    c.roundRect(MARGIN_X, y - 62, PAGE_W - 2 * MARGIN_X, 62, 4, stroke=1, fill=1)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.setFont('Helvetica-Bold', 9.5)
    c.drawString(MARGIN_X + 10, y - 15, 'Hardware Configuration (from Hardware.hwcfg):')
    c.setFont('Courier', 8.5)
    c.drawString(MARGIN_X + 10, y - 30, 'Rack 0 (IC200RAC001): PWR IC200PWR002 | CPU IC200CPU001 | Slot 3-5: 3x IC200ALG262 (8AI %AI0001-%AI0024) | Slot 6: IC200MDL650 (32DI %I0001-%I0032)')
    c.drawString(MARGIN_X + 10, y - 44, 'Rack 1 (IC200RAC001): PWR IC200PWR002 | Exp Receiver IC200ERM002 | Slot 2-3: 2x IC200MDL940 (16 Relay DO %Q0001-%Q0032)')
    c.drawString(MARGIN_X + 10, y - 56, 'Program Execution Flow: _MAIN -> Init (1st scan), Input (DI_1, DI_2, AI_1, AI_2, AI_3, Vote_1), Logic (CE_LOG, Sound), Output (Indicat, Shutdow, Protect, Loc_Al, FLT_1)')
    y -= 80

    # Block index table on cover
    c.setFont('Helvetica-Bold', 10.5)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawString(MARGIN_X, y, f'Ladder Diagram Blocks ({len(ordered)} Blocks):')
    y -= 14

    c.setFont('Courier-Bold', 8)
    c.setFillColor(colors.HexColor('#0369a1'))
    c.drawString(MARGIN_X, y, f'{"Block":<10} {"Rungs":<7} {"Subroutine Calls":<36} Description')
    y -= 4
    c.line(MARGIN_X, y, PAGE_W - MARGIN_X, y)
    y -= 11

    c.setFont('Courier', 8)
    for bname in ordered:
        rows, _, calls, _, _ = P.parse_block(blocks_raw[bname])
        rungs = E.split_rungs(rows)
        xref_map = E.parse_xref_rungs(ole, bname, tags, names)
        nr = max(len(rungs), max(xref_map) if xref_map else 0)
        cstr = ', '.join(names.get(x, str(x)) for x in calls)
        desc = ''
        if rungs and rows[rungs[0][0]][1] and rows[rungs[0][0]][1].cls == 'LDComment':
            desc = rows[rungs[0][0]][1].text.strip().splitlines()[0]
        c.setFillColor(colors.HexColor('#0f172a'))
        c.drawString(MARGIN_X, y, f'{bname:<10} {nr:<7d} {E.trunc(cstr, 34):<36} {E.trunc(desc, 75)}')
        y -= 12

    c.showPage()
    page_no += 1

    # Render each block
    for bname in ordered:
        data = blocks_raw[bname]
        rows, _, calls, _, _ = P.parse_block(data)
        rungs = E.split_rungs(rows)
        xref_map = E.parse_xref_rungs(ole, bname, tags, names)
        n_rungs = max(len(rungs), max(xref_map) if xref_map else 0)

        draw_header_footer(c, f'Block: {bname} ({n_rungs} rungs)', page_no)
        bm = f'BLK_{bname}'
        c.bookmarkPage(bm)
        c.addOutlineEntry(f'{bname} ({n_rungs} rungs)', bm, level=0)

        y = PAGE_H - MARGIN_TOP
        # Block banner
        c.setFillColor(colors.HexColor('#e0f2fe'))
        c.setStrokeColor(colors.HexColor('#0284c7'))
        c.roundRect(MARGIN_X, y - 22, PAGE_W - 2 * MARGIN_X, 22, 3, stroke=1, fill=1)
        c.setFillColor(colors.HexColor('#0369a1'))
        c.setFont('Courier-Bold', 11)
        c.drawString(MARGIN_X + 8, y - 15, f'LD BLOCK: {bname}')
        if calls:
            c.setFont('Helvetica-Bold', 8.5)
            c.drawRightString(PAGE_W - MARGIN_X - 8, y - 15, 'Calls: ' + ', '.join(names.get(x, str(x)) for x in calls))
        y -= 28

        avail_w = PAGE_W - 2 * MARGIN_X - 42

        for idx, rg in enumerate(rungs, 1):
            r0 = rg[0]
            first_cell = rows[r0][1]
            if first_cell and first_cell.cls == 'LDComment':
                raw_lines = first_cell.text.replace('\r\n', '\n').splitlines() or ['']
                wrapped = []
                for ln in raw_lines:
                    wrapped.extend(textwrap.wrap(ln, width=122) or [''])
                h_need = len(wrapped) * 9.5 + 10
                if y - h_need < MARGIN_BOT + 6:
                    c.showPage()
                    page_no += 1
                    draw_header_footer(c, f'Block: {bname} (cont.)', page_no)
                    y = PAGE_H - MARGIN_TOP
                c.setFillColor(colors.HexColor('#fefce8'))
                c.setStrokeColor(colors.HexColor('#fde047'))
                c.rect(MARGIN_X + 42, y - h_need, avail_w, h_need, stroke=1, fill=1)
                c.setFillColor(colors.HexColor('#64748b'))
                c.setFont('Courier-Bold', 7.5)
                c.drawString(MARGIN_X + 2, y - 11, f'Rung {idx}')
                c.setFillColor(colors.HexColor('#713f12'))
                c.setFont('Courier', 7.5)
                ty = y - 10
                for wln in wrapped:
                    c.drawString(MARGIN_X + 48, ty, wln)
                    ty -= 9.5
                y -= h_need + 4
            else:
                h_need = len(rg) * 44.0 + 8.0
                if y - h_need < MARGIN_BOT + 6 and (y < PAGE_H - MARGIN_TOP - 30):
                    c.showPage()
                    page_no += 1
                    draw_header_footer(c, f'Block: {bname} (cont.)', page_no)
                    y = PAGE_H - MARGIN_TOP
                # If a single rung is taller than one page (e.g. Vote_1 17-row continuation rung),
                # split rg into chunks of at most 11 rows per page.
                max_rows_per_page = 11
                for chunk_start in range(0, len(rg), max_rows_per_page):
                    sub_rg = rg[chunk_start:chunk_start + max_rows_per_page]
                    sub_h = len(sub_rg) * 44.0 + 8.0
                    if y - sub_h < MARGIN_BOT + 6 and (y < PAGE_H - MARGIN_TOP - 30):
                        c.showPage()
                        page_no += 1
                        draw_header_footer(c, f'Block: {bname} (cont.)', page_no)
                        y = PAGE_H - MARGIN_TOP
                    c.setStrokeColor(colors.HexColor('#e2e8f0'))
                    c.setLineWidth(0.5)
                    c.rect(MARGIN_X, y - sub_h, PAGE_W - 2 * MARGIN_X, sub_h, stroke=1, fill=0)
                    c.setFillColor(colors.HexColor('#475569'))
                    c.setFont('Courier-Bold', 7.5)
                    lbl = f'Rung {idx}' if chunk_start == 0 else f'Rung {idx} (cont.)'
                    c.drawString(MARGIN_X + 4, y - 16, lbl)
                    draw_rung_pdf(c, MARGIN_X + 42, y, avail_w, rows, sub_rg, calls, tags, names)
                    y -= sub_h + 3

        # Additional XRef rungs (only for Init and FLT_1)
        if bname in ('Init', 'FLT_1'):
            for x_rno in sorted(k for k in xref_map if k > len(rungs)):
                ops_str = '   |   '.join(xref_map[x_rno])
                wrapped = textwrap.wrap(ops_str, width=118) or ['']
                h_need = len(wrapped) * 10 + 10
                if y - h_need < MARGIN_BOT + 6:
                    c.showPage()
                    page_no += 1
                    draw_header_footer(c, f'Block: {bname} (cont.)', page_no)
                    y = PAGE_H - MARGIN_TOP
                c.setFillColor(colors.HexColor('#f8fafc'))
                c.setStrokeColor(colors.HexColor('#cbd5e1'))
                c.rect(MARGIN_X, y - h_need, PAGE_W - 2 * MARGIN_X, h_need, stroke=1, fill=1)
                c.setFillColor(colors.HexColor('#475569'))
                c.setFont('Courier-Bold', 7.5)
                c.drawString(MARGIN_X + 4, y - 12, f'Rung {x_rno}')
                c.setFillColor(colors.HexColor('#0f172a'))
                c.setFont('Courier', 7.5)
                ty = y - 12
                for wln in wrapped:
                    c.drawString(MARGIN_X + 48, ty, wln)
                    ty -= 10
                y -= h_need + 3

        c.showPage()
        page_no += 1

    # Tag Database section
    draw_header_footer(c, 'Tag Database', page_no)
    c.bookmarkPage('TAGS')
    c.addOutlineEntry('Variable / Tag Database', 'TAGS', level=0)
    y = PAGE_H - MARGIN_TOP
    c.setFont('Helvetica-Bold', 12)
    c.setFillColor(colors.HexColor('#0f172a'))
    c.drawString(MARGIN_X, y, f'PLC Variable / Tag Database ({len(tags)} tags)')
    y -= 16

    def draw_tag_hdr(y_pos):
        c.setFillColor(colors.HexColor('#e2e8f0'))
        c.rect(MARGIN_X, y_pos - 12, PAGE_W - 2 * MARGIN_X, 14, stroke=0, fill=1)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.setFont('Courier-Bold', 8)
        c.drawString(MARGIN_X + 4, y_pos - 9, f'{"Tag Name":<28} {"Address":<12} Description')
        return y_pos - 18

    y = draw_tag_hdr(y)
    for _, info in sorted(tags.items(), key=lambda kv: (kv[1].get('addr') or 'ZZZ', kv[1].get('name') or '')):
        nm = info.get('name', '')
        if not nm:
            continue
        ad = info.get('addr', '')
        ds = info.get('desc', '')
        if y < MARGIN_BOT + 12:
            c.showPage()
            page_no += 1
            draw_header_footer(c, 'Tag Database (cont.)', page_no)
            y = draw_tag_hdr(PAGE_H - MARGIN_TOP)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.setFont('Courier-Bold', 7.5)
        c.drawString(MARGIN_X + 4, y, f'{nm:<28}')
        c.setFillColor(colors.HexColor('#0284c7'))
        c.drawString(MARGIN_X + 4 + 28 * 4.5, y, f'{ad:<12}')
        c.setFillColor(colors.HexColor('#334155'))
        c.setFont('Helvetica', 7.5)
        c.drawString(MARGIN_X + 4 + 40 * 4.5, y, E.trunc(ds, 110))
        y -= 10.5

    c.save()
    print(f'Wrote PDF: {out_pdf} ({os.path.getsize(out_pdf):,} bytes, {page_no} pages)')


if __name__ == '__main__':
    build_pdf(sys.argv[1], sys.argv[2])
