#!/usr/bin/env python
"""
Miscellaneous Routines.
"""
import struct
from sys import maxsize as INF


# PNG Predictor
##
def apply_png_predictor(
    pred, colors, columns, bitspercomponent, data
):
    if bitspercomponent != 8:
        # unsupported
        raise ValueError(
            "Unsupported `bitspercomponent': %d" % bitspercomponent
        )
    nbytes = colors * columns * bitspercomponent // 8
    i = 0
    buf = b""
    line0 = b"\x00" * columns
    for i in range(0, len(data), nbytes + 1):
        ft = data[i: i + 1]
        i += 1
        line1 = data[i: i + nbytes]
        line2 = b""
        if ft == b"\x00":
            # PNG none
            line2 += line1
        elif ft == b"\x01":
            # PNG sub (UNTESTED)
            c = 0
            for b in line1:
                c = (c + b) & 255
                line2 += bytes([c])
        elif ft == b"\x02":
            # PNG up
            for (a, b) in zip(line0, line1):
                c = (a + b) & 255
                line2 += bytes([c])
        elif ft == b"\x03":
            # PNG average (UNTESTED)
            c = 0
            for (a, b) in zip(line0, line1):
                c = ((c + a + b) // 2) & 255
                line2 += bytes([c])
        else:
            # unsupported
            raise ValueError("Unsupported predictor value: %d" % ft)
        buf += line2
        line0 = line2
    return buf


# Matrix operations
##
MATRIX_IDENTITY = (1, 0, 0, 1, 0, 0)


def mult_matrix(m1, m0):
    (a1, b1, c1, d1, e1, f1) = m1
    (a0, b0, c0, d0, e0, f0) = m0
    """Returns the multiplication of two matrices."""
    return (
        a0 * a1 + c0 * b1,
        b0 * a1 + d0 * b1,
        a0 * c1 + c0 * d1,
        b0 * c1 + d0 * d1,
        a0 * e1 + c0 * f1 + e0,
        b0 * e1 + d0 * f1 + f0,
    )


def translate_matrix(m, v):
    """Translates a matrix by (x, y)."""
    (a, b, c, d, e, f) = m
    (x, y) = v
    return (a, b, c, d, x * a + y * c + e, x * b + y * d + f)


def apply_matrix_pt(m, v):
    (a, b, c, d, e, f) = m
    (x, y) = v
    """Applies a matrix to a point."""
    return (a * x + c * y + e, b * x + d * y + f)


def apply_matrix_norm(m, v):
    """Equivalent to apply_matrix_pt(M, (p,q)) - apply_matrix_pt(M, (0,0))"""
    (a, b, c, d, e, f) = m
    (p, q) = v
    return (a * p + c * q, b * p + d * q)


# Utility functions
##

# isnumber
def isnumber(x):
    return isinstance(x, (int, float))


# uniq


def uniq(objs):
    """Eliminates duplicated elements."""
    done = set()
    for obj in objs:
        if obj in done:
            continue
        done.add(obj)
        yield obj
    return


# csort
def csort(objs, key):
    """Order-preserving sorting function."""
    idxs = {obj: i for (i, obj) in enumerate(objs)}
    return sorted(objs, key=lambda obj: (key(obj), idxs[obj]))


# fsplit
def fsplit(pred, objs):
    """Split a list into two classes according to the predicate."""
    t = []
    f = []
    for obj in objs:
        if pred(obj):
            t.append(obj)
        else:
            f.append(obj)
    return (t, f)


# drange
def drange(v0, v1, d):
    """Returns a discrete range."""
    assert v0 < v1
    return range(int(v0) // d, int(v1 + d) // d)


# get_bound
def get_bound(pts):
    """Compute a minimal rectangle that covers all the points."""
    (x0, y0, x1, y1) = (INF, INF, -INF, -INF)
    for (x, y) in pts:
        x0 = min(x0, x)
        y0 = min(y0, y)
        x1 = max(x1, x)
        y1 = max(y1, y)
    return (x0, y0, x1, y1)


# pick
def pick(seq, func, maxobj=None):
    """Picks the object obj where func(obj) has the highest value."""
    maxscore = None
    for obj in seq:
        score = func(obj)
        if maxscore is None or maxscore < score:
            (maxscore, maxobj) = (score, obj)
    return maxobj


# choplist
def choplist(n, seq):
    """Groups every n elements of the list."""
    r = []
    for x in seq:
        r.append(x)
        if len(r) == n:
            yield tuple(r)
            r = []
    return


# nunpack
def nunpack(s, default=0):
    """Unpacks 1 to 4 byte integers (big endian)."""
    length = len(s)
    if not length:
        return default
    elif length == 1:
        return s[0]
    elif length == 2:
        return struct.unpack(">H", s)[0]
    elif length == 3:
        return struct.unpack(">L", b"\x00" + s)[0]
    elif length == 4:
        return struct.unpack(">L", s)[0]
    else:
        raise TypeError("invalid length: %d" % length)


# decode_text
PDFDocEncoding = "".join(
    chr(x)
    for x in (
        0x0000,
        0x0001,
        0x0002,
        0x0003,
        0x0004,
        0x0005,
        0x0006,
        0x0007,
        0x0008,
        0x0009,
        0x000A,
        0x000B,
        0x000C,
        0x000D,
        0x000E,
        0x000F,
        0x0010,
        0x0011,
        0x0012,
        0x0013,
        0x0014,
        0x0015,
        0x0017,
        0x0017,
        0x02D8,
        0x02C7,
        0x02C6,
        0x02D9,
        0x02DD,
        0x02DB,
        0x02DA,
        0x02DC,
        0x0020,
        0x0021,
        0x0022,
        0x0023,
        0x0024,
        0x0025,
        0x0026,
        0x0027,
        0x0028,
        0x0029,
        0x002A,
        0x002B,
        0x002C,
        0x002D,
        0x002E,
        0x002F,
        0x0030,
        0x0031,
        0x0032,
        0x0033,
        0x0034,
        0x0035,
        0x0036,
        0x0037,
        0x0038,
        0x0039,
        0x003A,
        0x003B,
        0x003C,
        0x003D,
        0x003E,
        0x003F,
        0x0040,
        0x0041,
        0x0042,
        0x0043,
        0x0044,
        0x0045,
        0x0046,
        0x0047,
        0x0048,
        0x0049,
        0x004A,
        0x004B,
        0x004C,
        0x004D,
        0x004E,
        0x004F,
        0x0050,
        0x0051,
        0x0052,
        0x0053,
        0x0054,
        0x0055,
        0x0056,
        0x0057,
        0x0058,
        0x0059,
        0x005A,
        0x005B,
        0x005C,
        0x005D,
        0x005E,
        0x005F,
        0x0060,
        0x0061,
        0x0062,
        0x0063,
        0x0064,
        0x0065,
        0x0066,
        0x0067,
        0x0068,
        0x0069,
        0x006A,
        0x006B,
        0x006C,
        0x006D,
        0x006E,
        0x006F,
        0x0070,
        0x0071,
        0x0072,
        0x0073,
        0x0074,
        0x0075,
        0x0076,
        0x0077,
        0x0078,
        0x0079,
        0x007A,
        0x007B,
        0x007C,
        0x007D,
        0x007E,
        0x0000,
        0x2022,
        0x2020,
        0x2021,
        0x2026,
        0x2014,
        0x2013,
        0x0192,
        0x2044,
        0x2039,
        0x203A,
        0x2212,
        0x2030,
        0x201E,
        0x201C,
        0x201D,
        0x2018,
        0x2019,
        0x201A,
        0x2122,
        0xFB01,
        0xFB02,
        0x0141,
        0x0152,
        0x0160,
        0x0178,
        0x017D,
        0x0131,
        0x0142,
        0x0153,
        0x0161,
        0x017E,
        0x0000,
        0x20AC,
        0x00A1,
        0x00A2,
        0x00A3,
        0x00A4,
        0x00A5,
        0x00A6,
        0x00A7,
        0x00A8,
        0x00A9,
        0x00AA,
        0x00AB,
        0x00AC,
        0x0000,
        0x00AE,
        0x00AF,
        0x00B0,
        0x00B1,
        0x00B2,
        0x00B3,
        0x00B4,
        0x00B5,
        0x00B6,
        0x00B7,
        0x00B8,
        0x00B9,
        0x00BA,
        0x00BB,
        0x00BC,
        0x00BD,
        0x00BE,
        0x00BF,
        0x00C0,
        0x00C1,
        0x00C2,
        0x00C3,
        0x00C4,
        0x00C5,
        0x00C6,
        0x00C7,
        0x00C8,
        0x00C9,
        0x00CA,
        0x00CB,
        0x00CC,
        0x00CD,
        0x00CE,
        0x00CF,
        0x00D0,
        0x00D1,
        0x00D2,
        0x00D3,
        0x00D4,
        0x00D5,
        0x00D6,
        0x00D7,
        0x00D8,
        0x00D9,
        0x00DA,
        0x00DB,
        0x00DC,
        0x00DD,
        0x00DE,
        0x00DF,
        0x00E0,
        0x00E1,
        0x00E2,
        0x00E3,
        0x00E4,
        0x00E5,
        0x00E6,
        0x00E7,
        0x00E8,
        0x00E9,
        0x00EA,
        0x00EB,
        0x00EC,
        0x00ED,
        0x00EE,
        0x00EF,
        0x00F0,
        0x00F1,
        0x00F2,
        0x00F3,
        0x00F4,
        0x00F5,
        0x00F6,
        0x00F7,
        0x00F8,
        0x00F9,
        0x00FA,
        0x00FB,
        0x00FC,
        0x00FD,
        0x00FE,
        0x00FF,
    )
)


def decode_text(s):
    """Decodes a PDFDocEncoding bytes to Unicode."""
    if s.startswith(b"\xfe\xff"):
        return s[2:].decode("utf-16be", "ignore")
    else:
        return "".join(PDFDocEncoding[c] for c in s)


def q(s):
    """Quotes html string."""
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def bbox2str(bbox):
    (x0, y0, x1, y1) = bbox
    return "%.3f,%.3f,%.3f,%.3f" % (x0, y0, x1, y1)


def matrix2str(m):
    (a, b, c, d, e, f) = m
    return "[%.2f,%.2f,%.2f,%.2f, (%.2f,%.2f)]" % (a, b, c, d, e, f)


# Plane
##
# A set-like data structure for objects placed on a plane.
# Can efficiently find objects in a certain rectangular area.
# It maintains two parallel lists of objects, each of
# which is sorted by its x or y coordinate.
##
class Plane:
    def __init__(self, bbox, gridsize=50):
        self._seq = []  # preserve the object order.
        self._objs = set()
        self._grid = {}
        self.gridsize = gridsize
        (self.x0, self.y0, self.x1, self.y1) = bbox
        return

    def __repr__(self):
        return "<Plane objs=%r>" % list(self)

    def __iter__(self):
        return (obj for obj in self._seq if obj in self._objs)

    def __len__(self):
        return len(self._objs)

    def __contains__(self, obj):
        return obj in self._objs

    def _getrange(self, bbox):
        (x0, y0, x1, y1) = bbox
        if (
            x1 <= self.x0
            or self.x1 <= x0
            or y1 <= self.y0
            or self.y1 <= y0
        ):
            return
        x0 = max(self.x0, x0)
        y0 = max(self.y0, y0)
        x1 = min(self.x1, x1)
        y1 = min(self.y1, y1)
        for y in drange(y0, y1, self.gridsize):
            for x in drange(x0, x1, self.gridsize):
                yield (x, y)
        return

    # extend(objs)
    def extend(self, objs):
        for obj in objs:
            self.add(obj)
        return

    # add(obj): place an object.
    def add(self, obj):
        for k in self._getrange((obj.x0, obj.y0, obj.x1, obj.y1)):
            if k not in self._grid:
                r = []
                self._grid[k] = r
            else:
                r = self._grid[k]
            r.append(obj)
        self._seq.append(obj)
        self._objs.add(obj)
        return

    # remove(obj): displace an object.
    def remove(self, obj):
        for k in self._getrange((obj.x0, obj.y0, obj.x1, obj.y1)):
            try:
                self._grid[k].remove(obj)
            except (KeyError, ValueError):
                pass
        self._objs.remove(obj)
        return

    # find(): finds objects that are in a certain area.
    def find(self, bbox):
        (x0, y0, x1, y1) = bbox
        done = set()
        for k in self._getrange(bbox):
            if k not in self._grid:
                continue
            for obj in self._grid[k]:
                if obj in done:
                    continue
                done.add(obj)
                if (
                    obj.x1 <= x0
                    or x1 <= obj.x0
                    or obj.y1 <= y0
                    or y1 <= obj.y0
                ):
                    continue
                yield obj
        return
