import re

class ArraySyntax:
    def __init__(self):
        self.tokens = []
        self.current_token_index = 0

    def tokenize(self, code):
        """
        Tokenize the input code based on predefined patterns for terminals.
        Each terminal is assigned a token type.
        """
        token_patterns = [
            (r'\bint\b', 'TYPE_INT'),
            (r'\bfloat\b', 'TYPE_FLOAT'),
            (r'\bstring\b', 'TYPE_STRING'),
            (r'[a-zA-Z_]\w*', 'VAR'),  # Matches identifiers like arr, myArray, my_Array, and etc.
            (r'\b\d+\b', 'NUM'),       # Matches numeric literals
            (r'\[', 'LBRACKET'),
            (r'\]', 'RBRACKET'),
            (r'\{', 'LBRACE'),
            (r'\}', 'RBRACE'),
            (r'\,', 'COMMA'),
            (r'\;', 'SEMICOLON'),
            (r'\=', 'EQUAL'),
        ]

        token_regex = '|'.join(f'(?P<{pair[1]}>{pair[0]})' for pair in token_patterns)

        for match in re.finditer(token_regex, code):
            token_type = match.lastgroup
            token_value = match.group(token_type)

            if token_type in ('TYPE_INT', 'TYPE_FLOAT', 'TYPE_STRING'):
                token_type = 'TYPE'

            self.tokens.append((token_type, token_value))

        self.tokens.append(('EOF', 'EOF'))


    def match(self, expected_type):
        """
        Matches the current token with the expected token type.
        If matched, moves to the next token; otherwise, raises an error.
        """
        if self.tokens[self.current_token_index][0] == expected_type:
            self.current_token_index += 1
        else:
            self.error(f"Expected {expected_type}, found {self.tokens[self.current_token_index][1]}")

    def match_sequence(self, sequence):
        """
        Matches a sequence of token types.
        """
        for token_type in sequence:
            self.match(token_type)

    def error(self, message):
        """
        Raises a syntax error with the provided message.
        """
        raise SyntaxError(f"Syntax error: {message}")

    def parse(self):
        """
        Entry point for parsing. Starts parsing the program.
        """
        self.Program()

    def Program(self):
        """
        Program -> (ArrayDecl | ArrayAssign | ArrayAccess)+
        Represents the entire program.
        """
        while self.tokens[self.current_token_index][0] != 'EOF':
            # Try to match one of the three top-level constructs
            if self.tokens[self.current_token_index][0] == 'TYPE':
                self.ArrayDecl()
            elif self.tokens[self.current_token_index][0] == 'VAR':
                if self.tokens[self.current_token_index + 1][0] == 'EQUAL':
                    self.ArrayAssign()
                elif self.tokens[self.current_token_index + 1][0] == 'LBRACKET':
                    self.ArrayAccess()
                else:
                    self.error("Expected '=' or '[', found {}".format(self.tokens[self.current_token_index + 1][1]))
            else:
                self.error("Unexpected token: {}".format(self.tokens[self.current_token_index][1]))


    def ArrayDecl(self):
        """
        ArrayDecl -> Type VAR '[' NUM ']' ';'
        Represents the declaration of an array.
        """
        self.match_sequence(['TYPE', 'VAR', 'LBRACKET', 'NUM', 'RBRACKET', 'SEMICOLON'])


    def ArrayAssign(self):
        """
        ArrayAssign -> var '=' '{' NumList '}' ';'
        Represents the initialization of an array with a list of values.
        """
        self.match('VAR')
        self.match('EQUAL')
        self.match('LBRACE')
        self.NumList()
        self.match_sequence(['RBRACE', 'SEMICOLON'])

    def ArrayAccess(self):
        """
        ArrayAccess -> var '[' num ']' '=' Expr ';'
        Represents accessing an array element and assigning a value to it.
        """
        self.match_sequence(['VAR', 'LBRACKET', 'NUM', 'RBRACKET', 'EQUAL', 'NUM', 'SEMICOLON'])

    def NumList(self):
        """
        NumList -> num | num ',' NumList
        Represents a list of numbers separated by commas.
        """
        self.match('NUM')
        while self.tokens[self.current_token_index][0] == 'COMMA':
            self.match_sequence(['COMMA', 'NUM'])


if __name__ == "__main__":
    print("Enter your program (end with an empty line):")
    user_input = []
    while True:
        line = input()
        if line.strip() == "":
            break
        user_input.append(line)
    code = "\n".join(user_input)

    # Initialize the syntax checker
    checker = ArraySyntax()
    try:
        checker.tokenize(code)   
        checker.parse()          # Parse input
        print("Syntax is valid!")  # If no errors, syntax is valid
    except SyntaxError as e:
        print(e)  # Print the syntax error
