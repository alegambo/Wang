"""
    Tests Wang Parser
    See grammar/Wang.g4
    based on jszheng git https://github.com/jszheng/py3antlr4book Example calc
    Extended by loriacarlos@gmail.com
    
"""
"""
    Tests Wang Parser
    See grammar/Wang.g4
    based on jszheng git https://github.com/jszheng/py3antlr4book Example calc
    Extended by loriacarlos@gmail.com
    
"""
__author__ = 'jszheng'
__coauthor__ = 'loriacarlos@gmail.com'

import sys

from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener, ConsoleErrorListener
from antlr4.InputStream import InputStream
from wang.parser.grammar.WangLexer import WangLexer
from wang.parser.grammar.WangParser import WangParser
from wang.src.visitor import WangPrintVisitor
from wang.lib.proof import *

class MyErrorListener(ErrorListener):
    """
        Based on https://stackoverflow.com/questions/18132078/handling-errors-in-antlr4
    """
    def syntaxError(self,  recognizer, 
                            offendingSymbol,
                            line, 
                            charPositionInLine,
                            msg, 
                            e):
        error_msg = f"{self.__class__.__name__}: line {line}: {charPositionInLine} {msg}"
        raise SyntaxError(error_msg)

def evaluacion(to_parse_line):				

    input_stream = InputStream(to_parse_line)
        
    # Setup Lexer 
    print(f"Data:\n{input_stream}")
    lexer = WangLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    #Setup Parser (and own ErrorListener)
    parser = WangParser(token_stream)
    parser.removeErrorListeners()
    parser.addErrorListener(MyErrorListener())
    try:
        tree = parser.assertion()
    except SyntaxError as e:
        print(e.msg)
        sys.exit(-1)
    #Setup the Visitor and visit Parse tree
    visitor = WangPrintVisitor()
    print("*** Starts visit of data ***")
    aaa = visitor.visit(tree)
    print(f"\n Ret:",aaa)
    return aaa	
    
