# Protocolo de pesquisa experimental

## 1. Definição do problema

Registrar **ID**, pergunta falsificável, hipótese nula, alternativa, estado da literatura, custos do problema, métricas e critérios claros de encerramento. Diferenciar novo mecanismo, nova informação, ablação e reprodução de resultado existente. Não reivindicar novidade sem auditoria de trabalhos relacionados.

## 2. Hierarquia de evidência

1. Proposições matemáticas com hipóteses, demonstração e escopo explícitos.
2. Testes unitários e de propriedades para a implementação.
3. Benchmark sintético exploratório, separado do resultado confirmatório.
4. Reprodução de baselines fiéis do estado da arte.
5. Experimento confirmatório em traces públicos reservados, com parâmetros congelados.
6. Reprodução independente, orçamento de memória e CPU equalizados.

## 3. Causalidade online

Nenhuma feature ou decisão em `t` pode acessar solicitações ou labels de `t+1` em diante. A avaliação contrafactual offline deve ser isolada do estado online. O mesmo conjunto de oportunidades e a mesma política geradora devem ser utilizados quando a pergunta for apenas sobre o valor de informação de um sinal.

## 4. Comparações justas

- Mesma capacidade física e modelo de custo em todas as políticas.
- Igualdade ou contabilização transparente de **metadados em bytes**, incluindo estruturas auxiliares e parâmetros dos modelos.
- Tempo de CPU medido na mesma implementação e equipamento; não comparar timings Python com bibliotecas nativas como equivalentes.
- Baselines com versões e commits fixados; implementar fielmente regiões de janela, admissão e estruturas internas quando relevante.
- Escolher o comparador principal em desenvolvimento e não modificá-lo depois de observar o holdout.

## 5. Estatística

- Definir o estimando (perda por oportunidade, hit rate ou custo total) antes da execução.
- Para pares dependentes, preservar índice temporal e sobreposição de labels, preferindo métodos explicitamente apropriados a séries dependentes.
- Não supor que bloco de comprimento H produz independência; não usar `n_eff=T/H` como regra universal.
- Se o objetivo for superar uma melhoria mínima `r`, testar o limiar diretamente: `X=loss_treatment-(1-r)*loss_control`.
- Usar avaliação de sensibilidade ao tamanho dos blocos e validar sua calibração em simulações específicas.
- Distinguir ausência de rejeição estatística, equivalência e decisão de engenharia de interromper a pesquisa.

## 6. Reprodutibilidade

Guardar versões do código, parâmetros, sementes, formato de traces, comandos, hashes de subconjuntos, resultados brutos, testes e procedimento de análise. Documentar problemas conhecidos, validação não executada e decisões tomadas após resultados exploratórios. Não retirar execuções desfavoráveis.

## 7. Estrutura de novos estudos

Criar `research/NNN-slug/` com `paper.md`, `README.md`, `code/`, `tests/` e `data/`. A conclusão deve indicar separadamente: **demonstrado**, **observado**, **não testado**, **limitação** e **decisão de continuidade**.
