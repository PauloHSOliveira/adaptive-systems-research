# Estudo 001 — CABS

**Status:** protótipo experimental encerrado como linha algorítmica principal.

Artigo científico completo: [paper.md](paper.md).

O código verifica uma política de admissão baseada em intervalos de Weighted Space-Saving, comparada a uma política pontual que compartilha estimador e metadados. Os limites garantem preferência **histórica**, não superioridade de misses futuros.

## Reprodução

```bash
cd research/001-cabs/code
PYTHONPATH=. python -m unittest discover -s ../tests -v
PYTHONPATH=. python -m cabs.bench --n 10000 --seeds 3 --k 100 --m 500 --epoch 10000 --output ../data/reproduction_local.json
```

Resultados primários: [data/benchmarks_reproduced.json](data/benchmarks_reproduced.json). Regressão observada no cenário de drift rápido: **+8,38%** de custo de misses em relação ao baseline pontual. Este é um resultado exploratório, com três sementes, e não demonstra dominância em geral. O cenário denominado `reset_churn` não chegou a trocar de fase em 10.000 requisições; esse limite é documentado no artigo.

Código Python standard library somente. O baseline `point` **não** é W-TinyLFU fiel. O LFU exato mantém contagens globais e **não** é um ótimo offline.
