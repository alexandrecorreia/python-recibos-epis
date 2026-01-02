# =============================================================================
# Nome do Software: Geracao de Recibos de EPIS
#
# Copyright (C) 2026 Alexandre Correia < dinhocorreia at gmail.com >
#
# Este programa é um software livre; você pode redistribuí-lo e/ou modificá-lo
# sob os termos da Licença Pública Geral GNU (GNU General Public License),
# conforme publicada pela Free Software Foundation; na versão 3 da Licença,
# ou (a seu critério) qualquer versão posterior.
#
# Este programa é distribuído na expectativa de que seja útil, porém,
# SEM NENHUMA GARANTIA; sem mesmo a garantia implícita de COMERCIALIZAÇÃO
# ou ADEQUAÇÃO A UMA FINALIDADE ESPECÍFICA. Consulte a Licença Pública Geral
# GNU para mais detalhes.
#
# Você deve ter recebido uma cópia da Licença Pública Geral GNU junto com
# este programa. Caso contrário, consulte <https://www.gnu.org/licenses/>.
#
# =============================================================================

import os
import configparser
import tkinter as tk
from tkinter import ttk, messagebox
import platform
import pandas as pd
from datetime import datetime
from weasyprint import HTML
import requests
from PIL import Image, ImageTk, ImageDraw  # Para criar imagens de checkboxes

# Diretório base do projeto
base_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(base_dir)

data_path = os.path.join(base_dir, "data", "estoque.csv")
funcionarios_path = os.path.join(base_dir, "data", "funcionarios.csv")
template_path = os.path.join(base_dir, "tpl", "template.tpl")

