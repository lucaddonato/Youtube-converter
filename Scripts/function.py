from Scripts.library import *
from Scripts.script import *





# Classes e funções
class Youtube:
    def __init__(self, url: str, caminho: str, formato: str = ".flac"):
        self.url = url
        self.caminho = caminho
        self.formato = formato


    def receber_url(self):
        # Verifica se a URL é de uma playlist ou de um único vídeo
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
        # Cria um nome temporário com o sufixo '_tmp' antes da extensão
        arquivo_temp = nome + "_tmp" + ext
        try:
            # O parâmetro -v error exibe apenas erros.
            comando = ["ffmpeg", "-v", "error", "-i", arquivo, "-c:a", "flac", "-y", arquivo_temp]
            subprocess.run(comando, check=True)
            os.remove(arquivo)
            os.rename(arquivo_temp, arquivo)
        except subprocess.CalledProcessError as e:
            print("Erro | ", e)



    def download(self):
        videos = self.receber_url()
        try:
            for video in videos:
                try:
                    yt = YouTube(video)
                    # Seleciona apenas a faixa de áudio, ordenada pela qualidade
                    audio = yt.streams.filter(only_audio=True).order_by("abr").desc().first()
                    arquivo_baixado = audio.download(output_path=self.caminho)
                    nome_original, ext = os.path.splitext(arquivo_baixado)
                    novo_arquivo = nome_original + self.formato
                    os.rename(arquivo_baixado, novo_arquivo)
                    # Corrige o áudio para remover possíveis corrupções
                    self.corrigir_audio(novo_arquivo)
                except KeyError:
                    print("Informações não encontradas")
                except FileExistsError:
                    print("Esse arquivo já existe")
        except TypeError:
            print("Erro")