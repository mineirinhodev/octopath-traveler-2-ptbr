"""Regras do texto: tipos de fala, quebra de linha na largura da caixa, itálico. 'g' = GameText, 't' = TalkData."""
import re, struct
import tabela

W, CAP = 50, 3
TAG = re.compile(r'<[^>]*>')
IT = '<span style="italic">'
SYM = re.compile('[←-⇿①-⓿☀-➿㌀-㏿®©]')


def falantes(ua, ue):
    """{linha da TalkData: nome interno de quem fala}"""
    names, _ = tabela._names(ua)
    out, p = {}, 0

    def name():
        nonlocal p
        i, num = struct.unpack_from('<II', ue, p)
        p += 8
        return names[i] + (f'_{num - 1}' if num else '')

    def props(row):
        nonlocal p
        while True:
            nm = name()
            if nm == 'None':
                return
            ty = name()
            size, = struct.unpack_from('<i', ue, p)
            p += 8
            if ty == 'StructProperty':
                p += 24
            elif ty == 'BoolProperty':
                p += 1
            elif ty in ('ByteProperty', 'EnumProperty', 'ArrayProperty'):
                p += 8
            p += 1
            if row and nm == 'Names' and struct.unpack_from('<i', ue, p)[0] >= 1:
                i, num = struct.unpack_from('<II', ue, p + 4)
                out[row] = names[i] + (f'_{num - 1}' if num else '')
            p += size
    props(None)
    n, = struct.unpack_from('<i', ue, p + 4)
    p += 8
    for _ in range(n):
        props(name())
    return out


def vlen(s):
    return len(TAG.sub('', s))


def kind(t, s):
    """'D' fala (requebra), 'L' mantém as linhas."""
    if t == 'g':
        return 'L'
    ls = s.split('\r\n')
    if len(ls) > 4 or max(vlen(l) for l in ls) > 60:
        return 'L'
    return 'D'


def norm(t, s):
    """Texto como vai para o tradutor: quebras só com \\n; nas falas, sem as quebras que eram só da caixa."""
    if t == 'g':
        return s
    ls = [l.rstrip(' ') for l in s.split('\r\n')]
    if kind(t, s) == 'L':
        return '\n'.join(ls)
    cur = ls[0]
    for prev, nxt in zip(ls, ls[1:]):
        p = TAG.sub('', prev)
        first = TAG.sub('', nxt).split(' ')[0]
        hard = not p or not nxt or (p.endswith(('.', '!', '?', ':', '"', '…', '—')) and len(p) + 1 + len(first) <= W - 4)
        cur += ('\n' if hard else ' ') + nxt
    return cur


def cap(s):
    return max(CAP, len(s.split('\r\n')))


def wrap(s):
    """Requebra uma fala em linhas de até W caracteres visíveis; devolve a lista de linhas."""
    out = []
    for seg in s.split('\n'):
        cur = ''
        for w in re.split(r' (?![^<]*>)', seg):
            if cur and vlen(cur) + 1 + vlen(w) > W:
                out.append(cur)
                cur = w
            else:
                cur = cur + ' ' + w if cur else w
        out.append(cur)
    return out


def italics(s, perword):
    if IT not in s:
        return s
    s = s.replace('</>' + IT, '').replace('</> ' + IT, ' ')
    if perword:
        s = re.sub(re.escape(IT) + r'(.*?)</>', lambda m: ' '.join(IT + w + '</>' for w in re.split(r'[ \n]', m.group(1)) if w), s, flags=re.S)
    return s


def final(t, en_orig, pt):
    """Texto como vai para o jogo."""
    if t == 'g':
        return italics(pt, False)
    if kind(t, en_orig) == 'L':
        return italics(pt, True).replace('\n', '\r\n')
    return ' \r\n'.join(wrap(italics(pt, True)))


def skip(s):
    return (not s.strip()) or s == 'None' or not re.search('[A-Za-z]', TAG.sub('', s)) or bool(re.search('[぀-ヿ一-鿿]', s))
