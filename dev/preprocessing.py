import re
import emoji
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

stemmer = StemmerFactory().create_stemmer()
stopper = StopWordRemoverFactory().create_stop_word_remover()

def preprocess_text(text):
    def process_hashtag(hashtag):
        # Pola 1: Remove hashtag
        if hashtag[1:].islower() and "" not in hashtag:
            return hashtag[1:]

        elif "" in hashtag:
            # Case khusus 1
            if hashtag[1].islower() and any(c.isupper() for c in hashtag.split("")[1:]):
                return hashtag[1:].replace("", " ")
            # Case khusus 2 & Pola 2: Remove hashtag + ganti  dengan spasi
            else:
                return hashtag[1:].replace("_", " ")

        # Pola 3: Remove hashtag + tambahkan spasi
        else:
            word = hashtag[1:2]
            for i in hashtag[2:]:
                if i.isupper():
                    word += " "
                word += i
            return word

    # Lowercase
    text = text.lower()

    # Remove mentions and links
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'http\S+|www.\S+', '', text)

    # Process hashtags
    processed_text = ""
    for word in text.split():
        if word.startswith("#"):
            processed_text += process_hashtag(word)
        else:
            processed_text += word + " "

    # Remove symbols and emoji
    text = re.sub(r'[^\w\s]', '', text)
    text = emoji.replace_emoji(text, replace='')

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def stemmer_and_remove_stopwords(text):
    stemmed = stemmer.stem(text)
    return stopper.remove(stemmed)
