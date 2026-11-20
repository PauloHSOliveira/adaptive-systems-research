# Adaptive Systems Research

**Pesquisa experimental em algoritmos online, estruturas de dados probabilísticas, políticas de cache e sistemas adaptativos.**

Repositório de estudos reproduzíveis, com artigos científicos, implementações, dados experimentais, testes e registro explícito de limitações e resultados negativos. O objetivo é distinguir correção matemática, evidência empírica e viabilidade de engenharia.

> **Status científico:** os estudos disponíveis são manuscritos exploratórios, não revisados por pares. Não existe alegação de descoberta inédita, superioridade sobre W-TinyLFU/Evolving Sketch ou validação em traces públicos.

## Estudos

| ID | Estudo | Questão central | Evidência | Estado |
|:--|:--|:--|:--|:--|
| **001 — CABS** | [Certificação histórica de admissão em cache](research/001-cabs/paper.md) | Certificados de dominância histórica reduzem misses futuros? | Invariantes formais; 60 execuções sintéticas; 7 testes; regressão de 8,38% sob drift rápido | Encerrado como linha principal |
| **002 — DATE** | [Valor das magnitudes de margem](research/002-date/paper.md) | Magnitudes acrescentam valor decisório aos sinais e feedback agregado? | Identidade de valor informacional; 12 execuções sintéticas; resultados inconclusivos | Hipótese aberta; linha suspensa |

## Estrutura

```text
adaptive-systems-research/
├── README.md
├── docs/
│   └── research-protocol.md
├── research/
│   ├── 001-cabs/
│   │   ├── paper.md
│   │   ├── README.md
│   │   ├── code/cabs/
│   │   ├── tests/
│   │   └── data/benchmarks_reproduced.json
│   └── 002-date/
│       ├── paper.md
│       ├── README.md
│       ├── code/
│       ├── tests/
│       └── data/
├── assets/
└── papers/                  # PDF e DOCX derivados dos manuscritos
```

## Como reproduzir

A reprodução de cada estudo começa em seu próprio `README.md`. Os experimentos são executáveis em CPU sem GPU e não requerem APIs pagas. As métricas exploratórias não substituem testes confirmatórios. Código e resultados são preservados sem modificar históricos para favorecer novas hipóteses.

## Protocolo para novos estudos

Consultar [docs/research-protocol.md](docs/research-protocol.md) antes de iniciar outra pesquisa. Cada estudo deve começar com literatura e um problema falsificável, avançar para reprodução de baselines, pré-registrar comparações, e divulgar também resultados negativos e limitações.

## Publicações

Os arquivos `.md` são as fontes editáveis canônicas. Versões PDF/DOCX, quando presentes em `papers/`, são derivadas dessas fontes. Dados de produção de terceiros não são redistribuídos sem verificação de licença.

## Licenças

A definição de licenças de reutilização para código e manuscritos permanece pendente. A disponibilização pública não implica, por si só, autorização irrestrita de redistribuição ou modificação.
