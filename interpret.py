from abc import ABC, abstractmethod

# Instruction interface
class IInstruction(ABC):
    @abstractmethod
    def doOperation(self):
        pass
    @abstractmethod
    def addArgument(self):
        pass

class Instruction(IInstruction):
    argumentList = []
    def doOperation(self):
        pass
    def addArgument(self,argument):
        self.argumentList.append(argument)

class MOVE(Instruction):
    def doOperation(self):
        pass
class CREATEFRAME(Instruction):
    def doOperation(self):
        pass
class PUSHFRAME(Instruction):
    def doOperation(self):
        pass
class POPFRAME(Instruction):
    def doOperation(self):
        pass
class DEFVAR(Instruction):
    def doOperation(self):
        pass
class CALL(Instruction):
    def doOperation(self):
        pass
class RETURN(Instruction):
    def doOperation(self):
        pass
class PUSHS(Instruction):
    def doOperation(self):
        pass
class POPS(Instruction):
    def doOperation(self):
        pass
class ADD(Instruction):
    def doOperation(self):
        pass
class SUB(Instruction):
    def doOperation(self):
        pass
class MUL(Instruction):
    def doOperation(self):
        pass
class IDIV(Instruction):
    def doOperation(self):
        pass
class LT(Instruction):
    def doOperation(self):
        pass
class GT(Instruction):
    def doOperation(self):
        pass
class EQE(Instruction):
    def doOperation(self):
        pass
class AND(Instruction):
    def doOperation(self):
        pass
class OR(Instruction):
    def doOperation(self):
        pass
class NOT(Instruction):
    def doOperation(self):
        pass
class INT2CHAR(Instruction):
    def doOperation(self):
        pass
class STRI2INT(Instruction):
    def doOperation(self):
        pass
class READ(Instruction):
    def doOperation(self):
        pass
class WRITE(Instruction):
    def doOperation(self):
        pass
class LABEL(Instruction):
    def doOperation(self):
        pass
class JUMP(Instruction):
    def doOperation(self):
        pass
class JUMPIFEQ(Instruction):
    def doOperation(self):
        pass
class JUMPIFNEQ(Instruction):
    def doOperation(self):
        pass
class EXIT(Instruction):
    def doOperation(self):
        pass
class DRPINT(Instruction):
    def doOperation(self):
        pass
class BREAK(Instruction):
    def doOperation(self):
        pass

    


# Factory method for instruction
# Creates instruction class based on the input
class InstructionFactory:
    def createInstruction(self,in
    struction):
        if instruction == 'MOVE':
            return MOVE()
        elif instruction == 'CREATEFRAME':
            return CREATEFRAME()
        elif instruction == 'PUSHFRAME':
            return PUSHFRAME()
        elif instruction == 'POPFRAME':
            return POPFRAME()
        elif instruction == 'DEFVAR':
            return DEFVAR()
        elif instruction == 'CALL':
            return CALL()
        elif instruction == 'RETURN':
            return RETURN()
        elif instruction == 'PUSHS':
            return PUSHS()
        elif instruction == 'POPS':
            return POPS()
        elif instruction == 'ADD':
            return ADD()
        elif instruction == 'SUB':
            return SUB()
        elif instruction == 'MUL':
            return MUL()
        elif instruction == 'IDIV':
            return IDIV()
        elif instruction == 'LT':
            return LT()
        elif instruction == 'GT':
            return GT()
        elif instruction == 'EQE':
            return EQE()
        elif instruction == 'AND':
            return AND()
        elif instruction == 'OR':
            return OR()
        elif instruction == 'NOT':
            return NOT()
        elif instruction == 'INT2CHAR':
            return INT2CHAR()
        elif instruction == 'STRI2INT':
            return STRI2INT()
        elif instruction == 'READ':
            return READ()
        elif instruction == 'WRITE':
            return WRITE()
        elif instruction == 'LABEL':
            return LABEL()
        elif instruction == 'JUMP':
            return JUMP()
        elif instruction == 'JUMPIFEQ':
            return JUMPIFEQ()
        elif instruction == 'JUMPIFNEQ':
            return JUMPIFNEQ()
        elif instruction == 'EXIT':
            return EXIT()
        elif instruction == 'DRPINT':
            return DRPINT()
        elif instruction == 'BREAK':
            return BREAK()

class Parser:
    def parseLine():
        print('[dev]: parsing line ... \n')

    def _createInstruction():
        print('[dev]: creating instruction ... \n')

    def _createArgument():
        print('[dev]: creating Argument ... \n')

