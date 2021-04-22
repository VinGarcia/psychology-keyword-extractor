
import RAKE

def keywordExtraction(docs, globalKeywords, minTokens=2, defaultKeywordScore=0, factor=1):
    rake = RAKE.Rake('stopwords')

    keywordsDict = {}
    for doc in docs:
        keywords = rake.run('%s\n%s' % (doc['title'], doc['abstract']))
        for kw, weight in keywords:
            if kw.count(" ") < minTokens-1: continue
            if kw in keywordsDict:
                keywordsDict[kw] += weight * factor
            else:
                keywordsDict[kw] = weight * factor

        # for kw in doc['keywords']:
            # if kw in keywordsDict:
                # keywordsDict[kw] += defaultKeywordScore
            # else:
                # keywordsDict[kw] = defaultKeywordScore
#
    # for kw in globalKeywords:
        # if kw in keywordsDict:
            # keywordsDict[kw] += defaultKeywordScore
        # else:
            # keywordsDict[kw] = defaultKeywordScore

    keywords = list(keywordsDict.items())
    keywords.sort(key = lambda x : -x[1])

    return keywords
