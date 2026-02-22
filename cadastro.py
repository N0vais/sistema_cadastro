
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

        # 2. Coleta de dados dos inputs
        user = reg_user.get().strip() # .strip() remove espaços vazios acidentais
        func = funcao_var.get()
        pw = reg_pass.get()
        pwc = reg_pass_confirm.get()
        senha_adm_digitada = reg_administrador.get()

            # --- NOVA VALIDAÇÃO DE COMPLEXIDADE DE SENHA ---
        padrao_senha = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[#!@$%^&*]).{6,}$"

        # 3. Validações de preenchimento básico
        if not all([user, pw, senha_adm_digitada]):
            error_label.configure(text="Preencha todos os campos!", text_color="#FF4B4B")
            return
        if not re.match(padrao_senha, pw):
            error_label.configure(
                text="Senha fraca! Use: Maiúscula, Minúscula, Número e #", 
                text_color="#FF4B4B")
            reg_pass.configure(border_color="#FF4B4B")
            return

        if pw != pwc:
            error_label.configure(text="Senhas não conferem!", text_color="#FF4B4B")
            reg_pass_confirm.configure(border_color="#FF4B4B", border_width=1)
            return

        # 4. Processamento de Dados (JSON)
        try:
            with open(root.db_file, "r", encoding='utf-8') as f:
                data = json.load(f)
            
            # --- NOVA VERIFICAÇÃO: USUÁRIO JÁ EXISTE? ---
            if user in data:
                error_label.configure(text="Usuário já cadastrado!", text_color="#FF4B4B")
                reg_user.configure(border_color="#FF4B4B", border_width=1)
                return

            # 5. Validação do Administrador
            nome_adm_autorizador = None
            funcao_adm_autorizador = None
            
            for nome_chave, info in data.items():
                if info.get("funcao") == "Administrador" and info.get("senha") == senha_adm_digitada:
                    nome_adm_autorizador = nome_chave
                    funcao_adm_autorizador = info.get("funcao")
                    break
            
            if not nome_adm_autorizador:
                error_label.configure(text="Senha de administrador inválida!", text_color="#FF4B4B")
                reg_administrador.configure(border_color="#FF4B4B", border_width=1)
                return

            # 6. Criar registro e salvar no JSON
            agora = datetime.now()
            data_f = agora.strftime("%d/%m/%Y")
            hora_f = agora.strftime("%H:%M:%S")

            data[user] = {
                "senha": pw, 
                "funcao": func, 
                "adm": nome_adm_autorizador, 
                "data_criacao": data_f,
                "hora_criacao": hora_f
            }
            
            with open(root.db_file, "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            # 7. Sistema de Logs (CSV)
            log_path = 'data/logs_sistema.csv'
            os.makedirs(os.path.dirname(log_path), exist_ok=True)
            
            mensagem_log = f"{funcao_adm_autorizador} '{nome_adm_autorizador}' cadastrou o usuario '{user}' como '{func}'"
            arquivo_existe = os.path.exists(log_path)
            
            with open(log_path, 'a', newline='', encoding='utf-8') as f_log:
                escritor = csv.writer(f_log)
                if not arquivo_existe:
                    escritor.writerow(["Data", "Hora", "Evento"])
                escritor.writerow([data_f, hora_f, mensagem_log])

            # 8. Finalização com sucesso
            error_label.configure(text="Cadastro realizado com sucesso!", text_color="#00FF88")
            root.after(1000, root.show_login_screen)

        except Exception as e:
            error_label.configure(text=f"Erro: {e}", text_color="#FF4B4B")
    
# Botao cadastrar
    ctk.CTkButton(frame, text="REGISTRAR",
        corner_radius=10, fg_color="#00D2FF", hover_color="#0095B3",
        width=280, height=45, text_color="#000000", font=("Segoe UI", 14, "bold"),
    command=salvar_cadastro).pack(pady=20)
    
    ctk.CTkButton(frame, text="Voltar ao Login", fg_color="transparent", command=root.show_login_screen).pack()

