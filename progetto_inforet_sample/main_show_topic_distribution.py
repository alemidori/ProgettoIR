
import logging
import show_html


#serve per stampare anche i log durante la fase di esecuzione
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def main():
    show_html.create_folder()
    show_html.set_topic_random_color()
    show_html.create_tablesfile()
    show_html.fill_index()
    return

main()