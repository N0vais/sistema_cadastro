import json
import os

def realizar_login(usuario_digitado, senha_digitada):
    db_file = "data/self.db_file" # O caminho que você definiu no self.db_file

    # 1. Verificar se o arquivo existe para não dar erro de "File Not Found"
    if not os.path.exists(db_file):
        print("Erro: Banco de dados não encontrado!")
        return False

    try:
        # 2. Abrir e carregar os dados
        with open(db_file, "r") as f:
            data = json.load(f)

        # 3. Verificar se o usuário existe no dicionário
        if usuario_digitado in data:
            # 4. Recuperar os dados do usuário encontrado
            dados_usuario = data[usuario_digitado]
            senha_salva = dados_usuario["senha"]
            funcao = dados_usuario["funcao"]
            nome_adm = dados_usuario["adm"]

            # 5. Comparar a senha
            if senha_digitada == senha_salva:
                print(f"Login bem-sucedido! Bem-vindo {usuario_digitado} ({funcao})")
                print(f"Cadastrado por: {nome_adm}")
                return True, dados_usuario
            else:
                print("Senha incorreta!")
                return False, "Senha incorreta"
        else:
            print("Usuário não encontrado!")
            return False, "Usuário não encontrado"

    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return False, str(e)
    