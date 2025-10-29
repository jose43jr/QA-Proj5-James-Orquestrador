import subprocess
import os
import datetime
import xml.etree.ElementTree as ET
import json

# ---------------------------
# Caminhos do Projeto 4 (Robot)
# ---------------------------

ROBOT_SUITE_PATH = r"H:\Cypress\projeto-04-robot-saucedemo\fluxo_login.robot"
ROBOT_WORKDIR = r"H:\Cypress\projeto-04-robot-saucedemo"
ROBOT_OUTPUT_XML = os.path.join(ROBOT_WORKDIR, "output.xml")

# ---------------------------
# Caminhos do Projeto 3 (API / Postman)
# ---------------------------

POSTMAN_COLLECTION = r"H:\Cypress\projeto-03-api-saucedemo\saucedemo-api.postman_collection.json"
POSTMAN_RESULT_JSON = r"H:\Cypress\projeto-03-api-saucedemo\resultado-postman.json"

# ---------------------------
# Caminhos do Projeto 2 (Cypress UI / Carrinho)
# ---------------------------

CYPRESS_WORKDIR = r"H:\Cypress\projeto-02-carrinho-saucedemo"
CYPRESS_SPEC = r"cypress/e2e/carrinho.cy.js"

# ---------------------------
# Relatório final do James
# ---------------------------

RELATORIO_PATH = "relatorio-execucao.md"


# =========
# ROBOT
# =========

def executar_robot():
    """
    Roda o Robot Framework na suíte de login e gera output.xml / report.html / log.html.
    """
    print("[James] Executando testes Robot Framework...")

    resultado = subprocess.run(
        ["robot", ROBOT_SUITE_PATH],
        cwd=ROBOT_WORKDIR,
        capture_output=True,
        text=True,
    )

    print("[James] Saída do Robot:")
    print(resultado.stdout)

    if resultado.returncode != 0:
        print("[James] Robot terminou com FALHA (returncode != 0).")
    else:
        print("[James] Robot terminou com SUCESSO (returncode == 0).")

    return resultado.returncode  # 0 = passou, diferente de 0 = falhou


def analisar_output_robot():
    """
    Lê o output.xml gerado pelo Robot e extrai:
    - nome do teste
    - status (PASS / FAIL)
    - mensagem de erro (se tiver)

    Retorna uma lista de dicionários com os resultados.
    """
    resultados = []

    if not os.path.exists(ROBOT_OUTPUT_XML):
        print("[James] output.xml não encontrado. Nada para analisar Robot.")
        return resultados

    tree = ET.parse(ROBOT_OUTPUT_XML)
    root = tree.getroot()

    for test in root.iter("test"):
        nome_teste = test.get("name", "SEM_NOME")

        status_tag = test.find("status")
        status = status_tag.get("status", "UNKNOWN") if status_tag is not None else "UNKNOWN"

        mensagem = ""
        if status != "PASS":
            if status_tag is not None and status_tag.text:
                mensagem = status_tag.text.strip()
            else:
                mensagem = "Falha sem mensagem detalhada capturada."

        resultados.append({
            "nome": nome_teste,
            "status": status,
            "mensagem": mensagem
        })

    return resultados


# =========
# API (POSTMAN / NEWMAN)
# =========

def executar_api_postman():
    """
    Roda a collection do Postman usando o Newman.
    Gera um arquivo JSON com o resultado da execução.
    """
    print("[James] Executando testes de API (Postman/Newman)...")

    comando = (
        f'newman run "{POSTMAN_COLLECTION}" '
        f'--reporters json '
        f'--reporter-json-export "{POSTMAN_RESULT_JSON}"'
    )

    resultado = subprocess.run(
        comando,
        capture_output=True,
        text=True,
        shell=True  # necessário no Windows pra achar "newman"
    )

    print("[James] Saída do Newman:")
    print(resultado.stdout)

    if resultado.returncode != 0:
        print("[James] Newman terminou com FALHA (returncode != 0).")
        print("[James] STDERR do Newman:")
        print(resultado.stderr)
    else:
        print("[James] Newman terminou com SUCESSO (returncode == 0).")

    return resultado.returncode  # 0 = passou, !=0 = falhou


