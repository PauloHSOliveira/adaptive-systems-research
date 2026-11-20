---
title: "Certificação de Dominância Histórica para Admissão em Cache com Weighted Space-Saving"
subtitle: "Propriedades formais, implementação de referência e avaliação experimental exploratória"
author: "Paulo H. S. Oliveira"
date: "20 de novembro de 2026"
lang: pt-BR
keywords: [cache admission, Weighted Space-Saving, data streams, frequency sketch, weighted caching, reprodução experimental]
---

**Natureza:** manuscrito de pesquisa exploratória. Não revisado por pares. A avaliação apresentada é limitada a cargas sintéticas e não estabelece superioridade sobre métodos do estado da arte.

# Resumo

**Contexto.** Sistemas de cache utilizam estatísticas históricas de acesso para selecionar objetos residentes sob restrições de capacidade. Estruturas compactas de estimação de frequência oferecem limites de erro para contagens agregadas, mas esses limites não representam necessariamente o benefício de armazenamento futuro. **Objetivo.** Analisar uma regra conservadora de admissão, denominada *Certificate-Aware Boundary Selection* (CABS), que aceita a substituição de um residente apenas quando o limite inferior da frequência ponderada histórica do candidato excede o limite superior da vítima. **Métodos.** Implementou-se um protótipo em Python com Weighted Space-Saving (WSS), metadados de residentes e épocas de observação. Foram analisados invariantes históricos, as relações entre regras de admissão e um contraexemplo temporal. Um experimento exploratório utilizou quatro geradores sintéticos, três sementes, 10.000 requisições por execução, cache com capacidade para 100 objetos e sketch com 500 entradas, comparando cinco estratégias (60 execuções). **Resultados.** A condição de certificação garante dominância estrita das contagens históricas na mesma época, desde que os intervalos sejam válidos; não garante melhor desempenho futuro. No cenário de migração rápida de objetos populares, o custo ponderado médio de misses foi 71.641,7 para CABS e 66.104,3 para a regra pontual com o mesmo estimador, uma regressão de 8,38%. Nos demais cenários, as diferenças foram pequenas e não sustentam conclusões inferenciais com apenas três sementes. Um contraexemplo demonstra que a regra conservadora pode ocasionalmente reduzir misses futuros apesar de rejeitar uma substituição historicamente correta. **Conclusão.** A certificação histórica constitui uma propriedade matemática válida, mas o protótipo não demonstrou ganho operacional consistente. A linha foi interrompida como proposta algorítmica principal, mantendo-se código, dados e limites da conclusão para futura reprodução.

**Palavras-chave:** admissão em cache; Weighted Space-Saving; perda ponderada; certificação histórica; sketches de frequência; dados sintéticos.

# Abstract

**Background.** Cache admission decisions often rely on compact historical frequency estimates, whose error bounds do not directly characterize future reuse. **Objective.** We examine Certificate-Aware Boundary Selection (CABS), a conservative admission rule that replaces a resident object only if the candidate's lower bound on historical weighted frequency exceeds the resident's upper bound. **Methods.** A Python reference prototype integrates Weighted Space-Saving, resident-bound tracking, and fixed observation epochs. We establish local invariants, analyze divergent cache trajectories, and execute a small synthetic pilot with four workloads, three seeds, 10,000 requests per run, cache capacity 100, and sketch capacity 500, yielding 60 policy/workload/seed runs. **Results.** The certificate soundly implies historical dominance at a fixed decision state but provides no guarantee of future hit rate or weighted miss cost. Under rapidly moving hot sets, mean weighted miss cost increased from 66,104.3 with point-estimate admission to 71,641.7 with CABS (+8.38%). Other synthetic workloads produced minor mixed differences. An adversarial continuation shows that rejecting a historically correct replacement can nevertheless improve a future cost sequence; this is not a typical-workload guarantee. **Conclusion.** Historical certification is formally sound but failed to show consistent operational benefit in this limited pilot. The algorithmic direction was suspended, and the implementation and data are preserved as a reproducible exploratory case study.

**Keywords:** cache admission; frequent items; weighted Space-Saving; historical certification; nonstationary streams; reproducibility.

# 1. Introdução

