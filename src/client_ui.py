import tkinter as tk
from enum import Enum

def button_click(text):
    def button_callback():
        print(f"{text} clicked!")
    return  button_callback

selected_card = None

class CardEnum(Enum):
    FIRST = 1
    SECOND = 2
    THIRD = 3

class CardButton():
    def card_click(self):
        self.selected = not self.selected

window = tk.Tk()
window.title("Simple Tkinter Window")

button = tk.Button(window, text="Pedra", command=button_click("pedra"))
button2 = tk.Button(window, text="Papel", command=button_click("papel"))
button3 = tk.Button(window, text="Tesoura", command=button_click("tesoura"))

button.pack()
button2.pack()
button3.pack()

window.mainloop()
