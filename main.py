from gui import WordleSolverGUI
import tkinter as tk

def main():
    root = tk.Tk()
    app = WordleSolverGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()