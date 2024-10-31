#Case folding
def case_folding(text):
    words = []

    for word in text:
        lower_word = word.lower()
        words.append(lower_word)
    
    return words

#Example
text = ["Hello WORLD!"]
result = case_folding(text)
print(result)