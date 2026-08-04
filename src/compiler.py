from parser import Parser
from codegen import CCodeGenerator
import sys

parser = Parser(open(sys.argv[1]).read())
ast = parser.parse()
codegenerator = CCodeGenerator()

with open('output.c', 'w') as f:
    f.write(codegenerator.generate(ast))
    f.close()
