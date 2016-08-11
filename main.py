import logging
import threading
from searching import Searcher
from download import Downloader


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S', )

label_filename = 'labels.txt'

if __name__ == "__main__":
    engine_name = 'bing'
    downloader = Downloader(engine_name)
    searcher = Searcher(engine_name)
    for i in range(10):
        thread = threading.Thread(target=downloader.download, name="Downloader {0}".format(str(i)))
        thread.start()
        # thread.join()
        logging.info(thread.name + "started")
    with open(label_filename, 'r') as f:
        key_words = f.read().split('\n')
        for key_word in key_words:
            if key_word:
                logging.info('Searching {0}'.format(key_word))
                searcher.do_search(key_word)
