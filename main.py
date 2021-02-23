import nbib
import json
import RAKE

refs = nbib.read_file('./pubmed-relational-set.nbib')

# keys = set()
# for item in refs:
    # for key in item:
        # keys.add(key)
#
# print(keys)
#
# exit(0)

# "list comprehension" -> Açúcar sintático
documents = [ {
    'title': item.get('title', ''),
    'abstract': item.get('abstract', ''),
    'keywords': item.get('keywords', ''),
} for item in refs ]

rake = RAKE.Rake('stopwords')

doc = documents[0]

factor = 3

def top10(docs, numTopKeywords = 10):
    keywordsDict = {}
    for doc in docs:
        # TODO(vinicius.garcia): We should differentiate the keywords from the rest of the text
        # since they are likely more important than the rest since they were selected by humans.
        keywords = rake.run('%s\n%s\n%s' % (doc['title'], doc['abstract'], doc['keywords']))

        for kw, weight in keywords:
            keywordsDict[kw] = keywordsDict.get(kw, 0) + weight * factor

    keywords = list(keywordsDict.items())
    keywords.sort(key = lambda x : -x[1])

    return keywords[:numTopKeywords]

topKeywords = top10(documents, 30)
print(topKeywords)

