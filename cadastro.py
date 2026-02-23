
from datetime import datetime
import re
import customtkinter as ctk
import json
import csv
import os


    # --- TELA DE CADASTRO ---
def show_register_screen(root):

    for widget in root.container.winfo_children():
        widget.destroy()

    frame = ctk.CTkFrame(root.container, corner_radius=20, border_width=2, border_color="#3d3d3d")
    frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.9)

    ctk.CTkLabel(frame, text="NOVO ACESSO",
        font=("Orbitron", 30, "bold"), text_color="#00D2FF").pack(pady=(40, 15))

    reg_user = ctk.CTkEntry(frame, placeholder_text="Nome de Usuário",
        width=350, height=50, border_color="#333333", fg_color="#1a1a1a", font=("Segoe UI", 20))
    reg_user.pack(pady=8)
        
# Senha
    reg_pass = ctk.CTkEntry(frame, placeholder_text="Senha (mín. 6)", 
        show="*", width=350, height=50, border_color="#333333", fg_color="#1a1a1a", font=("Segoe UI", 20))
    reg_pass.pack(pady=8)

# Confirme Senha
    reg_pass_confirm = ctk.CTkEntry(frame, placeholder_text="Confirmar Senha", 
        show="*", width=350, height=50, border_color="#333333", fg_color="#1a1a1a", font=("Segoe UI", 20))
    reg_pass_confirm.pack(pady=8)

# Campo de Função (OptionMenu para Hierarquia)
    funcao_var = ctk.StringVar(value="Nível de Acesso") # Texto inicial dentro do botão
    reg_func = ctk.CTkOptionMenu(frame, values=["Administrador", "Usuario" ], 
        variable=funcao_var, width=170, height=30, fg_color="#555",
        button_color="#1a1a1a", 
        button_hover_color="#555",
        dropdown_fg_color="#1a1a1a", # Cor do fundo do menu ao abrir
        dropdown_hover_color="#333",
        dropdown_text_color="#00D2FF",font=("Segoe UI", 14),
        anchor="center")
    reg_func.pack(pady=12)

# Senha do Adiministrador
    reg_administrador = ctk.CTkEntry(frame, placeholder_text="Senha do Administrador", 
        show="#", width=170, height=30, border_color="#333333", fg_color="#1a1a1a", font=("Segoe UI", 14))
    reg_administrador.pack(pady=8)

# Menssagen de erro
    error_label = ctk.CTkLabel(frame, text="", font=("Segoe UI", 18))
    error_label.pack(pady=2)

     

    def salvar_cadastro():
        # 1. Reset visual dos campos
        error_label.configure(text="")
        for widget in [reg_user, reg_pass, reg_pass_confirm, reg_administrador]:
            widget.configure(border_color="#949494", border_width=1)

        # 2. Coleta de dados
        user = reg_user.get().strip()
        func = funcao_var.get()
        pw = reg_pass.get()
        pwc = reg_pass_confirm.get()
        senha_adm_digitada = reg_administrador.get()

        # --- VALIDAÇÕES RÍGIDAS (Se falhar aqui, o 'return' impede a gravação) ---
        
        if not all([user, pw, senha_adm_digitada]) or func == "Nível de Acesso":
            error_label.configure(text="Preencha todos os campos obrigatórios!", text_color="#FF4B4B")
            return

        # Validação de Complexidade de Senha
        padrao_senha = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[#!@$%^&*]).{6,}$"
        if not re.match(padrao_senha, pw):
            error_label.configure(text="Senha fraca! Use: A, a, 1 e #", text_color="#FF4B4B")
            reg_pass.configure(border_color="#FF4B4B")
            return

        if pw != pwc:
            error_label.configure(text="As senhas não coincidem!", text_color="#FF4B4B")
            reg_pass_confirm.configure(border_color="#FF4B4B")
            return

        # 4. Processamento de Dados
        try:
            # Carregar banco de dados
            if not os.path.exists(root.db_file):
                with open(root.db_file, "w") as f:
                    json.dump({}, f)

            with open(root.db_file, "r", encoding='utf-8') as f:
                data = json.load(f)
            
            # Verificar se usuário já existe
            if user in data:
                error_label.configure(text="Este nome de usuário já existe!", text_color="#FF4B4B")
                reg_user.configure(border_color="#FF4B4B")
                return

            # 5. Validação do Administrador (Busca no Banco)
            nome_adm_autorizador = None
            funcao_adm_autorizador = None
            
            for nome_chave, info in data.items():
                if info.get("funcao") == "Administrador" and info.get("senha") == senha_adm_digitada:
                    nome_adm_autorizador = nome_chave
                    funcao_adm_autorizador = info.get("funcao")
                    break
            
            if not nome_adm_autorizador:
                error_label.configure(text="Senha de ADM incorreta ou não encontrado!", text_color="#FF4B4B")
                reg_administrador.configure(border_color="#FF4B4B")
                return

            # --- SÓ CHEGA AQUI SE TUDO ESTIVER 100% CORRETO ---
            
            agora = datetime.now()
            data_f = agora.strftime("%d/%m/%Y")
            hora_f = agora.strftime("%H:%M:%S")

            # Grava no Dicionário
            data[user] = {
                "senha": pw, 
                "funcao": func, 
                "adm": nome_adm_autorizador, 
                "data_criacao": data_f,
                "hora_criacao": hora_f
            }
            
            # Salva no arquivo JSON
            with open(root.db_file, "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            # --- 7. Sistema de Logs (Formato de Texto Puro para Dashboard) ---
            log_path = 'data/logs_sistema.csv'
            os.makedirs(os.path.dirname(log_path), exist_ok=True)
            
            # Formato padronizado que você pediu: [Data Hora] Função - Nome: Ação
            linha_log = f"[{data_f} {hora_f}] {funcao_adm_autorizador} {nome_adm_autorizador}: cadastrou o usuario '{user}' como '{func}'\n"
            
            with open(log_path, 'a', encoding='utf-8') as f_log:
                f_log.write(linha_log)

            # 8. Feedback de Sucesso Final
            error_label.configure(text="CADASTRO REALIZADO!", text_color="#00FF88")
            root.after(1500, root.show_login_screen)

        except json.JSONDecodeError:
            error_label.configure(text="Erro crítico: Arquivo de banco corrompido!", text_color="#FF4B4B")
        except Exception as e:
            error_label.configure(text=f"Erro inesperado: {e}", text_color="#FF4B4B")
    
# Botao cadastrar
    ctk.CTkButton(frame, text="REGISTRAR",
        corner_radius=10, fg_color="#00D2FF", hover_color="#0095B3",
        width=280, height=45, text_color="#000000", font=("Segoe UI", 14, "bold"),
    command=salvar_cadastro).pack(pady=20)
    
    ctk.CTkButton(frame, text="Voltar ao Login", fg_color="transparent", command=root.show_login_screen).pack()

