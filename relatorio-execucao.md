!relatorio-execucao.md

# Relatório de Execução - 2025-10-29 18:20:26

## Resultados Robot Framework (Login SauceDemo)

- Teste: Login Válido - Usuário Standard
  - Status: PASS

## Resultados API (Postman / Newman)

- Total de requisições: 4
- Falhas: 4
- Status geral da API: FALHA

Erros encontrados nas requisições:

- Request: Login - Sucesso
  Mensagem: expected PostmanResponse{ …(5) } to have property 'code'
- Request: Login - Sucesso
  Mensagem: "undefined" is not valid JSON
- Request: Login - Sucesso
  Mensagem: "undefined" is not valid JSON
- Request: Login - Credenciais inválidas
  Mensagem: expected PostmanResponse{ …(5) } to have property 'code'
- Request: Login - Credenciais inválidas
  Mensagem: "undefined" is not valid JSON
- Request: Login - Credenciais inválidas
  Mensagem: "undefined" is not valid JSON
- Request: Carrinho - Adicionar item
  Mensagem: expected PostmanResponse{ …(5) } to have property 'code'
- Request: Carrinho - Adicionar item
  Mensagem: "undefined" is not valid JSON
- Request: Carrinho - Adicionar item
  Mensagem: "undefined" is not valid JSON
- Request: Checkout - Iniciar
  Mensagem: expected PostmanResponse{ …(5) } to have property 'code'
- Request: Checkout - Iniciar
  Mensagem: "undefined" is not valid JSON

## Resultados UI (Cypress - Carrinho / Checkout)

- Status geral da UI: OK
- Detalhe: Fluxo de UI (carrinho/checkout) executou sem erro de execução.

---

Relatório gerado automaticamente pelo James (Projeto 05).
Robot = fluxo crítico de login
API = contrato/backend
Cypress = carrinho/checkout visual
