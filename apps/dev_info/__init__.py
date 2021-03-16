
def get():
    with open("version.txt") as f:
        return f.read()

def print():
    print(get())