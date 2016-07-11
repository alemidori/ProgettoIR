'''si occupa del salvataggio dei testi in un file json accessibile mediante mongodb e dell'accesso
a questi utlimi'''

import pymongo
from itertools import chain
from collections import Counter

client = pymongo.MongoClient()

# paragraphs_coll = db['paragraphs'] #collezione paragrafi con relativi tokens, racconto di riferimento e posizione nel racconto
# terms_ref_coll = db['terms_ref'] #collezione dei token con i rispettivi termini originali dai quali provengono
# topics_terms = db['topics_terms'] #collezione primi 50 termini restituiti dal modello lda per ogni topic
# term_frequency_corpus = db['term_frequency_corpus'] #collezione termini di tutto il corpus e relative occorrenze
# story_support = db['story_support'] #collezione di supporto per creare indici su determinati attributi (token,descr)
# #su ciascun paragrafo

#*******************************************************************************************************************
#*******************************************************************************************************************
#*******************************************************************************************************************
# parte di valutazione con nuovo db e nuovi metodi che lavorano su di esso
dbsample = client['sample'] #database creato per la valutazione del sistema

paragraphs_coll = dbsample['paragraphs'] #collezione paragrafi con relativi tokens, racconto di riferimento e posizione nel racconto
terms_ref_coll = dbsample['terms_ref'] #collezione dei token con i rispettivi termini originali dai quali provengono
topics_terms = dbsample['topics_terms'] #collezione primi 50 termini restituiti dal modello lda per ogni topic
term_frequency_corpus = dbsample['term_frequency_corpus'] #collezione termini di tutto il corpus e relative occorrenze
story_support = dbsample['story_support'] #collezione di supporto per creare indici su determinati attributi (token,descr)
#su ciascun paragrafo

#prende 3 parametri: l'id del racconto originale nel quale il paragrafo si trova
#il testo del paragrafo e la posizione all'interno del racconto

def insert_paragraph(story_id, text, position, list_of_tokens):
    paragraphs_coll.insert_one({'id_story': story_id, 'descr': text, 'pos': position, 'tokens': list_of_tokens})
    return

def insert_terms_ref(dict):
    for k,v in dict.items():
        json_toExport = {'token' : k, 'originals' : v}
        terms_ref_coll.insert_one(json_toExport)
    return

#prende per ogni paragrafo nella collezione la lista dei token associati
def get_stemmed_terms_paragraph():

    token_list_paragraph = []
    cursor = paragraphs_coll.find(None, {"tokens": 1, '_id': 0})  # metto None perche' sto facendo una selezione su niente quindi voglio che mi restituisca tutto
    for element in cursor:
        token_list_paragraph.append(element['tokens'])  #e' una lista di liste in cui ogni lista interna ha i token
        # riferiti ad ogni singolo paragrafo
    return token_list_paragraph

def get_paragr_descr_from_id(idstory, pos):
    cursor = paragraphs_coll.find({'id_story': idstory,'pos':pos}, {'_id': 0, 'descr': 1})
    a = ""
    for element in cursor:
        a = element['descr']
    return a


def insert_topics_3_most_significant_words(id_topic,arraywords):
    topics_terms.insert_one({'id_topic': id_topic,'words_list': arraywords})
    return

#salvo in una collezione tutti i termini del corpus con le rispettive occorrenze in modo da non doverlo ricalcolare
def insert_terms_frequency(term, freq):
    term_frequency_corpus.insert_one({'term': term,'frequency': freq})
    return

def save_frequency_allcorpus():
    alltokens = []
    print("Sto raccogliendo tutti i token...")
    # salvo una lista con tutte le liste di token di tutti i documenti del corpus in modo da poter calcolare la specificità
    for p in paragraphs_coll.find(None, {'_id': 0, 'tokens': 1}):
        alltokens.append(p['tokens'])

    print("Ho finito di raccogliere i token.")

    print("Conto le occorenze nella lista di token del corpus...")
    # riduco la lista di liste ad una singola lista con tutto mergiato per poter contare le occorrenze dei termini
    all_list = chain.from_iterable(alltokens)
    term_freqs_all = Counter(all_list)

    print("Riduzione ad un'unica lista terminata.")

    for x in term_freqs_all.keys():
        insert_terms_frequency(x, term_freqs_all[x])
    return




