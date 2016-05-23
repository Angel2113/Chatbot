#!/usr/bin/python2
# -*- encoding: utf-8 -*-

__author__  = 'Angel Callejas'
__credits__ = 'Angel Callejas'
__email__   = 'acallejas21@gmail.com'
__license__ = 'GLP'
__version__ = '2.0'

from Tkinter import *
import aiml
import ScrolledText

class Window:
    def __init__(self):
        self.chat = aiml.Kernel()
        self.chat.loadBrain('cerebro')
        self.window = Tk()
        self.entrada = StringVar()
        self.window.title('Chatbot')
        self.window.geometry('400x400')
        self.historial = ScrolledText.ScrolledText(self.window, width=54, height=25)
        self.interface()
        self.window.mainloop()

    def interface(self):
        self.historial.grid(row=0, column=0, columnspan=3)
        Label(self.window, text='Decir: ').grid(row=1, column=0)
        Entry(self.window, width=30, textvariable=self.entrada).grid(row=1, column=1)
        Button(self.window, text='Enviar', command=self.respond).grid(row=1, column=2)

    def respond(self):
        user   = self.entrada.get()
        answer = self.chat.respond(user)
        print user
        print answer
        self.historial.insert('insert','Usuario: '+ user +'\n')
        self.historial.insert('insert','Chatbot: '+ answer +'\n')

app = Window()