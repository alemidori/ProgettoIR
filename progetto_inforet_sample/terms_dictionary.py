import storage

terms_ref = dict()

def update_terms_dictionary(stemmed,original): #ammetto ripetizioni di termini originali nella lista
    if stemmed in terms_ref.keys():  # vedo se c'è nelle chiavi
            try:
                terms_ref[stemmed].append(original) #appendo alla lista già esistente per il token un altro "original"
            except KeyError:
                terms_ref[stemmed] = [original]
    else:
        terms_ref[stemmed] = [original]  # altrimenti aggiungo la chiave e il valore del termine non stemmizzato nell'array

    return

def create_terms_dictonary():
    print("Creazione collezione termini...")
    storage.insert_terms_ref(terms_ref)
    return

