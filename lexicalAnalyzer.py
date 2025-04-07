#Project 1: programming a lexical analyzer 
#Eugenio Guzman Vargas A01621084
#Ilan 
#Ximena 



# Transition table based on the automaton design
transition_table = {
    "initial": {"digits": "integer", "letters": "variable", "=": "assignment",
                "+": "sum", "-": "subtract", "*": "product", "/": "division",
                "(": "left parenthesis", ")": "right parenthesis"}, #Starts in the initial state and transitions to the corresponding state after reading a character
    "integer": {"digits": "integer", ".": "float"},#If an integer is read, it checks for more consecutive integers or a decimal point, becase +1 digit number and float numbers shouldnt be broken down into single digits
    "float": {"digits": "float"},#float numbers with more than one decimal digit
    "variable": {"letters": "variable"},#this transition ensures that multi-letter variables are read as a whole
    "assignment": {}, 
    "sum": {},
    "subtract": {},
    "product": {},
    "division": {},
    "left parenthesis": {},
    "right parenthesis": {} #for the rest of token classifications, once they are read, the next token is processed starting in the initial state
}


# Auxiliary function to determine the type of character
def get_char_type(char):
    if char.isdigit():
        return "digits"
    if char.isalpha():
        return "letters"
    return char  #if the token is a symbol, it is returned as so, because thats the only thing the transition table needs

# Main lexical analyzer function
def lexer(filepath):
    with open(filepath, "r") as file:
        content = file.read() #one single string stream for the whole file 

    tokens = [] # list of tuples for tokens and states
    state = "initial" # the state of the automaton
    buffer = "" # temporary storage for the current token

    for char in content:
        char_type = get_char_type(char)

        if char.isspace():
            if buffer:
                tokens.append((buffer, state))
                buffer = ""
                state = "initial"
            continue #if there is a space between characters, it means the token has ended and it resets to the initial state and restarts the buffer

        if char_type in transition_table[state]:
            state = transition_table[state][char_type]
            buffer += char #if the type of the current token is a valid transition (two consecutive letters, for example), it holds on to that token
        else: #if not, the token has ended
            if buffer:
                tokens.append((buffer, state))#the current token in the buffer and the current state are added to the list
            state = "initial"
            buffer = "" #both token and buffer are restarted
            if char_type in transition_table[state]:
                state = transition_table[state][char_type]
                buffer += char#the current token, which must be a different one to the one that was just stored, is now processed

    if buffer:
        tokens.append((buffer, state))#this solves the problem of losing the last token if the txt ends with a space

    print_tokens(tokens)

# Auxiliary function for result printing
def print_tokens(tokens):
    print("Token\tType")
    print("-" * 20)
    for token, token_type in tokens:
        print(f"{token}\t{token_type}")



# Run the program
lexer("expressions.txt")