def analisar_resultado_api():
    """
    Lê o arquivo JSON gerado pelo Newman e resume:
    - total de requisições
    - quantas falharam
    - status final (OK / FALHA)

    Retorna um dicionário com esse resumo.
    """
    if not os.path.exists(POSTMAN_RESULT_JSON):
        print("[James] resultado-postman.json não encontrado. Nada para analisar API.")
        return {
            "total_requests": 0,
            "failed_requests": 0,
            "status": "SEM_DADOS",
            "detalhes_erros": []
        }

    with open(POSTMAN_RESULT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    total_requests = data.get("run", {}).get("stats", {}).get("requests", {}).get("total", 0)
    failed_requests = data.get("run", {}).get("stats", {}).get("requests", {}).get("failed", 0)

    detalhes_erros = []
    if "run" in data and "executions" in data["run"]:
        for exec_data in data["run"]["executions"]:
            item_name = exec_data.get("item", {}).get("name", "SEM_NOME")
            assertions = exec_data.get("assertions", [])
            for a in assertions:
                if a.get("error"):
                    detalhes_erros.append({
                        "request": item_name,
                        "erro": a["error"].get("message", "Erro sem mensagem clara.")
                    })

    status_final = "OK" if failed_requests == 0 else "FALHA"

    return {
        "total_requests": total_requests,
        "failed_requests": failed_requests,
        "status": status_final,
        "detalhes_erros": detalhes_erros
    }


# =========
# CYPRESS (UI / CARRINHO)
# =========

def executar_cypress():
    """
    Roda o Cypress no projeto 2, headless, só na spec do carrinho.
    A ideia aqui é: dar uma validação visual/fluxo de compra.
    """
    print("[James] Executando testes de UI (Cypress - carrinho/checkout)...")

    comando = (
        f'npx cypress run --spec {CYPRESS_SPEC}'
    )

    resultado = subprocess.run(
    comando,
    cwd=CYPRESS_WORKDIR,      # roda dentro do projeto Cypress
    capture_output=True,
    text=True,
    shell=True,               # usa shell para achar npx/cypress
    encoding="utf-8",
    errors="ignore"
)


    print("[James] Saída do Cypress:")
    print(resultado.stdout)

    if resultado.returncode != 0:
        print("[James] Cypress terminou com FALHA (returncode != 0).")
        print("[James] STDERR do Cypress:")
        print(resultado.stderr)
        status_final = "FALHA"
    else:
        print("[James] Cypress terminou com SUCESSO (returncode == 0).")
        status_final = "OK"

    # Voltamos um resumo simples
    return {
        "status": status_final,
        "exit_code": resultado.returncode
    }


def analisar_resultado_cypress(resultado_bruto_cypress):
    """
    Recebe o dicionário vindo de executar_cypress() e devolve um resumo amigável.
    """
    if not resultado_bruto_cypress:
        return {
            "status": "SEM_DADOS",
            "detalhe": "Cypress não rodou ou não retornou resultado."
        }

    if resultado_bruto_cypress["status"] == "OK":
        return {
            "status": "OK",
            "detalhe": "Fluxo de UI (carrinho/checkout) executou sem erro de execução."
        }

    return {
        "status": "FALHA",
        "detalhe": "Cypress reportou falha na simulação de carrinho/checkout."
    }


# =========
# RELATÓRIO FINAL
# =========

def gerar_relatorio(resultados_robot, resultado_api, resumo_cypress):
    """
    Cria (ou sobrescreve) o arquivo relatorio-execucao.md
    com um resumo simples e direto do que aconteceu:
    - Robot (fluxo crítico de login)
    - API (Newman/Postman)
    - UI (Cypress carrinho/checkout)
    """
    agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linhas = []

    linhas.append(f"# Relatório de Execução - {agora}\n")

    # --- seção Robot ---
    linhas.append("## Resultados Robot Framework (Login SauceDemo)\n")
    if not resultados_robot:
        linhas.append("- Nenhum resultado lido do Robot.\n")
    else:
        for r in resultados_robot:
            linhas.append(f"- Teste: {r['nome']}")
            linhas.append(f"  - Status: {r['status']}")
            if r["status"] != "PASS":
                linhas.append(f"  - Detalhe: {r['mensagem']}")
            linhas.append("")

    # --- seção API ---
    linhas.append("## Resultados API (Postman / Newman)\n")
    if resultado_api["status"] == "SEM_DADOS":
        linhas.append("- Nenhum resultado lido do Newman.\n")
    else:
        linhas.append(f"- Total de requisições: {resultado_api['total_requests']}")
        linhas.append(f"- Falhas: {resultado_api['failed_requests']}")
        linhas.append(f"- Status geral da API: {resultado_api['status']}")
        linhas.append("")
        if resultado_api["detalhes_erros"]:
            linhas.append("Erros encontrados nas requisições:")
            for erro in resultado_api["detalhes_erros"]:
                linhas.append(f"  - Request: {erro['request']}")
                linhas.append(f"    Mensagem: {erro['erro']}")
            linhas.append("")
        else:
            linhas.append("Nenhum erro de validação reportado nas requisições.\n")

    # --- seção Cypress ---
    linhas.append("## Resultados UI (Cypress - Carrinho / Checkout)\n")
    linhas.append(f"- Status geral da UI: {resumo_cypress['status']}")
    linhas.append(f"- Detalhe: {resumo_cypress['detalhe']}")
    linhas.append("")

    linhas.append("\n---\n")
    linhas.append("Relatório gerado automaticamente pelo James (Projeto 05).")
    linhas.append("Robot = fluxo crítico de login")
    linhas.append("API = contrato/backend")
    linhas.append("Cypress = carrinho/checkout visual")
    linhas.append("")

    with open(RELATORIO_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))

    print(f"[James] Relatório gerado em {RELATORIO_PATH}")


# =========
# MAIN
# =========

def main():
    # 1. Robot
    executar_robot()
    resultados_robot = analisar_output_robot()

    # 2. API
    executar_api_postman()
    resultado_api = analisar_resultado_api()

    # 3. Cypress
    bruto_cypress = executar_cypress()
    resumo_cypress = analisar_resultado_cypress(bruto_cypress)

    # 4. Relatório final
    gerar_relatorio(resultados_robot, resultado_api, resumo_cypress)

    print("[James] Pronto.")


if __name__ == "__main__":
    main()
