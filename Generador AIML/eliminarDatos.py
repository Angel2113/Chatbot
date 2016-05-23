#! /usr/bin/python
# -*- eocoding: utf-8 -*-

import re

preguntas  = list()
respuestas = list()

doc = open('Corpus-ejemplo').read()
doc = doc.lower()


## Eliminar acentos y ñ
diccionario = {'á':'a', 'é':'e', 'í':'i', 'ó':'o', 'ú':'u', 'ñ':'n'}

## Eliminar nombres
n = open('nombres-propios-es.txt').read()
for i in n.lower().split('\n'):
    if len(i) > 0:
        if i not in diccionario:
            diccionario[i] = ''

## Eliminar apellidos 
ln = open('apellidos-es.txt').read()
for i in ln.lower().split('\n'):
    if len(i) > 0:
        if i not in diccionario:
            diccionario[i] = ''

print 'Antes: ', len(doc)

regex = re.compile("(%s)" % "|".join(map(re.escape, diccionario.keys())))
doc = regex.sub(lambda x:str(diccionario[x.string[x.start():x.end()]]), doc)


# Elimina enlaces; todos inician con 'http' o 'https' 
doc = re.sub(r'.?https*\:.*', '', doc)
doc = re.sub(r'.?www\.*', '', doc)



## Eliminar telefonos
doc = re.sub(r'([0-9]{10,13})','',doc)
doc = re.sub(r'([0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2})','',doc)

## Eliminar emails
doc = re.sub(r'(\w+@(\w+\.\w+)+)', '', doc)

print 'Despues: ', len(doc)
print "Escribiendo salida"
salida = open('salida','w')
salida.write(doc)


