__author__ = 'jszheng'
__coauthor__ = 'loriacarlos@gmail.com'

from wang.parser.grammar.WangVisitor import WangVisitor
from wang.parser.grammar.WangParser import WangParser
from wang.lib.proof import *

"""
    Tests Wang Visitor
    See grammar/Wang.g4
    based on jszheng git https://github.com/jszheng/py3antlr4book
    Example calc
"""
class WangPrintVisitor(WangVisitor):
    def __init__(self):
        pass
    
    def visitAssertion(self,ctx):
        return self.visit(ctx.formula(0))
        
    def visitFormExpr(self, ctx):
       # print(f'\nStart Visiting FormExpr (=>) {len(ctx.sequence())} children')
        #children = ctx.sequence()
        res_left = self.visit(ctx.premises())
        res_right = self.visit(ctx.conclusions())
        if res_left == None:
            res_left = []
        #return Deduction(self.visit(children[0]),self.visit(children[1]))
        return Deduction(res_left,res_right)
    
    def visitPremises(self, ctx):
        return self.visit(ctx.sequence())

    def visitConclusions(self, ctx):
        return self.visit(ctx.sequence())
    
    def visitSeqExpr(self, ctx):
        print(f'Visiting SeqExpr (,) with {len(ctx.expr())} children')
        children = ctx.expr()
        #for ch in children:
        #    self.visit(ch)
        return [self.visit(ch) for ch in children]
    
    def visitId(self, ctx):
        name = ctx.ID().getText()
        print(f'Visiting Id={name}')
        return Atom(f'{name}')

    def visitAndExpr(self, ctx):
        print('Visiting AndExpr (&)')
        res_left = self.visit(ctx.expr(0))
        res_right = self.visit(ctx.expr(1))
        return And(res_left, res_right)
    
    def visitImplyExpr(self, ctx):
        print('Visiting ImplyExpr (->)')
        res_left = self.visit(ctx.expr(0))
        res_right = self.visit(ctx.expr(1))
        return Then(res_left,res_right)

    def visitOrExpr(self, ctx):
        print('Visiting OrExpr (|)')
        res_left = self.visit(ctx.expr(0))
        res_right = self.visit(ctx.expr(1))
        return Or(res_left, res_right)
       

    def visitParens(self, ctx):
        print('Visiting ParenExpr (...)')
        only = self.visit(ctx.expr())
        return only

    def visitNotExpr(self, ctx):
        print('Visiting NotExpr (~) ')
        return Not(self.visit(ctx.expr()))
        

    
