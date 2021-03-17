
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer as v

def keywordExtraction(documents, globalKeywords):
    tfidfVectorized = v(use_idf=True)
    topKeywords = top10(tfidfVectorized, documents, globalKeywords, 30)
    return topKeywords

def top10(tfidf, docs, globalKeywords, numTopKeywords = 20, minTokens=3, defaultKeywordScore=0, factor=3):
    dataset = ['%s\n%s\n%s' % (doc['title'], doc['abstract'], doc['keywords']) for doc in docs]
    model = tfidf.fit_transform(dataset)
    df = pd.DataFrame(model[0].T.todense(), index=tfidf.get_feature_names(), columns=["TF-IDF"])
    keywordsDict = df.to_dict()['TF-IDF']

        # for kw, weight in keywords:
            # if kw.count(" ") < minTokens-1: continue
            # if kw in keywordsDict:
                # keywordsDict[kw] += weight * factor
            # else:
                # keywordsDict[kw] = weight * factor

        # for kw in doc['keywords']:
            # if kw in keywordsDict:
                # keywordsDict[kw] += defaultKeywordScore
            # else:
                # keywordsDict[kw] = defaultKeywordScore

    # for kw in globalKeywords:
        # if kw in keywordsDict:
            # keywordsDict[kw] += defaultKeywordScore
        # else:
            # keywordsDict[kw] = defaultKeywordScore

    keywords = list(keywordsDict.items())
    keywords.sort(key = lambda x : -x[1])

    return keywords[:numTopKeywords]

