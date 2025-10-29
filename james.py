import subprocess
import os
import datetime
import xml.etree.ElementTree as ET

# Caminhos do Projeto 4 (Robot Framework)
ROBOT_SUITE_PATH = r"H:\Cypress\projeto-04-robot-saucedemo\fluxo_login.robot"
ROBOT_WORKDIR = r"H:\Cypress\projeto-04-robot-saucedemo"
ROBOT_OUTPUT_XML = os.path.join(ROBOT_WORKDIR, "output.xml")

# Relatório que o James vai gerar aqui no Projeto 5
RELATORIO_PATH = "relatorio-execucao.md"


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
        print("[James] output.xml não encontrado. Nada para analisar.")
        return resultados

    tree = ET.parse(ROBOT_OUTPUT_XML)
    root = tree.getroot()

    # Cada caso de teste aparece em <test>
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


def gerar_relatorio(resultados_robot):
    """
    Cria (ou sobrescreve) o arquivo relatorio-execucao.md
    com um resumo simples e direto do que aconteceu.
    """
    agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    linhas = []
    linhas.append(f"# Relatório de Execução - {agora}\n")
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

    linhas.append("\n---\n")
    linhas.append("Este relatório foi gerado automaticamente pelo James (Projeto 05).")
    linhas.append("Próxima etapa: integrar Cypress e API.\n")

    with open(RELATORIO_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))

    print(f"[James] Relatório gerado em {RELATORIO_PATH}")


def main():
    executar_robot()
    resultados_robot = analisar_output_robot()
    gerar_relatorio(resultados_robot)
    print("[James] Pronto.")


if __name__ == "__main__":
    main()
