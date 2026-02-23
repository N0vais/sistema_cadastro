import sys
import os
import pandas as pd
import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox, ttk
from dashboard import DashboardFrame


# Mock das funções de log caso o módulo externo não exista
try:
    from registro_log import registrar_acao, buscar_ultimos_logs
except ImportError:
    def registrar_acao(usuario, perfil, acao):
        # Gera o log no formato solicitado
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"LOG: {agora} | {perfil} | {usuario} | {acao}")

    def buscar_ultimos_logs(filtro):
        return []

class SistemaTarefas(ctk.CTk):
    def __init__(self, user="Admin", funcao="Administrador"): 
        super().__init__() 

        # Dados da Sessão
        self.user = user
        self.funcao = funcao
        self.hora_login = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.cadastrados_sessao = [] 

        # Configuração da Janela
        self.title("Sistema de Cadastro - V1.0.2026")
        self.geometry("1000x650")
        
        # Layout Principal
        self.grid_columnconfigure(0, minsize=250) 
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Inicialização dos Componentes
        self.setup_sidebar()

        self.aplicar_restricoes()
        
        # Inicialização dos Frames de Conteúdo
        self.main_frame = self.setup_main_frame()
        self.frame_logs = self.setup_logs_frame()
        self.dash_frame = DashboardFrame(self)
        
        # Estado Inicial: Dashboard
        self.mostrar_dashboard()
        self.registrar_evento("Login realizado...")

        # Rastreamento da janela imprimir
        self.janela_relatorio = None

    def registrar_evento(self, acao):
        """Helper para registrar ações com os dados do usuário atual"""
        registrar_acao(self.user, self.funcao, acao)

    
    def mostrar_tela(self, frame_alvo):
        """Gerenciador central: Esconde absolutamente tudo e mostra o alvo"""
        # Lista de todos os frames que seu sistema possui
        frames_sistema = [
            self.main_frame, 
            self.frame_logs, 
            self.dash_frame,
        ]
        
        # Se o frame de ofertas já foi criado, adiciona ele na lista para esconder
        if hasattr(self, 'ofertas_frame'):
            frames_sistema.append(self.ofertas_frame)

        # Esconde todos
        for frame in frames_sistema:
            if frame:
                frame.grid_forget()
        
        # Mostra apenas o que você clicou
        frame_alvo.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    def mostrar_dashboard(self):
        self.dash_frame.atualizar_dados()
        self.mostrar_tela(self.dash_frame)
        self.btn_dash.configure(fg_color=("gray75", "gray25")) # Destaque visual
        self.btn_cadastro.configure(fg_color="transparent")

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="AD-PLATINA", font=("Segoe UI", 24, "bold"))
        self.logo_label.pack(pady=30)

        # Botão Cadastro
        self.btn_cadastro = ctk.CTkButton(self.sidebar, text="Cadastro  ▼", font=ctk.CTkFont(size=18),
                                          fg_color="transparent", anchor="w",height=40, command=self.toggle_submenu)
        self.btn_cadastro.pack(fill="x", padx=10, pady=5)
        
        # O frame que vai esconder os dois botoes aseguir
        self.sub_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        
        # Botao dizimo
        self.btn_sub_d = ctk.CTkButton(self.sub_frame, text="  DIZIMOS", font=ctk.CTkFont(size=16),
                                       fg_color="transparent", anchor="w", command=self.abrir_tela_cadastro)
        self.btn_sub_d.pack(fill="x", padx=(30, 15), pady=2)

        # Botao ofertas
        self.btn_sub_o = ctk.CTkButton(self.sub_frame, text="  OFERTAS", font=ctk.CTkFont(size=16),
                                       fg_color="transparent", anchor="w", command=self.abrir_tela_ofertas)
        self.btn_sub_o.pack(fill="x", padx=(30, 15), pady=2)


        # Outros Botões
        self.btn_dash = ctk.CTkButton(self.sidebar, text="Dashboard", font=("Segoe UI", 18), 
                                     fg_color="transparent", anchor="w",height=40, command=self.mostrar_dashboard)
        self.btn_dash.pack(fill="x", padx=10, pady=5)

        self.btn_logs = ctk.CTkButton(self.sidebar, text="Logs do Sistema", font=("Segoe UI", 18), 
                                     fg_color="transparent", anchor="w",height=40,command=self.abrir_tela_logs)
        self.btn_logs.pack(fill="x", padx=10, pady=5)

        # botao imprimir
        self.btn_imprimir_sidebar = ctk.CTkButton(self.sidebar, text="Imprimir Relatório", font=("Segoe UI", 18),
            anchor="w", height=40, fg_color="#aeb464", text_color=("black"), hover_color=("gray70", "#1f538d"),
            command=self.abrir_janela_impressao_global)
        self.btn_imprimir_sidebar.pack(fill="x", padx=10, pady=5)

        # Rodapé com Usuário e Sair
        self.container_usuario = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.container_usuario.pack(side="bottom", fill="x", padx=10, pady=20)

        ctk.CTkLabel(self.container_usuario, text=f"👤  {self.user}", font=("Segoe UI", 16, "bold")
                     ).pack(side="left", padx=(5, 2))
        
        ctk.CTkLabel(self.container_usuario, text="●", text_color="#2ecc71"
                     ).pack(side="left", padx=(0, 5))

        self.btn_sair = ctk.CTkButton(self.container_usuario, text="Sair", fg_color="#cc0000", 
                                     hover_color="#990000", width=65, command=self.encerrar_sistema)
        self.btn_sair.pack(side="right", padx=5)

    # função para desativar os campos de adm
    def aplicar_restricoes(self):
        # Verificamos a função que foi passada na inicialização
        if self.funcao.lower() == "usuario":
            # Desabilita os botões para nível usuário
            self.btn_logs.configure(state="disabled")
            self.btn_logs.pack_forget()
            self.btn_imprimir_sidebar.configure(state="disabled")
            self.btn_imprimir_sidebar.pack_forget()
    # tela de cadastro de dizimo
    def setup_main_frame(self):
        frame = ctk.CTkFrame(self, corner_radius=15)
        ctk.CTkLabel(frame, text="Cadastrar Dizimos", font=("Segoe UI", 24, "bold")).pack(pady=20, padx=30, anchor="w")

        self.entry_nome = self.create_input_nome(frame, "Nome Completo: ")
        self.entry_val1 = self.create_input_valores(frame, "Dízimos R$ (Ex: 100.50)")
        self.entry_val2 = self.create_input_valores(frame, "Outros valores R$")
        self.entry_outros = self.create_input_obs(frame, "Observações")

        btn_cont = ctk.CTkFrame(frame, fg_color="transparent")
        btn_cont.pack(fill="x", padx=30, pady=20)

        ctk.CTkButton(btn_cont, text="Salvar", text_color="#302828", fg_color="#2eb8ac", 
                    hover_color="#248f85", font=("Segoe UI", 18, "bold"), height=45, 
                    command=self.salvar_dados).pack(side="left", expand=True, fill="x", padx=(0, 10))

        ctk.CTkButton(btn_cont, text="Limpar", text_color="#302828", fg_color="#f09644", 
                    hover_color="#c77b38", font=("Segoe UI", 18, "bold"), height=45,
                    command=self.limpar_campos).pack(side="left", expand=True, fill="x")
        return frame

    def setup_logs_frame(self):
        frame = ctk.CTkFrame(self, corner_radius=15)
        ctk.CTkLabel(frame, text="Histórico de Atividades", font=("Segoe UI", 24, "bold")).pack(pady=10)
        
        self.txt_logs = ctk.CTkTextbox(frame, font=("Consolas", 14))
        self.txt_logs.pack(padx=20, pady=10, fill="both", expand=True)
        
        ctk.CTkButton(frame, text="Atualizar Logs",font=("Segoe UI", 15), command=self.atualizar_visualizacao_logs).pack(pady=5)
        return frame

    # Label Nome completo
    def create_input_nome(self, master, label_text):
        label = ctk.CTkLabel(master, text=label_text, font=ctk.CTkFont(size=14, weight="bold"))
        label.pack(anchor="w", padx=35, pady=(10, 0)) # pady=(cima, baixo)
        
        entry = ctk.CTkEntry(master, placeholder_text="EX: Joao Alves", height=40)
        entry.pack(fill="x", padx=30, pady=(2, 10))
        return entry
    
    # Label observaçoes
    def create_input_obs(self, master, label_text):
        label = ctk.CTkLabel(master, text=label_text, font=ctk.CTkFont(size=14, weight="bold"))
        label.pack(anchor="w", padx=35, pady=(10, 0)) # pady=(cima, baixo)
        
        entry = ctk.CTkEntry(master, placeholder_text="Ex: Abatimentos de valores notas.....", height=40)
        entry.pack(fill="x", padx=30, pady=(2, 10))
        return entry
    
    #Labels cadastro de ofertas
    def create_input_no_frame(self, master, label_text):
        """Helper para criar inputs rapidamente"""
        label = ctk.CTkLabel(master, text=label_text, font=ctk.CTkFont(size=14, weight="bold"))
        label.pack(anchor="w", padx=40, pady=(10, 0))

        entry = ctk.CTkEntry(master, placeholder_text="Se Hover alguma observação coloque aqui.....", height=45)
        entry.pack(fill="x", padx=30, pady=(0, 20))
        return entry

    # Label dizimos
    def create_input_valores(self, master, label_text):
        label = ctk.CTkLabel(master, text=label_text, font=ctk.CTkFont(size=14, weight="bold"))
        label.pack(anchor="w", padx=40, pady=(10, 0)) # pady=(cima, baixo)
        
        entry = ctk.CTkEntry(master, placeholder_text=" R$   ",height=40)
        vcmd = (self.register(self.validar_entrada), '%P')
        entry.configure(validate="key", validatecommand=vcmd)
        entry.pack(fill="x", padx=30, pady=(0,10) )
        self.focus_set()
        return entry
    
    def validar_entrada(self, texto):

        if texto == "":
            return True
    
        try:
            if texto.isdigit():
                return True
            float(texto.replace(',', '.'))
            return True
        except ValueError:
            return False

    def toggle_submenu(self):
        if self.sub_frame.winfo_manager():
            self.sub_frame.pack_forget()
        else:
            self.sub_frame.pack(fill="x", after=self.btn_cadastro)

    def abrir_tela_logs(self):
        self.mostrar_tela(self.frame_logs)
        self.atualizar_visualizacao_logs()

    def abrir_tela_cadastro(self):
        self.mostrar_tela(self.main_frame)

    def atualizar_visualizacao_logs(self):
        self.txt_logs.configure(state="normal")
        self.txt_logs.delete("1.0", "end")
        logs = buscar_ultimos_logs("")
        
        if logs:
            for log in logs:
                # Exibe formatado: Data | Perfil | Usuário | Ação
                self.txt_logs.insert("end", f"[{log.get('Data/Hora Login')}] {log.get('Perfil')} - {log.get('Usuário')}: {log.get('Ação')}\n")
        else:
            self.txt_logs.insert("end", "Logs offline ou nenhum registro encontrado.")
        self.txt_logs.configure(state="disabled")

    def salvar_dados(self):
        nome = self.entry_nome.get().strip()
        dizimo =self.entry_val1.get().strip()
        filename = 'data/base_dizimos.xlsx'
        
        if not nome:
            messagebox.showwarning("Aviso", "O nome é obrigatório.")
            return 
        if not dizimo:
            messagebox.showwarning("Aviso", "O dizimo é obrigatório.")
            return 

        try:
            val_d = float(self.entry_val1.get().replace(',', '.')) if self.entry_val1.get() else 0.0
            val_o = float(self.entry_val2.get().replace(',', '.')) if self.entry_val2.get() else 0.0
            total_num = val_d + val_o

            total_formatado = f"{total_num:.2f}".replace('.', ',')
            val_d_str = f"{val_d:.2f}".replace('.', ',')
            val_o_str = f"{val_o:.2f}".replace('.', ',')

            agora = datetime.now()
            data_string = agora.strftime("%d/%m/%Y %H:%M:%S")

            # Verificação de existência
            if os.path.exists(filename):
                df_e = pd.read_excel(filename)
                if not df_e.empty and 'Nome' in df_e.columns:
                    if nome.upper() in df_e['Nome'].astype(str).str.upper().values:
                        if not messagebox.askyesno("Confirmar", f"{nome} já existe. Adicionar novo lançamento?"):
                            return

            # Novo registro
            novo_reg = pd.DataFrame([{
                'Nome': nome,
                'Dizimos': val_d_str,
                'Ofertas': val_o_str,
                'Outros': self.entry_outros.get(),
                'Data_Criacao': data_string,
                'Responsavel': self.user
            }])

            if not os.path.exists(filename):
                novo_reg.to_excel(filename, index=False)
            else:
                df_atual = pd.read_excel(filename)
                pd.concat([df_atual, novo_reg], ignore_index=True).to_excel(filename, index=False)

            # O Dashboard vai ler essa lista e filtrar apenas esses horários
            self.cadastrados_sessao.append(data_string)

            if hasattr(self, 'dash_frame'):
                self.dash_frame.atualizar_dados()

            self.registrar_evento(f"Registrou Dizimo: {nome} (Total: R$ {total_formatado})")
            messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
            self.limpar_campos()

        except ValueError:
            messagebox.showerror("Erro", "Valores numéricos inválidos.")
        except PermissionError:
            messagebox.showerror("Erro", "Feche o arquivo Excel antes de salvar.")

    def limpar_campos(self):
        for entry in [self.entry_nome, self.entry_val1, self.entry_val2, self.entry_outros]:
            entry.delete(0, 'end')

    def encerrar_sistema(self):
        self.registrar_evento(f"Logout realizado (Entrada: {self.hora_login})")
        self.quit()
        self.destroy()
        sys.exit(0)

    def abrir_tela_ofertas(self):
        if not hasattr(self, 'ofertas_frame'):
            self.setup_ofertas_frame()
        self.mostrar_tela(self.ofertas_frame)
    
    # Tela de ofertas
    def setup_ofertas_frame(self):
        """Frame de Cadastro de Ofertas com Validação de Dia"""
        self.ofertas_frame = ctk.CTkFrame(self, corner_radius=15)

        ctk.CTkLabel(self.ofertas_frame, text="Lançamento de Ofertas", 
                     font=("Segoe UI", 24, "bold")).pack(pady=(20, 10), padx=30, anchor="w")

        # Label de Instrução Forçada
        ctk.CTkLabel(self.ofertas_frame, text="⚠️ Selecione obrigatoriamente o dia do culto:",
                     text_color="#ffcc00", font=("Segoe UI", 13, "bold")).pack(padx=30, anchor="w", pady=(10, 0))

        dias_opcoes = [
            "Escola Dominical", "Cuto da Familha", "Circulo de Oração", "Quinta Profética", 
            "Culto de Missões", "Culto de Ceia", "Outros"
        ]

        # ComboBox sem valor padrão inicial
        self.combo_dia = ctk.CTkComboBox(self.ofertas_frame, values=dias_opcoes, width=400, height=45, state="readonly")
        self.combo_dia.pack(fill="x", padx=30, pady=5)
        self.combo_dia.set("--- CLIQUE PARA SELECIONAR ---") # Texto de instrução

        self.entry_oferta_val = self.create_input_valores(self.ofertas_frame, "Valor Arrecadado R$")
        self.entry_oferta_val_saida = self.create_input_valores(self.ofertas_frame, "Valor de saida R$") # Este campo e para valores de saida
        self.entry_obs_oferta = self.create_input_no_frame(self.ofertas_frame, "Observações Adicionais")

        # Botão Salvar
        btn_salvar = ctk.CTkButton(self.ofertas_frame, text="Registrar Oferta", text_color="#302828",fg_color="#2eb8ac", 
                    hover_color="#248f85", font=("Segoe UI", 18, "bold"), height=50,
                    command=self.salvar_oferta_excel)
        btn_salvar.pack(fill="x", padx=30, pady=20)
    
    # Função para salvar no exel
    def salvar_oferta_excel(self):
        dia_selecionado = self.combo_dia.get()
        valor_raw = self.entry_oferta_val.get().strip()
        valor_raw_saida = self.entry_oferta_val_saida.get().strip()

        # Validações básicas...
        if dia_selecionado == "--- CLIQUE PARA SELECIONAR ---" or not valor_raw:
            messagebox.showwarning("Erro", "Preencha o dia e o valor.")
            return

        try:
            # 1. Trata a entrada: converte para float independente de usar . ou ,
            valor_num = float(valor_raw.replace(',', '.'))
            valor_num_saida = float(valor_raw_saida.replace(',', '.'))
            
            # 2. Formata para String padrão BR (123,45)
            valor_br = f"{valor_num:.2f}".replace('.', ',')
            valor_saida = f"{valor_num_saida:.2f}".replace('.', ',')

            data_agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            filename = 'data/base_ofertas.xlsx'
            
            nova_oferta = pd.DataFrame([{
                'Data': data_agora,
                'Dia_Culto': dia_selecionado,
                'Valor': valor_br, # Salva formatado no Excel
                'Valor_Saida':valor_saida,
                'Observacao': self.entry_obs_oferta.get().strip(),
                'Responsavel': self.user
            }])

            # Lógica de concatenação/salvamento...
            if not os.path.exists(filename):
                nova_oferta.to_excel(filename, index=False)
            else:
                df_existente = pd.read_excel(filename)
                pd.concat([df_existente, nova_oferta], ignore_index=True).to_excel(filename, index=False)

            self.cadastrados_sessao.append(data_agora)
            if hasattr(self, 'cadastrados_sessao'):
                self.cadastrados_sessao.append(data_agora)

            # 3. Registro de Log formatado (Sem os erros de casas decimais infinitas)
            registrar_acao(
                usuario=self.user, 
                perfil=self.funcao, 
                acao=f"Registrou Oferta : {dia_selecionado} - Valor: R$ {valor_br} - Retirada de R$ {valor_saida}"
            )

            messagebox.showinfo("Sucesso", f"Oferta de {dia_selecionado} registrada!")
            
            # Limpeza
            self.combo_dia.set("--- CLIQUE PARA SELECIONAR ---")
            self.entry_oferta_val.delete(0, 'end')
            self.entry_oferta_val_saida.delete(0, 'end')
            self.entry_obs_oferta.delete(0, 'end')

        except ValueError:
            messagebox.showerror("Erro", "Valor numérico inválido. Use apenas números e ponto/vírgula.")
        except PermissionError:
            messagebox.showerror("Erro", "Feche o arquivo 'base_ofertas.xlsx' antes de salvar.")
        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Erro inesperado: {e}")


