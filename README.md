#MP3 Player Soundwave
###Video Demo: https://youtu.be/WZXNlhJLIV0
###Description:

I developed a mp3 player with a GUI using python and the Tkinter GUI library. The goal I had was to create somethign a little more complicated than just a play/stop button, so I wanted to included some more involved features. To that end I wanted to able to load up a music directory, browse the directory, choose any song out of the directory, and be able to play/pause/stop it. I also wanted to include an option for a user to generate playlists to be able to easily save songs and return to them at another time. I also wanted to include an option for the user to find and search for songs they may not have using some popular music providers.

The initial window includes the control menu on the left, where a user can select their music library, control the audio, look up an unknown song, select/create a new playlist, and return the window on the right to the main library. This window on the right displays information about the song, including length, title, artist, album, and year released. Users can highlight a desired song by clicking on the song's row in the window. They can then play this song by using the Play button. Audio can be paused by hitting pause (for later resuming), or stopped more permanently by hitting Stop. Users can select multiple songs by holding Ctrl or Shift while clicking. Users can then hit the dropdown menu and select Create A Playlist to have the selected songs put into a playlist (Sqlite3 database). The window will then refresh to include only songs in the playlist. If users want to return to their main library they can select Return to Main Library, which will populate the window with their main library again.

If users can think of a song they do not have, or an artist they are interested in, they can select Look Up Song/Artist. This will open a new window where users can type in the song/artist and choose a service to search under, with options being Spotify, YouTube, and Google. Selecting one of these will open a webbrowswer which contains the results of a search for that term on that site. This way users can quickly find new content on common sources of music.

Finally, there are several error conditions that will prevent users from taking actions which could cause the program to fail or encounter unforseen issues. These include errors 1) Returning to main library without previously selecting one 2)Entering a playlist with invalid characters 3)leaving the playlist field blank 4)Entering a playlist name that is already in use. There are also two other possible error messages for unforseen issues including not being able to locate the playlist (in teh event the playlist database file is moved or deleted), or if there is some error in creating a playlist initially.

Tentative Roadmap:
There are a few things I may continue to improve as time goes on and if feasible. 
First I would like the player to continue autoplaying through the library. As it is now, once a song is over the music stops until the user selects a new song and presses play again. 
Second, improving the GUI would be nice. I chose Tkinter since it seemed a good entry-level tool, but there is no denying the GUI appears pretty basic as it is. I did not necessarily see ways to significantly improve it within the Tkinter library, so this might be a more involved process of either indepth research or changing how the UI is created. At the very least, I would also like to include the ability to view album artwork as part of the GUI.
Third, the initial loading of a large music library can take some time. Loading a library of a few hundred songs can lead to a few seconds where it seems like the program is not responding. Ideally, I would find someway to make this more efficient. I may also include some visual indicator such as a progress bar to inform users the system is behaving as exepcted and some patience is required.
