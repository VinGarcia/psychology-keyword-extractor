
from gensim.summarization import keywords as textrankKeywords

def keywordExtraction(docs, globalKeywords, minTokens=2, defaultKeywordScore=0, factor=1):
    keywordsDict = {}
    for doc in docs:
        content = '%s\n%s' % (doc['title'], doc['abstract'])
        keywords = textrankKeywords(content.lower()).split('\n')
        for kw in keywords:
            if kw.count(" ") < minTokens-1: continue
            if kw in keywordsDict:
                keywordsDict[kw] += factor
            else:
                keywordsDict[kw] = factor

        # for kw in doc['keywords']:
            # kw = kw.lower()
            # if kw in keywordsDict:
                # keywordsDict[kw] += defaultKeywordScore
            # else:
                # keywordsDict[kw] = defaultKeywordScore
#
    # for kw in globalKeywords:
        # kw = kw.lower()
        # if kw in keywordsDict:
            # keywordsDict[kw] += defaultKeywordScore
        # else:
            # keywordsDict[kw] = defaultKeywordScore

    keywords = list(keywordsDict.items())
    keywords.sort(key = lambda x : -x[1])

    return keywords
