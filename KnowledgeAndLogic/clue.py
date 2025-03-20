from logic import *
import termcolor
import random as rd

mA = Symbol("mA")
mB = Symbol("mB")
mC = Symbol("mC")
m = [mA, mB, mC]

rA = Symbol("rA")
rB = Symbol("rB")
rC = Symbol("rC")
r = [rA, rB, rC]

wA = Symbol("wA")
wB = Symbol("wB")
wC = Symbol("wC")
w = [wA, wB, wC]

knowledge = And(
    Or(mA, mB, mC), Or(rA, rB, rC), Or(wA, wB, wC),
)

symbols = m + r + w

def check_knowledge(knowledge):
    for symbol in symbols:
        if model_check(knowledge, symbol):
            termcolor.cprint(f"{symbol}:YES","green")
        elif not model_check(knowledge, Not(symbol)):
            termcolor.cprint(f"{symbol}:MAYBE","yellow")
print("Knowledge:", knowledge.formula())

mA = rd.choice(m)
rA = rd.choice(r)
wA = rd.choice(w)

m.remove(mA)
r.remove(rA)
w.remove(wA)

s = [m,r,w]

cardM1 = rd.choice(m)
cardR1 = rd.choice(r)
cardW1 = rd.choice(w)

cards = [cardM1, cardR1, cardW1]
m.remove(cardM1)
r.remove(cardR1)
w.remove(cardW1)

cD = rd.choice(rd.choice(s))
cardM2 = rd.choice(m)
cardR2 = rd.choice(r)
cardW2 = rd.choice(w)

cards2 = [cardM2, cardR2, cardW2]
m.remove(cardM2)
r.remove(cardR2)
w.remove(cardW2)

knowledge.add(Or(Not(cardM2), Not(cardR2), Not(cardW2)))
knowledge.add(Not(cD))

knowledge.add(Not(cardM1))
knowledge.add(Not(cardR1))
knowledge.add(Not(cardW1))

# Select one card that someone has
known_card1 = rd.choice(cards2)
known_card2 = rd.choice([card for card in cards2 if card != known_card1])

# Add the known card to the knowledge base
knowledge.add(Not(known_card1))
knowledge.add(Not(known_card2))

# Print the known card
termcolor.cprint(f"Known cards: {known_card1}, {known_card2}", "blue")

check_knowledge(knowledge)