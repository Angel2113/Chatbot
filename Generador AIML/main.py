#!/usr/bin/python2
# -*- encoding: utf-8 -*-

__author__  = 'Angel Callejas'
__credits__ = 'Angel Callejas'
__email__   = 'acallejas21@gmail.com'
__license__ = 'GLP'
__version__ = '2.0'

from Tkinter import *
from generator import GeneratorAIML
import tkFileDialog
import threading

class Main:
    def __init__(self):
        # window config
        self.window = Tk()
        self.window.title('Generador AIML')
        self.window.geometry('500x250')

        # Variable
        self.filename = ''
        self.LabelEntrada = Label(self.window, text='Nombre del archivo', width=30, borderwidth=1, bg='white')
        self.palabraMas   = False
        self.palabraMenos = False
        self.bigramaMas   = False
        self.bigramaMenos = False

        self.Interface()
        self.window.mainloop()

    def Interface(self):
        # In
        Label(self.window, text='Archivo: ').grid(row=0, column=0, rowspan=2)
        self.LabelEntrada.grid(row=0, column=1, columnspan=2, rowspan=2)
        Button(self.window, text='Abrir', command=self.open_file).grid(row=0, column=3, rowspan=2)

        # Options
        Label(self.window, text='Opciones').grid(row=3, column=0)
        self.listbox = Listbox(self.window, selectmode=MULTIPLE, width=60)
        self.listbox.insert(1, '1. Palabra mas frecuente')
        self.listbox.insert(2, '2. Palabra menos frecuente')
        self.listbox.insert(3, '3. Bigrama mas frecuente')
        self.listbox.insert(4, '4. Bigrama menos frecuente')
        self.listbox.grid(row=8, column=0, columnspan=5)
        Button(self.window, text="Generar", command=self.GenerateFiles).grid(row=9, column=0)

    def GenerateFiles(self):
        # Get selection
        self.listSelect = []
        select = self.listbox.curselection()
        for i in select:
            self.listSelect.append(self.listbox.get(i))

        # Generate Files
        gen = GeneratorAIML(self.filename)

        if len(self.listSelect) < 4:
            for i in self.listSelect:
                n = i.split('.')[0]
                select = i.split('.')[1]
                #tareas = Pool.map(gen.gen_aiml, int(n))
                t = threading.Thread(target=gen.gen_aiml, args=(int(n),))
                #hilos.append(t)
                t.start()
                #gen.gen_aiml(int(n))
        else:
            gen.gen_aiml(0)

    def open_file(self):
        dialog = tkFileDialog.Open(self.window)
        filename = dialog.show()
        if filename != '':
            self.filename = filename
            filename = self.filename.split('/')[-1]
            self.LabelEntrada.config(text=filename)

app = Main()

