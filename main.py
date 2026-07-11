import tkinter as tk
from menu import FanoronaGameMenu

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    window.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

def main():
    root = tk.Tk()
    root.title("Fanorona Game")
    root.resizable(False, False)
    
    # Center and size the window
    center_window(root, 800, 600)
    
    FanoronaGameMenu(root)
    root.mainloop()

main()
