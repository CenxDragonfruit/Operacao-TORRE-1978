import argparse
import csv
from datetime import datetime
import os
import glob

# --- Funções Auxiliares ---

def handle_limpar(args):
    """Limpa os arquivos gerados pela simulação (logs, filas e relatórios)."""
    print("--- INICIANDO LIMPEZA DOS ARQUIVOS GERADOS ---")
    arquivos_para_esvaziar = [
        'logs/torre.log',
        'dados/fila_decolagem.txt',
        'dados/fila_pouso.txt'
    ]
    for arquivo in arquivos_para_esvaziar:
        open(arquivo, 'w').close()
        print(f"- Arquivo '{arquivo}' foi limpo.")
    relatorios_antigos = glob.glob('relatorios/operacao_*.txt')
    if not relatorios_antigos:
        print("- Nenhum relatório antigo para remover.")
    else:
        for relatorio in relatorios_antigos:
            os.remove(relatorio)
            print(f"- Relatório '{relatorio}' foi removido.")
    print("\nLimpeza concluída com sucesso!")
    return

def escrever_log(mensagem):
    """Escreve uma mensagem com data/hora no arquivo de log."""
    with open("logs/torre.log", "a", encoding="utf-8") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {mensagem}\n")

# ... (todas as outras funções de carregar, ler_fila, verificar_notam continuam aqui, inalteradas)
def carregar_planos_de_voo(caminho_arquivo):
    try:
        with open(caminho_arquivo, mode='r', encoding='utf-8') as arquivo_csv:
            leitor_csv = csv.DictReader(arquivo_csv)
            return list(leitor_csv)
    except FileNotFoundError:
        escrever_log(f"ERRO CRÍTICO: Arquivo de planos de voo não encontrado em '{caminho_arquivo}'")
        return []

def carregar_pistas(caminho_arquivo):
    pistas = {}
    try:
        with open(caminho_arquivo, mode='r', encoding='utf-8') as arquivo_txt:
            for linha in arquivo_txt:
                nome, status = linha.strip().split(',')
                pistas[nome] = status
            return pistas
    except FileNotFoundError:
        escrever_log(f"ERRO CRÍTICO: Arquivo de pistas não encontrado em '{caminho_arquivo}'")
        return {}

def carregar_frota(caminho_arquivo):
    try:
        with open(caminho_arquivo, mode='r', encoding='utf-8') as arquivo_csv:
            leitor_csv = csv.DictReader(arquivo_csv)
            return list(leitor_csv)
    except FileNotFoundError:
        escrever_log(f"ERRO CRÍTICO: Arquivo da frota não encontrado em '{caminho_arquivo}'")
        return []

def carregar_pilotos(caminho_arquivo):
    try:
        with open(caminho_arquivo, mode='r', encoding='utf-8') as arquivo_csv:
            leitor_csv = csv.DictReader(arquivo_csv)
            return list(leitor_csv)
    except FileNotFoundError:
        escrever_log(f"ERRO CRÍTICO: Arquivo de pilotos não encontrado em '{caminho_arquivo}'")
        return []

def carregar_ocorrencias(caminho_arquivo):
    try:
        with open(caminho_arquivo, mode='r', encoding='utf-8') as arquivo_txt:
            return [linha.strip() for linha in arquivo_txt.readlines()]
    except FileNotFoundError:
        escrever_log(f"ERRO CRÍTICO: Arquivo de ocorrências não encontrado em '{caminho_arquivo}'")
        return []

def ler_fila(caminho_arquivo):
    try:
        with open(caminho_arquivo, mode='r', encoding='utf-8') as arquivo_txt:
            return [linha.strip() for linha in arquivo_txt.readlines()]
    except FileNotFoundError:
        return []

def verificar_notam_pista(pista, notams, hora_atual_simulada):
    for notam in notams:
        if f"PISTA {pista} FECHADA" in notam:
            partes = notam.split()
            periodo = partes[3]
            hora_inicio_str, hora_fim_str = periodo.split('-')
            hora_inicio = datetime.strptime(hora_inicio_str, "%H:%M").time()
            hora_fim = datetime.strptime(hora_fim_str, "%H:%M").time()
            if hora_inicio <= hora_atual_simulada <= hora_fim:
                return True
    return False


