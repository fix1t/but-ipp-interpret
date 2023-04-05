from abc import ABC, abstractmethod
import sys #arguments

PARAMETER_ERR = 10
IN_FILE_ERR = 11

DEVEL = 1

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
    def createInstruction(self,instruction):
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
    def __init__(self):
        self.source = -1
        self.input = -1
        # check number of arguments
        if not(len(sys.argv) == 2 or len(sys.argv) == 3):
            print("ERR: Invalid number of arguments")
            exit(PARAMETER_ERR)

    def usage(self):
        print("This is a Python script (interpret.py) that interprets an input XML representation of a program and generates output based on the command line parameters. The input XML representation is more loosely defined than the XML generated by the parse.php script, but it is assumed that it does not contain errors. The script supports optional documentation text attributes and various formatted tags. The program's instructions are described in section 5 and are interpreted in ascending order based on the order attribute.\n\nThe script has three parameters:\n--help (common to all scripts),\n--source=file (input file with XML representation of source code),\n--input=file (file with inputs for program interpretation).\n`At least one parameter (--source or --input) must be specified. If one is missing, the data is read from standard input.")
        exit(0)

# TODO nastavit druhy stram na STDIN

    def parseArgument(self, argument):
        argExploded = argument.split('=')
        # expect format x..x=x..x
        if(len(argExploded) != 2):
            if(argExploded[0] == '--help'):
                self.usage()
            print("ERR: Invalid parameter")
            exit(PARAMETER_ERR)
        # open file
        try:
            file = open(argExploded[1], 'r')
        except FileNotFoundError:
            print("ERR: Could not open file.")
            exit(IN_FILE_ERR)
        # assign file to stream
        if(argExploded[0] == '--source' and self.source == -1):
            if(DEVEL):print('[dev]: setting up source filestream ... ')
            self.source = file
        elif(argExploded[0] == '--input' and self.input == -1): 
            if(DEVEL):print('[dev]: setting up input filestream ... ')
            self.input = file
        else:
            print("ERR: Invalid parameter. 1")
            print(argExploded[0])
            exit(PARAMETER_ERR)

    def openStream(self):
        #number of arguments checked in the init
        self.parseArgument(sys.argv[1])
        if(len(sys.argv) == 3):
            self.parseArgument(sys.argv[2])
        
    def closeStream(self):
        if(self.input != -1):
            if(DEVEL):print('[dev]: closing input filestream ... ')
            self.input.close()
        if(self.source != -1):
            if(DEVEL):print('[dev]: closing source filestream ... ')
            self.source.close()
        
    def parseLine(self):
        if(DEVEL):print('[dev]: parsing line ... ')

    def _createInstruction(self):
        if(DEVEL):print('[dev]: creating instruction ... ')

    def _createArgument(self):
        if(DEVEL):print('[dev]: creating Argument ... ')

def main():
    parser = Parser()
    parser.openStream()
    parser.parseLine()
    
    parser.closeStream()

if __name__ == '__main__':
    main()