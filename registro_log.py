import pandas as pd
from datetime import datetime
import os

LOG_FILE = 'data/logs_sistema.csv'

def registrar_acao(usuario, perfil, acao, data_logout=""):
    """
    Salva uma nova ação no CSV com as colunas:
    Data/Hora Login, Perfil, Usuário, Ação, Data/Hora Logout
    """
    # Criamos o dicionário com a estrutura exata solicitada
    dados_log = {
        'Data/Hora Login': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        'Perfil': perfil,
        'Usuário': usuario,
        'Ação': acao,
        'Data/Hora Logout': data_logout  # Geralmente vazio, exceto no encerramento
    }
    
    log_entry = pd.DataFrame([dados_log])
    
    try:
        # mode='a' adiciona ao final; header=not os.path.exists só cria cabeçalho se o arquivo for novo
        log_entry.to_csv(LOG_FILE, mode='a', header=not os.path.exists(LOG_FILE), index=False, encoding='utf-8-sig')
    except PermissionError:
        print("Erro: O arquivo de log está aberto por outro programa.")

def buscar_ultimos_logs(filtro="", quantidade=30):
    """Retorna os logs filtrados de forma otimizada"""
    if not os.path.exists(LOG_FILE):
        return []

    try:
        # Lemos o CSV garantindo que as colunas sejam strings para o filtro funcionar
        df = pd.read_csv(LOG_FILE).fillna("")
        
        if filtro:
            # Filtra em múltiplas colunas (Ação, Usuário ou Perfil)
            mask = (df['Ação'].astype(str).str.contains(filtro, case=False)) | \
                   (df['Usuário'].astype(str).str.contains(filtro, case=False)) | \
                   (df['Perfil'].astype(str).str.contains(filtro, case=False))
            df = df[mask]
        
        # Pega os últimos registros, inverte para mostrar o mais recente primeiro e converte para dicionário
        return df.tail(quantidade).iloc[::-1].to_dict('records')
        
    except Exception as e:
        print(f"Erro ao ler logs: {e}")
        return []

def registrar_logout(usuario, perfil, hora_entrada):
    """Função específica para registrar o encerramento da sessão"""
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    dados_log = {
        'Data/Hora Login': hora_entrada,
        'Perfil': perfil,
        'Usuário': usuario,
        'Ação': "Sessão Finalizada",
        'Data/Hora Logout': agora
    }
    pd.DataFrame([dados_log]).to_csv(LOG_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')