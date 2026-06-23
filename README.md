# Transcrição e Resumo de Vídeos/Aúdios

Este programa permite transcrever vídeos do YouTube ou arquivos de áudio locais, gerando um resumo do conteúdo usando GPT-4.

## Funcionalidades

- Download de vídeos do YouTube
- Extração de áudio de vídeos
- Transcrição de áudio para texto
- Geração de resumo usando GPT-4
- Salvamento das transcrições e resumos em arquivos Markdown
- Exibição dos resultados diretamente no terminal

## Requisitos

- Python 3.8 ou superior
- FFmpeg instalado no sistema
- Chave de API da OpenAI

## Instalação

1. Clone este repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Instale o FFmpeg:
- macOS: `brew install ffmpeg`
- Ubuntu: `sudo apt-get install ffmpeg`
- Windows: Baixe do site oficial e adicione ao PATH

4. Crie um arquivo `.env` na raiz do projeto com sua chave da OpenAI:
```
OPENAI_API_KEY=sua_chave_aqui
```

## Uso

O programa pode ser executado diretamente do terminal com os seguintes argumentos:

### Para processar um vídeo do YouTube:
```bash
python transcriber.py --youtube URL_DO_VIDEO
```

### Para processar um arquivo de áudio local:
```bash
python transcriber.py --audio CAMINHO_DO_ARQUIVO
```

### Opções adicionais:
- `--output` ou `-o`: Especifica o caminho para o arquivo de saída
- `--terminal` ou `-t`: Exibe a saída diretamente no terminal

### Exemplos:
```bash
# Processar vídeo do YouTube e exibir no terminal
python transcriber.py --youtube https://www.youtube.com/watch?v=exemplo --terminal

# Processar arquivo de áudio e salvar em um arquivo específico
python transcriber.py --audio caminho/para/audio.mp3 --output minha_nota.md
```

Os resultados serão salvos na pasta `notas` em formato Markdown (se não especificar um arquivo de saída), contendo:
- Título do vídeo (quando aplicável)
- Resumo gerado pelo GPT-4
- Transcrição completa

## Estrutura dos Arquivos

- `transcriber.py`: Programa principal
- `requirements.txt`: Dependências do projeto
- `notas/`: Pasta onde são salvos os resultados (por padrão)
- `.env`: Arquivo de configuração com a chave da API

## Observações

- O programa utiliza o modelo "base" do Whisper para transcrição
- O resumo é gerado usando GPT-4
- Os arquivos temporários (vídeo e áudio) são automaticamente removidos após o processamento
---
*Este README foi atualizado automaticamente em 2026-06-23 09:23:59.*
