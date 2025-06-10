import yt_dlp
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import re # Importar o módulo re para expressões regulares
import platform # Importar o módulo platform para identificar o SO

def resource_path(relative_path):
    """Obtenha o caminho absoluto para recursos incluídos no executável."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def sanitize_filename(filename: str) -> str:
    """
    Sanitiza um nome de arquivo para remover caracteres inválidos para Windows e Linux.

    Args:
        filename (str): O nome do arquivo original.

    Returns:
        str: O nome do arquivo sanitizado.
    """
    if platform.system() == "Windows":
        # Caracteres inválidos no Windows: < > : " / \ | ? *
        invalid_chars = r'[<>:"/\\|?*]'
    else:  # Assumimos Linux/Unix-like
        # Caracteres inválidos comuns no Linux: / (barra, usada para diretórios)
        invalid_chars = r'[/]'

    # Substitui caracteres inválidos por um hífen
    sanitized_filename = re.sub(invalid_chars, '-', filename)

    # Remove caracteres nulos (que podem causar problemas em ambos os sistemas)
    sanitized_filename = sanitized_filename.replace('\0', '-')

    # Opcional: Remover espaços em branco no início/fim e múltiplos hífens
    sanitized_filename = sanitized_filename.strip()
    sanitized_filename = re.sub(r'-+', '-', sanitized_filename) # Substitui múltiplos hífens por um único

    # Opcional: Limitar o tamanho do nome do arquivo (Windows tem limite de 255 caracteres para o caminho completo)
    max_len = 200
    if len(sanitized_filename) > max_len:
        sanitized_filename = sanitized_filename[:max_len]

    return sanitized_filename

def music_download(url, output_path):
    ffmpeg_path = resource_path("ffmpeg/bin/ffmpeg.exe")
    ydl_opts = {
        'format': 'bestaudio/best',
        # Vamos deixar o yt-dlp gerar o nome temporário e depois sanitizar o título original.
        'outtmpl': os.path.join(output_path, 'temp_audio.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': ffmpeg_path
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        info_dict = yt_dlp.YoutubeDL().extract_info(url, download=False)
        video_title = info_dict.get('title', 'unknown_title') # Adicionado um fallback para 'unknown_title'
        
        # --- APLICAR A SANITIZAÇÃO AQUI ---
        sanitized_video_title = sanitize_filename(video_title)
        # --- FIM DA APLICAÇÃO DA SANITIZAÇÃO ---

        temp_audio_path = os.path.join(output_path, 'temp_audio.mp3')
        # Usar o título sanitizado para o nome do arquivo final
        audio_path = os.path.join(output_path, f"{sanitized_video_title}.mp3")

        if os.path.exists(temp_audio_path):
            # Adicionar um tratamento para caso o arquivo já exista
            if os.path.exists(audio_path):
                base, ext = os.path.splitext(audio_path)
                counter = 1
                while os.path.exists(f"{base} ({counter}){ext}"):
                    counter += 1
                audio_path = f"{base} ({counter}){ext}"

            os.rename(temp_audio_path, audio_path)
            messagebox.showinfo("Success", f'Music saved in: {audio_path}')
            url_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Temporary audio file not found.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download: {e}")

def download_playlist(url, output_path):
    ffmpeg_path = resource_path("ffmpeg/bin/ffmpeg.exe")
    ydl_opts = {
        'format': 'bestaudio/best',
        # --- APLICAR SANITIZAÇÃO AQUI, USANDO A OPÇÃO DE AUTO-SANITIZAÇÃO DO YT-DLP ---
        # yt-dlp pode sanitizar nomes automaticamente com a opção --restrict-filenames ou através do template
        # Para garantir compatibilidade com o sistema, podemos deixar o yt-dlp fazer o trabalho pesado
        # Ele já lida com caracteres inválidos em %(title)s
        'outtmpl': os.path.join(output_path, '%(playlist_index)s-%(title)s.%(ext)s'),
        'restrictfilenames': True, # Esta opção restringe os nomes de arquivos para caracteres ASCII seguros e curtos.
        # Você também pode usar %(title)s como está e deixar que o yt-dlp lide com os caracteres inválidos,
        # ou, se quiser ter um controle mais granular, usar um 'postprocessor' para renomear após o download.
        # No entanto, 'restrictfilenames' é a abordagem mais simples e eficaz para playlists.
        # --- FIM DA APLICAÇÃO DA SANITIZAÇÃO ---
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': ffmpeg_path
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", f'Playlist downloaded and saved in: {output_path}')
        url_entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download playlist: {e}")

def start_download():
    url = url_entry.get().strip()
    download_type = choice_var.get()
    output_path = filedialog.askdirectory(title="Select Download Folder")

    if not url:
        messagebox.showerror("Error", "Please enter a valid URL.")
        return
    if not output_path:
        messagebox.showerror("Error", "Please select a download folder.")
        return

    if download_type == "Single":
        music_download(url, output_path)
    elif download_type == "Playlist":
        download_playlist(url, output_path)
    else:
        messagebox.showerror("Error", "Invalid download type selected.")

# GUI Setup
root = tk.Tk()
root.title("YT FunkDown - Music Downloader")
root.geometry("400x300")
root.configure(bg="#1e1e1e")
root.resizable(False, False)

# Styling
font_label = ("Arial", 12)
font_button = ("Arial", 12, "bold")
fg_color = "#ffffff"
button_bg = "#007acc"
button_fg = "#ffffff"

# URL Entry
tk.Label(root, text="Enter YouTube URL:", font=font_label, bg="#1e1e1e", fg=fg_color).pack(pady=10)
url_entry = tk.Entry(root, width=50, bg="#2d2d2d", fg=fg_color, insertbackground=fg_color, relief="flat")
url_entry.pack(pady=5)

# Choice (Single/Playlist)
choice_var = tk.StringVar(value="Single")
tk.Label(root, text="Download Type:", font=font_label, bg="#1e1e1e", fg=fg_color).pack(pady=10)
tk.Radiobutton(root, text="Single Music", variable=choice_var, value="Single", bg="#1e1e1e", fg=fg_color, selectcolor="#2d2d2d").pack()
tk.Radiobutton(root, text="Playlist", variable=choice_var, value="Playlist", bg="#1e1e1e", fg=fg_color, selectcolor="#2d2d2d").pack()

# Download Button
download_button = tk.Button(
    root, 
    text="Download", 
    command=start_download, 
    bg=button_bg, 
    fg=button_fg, 
    font=font_button, 
    relief="flat", 
    bd=0,
    activebackground="#005f99", 
    activeforeground=fg_color
)
download_button.pack(pady=20)

# Set PNG icon
icon_path = resource_path("icon.png")
try:
    root.iconphoto(True, tk.PhotoImage(file=icon_path))
except Exception as e:
    print(f"Error loading icon: {e}")

# Run the GUI
root.mainloop()