class AppEpis:

    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("IMAH - Recibo de Entrega de EPIs")

        # Maximizar janela
        sistema = platform.system()
        if sistema == "Windows":
            self.janela.state('zoomed')
        elif sistema == "Linux":
            self.janela.attributes('-zoomed', True)
        elif sistema == "Darwin":
            self.janela.geometry(f"{self.janela.winfo_screenwidth()}x{self.janela.winfo_screenheight()-40}+0+0")
        else:
            self.janela.attributes('-zoomed', True)

        self.janela.configure(padx=20, pady=20, bg="#f0f0f0")

        # Criar imagens de checkboxes em memória
        self.im_checked, self.im_unchecked = self.create_checkbox_images()

        # ========= GRID SUPERIOR: FUNCIONÁRIOS =========
        frame_func = tk.LabelFrame(
            self.janela,
            text="Funcionário para Entrega",
            font=("Helvetica", 12, "bold"),
            bg="#f0f0f0",
            fg="#34495e",
            padx=10,
            pady=10
        )
        frame_func.pack(fill=tk.BOTH, expand=False, pady=(0, 20))

        columns_func = ("Funcionario", "Empresa", "CNPJ")
        self.tree_func = ttk.Treeview(
            frame_func,
            columns=columns_func,
            show="headings",
            height=8,
            selectmode="browse"
        )
        self.tree_func.heading("Funcionario", text="Funcionário")
        self.tree_func.heading("Empresa", text="Empresa")
        self.tree_func.heading("CNPJ", text="CNPJ")
        self.tree_func.column("Funcionario", width=400, anchor="w")
        self.tree_func.column("Empresa", width=300, anchor="w")
        self.tree_func.column("CNPJ", width=150, anchor="center")

        scrollbar_func = ttk.Scrollbar(frame_func, orient="vertical", command=self.tree_func.yview)
        self.tree_func.configure(yscrollcommand=scrollbar_func.set)
        self.tree_func.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 5), pady=10)
        scrollbar_func.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)

        # ========= GRID INFERIOR: EPIs =========
        frame_epis = tk.LabelFrame(
            self.janela,
            text="Seleção de EPIs",
            font=("Helvetica", 12, "bold"),
            bg="#f0f0f0",
            fg="#34495e",
            padx=10,
            pady=10
        )
        frame_epis.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        columns_epis = ("Código", "Descrição")
        self.tree_epis = ttk.Treeview(
            frame_epis,
            columns=columns_epis,
            show="tree headings",
            selectmode="extended"
        )
        self.tree_epis.heading("#0", text="Selecionar", anchor=tk.CENTER, command=self.desmarcar_todos_epis)
        self.tree_epis.heading("Código", text="Código", anchor=tk.CENTER)
        self.tree_epis.heading("Descrição", text="Descrição")
        self.tree_epis.column("#0", width=100, stretch=False, anchor=tk.CENTER)
        self.tree_epis.column("Código", width=150, anchor="center")
        self.tree_epis.column("Descrição", width=800, anchor="w")

        style = ttk.Style()
        style.configure("Treeview", rowheight=35, font=("Helvetica", 11))
        style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))

        # Configurar tags para imagens de checkboxes
        self.tree_epis.tag_configure("checked", image=self.im_checked)
        self.tree_epis.tag_configure("unchecked", image=self.im_unchecked)

        scrollbar_epis = ttk.Scrollbar(frame_epis, orient="vertical", command=self.tree_epis.yview)
        self.tree_epis.configure(yscrollcommand=scrollbar_epis.set)
        self.tree_epis.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 5), pady=10)
        scrollbar_epis.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)

        # Bindings
        self.tree_epis.bind("<Button-1>", self.handle_checkbox_click)
        self.tree_epis.bind("<<TreeviewSelect>>", self.handle_epis_selection)

        # Botão principal
        btn_frame = tk.Frame(self.janela, bg="#f0f0f0")
        btn_frame.pack(fill=tk.X, pady=10)

        self.btn_imprimir = ttk.Button(
            btn_frame,
            text="Imprimir Comprovante de Entrega",
            command=self.abrir_modal_quantidades
        )
        self.btn_imprimir.pack(side=tk.RIGHT, padx=20, pady=10)

        # Carregar config para API Omie
        self.config = configparser.ConfigParser()
        if not self.config.read("config.ini", encoding="utf-8"):
            messagebox.showerror("Erro", "Arquivo config.ini não encontrado!")
            self.janela.destroy()
            return

        # Valida seções necessárias
        if "Omie" not in self.config or "EstoqueAjuste" not in self.config:
            messagebox.showerror("Erro", "config.ini deve conter as seções [Omie] e [EstoqueAjuste]")
            self.janela.destroy()
            return

        self.app_key = self.config["Omie"].get("app_key")
        self.app_secret = self.config["Omie"].get("app_secret")
        self.ajustar = self.config["Omie"].getboolean("ajustar_estoque")
        self.omie_url = self.config["EstoqueAjuste"].get("url")

        if not all([self.app_key, self.app_secret, self.omie_url]):
            messagebox.showerror("Erro", "config.ini está faltando app_key, app_secret ou url em [EstoqueAjuste]")
            self.janela.destroy()
            return

        # Carregar dados
        self.carregar_funcionarios()
        self.carregar_epis()

    def create_checkbox_images(self):
        size = 16
        # Imagem unchecked (caixa vazia)
        unchecked = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(unchecked)
        draw.rectangle((2, 2, size-2, size-2), outline="black", width=1)

        # Imagem checked (caixa com X)
        checked = unchecked.copy()
        draw = ImageDraw.Draw(checked)
        draw.line((4, 4, size-4, size-4), fill="black", width=2)
        draw.line((4, size-4, size-4, 4), fill="black", width=2)

        im_unchecked = ImageTk.PhotoImage(unchecked, master=self.janela)
        im_checked = ImageTk.PhotoImage(checked, master=self.janela)
        return im_checked, im_unchecked

    def desmarcar_todos_epis(self):
        for item in self.tree_epis.get_children():
            self.tree_epis.item(item, tags=("unchecked",))
        self.tree_epis.selection_remove(self.tree_epis.get_children())

    def handle_checkbox_click(self, event):
        col = self.tree_epis.identify_column(event.x)
        item = self.tree_epis.identify_row(event.y)
        if col == "#0" and item:  # Clique na coluna de checkbox
            tags = self.tree_epis.item(item, "tags")
            if "checked" in tags:
                new_tag = "unchecked"
                self.tree_epis.selection_remove(item)
            else:
                new_tag = "checked"
                self.tree_epis.selection_add(item)
            self.tree_epis.item(item, tags=(new_tag,))
            return "break"

    def handle_epis_selection(self, event):
        selected = set(self.tree_epis.selection())
        for item in self.tree_epis.get_children():
            should_be_checked = item in selected
            current_tags = self.tree_epis.item(item, "tags")
            new_tag = "checked" if should_be_checked else "unchecked"
            if new_tag not in current_tags:
                self.tree_epis.item(item, tags=(new_tag,))

    def abrir_modal_quantidades(self):
        selected_func = self.tree_func.selection()
        if not selected_func:
            messagebox.showwarning("Aviso", "Selecione um funcionário primeiro.")
            return
        func_values = self.tree_func.item(selected_func[0], "values")
        funcionario = func_values[0]
        empresa = func_values[1]
        cnpj = func_values[2]
        itens_marcados = [i for i in self.tree_epis.get_children() if "checked" in self.tree_epis.item(i, "tags")]
        if not itens_marcados:
            messagebox.showwarning("Aviso", "Marque pelo menos um EPI para entrega.")
            return

        modal = tk.Toplevel(self.janela)
        modal.title("Informar Quantidades Entregues")
        modal.geometry("900x700")
        modal.configure(bg="#f8f9fa")
        modal.resizable(True, True)

        main_frame = ttk.Frame(modal, padding="30 20 30 30")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="COMPROVANTE DE ENTREGA DE EPI", font=("Helvetica", 16, "bold")).pack(anchor="center", pady=(0, 15))
        ttk.Label(main_frame, text=f"Funcionário: {funcionario}", font=("Helvetica", 13)).pack(anchor="w")
        ttk.Label(main_frame, text=f"Empresa: {empresa} - CNPJ: {cnpj}", font=("Helvetica", 11)).pack(anchor="w", pady=(0, 25))

        grid_frame = ttk.Frame(main_frame)
        grid_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 30))

        cols = ("Código", "Descrição", "Quantidade")
        tree_modal = ttk.Treeview(grid_frame, columns=cols, show="headings", height=10)
        tree_modal.heading("Código", text="Código")
        tree_modal.heading("Descrição", text="Descrição do EPI")
        tree_modal.heading("Quantidade", text="Quantidade Entregue")
        tree_modal.column("Código", width=120, anchor="center")
        tree_modal.column("Descrição", width=550, anchor="w")
        tree_modal.column("Quantidade", width=150, anchor="center")

        scrollbar_modal = ttk.Scrollbar(grid_frame, orient="vertical", command=tree_modal.yview)
        tree_modal.configure(yscrollcommand=scrollbar_modal.set)
        tree_modal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_modal.pack(side=tk.RIGHT, fill=tk.Y)

        itens_data = []
        for item in itens_marcados:
            v = self.tree_epis.item(item, "values")
            codigo = v[0]
            descricao = v[1]
            tree_modal.insert("", "end", values=(codigo, descricao, "1"))
            itens_data.append({"codigo": int(codigo), "descricao": descricao, "qtd": 1})

        entry_edit = None
        item_editando = None

        def iniciar_edicao(e):
            nonlocal entry_edit, item_editando
            col = tree_modal.identify_column(e.x)
            item = tree_modal.identify_row(e.y)
            if col != "#3" or not item:
                return
            if entry_edit:
                finalizar_edicao()
            x, y, w, h = tree_modal.bbox(item, col)
            entry_edit = ttk.Entry(tree_modal, justify="center", font=("Helvetica", 12))
            entry_edit.place(x=x, y=y, width=w, height=h)
            current = tree_modal.item(item, "values")[2]
            entry_edit.insert(0, current)
            entry_edit.focus()
            entry_edit.select_range(0, tk.END)
            item_editando = item
            entry_edit.bind("<Return>", lambda e: finalizar_edicao())
            entry_edit.bind("<FocusOut>", lambda e: finalizar_edicao())

        def finalizar_edicao():
            nonlocal entry_edit, item_editando
            if not entry_edit or not item_editando:
                return
            nova = entry_edit.get().strip() or "0"
            try:
                q = int(nova)
                if q < 0:
                    raise ValueError
            except:
                messagebox.showwarning("Erro", "Quantidade deve ser um número inteiro positivo.", parent=modal)
                entry_edit.focus()
                return
            values = tree_modal.item(item_editando, "values")
            tree_modal.item(item_editando, values=(values[0], values[1], str(q)))
            codigo_int = int(values[0])
            for it in itens_data:
                if it["codigo"] == codigo_int:
                    it["qtd"] = q
                    break
            entry_edit.destroy()
            entry_edit = None
            item_editando = None

        tree_modal.bind("<Double-1>", iniciar_edicao)

        # Botões centralizados
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=30)
        inner_buttons = ttk.Frame(buttons_frame)
        inner_buttons.pack()

        def gerar_pdf_e_baixa():
            itens_finais = [(it["codigo"], it["descricao"], it["qtd"]) for it in itens_data if it["qtd"] > 0]
            if not itens_finais:
                messagebox.showwarning("Aviso", "Informe pelo menos uma quantidade maior que zero.")
                return

            data_atual = datetime.now().strftime("%d/%m/%Y")
            data_omie = datetime.now().strftime("%d/%m/%Y")

            # 1. Dispara baixa no Omie para cada item
            if self.ajustar:

                for cod_int, desc, qtd in itens_finais:
                    payload = {
                        "call": "IncluirAjusteEstoque",
                        "app_key": self.app_key,
                        "app_secret": self.app_secret,
                        "param": [{
                            "codigo_local_estoque": 0,
                            "cod_int": cod_int,
                            "data": data_omie,
                            "quan": str(qtd),
                            "obs": f"FOI ENTREGUE AO COLABORADOR {funcionario.upper()} O(S) EPI(S) RELACIONADOS NO COMPROVANTE GERADO EM {data_atual}.",
                            "origem": "AJU",
                            "tipo": "SAI",
                            "motivo": "INV"
                        }]
                    }

                    try:
                        response = requests.post(self.omie_url, json=payload, timeout=10)
                        if response.status_code == 200:
                            result = response.json()
                            if result.get("faultcode"):
                                messagebox.showerror("Erro Omie", f"Erro ao dar baixa no item {cod_int}: {result.get('faultstring')}")
                        else:
                            messagebox.showerror("Erro Omie", f"HTTP {response.status_code} ao dar baixa no item {cod_int}")
                    except Exception as e:
                        messagebox.showerror("Erro de Rede", f"Erro ao conectar com Omie para o item {cod_int}: {str(e)}")
            
            # 2. Gera o PDF
            self.gerar_comprovante_pdf(funcionario, empresa, itens_finais, data_atual)

            # Mensagem final
            # if sucesso_total:
            #     messagebox.showinfo("Sucesso Total", "Comprovante gerado e baixa no estoque realizada com sucesso!")
            # else:
            #     messagebox.showwarning("Parcial", "Comprovante gerado, mas houve erro na baixa de alguns itens no Omie.")

            modal.destroy()

        def cancelar():
            modal.destroy()

        ttk.Button(inner_buttons, text="Cancelar", command=cancelar, width=25).pack(side=tk.LEFT, padx=50)
        ttk.Button(inner_buttons, text="Gerar PDF e Dar Baixa", command=gerar_pdf_e_baixa, width=35).pack(side=tk.LEFT, padx=50)

        style = ttk.Style()
        style.configure("Accent.TButton", font=("Helvetica", 12, "bold"))

        modal.update_idletasks()
        x = self.janela.winfo_rootx() + (self.janela.winfo_width() // 2) - (900 // 2)
        y = self.janela.winfo_rooty() + (self.janela.winfo_height() // 2) - (700 // 2)
        modal.geometry(f"900x700+{x}+{y}")
        modal.transient(self.janela)
        modal.grab_set()
        self.janela.wait_window(modal)

    def gerar_comprovante_pdf(self, funcionario, empresa, itens, data_hoje):
        if not os.path.exists(template_path):
            messagebox.showerror("Erro", "Arquivo TEMPLATE_CONTROLE_EPI.tpl não encontrado!")
            return

        with open(template_path, "r", encoding="utf-8") as f:
            html_template = f.read()

        tabela_itens = """
        <table border="1" cellpadding="8" cellspacing="0" style="width:100%; border-collapse: collapse; margin-top: 20px;">
            <thead>
                <tr style="background-color: #f0f0f0;">
                    <th style="text-align: center;">Código</th>
                    <th style="text-align: left;">Descrição do EPI</th>
                    <th style="text-align: center;">Quantidade</th>
                </tr>
            </thead>
            <tbody>
        """
        for cod, desc, qtd in itens:
            tabela_itens += f"""
                <tr>
                    <td style="text-align: center;">{cod}</td>
                    <td>{desc}</td>
                    <td style="text-align: center;">{qtd}</td>
                </tr>
            """
        tabela_itens += """
            </tbody>
        </table>
        """

        html_final = html_template.replace("{{NOME_FUNCIONARIO}}", funcionario) \
                                  .replace("{{NOME_DA_EMPRESA}}", empresa) \
                                  .replace("{{DATA_HOJE}}", data_hoje) \
                                  .replace("{{TABELA_DE_ITENS}}", tabela_itens)

        filename = f"Comprovante_EPI.pdf"

        try:
            HTML(string=html_final, base_url=base_dir).write_pdf(filename)
        except Exception as e:
            messagebox.showerror("Erro PDF", f"Erro ao gerar PDF: {str(e)}")
            return

        try:
            if platform.system() == "Windows":
                os.startfile(filename)
            elif platform.system() == "Darwin":
                os.system(f"open \"{filename}\"")
            else:
                os.system(f"xdg-open \"{filename}\"")
        except:
            messagebox.showinfo("PDF Gerado", f"Arquivo salvo como:\n{filename}")

    def carregar_funcionarios(self):
        if not os.path.exists(funcionarios_path):
            self.tree_func.insert("", "end", values=("ERRO: data/funcionarios.csv não encontrado!", "", ""))
            return
        try:
            df = pd.read_csv(funcionarios_path, sep=",", encoding="utf-8", dtype=str)
            df = df.dropna(subset=["funcionario", "empresa", "cnpj"])
            df["funcionario"] = df["funcionario"].astype(str).str.strip()
            df["empresa"] = df["empresa"].astype(str).str.strip()
            df["cnpj"] = df["cnpj"].astype(str).str.strip()
            dados = df[["funcionario", "empresa", "cnpj"]].values.tolist()
            dados.sort(key=lambda x: x[0].upper())
            for d in dados:
                self.tree_func.insert("", "end", values=d)
        except Exception as e:
            self.tree_func.insert("", "end", values=("Erro ao carregar funcionários:", str(e), ""))

    def carregar_epis(self):
        if not os.path.exists(data_path):
            self.tree_epis.insert("", "end", values=("", "ERRO: data/estoque.csv não encontrado!"), tags=("unchecked",))
            return
        try:
            df = pd.read_csv(data_path, sep=";", encoding="utf-8", usecols=["Código", "Descrição"], dtype=str)
            df = df.dropna(subset=["Código", "Descrição"])
            df["Código"] = df["Código"].astype(str).str.strip()
            for _, row in df.iterrows():
                self.tree_epis.insert("", "end", values=(row["Código"], row["Descrição"]), tags=("unchecked",))
        except Exception as e:
            self.tree_epis.insert("", "end", values=("", f"Erro: {str(e)}"), tags=("unchecked",))

    def run(self):
        self.janela.mainloop()


if __name__ == "__main__":
    app = AppEpis()
    app.run()
