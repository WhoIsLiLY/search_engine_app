import re
import emoji
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

stemmer = StemmerFactory().create_stemmer()
stopper = StopWordRemoverFactory().create_stop_word_remover()

def preprocess_text(text):
    def process_hashtag(hashtag):
        if len(hashtag) < 2:
            return "#"

        # Pola 1: Remove hashtag IF ada "_"
        if "_" in hashtag:  # Perbaikan logika pada tanda underscore
            return hashtag[1:].replace("_", " ") + " "

        # Pola 2: Remove hashtag IF gaada "_" dan all lowercase
        elif hashtag[1].islower() or hashtag[1:].isupper() and " " not in hashtag:
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
    # processed_text = re.sub(r'\\n|\\{[a-zA-Z]\\}', '', processed_text) #untuk menghilangkan /{huruf}

    # Remove symbols and emoji
    processed_text = re.sub(r'[^\w\s]', '', processed_text)
    processed_text = emoji.replace_emoji(processed_text, replace='')

    # Remove extra spaces
    processed_text = re.sub(r'\s+', ' ', processed_text).strip()

    return processed_text

def stemmer_and_remove_stopwords(text):
    stemmed = stemmer.stem(text)
    return stopper.remove(stemmed)

# text = preprocess_text("GAK NYANGKAMERINDING LAGU TERIMA KASIH COACH SHIN TAE-YONG MEMBUAT SUPORTER INDONESIA SEDIH\n\nVideo ini menghadirkan momen haru yang menggugah hati, di mana para suporter Indonesia mempersembahkan lagu berjudul “ \nTERIMA KASIH COACH SHIN TAE-YONG” sebagai bentuk apresiasi atas dedikasi dan perjuangan beliau bersama Timnas Indonesia.\n\nSimak bagaimana lagu ini menciptakan suasana penuh emosional di tengah dukungan para suporter yang tak pernah padam. Lagu ini bukan hanya ungkapan terima kasih, tapi juga wujud penghormatan atas kontribusi besar Coach Shin Tae-yong dalam mengangkat prestasi sepak bola Indonesia.\n\nTonton hingga akhir untuk merasakan getaran semangat, haru, dan kebersamaan yang luar biasa! Jangan lupa like, comment, dan subscribe untuk mendukung Timnas Indonesia dan perjalanan sepak bola kita ke tingkat yang lebih tinggi!\"\n\n#ShinTaeYong #TimnasIndonesia #TerimaKasihCoach #\n#SepakBolaIndonesia #SupporterIndonesia #rianrrr  #shintaeyong #viralvideo #coversong")
# print(text)