"""
Prototipo de modelo de objetos para Wang
loriacarlos@gmail.com
@since II-2018
"""


from enum import Enum, auto
from abc import ABCMeta, abstractmethod
from wang.lib.deduction import *
from wang.lib.formula import *
import wang.lib.utils

class RuleType(Enum):
    AXIOM = auto()
    OR_LEFT = auto()
    OR_RIGHT = auto()
    AND_LEFT = auto()
    AND_RIGHT = auto()
    NOT_LEFT =auto()
    NOT_RIGHT=auto()
    EQUIV = auto()

class Just:
    def __init__(self, subject, rule):
        self.subject = subject
        self.rule = rule
        
class Rule(metaclass=ABCMeta):
    def __init__(self, ruletype):
        self.__ruletype = ruletype
    @abstractmethod
    def apply(self, deduction): pass
    @property
    def kind(self):
        return self.__ruletype

class Axiom(Rule):
    def __init__(self):
        super().__init__(RuleType.AXIOM)
    
    def apply(self, deduction):
        for (pi, p) in enumerate(deduction.left):
            if p in deduction.right:
                yield (self.kind, pi, deduction)
        for (pi, p) in enumerate(y for y in deduction.left if isinstance(y, Not)):#soporta negativos
            if p.left in (y.left for y in deduction.right if isinstance(y, Not)):
                yield (self.kind, pi, deduction)
            

class EquivLeft(Rule):
    def __init__(self):
        super().__init__(RuleType.EQUIV)
    def apply(self, deduction):
        for (i, f) in enumerate(deduction.left):
            if isinstance(f, Then):
                newleft = wang.lib.utils.replace(deduction.left, i, [f.weak_nf()])
                yield (self.kind, i, Deduction(list(newleft),deduction.right))
            else:
                if hasattr(f, 'right'):#busca si aplica en el subarbol de la derecha
                    for g in Equiv_RULE_LEFT.apply(Deduction([f.right],deduction.right)):
                        for newf in updateBranch(f,g,1,0,deduction): 
                            newleft = wang.lib.utils.replace(deduction.left,i,[newf[2].left])
                            yield (self.kind,f"{i}-{newf[1]}", Deduction(list(newleft),deduction.right))
                if hasattr(f, 'left'):#busca si aplica en el subarbol de la izquierda
                    for g in Equiv_RULE_LEFT.apply(Deduction([f.left],deduction.right)):
                        for newf in updateBranch(f,g,0,0,deduction):#actualiza f y retorna
                            newleft = wang.lib.utils.replace(deduction.left,i,[newf[2].left])
                            yield (self.kind,f"{i}-{newf[1]}", Deduction(list(newleft),deduction.right))
class EquivRight(Rule):
    def __init__(self):
        super().__init__(RuleType.EQUIV)
    def apply(self, deduction):
        for (i, f) in enumerate(deduction.right):
            if isinstance(f, Then):
                newright = wang.lib.utils.replace(deduction.right, i, [f.weak_nf()])
                yield (self.kind, i, Deduction(deduction.left, list(newright)))
            else:
                if hasattr(f, 'right'):#busca si aplica en el subarbol de la derecha
                    for g in Equiv_RULE_RIGHT.apply(Deduction(deduction.left,[f.right])):
                        for newf in updateBranch(f,g,1,1,deduction): 
                            newright = wang.lib.utils.replace(deduction.right,i,[newf[2].right])
                            yield (self.kind,f"{i}-{newf[1]}", Deduction(deduction.left,list(newright)))
                if hasattr(f, 'left'):#busca si aplica en el subarbol de la izquierda
                    for g in Equiv_RULE_RIGHT.apply(Deduction(deduction.left,[f.left])):
                        for newf in updateBranch(f,g,0,1,deduction):#actualiza f y retorna
                            newright = wang.lib.utils.replace(deduction.right,i,[newf[2].right])
                            yield (self.kind,f"{i}-{newf[1]}", Deduction(deduction.left,list(newright)))