##############################################################################
    def abrir_janela_impressao_global(self):
        # Verifica se o frame de logs ainda existe no sistema
        if not self.winfo_exists():
            return
        
        if self.janela_relatorio is not None and self.janela_relatorio.winfo_exists():
            self.janela_relatorio.lift()
            self.janela_relatorio.focus_force()
            return
        
        df_para_imprimir = self.dash_frame.df_completo 
        if df_para_imprimir is None or df_para_imprimir.empty:
            messagebox.showwarning("Aviso", "Não há dados para imprimir.")
            return

        self.janela_relatorio = ctk.CTkToplevel(self)
        self.janela_relatorio.title("Configurar Impressão")
        self.janela_relatorio.geometry("950x700")
        self.janela_relatorio.lift()            # Traz para o topo da pilha de janelas
        self.janela_relatorio.focus_force()     # Força o Windows a dar foco a ela
        self.janela_relatorio.grab_set()        # Impede clicar no dashboard enquanto esta estiver aberta
        
        # Opcional: faz ela ser filha direta da principal para herdar o foco
        self.janela_relatorio.transient(self)

        ctk.CTkLabel(self.janela_relatorio, text="Relatório de Lançamentos", font=("Segoe UI", 28, "bold")).pack(pady=10)

        # --- FRAME DE FILTROS E AÇÕES ---
        filtros_frame = ctk.CTkFrame(self.janela_relatorio)
        filtros_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(filtros_frame, text="Início:").grid(row=0, column=0, padx=5, pady=10)
        ent_inicio = ctk.CTkEntry(filtros_frame, placeholder_text="DD/MM/AAAA", width=120)
        ent_inicio.grid(row=0, column=1, padx=5)

        ctk.CTkLabel(filtros_frame, text="Fim:").grid(row=0, column=2, padx=5, pady=10)
        ent_fim = ctk.CTkEntry(filtros_frame, placeholder_text="DD/MM/AAAA", width=120)
        ent_fim.grid(row=0, column=3, padx=5)

        # Botões lado a lado
        btn_calc = ctk.CTkButton(filtros_frame, text="Filtrar Preview", command=lambda: filtrar_preview(), fg_color="#1f538d", width=140)
        btn_calc.grid(row=0, column=4, padx=10)

        btn_confirmar = ctk.CTkButton(filtros_frame, text=" Gerar PDF/Imprimir", command=lambda: preparar_salvamento(), fg_color="green", hover_color="#1e5631", width=140)
        btn_confirmar.grid(row=0, column=5, padx=10)

        # --- PREVIEW ---
        lbl_info = ctk.CTkLabel(self.janela_relatorio, text="Filtre os dados para visualizar o relatório", font=("Segoe UI", 12))
        lbl_info.pack(pady=2)

        preview_frame = ctk.CTkFrame(self.janela_relatorio)
        preview_frame.pack(fill="both", expand=True, padx=20, pady=10)

        cols = ("Data", "Nome", "Dízimo", "Oferta","Saida", "Responsável")
        preview_tree = ttk.Treeview(preview_frame, columns=cols, show="headings")
        for col in cols:
            preview_tree.heading(col, text=col)
            preview_tree.column(col, width=120, anchor="center")
        preview_tree.pack(side="left", fill="both", expand=True)

        # --- ÁREA DE SALVAMENTO (APARECE ABAIXO) ---
        save_frame = ctk.CTkFrame(self.janela_relatorio, fg_color="transparent")
        save_frame.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(save_frame, text="Nome do Arquivo:", font=("Segoe UI", 12, "bold")).pack(side="left", padx=5)
        ent_nome_arquivo = ctk.CTkEntry(save_frame, width=250)
        ent_nome_arquivo.insert(0, f"Relatorio_{datetime.now().strftime('%d_%m_%Y')}")
        ent_nome_arquivo.pack(side="left", padx=5)

        lbl_status_save = ctk.CTkLabel(self.janela_relatorio, text="", font=("Segoe UI", 11, "italic"))
        lbl_status_save.pack(pady=5)

        # Variável para armazenar os dados filtrados
        self.dados_filtrados_backup = None

        def filtrar_preview():
            try:
                d_ini = datetime.strptime(ent_inicio.get(), "%d/%m/%Y")
                d_fim = datetime.strptime(ent_fim.get(), "%d/%m/%Y")
                
                df_temp = df_para_imprimir.copy()
                df_temp['Timestamp'] = pd.to_datetime(df_temp['Timestamp'])
                
                mask = (df_temp['Timestamp'].dt.date >= d_ini.date()) & (df_temp['Timestamp'].dt.date <= d_fim.date())
                df_filtrado = df_temp[mask]
                self.dados_filtrados_backup = df_filtrado # Guarda para o PDF

                for item in preview_tree.get_children(): preview_tree.delete(item)
                for _, row in df_filtrado.iterrows():
                    v_d = f"R$ {row['Dizimo_Val']:,.2f}".replace('.', ',') if row['Dizimo_Val'] > 0 else "---"
                    v_o = f"R$ {row['Oferta_Val']:,.2f}".replace('.', ',') if row['Oferta_Val'] > 0 else "---"
                    v_s = f"R$ {row['Oferta_Val_saida']:,.2f}".replace('.', ',') if row['Oferta_Val_saida'] > 0 else "---"
                    preview_tree.insert("", "end", values=(row['Data'], row['Nome'], v_d, v_o, v_s, row['Resp']))

                lbl_info.configure(text=f"Registros encontrados: {len(df_filtrado)}", text_color="#50fa7b")
            except:
                messagebox.showerror("Erro", "Data inválida! Use DD/MM/AAAA", parent=self.janela_relatorio)

        def preparar_salvamento():
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Frame, PageTemplate
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import cm

            if self.dados_filtrados_backup is None or self.dados_filtrados_backup.empty:
                messagebox.showwarning("Aviso", "Filtre os dados primeiro!", parent=self.janela_relatorio)
                return

            nome_sugerido = ent_nome_arquivo.get().strip()
            caminho_salvar = ctk.filedialog.asksaveasfilename(
                parent=self.janela_relatorio,
                defaultextension=".pdf", initialfile=nome_sugerido,
                title="Salvar Relatório Executivo", filetypes=[("Arquivos PDF", "*.pdf")]
            )

            if caminho_salvar:
                try:
                    doc = SimpleDocTemplate(caminho_salvar, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
                    elementos = []
                    estilos = getSampleStyleSheet()

                    # Estilos Personalizados
                    estilo_titulo = ParagraphStyle('CustomTitle', parent=estilos['Title'], fontSize=20, textColor=colors.HexColor("#161616"), spaceAfter=8)
                    estilo_sub = ParagraphStyle('CustomSub', parent=estilos['Normal'], fontSize=10, textColor=colors.HexColor("#161616"), spaceAfter=10)
                    estilo_card = ParagraphStyle('Card', parent=estilos['Normal'], fontSize=12, textColor=colors.black, alignment=1)

                    # 1. CABEÇALHO
                    elementos.append(Paragraph("RELATÓRIO DE LANÇAMENTOS - AD PLATINA", estilo_titulo))
                    elementos.append(Paragraph(f"Período: {ent_inicio.get()} - {ent_fim.get()}", estilo_sub))
                    elementos.append(Spacer(1, 10))

                    # 2. CARDS DE RESUMO (Destaque)
                    total_diz = self.dados_filtrados_backup['Dizimo_Val'].sum()
                    total_ofe = self.dados_filtrados_backup['Oferta_Val'].sum()
                    total_ofe_saida = self.dados_filtrados_backup['Oferta_Val_saida'].sum()
                    total = total_diz + total_ofe - total_ofe_saida
                    
                    resumo_data = [
                        [Paragraph(f"<b>TOTAL DÍZIMOS</b><br/>R$ {total_diz:,.2f}".replace('.',','), estilo_card),
                         Paragraph(f"<b>TOTAL OFERTAS</b><br/>R$ {total_ofe:,.2f}".replace('.',','), estilo_card)],

                         [Paragraph(f"<b>TOTAL SAIDAS</b><br/>R$ {total_ofe_saida:,.2f}".replace('.',','), estilo_card),
                         Paragraph(f"<b>TOTAL </b><br/>R$ {total:,.2f}".replace('.',','), estilo_card)]
                    ]
                    resumo_tab = Table(resumo_data, colWidths=[250, 250], rowHeights=35)
                    resumo_tab.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor("#a0a0a0")),
                        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor("#929292")),
                        
                        ('BACKGROUND', (0, 1), (0, 1), colors.HexColor("#929292")), 
                        ('BACKGROUND', (1, 1), (1, 1), colors.HexColor("#a0a0a0")), 
                        ('BOX', (0,0), (-1,-1), 2, colors.white),
                        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                        ('LEFTPADDING', (0,0), (-1,-1), 15),
                    ]))
                    elementos.append(resumo_tab)
                    elementos.append(Spacer(1, 20))

                    # 3. TABELA DE DADOS (Estilo Moderno)
                    dados_tabela = [["DATA", "MEMBRO / DESCRIÇÃO", "DÍZIMO", "OFERTA", "SAIDA", "RESPONSÁVEL"]]
                    
                    for _, row in self.dados_filtrados_backup.iterrows():
                        v_d = f"R$ {row['Dizimo_Val']:,.2f}".replace('.',',') if row['Dizimo_Val'] > 0 else "-"
                        v_o = f"R$ {row['Oferta_Val']:,.2f}".replace('.',',') if row['Oferta_Val'] > 0 else "-"
                        v_s = f"R$ {row['Oferta_Val_saida']:,.2f}".replace('.',',') if row['Oferta_Val_saida'] > 0 else "-"
                        
                        dados_tabela.append([
                            row['Data'][:10], 
                            row['Nome'].upper()[:30], 
                            v_d, v_o, v_s,
                            row['Resp'].split()[0] # Apenas primeiro nome do resp.
                        ])

                    # Configuração visual da tabela    [60, 195, 75, 75, 75, 55]
                    t = Table(dados_tabela, colWidths=[70, 150, 70, 70, 70,90])
                    t.setStyle(TableStyle([
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#444444")),
                        ('LINEBELOW', (0, 0), (-1, 0), 1.0, colors.HexColor("#929292")), # Linha grossa abaixo do cabeçalho
                        
                        ('FONTSIZE', (0, 1), (-1, -1), 9),
                        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#e0e0e0")]), # Efeito zebra suave
                        ('LINEBELOW', (0, 1), (-1, -1), 0.5, colors.HexColor("#bebebe")), # Linhas divisórias sutis
                        ('ALIGN', (2, 0), (3, -1), 'RIGHT'), # Alinha valores à direita
                        ('ALIGN', (0, 0), (1, -1), 'LEFT'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                        ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ]))

                    elementos.append(t)
                    
                    # Rodapé
                    elementos.append(Spacer(1, 30))
                    elementos.append(Paragraph(f"Documento gerado eletronicamente por {self.user} em {datetime.now().strftime('%d/%m/%Y %H:%M')}", 
                                             ParagraphStyle('Footer', parent=estilos['Italic'], fontSize=12, alignment=1)))

                    doc.build(elementos)

                    lbl_status_save.configure(text=f"✅ Relatório Gerado com Sucesso!", text_color="#2ecc71")
                    messagebox.showinfo("Sucesso", "O relatório foi estilizado e salvo com sucesso!")
                    
                except Exception as e:
                    messagebox.showerror("Erro", f"Falha ao gerar design: {e}")

if __name__ == "__main__":
    app = SistemaTarefas()
    app.mainloop()