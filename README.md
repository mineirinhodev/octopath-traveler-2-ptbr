# OCTOPATH TRAVELER II — Tradução PT-BR (não oficial)

Tradução dos textos de **OCTOPATH TRAVELER II** (Nintendo Switch, title ID `0100A3501946E000`) para
**português do Brasil**. O jogo não tem português; a tradução entra no lugar do texto em inglês.

- Interface, menus, batalha, habilidades, itens, tutoriais, diário e os diálogos das oito histórias, das histórias
  paralelas, das conversas de viagem e dos NPCs.
- 43.763 textos em 198 arquivos (cerca de 360 mil palavras em português).
- Vozes, vídeos e textos desenhados em imagens continuam como no original.

> **Aviso:** a tradução **ainda não foi revisada linha a linha nem conferida na tela do jogo**. Espere
> inconsistências, frases estranhas e linhas que não cabem na caixa de texto. Correções são bem-vindas: veja
> [Como contribuir](#como-contribuir).

## O que há neste repositório

Este repositório **não contém arquivos do jogo**. Ele guarda só o texto traduzido e os scripts que o aplicam sobre o
seu próprio dump:

```
texto/      texto em português, em JSON, separado por tabela do jogo
tools/      scripts em Python para montar o mod e exportar texto
```

As tabelas de texto do jogo (`.uasset` / `.uexp`) também carregam dados originais que não são texto, por isso o mod
já montado não é distribuído aqui.

## Como montar o mod

Você precisa do Python 3 (sem dependências) e do RomFS do seu próprio jogo, extraído do seu dump.

Rode, apontando para a raiz do RomFS (a pasta que contém `Majesty/Content/Paks/Majesty-Switch.pak`) ou, no
NX Library, direto para o `romfs.img` do jogo:

```
python3 tools/build.py "caminho/para/romfs" "Traducao PT-BR"
python3 tools/build.py "/caminho/OCTOPATH TRAVELER II.app/Contents/Resources/romfs.img" "Traducao PT-BR"
```

O resultado é uma pasta de mod pronta, com um único arquivo de uns 16 MB:

```
Traducao PT-BR/
└── romfs/
    └── Majesty/Content/Paks/Majesty-Switch_0_P.pak
```

Textos do jogo que não tiverem tradução (por exemplo, numa versão mais nova) ficam em inglês e o script avisa
quantos são.

## Instalação

Em qualquer caso, **deixe o idioma do jogo em inglês**: o português aparece no lugar dele.

### NX Library (Mac)

1. Copie a pasta `Traducao PT-BR` para
   `/Applications/NxNative_Data/AppSupport/0100A3501946E000/mods/`
2. Abra o NX Library, entre em OCTOPATH TRAVELER II → **Mods** e ligue `Traducao PT-BR`.
3. Inicie o jogo.

### Switch com Atmosphère

Copie o conteúdo da pasta `romfs` do mod para o cartão SD em

```
atmosphere/contents/0100A3501946E000/romfs/
```

Não testado.

### Outros emuladores

Emuladores que aceitam mods no formato `romfs` costumam ter uma pasta de mods por jogo: abra-a pelo menu do
emulador e copie a pasta `Traducao PT-BR` inteira para lá. Não testado.

### Desinstalar

Desligue o mod ou apague a pasta. Nada no jogo nem no save é alterado.

## Escolhas de tradução

- Nomes de personagens, cidades, reinos e deuses ficam como no original (Hikari, Agnea, Partitio, Osvald, Throné,
  Temenos, Ochette, Castti, Solistia, Ku, Flamechurch, New Delsta, Toto'haha, Hinoeuma, Aelfric…). Em nomes de lugar
  compostos, só a parte comum é traduzida ("Montwise: Biblioteca", "Areias Ocidentais de Sai").
- Regiões, classes, habilidades, itens e termos do sistema são traduzidos, com os mesmos termos da
  [tradução do primeiro jogo](https://github.com/mineirinhodev/octopath-traveler-ptbr) onde eles se repetem:

  | Inglês | Português |
  |---|---|
  | Merchant / Thief / Warrior / Hunter | Mercador(a) / Ladrão (Ladra) / Guerreiro(a) / Caçador(a) |
  | Cleric / Dancer / Scholar / Apothecary | Clérigo(a) / Dançarino(a) / Erudito(a) / Boticário(a) |
  | Armsmaster / Arcanist / Conjurer / Inventor | Mestre de Armas / Arcanista / Conjurador(a) / Inventor(a) |
  | Path Action / Latent Power | Ação de Caminho / Poder Latente |
  | Boost / Break | Impulso / Quebra |
  | Bribe / Entreat / Hire / Coerce | Subornar / Suplicar / Contratar / Coagir |
  | Mug / Befriend / Ambush / Soothe | Assaltar / Cativar / Emboscar / Acalmar |
  | Crestlands / Brightlands / Wildlands / Leaflands | Terras das Cristas / Terras Luminosas / Terras Selvagens / Terras Frondosas |
  | Harborlands / Winterlands | Terras Portuárias / Terras Invernais |
  | beastling | fera-humana |
  | leaves (moeda) | folhas |

- Partitio fala com um jeito interiorano leve; Ochette, com frases simples; a gente de Ku, com formalidade.
- As siglas HP, SP, BP, JP e EXP ficam como estão.

## Limitações conhecidas

- A única conferência dentro do jogo foi de carregamento: no NX Library, o jogo abre o arquivo do mod e o lê
  inteiro, sem erro. O texto não foi olhado na tela.
- Textos que são imagens (logotipo, "BREAK" e parecidos) não mudam.
- As falas são quebradas pelo script em linhas de até 50 caracteres, com no máximo as linhas que a caixa original
  usa (3, em geral); como a fonte não é monoespaçada, uma linha pode ficar um pouco larga demais.
- Nos menus, um texto pode ficar mais largo que o espaço.
- O jogo monta algumas frases com artigos do inglês ("a", "the") vindos de outra tabela, que não foi traduzida.
- O gênero de quem fala ou de quem ouve foi deduzido pelo contexto e pode estar errado em algumas falas.
- Instalação em Atmosphère e em outros emuladores não foi testada.

## Como contribuir

Achou um erro? Abra uma [issue](../../issues) com a frase como aparece no jogo (uma captura de tela ajuda) ou mande
um pull request.

A tradução fica em `texto/GameText/` (menus, batalha, itens, diário) e `texto/TalkData/` (falas). Cada arquivo é um
objeto `{"LINHA": "texto em português"}`, em que a linha é o nome que o próprio jogo dá àquele texto; os arquivos
agrupam as linhas pelo começo do nome (`TX_MS_KEN` história de Hikari, `TX_MS_ODO` Agnea, `TX_MS_SHO` Partitio,
`TX_MS_GAK` Osvald, `TX_MS_TOU` Throné, `TX_MS_SIN` Temenos, `TX_MS_KAR` Ochette, `TX_MS_KUS` Castti, `TX_SS`
histórias paralelas, `TX_FC` e `TXT_NPC` NPCs, `TX_PTC` conversas do grupo, `ABN`/`ABD` habilidades…). Para corrigir uma frase, procure-a nesses arquivos e edite o valor,
mantendo:

- as variáveis `{0}`, `{1}`… e os símbolos (`➓` é a moeda; `㌔`, `④` e parecidos são ícones);
- as marcações `<span style="italic">…</>` e `<br>`;
- as quebras de linha que já existirem (`\n`). Não acrescente quebras nas falas: o script cuida disso e avisa
  quando uma fala não cabe na caixa.

## Scripts

| Script | Função |
|---|---|
| `tools/build.py` | aplica `texto/` sobre as tabelas do seu dump e grava a pasta do mod |
| `tools/extract.py` | exporta o texto do seu dump para JSON, no mesmo formato de `texto/` (aceita o idioma: `EN`, `JA`, `FR`, `DE`, `ES`, `IT`, `KR`, `ZH_CN`, `ZH_TW`) |
| `tools/regras.py` | tipos de fala, quebra de linha na largura da caixa, itálico |
| `tools/tabela.py` | leitor / gravador do texto das tabelas (`.uasset` / `.uexp`) |
| `tools/pak.py` | leitor de `.pak` do Unreal Engine 4.27 e gravador do pak de patch |
| `tools/romfs.py` | acesso ao RomFS: pasta extraída ou imagem `romfs.img` do NX Library |

### Detalhe técnico

O jogo usa o Unreal Engine 4.27. O texto está em duas DataTables dentro de `Majesty-Switch.pak` (pak versão 11,
zlib): `GameText/Database/GameTextEN` (uma propriedade de texto por linha) e `Talk/Database/TalkData_EN` (uma fala
por linha, com tipo de balão e nome de quem fala). O `build.py` troca só as cadeias de texto, casando-as pelo nome
da linha, ajusta os tamanhos no `.uasset` e grava as duas tabelas num pak de patch sem compressão
(`Majesty-Switch_0_P.pak`, no formato antigo de pak, que o motor ainda lê), carregado por cima do original. O pak
do jogo não é modificado. As fontes do jogo já têm os acentos do português.

## Aviso legal

Projeto de fã, sem fins lucrativos, sem vínculo com a Square Enix nem com a Nintendo. OCTOPATH TRAVELER II é marca e
propriedade de seus respectivos donos. Este repositório não inclui o jogo nem seus arquivos originais e só funciona
com uma cópia sua, obtida legalmente. Os scripts em `tools/` estão sob a licença MIT (veja [`LICENSE`](LICENSE)).
