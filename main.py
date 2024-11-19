import os
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle
import yt_dlp

# Set a custom background color
Window.clearcolor = get_color_from_hex("#2E3440")  # Dark gray-blue background

class YouTubeDownloaderApp(App):
    def build(self):
        # Main layout with padding and spacing
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Add a logo or banner image
        self.banner = Image(source='D:\working\python\Android project\logo.jpg', size_hint=(1, 0.3))
        self.layout.add_widget(self.banner)

        # Animated text label
        self.title_label = Label(
            text="YouTube Video Downloader",
            font_size='20sp',
            color=get_color_from_hex("#88C0D0"),  # Light blue text
            bold=True,
            size_hint=(1, 0.1)
        )
        self.layout.add_widget(self.title_label)
        self.animate_label()

        # Input for video URL
        self.url_input = TextInput(
            hint_text="Enter YouTube video URL",
            multiline=False,
            size_hint=(1, 0.1),
            background_color=get_color_from_hex("#3B4252"),
            foreground_color=get_color_from_hex("#E5E9F0"),  # Light gray
            cursor_color=get_color_from_hex("#88C0D0"),
        )
        self.layout.add_widget(self.url_input)

        # Button to select output directory
        self.output_button = Button(
            text="Select Output Directory",
            size_hint=(1, 0.1),
            background_color=get_color_from_hex("#4C566A"),
            color=get_color_from_hex("#ECEFF4"),
        )
        self.output_button.bind(on_press=self.open_file_chooser)
        self.layout.add_widget(self.output_button)

        # Label to display selected output directory
        self.output_label = Label(
            text="Output Directory: Not Selected",
            font_size='14sp',
            color=get_color_from_hex("#D8DEE9"),  # Light gray
            size_hint=(1, 0.1),
        )
        self.layout.add_widget(self.output_label)

        # Progress Bar for downloading
        self.progress_bar = ProgressBar(
            max=100, 
            value=0, 
            size_hint=(1, 0.1),
        )
        self.layout.add_widget(self.progress_bar)

        # Add custom canvas instructions for styling the progress bar
        with self.progress_bar.canvas.before:
            Color(0.643, 0.741, 0.549, 1)  # Greenish color for the progress bar
            self.rect = Rectangle(size=self.progress_bar.size, pos=self.progress_bar.pos)

        self.progress_bar.bind(size=self.update_rect, pos=self.update_rect)

        # Status label
        self.status_label = Label(
            text="",
            font_size='16sp',
            color=get_color_from_hex("#A3BE8C"),  # Light green
            size_hint=(1, 0.2),
        )
        self.layout.add_widget(self.status_label)

        # Button to start download with hover effect
        self.download_button = Button(
            text="Download Video",
            size_hint=(1, 0.2),
            background_color=get_color_from_hex("#5E81AC"),
            color=get_color_from_hex("#ECEFF4"),
        )
        self.download_button.bind(on_press=self.start_download)
        self.layout.add_widget(self.download_button)

        return self.layout

    def animate_label(self):
        # Create a simple animation for the title label
        anim = Animation(color=get_color_from_hex("#D08770"), duration=1) + Animation(color=get_color_from_hex("#88C0D0"), duration=1)
        anim.repeat = True
        anim.start(self.title_label)

    def open_file_chooser(self, instance):
        # Popup for file chooser
        self.file_chooser = FileChooserListView(path=os.path.expanduser("~"))
        popup_layout = BoxLayout(orientation='vertical')
        popup_layout.add_widget(self.file_chooser)

        # Select and cancel buttons
        select_button = Button(text="Select", size_hint=(1, 0.1))
        select_button.bind(on_press=self.select_directory)
        popup_layout.add_widget(select_button)

        self.popup = Popup(title="Select Output Directory", content=popup_layout, size_hint=(0.9, 0.9))
        self.popup.open()

    def select_directory(self, instance):
        # Get selected directory
        selected_dir = self.file_chooser.path
        if selected_dir:
            self.output_label.text = f"Output Directory: {selected_dir}"
            self.output_directory = selected_dir
        self.popup.dismiss()

    def start_download(self, instance):
        video_url = self.url_input.text
        output_dir = getattr(self, 'output_directory', '.')

        if not video_url.strip():
            self.update_status("Error: Please enter a YouTube video URL.", "#BF616A")  # Red text
            return

        if not os.path.exists(output_dir):
            self.update_status("Error: Output directory does not exist.", "#BF616A")  # Red text
            return

        self.update_status("Starting download...", "#A3BE8C")  # Green text
        threading.Thread(target=self.download_video, args=(video_url, output_dir), daemon=True).start()

    def update_status(self, message, color):
        self.status_label.text = message
        self.status_label.color = get_color_from_hex(color)

    def download_video(self, url, output_dir):
        def hook(d):
            if d['status'] == 'downloading':
                # Update the progress bar based on download progress
                progress = d['downloaded_bytes'] / d['total_bytes'] * 100 if d['total_bytes'] else 0
                self.update_progress(progress)

                self.update_status(
                    f"Downloading: {d['filename']} - {d['downloaded_bytes'] / 1024 / 1024:.2f} MB downloaded",
                    "#EBCB8B",  # Yellow text
                )
            elif d['status'] == 'finished':
                self.update_status(f"Download completed: {d['filename']}", "#A3BE8C")  # Green text
                self.update_progress(100)

        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'progress_hooks': [hook],
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            self.update_status(f"Error: {e}", "#BF616A")  # Red text

    def update_progress(self, progress):
        self.progress_bar.value = progress

    def update_rect(self, instance, value):
        # Update the size of the rectangle inside the ProgressBar
        self.rect.size = instance.size
        self.rect.pos = instance.pos


if __name__ == '__main__':
    YouTubeDownloaderApp().run()