class AndLeft(Rule):
    def __init__(self):
        super().__init__(RuleType.AND_LEFT)
    def apply(self, deduction):
        if not isinstance(deduction.left, Atom):#si no es un atomo
            for (i,f) in enumerate(deduction.left):
                if isinstance(f, And):
                    newleft = wang.lib.utils.replace(deduction.left,i,[f.left,f.right])
                    yield (self.kind,i, Deduction(list(newleft), deduction.right))
                elif 0:  # desabilitado porque el and left solo puede ocurrir en la raiz?
                    if hasattr(f, 'right'):#busca si aplica en el subarbol de la derecha
                        for g in AND_LEFT_RULE.apply(Deduction([f.right],deduction.right)):
                            for newf in updateBranch(f,g,1,0,deduction): 
                                newleft = wang.lib.utils.replace(deduction.left,i,[newf[2].left])
                                yield (self.kind,f"{i}-{newf[1]}", Deduction(list(newleft), deduction.right))
                    if hasattr(f, 'left'):#busca si aplica en el subarbol de la izquierda
                        for g in AND_LEFT_RULE.apply(Deduction([f.left],deduction.right)):
                            for newf in updateBranch(f,g,0,0,deduction):#actualiza f y retorna
                                newleft = wang.lib.utils.replace(deduction.left,i,[newf[2].left])
                                yield (self.kind,f"{i}-{newf[1]}", Deduction(list(newleft), deduction.right))

class AndRight(Rule):
    def __init__(self):
        super().__init__(RuleType.AND_RIGHT)
    def apply(self, deduction):
        if not isinstance(deduction.right, Atom):#si no es un atomo
            for (i,f) in enumerate(deduction.right):
                if isinstance(f, And):#caso en el que se aplica
                    newright1 = wang.lib.utils.replace(deduction.right,i,[f.left])
                    newright2 = wang.lib.utils.replace(deduction.right,i,[f.right])
                    yield (self.kind,i,Deduction(deduction.left,list(newright1)), 
                                       Deduction(deduction.left,list(newright2)))
                else:
                        if hasattr(f, 'right'):#busca si aplica en el subarbol de la derecha
                            for g in AND_RIGHT_RULE.apply(Deduction(deduction.left,[f.right])):
                                for newf in updateBranch(f,g,1,1,deduction):
                                    newright1 = wang.lib.utils.replace(deduction.right,i,[newf[2].right])
                                    newright2 = wang.lib.utils.replace(deduction.right,i,[newf[3].right])
                                    yield (self.kind,f"{i}-{newf[1]}", 
                                           Deduction(deduction.left,list(newright1)),
                                           Deduction(deduction.left,list(newright2))) 
                        if hasattr(f, 'left'):#busca si aplica en el subarbol de la izquierda
                            for g in AND_RIGHT_RULE.apply(Deduction(deduction.left,[f.left])):
                                for newf in updateBranch(f,g,0,1,deduction):#nuevo f 
                                    newright1 = wang.lib.utils.replace(deduction.right,i,[newf[2].right])
                                    newright2 = wang.lib.utils.replace(deduction.right,i,[newf[3].right])
                                    yield (self.kind,f"{i}-{newf[1]}", 
                                           Deduction(deduction.left,list(newright1)),
                                           Deduction(deduction.left,list(newright2))) 

class OrLeft(Rule):#p|q=>p  ==  p=>p  q=>p
    def __init__(self):
        super().__init__(RuleType.OR_LEFT)
    def apply(self, deduction):
        if not isinstance(deduction.left, Atom):#si no es un atomo
            for (i,f) in enumerate(deduction.left):
                if isinstance(f, Or):
                    newleft1 = wang.lib.utils.replace(deduction.left,i,[f.left])
                    newleft2 = wang.lib.utils.replace(deduction.left,i,[f.right])
                    yield (self.kind,i,Deduction(list(newleft1),deduction.right), 
                                       Deduction(list(newleft2),deduction.right))
                else:# quitar si se quiere que se aplique en todos los logares posibles
                    if hasattr(f, 'right'):#busca si aplica en el subarbol de la derecha
                        for g in OR_LEFT_RULE.apply(Deduction([f.right],deduction.right)):
                            for newf in updateBranch(f,g,1,0,deduction):
                                newleft1 = wang.lib.utils.replace(deduction.left,i,[newf[2].left])
                                newleft2 = wang.lib.utils.replace(deduction.left,i,[newf[3].left])
                                yield (self.kind,i,Deduction(list(newleft1),deduction.right), 
                                                   Deduction(list(newleft2),deduction.right))
                    if hasattr(f, 'left'):#busca si aplica en el subarbol de la izquierda
                        for g in OR_LEFT_RULE.apply(Deduction([f.left],deduction.right)):
                            for newf in updateBranch(f,g,0,0,deduction):
                                newleft1 = wang.lib.utils.replace(deduction.left,i,[newf[2].left])
                                newleft2 = wang.lib.utils.replace(deduction.left,i,[newf[3].left])
                                yield (self.kind,i,Deduction(list(newleft1),deduction.right), 
                                                   Deduction(list(newleft2),deduction.right))

