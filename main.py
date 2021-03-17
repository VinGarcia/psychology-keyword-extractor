import nbib

import strategies.rake as rake
import strategies.tfidf as tfidf
import strategies.textrank as textrank

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

print("rake:", rake.keywordExtraction(documents, globalKeywords))
print("tfidf:", tfidf.keywordExtraction(documents, globalKeywords))
print("textrank:", textrank.keywordExtraction(documents, globalKeywords))
