#!/usr/bin/env python3
"""Aplica texto/ sobre o seu dump e grava a pasta do mod.

uso: python3 tools/build.py <romfs.img ou pasta do RomFS> <pasta do mod>
"""
import os, sys
from comum import TABELAS, RAIZ, abrir, ler_texto
import pak, regras, tabela


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    jogo = abrir(sys.argv[1])
    arquivos = []
    for nome, (t, caminho) in TABELAS.items():
        caminho = caminho.format('EN')
        pt = ler_texto(os.path.join(RAIZ, nome))
        ua, ue = jogo.read(caminho + '.uasset'), jogo.read(caminho + '.uexp')
        faltam, grandes = [], []

        def novo(linha, s):
            if linha not in pt:
                if not regras.skip(regras.norm(t, s)):
                    faltam.append(linha)
                return None
            f = regras.final(t, s, pt[linha])
            if t == 't' and regras.kind(t, s) == 'D' and f.count('\r\n') + 1 > regras.cap(s):
                grandes.append(linha)
            return f

        ua, ue, n = tabela.trocar(ua, ue, novo)
        print(f'{nome}: {n} textos trocados, {len(faltam)} sem tradução (ficam em inglês)')
        if grandes:
            print(f'  {len(grandes)} falas passam da caixa: {grandes[:10]}')
        arquivos += [(caminho + '.uasset', ua), (caminho + '.uexp', ue)]
    destino = os.path.join(sys.argv[2], 'romfs', 'Majesty', 'Content', 'Paks')
    os.makedirs(destino, exist_ok=True)
    destino = os.path.join(destino, 'Majesty-Switch_0_P.pak')
    pak.write(arquivos, destino)
    print(destino)


if __name__ == '__main__':
    main()