Caches com espaço físico limitado atendem repetidamente a pedidos para objetos de um catálogo muito maior que sua capacidade residente. A escolha de substituição afeta a taxa de acertos, o custo das faltas e a estabilidade operacional. Sob custos heterogêneos, uma falta para um objeto caro pode valer mais que várias faltas para objetos baratos; por isso, frequência bruta e frequência ponderada não são intercambiáveis.

Estruturas como *Space-Saving* aproximam contagens de itens em streams com memória limitada e oferecem limites explícitos de erro [1]. Essa propriedade sugere uma política de admissão que substitua apenas quando uma comparação entre limites permita certificar que o candidato foi mais requisitado, em peso, que a vítima. Uma motivação plausível é evitar substituições causadas por superestimações do sketch.

A hipótese crítica é diferente: **um ganho de confiabilidade sobre o passado melhora decisões sobre acessos futuros?** Um objeto historicamente dominante pode deixar de ser requisitado; outro com histórico fraco pode se tornar popular logo após a decisão. Em workloads sujeitos a mudanças de regime, uma regra excessivamente conservadora pode perder oportunidades de adaptação.

Este estudo apresenta um modelo específico, invariantes formais, casos adversariais e um teste exploratório desse compromisso. O objetivo não é reivindicar a invenção de certificados de frequência, já presentes em trabalhos anteriores, mas avaliar o efeito de sua aplicação à política de admissão com uma implementação comparativa controlada.

## 1.1. Pergunta e hipóteses

A pergunta experimental é se a condição estrita de certificação `L(x)>U(v)`, aplicada a estimativas históricas ponderadas, reduz o custo futuro de misses em comparação com uma regra pontual construída sobre o **mesmo WSS e os mesmos metadados residentes**.

A hipótese operacional inicial (H1) previa que rejeitar trocas incertas poderia proteger o cache de substituições danosas. A hipótese alternativa adversarial (H2) previa que a mesma rejeição atrasaria a resposta à migração do conjunto popular. Ambas são hipóteses de desempenho, não consequências matemáticas da validade dos intervalos.

## 1.2. Escopo e nível de evidência

O trabalho compreende: prova de invariantes relativos ao histórico da época, teste de regressão contrafactual, implementação executável e medições sintéticas exploratórias. Não há experimentos em traces públicos, comparação fiel com W-TinyLFU, calibração estatística confirmatória, equalização de consumo de metadados em bytes ou medição de overhead em linguagem de produção.

# 2. Trabalhos relacionados

## 2.1. Space-Saving e contagens aproximadas

Metwally, Agrawal e El Abbadi [1] desenvolveram o Space-Saving para a estimação dos itens frequentes e a recuperação aproximada de Top-k em streams. A representação substitui entradas de menor contagem e conserva informação sobre o erro da estimativa. Na variante ponderada, cada acesso carrega um peso positivo, como o custo de uma falta evitável.

Uma entrada armazenada pode ser representada por $(o,U_e(o),\varepsilon_e(o))$, em que $U_e$ é uma estimativa superior e $\varepsilon_e$ o erro associado. O limite inferior é $L_e(o)=U_e(o)-\varepsilon_e(o)$. Para objetos não rastreados, a incerteza depende do contador mínimo do sketch. A certificação exige atualizar esses limites de modo coerente com os pesos observados.

## 2.2. TinyLFU e políticas de admissão

TinyLFU [2] usa um estimador aproximado com envelhecimento para informar decisões de admissão de objetos. O arranjo W-TinyLFU combina uma região de janela com uma política principal, oferecendo amortecimento para bursts. Não se deve confundir a regra pontual implementada neste estudo com TinyLFU ou W-TinyLFU fiéis: ela usa WSS e sua estrutura de residentes, não o algoritmo de produção descrito por Einziger e colaboradores.

## 2.3. Políticas simples e concorrentes

LRU e LFU exato fornecem referências descritivas. O LFU usado mantém contagens históricas globais em um dicionário não limitado, o que altera radicalmente o orçamento de memória e não corresponde ao ótimo offline com conhecimento do futuro. Políticas posteriores como S3-FIFO [3] e SIEVE [4] mostram que o custo operacional, a recência e o comportamento de bursts podem ser tão importantes quanto uma aproximação histórica mais precisa.

# 3. Formulação matemática

## 3.1. Modelo de stream ponderado

Considere solicitações $(x_t,c_t)$, $t=1,\ldots,T$, onde $x_t$ é o identificador e $c_t>0$ é o peso de um miss. Um cache físico mantém um conjunto residente $C_t$ com $|C_t|\le k$. O custo total é

