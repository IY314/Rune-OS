from apps import account


def launch(dev=False):
    print("RUNE OS ALPHA 3.2.3")
    print("Booting up...")
    account.login(dev)


if __name__ == "__main__":
    launch()
