#TODO: not implemented yet
def linecount(code):
    return len(code)

def replace(code, pattern, str_to_replace):
    new_command = []
    for command in code:
        command = command.replace(pattern, str_to_replace)
        new_command.append(command)
    return new_command

def print_code(code):
    for command in code:
        print(command)