#%%
import os
import sys
import argparse
from dotenv import load_dotenv
import whisper as sr
from typing import Optional

# %%


class Transcriber:
    def __init__(self):
        #load_dotenv()
        self.model = sr.load_model("base")
        
    # def baixar_video_youtube(self, url: str) -> str:
    #     """Baixa um vídeo do YouTube e retorna o caminho do arquivo."""
    #     try:
    #         print(f"Baixando vídeo do YouTube: {url}")
    #         ydl_opts = {
    #             'extract_audio': ''
    #             'format': 'best[ext=wav]',
    #             'outtmpl': '%(title)s.%(ext)s',
    #         }
    #         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    #             info = ydl.extract_info(url, download=True)
    #             video_path = f"{info['title']}.wav"
    #         print(f"Vídeo baixado com sucesso: {video_path}")
    #         return video_path
    #     except Exception as e:
    #         print(f"Erro ao baixar vídeo: {str(e)}")
    #         return None

    # def extrair_audio(self, video_path: str) -> Optional[str]:
    #     """Extrai o áudio de um arquivo de vídeo."""
    #     try:
    #         print(f"Extraindo áudio do vídeo: {video_path}")
    #         video = VideoFileClip(video_path)
    #         audio_path = video_path.replace('.mp4', '.wav')
    #         video.audio.write_audiofile(audio_path)
    #         video.close()
    #         print(f"Áudio extraído com sucesso: {audio_path}")
    #         return audio_path
    #     except Exception as e:
    #         print(f"Erro ao extrair áudio: {str(e)}")
    #         return None

    def transcrever_audio(self, audio_path: str) -> Optional[str]:
        """Transcreve um arquivo de áudio para texto."""
        print(f"Transcrevendo áudio: {audio_path}")
        result = self.model.transcribe(audio_path, language='pt', FP16=False)  # Especifica o idioma português
        if result and 'text' in result:
            print(f"Transcrição concluída: {audio_path}")
            return result['text']
        else:           
            print(f"Erro na transcrição do áudio: {audio_path}")
            return None

    # %%
    # def gerar_resumo(self, texto: str) -> str:
    #     """Gera um resumo do texto usando GPT-4."""
    #     try:
    #         print("Gerando resumo com GPT-4...")
    #         response = openai.ChatCompletion.create(
    #             model="gpt-4",
    #             messages=[
    #                 {"role": "system", "content": "Você é um assistente especializado em criar resumos concisos e bem estruturados."},
    #                 {"role": "user", "content": f"Por favor, crie um resumo detalhado e bem estruturado do seguinte texto em português brasileiro:\n\n{texto}"}
    #             ]
    #         )
    #         print("Resumo gerado com sucesso")
    #         return response.choices[0].message.content
    #     except Exception as e:
    #         print(f"Erro ao gerar resumo: {str(e)}")
    #         return None

    # def salvar_nota(self, texto: str, resumo: str, titulo: str = None, output_file: str = None) -> str:
    #     """Salva a transcrição e o resumo em um arquivo markdown."""
    #     try:
    #         if output_file:
    #             filename = output_file
    #         else:
    #             if not os.path.exists("notas"):
    #                 os.makedirs("notas")
                
    #             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    #             filename = f"notas/transcricao_{timestamp}.md"
            
    #         print(f"Salvando nota em: {filename}")
            
    #         with open(filename, "w", encoding="utf-8") as f:
    #             f.write(f"# {titulo or 'Transcrição'}\n\n")
    #             f.write("## Resumo\n\n")
    #             f.write(f"{resumo}\n\n")
    #             f.write("## Transcrição Completa\n\n")
    #             f.write(f"{texto}\n")
            
    #         print(f"Nota salva com sucesso em: {filename}")
    #         return filename
    #     except Exception as e:
    #         print(f"Erro ao salvar nota: {str(e)}")
    #         return None

    # def processar_video_youtube(self, url: str, output_file: str = None, terminal_output: bool = False) -> Optional[str]:
    #     """Processa um vídeo do YouTube completo: download, extração de áudio, transcrição e resumo."""
    #     try:
    #         # Baixar vídeo
    #         video_path = self.baixar_video_youtube(url)
    #         if not video_path:
    #             return None

    #         # Extrair áudio
    #         audio_path = self.extrair_audio(video_path)
    #         if not audio_path:
    #             return None

    #         # Transcrever áudio
    #         transcricao = self.transcrever_audio(audio_path)
    #         if not transcricao:
    #             return None

    #         # Gerar resumo
    #         resumo = self.gerar_resumo(transcricao)
    #         if not resumo:
    #             return None

    #         # Salvar nota
    #         yt = yt_dlp.YoutubeDL()
    #         yt.extract_info(url)
    #         nota_path = self.salvar_nota(transcricao, resumo, yt.extract_info(url)['title'], output_file)
            
    #         # Limpar arquivos temporários
    #         os.remove(video_path)
    #         os.remove(audio_path)
            
    #         if terminal_output:
    #             print("\n" + "="*50)
    #             print(f"TÍTULO: {yt.extract_info(url)['title']}")
    #             print("="*50)
    #             print("\nRESUMO:")
    #             print("-"*50)
    #             print(resumo)
    #             print("-"*50)
    #             print("\nTRANSCRIÇÃO COMPLETA:")
    #             print("-"*50)
    #             print(transcricao)
    #             print("-"*50)
            
    #         return nota_path
    #     except Exception as e:
    #         print(f"Erro no processamento do vídeo: {str(e)}")
    #         return None

    # def processar_audio_local(self, audio_path: str, output_file: str = None, terminal_output: bool = False) -> Optional[str]:
    #     """Processa um arquivo de áudio local: transcrição e resumo."""
    #     try:
    #         if not os.path.exists(audio_path):
    #             print(f"Arquivo não encontrado: {audio_path}")
    #             return None

    #         # Transcrever áudio
    #         transcricao = self.transcrever_audio(audio_path)
    #         if not transcricao:
    #             return None

    #         # Gerar resumo
    #         resumo = self.gerar_resumo(transcricao)
    #         if not resumo:
    #             return None

    #         # Salvar nota
    #         titulo = os.path.basename(audio_path)
    #         nota_path = self.salvar_nota(transcricao, resumo, titulo, output_file)
            
    #         if terminal_output:
    #             print("\n" + "="*50)
    #             print(f"TÍTULO: {titulo}")
    #             print("="*50)
    #             print("\nRESUMO:")
    #             print("-"*50)
    #             print(resumo)
    #             print("-"*50)
    #             print("\nTRANSCRIÇÃO COMPLETA:")
    #             print("-"*50)
    #             print(transcricao)
    #             print("-"*50)
            
    #         return nota_path
        # except Exception as e:
        #     print(f"Erro no processamento do áudio: {str(e)}")
        #     return None

