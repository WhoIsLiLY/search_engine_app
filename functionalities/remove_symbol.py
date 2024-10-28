# import re

# def remove_at_symbol(text):
#     #Remove symbol
#     return re.sub(r'[.,/\'\"!?:;]', '', text)

# #Example
# text = "Halo brow, kita lagi coba-coba symbol nih! BTW ini ada symbol lain / "
# clean_text = remove_at_symbol(text)
# print(clean_text)


def remove_symbol(text):
    #List remove symbol 
    symbols = ".,:;\"'?!"
    words = []

    for word in text:
        if word not in symbols:
            words.append(word)

    #Combine words to text
    result_text = ''.join(words)
    return result_text

#Example
text = "@Hello, world! This is a test: let's remove symbols like ,.:;\"'?!"
result_text = remove_symbol(text)
print(result_text)

