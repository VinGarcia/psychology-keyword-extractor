import nbib
import csv

import strategies.rake as rake
import strategies.tfidf as tfidf
import strategies.textrank as textrank

# refs = nbib.read_file('./pubmed-relational-set.nbib')

refs = []
with open('dados.csv') as f:
    reader = csv.DictReader(f, delimiter=',')

    for row in reader:
        refs.append({
            'title': row['titulo'],
            'abstract': row['abstract'],
            'keywords': row['keywords'],
        })

print("number of refs before dedup:", len(refs))

refsDict = {}
for ref in refs:
    if 'title' not in ref: continue
    refsDict[ref['title']] = ref

refs = list(refsDict.values())

print("number of refs after dedup:", len(refs))

globalKeywords = set()
# for ref in refs:
    # if 'keywords' in ref:
        # globalKeywords = globalKeywords.union(ref['keywords'])

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

keywords = 2
rake_result = [x[0] for x in rake.keywordExtraction(documents, globalKeywords, keywords)]
tfidf_result = [x[0] for x in tfidf.keywordExtraction(documents, globalKeywords, keywords)]
textrank_result = [x[0] for x in textrank.keywordExtraction(documents, globalKeywords, keywords)]

def half(l):
    return l[:int(len(l)/2)]

# print('t' in rake_result)
# print(rake_result)
# print(tfidf_result[:30])
# print(textrank_result)
# exit(0)

counter = {}
for r in half(rake_result) + half(textrank_result) + half(tfidf_result):
    counter[r] = counter.get(r, 0) + 1

sortedItems = list(counter.items())
sortedItems.sort(key = lambda x : x[1])
sortedItems = [item for item in sortedItems if item[1] > 1]
print(sortedItems)

rake_result = set(half(rake_result))
tfidf_result = set(half(tfidf_result))
textrank_result = set(half(textrank_result))

print("rake vs tfidf:", rake_result.intersection(tfidf_result))
print("rake vs textrank:", rake_result.intersection(textrank_result))
print("tfidf vs textrank:", tfidf_result.intersection(textrank_result))

print("full intersection:", tfidf_result.intersection(textrank_result).intersection(rake_result))
