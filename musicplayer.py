import tkinter as tk
import os
import pygame.mixer
import sqlite3
import webbrowser
from functools import partial
from tinytag import TinyTag
from tkinter import ttk, filedialog
from tkinter.constants import END

pygame.mixer.init()
conn = sqlite3.connect("playlists.db")
c = conn.cursor()

class mainwindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__()
        ttk.Style().theme_use("clam")

        self.cwd = os.getcwd()
        self.lib_directory = ""
        self.paused = 0
        self.main_lib = ""
        self.playlists = []
        self.lib_backup = []
        
        # Configure Window Basic elements
        self.wm_title("Soundwave")
        self.geometry("1200x300")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.left_frame = tk.Frame(self, bd=2, height= 600)
        self.left_frame.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.right_frame = tk.Frame(self)
        self.right_frame.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.left_size = ttk.Sizegrip(self.left_frame)
        self.right_size = ttk.Sizegrip(self.right_frame)

        self.instructions = tk.Label(self.right_frame, text="Ctrl + Click to select separated songs or Shift + Click to select continuous list")
        self.instructions.grid(row=1, column=0)

        # Buttons
        self.selecbutton = tk.Button(self.left_frame, text="Select Music", width= 20)
        self.selecbutton.bind("<Button-1>", self.library_select)
        self.selecbutton.pack(expand=True)

        self.playbutton = tk.Button(self.left_frame, text="Play", width= 20)
        self.playbutton.bind("<Button-1>", self.play)
        self.playbutton.pack(expand=True)

        self.pausebutton = tk.Button(self.left_frame, text="Pause", width= 20)
        self.pausebutton.bind("<Button-1>", self.pause)
        self.pausebutton.pack(expand=True)  

        self.stopbutton = tk.Button(self.left_frame, text="Stop", width= 20)
        self.stopbutton.bind("<Button-1>", self.stop)
        self.stopbutton.pack(expand=True)

        self.lib_button = tk.Button(self.left_frame, text="Return to Main Library", width= 20)
        self.lib_button.bind("<Button-1>", self.lib_ref)
        self.lib_button.pack(expand=True)

        self.lookup_button = tk.Button(self.left_frame, text="Look Up Song/Artist", width= 20)
        self.lookup_button.bind("<Button-1>", self.win_lookup)
        self.lookup_button.pack(expand=True)

        # Playlist selector populated by database
        self.playlists = ["Create a Playlist"]

        temp = c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for table in temp.fetchall():
            x = table[0]
            self.playlists.append(x)

        self.options = tk.StringVar(self, )
        self.options.set(self.playlists[0])
        self.playlist_dropdown()

        # Tree View where songs and basicmetadata will be displayed
        columns = ["Length", "Title", "Artist", "Album", "Year", "Path"]
        self.library = ttk.Treeview(self.right_frame, columns = columns, show="headings", displaycolumns=("Length", "Title", "Artist", "Album", "Year"))
        self.library.grid(row=0, column = 0)
        self.library.heading("0", text = "Length")
        self.library.heading("1", text = "Title")
        self.library.heading("2", text = "Artist")
        self.library.heading("3", text = "Album")
        self.library.heading("4", text = "Year")

        for col in columns:
            self.library.heading(col, text=col, command= lambda _col=col: self.column_sort(self.library, _col, False))
        
        self.protocol("WM_DELETE_WINDOW", self.closing)
        return
    
    # This is where I am having the user select their music which should then get loaded into the tree view.
    def library_select(self, *args):
        self.main_lib = filedialog.askdirectory()
        self.lib_directory = self.main_lib
        os.chdir(self.main_lib)
        library = os.listdir(self.main_lib)

        # Getting song meta data and populating tree
        for songs in library:
            fpath = os.path.abspath(songs)
            audiofile = TinyTag.get(songs)
            length = audiofile.duration
            length = self.convert(length)
            title = audiofile.title
            artist = audiofile.artist
            album = audiofile.album
            year = audiofile.year
            self.library.insert('', index = END, values=(length, title, artist, album, year, fpath))
        
        for child in self.library.get_children():
            child_contents = (self.library.item(child)["values"])
            self.lib_backup.append(child_contents)
        os.chdir(self.cwd)
        return
        
    #Ability to refresh treeview with main library without re-selecting directory
    def lib_ref(self, event):
        if self.main_lib != "":
            self.library.delete(*self.library.get_children())
            os.chdir(self.main_lib)
            library = os.listdir(self.main_lib)

            for songs in library:
                fpath = os.path.abspath(songs)
                audiofile = TinyTag.get(songs)
                length = audiofile.duration
                length = self.convert(length)
                title = audiofile.title
                artist = audiofile.artist
                album = audiofile.album
                year = audiofile.year
                self.library.insert('', index = END, values=(length, title, artist, album, year, fpath))
            
            for child in self.library.get_children():
                child_contents = (self.library.item(child)["values"])
                self.lib_backup.append(child_contents)
        
            os.chdir(self.cwd)
        else:
            os.chdir(self.cwd)
            self.error(1)
        return
    
    # Play the music
    def play(self, event):
        play = self.select()
        if type(play) == list:
            pygame.mixer.music.load(play[0])
            pygame.mixer.music.play()
            return
        elif type(play) != list:
            pygame.mixer.music.load(play)
            pygame.mixer.music.play()
            return
    
    # Function to pause and unpause
    def pause(self, event):
        if self.paused == 0:
            pygame.mixer.music.pause()
            self.paused = 1
        elif self.paused == 1:
            pygame.mixer.music.unpause()
            self.paused = 0
        return

    # Function to stop the music
    def stop(self, event):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        return

    #create a drop down to refresh
    def playlist_dropdown(self):
        self.pl = tk.OptionMenu(self.left_frame, self.options, *self.playlists, command=self.playlist)
        self.pl.configure(state="normal", width=17)
        self.pl.pack(expand=True)
    
    def playlist(self, selection):
        if selection == "Create a Playlist":
            # Create a pop up window to get name of created playlist
            self.pl_create = tk.Toplevel()
            self.pl_create.geometry("400x200")
            self.pl_create.wm_title("Playlist Create")

            self.pl_label = tk.Label(self.pl_create, text="Enter the name of the playlist and hit submit")
            self.pl_label.pack(expand=True)

            self.pl_input = tk.Text(self.pl_create, height=1, width=20)
            self.pl_input.pack(expand=True)

            self.pl_submit = ttk.Button(self.pl_create, text = "Submit", command=self.playlist_helper)
            self.pl_submit.pack(expand=True)
            return
        
        elif selection in self.playlists:
            pl_list = c.execute(f"SELECT length, title, artist, album, year, loc FROM {selection}")
            self.library.delete(*self.library.get_children())
            for song in pl_list:
                self.library.insert('', index = END, values=(song))
            return
        else:
            self.error(2)

    def playlist_helper(self):
        # Creating the playlist
        self.playlist_title_input = self.pl_input.get("1.0", "end-1c")
        self.pl_create.destroy()

        for letter in self.playlist_title_input:
            if letter.isalnum() == False:
                self.error(3)

        if self.playlist_title_input in self.playlists:
            self.error(4)
            return
        
        if self.playlist_title_input == "":
            self.error(5)
            return

        if self.playlist_title_input not in self.playlists:

            self.playlists.append(self.playlist_title_input)
            c.execute(f"CREATE TABLE IF NOT EXISTS {self.playlist_title_input} (id INTEGER, length TEXT NOT NULL, title TEXT, artist TEXT, album TEXT, year INT, loc TEXT, PRIMARY KEY(id))")

            #Adding Selected Songs and metadata to Playlist
            additions = self.select()
            self.library.delete(*self.library.get_children())

            for songs in additions:
                audiofile = TinyTag.get(songs)
                length = audiofile.duration
                length = self.convert(length)
                title = audiofile.title
                artist = audiofile.artist
                album = audiofile.album
                year = audiofile.year

                c.execute(f"INSERT INTO {self.playlist_title_input} (length, title, artist, album, year, loc) VALUES(?, ?, ?, ?, ?, ?)", (length, title, artist, album, year, songs))

                # Updating the Treeview to show new playlist
                self.library.insert('', index = END, values=(length, title, artist, album, year, songs))

            conn.commit()

            #refresh UI with new info from playlist
            self.pl.destroy()
            self.playlist_dropdown()
            return
        
        else:
            self.error(6)
            return

    # Converting runtime of song from seconds to minute:seconds format
    def convert(self, length):
        min, sec = divmod(length, 60)
        return "%02d:%02d" % (min, sec)

     # Function to return the path of files to other functions
    def select(self):
        cursor = 0
        choice = []
        #Getting path of file from the treeview
        multi_select = self.library.selection()
        current_items = [self.library.item(i)['values'] for i in multi_select]
        if len(current_items) > 1:
            for j in current_items:
                tmp = current_items[cursor][5]
                tmp = os.path.abspath(tmp)
                choice.append(tmp)
                cursor += 1
            return choice
        else:
            return current_items[0][5]

    # Column Sorting under the tree view
    def column_sort(self, library, col, reverse):
        l = [(self.library.set(k, col), k) for k in self.library.get_children('')]
        l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            self.library.move(k, '', index)

        self.library.heading(col, command = lambda _col=col: self.column_sort(self.library, _col, not reverse))
    
    # Error Message
    def error(self, code):
        self.error_box = tk.Toplevel()
        self.error_box.geometry("300x200")
        self.error_box.wm_title("Error")
        self.error_notice1 = tk.Label(self.error_box, text="There was an error")
        self.error_notice1.pack(expand=True)

        if code == 1:
            message = "Can't Refresh Library Without Selecting Directory"
        elif code == 2:
            message = "Playlist Not Found"
        elif code == 3:
            message = "Can Only Use Letters and Numbers"
        elif code == 4: 
            message = "Playlist Name Already In Use"
        elif code == 5:
            message = "Playlist Name Can't Be Empty"
        elif code == 6:
            message = "Error Creating Playlist"

        self.error_notice2 = tk.Label(self.error_box, text=f"{message}")
        self.error_notice2.pack(expand=True)
        self.error_submit = ttk.Button(self.error_box, text = "Ok", command=lambda: self.error_box.destroy())
        self.error_submit.pack(expand=True)
        return

    def closing(self):
        conn.close()
        pygame.mixer.music.unload()
        self.destroy()  
        return

    #Run the class to create a window for looking up a song not in library
    def win_lookup(self, event):
        window = lookupwindow(self)
        window.grab_set()
        return

