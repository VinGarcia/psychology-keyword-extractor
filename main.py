import nbib
import csv
import json

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
    'title': item.get('title', '').lower(),
    'abstract': item.get('abstract', '').lower(),
    'keywords': item.get('keywords', '').lower(),
} for item in refs ]

nGramTokens = 2
rake_result = [x[0] for x in rake.keywordExtraction(documents, globalKeywords, nGramTokens)]
tfidf_result = [x[0] for x in tfidf.keywordExtraction(documents, globalKeywords, nGramTokens)]
textrank_result = [x[0] for x in textrank.keywordExtraction(documents, globalKeywords, nGramTokens)]

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

# sortedItems = list(counter.items())
# sortedItems.sort(key = lambda x : x[1])
# sortedItems = [item for item in sortedItems if item[1] > 1]
# print(sortedItems)

rake_result = set(half(rake_result))
tfidf_result = set(half(tfidf_result))
textrank_result = set(half(textrank_result))

words = rake_result.union(tfidf_result).union(textrank_result)
print('total words:', len(words))

# TODO: include 1-grams in the dataset below

matrix = {}
for word in words:
    matrix[word] = [word in doc['abstract'] for doc in documents]

# Count how many words are present on each document:
wordsInDoc = [0 for i in range(len(documents))]
for word in matrix:
    for i in range(len(matrix[word])):
        if matrix[word][i] == True:
            wordsInDoc[i] += 1

# Calculate the strength of each word
# based on the number of other words that are
# present in the same documents as it.
scores = []
for word in words:
    score = 0
    for i in range(len(matrix[word])):
        if matrix[word][i]:
            score += wordsInDoc[i] - 1
    scores.append((word, score))

scores.sort(key = lambda x : -x[1])

# filteredScores = set(scores)
# for (word1, score1) in scores:
    # for (word2, score2) in scores:
        # if word1 != word2 and word1 in word2 and word2.count(" ") > word1.count(" "):
            # if (word1, score1) not in filteredScores: continue
            # print("removed '%s'\n because of '%s'" % (word1, word2))
            # filteredScores.remove((word1, score1))

selected = set()
for (w, s) in scores:
    shouldChange = False
    shouldAdd = True
    replaceW, replaceS = "", 0
    for (selectedW, selectedS) in selected:
        if w in selectedW:
            shouldAdd = False
            break
        if selectedW in w:
            shouldChange = True
            replaceW, replaceS = selectedW, selectedS
            break

    if not shouldAdd: continue

    if shouldChange:
        print("should change '%s' for '%s'" % (selectedW, w))
        selected.remove((replaceW, replaceS))
        selected.add((w, s))
        continue

    print("adding '%s' %d" % (w, s))
    selected.add((w, s))
    if len(selected) == 19: break


scores = list(selected)
scores.sort(key = lambda x : -x[1])

print(len(scores))

scores.sort(key = lambda x : -x[1])

print("scores", scores[:20])

with open('scores.json', 'w') as f:
    f.write(json.dumps(scores))

# print("rake vs tfidf:", rake_result.intersection(tfidf_result))
# print("rake vs textrank:", rake_result.intersection(textrank_result))
# print("tfidf vs textrank:", tfidf_result.intersection(textrank_result))
#
# print("full intersection:", tfidf_result.intersection(textrank_result).intersection(rake_result))
