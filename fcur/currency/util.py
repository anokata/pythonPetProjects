
def get_growth_symbol(difference):
        if difference > 0:
            return "+"
        elif difference < 0:
            return "-"
        else:
            return "0"

def log(fun):
    def logger(*args):
        print(fun.__name__, " @ ", args, end=' ---> ')
        result = fun(*args)
        print(result)
        return result
    return logger
