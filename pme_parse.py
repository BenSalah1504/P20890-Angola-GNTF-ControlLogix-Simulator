"""Read-only parser for GE Proficy Machine Edition (.SwxCF) ladder projects.

Decodes the LD blocks (MFC CArchive serialized grid of ladder elements),
the NameService (symbol id -> name) and the TagData (descriptions/addresses).
"""
import re
import struct
import olefile

WIDTH_DEFAULT = 25


class Obj:
    def __init__(self, cls):
        self.cls = cls
        self.flags = b''

    def __repr__(self):
        d = {k: v for k, v in self.__dict__.items() if k not in ('cls', 'head')}
        return '%s(%s)' % (self.cls, d)


class Reader:
    def __init__(self, data, pos):
        self.d = data
        self.p = pos
        self.classes = {}   # index -> class name
        self.objs = {}      # index -> Obj
        self.idx = 1

    def u8(self):
        v = self.d[self.p]; self.p += 1; return v

    def u16(self):
        v = struct.unpack_from('<H', self.d, self.p)[0]; self.p += 2; return v

    def u32(self):
        v = struct.unpack_from('<I', self.d, self.p)[0]; self.p += 4; return v

    def i32(self):
        v = struct.unpack_from('<i', self.d, self.p)[0]; self.p += 4; return v

    def raw(self, n):
        v = self.d[self.p:self.p + n]; self.p += n; return v

    def cstring(self):
        n = self.u8()
        if n == 0xFF:
            n = self.u16()
            if n == 0xFFFE:   # unicode marker
                raise ValueError('unicode CString at %x' % self.p)
            if n == 0xFFFF:
                n = self.u32()
        return self.raw(n).decode('latin1')

    # ---- operands -------------------------------------------------------
    def operand(self):
        t = self.u16()
        if t == 0xFFFF:
            return None
        if t == 0x0002:
            scope = self.u32(); ident = self.u32()
            return ('var', ident)
        if t == 0xFF0A:            # integer constant + display text
            self.i32(); txt = self.cstring()
            return ('const', txt)
        if t == 0xFF0B:            # real constant (double) + display text
            self.raw(8); txt = self.cstring()
            return ('const', txt)
        if t == 0xFF01:            # array element: base[index]
            base = self.operand(); ix = self.operand()
            return ('index', base, ix)
        raise ValueError('unknown operand type %04x at %x' % (t, self.p - 2))

    # ---- MFC ReadObject -------------------------------------------------
    def read_object(self):
        tag = self.u16()
        if tag == 0x7FFF:
            tag = self.u32() | 0  # big object tag (not expected)
            raise ValueError('big tag')
        if tag == 0:
            return None
        if tag == 0xFFFF:
            self.u16()                       # schema
            n = self.u16()
            name = self.raw(n).decode('latin1')
            self.classes[self.idx] = name
            self.idx += 1
            cls = name
        elif tag & 0x8000:
            ci = tag & 0x7FFF
            if ci not in self.classes:
                raise ValueError('bad class ref %x at %x' % (ci, self.p - 2))
            cls = self.classes[ci]
        else:
            if tag not in self.objs:
                raise ValueError('bad obj ref %x at %x' % (tag, self.p - 2))
            return self.objs[tag]
        o = Obj(cls)
        self.objs[self.idx] = o
        self.idx += 1
        self.read_body(o)
        return o

    def read_body(self, o):
        c = o.cls
        if c == 'CObArray':
            n = self.u16()
            if n == 0xFFFF:
                n = self.u32()
            o.items = [self.read_object() for _ in range(n)]
        elif c == 'LDComment':
            o.flags = self.raw(4)
            self.u16()
            o.lines = self.u16()
            o.text = self.cstring()
        elif c == 'LDCoilContinue':
            return
        elif c.startswith('LDContact') or c.startswith('LDCoil') or c in ('LDDataInput', 'LDDataOutput'):
            o.flags = self.raw(4)
            o.op = self.operand()
        elif c.startswith('LDShunt'):
            o.flags = self.raw(4)
        elif c == 'LDCall':
            o.flags = self.raw(4)
            t = self.u16()
            if t != 0xFF08:
                raise ValueError('LDCall tag %04x at %x' % (t, self.p))
            o.target = self.u16()
        elif c == 'LDFunctionHead':
            o.flags = self.raw(4)
            n = self.u16()
            o.segs = [self.read_object() for _ in range(n)]
            o.b1 = self.u8()
            o.func = self.u32()
            o.b2 = self.u8()
            o.op1 = self.operand()
            o.op2 = self.operand()
        elif c == 'LDFunctionSegment':
            o.flags = self.raw(4)
            o.index = self.u8()
            o.head = self.read_object()
        else:
            raise ValueError('unknown class %s at %x' % (c, self.p))


