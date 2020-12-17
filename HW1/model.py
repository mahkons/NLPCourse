import json

import gensim
import gensim.corpora as corpora
import pyLDAvis.gensim


if __name__ == "__main__":
    with open("text_2.txt", 'r') as file:
        data = json.loads(file.read())

    bigram = gensim.models.Phrases(data, min_count=5, threshold=25)
    bigram_mod = gensim.models.phrases.Phraser(bigram)

    data = list(map(lambda text: bigram_mod[text], data))

    id2word = corpora.Dictionary(data)
    corpus = list(map(lambda text: id2word.doc2bow(text), data))
    tfidf = gensim.models.TfidfModel(corpus)[corpus]
    
    lda = gensim.models.LdaModel(tfidf, id2word=id2word, num_topics=10, passes=3, random_state=239)
    coherence_lda = gensim.models.CoherenceModel(model=lda, texts=data, dictionary=id2word, coherence='c_v').get_coherence()
    print("Perplexity: {}".format(lda.log_perplexity(corpus)))
    print("Coherence Score: {}".format(coherence_lda))

    vis = pyLDAvis.gensim.prepare(lda, corpus, dictionary=lda.id2word)
    pyLDAvis.show(vis)

