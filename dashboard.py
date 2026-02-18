import customtkinter as ctk
import pandas as pd
import os
from tkinter import ttk
from datetime import datetime

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15, fg_color="transparent")
        
        # Título
        self.lbl_dash = ctk.CTkLabel(self, text="Dashboard Administrativo", 
                                     font=ctk.CTkFont(size=24, weight="bold"))
        self.lbl_dash.pack(pady=(0, 20), anchor="w")

        # Container para os Cards
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.pack(fill="x", pady=10)

        # --- Tabela de Últimos Lançamentos ---
        self.lbl_recents = ctk.CTkLabel(self, text="Últimos Lançamentos Registrados", 
                                        font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_recents.pack(pady=(20, 10), anchor="w")

        # Configuração de Estilo
        style = ttk.Style()
        style.theme_use("clam")
        
        bg_color = "#c9c9c9"      # Fundo das linhas
        header_color = "#1f538d"  # Cor do cabeçalho
        text_color = "#474747"      # Cor do texto

        # Criando a Tabela
        self.tree_frame = ctk.CTkFrame(self, fg_color=bg_color, corner_radius=10)
        self.tree_frame.pack(fill="both", expand=True, padx=2, pady=5)

        columns = ("Data", "Nome", "Dízimo", "Oferta")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", selectmode="browse")
        
        # Isso força a cor na linha do cabeçlho da tabela
        self.tree.tag_configure('row_style', background=bg_color, foreground=text_color, font=("Segoe UI", 11))

        self.tree.heading("Data", text="DATA")
        self.tree.column("Data", width=110, anchor="center")
        self.tree.heading("Nome", text="NOME DO MEMBRO")
        self.tree.column("Nome", width=200, anchor="w")
        self.tree.heading("Dízimo", text="DÍZIMO")
        self.tree.column("Dízimo", width=120, anchor="center")
        self.tree.heading("Oferta", text="OFERTA")
        self.tree.column("Oferta", width=120, anchor="center")

        scrollbar = ctk.CTkScrollbar(self.tree_frame, orientation="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0,10), pady=10)

        self.atualizar_dados()

    def criar_card(self, titulo, valor, cor_borda):
        card = ctk.CTkFrame(self.cards_frame, height=120, border_width=2, border_color=cor_borda)
        ctk.CTkLabel(card, text=titulo, font=ctk.CTkFont(size=14)).pack(pady=(15, 0))
        ctk.CTkLabel(card, text=valor, font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(5, 15))
        return card

    def atualizar_dados(self):
        filename = 'base_tarefas.xlsx'
        for widget in self.cards_frame.winfo_children(): widget.destroy()
        for item in self.tree.get_children(): self.tree.delete(item)

        total_registros = "0"
        soma_valores = "R$ 0,00"

        if os.path.exists(filename):
            try:
                df = pd.read_excel(filename)
                df.columns = [str(c).strip() for c in df.columns]
                total_registros = str(len(df))

                def limpar_coluna(nome_coluna):
                    if nome_coluna in df.columns:
                        serie = df[nome_coluna].astype(str).str.replace('R$', '', regex=False)
                        serie = serie.str.replace('.', '', regex=False).str.replace(',', '.', regex=False).str.strip()
                        return pd.to_numeric(serie, errors='coerce').fillna(0)
                    return pd.Series([0])

                col_dizimos = limpar_coluna('Dizimos')
                col_ofertas = limpar_coluna('Ofertas')
                total_diz_soma = col_dizimos.sum()
                total_ofe_soma = col_ofertas.sum()
                total_financeiro = col_dizimos.sum() + col_ofertas.sum()

                soma_dizimos = f"R$ {total_diz_soma:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                soma_ofertas = f"R$ {total_ofe_soma:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                soma_valores = f"R$ {total_financeiro:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            
                recent_data = df.tail(10).iloc[::-1]

                for _, row in recent_data.iterrows():
                    # Formatação interna para garantir floats
                    v_diz = float(str(row.get('Dizimos', 0)).replace(',','.')) if row.get('Dizimos') else 0.0
                    v_ofe = float(str(row.get('Ofertas', 0)).replace(',','.')) if row.get('Ofertas') else 0.0

                    # AQUI: Inserimos com a TAG 'row_style'
                    self.tree.insert("", "end", values=(
                        row.get('Data_Criacao', '-'),
                        row.get('Nome', '-'),
                        f"R$ {v_diz:,.2f}".replace('.', ','),
                        f"R$ {v_ofe:,.2f}".replace('.', ',')
                    ), tags=('row_style',)) # <--- O SEGREDO ESTÁ AQUI

            except Exception as e:
                print(f"Erro ao ler Excel: {e}")

        self.criar_card("Total de Cadastros", total_registros, "#2eb8ac").pack(side="left", padx=10, expand=True, fill="both")
        self.criar_card("Total Dízimos", soma_dizimos, "#1f538d").pack(side="left", padx=5, expand=True, fill="both")
        self.criar_card("Total Ofertas", soma_ofertas, "#a2d149").pack(side="left", padx=5, expand=True, fill="both")
        self.criar_card("Volume Financeiro", soma_valores, "#f09644").pack(side="left", padx=10, expand=True, fill="both")
        
        


        "#1f538d" "#a2d149""#f09644"