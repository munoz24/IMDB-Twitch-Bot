import tkinter as tk
from tkinter import *
from tkinter import messagebox
import threading
import bot


def main():
    def startbot(button):
        messagebox.showinfo(title="Information", message="Close main window to terminate bot")
        botThread = threading.Thread(target=bot.bot)
        botThread.daemon = True
        botThread.start()
        button.config(text="Bot is Running")
        button.config(state=DISABLED)

    root = tk.Tk()
    root.title("IMdb Bot")
    root.resizable(False, False)

    canvas = tk.Canvas(root, height=230, width=400, bg="#263D42")
    canvas.pack(fill=BOTH, expand=YES)

    frame = tk.Frame(root, bg="grey")
    frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    runBot = tk.Button(frame, text="Run Bot", padx=40, pady=20, fg="white", bg="black",
                       command=lambda: startbot(button=runBot))
    runBot.pack()

    info1 = tk.Label(frame, text="Created by Andres Munoz Ornelas in Wisconsin, US")
    info1.pack()
    info2 = tk.Label(frame, text="Template of source code can be found here")
    info2.pack()
    info3 = tk.Label(frame, text="https://github.com/munoz24/Twitch-Bot")
    info3.pack()
    info4 = tk.Label(frame, text="Developer Contact Information for bugs or new features")
    info4.pack()
    info5 = tk.Label(frame, text="Preferred -> Reddit: https://www.reddit.com/user/CitrusGore")
    info5.pack()
    info6 = tk.Label(frame, text="Secondary -> E-mail: andres@munozo.com")
    info6.pack()

    root.mainloop()


if __name__ == '__main__':
    main()
