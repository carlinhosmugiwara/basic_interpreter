# This file contains the set of rules of basic

# defining the constants
DIGITS = '0123456789'

# defining the token types
TOKEN_INT = 'INT'
TOKEN_FLOAT = 'FLOAT'
TOKEN_PLUS = 'PLUS'
TOKEN_MULTI = 'MUL'
TOKEN_MINUS = 'MINUS'
TOKEN_DIVIDE = 'DIV'
TOKEN_LPAREN = 'LPAREN' # left parenthesis
TOKEN_RPAREN = 'RPAREN' # right parenthesis

# positions class
class Position:
    def __init__(self, indx, line, column, file_name, file_txt):
        self.indx = indx
        self.line = line
        self.column = column
        self.file_name = file_name
        self.file_txt = file_txt
    def go_through(self, current_char):
        self.indx += 1
        self.column += 1 

        if(current_char == '\n'):
            self.line += 1
            self.column = 0

        return self
    
    def copy(self):
        return Position(self.indx, self.line, self.column, self.file_name, self.file_txt)

# error class
class Error:
    def __init__(self, position_start, position_end, name, description):
        self.position_start = position_start
        self.position_end = position_end
        self.name = name # name of the error
        self.description = description # description for you to know how to fix it
    
    def error_message(self):
        message = f'{self.name}: {self.description}'
        message += f'File {self.position_start.file_name}, line {self.position_start.line + 1}'
        return message 

# class to define the illegal character error
class IllegalCharError(Error): # usging inheritance here for better organization
    def __init__(self, position_start, position_end, description):
        super().__init__(position_start, position_end, 'Illegal Character', description)





# defining the architecture of the token and how it's gonna be handled
class Token:
    def __init__(self, the_type, value=None): # type is a reserved word, so make to not put exactly type here
        self.type = the_type
        self.value = value

    def __repr__(self):
        if self.value: return str(f'{self.type}:{self.value}')
        return f'{self.type}'

# defining the lexer, they give meaning to the tokens through the programming language's set of rules 
class Lexer:
    def __init__(self, file_name, txt):
        self.file_name = file_name
        self.txt = txt
        self.position = Position(-1, 0, -1, file_name, txt) # we start at -1, because the advance function is gonna increment the index immediatly
        self.current_char = None
        self.next_char()

    # defining function to iterate through every character
    def next_char(self):
        self.position.go_through(self.current_char)
        self.current_char = self.txt[self.position.indx] if self.position.indx < len(self.txt) else None
    
    # defining function to create token based on the rules of basic
    def create_tokens(self):
        tokens = [] # list of tokens
        
        while self.current_char != None:
            if (self.current_char in '\t'):
                self.next_char()
            elif(self.current_char in DIGITS): 
                tokens.append(self.create_num())

            # giving identity to the arithmetic operators
            # from here            
            elif(self.current_char == '+'):
                tokens.append(Token(TOKEN_PLUS))
                self.next_char()

            elif(self.current_char == '-'):
                tokens.append(Token(TOKEN_MINUS))
                self.next_char()

            elif(self.current_char == '*'):
                tokens.append(Token(TOKEN_MULTI))
                self.next_char()

            elif(self.current_char == '/'):
                tokens.append(Token(TOKEN_DIVIDE))
                self.next_char()

            elif(self.current_char == '('):
                tokens.append(Token(TOKEN_LPAREN))
                self.next_char()

            elif(self.current_char == ')'):
                tokens.append(Token(TOKEN_RPAREN))
                self.next_char()
            # to here

            elif(self.current_char == ' '): # making it possible to use spaces
                self.next_char()
            
            
            else:
                # Throwing error
                position_start = self.position.copy()
                illegal_char = self.current_char
                self.next_char()
                return [], IllegalCharError(position_start, self.position,  "'" + illegal_char + "'")
        
        return tokens, None
    
    # set of rules to deal with numbers
    def create_num (self):
        num_string = ''
        has_dot = False # has_dot is to define the number as an integer or float

        while self.current_char != None and self.current_char in DIGITS + '.':
            if(self.current_char == '.'):
                if(has_dot): break 
                has_dot = True
                num_string += '.' 
            
            else:
                num_string += self.current_char
            self.next_char()
        
        if(not has_dot): return Token(TOKEN_INT, int(num_string))
        else: return Token(TOKEN_FLOAT, float(num_string))

def run(file_name, txt):
    lexer = Lexer(file_name, txt)
    tokens, error = lexer.create_tokens()

    return tokens, error
