import os
from tkinter import *
import pygame

class MusicPlayer:
    def __init__(self, master):
        self.master = master
        self.master.title("Music Player")
        self.master.geometry("400x350")
        self.master.configure(bg="#9370DB")  # Set background color to purple

        # Specify the directory path where your music files are located
        self.music_directory = "F:/music_player/songs"

        self.playlist = Listbox(self.master, bg="#483D8B", fg="white", selectbackground="green", selectmode=SINGLE)
        self.playlist.pack(pady=10)

        # Automatically load music from the specified directory
        self.load_music()

        # Create a frame to contain the buttons
        button_frame = Frame(self.master, bg="#9370DB")
        button_frame.pack()

        self.play_button = Button(button_frame, text="Play", command=self.play_music, bg="#8A2BE2", fg="white")  # Purple button
        self.play_button.pack(side=LEFT, padx=10)

        self.pause_button = Button(button_frame, text="Pause", command=self.pause_music, bg="#8A2BE2", fg="white")  # Purple button
        self.pause_button.pack(side=LEFT, padx=10)

        self.stop_button = Button(button_frame, text="Stop", command=self.stop_music, bg="#8A2BE2", fg="white")  # Purple button
        self.stop_button.pack(side=LEFT, padx=10)

        self.loop_button = Button(button_frame, text="Loop", command=self.toggle_loop, bg="#8A2BE2", fg="white")  # Purple button
        self.loop_button.pack(side=LEFT, padx=10)

        self.current_song = StringVar()
        self.song_label = Label(self.master, textvariable=self.current_song, wraplength=300, bg="#9370DB", fg="white")  # Purple label
        self.song_label.pack()

        self.progress_bar = Scale(self.master, from_=0, to=100, orient=HORIZONTAL, showvalue=0, length=350, sliderlength=10, command=self.set_position)
        self.progress_bar.pack(pady=10)

        self.current_index = 0
        self.playback_position = 0
        self.loop_enabled = False

        # Start the timer to update the progress bar
        self.master.after(100, self.update_progress)

    def load_music(self):
        if os.path.exists(self.music_directory):
            self.song_list = [file for file in os.listdir(self.music_directory) if file.endswith(".mp3")]
            self.playlist.delete(0, END)  # Clear the playlist
            for song in self.song_list:
                self.playlist.insert(END, song)

    def play_music(self):
        try:
            if pygame.mixer.get_busy():
                pygame.mixer.music.stop()

            self.current_index = self.playlist.curselection()[0]
            current_song = self.song_list[self.current_index]
            pygame.mixer.music.load(os.path.join(self.music_directory, current_song))
            pygame.mixer.music.play(loops=-1 if self.loop_enabled else 0, start=int(self.playback_position))
            self.current_song.set("Now Playing: " + current_song)
        except pygame.error as e:
            print(f"Error during playback: {e}")

    def pause_music(self):
        pygame.mixer.music.pause()

    def stop_music(self):
        pygame.mixer.music.stop()
        self.playback_position = 0
        self.progress_bar.set(0)
        self.current_song.set("")

    def set_position(self, value):
        # Convert scale value to percentage and update playback position
        percentage = float(value) / 100
        current_song_path = os.path.join(self.music_directory, self.song_list[self.current_index])
        duration = pygame.mixer.Sound(current_song_path).get_length()
        playback_position = percentage * duration

        # Update the cursor position
        self.playback_position = playback_position

        # If the song is currently playing, set the new playback position
        if pygame.mixer.get_busy():
            pygame.mixer.music.set_pos(percentage)

        # Update the progress bar and song timings
        self.update_progress()

    def update_progress(self):
        if pygame.mixer.get_busy():
            # Get the current position of the music
            current_position = pygame.mixer.music.get_pos() / 1000  # Convert milliseconds to seconds

            # Update the playback position for synchronization
            self.playback_position = current_position

            # Update progress bar and song timings
            current_song_path = os.path.join(self.music_directory, self.song_list[self.current_index])
            duration = pygame.mixer.Sound(current_song_path).get_length()

            # Update progress bar and song timings
            if duration > 0:
                percentage = (current_position / duration) * 100
                self.progress_bar.set(percentage)
                self.current_song.set(f"Now Playing: {self.format_time(current_position)} / {self.format_time(duration)}")

        # Schedule the update every 100 milliseconds
        self.master.after(100, self.update_progress)

    @staticmethod
    def format_time(seconds):
        minutes, seconds = divmod(int(seconds), 60)
        return f"{minutes:02d}:{seconds:02d}"

    def toggle_loop(self):
        self.loop_enabled = not self.loop_enabled
        loop_state = "ON" if self.loop_enabled else "OFF"
        self.loop_button.configure(text=f"Loop {loop_state}")

if __name__ == "__main__":
    pygame.mixer.pre_init(44100, -16, 2, 2048)  # Adjust buffer size
    pygame.init()
    root = Tk()
    app = MusicPlayer(root)
    root.mainloop()
    pygame
