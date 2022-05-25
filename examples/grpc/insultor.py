from random import seed
from random import randint

l = ['fortnite player', 'mumble rapper']

seed(1)

def addInsult(s):
    l.append(s)

def getInsults():
    return l

def insultMe():
    return l[randint(0, len(l) - 1)]