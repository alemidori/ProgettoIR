from gensim import corpora, models
import storage


dictionary = {}


def calculate_topic_distribution():

    corpus,dictionary = create_dictionary()
    # salvo una lista di array dove ogni array è un documento e
    # le coppie presenti nell'array sono rispettivamente (id_token, frequenza)

    # classe che prende un corpus il dizionario e il numero di topic (prende anche un parametro opzionale "iteration"
    # che se aumentato serve a migliorare il risultato)
    Lda_model = models.LdaModel(corpus, id2word=dictionary, num_topics=50)

    for k in Lda_model.show_topics(num_topics=50,num_words=50,formatted=False):
        terms = []
        for i in range(0,50):
            terms.append(k[1][i][0])
        storage.insert_topics_3_most_significant_words(k[0], terms)
        #print(k)


    corpus_Lda = Lda_model[corpus]
    #corpora.BleiCorpus.serialize("tmp/corpus_stories.lda-c",corpus)
    corpora.BleiCorpus.serialize('tmp/corpus_stories.lda-c', corpus_Lda)

    return

def create_dictionary():

    stemmed = storage.get_stemmed_terms_paragraph()
    dictionary = corpora.Dictionary(stemmed)

    corpus = [dictionary.doc2bow(token) for token in stemmed]

    # salvo il dizionario in una specifica cartella così da utilizzarlo eventualmente in futuro
    # dictionary.save('tmp/dictionary.dict')
    print("Dizionario creato.")
    return corpus, dictionary

def load_lda_corpus():

    corpus_Lda = corpora.BleiCorpus("tmp/corpus_stories.lda-c") #carico il corpus precedentemente salvato
    # stampa una serie di array aventi 100 coppie corrispondenti in questo caso ai 100 topic (se un topic non è per
    # niente presente in un documento la coppia non verrà mostrata affatto)
    # (se ci fossero tot topic stamperebbe tot coppie, ma solo se effettivamente nei documenti sono presenti)
    # in ciascuna delle coppie: (id_topic, distribuzione del documento su quel topic quindi più alto è il valore
    # e più il documento parlerà di quel tipic)

    # for doc in corpus_Lda[:10]: #prende i primi 10 in base a come sono stati inseriti nel corpus
    #    print(doc)

    return corpus_Lda

def calculate_main_topic_for_parag():

    corpusLda = load_lda_corpus()
    #creo una lista avente gli id dei topic più rilevanti per ogni documento, in ordine
    #in modo tale che posso per ogni documento associarvi il topic saliente

    max_list = []
    for doc in corpusLda:
        single_list = []  # singola lista di topic per ciascun paragrafo
        max_dict = {}
        for n in doc:  # per ogni topic nel pragrafo
            single_list.append(n[1])  # appendo il valore della sua distribuzione

        for n in doc:
            if n[1] == max(single_list) and n[1] not in max_dict.values():  # trovo il topic con maggiore distribuzione
                max_dict[n[0]] = n[1]

        max_list.append(max_dict)

    list_topicmax = []

    for elem in max_list:
        for key in elem:
            list_topicmax.append(key)

    return list_topicmax