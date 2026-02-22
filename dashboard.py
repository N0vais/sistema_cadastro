import customtkinter as ctk
import pandas as pd
import os
from tkinter import messagebox, ttk

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15, fg_color="transparent")
        
        self.df_completo = pd.DataFrame()

        # --- CONFIGURAÇÃO DE ESTILO MODERNO (TREEVIEW) ---
        self.style = ttk.Style()
        self.style.theme_use("default")
        
        self.style.configure("Treeview",
            background="#2b2b2b",
            foreground="white",
            fieldbackground="#2b2b2b",
            borderwidth=0,
            rowheight=35,
            font=("Segoe UI", 11)
        )
        
        self.style.configure("Treeview.Heading",
            background="#333333",
            foreground="white",
            relief="flat",
            font=("Segoe UI", 11, "bold")
        )
        self.style.map("Treeview.Heading", background=[('active', "#404040")])

        # Correção da cor de seleção: Fundo azul e texto branco ao clicar
        self.style.map("Treeview", 
            background=[('selected', '#1f538d')],
            foreground=[('selected', 'white')]
        )

        # --- CABEÇALHO (TÍTULO E PESQUISA NA MESMA LINHA) ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 20))

        # Título
        self.lbl_dash = ctk.CTkLabel(
            self.header_frame, 
            text="Dashboard Administrativo", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.lbl_dash.pack(side="left", anchor="w")

        # Container de busca (Lupa + Entry)
        self.search_container = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.search_container.pack(side="right", anchor="e")

        self.entry_busca = ctk.CTkEntry(
            self.search_container, 
            placeholder_text="Pesquisar...", 
            width=350,
            height=35
        )
        self.entry_busca.pack(side="left", padx=(0, 5))
        
        # Bind para a tecla Enter
        self.entry_busca.bind("<Return>", lambda e: self.filtrar_tabela())

        # Botão Lupa
        self.btn_lupa = ctk.CTkButton(
            self.search_container,
            text="🔍",
            width=40,
            height=35,
            fg_color="#333333",
            hover_color="#404040",
            command=self.filtrar_tabela
        )
        self.btn_lupa.pack(side="left")

        # --- RESTANTE DA ESTRUTURA ---
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.pack(fill="x", pady=10)

        self.lbl_recents = ctk.CTkLabel(self, text="Lançamentos Registrados", 
                                        font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_recents.pack(pady=(20, 5), anchor="w")

        # --- TABELA ---
        columns = ("Data", "Nome", "Dízimo", "Oferta", "Observações", "Responsável")
        
        self.tree_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#2b2b2b")
        self.tree_frame.pack(fill="both", expand=True, padx=2, pady=2)

        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.tag_configure('oddrow', background="#b9b9b9")
        self.tree.tag_configure('evenrow', background="#b1b1b1")

        for col in columns:
            self.tree.heading(col, text=col.upper())
            if col in ["Dízimo", "Oferta"]:
                self.tree.column(col, width=100, anchor="center")
            elif col == "Data":
                self.tree.column(col, width=100, anchor="center")
            else:
                self.tree.column(col, width=150, anchor="w")

        self.tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ctk.CTkScrollbar(self.tree_frame, orientation="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.atualizar_dados()

    def limpar_valor(self, v):
        if v is None or str(v).lower() == 'nan' or str(v).strip() == '': return 0.0
        try:
            s = str(v).replace('R$', '').replace('.', '').replace(',', '.').strip()
            return float(s)
        except: return 0.0

    def atualizar_dados(self):
        file_tasks = 'data/base_dizimos.xlsx'
        file_offers = 'data/base_ofertas.xlsx'
        dados_misturados = []

        if os.path.exists(file_tasks):
            try:
                df_t = pd.read_excel(file_tasks)
                for _, row in df_t.iterrows():
                    vd = self.limpar_valor(row.get('Dizimos', 0))
                    vo = self.limpar_valor(row.get('Ofertas', 0))
                    dados_misturados.append({
                        'Data': str(row.get('Data_Criacao', '-')),
                        'Nome': str(row.get('Nome', '-')),
                        'Dizimo_Val': vd,
                        'Oferta_Val': vo,
                        'Obs': str(row.get('Outros', '')).replace('nan', ''),
                        'Resp': str(row.get('Responsavel', '')).replace('nan', ''),
                        'Timestamp': pd.to_datetime(row.get('Data_Criacao'), dayfirst=True, errors='coerce')
                    })
            except Exception as e: print(f"Erro tarefas: {e}")

        if os.path.exists(file_offers):
            try:
                df_o = pd.read_excel(file_offers)
                for _, row in df_o.iterrows():
                    val = self.limpar_valor(row.get('Valor', 0))
                    dados_misturados.append({
                        'Data': str(row.get('Data', '-')),
                        'Nome': f"CULTO: {row.get('Dia_Culto', '-')}",
                        'Dizimo_Val': 0.0,
                        'Oferta_Val': val,
                        'Obs': str(row.get('Observacao', '')).replace('nan', ''),
                        'Resp': str(row.get('Responsavel', '')).replace('nan', ''), 
                        'Timestamp': pd.to_datetime(row.get('Data'), dayfirst=True, errors='coerce')
                    })
            except Exception as e: print(f"Erro ofertas: {e}")

        if dados_misturados:
            self.df_completo = pd.DataFrame(dados_misturados).sort_values(by='Timestamp', ascending=False)
            self.filtrar_tabela()

    def filtrar_tabela(self):
        termo = self.entry_busca.get().lower()
        for item in self.tree.get_children(): self.tree.delete(item)
        
        if self.df_completo.empty: return

        mask = (
            self.df_completo['Nome'].astype(str).str.lower().str.contains(termo) |
            self.df_completo['Data'].astype(str).str.lower().str.contains(termo) |
            self.df_completo['Obs'].astype(str).str.lower().str.contains(termo) |
            self.df_completo['Resp'].astype(str).str.lower().str.contains(termo)
        )
        df_filtrado = self.df_completo[mask]

        for i, (_, row) in enumerate(df_filtrado.iterrows()):
            d_txt = f"R$ {row['Dizimo_Val']:,.2f}".replace('.', 'X').replace(',', '.').replace('X', ',') if row['Dizimo_Val'] > 0 else "---"
            o_txt = f"R$ {row['Oferta_Val']:,.2f}".replace('.', 'X').replace(',', '.').replace('X', ',') if row['Oferta_Val'] > 0 else "---"
            
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            
            self.tree.insert("", "end", values=(
                row['Data'], row['Nome'], d_txt, o_txt, row['Obs'], row['Resp']
            ), tags=(tag,))
        
        self.atualizar_cards(df_filtrado)

    def criar_card(self, titulo, valor, cor):
        card = ctk.CTkFrame(self.cards_frame, height=120, border_width=1, border_color=cor, fg_color="#2b2b2b")
        ctk.CTkLabel(card, text=titulo, font=ctk.CTkFont(size=13), text_color="#aaaaaa").pack(pady=(15, 0))
        ctk.CTkLabel(card, text=valor, font=ctk.CTkFont(size=22, weight="bold"), text_color=cor).pack(pady=(5, 15))
        return card

    def atualizar_cards(self, df):
        for widget in self.cards_frame.winfo_children(): widget.destroy()
        
        total_d = df['Dizimo_Val'].sum()
        total_o = df['Oferta_Val'].sum()
        
        def br_money(v):
            return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        self.criar_card("Lançamentos", str(len(df)), "#50fa7b").pack(side="left", padx=5, expand=True, fill="both")
        self.criar_card("Total Dízimos", br_money(total_d), "#8be9fd").pack(side="left", padx=5, expand=True, fill="both")
        self.criar_card("Total Ofertas", br_money(total_o), "#f1fa8c").pack(side="left", padx=5, expand=True, fill="both")
        self.criar_card("Volume Total", br_money(total_d + total_o), "#ff79c6").pack(side="left", padx=5, expand=True, fill="both")
