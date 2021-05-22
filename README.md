# Tetris-Bot-Autoplayer
Please use a recent version of Python 3. You can download a bundle with all you need from https://www. python.org/.
Once you are in the code directory, you should be able to start the interface by running
python visual.py
To get a feeling for the game, you can also run any of the interfaces in manual mode by adding the flag -m:
python visual.py -m
If that interface does not work, there are two alternative interfaces available:
• A command-line interface; run python cmdline.py to use it. If you are using Windows, you may need to
install the windows-curses package first; try running pip --user install windows-curses.
• A Pygame-based interface; run python visual-pygame.py to use it. For this, you need to have a working
copy of Pygame; run pip --user install pygame to install it.
If you get an interface running, you should see the default player in action.
