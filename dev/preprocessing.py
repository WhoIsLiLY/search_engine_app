import re
import emoji
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

stemmer = StemmerFactory().create_stemmer()
stopper = StopWordRemoverFactory().create_stop_word_remover()

def preprocess_text(text):
    def process_hashtag(hashtag):
        # Pola 1: Remove hashtag IF ada "_"
        if "_" in hashtag:  # Perbaikan logika pada tanda underscore
            # Case khusus 1
            if hashtag[1].islower() and any(c.isupper() for c in list(hashtag[1:])):
                return hashtag[1:].replace("_", " ") + " "
            # Case khusus 2 & Pola 2: Remove hashtag + ganti dengan spasi
            else:
                return hashtag[1:].replace("_", " ") + " "
        
        # Pola 2: Remove hashtag IF gaada "_" dan all lowercase
        elif hashtag[1].islower() and " " not in hashtag:
            return hashtag[1:] + " "

        # Pola 3: Remove hashtag IF ada PascalCase + tambahkan spasi untuk pemisah
        else:
            word = hashtag[1:2]
            for i in hashtag[2:]:
                if i.isupper():
                    word += " "
                word += i
            return word + " "

    # Process hashtags
    processed_text = ""
    for word in text.split():
        if word.startswith("#"):
            processed_text += process_hashtag(word)
        else:
            processed_text += word + " "
    # Lowercase
    processed_text = processed_text.lower()

    # Remove mentions and links
    processed_text = re.sub(r'@\w+', '', processed_text)
    processed_text = re.sub(r'http\S+|www.\S+', '', processed_text)

    # Remove symbols and emoji
    processed_text = re.sub(r'[^\w\s]', '', processed_text)
    processed_text = emoji.replace_emoji(processed_text, replace='')

    # Remove extra spaces
    processed_text = re.sub(r'\s+', ' ', processed_text).strip()

    return processed_text

def stemmer_and_remove_stopwords(text):
    stemmed = stemmer.stem(text)
    return stopper.remove(stemmed)

# text = preprocess_text("#lifeisgood #LifeIsGood #life_is_good #lifeIsGood #LifeIs_Good")
# print(text)