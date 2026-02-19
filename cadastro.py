import customtkinter as ctk
import json

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
        show="•", width=350, height=50, border_color="#333333", fg_color="#1a1a1a", font=("Segoe UI", 20))
    reg_pass.pack(pady=8)

# Confirme Senha
    reg_pass_confirm = ctk.CTkEntry(frame, placeholder_text="Confirmar Senha", 
        show="•", width=350, height=50, border_color="#333333", fg_color="#1a1a1a", font=("Segoe UI", 20))
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
        error_label.configure(text="")
        reg_user.configure(border_color="#949494", border_width=1)
        reg_pass.configure(border_color="#949494", border_width=1)
        reg_pass_confirm.configure(border_color="#949494", border_width=1)
        reg_administrador.configure(border_color="#949494", border_width=1)

        user = reg_user.get()
        func = funcao_var.get()
        pw = reg_pass.get()
        pwc = reg_pass_confirm.get()
        adm = reg_administrador.get()

        if not user:
            error_label.configure(text="Usuário vazio!", text_color="#FF4B4B")
            reg_user.configure(border_color="#FF4B4B", border_width=1)
            return

        if len(pw) < 6:
            error_label.configure(text="Senha muito curta!", text_color="#FF4B4B")
            reg_pass.configure(border_color="#FF4B4B", border_width=1)
            return
        if pw != pwc:
            error_label.configure(text="Senhas não conferem!", text_color="#FF4B4B")
            reg_pass_confirm.configure(border_color="#FF4B4B", border_width=1)
            return
        
        if func == "Nível de Acesso":
            error_label.configure(text="Selecione um nível de acesso!", text_color="#FF4B4B")
            return
        
        if not adm :
            error_label.configure(text="Senha do adiministrador obrigatória", text_color="#FF4B4B")
            reg_administrador.configure(border_color="#FF4B4B", border_width=1)
            return
        
        if adm != "ADMIN":
            error_label.configure(text="Senha invalida", text_color="#FF4B4B")
            reg_administrador.configure(border_color="#FF4B4B", border_width=1)
            return
        

# Salvar no JSON
        with open(root.db_file, "r") as f:
            data = json.load(f)
        

        data[user] = {"senha": pw, "funcao": func} #>>>>> apos ter todos os dados preciso colocar o nome do adm
        
        with open(root.db_file, "w") as f:
            json.dump(data, f, indent=4)
        
        error_label.configure(text="Cadastro realizado!", text_color="#00FF88")
        root.after(1000, root.show_login_screen)

# Botao cadastrar
    ctk.CTkButton(frame, text="REGISTRAR",
        corner_radius=10, fg_color="#00D2FF", hover_color="#0095B3",
        width=280, height=45, text_color="#000000", font=("Segoe UI", 14, "bold"),
    command=salvar_cadastro).pack(pady=20)
    
    ctk.CTkButton(frame, text="Voltar ao Login", fg_color="transparent", command=root.show_login_screen).pack()

