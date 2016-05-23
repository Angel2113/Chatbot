#!/usr/bin/python2
# -*- encoding: utf-8 -*-

__author__  = 'Angel Callejas'
__credits__ = ['Angel Callejas', 'Esau Villatoro', 'Ivan Meza']
__email__   = 'acallejas21@gmail.com'
__license__ = 'GLP'
__version__ = '2.0'

import codecs, re, nltk
from nltk import ngrams

class GeneratorAIML:
    def __init__(self, filename):
        document = open(filename).read()
        self.questions   = list()
        self.answer      = list()
        self.frecuency   = list()
        self.frecuencyBi = list()
        self.bigrams     = list()
        self.names = {}

        self.token = nltk.word_tokenize(document)

        self.frecuency   = nltk.FreqDist(self.token)
        self.bigrams     = ngrams(self.token, 2)
        self.frecuencyBi = nltk.FreqDist(self.bigrams)

        n = open('nombres-propios-es.txt').readlines()
        ln = open('apellidos-es.txt').readlines()

        for name in n:
            self.names[name.upper()] = ''
        for last in ln:
            self.names[last.upper()] = ''

        # Get questions and anwswers
        for i in document.split('<question>'):
            try:
                aux = i.split('<answer>')
                if len(aux[0]) > 0 and len(aux[1]) > 0:
                    self.questions.append(aux[0])
                    self.answer.append(aux[1])
            except:
                pass

    def gen_aiml(self, n):
        # Use
        # 1 palabra mas
        # 2 palabra menos
        # 3 bigrama mas
        # 4 bigrama menos
        if n == 0:
            file1 = 'palabraMas.aiml'
            file2 = 'palabraMenos.aiml'
            file3 = 'bigramaMas.aiml'
            file4 = 'bigramaMenos.aiml'
        if n == 1:
            filename = 'palabraMas.aiml'
            #if not self.frecuency: self.frecuency = nltk.FreqDist(self.token)
        if n == 2:
            filename = 'palabraMenos.aiml'
            #if not self.frecuency: self.frecuency = nltk.FreqDist(self.token)
        if n == 3:
            filename = 'bigramaMas.aiml'
            #if not self.bigrams:
            #    self.bigrams     = ngrams(self.token, 2)
            #    self.frecuencyBi = nltk.FreqDist(self.bigrams)
        if n == 4:
            filename = 'bigramaMenos.aiml'
            #if not self.bigrams:
            #    self.bigrams = ngrams(self.token, 2)
            #    self.frecuencyBi = nltk.FreqDist(self.bigrams)

        if n == 0: 
            print 'iniciados los 4'
        else:
            print 'iniciado', filename
 
        diccionario = {}
        dict1 = {}
        dict2 = {}
        dict3 = {}
        dict4 = {}
        contador = 1
        for i in range(len(self.questions)):
            ## Seccion de pregunta
            if n == 0:
                p1 = self.search_pmas(self.questions[i]).upper()
                p2 = self.search_pmenos(self.questions[i]).upper()
                p3 = self.search_bmas(self.questions[i]).upper()
                p4 = self.search_bmenos(self.questions[i]).upper()        
            if n == 1:
                p = self.search_pmas(self.questions[i]).upper()
            if n == 2:
                p = self.search_pmenos(self.questions[i]).upper()
            if n == 3:
                p = self.search_bmas(self.questions[i]).upper()
            if n == 4:
                p = self.search_bmenos(self.questions[i]).upper()
            r = self.answer[i]

            ## respuesta y limpieza
            if n != 0:
                p, r = self.clean(p, r)
                if p not in diccionario:
                    if (len(p)>3):
                        diccionario[p] = []
                try:
                    if r not in dict[p]:
                        if len(r) > 2:
                            diccionario[p].append(r.lower())
                except:
                    #print('No procesada: ', r, ' de ', p)
                    pass
            else:
                p1, p2 = self.clean(p1, p2)
                p3, p4 = self.clean(p3, p4)
                r, r1  = self.clean(r, r)

                if p1 not in dict1:
                    if(len(p1)>3):
                        dict1[p1] = []
                try:
                    if r not in dict1[p1]:
                        if len(r) > 2:
                            dict1[p1].append(r.lower())
                except:
                    pass

                if p2 not in dict2:
                    if(len(p2)>3):
                        dict2[p2] = []
                try:
                    if r not in dict2[p2]:
                        if len(r) > 2:
                            dict2[p2].append(r.lower())
                except:
                    pass

                if p3 not in dict3:
                    if(len(p3)>3):
                        dict3[p3] = []
                try:
                    if r not in dict3[p3]:
                        if len(r) > 2:
                            dict3[p3].append(r.lower())
                except:
                    pass

                if p4 not in dict4:
                    if(len(p4)>3):
                        dict4[p4] = []
                try:
                    if r not in dict4[p4]:
                        if len(r) > 2:
                            dict4[p4].append(r.lower())
                except:
                    pass
            print contador, ' de ', len(self.questions)
            contador += 1
        print len(dict1), ' ',  len(dict2),' ',len(dict3),' ', len(dict4)
        if n == 0:
            self.toFile(file1, dict1)
            self.toFile(file2, dict2)
            self.toFile(file3, dict3)
            self.toFile(file4, dict4)
        else:
            self.toFile(filename, diccionario)
        print 'Termino'

    def clean(self, question, answer):
        question = question.upper()
        answer   = answer.upper()
        # search others
        replace = {'<' : '', '&':'', '*':'', '\\':'', '/': '|',
                   'á':'a', 'é':'e', 'í':'i','ó':'o', 'ú':'u',
                   'Á':'a', 'É':'e','Í':'i', 'Ó':'o', 'Ú':'u',
                   '      ':' ','\n':'', '\xc2\xa1':'', '\xc2\xbf':'',
                   '\xc3\x81':'a', '\xc3\x89':'e', '\xc3\x8d':'i', '\xc3\x93':'o', '\xc3\x9a':'u',
                   '\xc3\x9c':'u', '\xc3\xa1':'a', '\xc3\xa9':'e', '\xc3\xad':'i', '\xc3\xb3':'o', '\xc3\xba':'u',
                   '\xc3\xbc':'u', '\xc3\xb1':'n', '\xc3\x91':'n'}
        regex = re.compile("(%s)" % "|".join(map(re.escape, replace.keys())))
        regex2 = re.compile("(%s)" % "|".join(map(re.escape, self.names.keys())))

        question = regex.sub(lambda x:str(replace[x.string[x.start():x.end()]]), question)
        question = regex2.sub(lambda x:str(self.names[x.string[x.start():x.end()]]), question)
        question = re.sub('\*', '', question)
        question = re.sub('\s{2,}', ' ', question)

        answer   = regex.sub(lambda x:str(replace[x.string[x.start():x.end()]]), answer)
        answer   = regex2.sub(lambda x:str(self.names[x.string[x.start():x.end()]]), answer)
        answer   = re.sub('\*', '', answer)
        answer   = re.sub('\s{2,}', ' ', answer)

        if len(question) > 1 and len(answer) > 1:
            question = question.upper()
            answer   = answer.upper()
            return question, answer
        else:
            return '',''

    def search_pmas(self, line):
        div = nltk.word_tokenize(line)
        if len(div) > 1:
            bmax = self.frecuency[div[0]]
            word = div[0]
            for i in div:
                if self.frecuency[i] > bmax:
                    bmax = self.frecuency[i]
                    word = i
            return word
        else:
            return line
    
    def search_pmenos(self, line):
        div = nltk.word_tokenize(line)
        if len(div) > 1:
            bmin = self.frecuency[div[0]]
            word = div[0]
            for i in div:
                if self.frecuency[i] < bmin:
                    bmin = self.frecuency[i]
                    word = i
            return word
        else:
            return line
        
    def search_bmas(self, line):
        div = nltk.word_tokenize(line)
        cbi = ngrams(div, 2)
        maximo = 0
        word = line
        if len(div) > 1:
            for i in cbi:
                if i in self.frecuencyBi:
                    if maximo == 0 or self.frecuencyBi[i] > maximo:
                        maximo = self.frecuencyBi[i]
                        word   = i
            return ' '.join(word)
        else:
            return line
    
    def search_bmenos(self, line):
        div = nltk.word_tokenize(line)
        cbi = nltk.ngrams(div, 2)
        minim = 0
        word   = line
        if len(div) > 1:
            for i in cbi:
                if i in self.frecuencyBi:
                    if (minim == 0) or (self.frecuencyBi[i] < minim):
                        minim = self.frecuencyBi[i]
                        word   = i
            return ' '.join(word)
        else:
            return line

    def toFile(self, name, diccionario):
        arch = codecs.open(name, encoding='utf-8', mode='w+')
        arch.write("<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n")
        arch.write("<aiml version=\"1.0\">\n\n")

        for preg, resp in diccionario.iteritems():
            if len(resp) > 0:
                # Se escribe en archivo
                arch.write('<category>\n')
                arch.write('<pattern>')
                arch.write('* ' + preg)
                arch.write('</pattern>\n')
                arch.write("<template>\n")
                if len(resp) > 1:
                    arch.write("<random>\n")
                    for j in resp:
                        arch.write('<li>' + j + '</li>\n')
                    arch.write("</random>\n")
                else:
                    arch.write(resp[0])
                arch.write("</template>\n")
                arch.write("</category>\n\n")

                arch.write('<category>\n')
                arch.write('<pattern>')
                arch.write('* ' + preg + ' *')
                arch.write('</pattern>\n')
                arch.write("<template>\n")
                if len(resp) > 1:
                    arch.write("<random>\n")
                    for j in resp:
                        arch.write('<li>' + j + '</li>\n')
                    arch.write("</random>\n")
                else:
                    arch.write(resp[0])
                arch.write("</template>\n")
                arch.write("</category>\n\n")

                arch.write('<category>\n')
                arch.write('<pattern>')
                arch.write(preg + ' *')
                arch.write('</pattern>\n')
                arch.write("<template>\n")
                if len(resp) > 1:
                    arch.write("<random>\n")
                    for j in resp:
                        arch.write('<li>' + j + '</li>\n')
                    arch.write("</random>\n")
                else:
                    arch.write(resp[0])
                arch.write("</template>\n")
                arch.write("</category>\n\n")

                arch.write('<category>\n')
                arch.write('<pattern>')
                arch.write(preg)
                arch.write('</pattern>\n')
                arch.write("<template>\n")
                if len(resp) > 1:
                    arch.write("<random>\n")
                    for j in resp:
                        arch.write('<li>' + j + '</li>\n')
                    arch.write("</random>\n")
                else:
                    arch.write(resp[0])
                arch.write("</template>\n")
                arch.write("</category>\n")
        arch.write('</aiml>')
