from Scripts.library import *
from Scripts.function import *





# Classes
class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        self.delete("all")
        
        if not self.textwidget:
            return
        i = self.textwidget.index("@0,0")

        while True:
            dline = self.textwidget.dlineinfo(i)
            
            if dline is None:
                break
            
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, font=self.textwidget["font"])
            i = self.textwidget.index(f"{i}+1line")



# Janela
def janela():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        pass


    root = tk.Tk()
    root.title("YouTube")
    root.geometry("600x300")


    formato_var = StringVar()
    tipo_var = StringVar(value="audio")
    formato_var.set(".flac")


    frame_texto = tk.Frame(root)
    frame_texto.pack(fill="x", padx=10, pady=5)


    etiqueta_links = Label(frame_texto, text='YouTube Converter', font=('Calibri', 20, 'bold'))
    etiqueta_links.pack(anchor="center", pady=(0,5))


    container_text = tk.Frame(frame_texto)
    container_text.pack(fill="both", expand=True)


    text_line_numbers = TextLineNumbers(container_text, width=30)
    text_line_numbers.grid(row=0, column=0, sticky="ns")
    text_line_numbers.grid_remove()


    caixa_links = tk.Text(container_text, font=('Calibri', 10), height=1, width=60)
    caixa_links.grid(row=0, column=1, sticky="nsew")
    container_text.columnconfigure(1, weight=1)
    text_line_numbers.attach(caixa_links)


    frame_download = tk.Frame(root)
    frame_download.pack(fill="x", padx=10, pady=5)

    # Local
    def selecionar_pasta():
        global caminho_pasta
        
        caminho_pasta = filedialog.askdirectory()
        etiqueta_caminho.config(text=caminho_pasta)


    botao_selecionar = Button(frame_download, text="Local", command=selecionar_pasta)
    botao_selecionar.grid(row=0, column=0, padx=5)


    etiqueta_caminho = Label(frame_download, text="")
    etiqueta_caminho.grid(row=0, column=1, sticky="w")


    frame_tipo = tk.Frame(root)
    frame_tipo.pack(fill="x", padx=10, pady=10)


    # Lista suspensa
    def atualizar_opcoes():
        
        if tipo_var.get() == "audio":
            formato_var.set(".flac")
            opcoes_formato['menu'].delete(0, 'end')
            for fmt in [".mp3", ".wav", ".flac"]:
                opcoes_formato['menu'].add_command(label=fmt, command=tk._setit(formato_var, fmt))
        else:
            formato_var.set(".mp4")
            opcoes_formato['menu'].delete(0, 'end')
            
            for fmt in [".mp4", ".mov", ".avi"]:
                opcoes_formato['menu'].add_command(label=fmt, command=tk._setit(formato_var, fmt))


    frame_radio = tk.Frame(frame_tipo)
    frame_radio.pack(anchor="center")
    radio_audio = tk.Radiobutton(frame_radio, text="Áudio", variable=tipo_var, value="audio", command=atualizar_opcoes)
    radio_video = tk.Radiobutton(frame_radio, text="Vídeo", variable=tipo_var, value="video", command=atualizar_opcoes)
    radio_audio.pack(side="left", padx=5)
    radio_video.pack(side="left", padx=10)


    frame_formato = tk.Frame(root)
    frame_formato.pack(fill="x", padx=10, pady=5)


    opcoes_formato = tk.OptionMenu(frame_formato, formato_var, ".mp3", ".wav", ".flac", ".mp4", ".mov", ".avi")
    opcoes_formato.pack(anchor="center")
    atualizar_opcoes()



    # Confirmar
    def confirmar():
        texto_links = caixa_links.get("1.0", tk.END).strip()
        lista_links = texto_links.splitlines()
        formato = formato_var.get()
        tipo = tipo_var.get()
        
        for link in lista_links:
            if link.strip():
                downloader = Youtube(link.strip(), caminho_pasta, formato, tipo)
                downloader.download()
                print(f"{link.strip()} | {formato}")


    botao_confirmar = Button(root, text='Confirmar', command=confirmar)
    botao_confirmar.pack(pady=20)


    # Atualizar interface
    def atualizar_interface(event=None):
        numero_linhas = int(caixa_links.index("end-1c").split('.')[0])
        caixa_links.configure(height=numero_linhas if numero_linhas > 0 else 1)
        
        if numero_linhas > 1:
            if not text_line_numbers.winfo_ismapped():
                text_line_numbers.grid()
            text_line_numbers.redraw()
        else:
            if text_line_numbers.winfo_ismapped():
                text_line_numbers.grid_remove()


    caixa_links.bind("<KeyRelease>", atualizar_interface)
    caixa_links.bind("<MouseWheel>", atualizar_interface)
    caixa_links.bind("<Button-1>", atualizar_interface)
    caixa_links.bind("<Configure>", atualizar_interface)


    atualizar_interface()
    root.mainloop()


if __name__ == '__main__':
    janela()