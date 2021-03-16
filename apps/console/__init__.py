
from ..english import parse, VerbPhrase
from .. import english
from os import path
from glob import glob

def launch():
    while True:
        print(run_line(ask()))

def ask():
    return input("\t")

def run_line(line):
    data = parse(line)
    if not isinstance(data,VerbPhrase):
        raise Exception(f"'{response}' is not a verb phrase")

    matches = glob(path.join(BIN,f"{data.verb}.(py|rosa)"))
    if not matches:
        raise Exception(f"Could not find '{data.verb}.py' or '{data.verb}.rosa' in {BIN}")

    for match in matches:
        if match.endswith(".py"):
            if account.is_admin():
                os.system(f"python3 {match}")
            else:
                raise Exception("Cannot run .py files without admin permissions.")
        else:
            run_file(match)

def run_text(text):
    for l in text.split("\n"):
        run_line(l)

def run_file(path):
    run_text(util.read(path))
