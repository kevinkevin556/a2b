def green(string):
    return "\033[92m" + string + "\033[0m"

def yellow(string):
    return "\033[93m" + string + "\033[0m"

def red(string):
    return "\033[91m" + string + "\033[0m"

def get_update_message(link, title, journal, year):
    return f" {green('*')} {link} = {yellow(title)+'.'} {journal}, {red(str(year))} "

def prompt(msg):
    print(green(msg))