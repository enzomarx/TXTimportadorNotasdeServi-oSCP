import pandas as pd
import random
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText
import gettext
import os

# Configuração de internacionalização (i18n)
localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
gettext.bindtextdomain('messages', localedir)
gettext.textdomain('messages')
_ = gettext.gettext

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(_("CSV to TXT Processor"))
        self.geometry("800x600")
        self.configure(bg="#f0f0f0")

        # Fullscreen
        self.attributes('-fullscreen', True)
        self.bind("<Escape>", self.exit_fullscreen)

        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)

        # Botão para importar CSV
        self.import_button = ttk.Button(main_frame, text=_("Import CSV"), command=self.import_csv)
        self.import_button.pack(pady=10)

        # Label para mostrar o caminho do arquivo CSV importado
        self.csv_path_label = ttk.Label(main_frame, text="")
        self.csv_path_label.pack(pady=10)

        # Frame para a tabela e barra de rolagem
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(pady=10, fill="both", expand=True)

        # Tabela para visualizar dados CSV
        self.table = ttk.Treeview(table_frame, columns=("MATRICULA", "BRUTO", "CENTAVOS"), show="headings")
        self.table.heading("MATRICULA", text=_("MATRICULA"))
        self.table.heading("BRUTO", text=_("BRUTO"))
        self.table.heading("CENTAVOS", text=_("CENTAVOS"))

        # Barra de rolagem vertical
        self.vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.table.pack(fill="both", expand=True)

        # Botão para salvar o arquivo processado
        self.save_button = ttk.Button(main_frame, text=_("Save Processed File"), command=self.save_file, state="disabled")
        self.save_button.pack(pady=10)

        # Textbox para logs
        self.log_text = ScrolledText(main_frame, height=10)
        self.log_text.pack(pady=10)

        # Configurações adicionais
        self.config_frame = ttk.LabelFrame(main_frame, text=_("Additional Configurations"))
        self.config_frame.pack(pady=10, fill="x")

        self.date_label = ttk.Label(self.config_frame, text=_("Service Date (DD/MM/YYYY):"))
        self.date_label.grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(self.config_frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        # Botão para trocar de tema
        self.theme_button = ttk.Button(main_frame, text=_("Toggle Theme"), command=self.toggle_theme)
        self.theme_button.pack(pady=10)

    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[(_("CSV files"), "*.csv"), (_("All files"), "*.*")])
        if file_path:
            self.csv_path_label.config(text=file_path)
            try:
                self.df = pd.read_csv(file_path)
                self.df.columns = [col.strip() for col in self.df.columns]
                self.validate_columns()
                self.populate_table()
                self.save_button.config(state="normal")
                self.log_message(_("CSV file imported successfully."))
            except Exception as e:
                messagebox.showerror(_("Error"), str(e))
                self.log_message(_("Failed to import CSV file."))

    def validate_columns(self):
        required_columns = ["MATRICULA", "BRUTO"]
        for col in required_columns:
            if col not in self.df.columns:
                raise ValueError(_("Missing required column: {}").format(col))

    def populate_table(self):
        for i in self.table.get_children():
            self.table.delete(i)
        for _, row in self.df.iterrows():
            matricula = row["MATRICULA"]
            bruto = row["BRUTO"]
            centavos = row["CENTAVOS"]
            self.table.insert("", "end", values=(matricula, bruto, centavos))

    def save_file(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[(_("Text files"), "*.txt"), (_("All files"), "*.*")])
        if save_path:
            new_content = self.process_data()
            try:
                with open(save_path, 'w') as f:
                    f.write(_("Tipo do registro NFS|Cód, espécie|CNPJ cliente padrão|PE|Cód. acumulador|Série|Numero doc||Doc final|Data serviço|Data emissão|valor contábil|||||||||CFPS|||||Cod SCP|||Valor serviço||||\n"))
                    f.write(_("Parcela NFS|Data|Valor|||||||||||||||||||\n"))
                    for line in new_content:
                        f.write(line)
                messagebox.showinfo(_("Success"), _("New TXT file created successfully: {}").format(save_path))
                self.log_message(_("TXT file saved successfully."))
            except Exception as e:
                messagebox.showerror(_("Error"), str(e))
                self.log_message(_("Failed to save TXT file."))
        else:
            messagebox.showwarning(_("Cancelled"), _("Save action cancelled."))

    def process_data(self):
        new_content = []
        service_date = self.date_entry.get() if self.date_entry.get() else "30/06/2024"
        for _, row in self.df.iterrows():
            matricula = row['MATRICULA']
            numero_doc = random.randint(1000, 9999)
            doc_final = random.randint(1000, 9999)
            bruto = row['BRUTO']
            centavos = f"{float(bruto):.2f}".split('.')[1]

            tipo_registro_nfs = f"3000|31|00000000000000|PE|{matricula}|6|{numero_doc}||{numero_doc}|{service_date}|{service_date}|{bruto},{centavos}|||||||||9101|||||{matricula}|||{bruto},{centavos}||||"
            parcela_nfs = f"3500|{service_date}|{bruto},{centavos}|||||||||||||||||||"

            new_content.append(f"{tipo_registro_nfs}\n{parcela_nfs}\n")
        return new_content

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def toggle_theme(self):
        current_theme = self.tk.call("ttk::style", "theme", "use")
        new_theme = "clam" if current_theme == "default" else "default"
        self.tk.call("ttk::style", "theme", "use", new_theme)

    def exit_fullscreen(self, event=None):
        self.attributes('-fullscreen', False)

if __name__ == "__main__":
    app = Application()
    app.mainloop()

'''barra de rolagem na janela do aplicativo também
os centavos nao foram capturados do meu csv e est a coluna toda zerada
o csv que esta sendo importado deve ser csv separado por virgulas simples (x,x,x)
se o usuario tentar importar outro tipo de csv, entao converta para esse tipo de csv simples'''