# def main():
#     parser = argparse.ArgumentParser(description='Transcrição e resumo de vídeos do YouTube ou áudios locais')
#     parser.add_argument('--youtube', '-y', type=str, help='URL do vídeo do YouTube')
#     parser.add_argument('--audio', '-a', type=str, help='Caminho para o arquivo de áudio local')
#     parser.add_argument('--output', '-o', type=str, help='Caminho para o arquivo de saída (opcional)')
#     parser.add_argument('--terminal', '-t', action='store_true', help='Exibir saída no terminal')
    
#     args = parser.parse_args()
    
#     transcriber = Transcriber()
    
#     if args.youtube:
#         resultado = transcriber.processar_video_youtube(args.youtube, args.output, args.terminal)
#         if resultado:
#             print(f"\nProcessamento concluído! Nota salva em: {resultado}")
#         else:
#             print("\nErro no processamento do vídeo.")
#     elif args.audio:
#         resultado = transcriber.processar_audio_local(args.audio, args.output, args.terminal)
#         if resultado:
#             print(f"\nProcessamento concluído! Nota salva em: {resultado}")
#         else:
#             print("\nErro no processamento do áudio.")
#     else:
#         print("Erro: Você deve especificar uma URL do YouTube ou um arquivo de áudio local.")
#         print("Uso: python transcriber.py --youtube URL ou python transcriber.py --audio CAMINHO")
#         print("Opções adicionais: --output CAMINHO para especificar o arquivo de saída, --terminal para exibir a saída no terminal")

# %%
if __name__ == "__main__":
    transcriber = Transcriber()
    # Exemplo de uso:
    audio_path = "/Users/vitor/aula-2.mp4"
    transcricao = transcriber.transcrever_audio(audio_path)
    print(transcricao)
    
    # Para testar a transcrição, descomente a linha acima e forneça um caminho válido para um arquivo de áudio.
    #pass