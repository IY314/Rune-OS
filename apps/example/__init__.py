import sys
sys.path.append("../")


def launch():
    choice = input("Enter 1 to execute initial code\nEnter anything else to quit\n>")
    if choice == "1":
        execute_initial_code()
    else:
        from apps import homepage
        homepage.launch()


def execute_initial_code():
    print("Hello World")