class OrRight(Rule):
    def __init__(self):
        super().__init__(RuleType.OR_RIGHT)
    def apply(self, deduction):
        if not isinstance(deduction.right, Atom):#si no es un atomo
            for (i,f) in enumerate(deduction.right):
                if isinstance(f, Or):
                        newright = wang.lib.utils.replace(deduction.right,i,[f.left,f.right])
                        yield (self.kind,i, Deduction(deduction.left,list(newright)))
                elif 0: # desabilitado porque solo aplica para la raiz
                        if hasattr(f, 'right'):#busca si aplica en el subarbol de la derecha
                            for g in OR_RIGHT_RULE.apply(Deduction(deduction.left,[f.right])):

                                yield from updateBranch(f,g,1,1,deduction)#actualiza el arbol 
                        if hasattr(f, 'left'):#busca si aplica en el subarbol de la izquierda
                            for g in OR_RIGHT_RULE.apply(Deduction(deduction.left,[f.left])):
                                yield from updateBranch(f,g,0,1,deduction)#actualiza el arbol

class NotLeft(Rule):
    def __init__(self):
        super().__init__(RuleType.NOT_LEFT)
    def apply(self, deduction):
        for (i,f) in enumerate(deduction.left):
            if isinstance(f, Not):
                if isinstance(f.left, Not):
                    newleft = wang.lib.utils.replace(deduction.left,i,[f.left.left])
                    yield (self.kind,i, Deduction(list(newleft), deduction.right))
                elif isinstance(f.left, Or):
                    newleft = wang.lib.utils.replace(deduction.left,i,[And(Not(f.left.left),Not(f.left.right))])
                    yield (self.kind,i, Deduction(list(newleft), deduction.right))
                elif isinstance(f.left, And):
                    newleft = wang.lib.utils.replace(deduction.left,i,[Or(Not(f.left.left),Not(f.left.right))])
                    yield (self.kind,i, Deduction(list(newleft), deduction.right))
            else:  
                if hasattr(f, 'right'):#busca si aplica en el subarbol de la derecha               
                    for g in NOT_LEFT_RULE.apply(Deduction([f.right],deduction.right)):
                        for newf in updateBranch(f,g,1,0,deduction): 
                            newleft = wang.lib.utils.replace(deduction.left,i,[newf[2].left])
                            yield (self.kind,f"{i}-{newf[1]}", Deduction(list(newleft), deduction.right))
                if hasattr(f, 'left'):#busca si aplica en el subarbol de la izquierda
                    for g in NOT_LEFT_RULE.apply(Deduction([f.left],deduction.right)):
                        for newf in updateBranch(f,g,0,0,deduction):#actualiza f y retorna
                            newleft = wang.lib.utils.replace(deduction.left,i,[newf[2].left])
                            yield (self.kind,f"{i}-{newf[1]}", Deduction(list(newleft), deduction.right))