$$
\mathcal L_T=\sum_{t=1}^T c_t\,\mathbf 1[x_t\notin C_{t^-}],
$$

onde $C_{t^-}$ é o conjunto residente imediatamente antes do atendimento da requisição $t$. A estatística de histórico para uma época $e$ é

$$
w_e(o,t)=\sum_{s\in e,\,s\le t} c_s\mathbf 1[x_s=o].
$$

O valor histórico não é uma previsão de demanda futura nem uma estimativa de custo causal de uma substituição em todo o horizonte $T$.

## 3.2. Intervalos e metadados de residentes

O WSS fornece limites históricos $(L_e(o,t),U_e(o,t))$. No protótipo, uma estrutura auxiliar *Resident Metadata* (RM) conserva o intervalo do objeto quando ele entra no cache, inclusive se o WSS deixar de rastreá-lo. A cada hit residente de peso $c_t$, ambos os limites da RM são incrementados por $c_t$. Num reset de época, o sketch e os limites RM são zerados, mas os objetos continuam residentes.

**Proposição 1 — manutenção do intervalo histórico.** Suponha que os limites associados a uma entrada recém-admitida contêm a contagem ponderada verdadeira na época. Então os incrementos idênticos de limite inferior, limite superior e contagem real em cada hit mantêm o invariante

$$
L_e(o,t)\le w_e(o,t)\le U_e(o,t)
$$

para aquele residente, enquanto o mecanismo de atualização e reset seguir as regras especificadas.

**Demonstração.** No instante da admissão, o invariante vale por hipótese. Cada hit de peso $c_t$ aumenta a contagem real e os dois extremos pelo mesmo valor, preservando as desigualdades. A ausência de hit deixa os três valores inalterados. O reset inicia uma nova época com contagens zero e portanto restabelece a condição. Por indução sobre as requisições, a desigualdade permanece válida. $\square$

A amplitude $U-L$ pode continuar positiva durante toda a residência. Incrementos exatos posteriores não eliminam a incerteza herdada da admissão.

## 3.3. Certificado de dominância histórica

A regra CABS admite um candidato $x$ no lugar de um residente $v$ apenas quando

$$
\boxed{L_e(x,t)>U_e(v,t).}
$$

**Proposição 2 — correção local do certificado.** Se ambos os intervalos contêm as contagens verdadeiras da mesma época, então

$$
L_e(x,t)>U_e(v,t)\quad\Longrightarrow\quad w_e(x,t)>w_e(v,t).
$$

**Demonstração.** Pela validade dos intervalos, $w_e(x,t)\ge L_e(x,t)$ e $w_e(v,t)\le U_e(v,t)$. Compondo as desigualdades, obtém-se a conclusão. $\square$

A proposição é uma consequência imediata de limites conhecidos. Não estabelece originalidade matemática e, em particular, não prova que substituir $v$ por $x$ será vantajoso em requisições futuras.

## 3.4. Regra pontual e divergência de trajetórias

A política pontual utiliza o mesmo WSS e a RM, seleciona a vítima com menor limite superior e compara a estimativa pontual do candidato com o limite superior da vítima. Na implementação, a estimativa pontual do candidato é o seu limite superior:

$$
A_{\mathrm{point}}(x,v)=[U_e(x)>U_e(v)],\qquad
A_{\mathrm{CABS}}(x,v)=[L_e(x)>U_e(v)].
$$

Para um **estado idêntico** dos estimadores, da RM e da vítima, $L_e(x)\le U_e(x)$ implica

$$
A_{\mathrm{CABS}}(x,v)=1\ \Longrightarrow\ A_{\mathrm{point}}(x,v)=1.
$$

O inverso não vale em geral. Essa implicação é local: após uma rejeição por CABS e uma admissão pontual, os conteúdos físicos do cache e as possíveis vítimas futuras divergem. Não se pode concluir que as sequências completas de substituições ou misses sejam subconjuntos umas das outras.

## 3.5. Limite da informação histórica

Para qualquer prefixo finito, podem-se construir continuações que favoreçam preservar $x$ ou $v$, respectivamente. Assim, as contagens históricas, mesmo exatas, não bastam para garantir universalmente a ação de menor custo futuro sob sequências arbitrárias. Uma garantia preditiva exige hipóteses probabilísticas adicionais sobre os acessos ou informação externa.

