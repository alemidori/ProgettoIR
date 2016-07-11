''''
si occupa della suddivisione dei racconti in paragrafi, utilizzati in seguito
come documenti del corpus. Si serve di processing.py per applicare il processamento
di base del testo e di storage.py per memorizzare i paragrafi in file json
'''''

import storage
import glob
import processing

path = "../sample_texts/*.txt"
files = glob.glob(path) #lista di file txt da spezzare in paragrafi

def process_stories():
    for file in files:
        with open (file, "r") as inputfile:
            print("Apro nuovo file ["+str(files.index(file)+1)+"]...")
            string = inputfile.read()
            parags = string.split(sep='\n') #divide in paragrafi mediante il separatore di 'a capo'
            print("Creazione collezione paragrafi...")
            for p in parags:
                if p and (not p.isspace()): #se il paragrafo ha almeno un carattere
                    #print(p)
                    stemmed_list = processing.process_string(p)  # applico il processo base a ogni paragrafo
                    storage.insert_paragraph(file, p, parags.index(p), stemmed_list)  # memorizzo tutto con mongodb

    return




