import nbib
import json
import RAKE

refs = nbib.read_file('./pubmed-relational-set.nbib')
print("number of refs before dedup:", len(refs))

refsDict = {}
for ref in refs:
    if 'title' not in ref: continue
    refsDict[ref['title']] = ref

refs = list(refsDict.values())

print("number of refs after dedup:", len(refs))

globalKeywords = set()
for ref in refs:
    if 'keywords' in ref:
        globalKeywords = globalKeywords.union(ref['keywords'])

def listAllPossibleKeys(refs):
    keys = set()
    for ref in refs:
        for key in ref:
            keys.add(key)
    return keys

# print(listAllPossibleKeys(refs))
# exit(0)

# "list comprehension" -> Açúcar sintático
documents = [ {
    'title': item.get('title', ''),
    'abstract': item.get('abstract', ''),
    'keywords': item.get('keywords', ''),
} for item in refs ]

rake = RAKE.Rake('stopwords')

doc = documents[0]

def top10(docs, globalKeywords, numTopKeywords = 20, minTokens=3, defaultKeywordScore=5, factor=3):
    keywordsDict = {}
    for doc in docs:
        # TODO(vinicius.garcia): We should differentiate the keywords from the rest of the text
        # since they are likely more important than the rest since they were selected by humans.
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

topKeywords = top10(documents, globalKeywords, 30)
print(topKeywords)

