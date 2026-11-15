#!/usr/bin/env python3
"""Exporta o texto do seu dump para JSON, no mesmo formato de texto/ (para comparar ou traduzir).

uso: python3 tools/extract.py <romfs.img ou pasta do RomFS> <pasta de saída> [idioma: EN, JA, FR, DE, ES, IT, KR, ZH_CN, ZH_TW]
"""
import os, sys
from comum import TABELAS, abrir, gravar_texto
import regras, tabela


def main():
    if len(sys.argv) not in (3, 4):
        raise SystemExit(__doc__)
    idioma = sys.argv[3].upper() if len(sys.argv) == 4 else 'EN'
    jogo = abrir(sys.argv[1])
    for nome, (t, caminho) in TABELAS.items():
        caminho = caminho.format(idioma)
        pares = [(l, regras.norm(t, s)) for l, s in
                 tabela.textos(jogo.read(caminho + '.uasset'), jogo.read(caminho + '.uexp')) if s.strip()]
        n = gravar_texto(os.path.join(sys.argv[2], nome), pares)
        print(f'{nome}: {len(pares)} textos em {n} arquivos')


if __name__ == '__main__':
    main()
