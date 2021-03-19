import importlib, inspect
from system import utils


def launch():
    app_name = input("Enter the name of the app you want to test.\nEnter nothing to exit.\n>")
    if app_name == "":
        from system import homepage
        homepage.launch()
    try:
        app = importlib.import_module(f"testing.{app_name}")
        if not inspect.isfunction(app.launch):
            raise Exception("WRONG_TYPE")
    except ModuleNotFoundError:
        print("Invalid app.")
        return launch()
    except AttributeError:
        print("App has no `launch` function!")
        from system import homepage
        return homepage.launch()
    except Exception as err:
        if Exception.__str__() == "WRONG_TYPE":
            print("`launch` must be a function!")
            from system import homepage
            homepage.launch()
        print(err)
        from system import homepage
        return homepage.launch()
