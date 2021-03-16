
import json
config = json.loads("config.json")

def is_noun(w):
    return(not is_adv(w) and not is_spec(w))

def is_adj(w):
    return(not is_adv(w) and not is_spec(w))

def is_spec(w):
    return(w in config["spec"])

def is_adv(w):
    return(w.endswith("ly") or w in config["adv"])

def is_verb(w):
    # "Biscuit him!" is applicable if you have a giant biscuit you use to immobilize prisoners
    return True

class VerbPhrase:
    def __init__(self,verb,spec={}):
        self.verb = verb
        self.spec = spec
    def __getattr__(self,attr):
        try:
            return super().__getattr__(attr)
        except AttributeError as e:
            try:
                return self.spec[attr]
            except IndexError:
                raise e

class NounPhrase:
    def __init__(self,noun,adj=[]):
        self.noun = noun
        self.adj = adj

def parse_noun_phrase(w):
    try:
        return int(w)
    except ValueError:
        if w.startswith("'"):
            return w
       	else:
            adj = []
            while len(w) > 1 and w[0] in ADJ and (w[1] in NOUN or w[1][0].isupper()):
                adj.append(parse_adj(w))
            if w[0] in NOUN:
                return NounPhrase(w.pop(0),adj)
            else:
                raise Exception("Cannot parse noun phrase: does not end with noun")

def parse_verb_phrase(w):
    adv = []
    adj = {}

    while w[0] in ADV:
        adv.append(w.pop(0))

    verb = w.pop(0)

    while w:
        spec = parse_spec(w)
        phrase = parse_noun_phrase(w)
        specs[spec] = phrase

    return VerbPhrase(verb,specs)

def launch():
    choice = gui.choice("Verb phrase test","Noun phrase test", "Word diagnostics")
    if choice == 0:
        while True:
            print(parse_verb_phrase(input("Phrase? ")))
    elif choice == 1:
        while True:
            print(parse_noune_phrase(input("Phrase? ")))
    elif choice == 2:
        while True:
            word = input("Word? ")
            if word in NOUN:
                print("noun",end="")
            if word in ADJ:
                print("adj",end="")
            if word in ADV:
                print("adv",end="")
            if word in VERB:
                print("verb",end="")
            print()


def tokenize(line):
    return line.split(" ")

if __name__ == "__main__":
    launch()