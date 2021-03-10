
import RAKE

def keywordExtraction(documents, globalKeywords):
    rake = RAKE.Rake('stopwords')
    topKeywords = top10(rake, documents, globalKeywords, 30)
    return topKeywords

def top10(rake, docs, globalKeywords, numTopKeywords = 20, minTokens=3, defaultKeywordScore=5, factor=3):
    keywordsDict = {}
    for doc in docs:
        keywords = rake.run('%s\n%s' % (doc['title'], doc['abstract']))
        for kw, weight in keywords:
            if kw.count(" ") < minTokens-1: continue
            if kw in keywordsDict:
                keywordsDict[kw] += weight * factor
            else:
                keywordsDict[kw] = weight * factor

        for kw in doc['keywords']:
            if kw in keywordsDict:
                keywordsDict[kw] += defaultKeywordScore
            else:
                keywordsDict[kw] = defaultKeywordScore

    for kw in globalKeywords:
        if kw in keywordsDict:
            keywordsDict[kw] += defaultKeywordScore
        else:
            keywordsDict[kw] = defaultKeywordScore

    keywords = list(keywordsDict.items())
    keywords.sort(key = lambda x : -x[1])

    return keywords[:numTopKeywords]
