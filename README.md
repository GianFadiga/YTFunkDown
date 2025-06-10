# 🎵 YTFunkDown

YTFunkDown é uma aplicação simples que permite baixar vídeos do YouTube em formato MP3 com uma interface gráfica amigável. Ideal para quem quer suas músicas favoritas no computador, rápido e sem complicações.

---

## 📋 Requisitos

Para rodar o **YTFunkDown**, você vai precisar do seguinte:

- 🐍 **Python** 3.8 ou superior  
- 🎬 **FFmpeg** (necessário para conversão dos vídeos em áudio)

> ⚠️ O `ffmpeg.exe` **precisa** estar em um caminho específico para o programa funcionar corretamente.

### 📁 Estrutura Esperada do Projeto

```
seu_projeto_YTFunkDown/
├── ytfunkdown.py
├── requirements.txt
├── icon.png
└── ffmpeg/
    └── bin/
        └── ffmpeg.exe
```

> 🛠️ O YTFunkDown procura o `ffmpeg.exe` especificamente em `ffmpeg/bin/`. Certifique-se de manter essa estrutura.

Você pode baixar o FFmpeg aqui: [ffmpeg.org/download.html](https://ffmpeg.org/download.html)

---

## 🚀 Como Instalar e Executar

### 1️⃣ Clonar o Repositório

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
```

Substitua `SEU_USUARIO` e `SEU_REPOSITORIO` pelo seu nome de usuário e nome do repositório.

---

### 2️⃣ Criar e Ativar um Ambiente Virtual (Recomendado)

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
# No Windows:
.\venv\Scripts\activate

# No macOS/Linux:
source venv/bin/activate
```

---

### 3️⃣ Instalar as Dependências

Com o ambiente virtual ativado, instale as bibliotecas:

```bash
pip install -r requirements.txt
```

Certifique-se de que o arquivo `requirements.txt` contém dependências como `yt-dlp` e `Pillow`.

---

### 4️⃣ Executar o Software

#### 🅰️ Opção A: Rodar com Python (modo desenvolvedor)

```bash
python ytfunkdown.py
```

A interface gráfica será aberta automaticamente.

---

#### 🅱️ Opção B: Gerar um Executável Standalone

1. Instale o **PyInstaller**:

```bash
pip install pyinstaller
```

2. Gere o executável:

```bash
pyinstaller --onefile --windowed --add-data "icon.png;." ytfunkdown.py
```

- O executável será gerado na pasta `dist/`.
- O `ffmpeg.exe` **deve estar** em `ffmpeg/bin/` no mesmo diretório do `.exe`.

---

### 5️⃣ Desativar o Ambiente Virtual (Opcional)

```bash
deactivate
```

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---