# --- Lógica Principal da CLI ---

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Operação TORRE 1978 - CLI de Controle de Tráfego Aéreo.")
    subparsers = parser.add_subparsers(dest='command', required=True, help='Subcomandos disponíveis')
    parser_listar = subparsers.add_parser('listar', help='Lista os planos de voo cadastrados.')
    parser_listar.add_argument('--por', type=str, default='etd', choices=['voo', 'etd', 'tipo', 'prioridade'], help='Critério de ordenação da listagem.')
    parser_importar = subparsers.add_parser('importar-dados', help='Importa e valida os arquivos de dados iniciais.')
    parser_enfileirar = subparsers.add_parser('enfileirar', help='Adiciona um voo a uma das filas (pouso ou decolagem).')
    parser_enfileirar.add_argument('fila', choices=['decolagem', 'pouso'], help='O nome da fila (decolagem ou pouso).')
    parser_enfileirar.add_argument('--voo', type=str, required=True, help='O código do voo a ser enfileirado (ex: ALT123).')
    parser_autorizar = subparsers.add_parser('autorizar', help='Autoriza a próxima operação de uma fila para uma pista.')
    parser_autorizar.add_argument('operacao', choices=['decolagem', 'pouso'], help='O tipo de operação a ser autorizada.')
    parser_autorizar.add_argument('--pista', type=str, required=True, help='A pista a ser utilizada (ex: 10/28).')
    parser_status = subparsers.add_parser('status', help='Exibe o status atual das pistas, filas e ocorrências.')
    parser_relatorio = subparsers.add_parser('relatorio', help='Gera o relatório final do turno de operação.')
    parser_limpar = subparsers.add_parser('limpar', help='Limpa os arquivos gerados (logs, filas, relatórios).')
    args = parser.parse_args()

    if args.command == 'listar':
        planos_de_voo = carregar_planos_de_voo('dados/planos_voo.csv')
        # ... (código do listar continua igual)
        if not planos_de_voo:
            print("Nenhum plano de voo para exibir.")
        else:
            chave_ordenacao = args.por
            ordem_reversa = True if chave_ordenacao == 'prioridade' else False
            planos_de_voo.sort(key=lambda voo: voo[chave_ordenacao], reverse=ordem_reversa)
            print(f"{'Voo':<10} {'Origem':<8} {'Destino':<8} {'ETD':<8} {'ETA':<8} {'Aeronave':<10} {'Tipo':<12} {'Prioridade':<5}")
            print("-" * 80)
            for voo in planos_de_voo:
                print(f"{voo['voo']:<10} {voo['origem']:<8} {voo['destino']:<8} {voo['etd']:<8} {voo['eta']:<8} {voo['aeronave']:<10} {voo['tipo']:<12} {voo['prioridade']:<5}")
    
    elif args.command == 'importar-dados':
        # ... (código do importar-dados continua igual)
        print("--- VERIFICANDO ARQUIVOS DE DADOS ---")
        arquivos_necessarios = [
            'dados/planos_voo.csv', 'dados/pistas.txt', 'dados/frota.csv',
            'dados/pilotos.csv', 'dados/metar.txt', 'dados/notam.txt'
        ]
        todos_existem = True
        for arquivo in arquivos_necessarios:
            if not os.path.exists(arquivo):
                msg = f"FALHA NA VERIFICAÇÃO: Arquivo não encontrado: {arquivo}"
                print(msg)
                escrever_log(msg)
                todos_existem = False
        if todos_existem:
            msg = "SUCESSO: Todos os arquivos de dados necessários foram encontrados."
            print(msg)
            escrever_log(msg)
    
    elif args.command == 'enfileirar':
        # ... (código do enfileirar continua igual)
        voo_codigo = args.voo.upper()
        fila_alvo = f"dados/fila_{args.fila}.txt"
        planos = carregar_planos_de_voo('dados/planos_voo.csv')
        pilotos = carregar_pilotos('dados/pilotos.csv')
        fila_atual = ler_fila(fila_alvo)
        voo_info = next((v for v in planos if v['voo'] == voo_codigo), None)
        if not voo_info:
            msg = f"FALHA AO ENFILEIRAR: Voo {voo_codigo} não encontrado nos planos de voo."
            print(msg)
            escrever_log(msg)
        else:
            if voo_codigo in fila_atual:
                msg = f"FALHA AO ENFILEIRAR: Voo {voo_codigo} já está na fila de {args.fila}."
                print(msg)
                escrever_log(msg)
            else:
                aeronave = voo_info['aeronave']
                piloto_info = next((p for p in pilotos if p['habilitacao'] == aeronave), None)
                licenca_valida = True
                if piloto_info:
                    validade_licenca = datetime.strptime(piloto_info['validade'], "%Y-%m-%d").date()
                    data_operacao = datetime(1978, 12, 31).date()
                    if validade_licenca < data_operacao:
                        licenca_valida = False
                        msg = f"FALHA AO ENFILEIRAR: Licença do piloto para a aeronave {aeronave} (Voo {voo_codigo}) está VENCIDA ({validade_licenca})."
                        print(msg)
                        escrever_log(msg)
                else:
                    licenca_valida = False
                    msg = f"FALHA AO ENFILEIRAR: Nenhum piloto habilitado para a aeronave {aeronave} (Voo {voo_codigo}) encontrado."
                    print(msg)
                    escrever_log(msg)
                if licenca_valida:
                    with open(fila_alvo, "a", encoding="utf-8") as f:
                        f.write(f"{voo_codigo}\n")
                    msg = f"SUCESSO: Voo {voo_codigo} adicionado à fila de {args.fila}."
                    print(msg)
                    escrever_log(msg)
    
    elif args.command == 'autorizar':
        # ... (código do autorizar continua igual)
        operacao = args.operacao
        pista_selecionada = args.pista
        fila_alvo = f"dados/fila_{operacao}.txt"
        HORA_ATUAL_SIMULADA = datetime.strptime("14:30", "%H:%M").time()
        fila = ler_fila(fila_alvo)
        pistas = carregar_pistas('dados/pistas.txt')
        notams = carregar_ocorrencias('dados/notam.txt')
        if not fila:
            msg = f"NEGADO: Não há voos na fila de {operacao} para autorizar."
            print(msg)
            escrever_log(msg)
        else:
            voo_para_autorizar = fila[0]
            status_pista = pistas.get(pista_selecionada, "INEXISTENTE")
            if status_pista != 'ABERTA':
                msg = f"NEGADO: Voo {voo_para_autorizar} não autorizado. Pista {pista_selecionada} está {status_pista}."
                print(msg)
                escrever_log(msg)
            elif verificar_notam_pista(pista_selecionada, notams, HORA_ATUAL_SIMULADA):
                msg = f"NEGADO: Voo {voo_para_autorizar} não autorizado. Pista {pista_selecionada} fechada por NOTAM no horário atual."
                print(msg)
                escrever_log(msg)
            else:
                fila.pop(0)
                with open(fila_alvo, "w", encoding="utf-8") as f:
                    for voo in fila:
                        f.write(f"{voo}\n")
                msg = f"AUTORIZADO: {operacao.upper()} do voo {voo_para_autorizar} na pista {pista_selecionada}."
                print(msg)
                escrever_log(msg)
    
    elif args.command == 'status':
        # ... (código do status continua igual)
        print("--- STATUS DA TORRE ---")
        print("\n[ STATUS DAS PISTAS ]")
        pistas = carregar_pistas('dados/pistas.txt')
        if not pistas:
            print("Nenhuma informação de pista disponível.")
        else:
            for nome, status_pista in pistas.items():
                print(f"- Pista {nome}: {status_pista}")
        fila_pouso = ler_fila('dados/fila_pouso.txt')
        fila_decolagem = ler_fila('dados/fila_decolagem.txt')
        print("\n[ FILAS DE OPERAÇÃO ]")
        print(f"- Voos na fila de POUSO: {len(fila_pouso)}")
        if fila_pouso:
            print(f"  Próximos: {', '.join(fila_pouso[:3])}")
        print(f"- Voos na fila de DECOLAGEM: {len(fila_decolagem)}")
        if fila_decolagem:
            print(f"  Próximos: {', '.join(fila_decolagem[:3])}")
        print("\n[ OCORRÊNCIAS ATIVAS ]")
        metar = carregar_ocorrencias('dados/metar.txt')
        notam = carregar_ocorrencias('dados/notam.txt')
        print("- METAR (Clima):")
        if not metar:
            print("  Nenhum boletim METAR recente.")
        else:
            print(f"  {metar[-1]}")
        print("- NOTAM (Avisos):")
        if not notam:
            print("  Nenhum NOTAM ativo.")
        else:
            for aviso in notam:
                print(f"  {aviso}")

    elif args.command == 'relatorio':
        # ... (código do relatorio continua igual)
        print("--- GERANDO RELATÓRIO DE OPERAÇÃO ---")
        try:
            with open('logs/torre.log', 'r', encoding='utf-8') as f:
                log_completo = f.readlines()
        except FileNotFoundError:
            print("Arquivo de log não encontrado. Nenhuma operação para relatar.")
        else:
            autorizados = 0
            negados = 0
            motivos_negacao = {}
            for linha in log_completo:
                if "AUTORIZADO:" in linha:
                    autorizados += 1
                elif "NEGADO:" in linha or "FALHA" in linha:
                    negados += 1
                    if "Pista" in linha and "fechada por NOTAM" in linha:
                        motivo = "Pista Fechada (NOTAM)"
                    elif "Pista" in linha and ("FECHADA" in linha or "INEXISTENTE" in linha):
                        motivo = "Status de Pista Inválido"
                    elif "Licença" in linha and "VENCIDA" in linha:
                        motivo = "Licença de Piloto Vencida"
                    else:
                        motivo = "Outro"
                    motivos_negacao[motivo] = motivos_negacao.get(motivo, 0) + 1
            nome_arquivo_relatorio = datetime.now().strftime("relatorios/operacao_%Y%m%d.txt")
            with open(nome_arquivo_relatorio, 'w', encoding='utf-8') as f:
                f.write("--- RELATÓRIO DE OPERAÇÃO DA TORRE ---\n")
                f.write(f"Data de Geração: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("\n--- SUMÁRIO DE AUTORIZAÇÕES ---\n")
                f.write(f"Total de Operações Autorizadas: {autorizados}\n")
                f.write(f"Total de Operações Negadas: {negados}\n")
                f.write("\n--- MOTIVOS DE RECUSA ---\n")
                if not motivos_negacao:
                    f.write("Nenhuma recusa registrada.\n")
                else:
                    for motivo, contagem in motivos_negacao.items():
                        f.write(f"- {motivo}: {contagem} vez(es)\n")
            msg = f"SUCESSO: Relatório gerado em '{nome_arquivo_relatorio}'"
            print(msg)
            escrever_log(msg)

    elif args.command == 'limpar':
        handle_limpar(args)
