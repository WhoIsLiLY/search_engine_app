import re

def remove_link(text):
    #Remove symbol
    return re.sub(r'http\S+|www\.\S+', '', text)

#Example
text = "Check this out: https://example.com is not that cool video"
clean_text = remove_link(text)
print(clean_text)



# import nltk
# from nltk.tokenize import word_tokenize

# nltk.download('punkt')

# def remove_urls(text):
#     words = word_tokenize(text)
#     words_no_links = []

#     for word in words:
#         if not word.startswith(('http', 'www')):
#             words_no_links.append(word)

#     cleaned_text = ' '.join(words_no_links)
    
#     return cleaned_text

# #Example
# text = "Check this out: https://example.com"

# result = remove_urls(text)
# print(result)
