Requisitos
Para rodar o YTFunkDown, você vai precisar do Python instalado (versão 3.8 ou superior é o ideal). Além disso, o programa usa o FFmpeg para processar o áudio.

Python 3.8+

FFmpeg: O YTFunkDown precisa do FFmpeg para converter os vídeos para MP3. Você pode baixá-lo em ffmpeg.org/download.html. Depois de baixar o pacote do FFmpeg, descompacte-o e pegue o arquivo ffmpeg.exe de dentro da pasta bin. Você precisará colocar esse ffmpeg.exe dentro de uma pasta chamada ffmpeg/bin na raiz do seu projeto YTFunkDown.

A estrutura do seu projeto deve ficar assim:

seu_projeto_YTFunkDown/
├── ytfunkdown.py
├── requirements.txt
├── icon.png
└── ffmpeg/
    └── bin/
        └── ffmpeg.exe
(Importante: O YTFunkDown procura o ffmpeg.exe nesse caminho específico. Se ele não for encontrado, o download não funcionará.)*

Como Instalar e Executar
Siga os passos abaixo para configurar e rodar o YTFunkDown no seu computador.

1. Clonar o Repositório
Primeiro, clone o repositório para o seu computador:

Bash

git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
(Lembre-se de substituir SEU_USUARIO e SEU_REPOSITORIO pelo seu usuário e nome do repositório no GitHub.)

2. Criar e Ativar um Ambiente Virtual (Recomendado)
É uma ótima ideia usar um ambiente virtual para organizar as dependências do projeto. Isso evita qualquer tipo de conflito com outras instalações do Python que você possa ter.

Bash

# Criar o ambiente virtual (venv)
python -m venv venv

# Ativar o ambiente virtual

# No Windows:
.\venv\Scripts\activate

# No macOS/Linux:
source venv/bin/activate
3. Instalar as Dependências
Com o ambiente virtual ativado, instale as bibliotecas necessárias que estão listadas no arquivo requirements.txt. Certifique-se de que este arquivo existe na raiz do seu projeto e contém as dependências (como yt-dlp e Pillow).

Bash

pip install -r requirements.txt
4. Executar o Software
Você tem duas maneiras de executar o YTFunkDown:

Opção A: Executar Diretamente com Python (Ideal para quem está desenvolvendo)
Depois de baixar o ffmpeg.exe e colocá-lo na pasta correta (conforme explicado nos Requisitos), e com as dependências instaladas e o ambiente virtual ativado, é só rodar o script diretamente:

Bash

python ytfunkdown.py
A interface gráfica do YTFunkDown vai abrir.

Opção B: Gerar um Executável Standalone (.exe)
Se você prefere ter um único arquivo executável que pode ser compartilhado (ideal para usuários finais), você pode criá-lo usando o PyInstaller.

Certifique-se de que o PyInstaller está instalado no seu ambiente virtual:

Bash

pip install pyinstaller
Em seguida, execute este comando na raiz do projeto (confirme que o arquivo icon.png está na raiz do seu projeto):

Bash

pyinstaller --onefile --windowed --add-data "icon.png;." ytfunkdown.py
Após a execução, o executável (ytfunkdown.exe no Windows) estará na pasta dist/ dentro do seu diretório de projeto. Lembre-se: mesmo usando o executável, o ffmpeg.exe ainda precisará estar na pasta ffmpeg/bin dentro do mesmo diretório onde o ytfunkdown.exe está.

5. Desativar o Ambiente Virtual (Opcional)
Quando você terminar de usar o YTFunkDown ou quiser trabalhar em outro projeto, pode desativar o ambiente virtual:

Bash

deactivate
Contribuição
Contribuições são sempre bem-vindas! Se você tiver ideias para melhorias, encontrar bugs ou quiser adicionar novas funcionalidades, sinta-se à vontade para abrir uma issue ou enviar um pull request.
