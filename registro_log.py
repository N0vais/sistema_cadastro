import pandas as pd
from datetime import datetime
import os

LOG_FILE = 'logs_sistema.csv'

def registrar_acao(acao):
    """Salva uma nova ação no CSV"""
    log_entry = pd.DataFrame([{
        'Data/Hora': datetime.now().strftime("%d/%m/%Y  %H:%M:%S"),
        'Usuário': 'Admin',
        'Ação': acao
    }])
    log_entry.to_csv(LOG_FILE, mode='a', header=not os.path.exists(LOG_FILE), index=False)

def buscar_ultimos_logs(filtro="", quantidade=5):
    """Retorna os logs filtrados do arquivo CSV"""
    if not os.path.exists(LOG_FILE):
        return []

    try:
        df = pd.read_csv(LOG_FILE)
        
        # Filtro por nome ou data
        if filtro:
            df = df[df['Ação'].str.contains(filtro, case=False) | 
                    df['Data/Hora'].str.contains(filtro)]
        
        # Pega os últimos e converte para uma lista de dicionários
        ultimos = df.tail(quantidade).to_dict('records')
        return ultimos
    except Exception as e:
        print(f"Erro ao ler logs: {e}")
        return []