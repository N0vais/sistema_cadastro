import customtkinter as ctk
import json
import os
import datetime
from cadastro import show_register_screen
from home import SistemaTarefas

# Configurações de Design
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AdplatinaSystem(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Cadastro Ad-Platina - V1.0.2026")
        self.geometry("900x600")
    # Arquivo de dados
        self.db_file = "users_db.json"
        self._ensure_db_exists()
    # Container Principal para Transições
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)
        self.show_login_screen()

    def _ensure_db_exists(self):
        if not os.path.exists(self.db_file):
            with open(self.db_file, "w") as f:
                json.dump({}, f)

    def clear_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # --- TELA DE LOGIN ---
    def show_login_screen(self):
        self.clear_screen()
        
        frame = ctk.CTkFrame(self.container, corner_radius=20, border_width=2, border_color="#3d3d3d")
        frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.85)

        ctk.CTkLabel(frame, text="BEM-VINDO", font=("Orbitron", 28, "bold"), text_color="#00D2FF").pack(pady=(40, 5))

        ctk.CTkLabel(frame, text="Identifique-se para continuar", font=("Segoe UI", 18), text_color="#888888").pack(pady=(0, 30))
  
        user_entry = ctk.CTkEntry(frame, placeholder_text="Nome de Usuário", width=350, height=50, border_color="#333333",
            fg_color="#1a1a1a", font=("Segoe UI", 20))
        user_entry.pack(pady=10)

        pass_entry = ctk.CTkEntry(frame, placeholder_text="Senha", show="•", width=350, height=50, border_color="#333333",
            fg_color="#1a1a1a", font=("Segoe UI", 20))
        pass_entry.pack(pady=10)

     # Mensagem (Dinâmica de erro)
        msg_label = ctk.CTkLabel(frame, text="", font=("Segoe UI", 18))
        msg_label.pack(pady=5)

        # Função realizar validação dos campos
        def realizar_login():
            # variaveis de controle
            user = user_entry.get().strip()
            pw = pass_entry.get().strip()
    
            # 1. Reset padrão (limpa erros anteriores)
            user_entry.configure(border_color="#333333")
            pass_entry.configure(border_color="#333333")
            msg_label.configure(text="")

            # 2. Validação de Campos Vazios
            errors = []
            if not user:
                user_entry.configure(border_color="#FF4B4B")
                errors.append("usuário")
            if not pw:
                pass_entry.configure(border_color="#FF4B4B")
                errors.append("senha")

            # Se houver erros de preenchimento, exibe mensagem e para
            if errors:
                texto_erro = " e ".join(errors)
                msg_label.configure(text=f"Preencha o campo: {texto_erro}", text_color="#FF4B4B")
                return

            # Validação de Regra de Negócio (Tamanho)
            if not (6 <= len(pw) <= 10):
                msg_label.configure(text="A senha deve ter entre 6 e 10 caracteres", text_color="#FF4B4B")
                pass_entry.configure(border_color="#FF4B4B")
                return
            
            # Validações dos dados no banco de dados
            try:    
                with open(self.db_file, "r") as f:
                    users = json.load(f)
                
                if user in users and users[user]['senha'] == pw:
                    funcao = users[user]['funcao']
                    msg_label.configure(text="Autenticando...", text_color="#00ffac"),
                    
                    app.withdraw()

                    app.after(100, lambda: abrir_sistema_tarefas(user, funcao))
                    
                else:
                    msg_label.configure(text="Credenciais Inválidas", text_color="#FF4B4B")
                    user_entry.configure(border_color="#FF4B4B")
                    pass_entry.configure(border_color="#FF4B4B")

            except FileNotFoundError:
                msg_label.configure(text="Erro: Arquivo de dados não encontrado!", text_color="#FF4B4B")
            except json.JSONDecodeError:
                msg_label.configure(text="Erro: Banco de dados corrompido ou vazio!", text_color="#FF4B4B")
            except Exception as e:
                app.deiconify()
                msg_label.configure(text=f"Erro inesperado: {e}", text_color="#FF4B4B")
    
    # Botão logar
        ctk.CTkButton(frame, text="AUTENTICAR", 
            corner_radius=10, fg_color="#00D2FF", hover_color="#0095B3", 
            width=280, height=50, text_color="#000000", font=("Segoe UI", 14, "bold"),
            command=realizar_login).pack(pady=(20, 10))
        
        
    # Botão esqueci a senha
        ctk.CTkButton(frame, text="Problemas com o acesso?", 
            fg_color="transparent", hover=False, text_color="#8A8787",
            font=("Segoe UI", 14, "underline"), cursor="hand2").pack(pady=10)

    #Botão criar conta
        ctk.CTkButton(frame, text="Criar nova conta", 
            fg_color="transparent", hover=False, text_color="#ffc107", 
            font=("Segoe UI", 16, "bold"), cursor="hand2",
            command=lambda: show_register_screen(self)).pack(pady=10)
        
    #Função para esconder janela do login e abrir a home
        def abrir_sistema_tarefas(user, funcao):

            try:
                from home import SistemaTarefas
                for child in app.winfo_children():
                    child.destroy() # Destrói todos os widgets internos do login antes
            
                    app.withdraw() 
        
                    app_home = SistemaTarefas(user=user, funcao=funcao)
                    app_home.mainloop() # inicia o loop da nova janela
            except Exception as e:
                print(f"Erro crítico ao carregar home.py: {e}")
                self.deiconify()

if __name__ == "__main__":
    app = AdplatinaSystem()
    app.mainloop()