class NotRight(Rule):# De morgans laws + double not
    def __init__(self):
        super().__init__(RuleType.NOT_RIGHT)
    def apply(self, deduction):
        for (i,f) in enumerate(deduction.right):
            if isinstance(f, Not):
                if isinstance(f.left, Not):
                    newright = wang.lib.utils.replace(deduction.right,i,[f.left.left])
                    yield (self.kind,i, Deduction(deduction.left,list(newright)))
                elif isinstance(f.left, Or):
                    newright = wang.lib.utils.replace(deduction.right,i,[And(Not(f.left.left),Not(f.left.right))])
                    yield (self.kind,i, Deduction(deduction.left,list(newright)))
                elif isinstance(f.left, And):
                    newright = wang.lib.utils.replace(deduction.right,i,[Or(Not(f.left.left),Not(f.left.right))])
                    yield (self.kind,i, Deduction(deduction.left,list(newright)))
            else: 
                if hasattr(f, 'right'):#busca si aplica en el subarbol de la derecha               
                    for g in NOT_RIGHT_RULE.apply(Deduction(deduction.left,[f.right])):
                        for newf in updateBranch(f,g,1,1,deduction): 
                            newright = wang.lib.utils.replace(deduction.right,i,[newf[2].right])
                            yield (self.kind,f"{i}-{newf[1]}", Deduction(deduction.left,list(newright)))
                if hasattr(f, 'left'):#busca si aplica en el subarbol de la izquierda
                    for g in NOT_RIGHT_RULE.apply(Deduction(deduction.left,[f.left])):
                        for newf in updateBranch(f,g,0,1,deduction):#actualiza f y retorna
                            newright = wang.lib.utils.replace(deduction.right,i,[newf[2].right])
                            yield (self.kind,f"{i}-{newf[1]}", Deduction(deduction.left,list(newright)))


def first(obj):#fuerza que un objeto ya no sea una lista
    if isinstance(obj, list):
        return obj[0] 
    else: 
        return obj




#            **Advertencia**
#     tratar de entender esta funcion 
#puede producir demencia y depresion temporal
def updateBranch(parent,child,sideFormula,side,original):#para volver a crear el arbol con los cambios
                                                     #parent: nodo que uno de sus hijos sufrió un cambio
                                                     #child: la respuesta de un yeld con el cambio
                                                     #sideFormula: en cual hijo ocurrió el cambio
                                                     #side: enque lado de la deduccion .......
                                                     #original: la deduccion a la que pertenece el parent
    #se eliminan los parentesis cuadrados    
    child1left =  first(child[2].left)
    child1right = first(child[2].right)
    if len(child) ==4:
        child2left =  first(child[3].left)
        child2right = first(child[3].right)
    
    if isinstance(parent, And):
        if sideFormula == 1:#hijo derecho
            a= And(parent.left,child1left) if side == 0 else And(parent.left,child1right)
            if len(child) ==4:# es tres cuando no se divide y 4 cuando se divide
                b= And(parent.left,child2left) if side == 0 else And(parent.left,child2right)
        else:              #hijo izquierdo
            a= And(child1left,parent.right) if side == 0 else And(child1right,parent.right)
            if len(child) ==4:
                b= And(child2left,parent.right) if side == 0 else And(child2right,parent.right)
    elif isinstance(parent, Or):
        if sideFormula == 1:
            a= Or(parent.left,child1left) if side == 0 else Or(parent.left,child1right)
            if len(child) ==4:            
                b= Or(parent.left,child2left) if side == 0 else Or(parent.left,child2right)
        else:
            a= Or(child1left,parent.right) if side == 0 else Or(child1right,parent.right)
            if len(child) ==4:            
                b= Or(child2left,parent.right) if side == 0 else Or(child2right,parent.right)
    elif isinstance(parent, Then):
        if sideFormula == 1:
            a= Then(parent.left,child1left) if side == 0 else Then(parent.left,child1right)
            if len(child) ==4:            
                b= Then(parent.left,child2left) if side == 0 else Then(parent.left,child2right)
        else:
            a= Then(child1left,parent.right) if side == 0 else Then(child1right,parent.right)
            if len(child) ==4:            
                b= Then(child2left,parent.right) if side == 0 else Then(child2right,parent.right)
    elif isinstance(parent, Not):
        a= Not(child1left) if side == 0 else Not(child1right)
        if len(child) ==4:        
            b= Not(child2left) if side == 0 else Not(child2right)
    
    if side ==0:#si es la preposision
        if len(child) ==4:        
            yield (child[0],f"^{sideFormula}-{child[1]}",Deduction(a,original.right),
                                                        Deduction(b,original.right))
        else:
            yield (child[0],f"^{sideFormula}-{child[1]}",Deduction(a,original.right))
    else:       #si es la conclusion
        if len(child) ==4:        
            yield (child[0],f"^{sideFormula}-{child[1]}",Deduction(original.left,a),
                                                        Deduction(original.left,b))
        else:
            yield (child[0],f"^{sideFormula}-{child[1]}",Deduction(*original.left,a))