class lookupwindow(tk.Toplevel):
    def __init__(self, mainwindow):
        super().__init__(mainwindow)
        self.wm_title("Choose a Service")
        self.geometry("200x400")
        ttk.Style().theme_use("clam")


        self.label = tk.Label(self, text="Name of Song and/or Artist")
        self.label.pack(expand=True)

        #Text box for the person to enter the song name and artist
        self.input_box=tk.Text(self, height=1, width=20)
        self.input_box.pack(expand=True)
        
        self.label2 = tk.Label(self, text="Choose a Service to Search")
        self.label2.pack(expand=True)

        #Buttons for different lookup services
        self.spotify = ttk.Button(self, text="Spotify", command=partial(self.lookup, "spotify"))
        self.spotify.pack(expand=True)

        self.youtube = ttk.Button(self, text="YouTube", command=partial(self.lookup, "youtube"))
        self.youtube.pack(expand=True)

        self.google = ttk.Button(self, text="Google", command=partial(self.lookup, "google"))
        self.google.pack(expand=True)

        self.quitbutton = ttk.Button(self, text="Cancel", command=self.destroy)
        self.quitbutton.pack(expand=True)

    def lookup(self, service):
        request = self.input_box.get('1.0', 'end')

        self.destroy()
        if service == "spotify":
            for letter in request:
                if letter == " ":
                    letter = "%20"
            webbrowser.open(f"https://open.spotify.com/search/{request}")

        elif service == "youtube":
            webbrowser.open(f"https://www.youtube.com/results?search_query={request}")

        elif service == "google":
            webbrowser.open(f"https://www.google.com/search?q={request}")

        

        return



if __name__ == "__main__": 
    test = mainwindow()
    test.mainloop()