import csv
import json

from matplotlib import pyplot as plt

with open('scores.json') as f:
    strengths = json.load(f)[:20]

strengths.reverse()

x = list(range(len(strengths)))
y = [strength for (word, strength) in strengths]

fig = plt.figure()

graph = fig.add_subplot(111)

# Plot the data as a black line with round markers
# graph.bar(x,y)
graph.plot(x, y, 'k-o')

# Set the xtick locations to correspond to just the dates you entered.
graph.set_xticks(x)
graph.set_ylim(bottom=0)

# Set the xtick labels to correspond to just the dates you entered.
graph.set_xticklabels(
    ['' for (word, strength) in strengths],
    rotation=40,
)

for i in range(len(strengths)):
    plt.text(x[i], y[i], ' ' + strengths[i][0], color='black', rotation=45)

# plt.margins(0.14)
plt.subplots_adjust(bottom=0.25)

plt.show()

# 28/05/2020
# ['DATA DA NOTIFICACAO', 'DOR DE GARGANTA', 'DISPNEIA', 'FEBRE', 'TOSSE', 'OUTROS', 'E PROFISSIONAL DE SAUDE?', 'DATA DO INICIO DOS SINTOMAS', 'DOENCAS RESPIRATORIAS CRONICAS DESCOMPENSADAS', 'DOENCAS CARDIACAS CRONICAS', 'DIABETES', 'DOENCAS RENAIS CRONICAS EM ESTAGIO AVANCADO (GRAUS 3, 4 OU 5)', 'IMUNOSSUPRESSAO', 'GESTANTE DE ALTO RISCO', 'PORTADOR DE DOENCAS CROMOSSOMICAS OU ESTADO DE FRAGILIDADE IMUNO', 'CLASSIFICACAO FINAL', 'INVESTIGACAO CONCLUIDA', 'ESTADO DO TESTE', 'CBO', 'DATA DA COLETA DO TESTE', 'IDADE EM ANOS', 'TIPO IDADE', 'TIPO DE TESTE', 'RESULTADO DO TESTE', 'SEXO', 'ESTADO DE RESIDENCIA', 'MUNICIPIO DE RESIDENCIA', 'BANCO', 'RACA/COR', 'EPIDEMIA']
