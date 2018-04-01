# Python 3.6.3
import string
from tkinter import *


glyphs = string.digits + string.ascii_uppercase + string.ascii_lowercase + '+/'  # 64
BASEERROR = f'Base must range between 2 and {len(glyphs)}'
NUMBERERROR = f'Invalid number for the given base'


def tobase(num: int, base: int) -> str:
    """Converts a base-10 number into a string of the given base"""
    digits = ""
    while num:
        digits += glyphs[num % base]
        num //= base
    return digits[::-1]


def frombase(num: str, base: int) -> int:
    """Converts a string from a given base into a base-10 number"""
    return sum(glyphs.find(num[-1-n]) * base**n for n in range(len(num)))


def convertbase(num: str, base1: int, base2: int) -> str:
    """Converts a string representing a number between two provided bases"""
    if base1 < glyphs.index('a'):
        num = num.upper()

    assert 2 <= base1 <= len(glyphs) and 2 <= base2 <= len(glyphs), BASEERROR
    assert all(x in glyphs and glyphs.find(x) < base1 for x in num), NUMBERERROR

    if base1 == 10 and base2 == 10:
        return num
    elif base1 == 10:
        return tobase(int(num), base2)
    elif base2 == 10:
        return str(frombase(num, base1))
    else:
        return tobase(frombase(num, base1), base2)


class App(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(expand=True, fill=BOTH)
        self.create_widgets()
        self.create_bindings()
        self.place_widgets()

    def create_widgets(self):
        self.framemaster = Frame(self)
        self.result = Message(self, width=220)
        self.copybutton = Button(self, text='Copy', command=self.copy_to_clipboard)

        self.framenumber = Frame(self.framemaster, pady=10)
        self.number = Entry(self.framenumber, text='', width=25)
        self.numbermsg = Message(self.framenumber, text='Number to convert:', width=250)

        self.framebases = Frame(self.framemaster)
        self.sbase = Entry(self.framebases, width=3)
        self.rbase = Entry(self.framebases, width=3)
        self.sbasemsg = Message(self.framebases, text='Starting Base:', width=200)
        self.rbasemsg = Message(self.framebases, text='Desired Base:', width=200)
        self.swapbutton = Button(self.framebases, text='Swap', bg='lightgray', command=self.swap_bases)

        self.sbase.insert(END, '10')
        self.rbase.insert(END, '10')

    def place_widgets(self):
        self.framemaster.pack()
        self.result.place(anchor=E, relx=0.83, rely=0.75)
        self.copybutton.place(anchor=CENTER, relx=0.9, rely=0.75)

        self.framenumber.grid(row=0)
        self.numbermsg.grid(column=0, row=0)
        self.number.grid(column=1, row=0)

        self.framebases.grid(row=1)
        self.sbasemsg.grid(column=0, row=0)
        self.sbase.grid(column=1, row=0)
        self.swapbutton.grid(column=2, row=0, padx=(15, 5))
        self.rbasemsg.grid(column=3, row=0)
        self.rbase.grid(column=4, row=0)

    def create_bindings(self):
        bind_post(self.number, '<Key>', self.on_key_press)
        bind_post(self.sbase, '<Key>', self.on_key_press)
        bind_post(self.rbase, '<Key>', self.on_key_press)

    def on_key_press(self, event=None):
        num, base1, base2 = self.number.get(), self.sbase.get(), self.rbase.get()
        text, color = '', 'black'

        if num and base1 and base2:  # Not empty
            try:
                text = convertbase(num, int(base1), int(base2))
            except (AssertionError, ValueError) as error:
                text = error if isinstance(error, AssertionError) else BASEERROR
                color = 'red'

        self.result.config(fg=color, text=text)

    def swap_bases(self):
        base1, base2 = self.sbase.get(), self.rbase.get()
        self.sbase.delete(0, END)
        self.rbase.delete(0, END)
        self.sbase.insert(END, base2)
        self.rbase.insert(END, base1)
        self.on_key_press()

    def copy_to_clipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.result['text'])


def bind_post(widget, sequence, func, add=''):
    """Adds a widget event bind that triggers AFTER initial event"""
    bindtags = list(widget.bindtags())
    bindtags.insert(2, 'custom')
    widget.bindtags(tuple(bindtags))
    widget.bind_class('custom', sequence, func, add)


def main():
    root = Tk()
    root.geometry('300x150')
    root.title('Base Converter')

    app = App(root)
    app.mainloop()


if __name__ == '__main__':
    main()
