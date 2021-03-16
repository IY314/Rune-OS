from apps import account, dev_info

def launch(dev=False):
    dev_info.print()
    print("Booting up...")
    account.login(dev)


if __name__ == "__main__":
    launch()