def parse_block(data):
    """Return (rows, width, call_targets) where rows is list of lists of Obj/None."""
    m = data.find(b'\xff\xff\x00\x00\x08\x00CObArray')
    if m < 0:
        raise ValueError('no CObArray')
    hdr = data[:m]
    calls = [struct.unpack('<I', x.group(1))[0]
             for x in re.finditer(rb'\x16\x00(....)\xff\xff\x32\xff', hdr, re.S)]
    k = hdr.rfind(b'\x81\xff')
    nrows = struct.unpack_from('<I', hdr, k + 2)[0] if k >= 0 else None
    r = Reader(data, m)
    arr = r.read_object()
    items = arr.items
    width = WIDTH_DEFAULT
    if nrows and len(items) % nrows == 0:
        width = len(items) // nrows
    rows = [items[i:i + width] for i in range(0, len(items), width)]
    return rows, width, calls, r.p, len(data)


def load_names(ole):
    d = ole.openstream('Services/C3C42C0D197011D1933100AA005BE7/NameService').read()
    i = 0x12
    names = {}
    while i < len(d):
        n = d[i]
        nm = d[i + 1:i + 1 + n].decode('latin1')
        i += 1 + n
        if i + 13 > len(d):
            break
        ident, sc = struct.unpack_from('<HH', d, i)
        i += 13
        names.setdefault(ident, nm)
    return names


def load_tags(ole):
    """id -> dict(name, desc, addr) parsed from the tag database."""
    d = ole.openstream('Services/67B34FB23E6611D192FE00C0F0143C/TagData').read()
    tags = {}
    starts = [m.start() for m in re.finditer(rb'\x07\x00\x00\x00\xdf\x00\x00\x00', d)]
    for n, s in enumerate(starts):
        end = starts[n + 1] if n + 1 < len(starts) else len(d)
        ident = struct.unpack_from('<I', d, s + 8)[0]
        chunk = d[s:end]
        # length-prefixed strings (DWORD length)
        strs = []
        j = 12
        while j + 4 <= len(chunk):
            ln = struct.unpack_from('<I', chunk, j)[0]
            if 1 <= ln < 400 and j + 4 + ln <= len(chunk):
                s_ = chunk[j + 4:j + 4 + ln]
                if all(32 <= c < 256 and c != 127 for c in s_):
                    strs.append((j, s_.decode('latin1')))
                    j += 4 + ln
                    continue
            j += 1
        name = desc = addr = ''
        for _, s_ in strs:
            if not name:
                name = s_
            elif re.fullmatch(r'%[A-Z]{1,3}\d+', s_):
                if not addr:
                    addr = s_
            elif s_.startswith('$\\'):
                continue
            elif not desc and not addr:
                desc = s_
        if ident not in tags or (not tags[ident]['name']):
            tags[ident] = dict(name=name, desc=desc, addr=addr)
    return tags


def load_project(path):
    ole = olefile.OleFileIO(path)
    names = load_names(ole)
    tags = load_tags(ole)
    order = []
    hdr = ole.openstream('Document 2/LDBlocks/\x06Header').read()
    for m in re.finditer(rb'((?:[\x20-\x7e]\x00)+)\x00\x00', hdr):
        order.append(m.group(1).decode('utf-16-le'))
    blocks = {}
    for e in ole.listdir():
        if len(e) == 4 and e[:2] == ['Document 2', 'LDBlocks'] and e[3] == 'Data':
            blocks[e[2]] = ole.openstream(e).read()
    return names, tags, order, blocks, ole


if __name__ == '__main__':
    import sys
    names, tags, order, blocks, ole = load_project(sys.argv[1])
    print('blocks', order)
    for b, data in blocks.items():
        try:
            rows, w, calls, p, n = parse_block(data)
            print('%-10s rows=%3d width=%d consumed=%d/%d calls=%s' % (b, len(rows), w, p, n, [names.get(c) for c in calls]))
        except Exception as ex:
            print('%-10s ERROR %s' % (b, ex))