# 4. Materiais e métodos

## 4.1. Protótipo e políticas

O protótipo foi implementado em Python, sem dependências externas, com um heap mínimo indexado para WSS ($O(\log M)$ por atualização e $O(M)$ de estado principal). A RM mantém intervalos de $k$ residentes e seleciona a vítima varrendo os residentes, estratégia adequada à referência, mas não necessariamente a uma implementação otimizada em produção.

Foram avaliadas cinco políticas: LRU, LFU com contagens exatas globais, regra pontual WSS/RM, CABS certificado e CABS com *holdoff* de 200 requisições após a abertura da época. Os nomes diferenciam os controles reais; LFU exato não foi tratado como um oráculo de ótimo futuro.

## 4.2. Workloads e parâmetros

Os quatro cenários foram construídos com geradores pseudoaleatórios determinísticos: `stationary` (popularidade concentrada com estabilidade), `uniform` (catálogo praticamente uniforme), `drift` (conjunto quente deslocado a cada 2.000 solicitações), e `reset_churn` (gerador com deslocamento de regime a cada 10.000 solicitações).

**Limitação de implementação especialmente importante.** Com $T=10.000$ requisições, o cenário `reset_churn` executou apenas a primeira fase do gerador: o deslocamento previsto para o próximo bloco não ocorreu. Pela mesma razão, a configuração de época $W=10.000$ produziu o reset inicial, sem segundo reset durante essas execuções. Assim, os resultados desse cenário **não avaliam mudanças efetivas entre épocas** e não devem ser apresentados como evidência experimental sobre resets sucessivos.

| Parâmetro | Valor |
|:--|--:|
| Requisições por execução | 10.000 |
| Catálogo disponível | 100.000 objetos |
| Sementes por cenário | 3 (0, 1, 2) |
| Capacidade física $k$ | 100 objetos |
| Entradas do WSS $M$ | 500 |
| Época $W$ | 10.000 requisições |
| Políticas por cenário | 5 |
| Cenários | 4 |
| Execuções totais | 60 |
| Peso de miss | $1+((37\cdot\mathrm{id}+19)\bmod17)$, entre 1 e 17 |
| Métrica primária | Soma dos custos de misses |

Todas as políticas recebem o mesmo fluxo de requisições e pesos para uma determinada combinação de cenário e semente. Não houve calibração confirmatória de um limiar de ganho nem conjunto de validação independente.

## 4.3. Métricas e reprodução

Foram registrados custo ponderado de misses, miss ratio, substituições, bypasses, tempo médio de processamento por requisição e estimativa de tamanho de objetos Python no estado da política. O último valor é uma fotografia baseada em `sys.getsizeof`, não uma avaliação de RSS nem um orçamento rigorosamente igualado em bytes.

O experimento foi reproduzido por execução do módulo `cabs.bench` com argumentos `--n 10000 --seeds 3 --k 100 --m 500 --epoch 10000`. O arquivo JSON reproduzido acompanha o artigo. A suíte final contém sete testes, incluindo verificação de invariantes e contraexemplo de divergência temporal.

# 5. Resultados

## 5.1. Custo ponderado médio

**Tabela 2 — Média do custo ponderado de misses, três sementes. Menor é melhor.**

| Cenário | LRU | LFU exato | Regra pontual | CABS | CABS + holdoff |
|:--|--:|--:|--:|--:|--:|
| Estacionário | 61.980,7 | 46.612,0 | 46.575,0 | 46.570,0 | 46.607,0 |
| Uniforme | 89.982,7 | 89.927,0 | 89.904,3 | 89.887,7 | 89.900,0 |
| Drift rápido | **62.647,3** | 71.251,3 | 66.104,3 | 71.641,7 | 71.678,7 |
| `reset_churn` (primeira fase apenas) | 66.410,3 | 50.047,0 | 50.087,0 | 50.076,0 | 50.101,0 |

A diferença relativa de CABS em relação à regra pontual no cenário de drift é

$$
\frac{71641{,}7-66104{,}3}{66104{,}3}\times100\%\approx\boxed{+8{,}38\%}.
$$

Assim, o conservadorismo do certificado aumentou o custo nesse ambiente. Nos outros cenários, as diferenças percentuais entre CABS e a regra pontual ficaram próximas de zero, sem estabilidade suficiente para alegar uma melhoria relevante.

