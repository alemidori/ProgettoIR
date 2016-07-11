''''
si occupa del processamento preliminare del testo,
ossia elimina la punteggiatura, rimuove le stopword e applica o stemming dei termini
'''''

from string import punctuation
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
import terms_dictionary


stemmed = []
terms_ref = dict()

def process(file):
    with open(file, "r") as text:
        for line in text.readlines():
            stemmed.append(process_string(line))
    return stemmed

def process_string(string):
    row = string.rstrip("\n")
    no_punctuation = remove_punctuation(row)  # rimozione punteggiatura
    filtered_list = remove_stopwords(no_punctuation.lower().split()) # rimozione stopword
    stemmed_string = stem(filtered_list)
    return stemmed_string

# rimuove la punteggiatura
def remove_punctuation(string):
    s = ''.join(c for c in string if c not in punctuation)
    # print(s)
    return s

# rimuove le stopwords
def remove_stopwords(list):
    filtered = [w for w in list if w not in stopwords.words('english')]
    return filtered

# stemmatizza i termini
def stem(list):
    stemmer = SnowballStemmer('english')
    stemmed_tokens = []

    for x in list:
        stemmed_tokens.append(stemmer.stem(x))
        terms_dictionary.update_terms_dictionary(stemmer.stem(x), x) #creo il dizionario di token e termini originali
    return stemmed_tokens

