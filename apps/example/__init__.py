import sys
sys.path.append("../")


def launch():
    while True:
        choice = input("Enter 1 to execute initial code\nEnter anything else to quit\n>")
        if choice == "1":
            return execute_initial_code()
        else:
            from apps import homepage
            return homepage.launch()


def execute_initial_code():
    print("Hello World")
    return launch()
