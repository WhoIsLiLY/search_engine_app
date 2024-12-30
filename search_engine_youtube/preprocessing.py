import re
import sys
import emoji
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

stemmer = StemmerFactory().create_stemmer()
stopper = StopWordRemoverFactory().create_stop_word_remover()

def remove_prepocessing(text):
    # Lowercase
    text = text.lower()

    # Remove mentions, hashtags, and links
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#\w+', '', text)
    text = re.sub(r'http\S+|www\.\S+', '', text)

    # Remove symbols and emoji
    text = re.sub(r'[^\w\s]', '', text)
    text = emoji.replace_emoji(text, replace='')

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def stemmer_and_remove_stopwords(text):
    stemmed = stemmer.stem(text)
    return stopper.remove(stemmed)

if sys.argv[1]