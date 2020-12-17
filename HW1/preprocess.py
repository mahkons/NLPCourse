import json
import nltk
import autocorrect
import string

def process_text(text):
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    
    # slow
    #  speller = autocorrect.Speller(lang="en")
    #  tokens = list(map(speller, tokens))

    stopwords = set(nltk.corpus.stopwords.words('english'))
    stopwords.update(string.punctuation)
    tokens = list(filter(lambda x: x not in stopwords, tokens))

    lemmatizer = nltk.stem.WordNetLemmatizer()
    tokens = list(map(lambda word: lemmatizer.lemmatize(word), tokens))
    
    return tokens

if __name__ == "__main__":
    with open("text_1.txt", 'r') as file:
        data = json.loads(file.read())

    data = list(map(process_text, data))

    with open("text_2.txt", 'w') as file:
        file.write(json.dumps(data))

