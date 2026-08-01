INT         = 'INT'
FLOAT       = 'FLOAT'
PLUS        = 'PLUS'
MINUS       = 'MINUS'
EOF         = 'EOF'

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'


class Position:
    def __init__(self, idx, ln, col):
        self.idx = idx
        self.ln = ln
        self.col = col

    def advance(self, char=None):
        self.idx += 1
        self.col += 1

        if char == '\n':
            self.ln += 1
            self.col = 1


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = Position(-1, 0, 0)
        self.char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.char)

        if self.pos.idx < len(self.text):
            self.char = self.text[self.pos.idx]
        else:
            self.char = None

    def tokenize(self):
        tokens = []

        while self.char is not None:
            if self.char in " \t\n":
                self.advance()
            elif self.char.isdigit():
                tokens.append(self.ret_number())
            elif self.char == "+":
                tokens.append(Token(PLUS))
                self.advance()
            elif self.char == "-":
                tokens.append(Token(PLUS))
                self.advance()
            else:
                raise Exception("Unknown token.")

        tokens.append(Token(EOF))
        return tokens

    def ret_number(self):
        num = ""
        dots = 0

        while self.char is not None and (self.char.isdigit() or self.char == "."):
            if self.char == ".":
                if dots == 1:
                    raise Exception("Can't have more than one dot in a number.")
                num += '.'
            else:
                num += self.char
            self.advance()

        if num.startswith(".") or num.endswith("."):
            raise Exception("Invalid floating point.")

        if dots == 0:
            return Token(INT, int(num))
        else:
            return Token(FLOAT, float(num))


def lexer_main(text):
    lexer = Lexer(text)
    return lexer.tokenize()
