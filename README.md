# Projeto 05 – James (Assistente de QA)

James é um orquestrador de QA. A ideia é simples: rodar testes automaticamente, coletar o resultado e gerar um relatório pronto para enviar ao time (ex: dev).

Este projeto faz três coisas:

1. Executa testes automatizados existentes:

   - Testes de interface web (Cypress)
   - Testes funcionais de fluxo crítico (Robot Framework)
   - Testes de API (coleção Postman executada via Newman)

2. Lê os resultados de cada teste:

   - PASS / FAIL
   - Onde falhou
   - Qual parte do negócio foi impactada (ex: “checkout não finaliza → ninguém consegue comprar”)

3. Gera um relatório `.md` consolidado da execução.

A ideia é que você rode um único comando e receba um resumo do estado da qualidade do produto.

---

## Visão geral

Por enquanto a versão é local e sem IA. O script `james.py` faz:

- roda Robot Framework (`robot fluxo_login.robot`)
- roda Cypress (`npx cypress run ...`)
- roda API pelo Newman (`newman run ...`)
- junta os resultados
- cria `relatorio-execucao.md`

Depois, em uma versão futura, o James vai:

- interpretar o impacto (negócio bloqueado ou não)
- preparar texto de reporte para o desenvolvedor
- e opcionalmente montar e-mail automático

---

## Requisitos técnicos

Para rodar o James, precisamos ter instalado na máquina:

- Python (rodando no ambiente base do Miniconda)
- Robot Framework (projeto 04)
- Cypress (projeto 01 e 02)
- Node.js / npm
- Newman (runner de coleção Postman)
- Coleção Postman de API exportada (`saucedemo-api.postman_collection.json`)

O script `james.py` vai chamar essas ferramentas via linha de comando, capturar a saída e gerar o relatório final.

---

## Próximo passo

1. Criar o arquivo `james.py`
2. Fazer ele rodar o teste Robot do login e registrar PASS/FAIL no relatório

Depois disso, vamos integrar Cypress e Newman.
