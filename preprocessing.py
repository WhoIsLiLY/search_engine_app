import sys
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import re
import emoji
from nltk.corpus import stopwords

stemmer = StemmerFactory().create_stemmer()
stopper = StopWordRemoverFactory().create_stop_word_remover()

# indonesian_stopper = StopWordRemoverFactory().get_stop_words()
# english_stopper = set(stopwords.words('english'))
# combined_stopwords = set(indonesian_stopper).union(english_stopper)

# sendTitle = sys.argv[1]
# sendTitle = sendTitle.split("##")
# sendTitle = list(filter(None, sendTitle))
# sendTitle = ' '.join(sendTitle)

# stem_title = stemmer.stem(sendTitle)
# stop_title = stopper.remove(stem_title)

# print(stop_title)

def preprocess_hashtags(text):
    hashtags = []
    
    for hashtag in text.split():
        if not hashtag.startswith("#"):
            continue
        
        # Pola 1: Hapus tanda "#" jika semua karakter setelahnya huruf kecil dan tidak ada "_"
        if hashtag[1:].islower() and "_" not in hashtag:
            hashtags.append(hashtag[1:])
        
        elif "_" in hashtag:
            # Case khusus 1: Kata pertama huruf kecil, kata setelah "_" memiliki huruf besar
            if hashtag[1].islower() and any(c.isupper() for c in hashtag.split("_")[1:]):
                hashtags.append(hashtag[1:].replace("_", " "))
            # Case khusus 2 & Pola 2: Hapus "#" dan ganti "_" dengan spasi
            else:
                hashtags.append(hashtag[1:].replace("_", " "))
        
        # Pola 3: Hapus "#" dan tambahkan spasi antara huruf besar
        else:
            word = hashtag[1:2]  
            for i in hashtag[2:]:
                if i.isupper():
                    word += " "  
                word += i
            hashtags.append(word)
    
    return hashtags


def remove_link(text):
    preprocess_link = re.sub(r'http\S+|www\.\S+', '', text) # Remove Link
    return preprocess_link

def remove_prepocessing(text):
    preprocess_text = re.sub(r'\s+', ' ', text)
    preprocess_text = text.lower() # Case Folding
    preprocess_text = re.sub(r'@\w+', '', text) # Remove Mention
    preprocess_text = re.sub(r'[()|[].,/\'\"!?:;-]', '', text) # Remove Symbol
    preprocess_text = emoji.replace_emoji(text, replace="") # Remove Emoji
    symbol_pattern = re.compile(r"[^\w\s]", re.UNICODE) # Remove More Symbol
    preprocess_text = symbol_pattern.sub("", text)
    return preprocess_text

def stemmer_and_remove_stopwords(text):
    stemmer_text = stemmer.stem(text) # Stemming
    stop_removed_text = stopper.remove(stemmer_text) # Remove Stopwords
    return stop_removed_text

    # words = stemmer_text.split()
    # stopwords_text = []
    # for word in words:
    #     if word != combined_stopwords:
    #         stopwords_text.append(word)
    # return ' '.join(stopwords_text)