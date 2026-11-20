# Estudo 002 — DATE

**Status:** hipótese empírica aberta; estudo de engenharia suspenso. Nenhum algoritmo DATE foi validado end-to-end.

Artigo científico completo: [paper.md](paper.md).

O diagnóstico investiga se a magnitude das margens acrescenta informação ao par de decisões binárias dos horizontes curto/longo e ao feedback agregado. Uma identidade de teoria da decisão é demonstrada, mas o valor empírico não foi estabelecido.

## Reprodução do diagnóstico sintético

```bash
python -m pip install numpy scikit-learn pytest
cd research/002-date/code
OPENBLAS_NUM_THREADS=1 python diagnostic.py --t 30000 --n 10000 --seeds 3 --output ../data/reproduction_local.json
```

Resultados históricos: [data/results_synthetic.json](data/results_synthetic.json) e [data/bootstrap_exploratory.json](data/bootstrap_exploratory.json).

Foram executadas 12 combinações de cenário e semente, com perdas contrafactuais offline; nenhuma evidência estável demonstrou ganho do controlador C3. A instrumentação C do W-TinyLFU upstream não foi compilada nem validada integralmente. Nenhum trace público foi usado para validar DATE.

### Componentes isolados

- `code/extract_prefix.py`: extrator binário de `oracleGeneral`, com sanitização de `next_access_vtime`.
- `code/date_admission_log.h` e `code/apply_logger.py`: logger C e patcher **não integrados nem validados** contra W-TinyLFU upstream.
- `code/stats.py`: análise bootstrap para ganho mínimo, sujeita a hipóteses de dependência temporal.

**Não tratar esses módulos como prova de competitividade operacional.**
