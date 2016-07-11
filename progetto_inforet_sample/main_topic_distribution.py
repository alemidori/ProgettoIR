
import topic_distribution
import logging

#serve per stampare anche i log durante la fase di esecuzione
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def main():
    topic_distribution.calculate_topic_distribution()
    return

#print("Processo terminato.")