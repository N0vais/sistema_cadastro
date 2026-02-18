import datetime
import os

def registrar_log(usuario, acao, data_login, data_logout="-"):
    arquivo_log = "log_sistema.txt"
    data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # Formato: [Data/Hora Login], Perfil, Nome, Ação, [Data/Hora Logout]
    linha_log = f"Login: {data_login} | Perfil: Admin | Usuário: {usuario} | Ação: {acao} | Logout: {data_logout}\n"
    
    with open(arquivo_log, "a", encoding="utf-8") as f:
        f.write(linha_log)