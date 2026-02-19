import pandas as pd
from datetime import datetime
import os
import json

RESET_LOG_FILE = 'resets_senha.csv'

def registrar_reset(usuario, adm_autorizador):
    """Registra o evento de redefinição de senha em um CSV próprio"""
    dados = {
        'Data/Hora': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        'Usuario_Resetado': usuario,
        'Admin_Autorizador': adm_autorizador
    }
    df = pd.DataFrame([dados])
    df.to_csv(RESET_LOG_FILE, mode='a', header=not os.path.exists(RESET_LOG_FILE), index=False, encoding='utf-8-sig')

def validar_admin_e_resetar(db_file, target_user, admin_user, admin_pass, nova_senha):
    """Valida se o autorizador é admin e altera a senha no JSON"""
    try:
        with open(db_file, "r") as f:
            users = json.load(f)

        # 1. Verifica se o admin existe e se a senha dele está correta
        if admin_user in users and users[admin_user]['senha'] == admin_pass:
            # 2. Verifica se quem está autorizando tem perfil de Administrador
            if users[admin_user].get('funcao') == "Administrador":
                # 3. Verifica se o usuário alvo existe
                if target_user in users:
                    users[target_user]['senha'] = nova_senha
                    with open(db_file, "w") as f:
                        json.dump(users, f, indent=4)
                    
                    registrar_reset(target_user, admin_user)
                    return True, "Senha alterada com sucesso!"
                return False, "Usuário alvo não encontrado."
            return False, "Autorização negada: Usuário não é Administrador."
        return False, "Credenciais do Administrador inválidas."
    except Exception as e:
        return False, f"Erro no banco: {e}"