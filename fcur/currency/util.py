import datetime

def previous_day(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    date = date - datetime.timedelta(days=1)
    return date.strftime("%Y-%m-%d")

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
