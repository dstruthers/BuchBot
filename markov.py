import re
from random import randint

markov_data = []

def process_text(text):
    markov_data.append(filter(lambda x: x != '', re.split(r'[\.,;\?!\s\"]+', text)))

def markov_chain(length=32, order=2):
    chunks = []
    for d in markov_data:
        for i in range(0, len(d) - order + 1):
            chunks.append(d[i:i+order])

    chain = chunks[randint(0, len(chunks) - 1)]

    while len(chain) < length:
        tail = chain[-(order - 1):]

        def eligible(chunk):
            ihead = map(lambda x: x.upper(), chunk[0:order - 1])
            itail = map(lambda x: x.upper(), tail)
            return ihead == itail

        eligible_chunks = filter(eligible, chunks)

        if len(eligible_chunks) == 0:
            break

        chain.append(eligible_chunks[randint(0, len(eligible_chunks) - 1)][-1])
    
    sentence = ' '.join(chain)
    return sentence[0].upper() + sentence[1:]
