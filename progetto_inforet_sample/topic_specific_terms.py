import storage
import specificity
import show_html
from collections import Counter
import main_show_topic_distribution
from operator import itemgetter

terms_document_dict = {}

def calculate_specific_terms(listmaintopic):

    stories = []

    for k in storage.paragraphs_coll.distinct('id_story'):
        stories.append(k)

    increment_for_topiclist = 0
    finallist = []

    for p in stories:
        print("Documento "+str(stories.index(p)))

        number_topic = increment_for_topiclist

        print("Calcolo specificità...")
        for k in storage.paragraphs_coll.find({'id_story': p},{'_id':0,'tokens':1}):

            listwords = []
            if increment_for_topiclist <= len(listmaintopic)-1:
                for v in storage.topics_terms.find({'id_topic':listmaintopic[increment_for_topiclist]}, {'_id':0,'words_list':1}):
                    listwords = v['words_list'] #lista prime 50 parole del topic date dall'LDA

                #lista contenente liste di termini lda specifici nel paragrafo, quindi nella posizione 595 c'è la lista di
                #termini specifici per l'ultimo paragrafo del primo racconto e così via
                finallist.append(specificity.get_specific_words(listmaintopic[increment_for_topiclist],listwords, k['tokens']))

                increment_for_topiclist += 1

            else:
                exit(1)

        final_topic_dict = specificity.get_topic_dict()


        print("Scrivo tabella nell'html...")

        #print(number_topic)
        for k in storage.paragraphs_coll.find({'id_story': p}, {'_id': 0, 'descr': 1}):
            show_html.fill_tables(p, k['descr'], listmaintopic[number_topic],
                                final_topic_dict[listmaintopic[number_topic]],finallist[number_topic])
            number_topic += 1

        print("Tabella aggiunta nell'html")

        show_html.add_docrow_in_topic_description(stories.index(p))

        for key in final_topic_dict.keys():

            show_html.fill_topicfile(key, sorted(dict(Counter(sum(final_topic_dict[key], []))).items(),key=itemgetter(1),reverse=True))

        specificity.empty_topic_dict()
        print("Topic aggiunti nell'html")

    return