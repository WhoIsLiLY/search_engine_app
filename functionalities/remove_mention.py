# import re

# def remove_at_symbol(text):
#     #Remove mention @
#     return re.sub(r'@(\w+)', r'\1', text)

# #Example
# text = "@HelloWorld, adalah sebuah mention yang berada di IG!"
# clean_text = remove_at_symbol(text)
# print(clean_text)



def remove_mention(text):
    #List remove symbol 
    symbols = "@"
    words = []

    
    for word in text:
        if word != symbols:
            words.append(word)

    #Combine words to text
    result_text = ''.join(words)
    return result_text

#Example
text = "@HelloWorld, adalah sebuah mention yang berada di IG!"
result_text = remove_mention(text)
print(result_text)
