"""Leitor de .pak do Unreal Engine 4.26/4.27 (versão 11, zlib, sem criptografia) e gravador de pak de patch."""
import hashlib, struct, zlib

MAGIC = 0x5A6F12E1


def _rstr(b, p):
    n, = struct.unpack_from('<i', b, p)
    p += 4
    if n < 0:
        return b[p:p - 2 * n].decode('utf-16le').rstrip('\0'), p - 2 * n
    return b[p:p + n].rstrip(b'\0').decode('latin1'), p + n


def fstring(s):
    if s == '':
        return struct.pack('<i', 0)
    try:
        b = s.encode('ascii')
        return struct.pack('<i', len(b) + 1) + b + b'\0'
    except UnicodeEncodeError:
        return struct.pack('<i', -(len(s) + 1)) + s.encode('utf-16le') + b'\0\0'


class Pak:
    def __init__(self, path, base=0, size=None):
        self.f = open(path, 'rb')
        self.base = base
        if size is None:
            self.f.seek(0, 2)
            size = self.f.tell()
        self.f.seek(base + size - 221)
        foot = self.f.read(221)
        enc, magic, ver, ioff, isz = struct.unpack_from('<BIIQQ', foot, 16)
        if magic != MAGIC or ver != 11 or enc:
            raise SystemExit(f'{path}: pak não reconhecido (magic {magic:#x}, versão {ver})')
        self.methods = [None] + [foot[61 + i * 32:93 + i * 32].rstrip(b'\0').decode() for i in range(5)]
        b = self._at(ioff, isz)
        self.mount, p = _rstr(b, 0)
        n, self.seed, has = struct.unpack_from('<iQi', b, p)
        p += 16
        if has:
            p += 36
        has, = struct.unpack_from('<i', b, p)
        p += 4
        assert has, 'pak sem índice de diretórios'
        doff, dsz = struct.unpack_from('<qq', b, p)
        p += 36
        esz, = struct.unpack_from('<i', b, p)
        self.enc = b[p + 4:p + 4 + esz]
        d = self._at(doff, dsz)
        self.entries = {}
        nd, = struct.unpack_from('<i', d, 0)
        p = 4
        for _ in range(nd):
            dn, p = _rstr(d, p)
            nf, = struct.unpack_from('<i', d, p)
            p += 4
            for _ in range(nf):
                fn, p = _rstr(d, p)
                o, = struct.unpack_from('<i', d, p)
                p += 4
                self.entries[(dn + fn).lstrip('/')] = o

    def _at(self, off, n):
        self.f.seek(self.base + off)
        return self.f.read(n)

    def info(self, name):
        """(deslocamento, tamanho, método, [tamanhos dos blocos], tamanho do bloco)"""
        e, p = self.enc, self.entries[name]
        assert p >= 0
        fl, = struct.unpack_from('<I', e, p)
        p += 4
        bs = (fl & 0x3f) << 11
        if (fl & 0x3f) == 0x3f:
            bs, = struct.unpack_from('<I', e, p)
            p += 4
        nb, encr, cm = (fl >> 6) & 0xffff, (fl >> 22) & 1, (fl >> 23) & 0x3f
        assert not encr

        def num(bit):
            nonlocal p
            if fl & bit:
                v, = struct.unpack_from('<I', e, p)
                p += 4
            else:
                v, = struct.unpack_from('<Q', e, p)
                p += 8
            return v
        off = num(1 << 31)
        usz = num(1 << 30)
        csz = num(1 << 29) if cm else usz
        if nb == 1:
            blocks = [csz]
        else:
            blocks = list(struct.unpack_from(f'<{nb}I', e, p))
        return off, usz, cm, blocks, bs

    def read(self, name):
        if name not in self.entries:
            raise SystemExit(f'não encontrei {name} no pak')
        off, usz, cm, blocks, bs = self.info(name)
        if not cm:
            return self._at(off + 53, usz)
        assert self.methods[cm] == 'Zlib', self.methods[cm]
        p = off + 53 + 4 + 16 * len(blocks)
        d = b''
        for n in blocks:
            d += zlib.decompress(self._at(p, n))
            p += n
        assert len(d) == usz
        return d


def _record(off, data):
    return (struct.pack('<qqqi', off, len(data), len(data), 0) + hashlib.sha1(data).digest()
            + struct.pack('<BI', 0, 0))


def write(files, dst, mount='../../../'):
    """Grava um pak sem compressão (formato da versão 4, que o motor ainda lê) com a lista [(nome, bytes)]."""
    body = b''
    idx = fstring(mount) + struct.pack('<i', len(files))
    for name, data in files:
        idx += fstring(name) + _record(len(body), data)
        body += _record(0, data) + data
    foot = struct.pack('<IIqq', MAGIC, 4, len(body), len(idx)) + hashlib.sha1(idx).digest()
    with open(dst, 'wb') as f:
        f.write(body + idx + foot)