## 5.2. Comparação pareada por semente

**Tabela 3 — Diferença absoluta CABS − regra pontual. Valores positivos indicam pior desempenho de CABS.**

| Cenário | Semente 0 | Semente 1 | Semente 2 | Média |
|:--|--:|--:|--:|--:|
| Estacionário | −23 | −8 | +16 | −5,0 |
| Uniforme | −57 | −52 | +59 | −16,7 |
| Drift rápido | +5.827 | +5.324 | +5.461 | +5.537,3 |
| Primeira fase de `reset_churn` | −37 | −4 | +8 | −11,0 |

As três replicações no cenário de drift exibem o mesmo sinal e diferença substancial. Entretanto, três sementes e uma família sintética de drift não fornecem a base necessária para generalizar o resultado a cargas reais ou quantificar incerteza inferencial com precisão.

## 5.3. Contraexemplo de desempenho futuro

Para demonstrar que a implicação de admissão local não ordena custos futuros, foi construído um teste de capacidade três, WSS com três entradas e prefixo de requisições $(1,5,3,7,1)$ com pesos $(1,1,1,2,1)$. Na quinta requisição, a regra pontual admite o objeto 1 e remove o objeto 3. A contagem histórica verdadeira de 1 é 2, enquanto a de 3 é 1: a troca pontual é **correta segundo a preferência histórica**, embora não esteja certificada pelos intervalos. CABS rejeita essa troca.

O sufixo requisita o objeto 3 quarenta vezes. Com esse futuro construído intencionalmente, o custo de misses total foi 6 para CABS e 7 para a regra pontual; CABS registrou uma substituição e a regra pontual três. O exemplo refuta a afirmação universal de que uma certificação só poderia reduzir custo futuro se corrigisse uma troca historicamente errada. Não oferece evidência de que o ganho ocorra com frequência em workloads naturais.

## 5.4. Testes de invariantes

As sete verificações executadas com o pacote de referência passaram, inclusive a checagem de que limites inferiores e superiores contêm contagens exatas mantidas apenas como oráculo de depuração. O êxito nesses testes indica consistência dos casos exercitados; não constitui demonstração de ausência geral de bugs nem certificação formal da implementação em qualquer sequência.

# 6. Discussão

O principal resultado metodológico é a distinção entre três níveis: (i) limites válidos para contagens do passado, (ii) ordenação de candidatos e residentes em um mesmo estado, e (iii) consequências acumuladas de decisões online ao longo de futuros ainda não observados. Somente os dois primeiros são cobertos pelas proposições demonstradas.

O resultado desfavorável sob drift rápido é compatível com a interpretação de que exigências de confiança excessiva tornam a política pouco responsiva a novos objetos populares. Entretanto, o piloto não isola universalmente essa causa: são possíveis efeitos de implementação, escolha de vítima, parâmetros de época e estrutura do gerador de requisições.

A ausência de um W-TinyLFU fiel impede afirmar competitividade frente a sistemas modernos. A comparação com LFU global não equilibra metadados, e a comparação com LRU envolve mecanismos de substituição bastante diferentes. O único controle mais próximo de uma ablação causal do certificado é a regra pontual com o **mesmo WSS/RM**, ainda sujeita à divergência de estado após decisões distintas.

# 7. Ameaças à validade e limitações

**Validade interna.** A implementação é um protótipo Python. CPU, overhead de memória e comportamento do alocador não representam uma biblioteca otimizada. A política CABS e a pontual escolhem vítimas a partir de limites superiores residentes; uma regra pontual alternativa poderia utilizar outros escores. É importante preservar o significado exato do baseline.

**Validade de constructo.** O custo de miss é artificial, determinístico por ID, e não decorre de latências reais de recuperação. O WSS usa épocas fixas, não janelas móveis nem um algoritmo de estimação temporal adaptativa.

**Validade externa.** Nenhum trace público de produção foi analisado. A ausência de resets efetivos dentro do cenário `reset_churn` reduz ainda mais o alcance da avaliação sobre mudanças de regime.

**Validade estatística.** Há apenas três sementes por cenário, sem intervalo de confiança confirmatório, pré-registro formal de uma hipótese de superioridade ou correção para várias comparações de políticas/cenários. Pequenas diferenças nos outros regimes não podem ser interpretadas como melhoria estatisticamente estabelecida.