AXIOM_RULE = Axiom()
Equiv_RULE_LEFT= EquivLeft()
Equiv_RULE_RIGHT= EquivRight()
AND_LEFT_RULE= AndLeft()   
OR_RIGHT_RULE = OrRight()
AND_RIGHT_RULE = AndRight()
OR_LEFT_RULE=OrLeft()
NOT_LEFT_RULE=NotLeft()
NOT_RIGHT_RULE=NotRight()

class ArbolNodo:
    def __init__(self, regla, pos, ded, izq, der):
        self.left = izq
        self.right = der
        self.ded = ded
        self.regla = regla
        self.pos = pos

    def PrintTree(self):
        print("****** Deduc: ",  self.ded)
        print("Regla ", self.regla)
        print("Pos ", self.pos)
        print("Left ",self.left)
        print("Right ",self.right)
        return [self.ded,self.regla,self.pos,self.left,self.right]

    def printRecursive(self):
        self.PrintTree()
        if self.left :
            self.left.printRecursive()
        if self.right :
            self.left.printRecursive()

    def getJsonStr(self):
        if self.left is None:
            leftOut = ""
        else:
            leftOut = f",\"_left\": {self.left.getJsonStr()}"

        if self.right is None:
            rightOut = ""
        else:
            rightOut = f",\"_right\": {self.right.getJsonStr()}"
        return f"{{\"Deduc\":\"{self.ded}\", \"regla\": \"{self.regla}\", \"pos\": \"{self.pos}\"{leftOut}{rightOut}}}  "

    def __str__(self):
        return self.getJsonStr()


def recorrerArbol(ded):

    print("1) Axiom test", ded)
    for f in AXIOM_RULE.apply(ded):
        print(f)
        regla, pos, newDed = f
        return ArbolNodo(regla, pos, ded, None ,None)

    print("2) Equiv_RULE_LEFT Test", ded)
    for f in Equiv_RULE_LEFT.apply(ded):
        print(f)
        regla, pos, newDed = f
        return ArbolNodo(regla, pos, ded,recorrerArbol(newDed),None)

    print("3) Equiv_RULE_RIGHT Test", ded)
    for f in Equiv_RULE_RIGHT.apply(ded):
        print(f)
        regla, pos, newDed = f
        return ArbolNodo(regla, pos, ded, recorrerArbol(newDed), None)

    print("4) Andleft Test", ded)
    for f in AND_LEFT_RULE.apply(ded):
        print(f)
        regla, pos, newDed = f
        return ArbolNodo(regla, pos, ded, recorrerArbol(newDed), None)
         
    print("5) OrRight Test", ded)
    for f in OR_RIGHT_RULE.apply(ded):
        print(f)
        regla, pos, newDed = f
        return ArbolNodo(regla, pos, ded, recorrerArbol(newDed), None)
    
    print("6) NotLeft Test", ded)
    for f in NOT_LEFT_RULE.apply(ded):
        print(f)
        regla, pos, newDed = f
        return ArbolNodo(regla, pos, ded, recorrerArbol(newDed), None)

    print("7) NotRight Test", ded)
    for f in NOT_RIGHT_RULE.apply(ded):
        print(f)
        regla, pos, newDed = f
        return ArbolNodo(regla, pos, ded, recorrerArbol(newDed), None)

    # split
    print("8) AndRight Test", ded)
    for f in AND_RIGHT_RULE.apply(ded):
        print(f)
        regla, pos, fl, fr = f
        return ArbolNodo(regla, pos, ded, recorrerArbol(fl), recorrerArbol(fr))

    print("9) OrLeft Test", ded)
    for f in OR_LEFT_RULE.apply(ded):
        print(f)
        regla, pos, fl, fr = f
        return ArbolNodo(regla, pos, ded, recorrerArbol(fl), recorrerArbol(fr))


if __name__ == "__main__":
    print("*** Testing Proofs ***")
    # t = TRUE
    #f = FALSE
    p = Atom("p")
    q = Atom("q")
    r = Atom("r")
    np=Not(p)
    nnp=Not(np)
    a=And(nnp,p)
    ded = Deduction([Or(Then(p,r),Then(q,r))],[Then(And(p,q),r)])
    print("\n\n************** EL RECORRIDO  ******************")
    print(ded)
    print("*********************************************")
    ARB = recorrerArbol(ded)
    print("\n************** EL ARBOL  ******************")
    ARB.printRecursive()




