import random
import json

#gerador de pseudopalavras
vowels = ['a', 'e', 'i', 'o', 'u']
consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'x', 'z']

#def how_many():
#    dataset = int(input("How many pseudowords do you need?"))
#    return dataset

def pw(n):
    pseudowords = []
    print("Generating pseudowords... please wait")
    while len(pseudowords) < n:
        word = ''
        size = random.randint(3,4)
        vs = random.sample(vowels, 2)
        cs = random.sample(consonants,2)
        if size == 3:
            word = cs[0]+vs[0]+cs[1]
        else:
            word = cs[0]+vs[0]+cs[1]+vs[1]
        pseudowords.append(word)
    return pseudowords

pseudowords = pw(1000)
print(pseudowords)
with open('pseudowords.json', 'w') as f:
    json.dump(pseudowords, f)


#d_english = enchant.Dict("en_US")
#d_portuguese = enchant.Dict("pt_BR")
#d_spanish = enchant.Dict("es_AR")



