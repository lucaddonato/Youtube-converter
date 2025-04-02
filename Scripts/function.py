from Scripts.library import *
from Scripts.script import *





# Classes e funções
class Youtube:
    def __init__(self, url: str, caminho: str, formato: str = ".flac", tipo: str = "audio"):
        self.url = url
        self.caminho = caminho
        self.formato = formato
        self.tipo = tipo



    def receber_url(self):
        if 'com/play' in self.url:
            playlist = Playlist(self.url)
            lista = []
            for video in playlist.video_urls:
                lista.append(video)
            return lista
        else:
            return [self.url]



    def corrigir_audio(self, arquivo):
        nome, ext = os.path.splitext(arquivo)
        arquivo_temp = nome + "_tmp" + ext
        
        try:
            comando = ["ffmpeg", "-v", "error", "-i", arquivo, "-c:a", "flac", "-y", arquivo_temp]
            subprocess.run(comando, check=True)
            os.remove(arquivo)
            os.rename(arquivo_temp, arquivo)
            print("Áudio corrigido com sucesso!")
        except subprocess.CalledProcessError as e:
            print("Erro ao corrigir o áudio:", e)



    def download(self):
        videos = self.receber_url()
        try:
            for video in videos:
                try:
                    yt = YouTube(video)
                    if self.tipo == "video":
                        stream_video = yt.streams.filter(progressive=True).get_highest_resolution()
                        arquivo_baixado = stream_video.download(output_path=self.caminho)
                        nome_original, ext = os.path.splitext(arquivo_baixado)
                        novo_arquivo = nome_original + self.formato
                        if self.formato.lower() != ext.lower():
                            os.rename(arquivo_baixado, novo_arquivo)
                        print(yt.title + " Download Concluído!")
                    else:
                        audio = yt.streams.filter(only_audio=True).order_by("abr").desc().first()
                        arquivo_baixado = audio.download(output_path=self.caminho)
                        nome_original, ext = os.path.splitext(arquivo_baixado)
                        novo_arquivo = nome_original + self.formato
                        os.rename(arquivo_baixado, novo_arquivo)
                        self.corrigir_audio(novo_arquivo)
                        print(yt.title + " Download Concluído!")
                except KeyError:
                    print("Informações não encontradas")
                except FileExistsError:
                    print("Esse arquivo já existe")
        except TypeError:
            print("Erro")