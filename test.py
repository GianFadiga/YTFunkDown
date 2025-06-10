import yt_dlp
import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.stop_flag = False

    def setup_ui(self):
        self.root.title("YT FunkDown - Music Downloader")
        self.root.geometry("720x500")
        self.root.configure(bg="#1a1a1a")
        self.root.resizable(False, False)

        # Configure custom styles
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure_styles()

        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        ttk.Label(self.main_frame, text="🎵 YT FunkDown", style="Header.TLabel").pack(pady=(0, 10))
        ttk.Label(self.main_frame, text="Download High Quality Music", style="Subheader.TLabel").pack(pady=(0, 20))

        # URL Input
        ttk.Label(self.main_frame, text="YouTube URL:", style="Input.TLabel").pack(anchor="w")
        self.url_entry = ttk.Entry(self.main_frame, width=60, style="Modern.TEntry")
        self.url_entry.pack(fill="x", pady=5)

        # Download Type
        self.type_frame = ttk.Frame(self.main_frame)
        self.type_frame.pack(fill="x", pady=10)
        
        self.choice_var = tk.StringVar(value="Single")
        ttk.Radiobutton(self.type_frame, text="Single Track 🎧", variable=self.choice_var, 
                       value="Single", style="Radio.TRadiobutton").pack(side="left", padx=20)
        ttk.Radiobutton(self.type_frame, text="Playlist 📀", variable=self.choice_var, 
                       value="Playlist", style="Radio.TRadiobutton").pack(side="left", padx=20)

        # Progress Section
        self.progress = ttk.Progressbar(self.main_frame, orient="horizontal", 
                                      mode="determinate", style="Modern.Horizontal.TProgressbar")
        self.progress.pack(fill="x", pady=10)
        
        self.status_label = ttk.Label(self.main_frame, text="Ready", style="Status.TLabel")
        self.status_label.pack(pady=5)

        # Download Button
        ttk.Button(self.main_frame, text="⏬ Start Download", style="Modern.TButton", 
                 command=self.start_download).pack(pady=20)

    def configure_styles(self):
        # Color scheme
        self.style.configure("TFrame", background="#1a1a1a")
        self.style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), 
                           foreground="#ffffff", background="#1a1a1a")
        self.style.configure("Subheader.TLabel", font=("Segoe UI", 12), 
                           foreground="#cccccc", background="#1a1a1a")
        self.style.configure("Input.TLabel", font=("Segoe UI", 11), 
                           foreground="#ffffff", background="#1a1a1a")
        self.style.configure("Modern.TEntry", fieldbackground="#2a2a2a", 
                           foreground="#ffffff", insertcolor="#ffffff")
        self.style.configure("Radio.TRadiobutton", font=("Segoe UI", 11), 
                           foreground="#ffffff", background="#1a1a1a")
        self.style.configure("Modern.Horizontal.TProgressbar", troughcolor="#2a2a2a", 
                           background="#007acc")
        self.style.configure("Status.TLabel", font=("Segoe UI", 10), 
                           foreground="#cccccc", background="#1a1a1a")
        self.style.configure("Modern.TButton", font=("Segoe UI", 12, "bold"), 
                           foreground="#ffffff", background="#007acc", 
                           borderwidth=0, padding=10)
        self.style.map("Modern.TButton", background=[("active", "#005f99")])

    def start_download(self):
        url = self.url_entry.get().strip()
        download_type = self.choice_var.get()
        output_path = filedialog.askdirectory(title="Select Download Folder")

        if not url:
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return
        if not output_path:
            return

        self.progress['value'] = 0
        self.status_label.config(text="Starting download...")
        self.root.update_idletasks()

        try:
            if download_type == "Single":
                self.music_download(url, output_path)
            else:
                self.download_playlist(url, output_path)
        except Exception as e:
            messagebox.showerror("Error", f"Download failed: {str(e)}")

    def music_download(self, url, output_path):
        ffmpeg_path = resource_path("ffmpeg/bin/ffmpeg.exe")
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, 'temp_audio.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': ffmpeg_path,
            'progress_hooks': [self.progress_hook],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None)
            
            ydl.download([url])
            
            temp_audio_path = os.path.join(output_path, 'temp_audio.mp3')
            audio_path = os.path.join(output_path, f"{video_title}.mp3")

            if os.path.exists(temp_audio_path):
                os.rename(temp_audio_path, audio_path)
                messagebox.showinfo("Success", f"Saved: {video_title}")
                self.url_entry.delete(0, 'end')
                self.status_label.config(text="Ready")
            else:
                messagebox.showerror("Error", "File conversion failed")

    def download_playlist(self, url, output_path):
        ffmpeg_path = resource_path("ffmpeg/bin/ffmpeg.exe")
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(playlist_index)s-%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': ffmpeg_path,
            'progress_hooks': [self.progress_hook],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            messagebox.showinfo("Success", "Playlist downloaded successfully!")
            self.url_entry.delete(0, 'end')
            self.status_label.config(text="Ready")

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            downloaded_bytes = d.get('downloaded_bytes', 0)
            total_bytes = d.get('total_bytes', 1)
            percent = (downloaded_bytes / total_bytes) * 100
            
            self.progress['value'] = percent
            self.status_label.config(
                text=f"Downloading: {percent:.1f}% | "
                     f"Speed: {d.get('_speed_str', 'N/A')} | "
                     f"ETA: {d.get('_eta_str', 'N/A')}"
            )
            self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = DownloaderApp(root)
    root.mainloop()