**Memória e recursos.** As estruturas não foram equalizadas em bytes físicos. LFU exato mantém estatísticas potencialmente ilimitadas; comparações de memória ou latência precisam ser redesenhadas para conclusões operacionais.

**Novidade científica.** O uso de limites para heavy hitters e Top-k é anterior a este estudo. Nenhuma nova garantia de regret ou de otimização futura foi demonstrada.

# 8. Reprodutibilidade

O código-fonte, as entradas sintéticas determinísticas, os testes e o JSON de 60 execuções acompanham este artigo no mesmo repositório. Para reproduzir a configuração:

```bash
cd research/001-cabs/code
PYTHONPATH=. python -m unittest discover -s ../tests -v
PYTHONPATH=. python -m cabs.bench --n 10000 --seeds 3 --k 100 --m 500 --epoch 10000 --output ../data/benchmarks_reproduced.json
```

Os arquivos JSON podem variar no tempo médio de CPU e em estimativas de tamanho de objetos conforme hardware e versão de Python; custos de misses, requisições e substituições devem permanecer determinísticos para a mesma implementação e sementes. O sufixo adversarial pertence ao teste de regressão, não ao conjunto de workloads usado na Tabela 2.

# 9. Considerações éticas e uso de dados

Todos os workloads efetivamente executados foram gerados sinteticamente. Nenhum dado pessoal, conteúdo de cache em produção ou trace privado foi processado. Os arquivos publicados devem permitir a verificação das afirmações experimentais sem acesso a serviços pagos ou dados restritos.

# 10. Conclusão

A regra de admissão CABS obtém um certificado matematicamente correto de dominância das contagens ponderadas históricas, desde que os intervalos correspondam ao mesmo estado e à mesma época. Essa propriedade não se converte automaticamente em vantagem no custo futuro de misses. O protótipo reprodutível apresentou aumento de 8,38% no custo médio relativo à regra pontual sob migração rápida de hot sets, e efeitos pequenos ou mistos nas outras cargas. Uma construção adversarial demonstra, ao mesmo tempo, que CABS pode superar a regra pontual em futuros específicos, sem contradizer a dominância local.

A evidência disponível não suporta adoção, superioridade nem originalidade algorítmica. Por razões de priorização de pesquisa, o desenvolvimento de CABS foi encerrado como linha principal. Permanece como caso reproduzível da separação entre certificação histórica e utilidade preditiva em sistemas online.

# Referências

[1] METWALLY, A.; AGRAWAL, D.; EL ABBADI, A. *Efficient Computation of Frequent and Top-k Elements in Data Streams*. ICDT, 2005. https://www.cs.ucsb.edu/research/tech-reports/2005-23

[2] EINZIGER, G.; FRIEDMAN, R.; MANES, B. *TinyLFU: A Highly Efficient Cache Admission Policy*. ACM Transactions on Storage, 2017. https://arxiv.org/abs/1512.00727

[3] YANG, J. et al. *FIFO Queues Are All You Need for Cache Eviction*. SOSP, 2023. https://s3fifo.com/

[4] YANG, J. et al. *SIEVE Is Simpler than LRU: An Efficient Cache Eviction Algorithm for Web Caches*. NSDI, 2024. https://www.usenix.org/conference/nsdi24/presentation/zhang-yazhuo

[5] MUKHOPADHYAY, S.; SINHA, A. *Online Caching with Optimal Switching Regret*. 2021. https://arxiv.org/abs/2101.07043

# Apêndice A — Rastreabilidade

Os principais números são extraídos diretamente de `data/benchmarks_reproduced.json`. O código de referência está em `code/cabs/`, e o contraexemplo consta em `tests/test_round10_counterexample.py` (mantido com o nome histórico do arquivo para preservar a referência de teste). O estudo analítico é independente de variações de formatação do documento.

# Apêndice B — Delimitação da decisão de pesquisa

O encerramento de CABS constitui uma decisão de priorização após um piloto desfavorável em cenário relevante, **não** um teorema de impossibilidade ou uma rejeição inferencial de toda implementação possível. Uma reavaliação científica exigiria workloads públicos, comparação fiel com W-TinyLFU e outras políticas modernas, equalização de bytes, validação temporal e medição de custo computacional sob protocolo congelado.
