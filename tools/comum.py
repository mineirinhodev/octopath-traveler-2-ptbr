"""O que build.py e extract.py têm em comum: onde ficam as tabelas e como o texto é guardado em texto/."""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from romfs import RomFS
from pak import Pak

PAK = 'Majesty/Content/Paks/Majesty-Switch.pak'
TABELAS = {
    'GameText': ('g', 'Majesty/Content/GameText/Database/GameText{}'),
    'TalkData': ('t', 'Majesty/Content/Talk/Database/TalkData_{}'),
}
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'texto')


def abrir(romfs):
    path, off, size = RomFS(romfs).locate(PAK)
    return Pak(path, off, size)


def grupo(linha):
    p = linha.split('_')
    if p[0] in ('TX', 'TXT') and len(p) > 2:
        return '_'.join(p[:3] if p[1] in ('MS', 'SS', 'FC', 'NPC') and len(p) > 3 else p[:2])
    return p[0]


def ler_texto(pasta):
    d = {}
    if os.path.isdir(pasta):
        for f in sorted(os.listdir(pasta)):
            if f.endswith('.json'):
                with open(os.path.join(pasta, f), encoding='utf-8') as fh:
                    d.update(json.load(fh))
    return d


def gravar_texto(pasta, pares):
    os.makedirs(pasta, exist_ok=True)
    grupos, nomes = {}, {}
    for linha, s in pares:
        # nomes que só diferem em maiúsculas vão para o mesmo arquivo (discos que não as distinguem)
        g = nomes.setdefault(grupo(linha).lower(), grupo(linha))
        grupos.setdefault(g, {})[linha] = s
    for g, d in grupos.items():
        with open(os.path.join(pasta, g + '.json'), 'w', encoding='utf-8') as fh:
            json.dump(d, fh, ensure_ascii=False, indent=0)
            fh.write('\n')
    return len(grupos)
