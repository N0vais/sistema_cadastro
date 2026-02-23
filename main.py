from tkinter import messagebox
import customtkinter as ctk
import json
import os
import sys
from cadastro import show_register_screen

# Configurações de Design
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AdplatinaSystem(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Cadastro Ad-Platina - V1.0.2026")
        self.geometry("900x600")
        self.resizable(False, False)

        # Arquivo de dados
        self.db_file = "data/users_db.json"
        self._ensure_db_exists()

        # Container Principal
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)
        
        self.show_login_screen()

    def _ensure_db_exists(self):
        """Garante que o banco de dados JSON exista"""
        if not os.path.exists(self.db_file):
            with open(self.db_file, "w") as f:
                json.dump({}, f)

    def clear_screen(self):
        """Limpa o container principal para troca de telas"""
        for widget in self.container.winfo_children():
            widget.destroy()

    def load_users(self):
        """Carrega usuários do JSON com tratamento de erro"""
        try:
            with open(self.db_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    # --- TELA DE LOGIN ---
    def show_login_screen(self):
        self.clear_screen()
        
        # Frame Centralizado
        frame = ctk.CTkFrame(self.container, corner_radius=20, border_width=2, border_color="#3d3d3d")
        frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7, relheight=0.8)

        # Labels
        ctk.CTkLabel(frame, text="BEM-VINDO", font=("Orbitron", 28, "bold"), text_color="#00D2FF").pack(pady=(40, 5))
        ctk.CTkLabel(frame, text="Identifique-se para continuar", font=("Segoe UI", 16), text_color="#888888").pack(pady=(0, 30))
  
        # Inputs
        self.user_entry = ctk.CTkEntry(frame, placeholder_text="Nome de Usuário", width=350, height=45, 
                                       border_color="#333333", fg_color="#1a1a1a", font=("Segoe UI", 16))
        self.user_entry.pack(pady=10)

        self.pass_entry = ctk.CTkEntry(frame, placeholder_text="Senha", show="•", width=350, height=45, 
                                       border_color="#333333", fg_color="#1a1a1a", font=("Segoe UI", 16))
        self.pass_entry.pack(pady=10)

        # Label de Erro
        self.msg_label = ctk.CTkLabel(frame, text="", font=("Segoe UI", 14))
        self.msg_label.pack(pady=5)

        # Botão Autenticar
        ctk.CTkButton(frame, text="AUTENTICAR", corner_radius=10, fg_color="#00D2FF", 
                      hover_color="#0095B3", width=350, height=50, text_color="#000000", 
                      font=("Segoe UI", 14, "bold"), command=self.realizar_login).pack(pady=(10, 5))
        
        # Links Adicionais
        ctk.CTkButton(frame, text="Problemas com o acesso?", fg_color="transparent", hover=False, 
                      text_color="#8A8787", font=("Segoe UI", 13, "underline"), cursor="hand2",
                      command=self.recuperar_acesso).pack()

        ctk.CTkButton(frame, text="Criar nova conta", fg_color="transparent", hover=False, 
                      text_color="#ffc107", font=("Segoe UI", 14, "bold"), cursor="hand2",
                      command=lambda: show_register_screen(self)).pack(pady=5)

    def realizar_login(self):
        """Lógica de validação de login"""
        user = self.user_entry.get().strip()
        pw = self.pass_entry.get().strip()
        
        # Reset visual
        self.user_entry.configure(border_color="#333333")
        self.pass_entry.configure(border_color="#333333")
        self.msg_label.configure(text="")

        # Validação básica
        if not user or not pw:
            self.msg_label.configure(text="Preencha todos os campos!", text_color="#FF4B4B")
            if not user: self.user_entry.configure(border_color="#FF4B4B")
            if not pw: self.pass_entry.configure(border_color="#FF4B4B")
            return

        if not (6 <= len(pw) <= 10):
            self.msg_label.configure(text="A senha deve ter entre 6 e 10 caracteres", text_color="#FF4B4B")
            self.pass_entry.configure(border_color="#FF4B4B")
            return

        # Validação no "Banco de Dados"
        users = self.load_users()
        
        if user in users and users[user]['senha'] == pw:
            funcao = users[user].get('funcao', 'Usuário')
            self.msg_label.configure(text="Autenticando...", text_color="#00ffac")
            
            # Pequeno delay para feedback visual
            self.after(500, lambda: self.abrir_home(user, funcao))
        else:
            self.msg_label.configure(text="Usuário ou senha inválidos", text_color="#FF4B4B")
            self.user_entry.configure(border_color="#FF4B4B")
            self.pass_entry.configure(border_color="#FF4B4B")

    def abrir_home(self, user, funcao):
        """Transição para o sistema principal"""
        try:
            from home import SistemaTarefas
            self.withdraw()  # Oculta a tela de login
            
               
            # Cria a nova janela
            app_home = SistemaTarefas(user=user, funcao=funcao)
            app_home.mainloop()
            
            # Se a home for fechada, encerra o app inteiro
            sys.exit() 
            
        except Exception as e:
            self.msg_label.configure(text=f"Erro ao carregar Home: {e}", text_color="#FF4B4B")
            self.deiconify()

    def recuperar_acesso(self):
        """Janela de autorização e troca de senha"""
        # Criamos uma nova janela (Toplevel) para o processo
        janela_reset = ctk.CTkToplevel(self)
        janela_reset.title("Autorização de Segurança")
        janela_reset.geometry("400x500")
        janela_reset.grab_set() # Foca apenas nesta janela

        ctk.CTkLabel(janela_reset, text="REDEFINIR SENHA", font=("Segoe UI", 28, "bold"),text_color="#00D2FF").pack(pady=20)

        # Campos
        user_target = ctk.CTkEntry(janela_reset, placeholder_text="Usuário para resetar", width=300, height=40,
                                   border_color="#333333", fg_color="#1a1a1a", font=("Segoe UI", 16) )
        user_target.pack(pady=10)

        ctk.CTkLabel(janela_reset, text="Autorização do Admin", font=("Segoe UI", 18)).pack()
        adm_user = ctk.CTkEntry(janela_reset, placeholder_text="Login do Admin", width=300,height=40,
                                border_color="#333333", fg_color="#1a1a1a", font=("Segoe UI", 16))
        adm_user.pack(pady=5)
        
        adm_pass = ctk.CTkEntry(janela_reset, placeholder_text="Senha do Admin", show="•", width=300,height=40,
                                border_color="#333333", fg_color="#1a1a1a", font=("Segoe UI", 16))
        adm_pass.pack(pady=5)

        ctk.CTkLabel(janela_reset, text="Nova Senha", font=("Segoe UI", 18)).pack(pady=(10,0))
        new_pass = ctk.CTkEntry(janela_reset, placeholder_text="Nova Senha (6-10 caracteres)", show="*", width=300,height=40,
                                border_color="#333333", fg_color="#1a1a1a", font=("Segoe UI", 16))
        new_pass.pack(pady=5)

        def processar_troca():
            from reset_manager import validar_admin_e_resetar
            from registro_log import registrar_acao

            sucesso, msg = validar_admin_e_resetar(
                self.db_file, 
                user_target.get().strip(),
                adm_user.get().strip(),
                adm_pass.get().strip(),
                new_pass.get().strip()
            )

            if sucesso:
                registrar_acao(adm_user.get(), "Administrador", f"Resetou senha de {user_target.get()}")
                messagebox.showinfo("Sucesso", msg)
                janela_reset.destroy()
            else:
                messagebox.showerror("Erro", msg)

        ctk.CTkButton(janela_reset, text="CONFIRMAR RESET", fg_color="#2eb8ac", text_color="#000000", 
                       font=("Segoe UI", 14, "bold"),
                    command=processar_troca).pack(pady=30)

if __name__ == "__main__":
    app = AdplatinaSystem()
    app.mainloop()