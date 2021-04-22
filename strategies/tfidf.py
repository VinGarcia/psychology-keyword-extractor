
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer as v

def keywordExtraction(docs, globalKeywords, minTokens=2, defaultKeywordScore=0, factor=1):
    tfidf = v(use_idf=True)

    dataset = ['%s\n%s' % (doc['title'], doc['abstract']) for doc in docs]
    model = tfidf.fit_transform(dataset)
    df = pd.DataFrame(model[0].T.todense(), index=tfidf.get_feature_names(), columns=["TF-IDF"])
    keywordsDict = df.to_dict()['TF-IDF']

    keywords = list(keywordsDict.items())
    keywords.sort(key = lambda x : -x[1])

    return keywords
