import storage
import cmath
from collections import Counter


topic_dict = {}

def get_specific_words(topicId,Ldawords, tokenlist):
    specific_words = []
    final_words_list = []

    #print("1. Conto le occorrenze nella lista di token del paragrafo...")
    # creo un dizionario in cui salvo ogni termine e la sua frequenza nella lista
    term_freqs = Counter(tokenlist)
    total_f = list(storage.term_frequency_corpus.aggregate([{'$group': {'_id': None, 'count': {'$sum': 1}}}]))[0]['count']


    #print("2. Per ogni parola dell'Lda calcolo la sua specificità nel paragrafo...")
    for word in Ldawords:
        tf = 0
        tf_all = 1

        if word in term_freqs.keys():
            for t in term_freqs.keys():
                if t == word:
                    tf = float(term_freqs[t]) / len(tokenlist)

            for k in storage.term_frequency_corpus.find({'term': word}, {'_id':0,'frequency':1}):
                tf_all = float(k['frequency']) / total_f
            try:
                specificity = (tf - tf_all)/cmath.sqrt(tf_all)

            except KeyError:
                specificity = -1

            if cmath.phase(specificity) > -0.5:
                specific_words.append(word)

    #vado a prendere il termine originale con maggiore occorrenza nella collezione di riferimento per i termini stemmizzati
    for w in specific_words:
        for k in storage.terms_ref_coll.find({'token': w},{'_id':0,'originals':1}):
            counter = Counter(k['originals'])
            mostcomm = counter.most_common(1)[0][0] #perche' restituisce una lista di coppie (term, freq)
            final_words_list.append(mostcomm)


    #metto in un dict la lista completa di termini specifici per i paragrafi per ogni topic
    #quindi chiave > topic, valore > lista termini specifici in tutti i paragrafi
    if topicId not in topic_dict.keys():
        topic_dict[topicId] = [final_words_list]

    else:
        topic_dict[topicId].append(final_words_list)


    return final_words_list


def get_topic_dict():
    return topic_dict

def empty_topic_dict():
    topic_dict.clear()
    return