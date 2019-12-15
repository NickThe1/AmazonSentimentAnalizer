import matplotlib

matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from sentimentanalysis import Analizer
import numpy as np

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb

import traceback

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.report_callback_exception = self.show_error
        title1 = self.title("prototype of analitic platform")
        self.label0 = tk.Label(self, text="Amazon product Analizer")
        self.label0.pack()
        self.label1 = tk.Label(self, text="Enter Amazon URL:")
        self.label1.pack()
        self.ent1 = tk.Entry(self)
        self.ent1.bind('<Any-KeyRelease>', self.foo)
        self.ent1.pack()

        self.btn = ttk.Button(self, text="Analize",state='disabled', command=self.show)
        self.label2 = tk.Label(self, text= "Processing..." )
        self.btn.pack()

    def foo(self, event):
        data1 = self.ent1.get()
        if len(data1) != 0 :
            self.btn.config(state='enabled')

    def hide_me(self, event):
        event.widget.pack_forget()

    def show_error(self, *args):
        err = traceback.format_exception(*args)
        print(args)
        mb.showerror('Exception',args[1])

    def show(self):
        try:
            self.btn.config(state='disabled')
            url = self.ent1.get()
        except Exception as e:
            self.btn.config(state='enabled')
            mb.showerror("Error", e)
        anl = Analizer(url)
        anl.make_data()
        anl.polarity()
        fig = anl.get_figure(0.7)

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack()
        canvas._tkcanvas.pack()


window = Application()
window.geometry('900x800')
window.mainloop()
